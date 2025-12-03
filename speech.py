import pyaudio
import wave

DEVICE_NAME = "Mixage Stéréo"  # ou "Mixage Stéréo" ou "What U Hear"
OUTPUT = "audio_interne.wav"

p = pyaudio.PyAudio()

# Trouver l’ID du périphérique par son nom
device_index = None
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if DEVICE_NAME.lower() in info["name"].lower():
        device_index = i
        break

if device_index is None:
    raise Exception(f"Impossible de trouver: {DEVICE_NAME}")

print(f"🎧 Capture depuis: {DEVICE_NAME}")

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=CHUNK)

print("🎙️ Enregistrement du son interne... (Ctrl+C pour arrêter)")

frames = []
try:
    while True:
        frames.append(stream.read(CHUNK))
except KeyboardInterrupt:
    print("\n Enregistrement arrêté")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(OUTPUT, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print(f" Sauvegardé dans : {OUTPUT}")
