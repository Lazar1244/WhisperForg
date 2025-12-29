import time
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("data")
TYPES = ["interne", "externe", "merge"]

def next_index(folder):
    return len(list(folder.glob("*.txt"))) + 1

def generate_files():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for t in TYPES:
        folder = BASE_DIR / t
        folder.mkdir(parents=True, exist_ok=True)

        idx = next_index(folder)
        filename = folder / f"{t}_{idx}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"""
Type      : {t}
Index     : {idx}
Créé le   : {timestamp}
Contenu   : Ceci est le fichier {t}_{idx}
""")

        print(f"Créé : {filename}")

if __name__ == "__main__":
    while True:
        generate_files()
        time.sleep(10)
