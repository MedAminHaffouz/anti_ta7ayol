import pickle
from sklearn.pipeline import make_pipeline
import os


#function that loads the model and takes the path to the model as a parameter as simple as that bro
def load_model(model_path: str):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"{model_path} does not exist")
    model_file = os.path.join(model_path, "final_phishing_model.pkl")
    scaler_file = os.path.join(model_path, "scaler.pkl")

    with open(model_file, 'rb') as f:
        model = pickle.load(f)
    with open(scaler_file, 'rb') as f:
        scaler = pickle.load(f)
    pipeline = make_pipeline(scaler, model)
    return pipeline