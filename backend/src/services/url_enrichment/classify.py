import numpy as np
import pandas as pd
from .extract_url_data import extract_url_features

from xgboost import XGBClassifier

def classify_url(url: str, model: XGBClassifier) -> float:
    url_features = extract_url_features(url)

    input = pd.DataFrame([url_features])
    score = model.predict_proba(input)
    return np.squeeze(score)[1]

if __name__ == '__main__':
    from .model import load_model
    import sys

    model_path = sys.argv[1]
    model = load_model(model_path)

    print(classify_url("https://en.wikipedia.org/wiki/Main_Page", model))

