from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os
import pickle
from typing import List, Optional

class VectorDB:
    def __init__(self, model: SentenceTransformer,
                 phrases_path: str,
                 index_path: str,
                 metadata_path: str):
        self.model = model
        self.phrases_path = phrases_path
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.metadata = []
        self.index = None
        self.dimension = self.model.get_sentence_embedding_dimension()

    def _read_phrases(self, file_path: str) -> List[str]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist")
        with open(file_path, "r", encoding= "utf-8") as f:
            phrases = [line.strip() for line in f if line.strip()]
        return phrases

    def init_index(self, phrases_file: Optional[str] = None):
        file_path = phrases_file or self.phrases_path
        scam_phrases = self._read_phrases(file_path)

        embeddings = self.model.encode(scam_phrases, convert_to_tensor= False)
        embeddings = np.array(embeddings).astype(np.float32)

        self.index = faiss.IndexHNSWFlat(self.dimension, 32)
        self.index.metric_type= faiss.METRIC_INNER_PRODUCT
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)

        faiss.write_index(self.index, self.index_path)
        self.metadata = scam_phrases
        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def load_index(self):
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            self.index= faiss.read_index(self.index_path)
            with open(self.metadata_path, "rb") as f:
                self.metadata = pickle.load(f)
        else:
            raise FileNotFoundError(f"File {self.index_path} does not exist")

    def add_phrases(self, new_phrases: List[str],
                    append_to_file: bool = True) -> None:

        embeddings = self.model.encode(new_phrases, convert_to_tensor= False)
        embeddings = np.array(embeddings).astype(np.float32)

        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)
        self.metadata.extend(new_phrases)

        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)

        if append_to_file:
            with open(self.phrases_file, 'a', encoding='utf-8') as f:
                for phrase in new_phrases:
                    f.write(phrase + '\n')