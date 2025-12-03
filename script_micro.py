import sounddevice as sd
import numpy as np
import wave

OUTPUT_FILENAME = "micro_externe.wav"

# Trouver le périphérique WASAPI correspondant au micro externe
devices = sd.query_devices()
mic_index = None
for i, dev in enumerate(devices):
    if "Microphone" in dev['name'] and dev['max_input_channels'] > 0:
        mic_index = i
        break

if mic_index is None:
    print(" Aucun micro externe trouvé")
    exit()

device_info = sd.query_devices(mic_index)
SAMPLE_RATE = int(device_info['default_samplerate'])
CHANNELS = device_info['max_input_channels']

print(f"🎤 Enregistrement depuis {device_info['name']} à {SAMPLE_RATE} Hz... (CTRL+C pour arrêter)")

frames = []

def callback(indata, frames_count, time_info, status):
    if status:
        print(status)
    frames.append(indata.copy())

try:
    with sd.InputStream(samplerate=SAMPLE_RATE, device=mic_index,
                        channels=CHANNELS, dtype='int16', callback=callback):
        print("🎤 Enregistrement en cours...")
        while True:
            sd.sleep(100)
except KeyboardInterrupt:
    print("\n Arrêt manuel détecté.")

# Sauvegarde dans un fichier WAV
if frames:
    wf = wave.open(OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)  # int16 = 2 bytes
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(b''.join([f.tobytes() for f in frames]))
    wf.close()
    print(f" Fichier enregistré : {OUTPUT_FILENAME}")
else:
    print(" Aucun audio enregistré.")
