import sounddevice as sd
import soundfile as sf
import numpy as np

SEGMENT_DURATION = 10  # secondes

# === CONFIG DEVICES ===
DEVICE_EXTERNE = 1   # Microphone (Realtek Audio)
DEVICE_INTERNE = 15  # Voicemeeter Out B1 (WASAPI)

# Récupération des infos
info_ext = sd.query_devices(DEVICE_EXTERNE)
info_int = sd.query_devices(DEVICE_INTERNE)

rate_ext = int(info_ext['default_samplerate'])
rate_int = int(info_int['default_samplerate'])

channels_ext = info_ext['max_input_channels']
channels_int = info_int['max_input_channels']

print("🎤 Micro externe :", info_ext["name"], "(canaux :", channels_ext, ")")
print("🔊 Son interne  :", info_int["name"], "(canaux :", channels_int, ")")
print("\nAppuie sur Ctrl+C pour stopper.\n")

segment = 0

try:
    with sd.InputStream(device=DEVICE_EXTERNE,
                        samplerate=rate_ext,
                        channels=channels_ext,
                        dtype="float32") as stream_ext, \
         sd.InputStream(device=DEVICE_INTERNE,
                        samplerate=rate_int,
                        channels=channels_int,
                        dtype="float32") as stream_int:

        while True:
            print(f"🎬 Segment {segment} enregistrement...")

            frames_ext = stream_ext.read(int(rate_ext * SEGMENT_DURATION))[0]
            frames_int = stream_int.read(int(rate_int * SEGMENT_DURATION))[0]

            audio_ext = np.array(frames_ext)
            audio_int = np.array(frames_int)

            file_ext = f"externe_{segment}.wav"
            file_int = f"interne_{segment}.wav"

            sf.write(file_ext, audio_ext, rate_ext)
            sf.write(file_int, audio_int, rate_int)

            print(f"💾 Sauvegardé : {file_ext}")
            print(f"💾 Sauvegardé : {file_int}")

            segment += 1

except KeyboardInterrupt:
    print("\n🛑 Enregistrement arrêté.")

except Exception as e:
    print("\n❌ ERREUR :", e)
