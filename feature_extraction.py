import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import os
import numpy as np

class FeatureExtractor:
    def __init__(self):
        # Load pretrained ResNet18
        self.model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        # Remove the classification layer (last fully connected layer)
        self.model = torch.nn.Sequential(*(list(self.model.children())[:-1]))
        self.model.eval()
        
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                 std=[0.229, 0.224, 0.225])
        ])

    def extract_features(self, image_path):
        """
        Extracts features from an image file.
        """
        try:
            image = Image.open(image_path).convert('RGB')
            image = self.transform(image).unsqueeze(0)
            
            with torch.no_grad():
                features = self.model(image)
            
            # Flatten the features
            return features.flatten().numpy()
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return None

    def extract_features_from_directory(self, directory):
        """
        Extracts features for all images in a directory.
        """
        features_list = []
        filenames = []
        
        files = [f for f in os.listdir(directory) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        print(f"Extracting features from {len(files)} images...")
        
        for i, filename in enumerate(files):
            if i % 100 == 0:
                print(f"Processed {i}/{len(files)}")
            
            path = os.path.join(directory, filename)
            features = self.extract_features(path)
            
            if features is not None:
                features_list.append(features)
                filenames.append(filename)
                
        return np.array(features_list), filenames

if __name__ == "__main__":
    extractor = FeatureExtractor()
    # Test on a dummy image if needed, or run main extraction logic
