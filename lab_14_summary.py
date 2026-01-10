import os
import numpy as np
from feature_extraction import FeatureExtractor
from clustering import ImageClusterer
from sklearn.metrics import silhouette_score

def main():
    print("="*50)
    print("LAB 14: COMPLEX COMPUTING ACTIVITY")
    print("PROJECT: IMAGE CLUSTERING & RETRIEVAL SYSTEM")
    print("="*50)

    # 1. Setup
    data_dir = "data"
    if not os.path.exists(data_dir):
        print(f"Error: Data directory '{data_dir}' not found.")
        return

    # 2. Feature Extraction
    print("\n[STEP 1] Feature Extraction (CNN - ResNet18)")
    extractor = FeatureExtractor()
    
    # Extract features for a subset of images to save time for the demo
    all_files = [f for f in os.listdir(data_dir) if f.endswith(('.jpg', '.png'))]
    sample_files = all_files[:20] # Use 20 images for this demo
    
    print(f"Processing {len(sample_files)} images...")
    features = []
    valid_files = []
    
    for f in sample_files:
        path = os.path.join(data_dir, f)
        feat = extractor.extract_features(path)
        if feat is not None:
            features.append(feat)
            valid_files.append(f)
            
    features = np.array(features)
    print(f"Extracted Features Shape: {features.shape}")

    # 3. Clustering
    print("\n[STEP 2] Clustering (K-Means)")
    n_clusters = 3
    clusterer = ImageClusterer(features)
    labels = clusterer.apply_kmeans(n_clusters=n_clusters)
    
    print(f"\nClustering Results (K={n_clusters}):")
    for i in range(n_clusters):
        count = sum(labels == i)
        print(f"Cluster {i}: {count} images")
        # Show a few filenames in this cluster
        cluster_files = [valid_files[j] for j, l in enumerate(labels) if l == i]
        print(f"  - Examples: {cluster_files[:3]}")

    # 4. Evaluation
    print("\n[STEP 3] Evaluation")
    if len(np.unique(labels)) > 1:
        sil_score = silhouette_score(features, labels)
        print(f"Silhouette Score: {sil_score:.4f}")
    else:
        print("Silhouette Score: N/A (Only 1 cluster found)")

    print("\n" + "="*50)
    print("PROJECT EXECUTION COMPLETE")
    print("="*50)

if __name__ == "__main__":
    main()
