![image](https://github.com/user-attachments/assets/86d83453-a511-485f-bd15-37e69ba9f417)

A Python-based Script Manager that provides a modern, graphical user interface (GUI) to manage your Python scripts with ease. This application enables you to add, start, stop, restart, and remove scripts—all from a single, user-friendly interface.

Overview
The Script Manager is designed to simplify the process of running and managing multiple Python scripts. Whether you’re a developer looking to streamline testing, a hobbyist automating tasks, or an operations engineer managing routine scripts, this tool offers an intuitive way to handle script execution without needing to switch between command line windows.

Key components include:

GUI Built with Tkinter and ttk: A modern, responsive interface with a table-like view (Treeview) displaying script details.
Process Management with psutil and subprocess: Seamlessly start, stop, and monitor Python script processes.
Persistent Configuration: Script paths and statuses are stored in a JSON file, ensuring your configuration is saved across sessions.
Cross-Platform Compatibility: Automatically adapts to Windows and Unix-like systems for launching Python scripts.
Features
Add Scripts: Easily add new Python scripts via a file dialog.
Script Execution: Start, stop, and restart individual scripts.
Batch Operations: Start or stop all scripts with a single click.
Real-Time Status Monitoring: Displays the current status (Running/Stopped) of each script.
Interactive Table Display: Uses Tkinter’s Treeview for a structured, table-like presentation.
Contextual Actions: Right-click context menu for quick operations (start, stop, restart) and double-click toggling.
Persistent Storage: Saves script information in a JSON file (script_status.json), ensuring that your setup persists between sessions.
Clean & Modern UI: Utilizes Tkinter’s themed widgets (ttk) and a customizable layout for an enhanced user experience.
Cross-Platform: Adapts to both Windows and Unix-like systems, managing differences in process creation and command invocation.
Technologies Used
Python 3.x: The programming language used to build the application.
Tkinter & ttk: For constructing the graphical user interface.
psutil: To monitor and manage script processes.
subprocess: To launch scripts as background processes.
JSON: For saving and loading script configuration data.
platform: To detect the operating system and adjust command invocations accordingly.
Installation
Clone the Repository:

bash
Copy
Edit
git clone https://github.com/your-username/script-manager.git
cd script-manager
Create a Virtual Environment (Optional but Recommended):

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install Dependencies: The only external dependency is psutil. Install it using pip:

bash
Copy
Edit
pip install psutil
Run the Application:

bash
Copy
Edit
python script_manager.py
Usage
Adding a Script:
Click the "Add Script" button or select it from the File menu.
Choose a Python script file (*.py) from your file system.
Managing Scripts:
Use the Treeview to see a list of all added scripts along with their folder paths and current status.
Right-click on a script to open the context menu and choose to start, stop, or restart it.
Double-click a script row to toggle its state (start if stopped, stop if running).
Batch Operations:
Use the "Start All" or "Stop All" buttons in the toolbar to manage all scripts simultaneously.
Removing Scripts:
Select one or more scripts in the Treeview and click the "Remove Script" button to delete them from the manager.
Refreshing Status:
Click the "Refresh Status" button to update the running status of all scripts.
Configuration
Persistent Storage:
Script information is stored in script_status.json. This file is automatically updated when you add, remove, or change the status of scripts.

Platform-Specific Handling:
The application uses the platform module to detect the operating system and adjust how scripts are launched:

On Windows, it uses subprocess.CREATE_NO_WINDOW to run scripts without opening an extra window.
On Unix-like systems, it suppresses script output using subprocess.DEVNULL.
Contributing
Contributions are welcome! If you’d like to enhance the Script Manager, please follow these steps:

Fork the Repository: Click the "Fork" button on GitHub.
Create a Feature Branch:
bash
Copy
Edit
git checkout -b feature/YourFeature
Commit Your Changes:
bash
Copy
Edit
git commit -m "Add Your Feature"
Push to Your Fork:
bash
Copy
Edit
git push origin feature/YourFeature
Open a Pull Request: Submit your pull request for review.
For any major changes, please open an issue first to discuss what you would like to change.

License
This project is licensed under the MIT License. Feel free to use, modify, and distribute it as per the license terms.

Future Enhancements
Enhanced Error Handling: More robust mechanisms to handle process errors and logging.
Customizable Themes: Allow users to customize the UI theme and colors.
Notification System: Implement desktop notifications for script status changes.
Advanced Scheduling: Integrate scheduling features to automate script execution at specified times.
Multi-User Support: Extend the application to support multi-user environments with authentication.

