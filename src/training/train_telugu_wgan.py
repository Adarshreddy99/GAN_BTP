
import os
import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import torch.autograd as autograd

# --- CONFIGURATION ---
DATA_DIR = "telugu_gan_dataset"
MAPPING_FILE = "telugu_class_mapping.json"
RESULTS_DIR = "results_telugu_all"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Increased Robustness
IMG_SIZE = 64
LATENT_DIM = 256 # Increased for more variety
EMBED_DIM = 120  # Increased for class information
BATCH_SIZE = 32
CHANNELS = 1 # Grayscale
LR_G = 0.0001
LR_D = 0.0004
B1 = 0.0
B2 = 0.9
EPOCHS = 200 # Adjustable
SAMPLES_PER_CLASS = 200
LAMBDA_GP = 10
PATIENCE = 50 
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- DATASET ---
class TeluguAllDataset(Dataset):
    def __init__(self, data_dir, mapping_file, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.samples = []
        self.class_map = {} # local_idx -> char
        
        # 1. Load Full Mapping
        with open(mapping_file, 'r', encoding='utf-8') as f:
            self.full_mapping = json.load(f)
            
        # 2. Iterate ALL entries in mapping
        print(f"Loading full dataset from {len(self.full_mapping)} classes...")
        
        found_classes = 0
        
        # The JSON uses "0", "1"... as keys. We will use these as our labels directly if possible, 
        # but let's re-enumerate to be safe (0..N-1)
        # Sort by key to ensure deterministic order "0", "1", "10", etc. might become "0", "1", "10"...
        # Actually keys are strings "0", "1". 
        # Let's sort numerically.
        sorted_keys = sorted(self.full_mapping.keys(), key=lambda x: int(x))
        
        for idx, key in enumerate(sorted_keys):
            entry = self.full_mapping[key]
            folder_name = entry['folder_name']
            char = entry['char']
            
            self.class_map[idx] = char
            folder_path = os.path.join(data_dir, folder_name)
            
            if os.path.exists(folder_path):
                files = sorted([f for f in os.listdir(folder_path) if f.endswith('.png')])
                # Limit samples if needed, but for "all" maybe we just check if empty
                if len(files) > 0:
                    files = files[:SAMPLES_PER_CLASS]
                    for f in files:
                        self.samples.append((os.path.join(folder_path, f), idx))
                    found_classes += 1
            else:
                print(f"  Warning: Folder {folder_name} (Class {key}: {char}) not found.")
                
        print(f"Dataset Loaded: {len(self.samples)} samples across {found_classes} classes.")
        self.num_classes = found_classes

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        try:
            image = Image.open(img_path).convert('L')
            if image.size != (IMG_SIZE, IMG_SIZE):
                image = image.resize((IMG_SIZE, IMG_SIZE), Image.BICUBIC)
            if self.transform:
                image = self.transform(image)
            return image, label
        except Exception as e:
            print(f"Error loading {img_path}: {e}")
            # Return a black image or handle error? Usually cleaner to skip but Dataset requires item.
            # Return dummy
            return torch.zeros((1, IMG_SIZE, IMG_SIZE)), label

# --- MODELS (ROBUST) ---
class Generator(nn.Module):
    def __init__(self, num_classes):
        super(Generator, self).__init__()
        self.label_emb = nn.Embedding(num_classes, EMBED_DIM)
        # Deep: 512 channels base
        self.init_linear = nn.Linear(LATENT_DIM + EMBED_DIM, 512 * 4 * 4) 
        
        self.conv_blocks = nn.Sequential(
            nn.BatchNorm2d(512),
            # 4x4 -> 8x8
            nn.ConvTranspose2d(512, 256, 4, stride=2, padding=1),
            nn.BatchNorm2d(256), nn.ReLU(True),
            # 8x8 -> 16x16
            nn.ConvTranspose2d(256, 128, 4, stride=2, padding=1),
            nn.BatchNorm2d(128), nn.ReLU(True),
            # 16x16 -> 32x32
            nn.ConvTranspose2d(128, 64, 4, stride=2, padding=1),
            nn.BatchNorm2d(64), nn.ReLU(True),
            # 32x32 -> 64x64
            nn.ConvTranspose2d(64, CHANNELS, 4, stride=2, padding=1),
            nn.Tanh()
        )

    def forward(self, z, labels):
        c = self.label_emb(labels)
        x = torch.cat([z, c], 1)
        x = self.init_linear(x).view(-1, 512, 4, 4)
        return self.conv_blocks(x)

class Critic(nn.Module):
    def __init__(self, num_classes):
        super(Critic, self).__init__()
        self.label_emb = nn.Embedding(num_classes, IMG_SIZE * IMG_SIZE)
        
        self.model = nn.Sequential(
            # 64x64 -> 32x32
            nn.Conv2d(CHANNELS + 1, 64, 4, stride=2, padding=1), 
            nn.LeakyReLU(0.2, inplace=True),
            
            # 32x32 -> 16x16
            nn.Conv2d(64, 128, 4, stride=2, padding=1),
            nn.LayerNorm([128, 16, 16]),
            nn.LeakyReLU(0.2, inplace=True),
            
            # 16x16 -> 8x8
            nn.Conv2d(128, 256, 4, stride=2, padding=1),
            nn.LayerNorm([256, 8, 8]),
            nn.LeakyReLU(0.2, inplace=True),
            
            # 8x8 -> 4x4
            nn.Conv2d(256, 512, 4, stride=2, padding=1),
            nn.LayerNorm([512, 4, 4]),
            nn.LeakyReLU(0.2, inplace=True),
            
            nn.Flatten(),
            nn.Linear(512 * 4 * 4, 1) # Critics output scalar score
        )

    def forward(self, img, labels):
        c = self.label_emb(labels).view(-1, 1, IMG_SIZE, IMG_SIZE)
        x = torch.cat([img, c], 1)
        return self.model(x)

# --- UTILS ---
def compute_gradient_penalty(critic, real_samples, fake_samples, labels):
    alpha = torch.rand(real_samples.size(0), 1, 1, 1).to(DEVICE) # Sample random alpha
    interpolates = (alpha * real_samples + ((1 - alpha) * fake_samples)).requires_grad_(True)
    d_interpolates = critic(interpolates, labels)
    fake = torch.ones(real_samples.size(0), 1).to(DEVICE)
    gradients = autograd.grad(
        outputs=d_interpolates,
        inputs=interpolates,
        grad_outputs=fake,
        create_graph=True,
        retain_graph=True,
        only_inputs=True,
    )[0]
    gradients = gradients.view(gradients.size(0), -1)
    gradient_penalty = ((gradients.norm(2, dim=1) - 1) ** 2).mean()
    return gradient_penalty

def train():
    transform = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.5], [0.5])
    ])

    dataset = TeluguAllDataset(DATA_DIR, MAPPING_FILE, transform=transform)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True, drop_last=True)
    
    num_classes = dataset.num_classes
    print(f"Training on {num_classes} classes.")
    
    gen = Generator(num_classes).to(DEVICE)
    critic = Critic(num_classes).to(DEVICE)
    
    opt_g = optim.Adam(gen.parameters(), lr=LR_G, betas=(B1, B2))
    opt_d = optim.Adam(critic.parameters(), lr=LR_D, betas=(B1, B2))
    
    # Progress: Generate a few samples (e.g. first 12 chars)
    eval_classes = min(num_classes, 25)
    fixed_z = torch.randn(eval_classes, LATENT_DIM).to(DEVICE)
    fixed_labels = torch.arange(eval_classes).to(DEVICE)
    
    best_g_loss = float('inf')
    stop_counter = 0
    
    print(f"Starting Robust WGAN Training on {DEVICE}...")
    
    for epoch in range(EPOCHS):
        epoch_g_loss_sum = 0
        steps_g = 0
        
        pbar = tqdm(dataloader, desc=f"Epoch {epoch+1}/{EPOCHS}")
        
        for i, (real_imgs, labels) in enumerate(pbar):
            real_imgs = real_imgs.to(DEVICE)
            labels = labels.to(DEVICE)
            batch_sz = real_imgs.size(0)
            
            # --- Train Critic ---
            opt_d.zero_grad()
            z = torch.randn(batch_sz, LATENT_DIM).to(DEVICE)
            fake_imgs = gen(z, labels).detach()
            
            real_validity = critic(real_imgs, labels)
            fake_validity = critic(fake_imgs, labels)
            
            gp = compute_gradient_penalty(critic, real_imgs, fake_imgs, labels)
            d_loss = -torch.mean(real_validity) + torch.mean(fake_validity) + LAMBDA_GP * gp
            d_loss.backward()
            opt_d.step()
            
            g_loss_val = 0
            # --- Train Generator ---
            if i % 5 == 0:
                opt_g.zero_grad()
                gen_imgs = gen(z, labels)
                fake_validity = critic(gen_imgs, labels)
                g_loss = -torch.mean(fake_validity)
                g_loss.backward()
                opt_g.step()
                
                g_loss_val = g_loss.item()
                epoch_g_loss_sum += g_loss_val
                steps_g += 1
            
            pbar.set_postfix(d_loss=f"{d_loss.item():.4f}", g_loss=f"{g_loss_val:.4f}")

        # Early Stopping Check
        avg_g_loss = epoch_g_loss_sum / max(steps_g, 1)
        print(f"Epoch {epoch+1} Avg G Loss: {avg_g_loss:.4f}")

        if avg_g_loss < best_g_loss:
            best_g_loss = avg_g_loss
            stop_counter = 0
            torch.save(gen.state_dict(), os.path.join(RESULTS_DIR, "best_telugu_all_gen.pth"))
            torch.save(critic.state_dict(), os.path.join(RESULTS_DIR, "best_telugu_all_critic.pth"))
        else:
            stop_counter += 1
            if stop_counter >= PATIENCE:
                print(f"Early Stopping Triggered at Epoch {epoch+1}")
                break

        # Save Progress Images
        if (epoch+1) % 5 == 0:
            with torch.no_grad():
                gen.eval()
                fake = gen(fixed_z, fixed_labels).detach().cpu()
                
                # Grid size depends on eval_classes. Let's do 5x5 max
                grid_size = int(np.ceil(np.sqrt(eval_classes)))
                fig, axes = plt.subplots(grid_size, grid_size, figsize=(10, 10))
                axes = axes.flatten()
                
                for idx in range(eval_classes):
                    if idx < len(fake):
                        img = fake[idx].squeeze().numpy()
                        img = (img * 0.5) + 0.5
                        axes[idx].imshow(img, cmap='gray')
                        axes[idx].set_title(str(idx))
                        axes[idx].axis('off')
                
                # Hide unused axes
                for idx in range(eval_classes, len(axes)):
                    axes[idx].axis('off')

                plt.tight_layout()
                plt.savefig(os.path.join(RESULTS_DIR, f"progress_all_epoch_{epoch+1}.png"))
                plt.close()
                gen.train()

    print("Training Complete!")

if __name__ == "__main__":
    train()
