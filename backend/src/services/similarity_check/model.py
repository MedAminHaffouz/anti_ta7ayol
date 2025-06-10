from sentence_transformers import SentenceTransformer
import os

def save_model(save_path: str) -> None:
    model_name = "paraphrase-multilingual-MiniLM-L12-v2"

    abs_save_path = os.path.abspath(save_path)
    if os.path.exists(abs_save_path):
        return

    try:
        os.makedirs(abs_save_path, exist_ok=True)
        model = SentenceTransformer(model_name)
        model.save(abs_save_path)
        print(f"Model saved successfully to {abs_save_path}")
    except ValueError as ve:
        raise ValueError(f"Invalid model name or configuration: {ve}")
    except PermissionError as pe:
        raise PermissionError(f"Permission denied to access {abs_save_path}: {pe}")
    except Exception as e:
        raise Exception(f"Failed to save model to {abs_save_path}: {e}")



def load_model(save_path: str)-> SentenceTransformer:
    abs_save_path = os.path.abspath(save_path)

    if not os.path.exists(abs_save_path):
        raise FileNotFoundError(f"model directory not fount at {abs_save_path}")

    try:
        model = SentenceTransformer(abs_save_path)
        return model
    except ValueError as ve:
        raise ValueError(f"Invalid model name or configuration: {ve}")
    except Exception as e:
        raise Exception(f"Failed to load model from {abs_save_path}: {e}")


if __name__ == "__main__":
    from sentence_transformers.util import cos_sim
    import torch
    import sys

    if len(sys.argv) > 1:
        save_path = sys.argv[1]
        save_model(save_path)
        print(f"Setup complete. You can now comment out or delete the save_model call.")
    else:
        print(
            "Please provide a save path as a command-line argument, e.g., python script.py /path/to/models/paraphrase-multilingual-minilm")
        sys.exit(1)

    model_path = sys.argv[1]
    model = load_model(model_path)

    scam_keywords = [
        "تحويل فلوس فوري",
        "اربح جائزة كبيرة",
        "ادفع الان لتأكيد الحجز",
        "Vous avez gagné un prix, réclamez maintenant !",
        "andek forset reb7 kbira"
    ]
    claim = ["ija erba7 flouss"]

    claim_embedding = model.encode(claim, convert_to_tensor=True)
    scam_embeddings = model.encode(scam_keywords, convert_to_tensor=True)

    similarities = cos_sim(claim_embedding, scam_embeddings)

    print(f"similarities: {similarities}")

    max_similarity = torch.max(similarities).item()

    print(f"Similarities: {similarities}")
    print(f"Maximum similarity: {max_similarity:.4f}")