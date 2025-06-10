import numpy as np
import faiss
from .vector_db import VectorDB

def classify(vector_db: VectorDB, text: str) -> float:
    model = vector_db.model
    input_embeddings = model.encode([text])
    input_embeddings = np.array(input_embeddings).astype(np.float32)
    faiss.normalize_L2(input_embeddings)
    distances, indices = vector_db.index.search(input_embeddings, k=1)
    max_similarity = distances[0][0]

    return max_similarity

if __name__ == "__main__":
    import sys
    from .model import load_model

    model = load_model(sys.argv[1])
    phrases_path = sys.argv[2]
    index_path = sys.argv[3]
    metadata_path = sys.argv[4]

    vector_db = VectorDB(model, phrases_path, index_path, metadata_path)
    vector_db.load_index()

    claim= "wallah kima nahkilek sahbi"

    score = classify(vector_db, claim)
    print(abs(score))