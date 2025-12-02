# hz_overlay_transparent3.py
# Transparent background, more transparent text, 120 Hz = white.

import ctypes, sys, tkinter as tk
from ctypes import wintypes
from tkinter import font

if sys.platform != "win32":
    print("Windows only"); sys.exit(1)

ENUM_CURRENT_SETTINGS = -1

class DEVMODE(ctypes.Structure):
    _fields_ = [
        ("dmDeviceName", wintypes.WCHAR * 32),
        ("dmSpecVersion", wintypes.WORD),
        ("dmDriverVersion", wintypes.WORD),
        ("dmSize", wintypes.WORD),
        ("dmDriverExtra", wintypes.WORD),
        ("dmFields", wintypes.DWORD),
        ("dmOrientation", wintypes.SHORT),
        ("dmPaperSize", wintypes.SHORT),
        ("dmPaperLength", wintypes.SHORT),
        ("dmPaperWidth", wintypes.SHORT),
        ("dmScale", wintypes.SHORT),
        ("dmCopies", wintypes.SHORT),
        ("dmDefaultSource", wintypes.SHORT),
        ("dmPrintQuality", wintypes.SHORT),
        ("dmColor", wintypes.SHORT),
        ("dmDuplex", wintypes.SHORT),
        ("dmYResolution", wintypes.SHORT),
        ("dmTTOption", wintypes.SHORT),
        ("dmCollate", wintypes.SHORT),
        ("dmFormName", wintypes.WCHAR * 32),
        ("dmLogPixels", wintypes.WORD),
        ("dmBitsPerPel", wintypes.DWORD),
        ("dmPelsWidth", wintypes.DWORD),
        ("dmPelsHeight", wintypes.DWORD),
        ("dmDisplayFlags", wintypes.DWORD),
        ("dmDisplayFrequency", wintypes.DWORD),
        ("dmICMMethod", wintypes.DWORD),
        ("dmICMIntent", wintypes.DWORD),
        ("dmMediaType", wintypes.DWORD),
        ("dmDitherType", wintypes.DWORD),
        ("dmReserved1", wintypes.DWORD),
        ("dmReserved2", wintypes.DWORD),
        ("dmPanningWidth", wintypes.DWORD),
        ("dmPanningHeight", wintypes.DWORD),
    ]

def raw_hz():
    dm = DEVMODE()
    dm.dmSize = ctypes.sizeof(DEVMODE)
    ok = ctypes.windll.user32.EnumDisplaySettingsW(
        None, ENUM_CURRENT_SETTINGS, ctypes.byref(dm)
    )
    return int(dm.dmDisplayFrequency) if ok else None

# ---- transparent overlay ----
root = tk.Tk()

root.overrideredirect(True)
root.attributes("-topmost", True)

# fully transparent background
root.config(bg="black")
root.attributes("-transparentcolor", "black")

# MORE transparent text/window
root.attributes("-alpha", 0.35)   # <-- lowered from 0.75 → more transparent

root.bind("<Escape>", lambda e: root.destroy())

lbl_font = font.Font(family="Segoe UI", size=28)

# pushed higher
label = tk.Label(root, text="Hz", font=lbl_font, bg="black")
label.pack(padx=6, pady=(0, 0))

def place():
    root.update_idletasks()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    w = root.winfo_width()
    h = root.winfo_height()
    margin = 14
    y_offset = 20
    x = sw - w - margin
    y = sh - h - margin - y_offset
    root.geometry(f"+{x}+{y}")

place()

last_good = 120

def tick():
    global last_good
    hz = raw_hz()
    if hz is None or hz < 20 or hz > 500:
        hz = last_good
    else:
        last_good = hz

    txt = f"{hz}Hz"
    if label.cget("text") != txt:
        label.config(text=txt)

        if hz == 144:
            lbl_font.config(weight="bold", slant="italic", size=30)
            label.config(fg="white")

        elif hz == 120:
	    # ✔ 120 Hz is now white
            lbl_font.config(weight="bold", slant="roman", size=30)
            label.config(fg="white")

        else:
            lbl_font.config(weight="normal", slant="roman", size=28)
            label.config(fg="#B0B0B0")

        place()

    root.after(300, tick)
root.after(10, tick)
root.mainloop()
