import os 
import time
from faster_whisper import WhisperModel

# Input and output Folders
AUDIO_FOLDER = "audio_input"
OUTPUT_FOLDER = "text_output"

# Extensions that will be accepted xD
SUPPORTED_EXTENSIONS = {".wav", ".mp3", ".m4a", ".flac", ".ogg", ".webm"}

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

print("Loading Whisper model on GPU...")
model = WhisperModel("large-v3", device="cuda", compute_type="float16")
print("Model loaded successfully.\n")

# Here I keep track of processed files
processed = set()

def transcribe_file(file_path):
    filename = os.path.basename(file_path)
    out_file = os.path.join(OUTPUT_FOLDER, filename + ".txt")

    print(f"\nTranscribing new file: {filename}")

    segments, info = model.transcribe(file_path, beam_size=1)

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"Detected language: {info.language}\n\n")
        for segment in segments:
            line = f"[{segment.start:.2f}s → {segment.end:.2f}s] {segment.text}\n"
            f.write(line)

    print(f"Transcription saved → {out_file}")


print("Waiting For New Filess...\n")

# Loop for multichecks inside the folder
while True:
    for file in os.listdir(AUDIO_FOLDER):
        path = os.path.join(AUDIO_FOLDER, file)

        # Skip folders
        if not os.path.isfile(path):
            continue

        # Only process supported formats
        ext = os.path.splitext(file)[1].lower()
        if ext not in SUPPORTED_EXTENSIONS:
            continue

        # Process only once 
        if file not in processed:
            transcribe_file(path)
            processed.add(file)

    time.sleep(1)  
