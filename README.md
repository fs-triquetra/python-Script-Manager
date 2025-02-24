![image](https://github.com/user-attachments/assets/86d83453-a511-485f-bd15-37e69ba9f417)

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

# 🛠️ Python Script Manager

A modern, graphical user interface (GUI) tool to manage your Python scripts with ease. Whether you're a developer streamlining testing, a hobbyist automating tasks, or an operations engineer managing routine scripts, this application offers an intuitive way to run and control multiple Python scripts from one unified interface.

---

## 🔍 Overview

The **Python Script Manager** is designed to simplify script management by providing:

- **GUI Built with Tkinter & ttk:**  
  A responsive, table-like view (Treeview) displaying script details in a clean, modern layout.

- **Process Management with psutil & subprocess:**  
  Seamlessly start, stop, restart, and monitor your scripts.

- **Persistent Configuration:**  
  Script paths and statuses are stored in a JSON file (`script_status.json`), ensuring your setup persists across sessions.

- **Cross-Platform Compatibility:**  
  Automatically adapts to Windows and Unix-like systems, handling differences in process creation and command invocation.

---

## ✨ Features

- **Add Scripts:**  
  Easily add new Python scripts via a file dialog.

- **Script Execution:**  
  Start, stop, and restart individual scripts with simple controls.

- **Batch Operations:**  
  Manage all scripts simultaneously using "Start All" or "Stop All" buttons.

- **Real-Time Status Monitoring:**  
  Displays the current status (Running/Stopped) of each script.

- **Interactive Table Display:**  
  Uses Tkinter’s Treeview for a structured, table-like presentation.

- **Contextual Actions:**  
  Right-click on a script for quick operations and double-click to toggle its state.

- **Persistent Storage:**  
  Automatically saves script information to `script_status.json`.

- **Clean & Modern UI:**  
  Utilizes Tkinter’s themed widgets (ttk) and a customizable layout for an enhanced user experience.

- **Cross-Platform Support:**  
  Adapts seamlessly to both Windows and Unix-like systems.

---

## 🛠 Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/script-manager.git
cd script-manager

Notification System: Implement desktop notifications for script status changes.
Advanced Scheduling: Integrate scheduling features to automate script execution at specified times.
Multi-User Support: Extend the application to support multi-user environments with authentication.

