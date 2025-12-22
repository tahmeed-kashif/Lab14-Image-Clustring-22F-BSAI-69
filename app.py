import streamlit as st
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

from feature_extraction import FeatureExtractor
from clustering import ImageClusterer
from evaluation import evaluate_clustering
from classifier import ImageClassifier
from retrieval import ImageRetrieval

# Page Config
st.set_page_config(page_title="Image Clustering & Retrieval", layout="wide")

# Title
st.title("Image Clustering & Retrieval System")

# Sidebar
st.sidebar.header("Settings")
data_dir = st.sidebar.text_input("Data Directory", "data")

# Initialize Session State
if 'features' not in st.session_state:
    st.session_state['features'] = None
if 'filenames' not in st.session_state:
    st.session_state['filenames'] = None
if 'labels' not in st.session_state:
    st.session_state['labels'] = None

# 1. Load Data & Extract Features
st.header("1. Feature Extraction")
if st.button("Load Data & Extract Features"):
    if os.path.exists(data_dir):
        extractor = FeatureExtractor()
        with st.spinner("Extracting features... This may take a while."):
            features, filenames = extractor.extract_features_from_directory(data_dir)
        
        st.session_state['features'] = features
        st.session_state['filenames'] = filenames
        
        # Try to load labels if they exist
        labels_path = os.path.join(data_dir, 'labels.npy')
        if os.path.exists(labels_path):
            labels_map = np.load(labels_path, allow_pickle=True).item()
            # Align labels with filenames
            labels = [labels_map.get(f, "Unknown") for f in filenames]
            st.session_state['labels'] = labels
            st.success(f"Extracted features for {len(features)} images. Labels loaded.")
        else:
            st.success(f"Extracted features for {len(features)} images. No labels found.")
    else:
        st.error("Data directory not found. Please run 'download_data.py' first.")

if st.session_state['features'] is not None:
    features = st.session_state['features']
    filenames = st.session_state['filenames']
    
    # 2. Clustering
    st.header("2. Clustering")
    cluster_method = st.selectbox("Choose Clustering Method", ["K-Means", "Hierarchical"])
    
    # Dynamic slider max based on number of images
    max_clusters = min(20, len(features))
    if max_clusters < 2:
        st.warning("Not enough images to perform clustering. Please add more images.")
        n_clusters = 1
    else:
        n_clusters = st.slider("Number of Clusters", 2, max_clusters, min(5, max_clusters))
    
    if n_clusters >= 2 and st.button("Run Clustering"):
        clusterer = ImageClusterer(features)
        if cluster_method == "K-Means":
            cluster_labels = clusterer.apply_kmeans(n_clusters)
        else:
            cluster_labels = clusterer.apply_hierarchical(n_clusters)
            
        # Evaluation
        scores = evaluate_clustering(features, cluster_labels)
        st.write("### Clustering Evaluation")
        st.write(f"**Silhouette Score:** {scores['silhouette']:.4f}")
        st.write(f"**Davies-Bouldin Index:** {scores['davies_bouldin']:.4f}")
        
        # Visualization (PCA)
        st.write("### Cluster Visualization (PCA)")
        reduced_features = clusterer.reduce_dimensions(n_components=2)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(reduced_features[:, 0], reduced_features[:, 1], c=cluster_labels, cmap='viridis', alpha=0.6)
        legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
        ax.add_artist(legend1)
        st.pyplot(fig)
        
        # Show sample images from each cluster
        st.write("### Sample Images per Cluster")
        for c in range(n_clusters):
            st.write(f"**Cluster {c}**")
            cluster_indices = [i for i, l in enumerate(cluster_labels) if l == c]
            if cluster_indices:
                cols = st.columns(min(5, len(cluster_indices)))
                for i, idx in enumerate(cluster_indices[:5]):
                    img_path = os.path.join(data_dir, filenames[idx])
                    img = Image.open(img_path)
                    cols[i].image(img, caption=filenames[idx], use_container_width=True)

    # 3. Classification (Optional)
    st.header("3. Classification (Optional)")
    if st.session_state['labels'] is not None:
        classifier_type = st.selectbox("Choose Classifier", ["SVM", "Random Forest"])
        if st.button("Train Classifier"):
            # Filter out 'Unknown' labels if any
            valid_indices = [i for i, l in enumerate(st.session_state['labels']) if l != "Unknown"]
            if not valid_indices:
                st.error("No valid labels found for classification.")
            else:
                X = features[valid_indices]
                y = [st.session_state['labels'][i] for i in valid_indices]
                
                classifier = ImageClassifier(X, y)
                if classifier_type == "SVM":
                    acc = classifier.train_svm()
                else:
                    acc = classifier.train_rf()
                
                st.success(f"Classifier trained with Accuracy: {acc:.4f}")
    else:
        st.info("No labels available for classification.")

    # 4. Retrieval System
    st.header("4. Image Retrieval")
    st.write("Upload an image to find similar images in the dataset.")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        # Display uploaded image
        st.image(uploaded_file, caption='Uploaded Image', width=200)
        
        # Save temp file to extract features
        with open("temp_query.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Extract features
        extractor = FeatureExtractor()
        query_features = extractor.extract_features("temp_query.jpg")
        
        if query_features is not None:
            retriever = ImageRetrieval(features, filenames)
            results = retriever.retrieve_similar(query_features, n_results=6)
            
            st.write("### Similar Images Found:")
            cols = st.columns(5)
            # Skip the first one if it's the same image (distance 0), but here we are uploading a new image so it won't be in the dataset usually.
            # However, if we upload an image from the dataset, the first result will be itself.
            
            for i, res in enumerate(results):
                if i < 5:
                    img_path = os.path.join(data_dir, res['filename'])
                    img = Image.open(img_path)
                    cols[i].image(img, caption=f"{res['filename']}\nDist: {res['distance']:.4f}", use_container_width=True)
        
        # Clean up
        os.remove("temp_query.jpg")

st.sidebar.info("Scaling Note: For large datasets, use Approximate Nearest Neighbors (ANN) libraries like Faiss or Annoy instead of standard NearestNeighbors.")
