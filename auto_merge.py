import os
import time
import re

TEXT_OUTPUT = "text_output"
FINAL_FILE = "full_conversation.txt"

# Regex to capture Whisper timestamps, example:
# [0.00s → 2.50s] Hello there
TIMESTAMP_REGEX = r"\[(\d+\.\d+)s[^\]]*\]\s*(.*)"

processed_pairs = set()


def parse_transcript(path, speaker_label):
    segments = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(TIMESTAMP_REGEX, line)
            if match:
                start = float(match.group(1))
                text = match.group(2).strip()
                segments.append({
                    "start": start,
                    "text": text,
                    "speaker": speaker_label
                })
    return segments


def merge_segments(internal_path, external_path, pair_id):
    print(f"\n🔄 Merging pair #{pair_id}...")

    # Parse both text files
    internal_segs = parse_transcript(internal_path, "COMPANY")
    external_segs = parse_transcript(external_path, "CLIENT")

    # Merge + sort by timestamp
    merged = sorted(internal_segs + external_segs, key=lambda x: x["start"])

    # Save merged_N.txt
    merged_file = os.path.join(TEXT_OUTPUT, f"merged_{pair_id}.txt")
    with open(merged_file, "w", encoding="utf-8") as f:
        for seg in merged:
            f.write(f"[{seg['start']:.2f}s] {seg['speaker']}: {seg['text']}\n")

    # Append to full_conversation.txt
    with open(FINAL_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n--- MERGE {pair_id} ---\n")
        for seg in merged:
            f.write(f"[{seg['start']:.2f}s] {seg['speaker']}: {seg['text']}\n")

    print(f"✔ Saved merged_{pair_id}.txt")
    print(f"✔ Updated {FINAL_FILE}")


def extract_pair_id(filename):
    """
    Extracts the number N from:
    - internal_N.txt
    - external_N.txt
    """
    if filename.startswith("internal_") and filename.endswith(".txt"):
        return filename.replace("internal_", "").replace(".txt", "")
    if filename.startswith("external_") and filename.endswith(".txt"):
        return filename.replace("external_", "").replace(".txt", "")
    return None


def find_pair_ids():
    """Find all pair numbers that appear in text_output"""
    ids = set()
    for fname in os.listdir(TEXT_OUTPUT):
        pair_id = extract_pair_id(fname)
        if pair_id is not None:
            ids.add(pair_id)
    return ids


print("📡 Auto-merger running... Watching text_output/ for internal/external pairs.\n")

while True:
    pair_ids = find_pair_ids()

    for pair_id in pair_ids:
        if pair_id in processed_pairs:
            continue

        internal_path = os.path.join(TEXT_OUTPUT, f"internal_{pair_id}.txt")
        external_path = os.path.join(TEXT_OUTPUT, f"external_{pair_id}.txt")

        # Both files exist → merge them
        if os.path.exists(internal_path) and os.path.exists(external_path):
            merge_segments(internal_path, external_path, pair_id)
            processed_pairs.add(pair_id)

    time.sleep(1)
