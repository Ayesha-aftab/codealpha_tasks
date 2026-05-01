import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading

# -----------------------------
# Optional TTS
# -----------------------------
try:
    import pyttsx3
    engine = pyttsx3.init()
    tts_available = True
except:
    tts_available = False

# -----------------------------
# Languages (FULL LIST)
# -----------------------------
languages = {
    "Auto Detect": "auto",
    "English": "en",
    "Urdu": "ur",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Dutch": "nl",
    "Russian": "ru",
    "Chinese": "zh",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Hindi": "hi",
    "Turkish": "tr",
    "Greek": "el",
    "Polish": "pl",
    "Swedish": "sv",
    "Thai": "th",
    "Vietnamese": "vi",
    "Indonesian": "id",
    "Czech": "cs",
    "Romanian": "ro",
    "Hungarian": "hu",
    "Danish": "da",
    "Finnish": "fi",
    "Norwegian": "no",
    "Ukrainian": "uk",
    "Hebrew": "he"
}

# -----------------------------
# Translation API
# -----------------------------
def do_translation(text, source, target):
    url = "https://api.mymemory.translated.net/get"
    params = {"q": text, "langpair": f"{source}|{target}"}
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    return data.get("responseData", {}).get("translatedText", "Error")

# -----------------------------
# SAFE UI UPDATE
# -----------------------------
def update_ui(original, translated):
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, translated)
    history_box.insert(tk.END, f"{original} ➜ {translated}\n")
    loading_label.config(text="")

# -----------------------------
# TRANSLATE
# -----------------------------
def translate_text():
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "Enter text first")
        return

    src = languages[source_lang.get()]
    tgt = languages[target_lang.get()]

    if src == "auto":
        src = "en"

    loading_label.config(text="Translating...")

    def task():
        try:
            translated = do_translation(text, src, tgt)
            root.after(0, update_ui, text, translated)
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("Error", str(e)))

    threading.Thread(target=task, daemon=True).start()

# -----------------------------
# COPY
# -----------------------------
def copy_text():
    text = output_text.get("1.0", tk.END)
    root.clipboard_clear()
    root.clipboard_append(text)

# -----------------------------
# SPEAK
# -----------------------------
def speak_text():
    if not tts_available:
        messagebox.showerror("Error", "TTS not installed")
        return
    text = output_text.get("1.0", tk.END).strip()
    if text:
        engine.say(text)
        engine.runAndWait()

# -----------------------------
# SWAP
# -----------------------------
def swap_lang():
    a = source_lang.get()
    b = target_lang.get()
    source_lang.set(b)
    target_lang.set(a)

# -----------------------------
# UI DESIGN (NEON CYBER PREMIUM UI)
root = tk.Tk()
root.title("CodeAlpha Translator")
root.geometry("850x730")
root.configure(bg="#050816")

# STYLE
style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", padding=6)

# COLORS (NEON CYBER THEME)
bg = "#050816"
panel = "#0b1228"
panel2 = "#0a1022"
neon_blue = "#00e5ff"
neon_purple = "#a855f7"
neon_green = "#00ff88"
neon_orange = "#ff7a18"
text = "#e5e7eb"
muted = "#94a3b8"

# HEADER
header = tk.Label(root, text="⚡ CodeAlpha Translator",
         font=("Segoe UI", 26, "bold"),
         bg=bg, fg=neon_blue)
header.pack(pady=18)

# INPUT LABEL
tk.Label(root, text="Enter Text",
         bg=bg, fg=muted, font=("Segoe UI", 11)).pack(anchor="w", padx=24)

# INPUT PANEL
input_frame = tk.Frame(root, bg=panel, highlightbackground=neon_blue, highlightthickness=2)
input_frame.pack(padx=22, pady=8, fill="both")

input_text = tk.Text(input_frame, height=5,
                     bg=panel2, fg=text,
                     insertbackground="white",
                     relief="flat",
                     font=("Segoe UI", 12))
input_text.pack(padx=10, pady=10, fill="both")

# CONTROLS
frame = tk.Frame(root, bg=bg)
frame.pack(pady=14)

source_lang = tk.StringVar(value="Auto Detect")
target_lang = tk.StringVar(value="Urdu")

src_box = ttk.Combobox(frame, textvariable=source_lang,
             values=list(languages.keys()), width=20)
src_box.grid(row=0, column=0, padx=6)

tgt_box = ttk.Combobox(frame, textvariable=target_lang,
             values=list(languages.keys()), width=20)
tgt_box.grid(row=0, column=1, padx=6)

# BUTTON STYLE

def style_btn(btn, color):
    btn.configure(bg=color, fg="white",
                  activebackground="#111827",
                  relief="flat",
                  font=("Segoe UI", 10, "bold"))

swap_btn = tk.Button(frame, text="⇄", command=swap_lang)
style_btn(swap_btn, "#1f2937")
swap_btn.grid(row=0, column=2, padx=6)

translate_btn = tk.Button(frame, text="Translate", command=translate_text)
style_btn(translate_btn, neon_green)
translate_btn.grid(row=0, column=3, padx=6)

copy_btn = tk.Button(frame, text="Copy", command=copy_text)
style_btn(copy_btn, neon_blue)
copy_btn.grid(row=0, column=4, padx=6)

speak_btn = tk.Button(frame, text="Speak", command=speak_text)
style_btn(speak_btn, neon_orange)
speak_btn.grid(row=0, column=5, padx=6)

# OUTPUT LABEL
tk.Label(root, text="Translated Text",
         bg=bg, fg=muted, font=("Segoe UI", 11)).pack(anchor="w", padx=24)

# OUTPUT PANEL
output_frame = tk.Frame(root, bg=panel, highlightbackground=neon_purple, highlightthickness=2)
output_frame.pack(padx=22, pady=8, fill="both")

output_text = tk.Text(output_frame, height=5,
                      bg=panel2, fg=neon_blue,
                      insertbackground="white",
                      relief="flat",
                      font=("Segoe UI", 12))
output_text.pack(padx=10, pady=10, fill="both")

# HISTORY LABEL
tk.Label(root, text="History",
         bg=bg, fg=text, font=("Segoe UI", 11)).pack(anchor="w", padx=24)

# HISTORY FRAME WITH BORDER ADDED
history_frame = tk.Frame(root, bg=panel,
                         highlightbackground=neon_blue,
                         highlightthickness=2)
history_frame.pack(padx=22, pady=8, fill="both")

history_box = tk.Text(history_frame, height=6,
                      bg="#070b18", fg="#9ca3af",
                      relief="flat",
                      font=("Consolas", 10))
history_box.pack(padx=10, pady=10, fill="both")

# LOADING
loading_label = tk.Label(root, text="", bg=bg, fg="#facc15", font=("Segoe UI", 10))
loading_label.pack()

# FOOTER
tk.Label(root, text="Created by Ayesha 💜/code alpha",
         bg=bg, fg="#64748b", font=("Segoe UI", 10)).pack(pady=10)

root.mainloop()
