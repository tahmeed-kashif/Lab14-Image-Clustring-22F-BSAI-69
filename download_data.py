import os
import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image
import numpy as np

def download_and_save_cifar10(root_dir='data', num_images=1000):
    """
    Downloads CIFAR-10 and saves a subset of images to disk.
    """
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

    # Download CIFAR-10
    transform = transforms.Compose([transforms.ToTensor()])
    trainset = torchvision.datasets.CIFAR10(root='./temp_data', train=True,
                                            download=True, transform=transform)

    print(f"Saving {num_images} images to {root_dir}...")
    
    classes = trainset.classes
    
    # Create a mapping for labels to use in the classifier later
    labels_map = {}

    for i in range(num_images):
        image, label = trainset[i]
        # Convert tensor to PIL image
        image = transforms.ToPILImage()(image)
        
        # Save image
        filename = f"image_{i}_{classes[label]}.png"
        image.save(os.path.join(root_dir, filename))
        
        labels_map[filename] = classes[label]

    # Save labels to a file for the classifier part
    np.save(os.path.join(root_dir, 'labels.npy'), labels_map)
    print("Done!")

if __name__ == "__main__":
    download_and_save_cifar10()
