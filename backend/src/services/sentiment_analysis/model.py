from transformers import pipeline
import torch

# Initialize sentiment classifier with all scores

def classify_text(text, sentiment_classifier):
    # Get probabilities for all classes
    all_scores = sentiment_classifier(text)[0]
    # Return as dict with rounded scores
    probs=  {item['label']: round(item['score'], 3) for item in all_scores}
    if max(probs.values()) == max(probs.get('1 star', 0), probs.get('5 star', 0)):
        return 1.2
    else:
        return 1

if __name__ == "__main__":
    text = "URGENT! Your account has been compromised. Click the link."
    probs = classify_text(text)
    # print(f"Text: {text}")
    print(f"Probabilities: {probs}")

    # # Example threshold check
    # if probs.get('1 star', 0) > 0.4 or probs.get('5 stars', 0) > 0.4:
    #     print("⚠️ Potential scam detected due to extreme sentiment!")
    # else:
    #     print("✅ Normal message")
