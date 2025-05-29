WLFK Tool - Windows/Linux/macOS Fix Kit

The WLFK (Windows/Linux/macOS Fix Kit) Tool is a Python-based graphical utility designed to help users troubleshoot and manage their Windows, Linux, and macOS operating systems. It provides a user-friendly interface built with Tkinter to execute common system commands, making system maintenance and diagnostics more accessible.
Features

    Cross-Platform Support: Dedicated sections for Windows (Vista to 11), various Linux distributions (Ubuntu/Debian, Fedora, Arch, OpenSUSE, Generic), and macOS.

    Intuitive GUI: A clean and modern user interface inspired by Windows 11 design principles, featuring smooth button animations and clear visual feedback.

    Extensive Command Library: A curated list of common and useful commands for each operating system, covering areas like system file checks, disk management, network diagnostics, package management, and more.

    Real-time Output: Displays the output of executed commands directly within the application's console-like text area.

    Copy Output: Easily copy the command output to your clipboard for further analysis or sharing.

    Administrator/Root Privilege Prompt: On Windows, the tool automatically attempts to elevate its privileges if not run as Administrator. For Linux/macOS, clear instructions are provided on how to run the tool with sudo.

    Loading Animations: Visual indicators appear while commands are executing, providing a better user experience.

How to Run

    Save the Code: Save the Python code (e.g., WLFK1.py) to a location on your computer.

    Open Terminal/Command Prompt:

        Windows: Open the Start Menu, type cmd, and press Enter.

        Linux/macOS: Open your preferred terminal application.

    Navigate to the Directory: Use the cd command to navigate to the directory where you saved WLFK1.py.

        Example: cd /home/sarigs/Desktop/AbramichS/Windows or Linux Fix Kit Tool WLFK Tool/

    Execute the Tool with Privileges:

        Windows:
        Right-click on the WLFK1.py file in File Explorer and select "Run as administrator".
        (The tool includes an automatic elevation request, but direct elevation is often more reliable.)

        Linux / macOS:
        Run the script using sudo from your terminal:

        sudo python3 WLFK1.py

        (You might need to replace python3 with python depending on your system's Python setup.)

Usage

    Select Your OS: On the main screen, click the button corresponding to your operating system (Windows, Linux, or macOS).

    Choose Version/Distribution: For Windows and Linux, select your specific version or distribution from the dropdown menu.

    Select a Command: A list of relevant commands will appear. Choose the one you wish to execute.

    Run Command: Click the "Run Selected Command" button. The output will be displayed in the console area.

    Copy Output: Use the "Copy Output" button to copy the results to your clipboard.

Important Notes & Troubleshooting

    Administrator/Root Privileges are CRITICAL: Many system-level commands require elevated permissions. If a command fails with "Access Denied" or "Operation not permitted" errors, it's almost certainly because the WLFK Tool itself was not run with Administrator (Windows) or root (sudo on Linux/macOS) privileges.

    sudo Command: The sudo command is exclusive to Linux and macOS. Do NOT attempt to use sudo within a Windows command. If you select a Linux/macOS command that starts with sudo while running the tool on Windows, it will result in a "command not found" error.

    "Command not found" Errors:

        Ensure you have selected the correct operating system (Windows, Linux, or macOS) within the tool for your current environment.

        Verify that the command you are trying to run is actually installed and available in your system's PATH. Some commands (e.g., gnome-disks on Linux, brew on macOS) might require additional software installations.

    GUI Applications: Some commands (e.g., rstrui.exe on Windows, gnome-disks on Linux) will launch separate graphical applications. The WLFK Tool will indicate that it has launched the application, but the interaction will happen in the new window.

    Disk Operations: Commands involving chkdsk or fsck often require the target partition to be unmounted. Please read the output carefully for instructions.

Credits

Created by AbramichS inc. 2015-2025
