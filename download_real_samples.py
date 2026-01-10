import os
import requests
import numpy as np
import shutil
import time
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import random

def download_image(url, save_path):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        # Add random query param to avoid caching
        if '?' in url:
            url += f"&random={random.random()}"
        else:
            url += f"?random={random.random()}"
            
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
    return False

def augment_image(file_path, root_dir, label, base_count):
    """
    Creates multiple augmented copies to increase dataset size.
    Target: ~10 variations per image.
    """
    try:
        img = Image.open(file_path).convert('RGB')
        new_files = []
        
        # Transformations list
        transformations = [
            ("flip", lambda i: ImageOps.mirror(i)),
            ("rot15", lambda i: i.rotate(15)),
            ("rot_15", lambda i: i.rotate(-15)),
            ("rot30", lambda i: i.rotate(30)),
            ("gray", lambda i: ImageOps.grayscale(i).convert('RGB')),
            ("bright1.2", lambda i: ImageEnhance.Brightness(i).enhance(1.2)),
            ("contrast1.2", lambda i: ImageEnhance.Contrast(i).enhance(1.2)),
            ("blur", lambda i: i.filter(ImageFilter.BLUR)),
            ("noise", lambda i: ImageEffect_noise(i)) # Custom noise function below
        ]

        for suffix, func in transformations:
            new_img = func(img)
            new_name = f"image_{base_count}_{suffix}_{label}.jpg"
            new_img.save(os.path.join(root_dir, new_name))
            new_files.append(new_name)
        
        return new_files
    except Exception as e:
        print(f"Augmentation failed for {file_path}: {e}")
        return []

def ImageEffect_noise(img):
    # Simple noise simulation
    arr = np.array(img)
    noise = np.random.randint(0, 50, arr.shape, dtype='uint8')
    arr = np.clip(arr + noise, 0, 255).astype('uint8')
    return Image.fromarray(arr)

def setup_real_data():
    root_dir = 'data'
    
    # 1. Clear existing data
    if os.path.exists(root_dir):
        print("Clearing old data...")
        shutil.rmtree(root_dir)
    os.makedirs(root_dir)

    print("Downloading images from LoremFlickr and applying Data Augmentation...")
    
    categories = ["cat", "dog", "lion", "bird", "apple", "banana", "watermelon"]
    images_per_category = 15 # 15 base images * (1 + 9 variations) = 150 images per category. Total ~1050 images.
    
    labels_map = {}
    count = 0

    for label in categories:
        print(f"Processing {label}...")
        base_url = f"https://loremflickr.com/320/240/{label}"
        
        for i in range(images_per_category):
            filename = f"image_{count}_{label}.jpg"
            save_path = os.path.join(root_dir, filename)
            
            if download_image(base_url, save_path):
                labels_map[filename] = label
                
                # Apply Augmentation
                augmented_files = augment_image(save_path, root_dir, label, count)
                for aug_file in augmented_files:
                    labels_map[aug_file] = label
                
                print(f"Downloaded & Augmented: {filename} (+{len(augmented_files)} copies)")
                count += 1
                time.sleep(1.0) # Be nice to the server
            else:
                print(f"Skipped {filename}")

    # Save labels
    np.save(os.path.join(root_dir, 'labels.npy'), labels_map)
    print(f"Done! Total images in dataset: {len(labels_map)}")

if __name__ == "__main__":
    setup_real_data()
