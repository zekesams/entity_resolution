from dtsc330_26 import entity_resolution_features, merged_data
from dtsc330_26.classifiers import entity_resolution_classifier


def train():
    # Add your training data here
    erc = entity_resolution_classifier.EntityResolutionClassifier()
    erc.train(features, labels)
    erc.save("data/erc.model")


def test():
    erc = entity_resolution_classifier.EntityResolutionClassifier()
    erc.load("data/erc.model")

    feature_model = entity_resolution_features.EntityResolutionFeatures()
    md = merged_data.MergedData()
    for batch in md.get_merged_data():
        features = feature_model.features(batch)
        is_match = erc.predict(features)
