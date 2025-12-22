from sklearn.metrics import silhouette_score, davies_bouldin_score

def evaluate_clustering(features, labels):
    """
    Calculates Silhouette Score and Davies-Bouldin Index.
    """
    if len(set(labels)) < 2:
        return {"silhouette": -1, "davies_bouldin": -1}
        
    sil_score = silhouette_score(features, labels)
    db_score = davies_bouldin_score(features, labels)
    
    return {
        "silhouette": sil_score,
        "davies_bouldin": db_score
    }
