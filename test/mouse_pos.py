# -*- coding: utf-8 -*-
# Copyright (C) 2026 plaisant
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import tkinter as tk
import pyautogui
import threading
import time
import os
import sys

def update_loop():
    while True:
        try:
            x, y = pyautogui.position()
            # Używamy root.after_idle, aby bezpiecznie aktualizować GUI z innego wątku (choć tutaj pętla główna też by zadziałała, to podejście jest bezpieczne)
            # W prostym przypadku z after() w głównym wątku jest lżej.
            pass
        except:
            break
        time.sleep(0.05)

def update_label():
    try:
        x, y = pyautogui.position()
        label.config(text=f"X: {x}  Y: {y}")
        # Przesunięcie okienka aby nie zasłaniało kursora (np. 20px w prawo i w dół)
        root.geometry(f"+{x+20}+{y+20}")
        root.after(50, update_label)
    except Exception:
        pass

print("=== MOUSE POSITION TRACKER ===")
print("Naciśnij ESCAPE, aby zamknąć okienko.")

root = tk.Tk()
# Usunięcie obramowania okna
root.overrideredirect(True)
# Ustawienie okna zawsze na wierzchu
root.wm_attributes("-topmost", True)
# Ustawienie tła na żółte dla widoczności
root.configure(bg='yellow')

label = tk.Label(root, text="Init...", font=("Consolas", 12, "bold"), bg="yellow", fg="black")
label.pack(ipadx=5, ipady=5)

# Zamykanie na ESC
# Zamykanie na ESC - wymuszenie zabicia procesu
def on_close(event=None):
    try:
        root.destroy()
    except:
        pass
    os._exit(0)

root.bind("<Escape>", on_close)

# Start pętli aktualizującej
update_label()

root.mainloop()
