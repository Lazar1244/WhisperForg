import tkinter as tk
from pathlib import Path

BASE_DIR = Path("data")
displayed_files = set()

COLORS = {
    "interne": "#cce5ff",
    "externe": "#d4edda",
    "merge": "#e2d6f3"
}

def read_new_files():
    for t in ["interne", "externe", "merge"]:
        folder = BASE_DIR / t
        folder.mkdir(parents=True, exist_ok=True)

        for file in sorted(folder.glob("*.txt")):
            if file not in displayed_files:
                with open(file, "r", encoding="utf-8") as f:
                    content = f.read()

                text_widgets[t].insert(
                    tk.END,
                    f"\n{file.name}\n{content}\n",
                    t
                )
                text_widgets[t].see(tk.END)
                displayed_files.add(file)

    root.after(1000, read_new_files)

def clear_all():
    for text in text_widgets.values():
        text.delete("1.0", tk.END)
    displayed_files.clear()

# ---------------- UI ---------------- #

root = tk.Tk()
root.title("Surveillance des fichiers")
root.geometry("1100x500")

frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

text_widgets = {}

for i, t in enumerate(["interne", "externe", "merge"]):
    col_frame = tk.Frame(frame)
    col_frame.grid(row=0, column=i, sticky="nsew", padx=5)

    label = tk.Label(col_frame, text=t.upper(), font=("Arial", 12, "bold"))
    label.pack()

    text = tk.Text(col_frame, width=40, height=25)
    text.pack()
    text.tag_config(t, background=COLORS[t])

    text_widgets[t] = text

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.columnconfigure(2, weight=1)


read_new_files()
root.mainloop()
