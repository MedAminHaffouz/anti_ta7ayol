import cv2
from PIL import Image
import torch
from transformers import AutoImageProcessor, SiglipForImageClassification

MODEL_IDENTIFIER = "Ateeqq/ai-vs-human-image-detector"

# Load model and processor
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

processor = AutoImageProcessor.from_pretrained(MODEL_IDENTIFIER)
model = SiglipForImageClassification.from_pretrained(MODEL_IDENTIFIER)
model.to(device)
model.eval()

id2label = model.config.id2label

def classify_frame(frame):
    # frame is a BGR OpenCV numpy array
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.nn.functional.softmax(logits, dim=1).squeeze().tolist()
    # Return probability of AI-generated (assuming label 'ai-generated' or similar)
    # Check label names to be sure, here I assume 'ai-generated' label exists
    ai_prob = 0
    for i, label in id2label.items():
        if "ai" in label.lower():
            ai_prob = probs[i]
            break
    return ai_prob

def analyze_video(video_path, frame_sample_rate=30, frame_ai_threshold=0.5, video_ai_threshold=0.05):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Failed to open video file {video_path}")
        return

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames in video: {frame_count}")

    ai_frames = 0
    total_sampled_frames = 0

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % frame_sample_rate == 0:
            total_sampled_frames += 1
            ai_prob = classify_frame(frame)
            print(f"Frame {frame_idx}: AI probability = {ai_prob:.3f}")
            if ai_prob > frame_ai_threshold:
                ai_frames += 1
        frame_idx += 1

    cap.release()

    if total_sampled_frames == 0:
        print("No frames were sampled.")
        return

    ai_ratio = ai_frames / total_sampled_frames
    print(f"AI frames: {ai_frames} / {total_sampled_frames} = {ai_ratio:.3f}")

    if ai_ratio > video_ai_threshold:
        print("Final video classification: AI-generated")
    else:
        print("Final video classification: Human-generated")

if __name__ == "__main__":
    video_file = "input_video.mp4"  # replace with your video path
    analyze_video(video_file)
