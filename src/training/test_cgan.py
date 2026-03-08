import os
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

# --- CONFIG ---
IMG_H, IMG_W = 64, 256
LATENT_DIM = 100
NUM_WORDS = 10
DEVICE = torch.device("cpu")
RESULTS_DIR = "results_cgan"
MODEL_PATH = os.path.join(RESULTS_DIR, "best_generator.pth")

# The words we trained on
SELECTED_WORDS = [
    "believe", "country", "garden", "house", "journey",
    "perfect", "quality", "street", "water", "world"
]

# --- MODEL ARCHITECTURE (Must match training) ---
class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        self.label_emb = nn.Embedding(NUM_WORDS, 50)
        self.init_linear = nn.Linear(LATENT_DIM + 50, 256 * 4 * 16)
        
        self.conv_blocks = nn.Sequential(
            nn.BatchNorm2d(256),
            nn.ConvTranspose2d(256, 128, 4, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(True),
            nn.ConvTranspose2d(128, 64, 4, stride=2, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(True),
            nn.ConvTranspose2d(64, 32, 4, stride=2, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(True),
            nn.ConvTranspose2d(32, 1, 4, stride=2, padding=1),
            nn.Tanh()
        )

    def forward(self, z, labels):
        c = self.label_emb(labels)
        x = torch.cat([z, c], 1)
        x = self.init_linear(x).view(-1, 256, 4, 16)
        return self.conv_blocks(x)

def test():
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model not found at {MODEL_PATH}")
        return

    # Initialize and load generator
    gen = Generator().to(DEVICE)
    gen.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    gen.eval()

    # Create inputs
    z = torch.randn(NUM_WORDS, LATENT_DIM).to(DEVICE)
    labels = torch.arange(NUM_WORDS).to(DEVICE)

    # Generate images
    with torch.no_grad():
        sample_imgs = gen(z, labels)
        sample_imgs = sample_imgs * 0.5 + 0.5  # Denormalize

    # Plot and save
    fig, axes = plt.subplots(NUM_WORDS, 1, figsize=(12, 20))
    for idx in range(NUM_WORDS):
        img = sample_imgs[idx].squeeze().cpu().numpy()
        axes[idx].imshow(img, cmap='gray')
        axes[idx].set_title(f"Generated: {SELECTED_WORDS[idx]}", fontsize=14)
        axes[idx].axis('off')

    plt.tight_layout()
    output_path = os.path.join(RESULTS_DIR, "final_test_generation.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Test generation complete! Result saved to: {output_path}")

if __name__ == "__main__":
    test()
