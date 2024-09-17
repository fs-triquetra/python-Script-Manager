import os
import subprocess
import psutil
import json
import tkinter as tk
from tkinter import filedialog, messagebox
import platform

# File to store script paths
STATUS_FILE = 'script_status.json'

# Dictionary to hold the scripts and their file paths
SCRIPTS = {}
# Dictionary to hold process IDs for scripts
PROCESS_IDS = {}
# Dictionary to hold status labels for the GUI
status_labels = {}

# Load script paths from JSON file
def load_statuses():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as f:
            scripts = json.load(f)
            return scripts
    else:
        return {}

# Save script paths to JSON file
def save_statuses():
    with open(STATUS_FILE, 'w') as f:
        json.dump({name: {'path': data['path']} for name, data in SCRIPTS.items()}, f)

# Terminate any existing processes for the script
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
        except psutil.NoSuchProcess:
            del PROCESS_IDS[script_name]
        except psutil.AccessDenied:
            pass
    return False

# Start a script in the background and suppress its output
def start_script(script_name):
    script_path = SCRIPTS[script_name]['path']
    try:
        if platform.system() == "Windows":
            process = subprocess.Popen(['python', script_path], creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            process = subprocess.Popen(['python3', script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        PROCESS_IDS[script_name] = process.pid
        # Update the status in-memory
        update_status_label(script_name, "Running")
        save_statuses()
        print(f"Script {script_name} was successfully started")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start {script_name}: {e}")
        update_status_label(script_name, "Error")

# Stop a running script
def stop_script(script_name):
    if terminate_script(script_name):
        # Update the status in-memory
        update_status_label(script_name, "Stopped")
    else:
        update_status_label(script_name, "Error")
    save_statuses()

# Restart a script
def restart_script(script_name):
    stop_script(script_name)
    start_script(script_name)

# Stop all scripts
def stop_all_scripts():
    for script_name in list(SCRIPTS.keys()):
        stop_script(script_name)

# Start all scripts
def start_all_scripts():
    for script_name in list(SCRIPTS.keys()):
        start_script(script_name)

# Remove selected scripts
def remove_scripts(script_names):
    for script_name in script_names:
        if script_name in SCRIPTS:
            stop_script(script_name)  # Stop the script before removing
            del SCRIPTS[script_name]
            if script_name in PROCESS_IDS:
                del PROCESS_IDS[script_name]
    save_statuses()
    update_status_labels()

# Display script manager popup
def manage_scripts_popup():
    global root
    popup = tk.Toplevel(root)
    popup.title("Manage Scripts")
    popup.geometry("400x300")
    popup.config(bg="black")

    # Listbox to display available scripts
    script_listbox = tk.Listbox(popup, selectmode=tk.MULTIPLE, bg="gray", fg="white", font=("Arial", 10))
    script_listbox.pack(pady=10, fill="both", expand=True)

    # Populate the listbox with numbered script names
    for idx, script_name in enumerate(SCRIPTS, start=1):
        script_listbox.insert(tk.END, f"{idx}. {script_name}")

    # Function to delete selected scripts
    def delete_selected_scripts():
        selected_indices = script_listbox.curselection()
        selected_scripts = [script_listbox.get(i).split('. ', 1)[1] for i in selected_indices]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected scripts?"):
            remove_scripts(selected_scripts)
            popup.destroy()

    # Delete button
    delete_button = tk.Button(popup, text="Delete Selected", command=delete_selected_scripts, bg="red", fg="white", font=("Arial", 10))
    delete_button.pack(pady=10)

    # Cancel button
    cancel_button = tk.Button(popup, text="Cancel", command=popup.destroy, bg="gray", fg="white", font=("Arial", 10))
    cancel_button.pack(pady=5)

    # Populate the listbox with script names
    for script_name in SCRIPTS:
        script_listbox.insert(tk.END, script_name)

    # Function to delete selected scripts
    def delete_selected_scripts():
        selected_indices = script_listbox.curselection()
        selected_scripts = [script_listbox.get(i) for i in selected_indices]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected scripts?"):
            remove_scripts(selected_scripts)
            popup.destroy()

    # Delete button
    delete_button = tk.Button(popup, text="Delete Selected", command=delete_selected_scripts, bg="red", fg="white", font=("Arial", 10))
    delete_button.pack(pady=10)

    # Cancel button
    cancel_button = tk.Button(popup, text="Cancel", command=popup.destroy, bg="gray", fg="white", font=("Arial", 10))
    cancel_button.pack(pady=5)

    def delete_selected_scripts():
        selected_indices = script_listbox.curselection()
        selected_scripts = [script_listbox.get(i) for i in selected_indices]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected scripts?"):
            remove_scripts(selected_scripts)
            popup.destroy()

    delete_button = tk.Button(popup, text="Delete Selected", command=delete_selected_scripts, bg="red", fg="white", font=("Arial", 10))
    delete_button.pack(pady=10)

# Add a new script to the list
def add_new_script():
    file_path = filedialog.askopenfilename(
        title="Select Script",
        filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
    )
    
    if file_path:
        script_name = os.path.basename(file_path)
        if script_name not in SCRIPTS:
            folder = os.path.dirname(file_path)
            SCRIPTS[script_name] = {'path': file_path}
            add_script_to_gui(script_name, folder)

# Add a script to the GUI
def add_script_to_gui(script_name, folder):
    script_row = tk.Frame(script_frame, bg="black")
    script_row.pack(fill="x", padx=20, pady=5)

    # Folder label
    folder_label = tk.Label(script_row, text=folder, font=("Arial", 10), bg="black", fg="white", width=30, anchor="w")
    folder_label.pack(side="left", padx=5)

    # Script name label
    script_label = tk.Label(script_row, text=script_name, font=("Arial", 10), bg="black", fg="white", width=30, anchor="w")
    script_label.pack(side="left", padx=5)

    # Status label
    status_label = tk.Label(script_row, text="Stopped", font=("Arial", 10), width=10, bg="orange", fg="black")
    status_label.pack(side="left", padx=5)
    status_labels[script_name] = status_label

    # Button frame for start and stop buttons
    button_frame = tk.Frame(script_row, bg="black")
    button_frame.pack(side="left", padx=5)

    # Start button
    start_button = tk.Button(button_frame, text="Start", font=("Arial", 10), bg="green", fg="white", command=lambda name=script_name: start_script(name))
    start_button.pack(side="left", padx=5)

    # Stop button
    stop_button = tk.Button(button_frame, text="Stop", font=("Arial", 10), bg="red", fg="white", command=lambda name=script_name: stop_script(name))
    stop_button.pack(side="left", padx=5)

    update_status_labels()

# Update status labels in the GUI
def update_status_labels():
    for script_name in SCRIPTS:
        status = check_status(script_name)
        update_status_label(script_name, status)

# Update the status label of a single script
def update_status_label(script_name, status):
    if script_name in status_labels:
        if status == "Running":
            status_labels[script_name].config(text="Running", bg="green", fg="white")
        elif status == "Stopped":
            status_labels[script_name].config(text="Stopped", bg="orange", fg="black")
        else:
            status_labels[script_name].config(text="Error", bg="red", fg="white")

# Check the status of a script
def check_status(script_name):
    pid = PROCESS_IDS.get(script_name)
    if pid:
        try:
            proc = psutil.Process(pid)
            if proc.is_running():
                return "Running"
        except psutil.NoSuchProcess:
            # Process is no longer available
            del PROCESS_IDS[script_name]
    return "Stopped"

# Create the GUI window
def create_gui():
    global root, script_frame
    root = tk.Tk()
    root.title("Script Manager")
    root.geometry("800x600")
    root.config(bg="black")

    # Title
    title_label = tk.Label(root, text="Script Manager", font=("Arial", 16), bg="black", fg="white")
    title_label.pack(pady=10)

    # Button frame for top buttons
    top_button_frame = tk.Frame(root, bg="black")
    top_button_frame.pack(pady=10, fill="x")

    # Select script button
    select_button = tk.Button(top_button_frame, text="Select Script", font=("Arial", 12), bg="blue", fg="white", command=add_new_script)
    select_button.pack(side="left", padx=10)

    # Restart All button
    restart_all_button = tk.Button(top_button_frame, text="Restart All", font=("Arial", 12), bg="yellow", fg="black", command=start_all_scripts)
    restart_all_button.pack(side="left", padx=10)

    # Stop All button
    stop_all_button = tk.Button(top_button_frame, text="Stop All", font=("Arial", 12), bg="red", fg="white", command=stop_all_scripts)
    stop_all_button.pack(side="left", padx=10)

    # Remove button
    remove_button = tk.Button(top_button_frame, text="Remove", font=("Arial", 12), bg="gray", fg="white", command=manage_scripts_popup)
    remove_button.pack(side="left", padx=10)

    # Frame to hold the scripts
    script_frame = tk.Frame(root, bg="black")
    script_frame.pack(pady=10, fill="both", expand=True)

    # Refresh button to update statuses
    refresh_button = tk.Button(root, text="Refresh Status", font=("Arial", 12), bg="cyan", fg="black", command=update_status_labels)
    refresh_button.pack(pady=10)

    # Load existing scripts into GUI
    for script_name, data in SCRIPTS.items():
        folder = os.path.dirname(data['path'])
        add_script_to_gui(script_name, folder)

    root.mainloop()

# Main function to launch the GUI
def main():
    global SCRIPTS
    # Load existing script paths from file
    SCRIPTS = load_statuses()

    # Create and run the GUI
    create_gui()

if __name__ == "__main__":
    main()
