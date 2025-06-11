import torch
from transformers import AutoImageProcessor, SiglipForImageClassification

MODEL_IDENTIFIER = "Ateeqq/ai-vs-human-image-detector"

# Load model and processor that are used in the classify finctions as simple as that haffouz my friend
def load_processor(model_identifier: str = MODEL_IDENTIFIER):
    processor = AutoImageProcessor.from_pretrained(model_identifier)
    return processor


def load_model(model_identifier: str = MODEL_IDENTIFIER):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SiglipForImageClassification.from_pretrained(model_identifier)
    model.to(device)
    model.eval()
    return model