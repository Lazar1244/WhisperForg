import json
from vosk import Model, KaldiRecognizer

class RecognizerWrapper:
    def __init__(self):
        self.model = Model("model-fr")  # chemin vers le modèle français VOSK
        self.recognizer = KaldiRecognizer(self.model, 16000)

    def transcribe_chunk(self, chunk_bytes):
        if self.recognizer.AcceptWaveform(chunk_bytes):
            result = json.loads(self.recognizer.Result())
            return result.get("text", "")
        else:
            partial = json.loads(self.recognizer.PartialResult())
            return partial.get("partial", "")
