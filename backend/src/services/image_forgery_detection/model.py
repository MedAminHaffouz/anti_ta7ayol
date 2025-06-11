from transformers import AutoImageProcessor, SiglipForImageClassification
from PIL import Image
import torch

# Change this to your image file path:
image_path = "image.webp"

MODEL_IDENTIFIER = "Ateeqq/ai-vs-human-image-detector"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

processor = AutoImageProcessor.from_pretrained(MODEL_IDENTIFIER)
model = SiglipForImageClassification.from_pretrained(MODEL_IDENTIFIER)
model.to(device)
model.eval()

id2label = model.config.id2label

def classify_image(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.nn.functional.softmax(logits, dim=1).squeeze().tolist()

    prediction = {id2label[i]: round(probs[i], 3) for i in range(len(probs))}
    return prediction

result = classify_image(image_path)
print(f"Prediction for {image_path}: {result}")
