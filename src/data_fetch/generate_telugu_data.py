import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

# ==========================================
# CONFIGURATION
# ==========================================
OUTPUT_DIR = "telugu_gan_dataset"
FONT_PATH = "telugu_font.ttf"  # Ensure this file exists in the directory
NUM_SAMPLES = 300              # Images per letter
IMG_SIZE = 64                  # 64x64 is standard for simple GANs (DCGAN)
FONT_SIZE_BASE = 40            # Base font size (approx 60-70% of IMG_SIZE)

# Augmentation Limits (Little variations)
ROTATION_RANGE = 12            # Degrees +/-
TRANSLATION_RANGE = 4          # Pixels +/-
SCALE_RANGE = 4                # Point size +/-
NOISE_INTENSITY = 0.02         # Factor for salt-and-pepper noise

# ==========================================
# TELUGU CHARACTER SET
# ==========================================
# Vowels (Achulu)
VOWELS = [
    'అ', 'ఆ', 'ఇ', 'ఈ', 'ఉ', 'ఊ', 'ఋ',
    'ఎ', 'ఏ', 'ఐ', 'ఒ', 'ఓ', 'ఔ', 'అం', 'అః'
]

# Consonants (Hallulu)
CONSONANTS = [
    'క', 'ఖ', 'గ', 'ఘ', 'ఙ',
    'చ', 'ఛ', 'జ', 'ఝ', 'ఞ',
    'ట', 'ఠ', 'డ', 'ఢ', 'ణ',
    'త', 'థ', 'ద', 'ధ', 'న',
    'ప', 'ఫ', 'బ', 'భ', 'మ',
    'య', 'ర', 'ల', 'వ', 'శ', 'ష', 'స', 'హ',
    'ళ', 'క్ష', 'ఱ'
]

ALL_CHARS = VOWELS + CONSONANTS

def add_noise(image, intensity=0.02):
    """Adds random salt-and-pepper noise to the image."""
    img_array = np.array(image)
    
    # Random noise mask
    noise = np.random.rand(*img_array.shape)
    
    # Salt (White)
    img_array[noise < (intensity / 2)] = 255
    # Pepper (Black)
    img_array[noise > (1 - intensity / 2)] = 0
    
    return Image.fromarray(img_array)

def generate_sample(char, font_path, sample_id, save_dir):
    """Generates a single augmented image for a character."""
    
    # 1. Randomize Parameters
    current_font_size = FONT_SIZE_BASE + random.randint(-SCALE_RANGE, SCALE_RANGE)
    angle = random.uniform(-ROTATION_RANGE, ROTATION_RANGE)
    offset_x = random.randint(-TRANSLATION_RANGE, TRANSLATION_RANGE)
    offset_y = random.randint(-TRANSLATION_RANGE, TRANSLATION_RANGE)
    
    try:
        font = ImageFont.truetype(font_path, current_font_size)
    except OSError:
        print(f"Error: Could not open font file at {font_path}. Please check the path.")
        exit()

    # 2. Create Canvas (Black text on White bg is standard, or inverse)
    # Using L mode (Grayscale)
    image = Image.new('L', (IMG_SIZE, IMG_SIZE), color=255) # White background
    draw = ImageDraw.Draw(image)
    
    # 3. Calculate Text Size to center it roughly
    # (bbox is left, top, right, bottom)
    bbox = draw.textbbox((0, 0), char, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    # Center position + random offset
    x = (IMG_SIZE - text_w) / 2 + offset_x
    y = (IMG_SIZE - text_h) / 2 + offset_y
    
    # 4. Draw Text
    draw.text((x, y), char, font=font, fill=0) # Black text
    
    # 5. Apply Rotation (with white fill for empty corners)
    image = image.rotate(angle, resample=Image.BICUBIC, fillcolor=255)
    
    # 6. Apply Noise (Optional: Helps GAN generalize)
    image = add_noise(image, intensity=NOISE_INTENSITY)

    # 7. Save
    filename = f"{sample_id:03d}.png"
    image.save(os.path.join(save_dir, filename))

def main():
    if not os.path.exists(FONT_PATH):
        print(f"CRITICAL ERROR: Font file '{FONT_PATH}' not found.")
        return

    print(f"Generating dataset in '{OUTPUT_DIR}'...")
    print(f"Total Characters: {len(ALL_CHARS)}")
    
    for char in ALL_CHARS:
        # --- FIXED SECTION START ---
        # If char has length 1, use simple hex (e.g., C05)
        # If char has length > 1, join hex codes with underscore (e.g., C05_C02)
        folder_name = "_".join([f"{ord(c):X}" for c in char])
        # --- FIXED SECTION END ---

        char_dir = os.path.join(OUTPUT_DIR, folder_name)
        os.makedirs(char_dir, exist_ok=True)
        
        print(f"Generating {NUM_SAMPLES} samples for: {char} (Folder: {folder_name})")
        
        for i in range(NUM_SAMPLES):
            generate_sample(char, FONT_PATH, i, char_dir)
            
    print("\nDataset generation complete!")

if __name__ == "__main__":
    main()