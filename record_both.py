import sounddevice as sd
import wave
import threading
import numpy as np

# ---------- Paramètres ----------
INTERNAL_OUTPUT = "audio_interne.wav"
EXTERNAL_OUTPUT = "micro_externe.wav"
CHANNELS = 2
RATE = 44100
CHUNK = 1024

# ---------- Détection des périphériques ----------
devices = sd.query_devices()
internal_index = None
external_index = None

for i, dev in enumerate(devices):
    if "mixage stéréo" in dev['name'].lower() and dev['max_input_channels'] > 0:
        internal_index = i
    if "microphone" in dev['name'].lower() and dev['max_input_channels'] > 0:
        external_index = i

if internal_index is None:
    print("❌ Mixage stéréo non trouvé")
if external_index is None:
    print("❌ Micro externe non trouvé")

# ---------- Buffers ----------
internal_frames = []
external_frames = []

# ---------- Callbacks ----------
def internal_callback(indata, frames, time, status):
    if status:
        print("Internal:", status)
    internal_frames.append(indata.copy())

def external_callback(indata, frames, time, status):
    if status:
        print("External:", status)
    external_frames.append(indata.copy())

# ---------- Drapeau pour arrêter ----------
STOP_RECORDING = False

# ---------- Fonctions d'enregistrement ----------
def record_internal():
    global STOP_RECORDING
    if internal_index is None:
        return
    try:
        wasapi_settings = sd.WasapiSettings(loopback=True)
        with sd.InputStream(samplerate=RATE,
                            device=internal_index,
                            channels=CHANNELS,
                            dtype='int16',
                            callback=internal_callback,
                            extra_settings=wasapi_settings):
            print(f"🎧 Enregistrement audio interne: {devices[internal_index]['name']}")
            while not STOP_RECORDING:
                sd.sleep(100)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt manuel audio interne")

def record_external():
    global STOP_RECORDING
    if external_index is None:
        return
    try:
        with sd.InputStream(samplerate=RATE,
                            device=external_index,
                            channels=CHANNELS,
                            dtype='int16',
                            callback=external_callback):
            print(f"🎤 Enregistrement micro externe: {devices[external_index]['name']}")
            while not STOP_RECORDING:
                sd.sleep(100)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt manuel micro externe")

# ---------- Lancer les deux threads ----------
t1 = threading.Thread(target=record_internal)
t2 = threading.Thread(target=record_external)
t1.start()
t2.start()

try:
    input("Appuie sur Entrée pour arrêter l'enregistrement...\n")
finally:
    STOP_RECORDING = True
    t1.join()
    t2.join()

# ---------- Sauvegarde des fichiers ----------
if internal_frames:
    wf = wave.open(INTERNAL_OUTPUT, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)
    wf.setframerate(RATE)
    wf.writeframes(b''.join([f.tobytes() for f in internal_frames]))
    wf.close()
    print(f"✅ Audio interne sauvegardé: {INTERNAL_OUTPUT}")
else:
    print("⚠️ Aucun audio interne enregistré")

if external_frames:
    wf = wave.open(EXTERNAL_OUTPUT, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)
    wf.setframerate(RATE)
    wf.writeframes(b''.join([f.tobytes() for f in external_frames]))
    wf.close()
    print(f"✅ Micro externe sauvegardé: {EXTERNAL_OUTPUT}")
else:
    print("⚠️ Aucun audio micro enregistré")
