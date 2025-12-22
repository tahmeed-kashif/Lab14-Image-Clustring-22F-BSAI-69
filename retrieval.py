from sklearn.neighbors import NearestNeighbors
import numpy as np

class ImageRetrieval:
    def __init__(self, features, filenames):
        self.features = features
        self.filenames = filenames
        self.nbrs = NearestNeighbors(n_neighbors=10, algorithm='ball_tree').fit(self.features)

    def retrieve_similar(self, query_feature, n_results=5):
        """
        Retrieves n_results most similar images to the query_feature.
        """
        distances, indices = self.nbrs.kneighbors([query_feature], n_neighbors=n_results)
        
        results = []
        for i, idx in enumerate(indices[0]):
            results.append({
                "filename": self.filenames[idx],
                "distance": distances[0][i]
            })
        return results
