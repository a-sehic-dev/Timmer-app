import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading


class PremiumTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Adjustable Speed Timer")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(True, False)

        # Colors
        self.bg_dark = "#1a1a2e"
        self.bg_card = "#16213e"
        self.accent = "#e94560"
        self.accent_hover = "#ff6b6b"
        self.text_primary = "#eaeaea"
        self.text_secondary = "#a0a0b0"
        self.green = "#00d9a5"
        self.blue = "#4d8af0"
        self.yellow = "#f5c542"

        # Timer state
        self.actual_total = 0
        self.display_total = 0
        self.actual_left = 0
        self.display_left = 0
        self.speed = 1.0
        self.running = False
        self.lock = threading.Lock()

        self.build_ui()
        self.root.update_idletasks()
        height = self.root.winfo_reqheight() + 50
        self.root.geometry(f"480x{height}")
        self.root.minsize(480, height)

    def build_ui(self):
        # ===== HEADER =====
        header = tk.Frame(self.root, bg=self.bg_dark, height=60)
        header.pack(fill="x", padx=20, pady=(20, 10))
        header.pack_propagate(False)

        tk.Label(header, text="⏱ Adjustable Speed Timer", font=("Segoe UI", 18, "bold"),
                 bg=self.bg_dark, fg=self.text_primary).pack(side="left", anchor="w")

        tk.Label(header, text="v1.0", font=("Segoe UI", 10),
                 bg=self.bg_dark, fg=self.text_secondary).pack(side="left", anchor="sw", padx=(5, 0), pady=(0, 2))

        # ===== SETUP CARD =====
        setup_card = tk.Frame(self.root, bg=self.bg_card, bd=0)
        setup_card.pack(fill="x", padx=20, pady=10)

        tk.Label(setup_card, text="SETUP", font=("Segoe UI", 10, "bold"),
                 bg=self.bg_card, fg=self.accent).pack(anchor="w", padx=15, pady=(12, 8))

        # Actual time row
        row1 = tk.Frame(setup_card, bg=self.bg_card)
        row1.pack(fill="x", padx=15, pady=5)
        tk.Label(row1, text="Actual Duration:", font=("Segoe UI", 11),
                 bg=self.bg_card, fg=self.text_primary, width=14, anchor="w").pack(side="left")
        self.entry_actual = tk.Entry(row1, font=("Segoe UI", 12, "bold"), width=8,
                                      bg=self.bg_dark, fg=self.green, insertbackground=self.green,
                                      relief="flat", justify="center")
        self.entry_actual.pack(side="left", padx=(5, 0))
        self.entry_actual.insert(0, "60")
        tk.Label(row1, text="minutes", font=("Segoe UI", 10),
                 bg=self.bg_card, fg=self.text_secondary).pack(side="left", padx=(5, 0))

        # Display time row
        row2 = tk.Frame(setup_card, bg=self.bg_card)
        row2.pack(fill="x", padx=15, pady=5)
        tk.Label(row2, text="Display Time:", font=("Segoe UI", 11),
                 bg=self.bg_card, fg=self.text_primary, width=14, anchor="w").pack(side="left")
        self.entry_display = tk.Entry(row2, font=("Segoe UI", 12, "bold"), width=8,
                                       bg=self.bg_dark, fg=self.blue, insertbackground=self.blue,
                                       relief="flat", justify="center")
        self.entry_display.pack(side="left", padx=(5, 0))
        self.entry_display.insert(0, "30")
        tk.Label(row2, text="minutes", font=("Segoe UI", 10),
                 bg=self.bg_card, fg=self.text_secondary).pack(side="left", padx=(5, 0))

        # Start button
        self.btn_start = tk.Button(setup_card, text="▶ START TIMER", font=("Segoe UI", 11, "bold"),
                                   bg=self.accent, fg="white", activebackground=self.accent_hover,
                                   activeforeground="white", relief="flat", cursor="hand2",
                                   command=self.start_timer, padx=20, pady=8)
        self.btn_start.pack(pady=(10, 12))

        # ===== TIMER CARD =====
        timer_card = tk.Frame(self.root, bg=self.bg_card, bd=0)
        timer_card.pack(fill="x", padx=20, pady=10)

        tk.Label(timer_card, text="TIMER", font=("Segoe UI", 10, "bold"),
                 bg=self.bg_card, fg=self.accent).pack(anchor="w", padx=15, pady=(12, 4))

        # Display time (big)
        self.lbl_display_big = tk.Label(timer_card, text="00:00", font=("Segoe UI", 42, "bold"),
                                        bg=self.bg_card, fg=self.blue)
        self.lbl_display_big.pack(pady=(4, 2))

        tk.Label(timer_card, text="DISPLAY TIME", font=("Segoe UI", 8),
                 bg=self.bg_card, fg=self.text_secondary).pack()

        # Actual time (smaller)
        self.lbl_actual = tk.Label(timer_card, text="Actual: 00:00", font=("Segoe UI", 11),
                                   bg=self.bg_card, fg=self.text_secondary)
        self.lbl_actual.pack(pady=(4, 2))

        # Speed indicator
        self.lbl_speed = tk.Label(timer_card, text="Speed: 1.000x", font=("Segoe UI", 13, "bold"),
                                  bg=self.bg_card, fg=self.yellow)
        self.lbl_speed.pack(pady=(2, 10))

        # ===== CONTROLS CARD =====
        ctrl_card = tk.Frame(self.root, bg=self.bg_card, bd=0)
        ctrl_card.pack(fill="x", padx=20, pady=10)

        tk.Label(ctrl_card, text="CONTROLS", font=("Segoe UI", 10, "bold"),
                 bg=self.bg_card, fg=self.accent).pack(anchor="w", padx=15, pady=(12, 8))

        # Buttons row
        btn_row = tk.Frame(ctrl_card, bg=self.bg_card)
        btn_row.pack(padx=15, pady=(0, 8))

        self.btn_add = tk.Button(btn_row, text="  +  ", font=("Segoe UI", 16, "bold"),
                                 bg=self.green, fg=self.bg_dark, activebackground="#00ffbb",
                                 relief="flat", cursor="hand2", command=self.add_time, state="disabled")
        self.btn_add.pack(side="left", padx=(0, 15))

        self.btn_sub = tk.Button(btn_row, text="  −  ", font=("Segoe UI", 16, "bold"),
                                 bg=self.accent, fg="white", activebackground=self.accent_hover,
                                 relief="flat", cursor="hand2", command=self.reduce_time, state="disabled")
        self.btn_sub.pack(side="left", padx=(0, 15))

        self.btn_stop = tk.Button(btn_row, text="  ⏹ STOP  ", font=("Segoe UI", 12, "bold"),
                                  bg="#555", fg="white", activebackground="#777",
                                  relief="flat", cursor="hand2", command=self.stop_timer, state="disabled")
        self.btn_stop.pack(side="left", padx=(10, 0))

        # Legend
        legend = tk.Frame(ctrl_card, bg=self.bg_card)
        legend.pack(padx=15, pady=(4, 12), fill="x")

        tk.Label(legend, text="[+] Display +1min, Actual +2min", font=("Segoe UI", 9),
                 bg=self.bg_card, fg=self.text_secondary).pack(anchor="w")
        tk.Label(legend, text="[−] Display −1min, Actual unchanged", font=("Segoe UI", 9),
                 bg=self.bg_card, fg=self.text_secondary).pack(anchor="w")

        # ===== STATUS BAR =====
        self.lbl_status = tk.Label(self.root, text="Ready — Enter times and click Start",
                                   font=("Segoe UI", 9), bg=self.bg_dark, fg=self.text_secondary)
        self.lbl_status.pack(pady=(10, 20))

        # Keyboard shortcuts
        self.root.bind("+", lambda e: self.add_time())
        self.root.bind("-", lambda e: self.reduce_time())
        self.root.bind("q", lambda e: self.stop_timer())
        self.root.bind("<Return>", lambda e: self.start_timer())

    def fmt(self, seconds):
        m, s = divmod(int(seconds), 60)
        return f"{m:02d}:{s:02d}"

    def start_timer(self):
        if self.running:
            return

        try:
            actual = int(self.entry_actual.get())
            display = int(self.entry_display.get())
            if actual <= 0 or display <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter positive numbers for both times.")
            return

        self.actual_total = actual * 60
        self.display_total = display * 60
        self.actual_left = self.actual_total
        self.display_left = self.display_total
        self.speed = self.display_left / self.actual_left
        self.running = True

        # Disable inputs, enable controls
        self.entry_actual.config(state="disabled")
        self.entry_display.config(state="disabled")
        self.btn_start.config(state="disabled", bg="#444")
        self.btn_add.config(state="normal")
        self.btn_sub.config(state="normal")
        self.btn_stop.config(state="normal", bg=self.accent)

        self.lbl_status.config(text="Timer running — Use [+] [-] keys or buttons")

        # Start tick thread
        tick = threading.Thread(target=self._tick, daemon=True)
        tick.start()

    def _tick(self):
        while self.running and self.actual_left > 0 and self.display_left > 0:
            time.sleep(0.05)
            with self.lock:
                self.actual_left -= 0.05
                self.display_left -= 0.05 * self.speed

                if self.actual_left <= 0 or self.display_left <= 0:
                    self.actual_left = max(0, self.actual_left)
                    self.display_left = max(0, self.display_left)
                    self.running = False
                    self.root.after(0, self.on_complete)
                    break

            # Update UI from main thread
            self.root.after(0, self.update_ui)

    def update_ui(self):
        self.lbl_display_big.config(text=self.fmt(self.display_left))
        self.lbl_actual.config(text=f"Actual: {self.fmt(self.actual_left)}")
        self.lbl_speed.config(text=f"Speed: {self.speed:.3f}x")

    def add_time(self):
        if not self.running:
            return
        with self.lock:
            self.display_left += 60
            self.actual_left += 120
        self.recalc_speed()
        self.lbl_status.config(text=f"[+] Added — New speed: {self.speed:.3f}x")
        self.update_ui()

    def reduce_time(self):
        if not self.running:
            return
        with self.lock:
            self.display_left = max(0, self.display_left - 60)
        self.recalc_speed()
        self.lbl_status.config(text=f"[-] Reduced — New speed: {self.speed:.3f}x")
        self.update_ui()

    def recalc_speed(self):
        with self.lock:
            if self.actual_left > 0:
                self.speed = self.display_left / self.actual_left

    def stop_timer(self):
        self.running = False
        self.entry_actual.config(state="normal")
        self.entry_display.config(state="normal")
        self.btn_start.config(state="normal", bg=self.accent)
        self.btn_add.config(state="disabled")
        self.btn_sub.config(state="disabled")
        self.btn_stop.config(state="disabled", bg="#555")
        self.lbl_status.config(text="Timer stopped — Press Start to run again")

    def on_complete(self):
        self.stop_timer()
        self.lbl_display_big.config(text="DONE!")
        self.lbl_status.config(text="✓ Timer complete!")
        messagebox.showinfo("Timer Complete", "Countdown finished!")


if __name__ == "__main__":
    root = tk.Tk()
    app = PremiumTimerApp(root)
    root.mainloop()
