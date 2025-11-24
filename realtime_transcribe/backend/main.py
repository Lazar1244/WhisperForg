from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from vosk import Model, KaldiRecognizer
import json

app = FastAPI()

# Autoriser CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Charger le modèle Vosk français
model = Model(r"C:\Users\pourtoi\Documents\PROJET_WHISPER\realtime_transcribe\backend\model-fr")

@app.websocket("/ws/transcribe")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connecté")

    rec = KaldiRecognizer(model, 16000)

    try:
        while True:
            try:
                data = await websocket.receive_bytes()
            except Exception as e:
                # Si le client se déconnecte
                print("Client déconnecté :", e)
                break

            print(f"Reçu : {len(data)} bytes")

            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                await websocket.send_text(result.get("text", ""))
            else:
                partial = json.loads(rec.PartialResult())
                await websocket.send_text(partial.get("partial", ""))
    except Exception as e:
        print("Erreur WebSocket :", e)

    print("Connexion fermée")
