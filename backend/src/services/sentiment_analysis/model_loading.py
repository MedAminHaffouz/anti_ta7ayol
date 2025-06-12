# model_loading.py
from transformers import pipeline
import torch

def load_sentiment_classifier():
    return pipeline(
        "sentiment-analysis",
        model="nlptown/bert-base-multilingual-uncased-sentiment",
        top_k=None,  # recommended replacement for return_all_scores=True
        device=0 if torch.cuda.is_available() else -1
    )
