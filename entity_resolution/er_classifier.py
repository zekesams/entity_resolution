"""
This is a classifier for an entity resolution problem linking PubMed article authors and grantees.
It will train and make a probabilistic prediction.
"""

import numpy as np
import sklearn


class EntityResolutionClassifier:
    def __init__(self, model_type: str = "logistic_regression"):
        """Create a reusable classifier

        Args:
            model_type (str): model type can be either logistic_regression or random_forest. 
            Defaults to 'logistic_regression'.
        """
        self.model = None

    def train(self, features, labels):
        """ Train model taking in features and labels from training data as input
        
        Args:
            features: 
            labels: entity match or non match
        """
        if self.model_type == "logistic_regression":
            self.model = sklearn.linear_model.LogisticRegression()
        elif self.model_type == "random_forest":
            self.model = sklearn.ensemble.RandomForestClassifier()
        
        self.model.fit(features,labels.astype(int))

    def predict(self, features):
        """Predict labels using model_type from features

        Args:
            features (_type_): Features MUST be the same types as in
                the training data, and in the same order
        """
        features = self.scaler.transform(features)
        return self.model.predict_proba(features)[:, 1]


if __name__ == "__main__":
    er_classifier = EntityResolutionClassifier() 