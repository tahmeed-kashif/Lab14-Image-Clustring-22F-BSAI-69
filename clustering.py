from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
import numpy as np

class ImageClusterer:
    def __init__(self, features):
        self.features = features
        self.kmeans_model = None
        self.hierarchical_model = None

    def apply_kmeans(self, n_clusters=5):
        """
        Applies K-Means clustering.
        """
        print(f"Running K-Means with {n_clusters} clusters...")
        self.kmeans_model = KMeans(n_clusters=n_clusters, random_state=42)
        labels = self.kmeans_model.fit_predict(self.features)
        return labels

    def apply_hierarchical(self, n_clusters=5):
        """
        Applies Hierarchical (Agglomerative) clustering.
        """
        print(f"Running Hierarchical clustering with {n_clusters} clusters...")
        self.hierarchical_model = AgglomerativeClustering(n_clusters=n_clusters)
        labels = self.hierarchical_model.fit_predict(self.features)
        return labels

    def reduce_dimensions(self, n_components=2):
        """
        Reduces dimensions for visualization using PCA.
        """
        pca = PCA(n_components=n_components)
        reduced_features = pca.fit_transform(self.features)
        return reduced_features
