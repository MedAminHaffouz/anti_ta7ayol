import cv2
from PIL import Image
import torch
from ..model_loading import load_model, load_processor

#you don't need to understand that my friend haffouz
def classify_frame(frame, device, processor, model):
    id2label = model.config.id2label

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

#this is the classify function of a video basically
#takes video path, processor(loaded from load_model.py file), model (loaded from load_model.py file), device ("cpu" or "gpu")
#it returns 1 if ai generated and 0 if not
def analyze_video(video_path, processor, model, device="cpu",frame_sample_rate=30, frame_ai_threshold=0.5, video_ai_threshold=0.05):
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
            ai_prob = classify_frame(frame, device, processor, model)
            if ai_prob > frame_ai_threshold:
                ai_frames += 1
        frame_idx += 1

    cap.release()

    if total_sampled_frames == 0:
        raise Exception("No frames in video")

    ai_ratio = ai_frames / total_sampled_frames

    if ai_ratio > video_ai_threshold:
        return 1
    else:
        return 0

if __name__ == "__main__":
    import sys
    video_file = sys.argv[1]
    processor = load_processor()
    model = load_model()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("ai video" if analyze_video(video_file, device, processor, model) == 1 else "not ai video")
