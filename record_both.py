import sounddevice as sd
import soundfile as sf
import time
import numpy as np

# Durée de chaque segment audio
SEGMENT_DURATION = 10  # secondes

# Nom du périphérique à chercher
TARGET_NAME = "voicemeeter"

print("🔍 Recherche du périphérique Voicemeeter...")

selected_index = None
selected_info = None

# Recherche d’un périphérique contenant "Voicemeeter"
for i, dev in enumerate(sd.query_devices()):
    if TARGET_NAME in dev["name"].lower() and dev["max_input_channels"] > 0:
        selected_index = i
        selected_info = dev
        break

if selected_index is None:
    print("❌ Aucun périphérique Voicemeeter détecté.")
    exit()

print(f"✔ Voicemeeter trouvé : {selected_info['name']} (index {selected_index})")

# Utilisation du samplerate du device
rate = int(selected_info["default_samplerate"])

# Déterminer automatiquement le nombre max de canaux que Voicemeeter accepte
channels = selected_info["max_input_channels"]

print(f"➡ Sample rate : {rate} Hz")
print(f"➡ Canaux disponibles : {channels}")

print("\n🎙 Enregistrement Voicemeeter (mix micro + audio PC)")
print("Appuie sur Ctrl+C pour arrêter.\n")

segment_id = 0

try:
    with sd.InputStream(
        device=selected_index,
        samplerate=rate,
        channels=channels,
        dtype="float32"
    ) as stream:

        while True:
            print(f"📦 Enregistrement segment {segment_id}...")

            # Lire une seconde x SEGMENT_DURATION
            frames = stream.read(int(rate * SEGMENT_DURATION))[0]

            # Convertir en numpy array
            audio = np.array(frames)

            # Nom du fichier
            filename = f"segment_{segment_id}.wav"

            # Sauvegarder
            sf.write(filename, audio, rate)

            print(f"💾 Sauvegardé : {filename}")

            segment_id += 1

except KeyboardInterrupt:
    print("\n🛑 Arrêt")

except Exception as e:
    print("\n❌ ERREUR :", e)
