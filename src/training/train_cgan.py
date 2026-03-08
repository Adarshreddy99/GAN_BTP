import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from torch.nn.utils import spectral_norm
import torch.autograd as autograd

# --- CONFIG ---
IMG_H, IMG_W = 64, 256
LATENT_DIM = 128 # Increased
NUM_WORDS = 10
BATCH_SIZE = 32
DEVICE = torch.device("cpu")
# TTUR - Different learning rates for G and D
G_LR = 0.0001
D_LR = 0.0004
LAMBDA_GP = 10 # Gradient penalty coefficient

# Results Directory
RESULTS_DIR = "results_cgan"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Data Paths
DATA_A_PATH = r"c:\Users\Adarsh Reddy\Documents\GAN_BTP\data\realistic_word_dataset"
DATA_B_PATH = r"c:\Users\Adarsh Reddy\Documents\GAN_BTP\data\clean_printed_dataset"

SELECTED_WORDS = [
    "believe", "country", "garden", "house", "journey",
    "perfect", "quality", "street", "water", "world"
]

word_to_idx = {word: i for i, word in enumerate(SELECTED_WORDS)}
idx_to_word = {i: word for word, i in word_to_idx.items()}

class HybridWordDataset(Dataset):
    def __init__(self, transform=None):
        self.samples = []
        self.transform = transform
        for word in SELECTED_WORDS:
            label = word_to_idx[word]
            # Load from Source A
            path_a = os.path.join(DATA_A_PATH, word)
            if os.path.exists(path_a):
                files_a = sorted([os.path.join(path_a, f) for f in os.listdir(path_a) if f.endswith('.png')])
                self.samples.extend([(f, label) for f in files_a[:150]])
            # Load from Source B
            path_b = os.path.join(DATA_B_PATH, word)
            if os.path.exists(path_b):
                files_b = sorted([os.path.join(path_b, f) for f in os.listdir(path_b) if f.endswith('.png')])
                self.samples.extend([(f, label) for f in files_b[:150]])
        print(f"Dataset initialized with {len(self.samples)} samples.")

    def __len__(self): return len(self.samples)
    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        image = Image.open(img_path).convert('L')
        if self.transform: image = self.transform(image)
        return image, label

transform = transforms.Compose([
    transforms.Resize((IMG_H, IMG_W)),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])

# --- MODELS ---

class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        self.label_emb = nn.Embedding(NUM_WORDS, 50)
        self.init_linear = nn.Linear(LATENT_DIM + 50, 512 * 4 * 16) # Increased filters
        
        self.conv_blocks = nn.Sequential(
            nn.BatchNorm2d(512),
            nn.ConvTranspose2d(512, 256, 4, stride=2, padding=1),
            nn.BatchNorm2d(256), nn.ReLU(True),
            nn.ConvTranspose2d(256, 128, 4, stride=2, padding=1),
            nn.BatchNorm2d(128), nn.ReLU(True),
            nn.ConvTranspose2d(128, 64, 4, stride=2, padding=1),
            nn.BatchNorm2d(64), nn.ReLU(True),
            nn.ConvTranspose2d(64, 1, 4, stride=2, padding=1),
            nn.Tanh()
        )

    def forward(self, z, labels):
        c = self.label_emb(labels)
        x = torch.cat([z, c], 1)
        x = self.init_linear(x).view(-1, 512, 4, 16)
        return self.conv_blocks(x)

class Critic(nn.Module): # Renamed for WGAN
    def __init__(self):
        super(Critic, self).__init__()
        self.label_emb = nn.Embedding(NUM_WORDS, 1 * IMG_H * IMG_W)
        self.model = nn.Sequential(
            nn.Conv2d(2, 64, 4, stride=2, padding=1),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(64, 128, 4, stride=2, padding=1),
            nn.LayerNorm([128, 16, 64]), # LayerNorm preferred for WGAN-GP
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(128, 256, 4, stride=2, padding=1),
            nn.LayerNorm([256, 8, 32]),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Flatten(),
            nn.Linear(256 * 8 * 32, 1)
        )

    def forward(self, img, labels):
        c = self.label_emb(labels).view(-1, 1, IMG_H, IMG_W)
        x = torch.cat([img, c], 1)
        return self.model(x)

