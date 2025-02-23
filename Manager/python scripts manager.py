import os
import subprocess
import psutil
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import platform

# File to store script paths
STATUS_FILE = 'script_status.json'

# Global dictionaries to hold scripts and process IDs
SCRIPTS = {}
PROCESS_IDS = {}

def load_statuses():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_statuses():
    with open(STATUS_FILE, 'w') as f:
        json.dump({name: {'path': data['path']} for name, data in SCRIPTS.items()}, f, indent=4)

def terminate_script(script_name):
    pid = PROCESS_IDS.get(script_name)
    if pid:
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            proc.wait(timeout=5)
            if proc.is_running():
                proc.kill()
            del PROCESS_IDS[script_name]
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            if script_name in PROCESS_IDS:
                del PROCESS_IDS[script_name]
    return False

def start_script(script_name):
    script_path = SCRIPTS[script_name]['path']
    try:
        if platform.system() == "Windows":
            process = subprocess.Popen(['python', script_path],
                                       creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            process = subprocess.Popen(['python3', script_path],
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        PROCESS_IDS[script_name] = process.pid
        save_statuses()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start {script_name}: {e}")

def stop_script(script_name):
    if terminate_script(script_name):
        pass
    else:
        messagebox.showerror("Error", f"Failed to stop {script_name}")
    save_statuses()

def restart_script(script_name):
    stop_script(script_name)
    start_script(script_name)

def stop_all_scripts():
    for script_name in list(SCRIPTS.keys()):
        stop_script(script_name)

def start_all_scripts():
    for script_name in list(SCRIPTS.keys()):
        start_script(script_name)

def remove_scripts(script_names):
    for script_name in script_names:
        stop_script(script_name)
        if script_name in SCRIPTS:
            del SCRIPTS[script_name]
        if script_name in PROCESS_IDS:
            del PROCESS_IDS[script_name]
    save_statuses()

# ------------------- GUI using ttk -------------------
class ScriptManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Script Manager")
        self.geometry("900x600")
        self.configure(bg="#2e2e2e")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.create_widgets()
        self.load_scripts()

    def create_widgets(self):
        # Menu
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Add Script", command=self.add_script)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

        # Toolbar Frame for buttons
        toolbar = tk.Frame(self, bg="#3e3e3e")
        toolbar.pack(side="top", fill="x", padx=10, pady=5)

        add_btn = tk.Button(toolbar, text="Add Script", command=self.add_script,
                            bg="#4CAF50", fg="white", font=("Arial", 10))
        add_btn.pack(side="left", padx=5)

        start_all_btn = tk.Button(toolbar, text="Start All", command=start_all_scripts,
                                  bg="#2196F3", fg="white", font=("Arial", 10))
        start_all_btn.pack(side="left", padx=5)

        stop_all_btn = tk.Button(toolbar, text="Stop All", command=stop_all_scripts,
                                 bg="#f44336", fg="white", font=("Arial", 10))
        stop_all_btn.pack(side="left", padx=5)

        remove_btn = tk.Button(toolbar, text="Remove Script", command=self.remove_selected_scripts,
                               bg="#9E9E9E", fg="white", font=("Arial", 10))
        remove_btn.pack(side="left", padx=5)

        refresh_btn = tk.Button(toolbar, text="Refresh Status", command=self.refresh_status,
                                bg="#00BCD4", fg="white", font=("Arial", 10))
        refresh_btn.pack(side="left", padx=5)

        # Treeview for scripts
        columns = ("Script", "Folder", "Status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="extended")
        self.tree.heading("Script", text="Script")
        self.tree.heading("Folder", text="Folder")
        self.tree.heading("Status", text="Status")
        self.tree.column("Script", width=200)
        self.tree.column("Folder", width=400)
        self.tree.column("Status", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Bind right-click for context menu and double-click for toggle action
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Double-1>", self.on_double_click)

        # Right-click context menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Start", command=lambda: self.context_action("start"))
        self.context_menu.add_command(label="Stop", command=lambda: self.context_action("stop"))
        self.context_menu.add_command(label="Restart", command=lambda: self.context_action("restart"))

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Welcome to Script Manager")
        status_bar = tk.Label(self, textvariable=self.status_var, bd=1, relief="sunken",
                              anchor="w", bg="#404040", fg="white")
        status_bar.pack(side="bottom", fill="x")

    def load_scripts(self):
        global SCRIPTS
        SCRIPTS = load_statuses()
        self.refresh_tree()

    def refresh_tree(self):
        # Clear the tree view and insert updated scripts
        for item in self.tree.get_children():
            self.tree.delete(item)
        for script_name, data in SCRIPTS.items():
            folder = os.path.dirname(data['path'])
            status = self.get_script_status(script_name)
            self.tree.insert("", "end", iid=script_name, values=(script_name, folder, status))

    def get_script_status(self, script_name):
        pid = PROCESS_IDS.get(script_name)
        if pid:
            try:
                proc = psutil.Process(pid)
                if proc.is_running():
                    return "Running"
            except psutil.NoSuchProcess:
                if script_name in PROCESS_IDS:
                    del PROCESS_IDS[script_name]
        return "Stopped"

    def refresh_status(self):
        for script in SCRIPTS:
            status = self.get_script_status(script)
            self.tree.set(script, column="Status", value=status)
        self.status_var.set("Status refreshed.")

    def add_script(self):
        file_path = filedialog.askopenfilename(
            title="Select Script",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
        )
        if file_path:
            script_name = os.path.basename(file_path)
            if script_name in SCRIPTS:
                messagebox.showinfo("Info", "Script already added.")
            else:
                SCRIPTS[script_name] = {'path': file_path}
                save_statuses()
                self.refresh_tree()
                self.status_var.set(f"Added {script_name}")

    def remove_selected_scripts(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "No script selected.")
            return
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to remove the selected scripts?")
        if confirm:
            for script_name in selected_items:
                remove_scripts([script_name])
            self.refresh_tree()
            self.status_var.set("Selected scripts removed.")

    def show_context_menu(self, event):
        selected_item = self.tree.identify_row(event.y)
        if selected_item:
            self.tree.selection_set(selected_item)
            self.context_menu.post(event.x_root, event.y_root)

    def context_action(self, action):
        selected_items = self.tree.selection()
        if not selected_items:
            return
        for script_name in selected_items:
            if action == "start":
                start_script(script_name)
            elif action == "stop":
                stop_script(script_name)
            elif action == "restart":
                restart_script(script_name)
        self.refresh_tree()
        self.status_var.set(f"Action '{action}' executed on selected scripts.")

    def on_double_click(self, event):
        # Toggle start/stop on double-click based on current status
        item = self.tree.identify_row(event.y)
        if item:
            current_status = self.tree.set(item, "Status")
            if current_status == "Running":
                stop_script(item)
            else:
                start_script(item)
            self.refresh_tree()

if __name__ == "__main__":
    app = ScriptManagerApp()
    app.mainloop()
