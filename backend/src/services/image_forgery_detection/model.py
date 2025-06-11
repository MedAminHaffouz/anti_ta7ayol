import gradio as gr
from transformers import AutoImageProcessor, SiglipForImageClassification
from PIL import Image
import torch

MODEL_IDENTIFIER = "Ateeqq/ai-vs-human-image-detector"

# Load model and processor
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

processor = AutoImageProcessor.from_pretrained(MODEL_IDENTIFIER)
model = SiglipForImageClassification.from_pretrained(MODEL_IDENTIFIER)
model.to(device)
model.eval()

# id2label mapping from the model config
id2label = model.config.id2label

def classify_image(image):
    # image from gr.Image is a numpy array
    image = Image.fromarray(image).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.nn.functional.softmax(logits, dim=1).squeeze().tolist()

    prediction = {id2label[i]: round(probs[i], 3) for i in range(len(probs))}
    return prediction

iface = gr.Interface(
    fn=classify_image,
    inputs=gr.Image(type="numpy"),
    outputs=gr.Label(num_top_classes=2, label="AI vs Human Image Detection"),
    title="AI vs Human Image Detector",
    description="Upload an image to detect if it's AI-generated or a real photo."
)

if __name__ == "__main__":
    iface.launch()
