from transformers import AutoImageProcessor, SiglipForImageClassification
from PIL import Image
import torch
from ..model_loading import load_processor, load_model

# this function is the classifies if an image is ai generated
#it takes as inpput an image path, a model (loaded by the model_loading.py file), a processor(loaded by the model_loading.py file)
#returns the result as a dictionary in this format: {'ai': 1.0, 'hum': 0.0}
def classify_image(image_path, model, processor, device = "cpu"):
    id2label = model.config.id2label

    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.nn.functional.softmax(logits, dim=1).squeeze().tolist()

    prediction = {id2label[i]: round(probs[i], 3) for i in range(len(probs))}
    return prediction

if __name__ == "__main__":
    import sys
    image_path = sys.argv[1]
    model = load_model()
    processor = load_processor()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    result = classify_image(image_path, model, processor, device)
    print(f"Prediction for {image_path}: {result}")
