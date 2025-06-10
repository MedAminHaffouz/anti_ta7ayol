from sentence_transformers import SentenceTransformer
import torch
from sentence_transformers.util import cos_sim

def classify_score(model: SentenceTransformer, input_text: str, scam_dataset: list) -> float:
    input_embedding = model.encode([input_text], convert_to_tensor=True)
    scam_embeddings = model.encode(scam_dataset, convert_to_tensor=True)

    similarities = cos_sim(input_embedding, scam_embeddings)
    score = torch.max(similarities).item()
    return score