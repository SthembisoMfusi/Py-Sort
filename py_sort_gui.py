#!/usr/bin/env python3
"""
File Organizer GUI
A minimal Tkinter interface for py_sort.py

Features:
- Select folder to organize
- Run py_sort.py as a subprocess
- Show live progress log
- No external dependencies
"""

import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import subprocess
import threading
import sys
import os

class OrganizerGUI:
    def __init__(self, master):
        self.master = master
        master.title("File Organizer")
        master.geometry("650x450")
        master.resizable(False, False)

        self.folder_path = tk.StringVar()

        # --- Folder selection ---
        tk.Label(master, text="Select folder to organize:", font=("Arial", 11, "bold")).pack(pady=5)
        frame = tk.Frame(master)
        frame.pack(pady=5)

        self.entry = tk.Entry(frame, textvariable=self.folder_path, width=60)
        self.entry.pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Browse", command=self.browse_folder).pack(side=tk.LEFT)

        # --- Options ---
        self.dry_run = tk.BooleanVar(value=False)
        self.undo = tk.BooleanVar(value=False)
        tk.Checkbutton(master, text="Dry Run (preview only)", variable=self.dry_run).pack(anchor="w", padx=15)
        tk.Checkbutton(master, text="Undo last organization", variable=self.undo).pack(anchor="w", padx=15)

        # --- Run button ---
        tk.Button(master, text="Run Organizer", command=self.run_organizer, bg="#2d7", fg="white",
                  font=("Arial", 10, "bold"), width=20).pack(pady=10)

        # --- Progress area ---
        tk.Label(master, text="Progress:", font=("Arial", 11, "bold")).pack(pady=3)
        self.log_area = scrolledtext.ScrolledText(master, height=15, width=80, state=tk.DISABLED)
        self.log_area.pack(padx=10, pady=5)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def append_log(self, text):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, text + "\n")
        self.log_area.yview(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def run_organizer(self):
        folder = self.folder_path.get().strip()
        if not folder:
            messagebox.showwarning("Missing Folder", "Please select a folder first.")
            return

        if not os.path.exists("py_sort.py"):
            messagebox.showerror("Error", "py_sort.py not found in this directory.")
            return

        self.log_area.config(state=tk.NORMAL)
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state=tk.DISABLED)

        self.append_log(f"Starting organization in: {folder}")
        self.append_log("=======================================")

        args = [sys.executable, "py_sort.py", folder]

        if self.dry_run.get():
            args.append("--dry-run")
        if self.undo.get():
            args.append("--undo")

        thread = threading.Thread(target=self.run_subprocess, args=(args,))
        thread.daemon = True
        thread.start()

    def run_subprocess(self, args):
        try:
            process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                self.append_log(line.strip())
            process.wait()
            if process.returncode == 0:
                self.append_log("=======================================")
                self.append_log("✔ Done.")
            else:
                self.append_log("⚠ Organizer exited with errors.")
        except Exception as e:
            self.append_log(f"Error running py_sort.py: {e}")

def main():
    root = tk.Tk()
    app = OrganizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    try:
        import tkinter as tk
        root = tk.Tk()
        root.destroy()
        main()
    except tk.TclError:
        print(
            "⚠️ GUI cannot be launched: no display found.\n"
            "Please run this program on your local machine, not in a headless or remote environment."
        )
