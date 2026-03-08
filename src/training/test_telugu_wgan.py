
import torch
import torch.nn as nn
from torchvision import transforms
import matplotlib.pyplot as plt
import numpy as np
import os
import json

# --- CONFIGURATION ---
RESULTS_DIR = "results_telugu_all"
# Matching the training script's save name
MODEL_PATH = os.path.join(RESULTS_DIR, "best_telugu_all_gen.pth") 
MAPPING_FILE = "telugu_class_mapping.json"

IMG_SIZE = 64
LATENT_DIM = 256 # Updated to match training
EMBED_DIM = 120  # Updated to match training
CHANNELS = 1
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- MODEL (Must match training structure) ---
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

def load_mapping(mapping_file):
    with open(mapping_file, 'r', encoding='utf-8') as f:
        full_mapping = json.load(f)
    
    # EXACT same sorting logic as training script to ensure indices align
    sorted_keys = sorted(full_mapping.keys(), key=lambda x: int(x))
    
    idx_to_char = {}
    for idx, key in enumerate(sorted_keys):
        idx_to_char[idx] = full_mapping[key]['char']
        
    return idx_to_char

def test():
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model not found at {MODEL_PATH}")
        print("Training might still be in progress or failed.")
        return

    # Load Mapping
    idx_to_char = load_mapping(MAPPING_FILE)
    num_classes = len(idx_to_char)
    print(f"Loaded mapping for {num_classes} classes.")

    gen = Generator(num_classes).to(DEVICE)
    
    try:
        gen.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
        gen.eval()
        print(f"Model loaded successfully from {MODEL_PATH}")
    except Exception as e:
        print(f"Failed to load model: {e}")
        return
    
    # Generate samples
    # Let's generate a grid for ALL classes (or a subset if too many)
    # 51 classes -> 6x9 grid approx
    
    fixed_z = torch.randn(num_classes, LATENT_DIM).to(DEVICE)
    fixed_labels = torch.arange(num_classes).to(DEVICE)
    
    with torch.no_grad():
        fake_imgs = gen(fixed_z, fixed_labels).cpu()
        
        # Calculate grid size
        grid_rows = int(np.ceil(np.sqrt(num_classes)))
        grid_cols = int(np.ceil(num_classes / grid_rows))
        
        fig, axes = plt.subplots(grid_rows, grid_cols, figsize=(15, 15))
        axes = axes.flatten()
        
        for idx in range(num_classes):
            img = fake_imgs[idx].squeeze().numpy()
            img = (img * 0.5) + 0.5
            
            axes[idx].imshow(img, cmap='gray')
            axes[idx].set_title(f"{idx}: {idx_to_char[idx]}", fontname="Nirmala UI", fontsize=8) 
            axes[idx].axis('off')
            
        # Hide empty axes
        for idx in range(num_classes, len(axes)):
            axes[idx].axis('off')

        save_path = "telugu_generated_all.png"
        plt.tight_layout()
        plt.savefig(save_path)
        print(f"Saved generated characters to {save_path}")
        plt.show()

if __name__ == "__main__":
    test()
