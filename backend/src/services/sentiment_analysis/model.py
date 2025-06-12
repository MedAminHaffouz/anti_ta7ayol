from transformers import pipeline
import torch

# Initialize sentiment classifier with all scores
sentiment_classifier = pipeline(
    "sentiment-analysis", 
    model="nlptown/bert-base-multilingual-uncased-sentiment",
    return_all_scores=True,
    device=0 if torch.cuda.is_available() else -1
)

def classify_text(text):
    # Get probabilities for all classes
    all_scores = sentiment_classifier(text)[0]
    # Return as dict with rounded scores
    return {item['label']: round(item['score'], 3) for item in all_scores}

if __name__ == "__main__":
    text = "URGENT! Your account has been compromised. Click the link."
    probs = classify_text(text)
    print(f"Text: {text}")
    print(f"Probabilities: {probs}")

    # Example threshold check
    if probs.get('1 star', 0) > 0.4 or probs.get('5 stars', 0) > 0.4:
        print("⚠️ Potential scam detected due to extreme sentiment!")
    else:
        print("✅ Normal message")
