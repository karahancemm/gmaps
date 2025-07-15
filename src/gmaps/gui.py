import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import queue
import sys, os, tempfile
from gmaps.scraper import run


class ScraperGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Google Maps Scraper')
        self.geometry('600x400')
        self._build_widgets()
        self.log_queue = queue.Queue()
        self._poll_log()

    def _build_widgets(self):
        frm = tk.Frame(self)
        frm.pack(padx = 10, pady = 10, fill = 'x')

        tk.Label(frm, text = 'Place ID: ', width = 12, anchor = 'w').grid(row = 0, column = 0)
        self.place_entry = tk.Entry(frm)
        self.place_entry.grid(row = 0, column = 1, sticky = 'ew')

        tk.Label(frm, text = 'Save CSV to: ', width = 12, anchor = 'w').grid(row= 1, column = 0, pady = (5,0))
        out_frm = tk.Frame(frm)
        out_frm.grid(row = 1, column = 1, sticky = 'ew', pady = (5,0))
        self.out_entry = tk.Entry(out_frm)
        self.out_entry.pack(side = 'left', fill = 'x', expand = True)
        tk.Button(out_frm, text = 'Browse..', command = self._browse).pack(side = 'right')

        frm.columnconfigure(1, weight = 1)

        btn_frm = tk.Frame(self)
        btn_frm.pack(fill = 'x', padx = 10)
        self.run_btn = tk.Button(btn_frm, text = 'Run', command = self._on_run)
        self.run_btn.pack(side = 'left')
        tk.Button(btn_frm, text = 'Exit', command = self.destroy).pack(side = 'right')

        self.log = scrolledtext.ScrolledText(self, state = 'disabled', wrap = 'word')
        self.log.pack(fill = 'both', expand = True, padx = 10, pady = 10)


    def _browse(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV files","*.csv")])
        if path:
            self.out_entry.delete(0, tk.END)
            self.out_entry.insert(0, path)

    def _on_run(self):
        place = self.place_entry.get().strip()
        out   = self.out_entry.get().strip()
        if not place or not out:
            messagebox.showerror("Error", "Both Place ID and output path are required.")
            return

        self.run_btn.config(state="disabled")
        threading.Thread(target=self._worker, args=(place, out), daemon=True).start()

    def _worker(self, place, out):
        # hijack stdout so prints go to our queue
        old_stdout = sys.stdout
        sys.stdout = self
        try:
            print(f"▶ Scraping {place!r} …")
            run(place, out)
            print("✅ Completed!")
        except Exception as e:
            print("❌ Error:", e)
        finally:
            sys.stdout = old_stdout
            self.log_queue.put(("ENABLE_BUTTON", None))

    # file-like interface: GUI can be sys.stdout
    def write(self, msg):
        self.log_queue.put(("LOG", msg))

    def flush(self):
        pass

    def _poll_log(self):
        try:
            while True:
                typ, msg = self.log_queue.get_nowait()
                if typ == "LOG":
                    self.log.config(state="normal")
                    self.log.insert("end", msg)
                    self.log.see("end")
                    self.log.config(state="disabled")
                elif typ == "ENABLE_BUTTON":
                    self.run_btn.config(state="normal")
        except queue.Empty:
            pass
        self.after(100, self._poll_log)


