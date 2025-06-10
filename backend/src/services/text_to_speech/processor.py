from .model import transcribe_audio, load_vosk_model
class TextToSpeechProcessor:
    @staticmethod
    def transcribe_audio(audio_path: str, model):
        return transcribe_audio(model, audio_path)

if __name__ == "__main__":
    from bidi.algorithm import get_display
    import arabic_reshaper
    import sys

    audio_path = sys.argv[1]
    model_path = sys.argv[2]
    model = load_vosk_model(model_path)

    transcript = TextToSpeechProcessor.transcribe_audio(audio_path, model)
    transcript = get_display(arabic_reshaper.reshape(transcript))
    print(f"Transcript: {transcript}")