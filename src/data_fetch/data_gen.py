import os
import random
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

# --- Configuration ---
SAMPLES_PER_WORD = 300
IMAGE_SIZE = (256, 64) 
OUTPUT_DIR = "printed_dataset"

# 50 Actual Words
ACTUAL_WORDS = [
    "book", "time", "hand", "work", "play", "good", "life", "kind", "city", "road",
    "house", "light", "world", "water", "bread", "large", "small", "study", "heart", "great",
    "school", "family", "father", "mother", "better", "friend", "winter", "summer", "street", "garden",
    "morning", "journey", "quality", "picture", "student", "example", "perfect", "through", "believe", "special",
    "blue", "fast", "love", "home", "paper", "sound", "flower", "forest", "between", "country"
]

def apply_clean_variation(image):
    img = np.array(image)
    
    # 1. Sub-pixel rotation (keeps edges sharp but prevents perfect alignment)
    rows, cols, _ = img.shape
    angle = random.uniform(-0.5, 0.5) 
    M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    img = cv2.warpAffine(img, M, (cols, rows), borderValue=(255, 255, 255), flags=cv2.INTER_LANCZOS4)

    # 2. Very light Gaussian Blur to simulate ink absorption (not distortion)
    img = cv2.GaussianBlur(img, (3, 3), 0.2)

    return Image.fromarray(img)

def generate_dataset():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Attempt to load a real font for clarity
    # Windows: "arial.ttf" | Mac/Linux: "/Library/Fonts/Arial.ttf" or similar
    try:
        font_path = "arial.ttf" # Or change to "Roboto-Regular.ttf"
        font_size = 36 # Much larger for clarity
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("Real font not found. Using default (will be small). Please provide a .ttf file!")
        font = ImageFont.load_default()

    for word in ACTUAL_WORDS:
        word_dir = os.path.join(OUTPUT_DIR, word)
        os.makedirs(word_dir, exist_ok=True)
        print(f"Generating high-quality samples for: {word}")
        
        for i in range(SAMPLES_PER_WORD):
            # Create a high-res canvas
            img = Image.new('RGB', IMAGE_SIZE, color=(255, 255, 255))
            draw = ImageDraw.Draw(img)
            
            # Get text size for centering
            bbox = draw.textbbox((0, 0), word, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            
            # Center with very tiny random jitter for variation
            x = (IMAGE_SIZE[0] - w) / 2 + random.uniform(-2, 2)
            y = (IMAGE_SIZE[1] - h) / 2 + random.uniform(-1, 1)
            
            # Draw text - using a dark grey instead of pure black for a more "printed" look
            draw.text((x, y), word, fill=(30, 30, 30), font=font)
            
            # Apply variations
            final_img = apply_clean_variation(img)
            final_img.save(os.path.join(word_dir, f"{word}_{i}.png"))

if __name__ == "__main__":
    generate_dataset()