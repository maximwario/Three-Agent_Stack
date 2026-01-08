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
from tkinter import font
import time
import json
import os
from utils.logger import AgentLogger

class HeadsUpDisplay:
    def __init__(self, root_ref, config_manager=None, stop_callback=None):
        self.root_ref = root_ref
        self.cfg = config_manager
        self.stop_cb = stop_callback
        self.log = AgentLogger("HUD_CTRL")
        try:
            self.win = tk.Toplevel(root_ref)
            self.win.title("PERCEPTRON HUD")
            
            screen_w = self.win.winfo_screenwidth()
            screen_h = self.win.winfo_screenheight()
            width = int(screen_w * 0.50)  # Węższy (było 0.75)
            height = 120                  # Wyższy (było 85 + 35)
            x = 0                         # Lewy Róg (Flush)
            y = screen_h - height         # Sam Dół (zasłania pasek) 
            
            self.win.geometry(f"{width}x{height}+{x}+{y}")
            self.win.attributes('-topmost', True)
            self.win.overrideredirect(True)
            self.win.configure(bg="#050505")
            self.win.minsize(500, 60)
            
            self.main_frame = tk.Frame(self.win, bg="#050505", highlightbackground="#00ff00", highlightthickness=1)
            self.main_frame.pack(fill=tk.BOTH, expand=True)
            
            self.alive = True
            
            self._setup_fonts()
            self._setup_layout()
            self.make_draggable(self.main_frame)
            self._add_resize_grip()
        except: self.alive = False

    def make_draggable(self, w):
        w.bind("<Button-1>", self.start_move); w.bind("<B1-Motion>", self.do_move)
        if isinstance(w, (tk.Frame, tk.Label)):
            for c in w.winfo_children(): 
                if not isinstance(c, (tk.Button, tk.Label, tk.Listbox)): self.make_draggable(c)
    def start_move(self,e): self.x=e.x; self.y=e.y
    def do_move(self,e): self.win.geometry(f"+{self.win.winfo_x()+(e.x-self.x)}+{self.win.winfo_y()+(e.y-self.y)}")
    def _add_resize_grip(self):
        l=tk.Label(self.main_frame,text="◿",bg="#080808",fg="gray",cursor="sizing");l.place(relx=1,rely=1,anchor="se")
        l.bind("<Button-1>",lambda e: setattr(self,'rx',e.x)); l.bind("<B1-Motion>", self.do_resize)
    def do_resize(self,e): 
        w=(e.x_root-self.win.winfo_rootx()); h=(e.y_root-self.win.winfo_rooty())
        if w>400 and h>50: self.win.geometry(f"{w}x{h}")
    def close_hud(self): self.alive=False; self.win.destroy()
    def minimize_hud(self): self.win.geometry(f"{self.win.winfo_width()}x{'20' if self.win.winfo_height()>30 else '85'}")
    def is_alive(self): return self.alive and self.win.winfo_exists()

    def _setup_fonts(self):
        self.f_big = font.Font(family="Consolas", size=14, weight="bold")
        self.f_head = font.Font(family="Consolas", size=8, weight="bold")
        self.f_norm = font.Font(family="Consolas", size=9)
        self.f_mono = font.Font(family="Consolas", size=9, weight="bold")
        self.f_small = font.Font(family="Consolas", size=8)

    def _setup_layout(self):
        top = tk.Frame(self.main_frame, bg="#151515", height=10); top.pack(fill=tk.X)
        self.make_draggable(top)
        tk.Button(top, text="✕", bg="#300", fg="white", bd=0, font=("Arial",6), width=3, command=self.close_hud).pack(side=tk.RIGHT)
        tk.Button(top, text="_", bg="#222", fg="gray", bd=0, font=("Arial",6), width=3, command=self.minimize_hud).pack(side=tk.RIGHT)

        content = tk.Frame(self.main_frame, bg="#050505"); content.pack(fill=tk.BOTH, expand=True, padx=2)
        self.make_draggable(content)

        fr_ctrl = tk.Frame(content, bg="#080808", width=130); fr_ctrl.pack(side=tk.LEFT, fill=tk.Y, padx=2, pady=2)
        r1 = tk.Frame(fr_ctrl, bg="#080808"); r1.pack(fill=tk.X, pady=2)
        self.btn_stop = tk.Button(r1, text="STOP", bg="#900", fg="white", font=("Arial",8,"bold"), bd=0, command=self.force_stop)
        self.btn_stop.pack(side=tk.LEFT, padx=2)
        self.lbl_err = tk.Label(r1, text="SYS OK", font=("Arial",7), bg="#080808", fg="#0f0"); self.lbl_err.pack(side=tk.LEFT, padx=5)
        r2 = tk.Frame(fr_ctrl, bg="#080808"); r2.pack(fill=tk.X)
        self.lbl_status = tk.Label(r2, text="IDLE", font=self.f_mono, bg="#080808", fg="orange"); self.lbl_status.pack(side=tk.LEFT, padx=2)
        self.lbl_timer = tk.Label(r2, text="00:00", font=self.f_small, bg="#080808", fg="gray"); self.lbl_timer.pack(side=tk.LEFT, padx=5)
        
        # --- AGENT 3 SWITCH (CYBERPUNK STYLE) ---
        r3 = tk.Frame(fr_ctrl, bg="#080808"); r3.pack(fill=tk.X, pady=1)
        self.lbl_a3_switch = tk.Label(r3, text="A3: ON", font=self.f_mono, bg="#003333", fg="cyan", width=10, cursor="hand2")
        self.lbl_a3_switch.pack(side=tk.LEFT, padx=5)
        self.lbl_a3_switch.bind("<Button-1>", self.toggle_a3)
        self._refresh_a3_visuals()
        # ----------------------------------------

        fr_data = tk.Frame(content, bg="#050505"); fr_data.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        for i,h in enumerate(["SRC","SIZE","ENTRY","TP / SL","PnL"]):
            tk.Label(fr_data, text=h, font=self.f_head, bg="#050505", fg="#444").grid(row=0, column=i, sticky="w", padx=4)
        
        tk.Label(fr_data, text="BN", font=self.f_mono, bg="#050505", fg="gold").grid(row=1, column=0, sticky="w")
        self.lbl_bn_size = tk.Label(fr_data, text="---", font=self.f_norm, bg="#050505", fg="white")
        self.lbl_bn_size.grid(row=1, column=1, sticky="w")
        self.lbl_bn_entry = tk.Label(fr_data, text="---", font=self.f_norm, bg="#050505", fg="white")
        self.lbl_bn_entry.grid(row=1, column=2, sticky="w")
        self.lbl_bn_tpsl = tk.Label(fr_data, text="--/--", font=self.f_small, bg="#050505", fg="gray")
        self.lbl_bn_tpsl.grid(row=1, column=3, sticky="w")
        self.lbl_bn_pnl = tk.Label(fr_data, text="0.00", font=self.f_mono, bg="#050505", fg="gray")
        self.lbl_bn_pnl.grid(row=1, column=4, sticky="w")

        tk.Label(fr_data, text="TV", font=self.f_mono, bg="#050505", fg="cyan").grid(row=2, column=0, sticky="w")
        self.lbl_tv_size = tk.Label(fr_data, text="---", font=self.f_norm, bg="#050505", fg="white")
        self.lbl_tv_size.grid(row=2, column=1, sticky="w")
        self.lbl_tv_entry = tk.Label(fr_data, text="---", font=self.f_norm, bg="#050505", fg="white")
        self.lbl_tv_entry.grid(row=2, column=2, sticky="w")
        self.lbl_tv_tpsl = tk.Label(fr_data, text="--/--", font=self.f_small, bg="#050505", fg="gray")
        self.lbl_tv_tpsl.grid(row=2, column=3, sticky="w")
        self.lbl_tv_pnl = tk.Label(fr_data, text="0.00", font=self.f_mono, bg="#050505", fg="gray")
        self.lbl_tv_pnl.grid(row=2, column=4, sticky="w")

        fr_right = tk.Frame(content, bg="#080808", width=140); fr_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.lbl_btc = tk.Label(fr_right, text="$-----", font=self.f_big, bg="#080808", fg="white"); self.lbl_btc.pack(pady=2)
        self.log_list = tk.Listbox(fr_right, bg="#000", fg="#0f0", font=("Courier",7), height=3, bd=0); self.log_list.pack(fill=tk.BOTH, expand=True)
        self.btn_scan = tk.Button(r3, text="SCAN: ON", bg="#004400", fg="white", font=("Arial", 8), command=self.toggle_scan)
        self.btn_scan.pack(side=tk.LEFT, padx=2)

    # --- UPDATE METODY (POPRAWIONE) ---

    def toggle_scan(self):
        """Bezpiecznik skanowania tła."""
        curr = self.cfg.get('SYSTEM', 'background_scan_enabled', 'True') == 'True'
        new_state = not curr
        self.cfg.set_and_save('SYSTEM', 'background_scan_enabled', str(new_state))
        self.btn_scan.config(text=f"SCAN: {'ON' if new_state else 'OFF'}", bg="#004400" if new_state else "#440000")

    def _update_state_files(self, source, data):
        """
        Aktualizuje pliki stanu:
        1. runtime_state.json -> Snapshot aktualnego stanu (Overwrite)
        2. market_history.jsonl -> Log historyczny (Append)
        """
        t_str = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # 1. LOAD EXISTING SNAPSHOT (to merge valid data from other source)
        state_file = "runtime_state.json"
        current_state = {}
        
        if os.path.exists(state_file):
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    current_state = json.load(f)
            except: current_state = {}
            
        # Update timestamp
        current_state["last_update"] = t_str
        
        # Przygotuj obiekt danych dla tego źródła
        source_key = source.lower() # binance or tradingview
        current_state[source_key] = {
            "status": data.get('status', 'N/A'),
            "pnl": data.get('pnl', 0.0),
            "size": data.get('size', 'N/A'),
            "entry": data.get('entry', 'N/A'),
            "tp_sl": data.get('tp_sl', 'N/A'),
            # Jeśli w data są orders, też je zapiszmy
            "orders": data.get('orders', []) 
        }
        
        # 2. SAVE SNAPSHOT
        try:
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(current_state, f, indent=2)
        except Exception as e: print(f"State Write Error: {e}")
        
        # 3. APPEND TO HISTORY (JSONL)
        hist_file = "market_history.jsonl"
        log_entry = {
            "time": t_str,
            "src": source,
            "data": current_state[source_key]
        }
        try:
            with open(hist_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e: print(f"Hist Write Error: {e}")

    def update_bn_data(self, data):
        """Aktualizacja Binance"""
        if not self.is_alive(): return
        self._update_state_files("BINANCE", data)
        try:
            status = data.get('status', 'NO DATA')
            pnl_val = data.get('pnl', 0.0)
            
            if status == "FLAT":
                self.lbl_bn_size.config(text="FLAT", fg="gray") # POPRAWKA: lbl_bn_size (było pos)
                self.lbl_bn_pnl.config(text="0.00", fg="gray")
                self.lbl_bn_entry.config(text="----")
                self.lbl_bn_tpsl.config(text="--/--")
            else:
                col = "#00ff00" if pnl_val >= 0 else "#ff3333"
                self.lbl_bn_size.config(text=f"{data.get('size','?')}", fg="white") # POPRAWKA
                self.lbl_bn_entry.config(text=f"@{data.get('entry','?')}", fg="white")
                self.lbl_bn_pnl.config(text=f"{pnl_val:.2f}$", fg=col)
                self.lbl_bn_tpsl.config(text=f"{data.get('tp_sl','--/--')}", fg="gray")
        except Exception as e:
            # Teraz błąd nie będzie cichy
            print(f"HUD Update Error (BN): {e}")

    def update_tv_data(self, data):
        if not self.is_alive(): return
        self._update_state_files("TRADINGVIEW", data)
        try:
            status = data.get('status', 'WAITING')
            pnl_val = data.get('pnl', 0.0)
            
            if status != "ACTIVE":
                self.lbl_tv_size.config(text="WAIT", fg="gray")
                self.lbl_tv_pnl.config(text="0.00", fg="gray")
            else:
                col = "#00ff00" if pnl_val >= 0 else "#ff3333"
                self.lbl_tv_size.config(text=f"{data.get('size','POS')}", fg="cyan")
                self.lbl_tv_entry.config(text=f"@{data.get('entry','?')}", fg="white")
                self.lbl_tv_pnl.config(text=f"{pnl_val:.2f}$", fg=col)
                self.lbl_tv_tpsl.config(text="--/--", fg="#444")
        except: pass

    def update_mission(self, status, countdown, last_action, error=None):
        if not self.is_alive(): return
        try:
            cols = {"SLEEP": "#555", "HARVEST": "cyan", "THINK": "magenta", "STOP": "red", "WORKING": "orange"}
            fg = cols.get(status, "orange")
            for k in cols: 
                if k in status: fg = cols[k]
            self.lbl_status.config(text=status, fg=fg)
            m, s = divmod(int(countdown), 60)
            self.lbl_timer.config(text=f"{m:02}:{s:02}")
            if error: self.lbl_err.config(text="ERROR", fg="red")
            else: self.lbl_err.config(text="SYS OK", fg="#0f0")
        except: pass

    def update_market(self, price, funding=None):
        if self.is_alive():
            try: self.lbl_btc.config(text=f"${price}")
            except: pass

    def log_action(self, msg):
        if not self.is_alive(): return
        try:
            t = time.strftime("%H:%M:%S")
            self.log_list.insert(0, f"[{t}] {msg}")
            if self.log_list.size() > 50: self.log_list.delete(50, tk.END)
        except: pass

    def set_ai_status(self, ai, status): pass 

    def toggle_a3(self, event=None):
        """Przełącznik włącz/wyłącz Agenta 3"""
        if not self.cfg: return
        
        curr = self.cfg.get("SYSTEM", "agent_3_enabled", "True") == "True"
        new_state = not curr
        self.cfg.set_and_save("SYSTEM", "agent_3_enabled", str(new_state))
        
        status_str = "ENABLED" if new_state else "DISABLED"
        self.log.log(f"MANUAL TOGGLE: Agent 3 is now {status_str}", "CONFIG")
        
        self._refresh_a3_visuals()
        
    def _refresh_a3_visuals(self):
        if not self.cfg: return
        state = self.cfg.get("SYSTEM", "agent_3_enabled", "True") == "True"
        if state:
            self.lbl_a3_switch.config(text="A3: [ON]", bg="#004444", fg="cyan")
        else:
            self.lbl_a3_switch.config(text="A3: OFF", bg="#222", fg="#555") 

    def force_stop(self):
        self.lbl_status.config(text="KILL...", fg="red")
        self.main_frame.config(highlightbackground="red")
        if self.stop_cb: self.stop_cb()