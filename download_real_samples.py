import os
import requests
import numpy as np
import shutil
import time
from PIL import Image, ImageOps

def download_image(url, save_path):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
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
    Creates augmented copies of the image (Flip, Rotate, Grayscale)
    to artificially increase dataset size.
    """
    try:
        img = Image.open(file_path)
        new_files = []
        
        # 1. Flip
        img_flip = ImageOps.mirror(img)
        flip_name = f"image_{base_count}_flip_{label}.jpg"
        img_flip.save(os.path.join(root_dir, flip_name))
        new_files.append(flip_name)
        
        # 2. Rotate
        img_rot = img.rotate(15)
        rot_name = f"image_{base_count}_rot_{label}.jpg"
        img_rot.save(os.path.join(root_dir, rot_name))
        new_files.append(rot_name)
        
        # 3. Grayscale
        img_gray = ImageOps.grayscale(img)
        gray_name = f"image_{base_count}_gray_{label}.jpg"
        img_gray.save(os.path.join(root_dir, gray_name))
        new_files.append(gray_name)
        
        return new_files
    except Exception as e:
        print(f"Augmentation failed for {file_path}: {e}")
        return []

def setup_real_data():
    root_dir = 'data'
    
    # 1. Clear existing data
    if os.path.exists(root_dir):
        print("Clearing old data...")
        shutil.rmtree(root_dir)
    os.makedirs(root_dir)

    print("Downloading images and applying Data Augmentation...")
    
    samples = {
        "apple": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Red_Apple.jpg/320px-Red_Apple.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Fuji_apple.jpg/320px-Fuji_apple.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Pink_Lady_apples_%284589886707%29.jpg/320px-Pink_Lady_apples_%284589886707%29.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Honeycrisp.jpg/320px-Honeycrisp.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Honeycrisp-Apple.jpg/320px-Honeycrisp-Apple.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Fresh_Apple.jpg/320px-Fresh_Apple.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Apple_braeburn_2009.jpg/320px-Apple_braeburn_2009.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Santana_apple.jpg/320px-Santana_apple.jpg"
        ],
        "cat": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/320px-Cat03.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Cat_November_2010-1a.jpg/320px-Cat_November_2010-1a.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Kittyply_edit1.jpg/320px-Kittyply_edit1.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Sleeping_cat_on_her_back.jpg/320px-Sleeping_cat_on_her_back.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Orange_tabby_cat_sitting_on_fallen_leaves-Hisashi-01A.jpg/320px-Orange_tabby_cat_sitting_on_fallen_leaves-Hisashi-01A.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Grumpy_Cat_%2814556024763%29_%28cropped%29.jpg/320px-Grumpy_Cat_%2814556024763%29_%28cropped%29.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Cat_poster_1.jpg/320px-Cat_poster_1.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/June_odd-eyed-cat.jpg/320px-June_odd-eyed-cat.jpg"
        ],
        "banana": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Banana-Single.jpg/320px-Banana-Single.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Bananas_white_background_DS.jpg/320px-Bananas_white_background_DS.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Banana_and_cross_section.jpg/320px-Banana_and_cross_section.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Bananas_white_background.jpg/320px-Bananas_white_background.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Cavendish_Banana_DS.jpg/320px-Cavendish_Banana_DS.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Bananas.jpg/320px-Bananas.jpg"
        ],
        "lion": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Lion_waiting_in_Namibia.jpg/320px-Lion_waiting_in_Namibia.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Okonjima_Lioness.jpg/320px-Okonjima_Lioness.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Lion_d%27Afrique.jpg/320px-Lion_d%27Afrique.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Lion_s%27stretching.jpg/320px-Lion_s%27stretching.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Sultan_the_Barbary_Lion.jpg/320px-Sultan_the_Barbary_Lion.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Lion_%28Panthera_leo%29_male_6_years_old.jpg/320px-Lion_%28Panthera_leo%29_male_6_years_old.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/African_Lion_Panthera_leo_Male_Pittsburgh_2800px.jpg/320px-African_Lion_Panthera_leo_Male_Pittsburgh_2800px.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Lioness_Etosha_NP.jpg/320px-Lioness_Etosha_NP.jpg"
        ]
    }

    labels_map = {}
    count = 0

    for label, urls in samples.items():
        print(f"Processing {label}...")
        for i, url in enumerate(urls):
            filename = f"image_{count}_{label}.jpg"
            save_path = os.path.join(root_dir, filename)
            
            if download_image(url, save_path):
                labels_map[filename] = label
                
                # Apply Augmentation (Create 3 copies: Flip, Rotate, Gray)
                # This turns 1 download into 4 images
                augmented_files = augment_image(save_path, root_dir, label, count)
                for aug_file in augmented_files:
                    labels_map[aug_file] = label
                
                print(f"Downloaded & Augmented: {filename} (+{len(augmented_files)} copies)")
                count += 1
                time.sleep(0.5) 
            else:
                print(f"Skipped {filename}")

    # Save labels
    np.save(os.path.join(root_dir, 'labels.npy'), labels_map)
    print(f"Done! Total images in dataset: {len(labels_map)}")
    print("You can now run the app and click 'Load Data' to see the new images.")

if __name__ == "__main__":
    setup_real_data()
