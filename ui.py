import tkinter as tk
from pathlib import Path

BASE_DIR = Path("data")
already_displayed = set()

def read_new_files():
    for folder in ["interne", "externe", "merge"]:
        for file in sorted((BASE_DIR / folder).glob("*.txt")):
            if file not in already_displayed:
                with open(file, "r", encoding="utf-8") as f:
                    content = f.read()

                text.insert(tk.END, f"\n===== {file.name} =====\n")
                text.insert(tk.END, content + "\n")
                text.see(tk.END)

                already_displayed.add(file)

    root.after(1000, read_new_files)  # vérifie toutes les 1s

root = tk.Tk()
root.title("Contenu des fichiers reçus")

text = tk.Text(root, width=80, height=30)
text.pack()

read_new_files()
root.mainloop()
