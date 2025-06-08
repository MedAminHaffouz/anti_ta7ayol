from vosk import KaldiRecognizer, Model
import wave
import json

def load_vosk_model(model_path: str)-> Model:
    return Model(model_path)

def transcribe_audio(model: Model, audio_path: str) -> str:
    with wave.open(audio_path, "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            raise ValueError("Audio file must be WAV format mono PCM.")
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.AcceptWaveform(wf.readframes(wf.getnframes()))
        res = rec.FinalResult()

        return json.loads(res)["text"]