import os
import numpy as np
from PIL import Image, ImageDraw
import random

def generate_synthetic_data(root_dir='data', num_images=200):
    """
    Generates synthetic images with different shapes and colors.
    """
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

    print(f"Generating {num_images} synthetic images in {root_dir}...")
    
    shapes = ['circle', 'rectangle', 'triangle']
    colors = ['red', 'green', 'blue', 'yellow', 'purple']
    
    labels_map = {}

    for i in range(num_images):
        # Create a blank image
        img = Image.new('RGB', (224, 224), color='white')
        draw = ImageDraw.Draw(img)
        
        shape = random.choice(shapes)
        color = random.choice(colors)
        
        # Random position and size
        x0 = random.randint(20, 100)
        y0 = random.randint(20, 100)
        x1 = random.randint(120, 200)
        y1 = random.randint(120, 200)
        
        if shape == 'circle':
            draw.ellipse([x0, y0, x1, y1], fill=color, outline='black')
        elif shape == 'rectangle':
            draw.rectangle([x0, y0, x1, y1], fill=color, outline='black')
        elif shape == 'triangle':
            draw.polygon([(x0, y1), ((x0+x1)//2, y0), (x1, y1)], fill=color, outline='black')
            
        # Save image
        label = f"{color}_{shape}"
        filename = f"image_{i}_{label}.png"
        img.save(os.path.join(root_dir, filename))
        
        labels_map[filename] = label

    # Save labels
    np.save(os.path.join(root_dir, 'labels.npy'), labels_map)
    print("Done!")

if __name__ == "__main__":
    generate_synthetic_data()