def compute_gradient_penalty(critic, real_samples, fake_samples, labels):
    alpha = torch.rand(real_samples.size(0), 1, 1, 1).to(DEVICE)
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

# --- TRAINING ---

def train():
    dataset = HybridWordDataset(transform=transform)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    
    gen = Generator().to(DEVICE)
    critic = Critic().to(DEVICE)
    
    g_opt = optim.Adam(gen.parameters(), lr=G_LR, betas=(0.0, 0.9)) # Optimized betas for WGAN
    d_opt = optim.Adam(critic.parameters(), lr=D_LR, betas=(0.0, 0.9))

    fixed_z = torch.randn(NUM_WORDS, LATENT_DIM).to(DEVICE)
    fixed_labels = torch.arange(NUM_WORDS).to(DEVICE)

    # Early Stopping Config
    best_g_loss = float('inf')
    early_stop_patience = 50
    stop_counter = 0

    num_epochs = 150
    print(f"Starting WGAN-GP training on {DEVICE}...")

    for epoch in range(num_epochs):
        epoch_g_loss = 0
        pbar = tqdm(dataloader, desc=f"Epoch {epoch+1}/{num_epochs}")
        
        for i, (real_imgs, labels) in enumerate(pbar):
            batch_sz = real_imgs.size(0)
            real_imgs, labels = real_imgs.to(DEVICE), labels.to(DEVICE)
            
            # --- Train Critic ---
            d_opt.zero_grad()
            z = torch.randn(batch_sz, LATENT_DIM).to(DEVICE)
            fake_imgs = gen(z, labels).detach()
            
            real_validity = critic(real_imgs, labels)
            fake_validity = critic(fake_imgs, labels)
            
            gp = compute_gradient_penalty(critic, real_imgs, fake_imgs, labels)
            d_loss = -torch.mean(real_validity) + torch.mean(fake_validity) + LAMBDA_GP * gp
            d_loss.backward()
            d_opt.step()
            
            # --- Train Generator every 5 steps (standard for WGAN) ---
            if i % 1 == 0: # on CPU we can do 1:1, usually 5:1 on GPU
                g_opt.zero_grad()
                gen_imgs = gen(z, labels)
                fake_val = critic(gen_imgs, labels)
                g_loss = -torch.mean(fake_val)
                g_loss.backward()
                g_opt.step()
                epoch_g_loss += g_loss.item()
            
            pbar.set_postfix(d_loss=f"{d_loss.item():.4f}", g_loss=f"{-torch.mean(fake_validity).item():.4f}")

        avg_g_loss = epoch_g_loss / len(dataloader)

        # Early Stopping
        if avg_g_loss < best_g_loss:
            best_g_loss = avg_g_loss
            stop_counter = 0
            torch.save(gen.state_dict(), os.path.join(RESULTS_DIR, "best_generator_wgan.pth"))
        else:
            stop_counter += 1
            if stop_counter >= early_stop_patience:
                print(f"\nEarly stopping at epoch {epoch+1}")
                break
            
        if (epoch + 1) % 10 == 0:
            with torch.no_grad():
                gen.eval()
                sample_imgs = gen(fixed_z, fixed_labels) * 0.5 + 0.5
                save_path = os.path.join(RESULTS_DIR, f"wgan_progress_epoch_{epoch+1}.png")
                fig, axes = plt.subplots(NUM_WORDS, 1, figsize=(10, 15))
                for idx in range(NUM_WORDS):
                    axes[idx].imshow(sample_imgs[idx].squeeze().cpu().numpy(), cmap='gray')
                    axes[idx].set_title(idx_to_word[idx])
                    axes[idx].axis('off')
                plt.tight_layout()
                plt.savefig(save_path)
                plt.close()
                gen.train()

    print(f"Training Complete. Model saved in {RESULTS_DIR}")

if __name__ == "__main__":
    train()
