import os
import shutil
import random

# --- Configuration ---
DATASET_A = "realistic_word_dataset"  # Path to first dataset
DATASET_B = "clean_printed_dataset"      # Path to second dataset
MERGED_DATASET = "merged_final_dataset"   # Path to the new folder
SAMPLES_PER_WORD = 100  # Total samples you want in the new folder per word

os.makedirs(MERGED_DATASET, exist_ok=True)

# Get list of words (assuming folder names are the same in both)
words = os.listdir(DATASET_A)

for word in words:
    path_a = os.path.join(DATASET_A, word)
    path_b = os.path.join(DATASET_B, word)
    
    # Check if the word folder exists in both datasets
    if os.path.isdir(path_a) and os.path.isdir(path_b):
        target_dir = os.path.join(MERGED_DATASET, word)
        os.makedirs(target_dir, exist_ok=True)
        
        # Get list of all images in both folders
        images_a = [f for f in os.listdir(path_a) if f.endswith(('.png', '.jpg', '.jpeg'))]
        images_b = [f for f in os.listdir(path_b) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        # Shuffle to pick random samples
        random.shuffle(images_a)
        random.shuffle(images_b)
        
        # Select 50% from each (e.g., 150 from A, 150 from B)
        half = SAMPLES_PER_WORD // 2
        selected_a = images_a[:half]
        selected_b = images_b[:half]
        
        print(f"Mixing word: {word} ({len(selected_a)} from A, {len(selected_b)} from B)")

        # Copy images from A
        for img_name in selected_a:
            shutil.copy(os.path.join(path_a, img_name), os.path.join(target_dir, f"A_{img_name}"))
            
        # Copy images from B
        for img_name in selected_b:
            shutil.copy(os.path.join(path_b, img_name), os.path.join(target_dir, f"B_{img_name}"))

print(f"\nSuccess! Mixed dataset created at: {MERGED_DATASET}")