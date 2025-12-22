from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

class ImageClassifier:
    def __init__(self, features, labels):
        self.features = features
        self.labels = labels
        self.model = None

    def train_svm(self):
        """
        Trains an SVM classifier.
        """
        print("Training SVM...")
        X_train, X_test, y_train, y_test = train_test_split(self.features, self.labels, test_size=0.2, random_state=42)
        
        self.model = SVC(kernel='linear', probability=True)
        self.model.fit(X_train, y_train)
        
        predictions = self.model.predict(X_test)
        acc = accuracy_score(y_test, predictions)
        print(f"SVM Accuracy: {acc}")
        print(classification_report(y_test, predictions))
        
        return acc

    def train_rf(self):
        """
        Trains a Random Forest classifier.
        """
        print("Training Random Forest...")
        X_train, X_test, y_train, y_test = train_test_split(self.features, self.labels, test_size=0.2, random_state=42)
        
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        predictions = self.model.predict(X_test)
        acc = accuracy_score(y_test, predictions)
        print(f"Random Forest Accuracy: {acc}")
        print(classification_report(y_test, predictions))
        
        return acc

    def predict(self, feature_vector):
        if self.model:
            return self.model.predict([feature_vector])[0]
        return None
