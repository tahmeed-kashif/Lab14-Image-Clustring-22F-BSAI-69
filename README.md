# Image Clustering & Retrieval System

An unsupervised machine learning project that organizes images into semantic clusters and provides a content-based image retrieval system.

## 🚀 Features
- **Feature Extraction:** Uses a pre-trained **ResNet18** (CNN) to extract 512-dimensional feature vectors from images.
- **Clustering:** Implements **K-Means** and **Hierarchical Clustering** to group similar images (e.g., cats, dogs, fruits) without labels.
- **Dimensionality Reduction:** Uses **PCA** to visualize high-dimensional clusters in 2D.
- **Image Retrieval:** Find similar images to a query image using Euclidean distance.
- **Interactive UI:** Built with **Streamlit** for easy interaction and visualization.

## 📂 Project Structure
- `app.py`: Main Streamlit application.
- `feature_extraction.py`: Logic for extracting features using PyTorch/ResNet.
- `clustering.py`: K-Means and Hierarchical clustering implementations.
- `download_real_samples.py`: Script to download and augment the dataset.
- `lab_14_summary.py`: Summary script for execution metrics.

## 🛠️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Image_Clustering_Project.git
   cd Image_Clustering_Project
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download Dataset:**
   ```bash
   python download_real_samples.py
   ```
   *This will download ~1000 images of cats, dogs, fruits, etc.*

4. **Run the App:**
   ```bash
   streamlit run app.py
   ```

## 📊 Results
The system effectively separates distinct categories (e.g., Apples vs. Lions) using unsupervised learning.
- **Silhouette Score:** ~0.27 (varies with dataset)
- **Clustering Method:** K-Means (K=7 recommended for full dataset)

## 📝 License
This project is for educational purposes.
