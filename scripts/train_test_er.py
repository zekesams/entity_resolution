from entity_resolution import er_features, merged_data, er_classifier


def train():
    erc = er_classifier.EntityResolutionClassifier()
    erc.train(features, labels)
    erc.save("data/erc.model")


def test():
    erc = er_classifier.EntityResolutionClassifier()
    erc.load("data/erc.model")

    feature_model = er_features.EntityResolutionFeatures()
    md = merged_data.MergedData()
    for batch in md.get_merged_data():
        features = feature_model.features(batch)
        is_match = erc.predict(features)
