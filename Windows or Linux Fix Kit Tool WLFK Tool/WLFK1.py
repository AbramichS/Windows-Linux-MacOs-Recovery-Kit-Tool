import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import platform
import subprocess
import threading
import os
import sys

# --- Administrator Elevation Check (Windows Only) ---
# This section attempts to re-run the script with administrator privileges on Windows
# if it's not already running as administrator.
if platform.system() == "Windows":
    try:
        import ctypes
        # Check if the current process is elevated
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if not is_admin:
            # If not admin, try to re-run the script with 'runas' verb
            # This will trigger the UAC prompt
            script_path = os.path.abspath(sys.argv[0])
            # Use ShellExecuteW for better handling of paths with spaces
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{script_path}"', None, 1
            )
            sys.exit(0) # Exit the current non-elevated process
    except Exception as e:
        # Handle cases where ctypes or elevation fails (e.g., non-Windows, or permission issues)
        # For simplicity, we just print an error and continue without elevation.
        # A more robust app might show a user-friendly error message.
        print(f"Failed to check/request admin privileges: {e}")
# --- End of Administrator Elevation Check ---


class WLFKTool:
    def __init__(self, master):
        self.master = master
        master.title("WLFK Tool - Windows/Linux/macOS Fix Kit")
        master.geometry("950x750") # Slightly larger default size for more content
        master.resizable(True, True) # Allow resizing

        # Configure default styles for a smoother, 'Windows 11-inspired' look
        self.style = ttk.Style()
        self.style.theme_use('clam') # 'clam' is a good base for customization
        
        # Define a custom color palette for a modern, clean look (Windows 11 inspired)
        self.primary_bg = '#f3f6fc' # Very light blue-gray background
        self.secondary_bg = '#e0e7f2' # Slightly darker for frames/sections
        self.text_color = '#2c3e50' # Dark blue-gray for general text
        self.heading_color = '#1a252f' # Even darker for headings
        self.accent_color = '#0078d4' # Windows 11 blue
        self.hover_color = '#005ea6' # Darker blue for button hover
        self.pressed_color = '#00457a' # Even darker for button pressed
        self.output_bg = '#1e1e1e' # Dark background for console output
        self.output_fg = '#00ff00' # Green text for console output (classic console look)
        self.border_color = '#c0c0c0' # Light border for subtle separation

        # General Frame and Label styles
        self.style.configure('TFrame', background=self.primary_bg)
        self.style.configure('TLabel', font=('Inter', 12), background=self.primary_bg, foreground=self.text_color, padding=5)
        self.style.configure('Heading.TLabel', font=('Segoe UI', 24, 'bold'), background=self.primary_bg, foreground=self.heading_color, padding=(0, 20, 0, 15))
        self.style.configure('SubHeading.TLabel', font=('Segoe UI', 18, 'bold'), background=self.primary_bg, foreground=self.heading_color, padding=(0, 15, 0, 10))
        self.style.configure('Info.TLabel', font=('Segoe UI', 11, 'italic'), background=self.primary_bg, foreground='#555555')
        
        # Button styles with enhanced animation (subtle glow/shadow on hover)
        self.style.configure('TButton', font=('Segoe UI', 13, 'bold'), padding=(18, 12), 
                             background=self.accent_color, foreground='white', 
                             borderwidth=0, relief='flat', 
                             focusthickness=2, focuscolor=self.hover_color)
        self.style.map('TButton',
                       background=[('active', self.hover_color), ('pressed', self.pressed_color)],
                       foreground=[('active', 'white'), ('pressed', 'white')],
                       relief=[('pressed', 'sunken')],
                       # Add a subtle border/shadow effect on hover
                       bordercolor=[('active', self.hover_color)],
                       lightcolor=[('active', self.hover_color)],
                       darkcolor=[('active', self.hover_color)])
        
        # Combobox style
        self.style.configure('TCombobox', font=('Segoe UI', 11), padding=7, fieldbackground='white')
        self.style.map('TCombobox', fieldbackground=[('readonly', 'white')], selectbackground=[('readonly', self.secondary_bg)],
                       selectforeground=[('readonly', self.text_color)])
        
        # ScrolledText (Output Area) style
        self.style.configure('TScrolledtext', font=('Consolas', 10), background=self.output_bg, foreground=self.output_fg, 
                             insertbackground=self.output_fg, borderwidth=1, relief='solid', bordercolor=self.border_color)

        # Main frame to hold all content
        self.main_frame = ttk.Frame(master, padding="35 35 35 35", relief='flat', borderwidth=1, style='TFrame') # Added subtle border
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Initialize loading_label as None, it will be created in show_main_menu
        self.loading_label = None 
        self.loading_animation_id = None # To store the ID for the loading animation loop

        # Call show_main_menu after all initializations and method definitions
        self.show_main_menu()
        
    def clear_frame(self, frame):
        """Clears all widgets from a given frame."""
        for widget in frame.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        """Displays the initial menu with Windows, Linux, MacOS buttons and Credits button."""
        self.clear_frame(self.main_frame)

        # Title
        ttk.Label(self.main_frame, text="WLFK Tool", style='Heading.TLabel').pack(pady=(20, 10))
        ttk.Label(self.main_frame, text="Windows/Linux/macOS Fix Kit", font=('Segoe UI', 15, 'italic'), background=self.primary_bg, foreground=self.text_color).pack(pady=(0, 40))


        ttk.Label(self.main_frame, text="Select Your Operating System", style='SubHeading.TLabel').pack(pady=(0, 25))

        # OS Selection Buttons
        button_frame = ttk.Frame(self.main_frame, style='TFrame')
        button_frame.pack(pady=20)

        # Windows Button
        windows_btn = ttk.Button(button_frame, text="Windows Fix Kit", command=self.show_windows_menu, style='TButton')
        windows_btn.grid(row=0, column=0, padx=20, pady=15)

        # Linux Button
        linux_btn = ttk.Button(button_frame, text="Linux Fix Kit", command=self.show_linux_menu, style='TButton')
        linux_btn.grid(row=0, column=1, padx=20, pady=15)
        
        # MacOS Button
        macos_btn = ttk.Button(button_frame, text="macOS Fix Kit", command=self.show_macos_menu, style='TButton')
        macos_btn.grid(row=0, column=2, padx=20, pady=15)

        # Credits Button
        credits_btn = ttk.Button(self.main_frame, text="Credits", command=self.show_credits, style='TButton')
        credits_btn.pack(pady=30)

        # Current OS Info
        current_os = platform.system()
        ttk.Label(self.main_frame, text=f"Detected OS: {current_os}", style='Info.TLabel').pack(pady=40)
        
        # Create and pack the loading label here for the main menu
        self.loading_label = ttk.Label(self.main_frame, text="", font=('Segoe UI', 11, 'italic'), foreground=self.accent_color, background=self.primary_bg)
        self.loading_label.pack(pady=10) # Ensure it's packed

        # Display initial message about admin/root privileges
        self.display_initial_message()

    def show_credits(self):
        """Displays the credits information."""
        messagebox.showinfo("Credits", "Created by AbramichS inc. 2015-2025")

    def display_initial_message(self):
        """Displays a message about running with admin/root privileges."""
        script_name = os.path.basename(sys.argv[0]) # Get the script's filename
        messagebox.showinfo("WLFK Tool - Important!",
                            "For full functionality and to run many system-level commands, "
                            "please ensure you run this WLFK Tool with Administrator (Windows) "
                            "or root (Linux/macOS via 'sudo') privileges.\n\n"
                            "On Windows: Right-click the Python script and select 'Run as administrator'.\n"
                            f"On Linux/macOS: Run from terminal using 'sudo python {script_name}'.\n\n" # Dynamically use script name
                            "Remember: 'sudo' is a command for Linux/macOS. Do NOT use it on Windows commands.")

    def show_windows_menu(self):
        """Displays the Windows specific menu with version selection and command execution."""
        self.clear_frame(self.main_frame)

        ttk.Label(self.main_frame, text="Windows Fix Kit", style='Heading.TLabel').pack(pady=(10, 25))

        # Back button
        ttk.Button(self.main_frame, text="← Back to Main Menu", command=self.show_main_menu, style='TButton').pack(anchor=tk.NW, padx=15, pady=15)

        # Windows Versions
        ttk.Label(self.main_frame, text="Select Windows Version:", style='TLabel').pack(pady=(10, 5), anchor=tk.W, padx=15)
        self.windows_versions = ["Windows Vista", "Windows 7", "Windows 8/8.1", "Windows 10", "Windows 11"]
        self.selected_windows_version = tk.StringVar()
        self.version_combobox = ttk.Combobox(self.main_frame, textvariable=self.selected_windows_version, values=self.windows_versions, state="readonly", font=('Segoe UI', 11), width=35)
        self.version_combobox.set("Select a version") # Default text
        self.version_combobox.pack(pady=5, anchor=tk.W, padx=15)
        self.version_combobox.bind("<<ComboboxSelected>>", self.update_windows_commands)

        # Command selection
        ttk.Label(self.main_frame, text="Select a Command to Run:", style='TLabel').pack(pady=(10, 5), anchor=tk.W, padx=15)
        self.windows_commands_options = {} # Populated dynamically
        self.selected_windows_command = tk.StringVar()
        self.command_combobox = ttk.Combobox(self.main_frame, textvariable=self.selected_windows_command, state="readonly", font=('Segoe UI', 11), width=70)
        self.command_combobox.set("Select a command")
        self.command_combobox.pack(pady=5, anchor=tk.W, padx=15)

        # Run Command Button
        run_btn = ttk.Button(self.main_frame, text="Run Selected Command", command=self.run_selected_command, style='TButton')
        run_btn.pack(pady=25)
        
        # Create and pack the loading label here for this menu
        self.loading_label = ttk.Label(self.main_frame, text="", font=('Segoe UI', 11, 'italic'), foreground=self.accent_color, background=self.primary_bg)
        self.loading_label.pack(pady=5)

        # Output area
        ttk.Label(self.main_frame, text="Command Output:", style='TLabel').pack(pady=(10, 5), anchor=tk.W, padx=15)
        
        # Frame for output text and copy button
        output_frame = ttk.Frame(self.main_frame, style='TFrame')
        output_frame.pack(expand=True, fill=tk.BOTH, padx=15)

        # Increased height for output text area
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=80, height=20, font=('Consolas', 10), background=self.output_bg, foreground=self.output_fg, insertbackground=self.output_fg)
        self.output_text.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(0, 10))
        self.output_text.config(state=tk.DISABLED) # Make it read-only
        
        copy_btn = ttk.Button(output_frame, text="Copy Output", command=self.copy_output, style='TButton')
        copy_btn.pack(side=tk.RIGHT, anchor=tk.N, pady=5)


    def update_windows_commands(self, event=None):
        """Updates the command combobox based on the selected Windows version."""
        version = self.selected_windows_version.get()
        # Common Windows Fix Commands (placeholders)
        # Note: Many of these require Administrator privileges.
        self.windows_commands_options = {
            "Windows Vista": {
                "System File Checker (SFC)": "sfc /scannow",
                "Check Disk (C:)": "chkdsk C: /f /r",
                "Restore Point (System Restore)": "rstrui.exe", # Opens GUI
                "Network Reset (Winsock)": "netsh winsock reset",
                "IP Configuration Reset": "netsh int ip reset",
                "Flush DNS Cache": "ipconfig /flushdns",
                "View Network Config": "ipconfig /all",
                "View Running Processes": "tasklist",
                "View Active Network Connections": "netstat -ano",
                "Disk Cleanup": "cleanmgr.exe", # Opens GUI
                "System Configuration (msconfig)": "msconfig.exe", # Opens GUI
                "Check System Health": "perfmon /report" # Generates system health report
            },
            "Windows 7": {
                "System File Checker (SFC)": "sfc /scannow",
                "Check Disk (C:)": "chkdsk C: /f /r",
                "Deployment Image Servicing and Management (DISM)": "dism /online /cleanup-image /restorehealth",
                "Restore Point (System Restore)": "rstrui.exe",
                "Network Reset (Winsock)": "netsh winsock reset",
                "IP Configuration Reset": "netsh int ip reset",
                "Flush DNS Cache": "ipconfig /flushdns",
                "View Network Config": "ipconfig /all",
                "View Running Processes": "tasklist",
                "View Active Network Connections": "netstat -ano",
                "System Information": "msinfo32",
                "Disk Cleanup": "cleanmgr.exe",
                "System Configuration (msconfig)": "msconfig.exe",
                "Event Viewer": "eventvwr.msc",
                "Check System Health": "perfmon /report",
                "Run Disk Defragmenter": "defrag C: /U /V"
            },
            "Windows 8/8.1": {
                "System File Checker (SFC)": "sfc /scannow",
                "Check Disk (C:)": "chkdsk C: /f /r",
                "Deployment Image Servicing and Management (DISM)": "dism /online /cleanup-image /restorehealth",
                "Restore Point (System Restore)": "rstrui.exe",
                "Network Reset (Winsock)": "netsh winsock reset",
                "IP Configuration Reset": "netsh int ip reset",
                "Flush DNS Cache": "ipconfig /flushdns",
                "View Network Config": "ipconfig /all",
                "View Running Processes": "tasklist",
                "View Active Network Connections": "netstat -ano",
                "System Information": "msinfo32",
                "Disk Cleanup": "cleanmgr.exe",
                "System Configuration (msconfig)": "msconfig.exe",
                "Event Viewer": "eventvwr.msc",
                "Check System Health": "perfmon /report",
                "Run Disk Defragmenter": "defrag C: /U /V"
            },
            "Windows 10": {
                "System File Checker (SFC)": "sfc /scannow",
                "Check Disk (C:)": "chkdsk C: /f /r",
                "Deployment Image Servicing and Management (DISM)": "dism /online /cleanup-image /restorehealth",
                "Restore Point (System Restore)": "rstrui.exe",
                "Network Reset (Winsock)": "netsh winsock reset",
                "IP Configuration Reset": "netsh int ip reset",
                "Flush DNS Cache": "ipconfig /flushdns",
                "View Network Config": "ipconfig /all",
                "View Running Processes": "tasklist",
                "View Active Network Connections": "netstat -ano",
                "Power Troubleshooter": "msdt.exe -id PowerDiagnostic",
                "Windows Update Troubleshooter": "msdt.exe -id WindowsUpdateDiagnostic",
                "Battery Health Report (Laptops)": "powercfg /batteryreport",
                "DirectX Diagnostic Tool": "dxdiag",
                "Disk Cleanup": "cleanmgr.exe",
                "System Configuration (msconfig)": "msconfig.exe",
                "Event Viewer": "eventvwr.msc",
                "Open Services": "services.msc",
                "Open Device Manager": "devmgmt.msc",
                "Check System Health": "perfmon /report",
                "Run Disk Defragmenter": "defrag C: /U /V"
            },
            "Windows 11": {
                "System File Checker (SFC)": "sfc /scannow",
                "Check Disk (C:)": "chkdsk C: /f /r",
                "Deployment Image Servicing and Management (DISM)": "dism /online /cleanup-image /restorehealth",
                "Restore Point (System Restore)": "rstrui.exe",
                "Network Reset (Winsock)": "netsh winsock reset",
                "IP Configuration Reset": "netsh int ip reset",
                "Flush DNS Cache": "ipconfig /flushdns",
                "View Network Config": "ipconfig /all",
                "View Running Processes": "tasklist",
                "View Active Network Connections": "netstat -ano",
                "Power Troubleshooter": "msdt.exe -id PowerDiagnostic",
                "Windows Update Troubleshooter": "msdt.exe -id WindowsUpdateDiagnostic",
                "Startup Repair": "shutdown /r /o /f /t 0", # Reboots into advanced startup options
                "Battery Health Report (Laptops)": "powercfg /batteryreport",
                "DirectX Diagnostic Tool": "dxdiag",
                "Disk Cleanup": "cleanmgr.exe",
                "System Configuration (msconfig)": "msconfig.exe",
                "Event Viewer": "eventvwr.msc",
                "Open Services": "services.msc",
                "Open Device Manager": "devmgmt.msc",
                "Check System Health": "perfmon /report",
                "Run Disk Defragmenter": "defrag C: /U /V"
            }
        }
        commands = list(self.windows_commands_options.get(version, {}).keys())
        self.command_combobox['values'] = commands
        if commands:
            self.command_combobox.set(commands[0]) # Set first command as default
        else:
            self.command_combobox.set("No commands available")

    def show_linux_menu(self):
        """Displays the Linux specific menu with distribution selection and command execution."""
        self.clear_frame(self.main_frame)

        ttk.Label(self.main_frame, text="Linux Fix Kit", style='Heading.TLabel').pack(pady=(10, 25))

        # Back button
        ttk.Button(self.main_frame, text="← Back to Main Menu", command=self.show_main_menu, style='TButton').pack(anchor=tk.NW, padx=15, pady=15)

        # Linux Distros
        ttk.Label(self.main_frame, text="Select Linux Distribution:", style='TLabel').pack(pady=(10, 5), anchor=tk.W, padx=15)
        self.linux_distros = ["Ubuntu/Debian", "Fedora/CentOS/RHEL", "Arch Linux", "OpenSUSE", "Generic Linux"]
        self.selected_linux_distro = tk.StringVar()
        self.distro_combobox = ttk.Combobox(self.main_frame, textvariable=self.selected_linux_distro, values=self.linux_distros, state="readonly", font=('Segoe UI', 11), width=35)
        self.distro_combobox.set("Select a distribution") # Default text
        self.distro_combobox.pack(pady=5, anchor=tk.W, padx=15)
        self.distro_combobox.bind("<<ComboboxSelected>>", self.update_linux_commands)

        # Command selection
        ttk.Label(self.main_frame, text="Select a Command to Run:", style='TLabel').pack(pady=(10, 5), anchor=tk.W, padx=15)
        self.linux_commands_options = {} # Populated dynamically
        self.selected_linux_command = tk.StringVar()
        self.command_combobox = ttk.Combobox(self.main_frame, textvariable=self.selected_linux_command, state="readonly", font=('Segoe UI', 11), width=70)
        self.command_combobox.set("Select a command")
        self.command_combobox.pack(pady=5, anchor=tk.W, padx=15)

        # Run Command Button
        run_btn = ttk.Button(self.main_frame, text="Run Selected Command", command=self.run_selected_command, style='TButton')
        run_btn.pack(pady=25)
        
        # Create and pack the loading label here for this menu
        self.loading_label = ttk.Label(self.main_frame, text="", font=('Segoe UI', 11, 'italic'), foreground=self.accent_color, background=self.primary_bg)
        self.loading_label.pack(pady=5)

        # Output area
        ttk.Label(self.main_frame, text="Command Output:", style='TLabel').pack(pady=(10, 5), anchor=tk.W, padx=15)
        
        # Frame for output text and copy button
        output_frame = ttk.Frame(self.main_frame, style='TFrame')
        output_frame.pack(expand=True, fill=tk.BOTH, padx=15)

        # Increased height for output text area
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=80, height=20, font=('Consolas', 10), background=self.output_bg, foreground=self.output_fg, insertbackground=self.output_fg)
        self.output_text.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(0, 10))
        self.output_text.config(state=tk.DISABLED) # Make it read-only
        
        copy_btn = ttk.Button(output_frame, text="Copy Output", command=self.copy_output, style='TButton')
        copy_btn.pack(side=tk.RIGHT, anchor=tk.N, pady=5)


    def update_linux_commands(self, event=None):
        """Updates the command combobox based on the selected Linux distribution."""
        distro = self.selected_linux_distro.get()
        # Common Linux Fix Commands (placeholders)
        # Note: Many of these require root/sudo privileges.
        self.linux_commands_options = {
            "Ubuntu/Debian": {
                "Update & Upgrade Packages": "sudo apt update && sudo apt upgrade -y",
                "Clean APT Cache": "sudo apt clean && sudo apt autoremove -y",
                "Fix Broken Packages": "sudo apt install -f",
                "Reconfigure All Packages": "sudo dpkg --configure -a",
                "Check Disk (e.g., /dev/sda1)": "echo 'Remember to unmount partition first: sudo umount /dev/sda1; sudo fsck /dev/sda1'",
                "View System Journal": "journalctl -xe",
                "Follow System Journal (Live)": "journalctl -f",
                "View Running Processes": "ps aux",
                "Restart Networking Service": "sudo systemctl restart networking",
                "List Hardware": "sudo lshw -short",
                "List Disk Partitions": "sudo fdisk -l",
                "Fix Missing Packages": "sudo apt-get update --fix-missing",
                "View Network Connections": "netstat -tulnp",
                "Check Systemd Status": "systemctl status",
                "List Installed Packages": "dpkg -l",
                "Show Disk Usage (Graphical)": "gnome-disks", # Requires gnome-disks to be installed
                "Check for Dead Processes": "ps aux | grep 'Z'", # Z for zombie processes
                "Show Open Files": "lsof -i",
                "Check CPU Usage": "top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\\([0-9.]*\\)%*id.*/\\1/' | awk '{print 100 - $1}'"
            },
            "Fedora/CentOS/RHEL": {
                "Update & Upgrade Packages": "sudo dnf update -y",
                "Clean DNF Cache": "sudo dnf clean all",
                "Check Disk (e.g., /dev/sda1)": "echo 'Remember to unmount partition first: sudo umount /dev/sda1; sudo fsck /dev/sda1'",
                "View System Journal": "journalctl -xe",
                "Follow System Journal (Live)": "journalctl -f",
                "View Running Processes": "ps aux",
                "Restart NetworkManager Service": "sudo systemctl restart NetworkManager",
                "List Hardware": "sudo lshw -short",
                "List Disk Partitions": "sudo fdisk -l",
                "View Network Connections": "netstat -tulnp",
                "Check Systemd Status": "systemctl status",
                "List Installed Packages": "rpm -qa",
                "Check for Dead Processes": "ps aux | grep 'Z'",
                "Show Open Files": "lsof -i",
                "Check CPU Usage": "top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\\([0-9.]*\\)%*id.*/\\1/' | awk '{print 100 - $1}'"
            },
            "Arch Linux": {
                "Update & Upgrade Packages": "sudo pacman -Syu",
                "Clean Pacman Cache": "sudo pacman -Sc",
                "Check Disk (e.g., /dev/sda1)": "echo 'Remember to unmount partition first: sudo umount /dev/sda1; sudo fsck /dev/sda1'",
                "View System Journal": "journalctl -xe",
                "Follow System Journal (Live)": "journalctl -f",
                "View Running Processes": "ps aux",
                "Restart NetworkManager Service": "sudo systemctl restart NetworkManager",
                "List Hardware": "sudo lshw -short",
                "List Disk Partitions": "sudo fdisk -l",
                "View Network Connections": "netstat -tulnp",
                "Check Systemd Status": "systemctl status",
                "List Installed Packages": "pacman -Q",
                "Check for Dead Processes": "ps aux | grep 'Z'",
                "Show Open Files": "lsof -i",
                "Check CPU Usage": "top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\\([0-9.]*\\)%*id.*/\\1/' | awk '{print 100 - $1}'"
            },
            "OpenSUSE": {
                "Update & Upgrade Packages": "sudo zypper update -y",
                "Clean Zypper Cache": "sudo zypper clean",
                "Check Disk (e.g., /dev/sda1)": "echo 'Remember to unmount partition first: sudo umount /dev/sda1; sudo fsck /dev/sda1'",
                "View System Journal": "journalctl -xe",
                "Follow System Journal (Live)": "journalctl -f",
                "View Running Processes": "ps aux",
                "Restart NetworkManager Service": "sudo systemctl restart NetworkManager",
                "List Hardware": "sudo lshw -short",
                "List Disk Partitions": "sudo fdisk -l",
                "View Network Connections": "netstat -tulnp",
                "Check Systemd Status": "systemctl status",
                "List Installed Packages": "rpm -qa",
                "Check for Dead Processes": "ps aux | grep 'Z'",
                "Show Open Files": "lsof -i",
                "Check CPU Usage": "top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\\([0-9.]*\\)%*id.*/\\1/' | awk '{print 100 - $1}'"
            },
            "Generic Linux": {
                "View Disk Usage": "df -h",
                "View Memory Usage": "free -h",
                "List Running Services": "systemctl list-units --type=service --state=running",
                "View Network Interfaces": "ip a",
                "Ping Google": "ping -c 4 google.com",
                "Check DNS Resolution": "nslookup google.com",
                "Check Uptime": "uptime",
                "View Kernel Messages": "dmesg | tail",
                "View CPU Info": "lscpu",
                "View PCI Devices": "lspci -knn",
                "View USB Devices": "lsusb -v",
                "Check for Dead Processes": "ps aux | grep 'Z'",
                "Show Open Files": "lsof -i",
                "Check CPU Usage": "top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\\([0-9.]*\\)%*id.*/\\1/' | awk '{print 100 - $1}'"
            }
        }
        commands = list(self.linux_commands_options.get(distro, {}).keys())
        self.command_combobox['values'] = commands
        if commands:
            self.command_combobox.set(commands[0]) # Set first command as default
        else:
            self.command_combobox.set("No commands available")

    def show_macos_menu(self):
        """Displays the macOS specific menu with command execution."""
        self.clear_frame(self.main_frame)

        ttk.Label(self.main_frame, text="macOS Fix Kit", style='Heading.TLabel').pack(pady=(10, 25))

        # Back button
        ttk.Button(self.main_frame, text="← Back to Main Menu", command=self.show_main_menu, style='TButton').pack(anchor=tk.NW, padx=15, pady=15)

        # Warning for non-macOS users
        if platform.system() != "Darwin": # 'Darwin' is the system name for macOS
            ttk.Label(self.main_frame, text="NOTE: These commands are for macOS. Running them on Windows or Linux will likely result in 'command not found' errors.", 
                      font=('Segoe UI', 11, 'bold'), foreground='red', background=self.primary_bg).pack(pady=(5, 15), padx=15)

        # Command selection
        ttk.Label(self.main_frame, text="Select a Command to Run:", style='TLabel').pack(pady=(10, 5), anchor=tk.W, padx=15)
        self.macos_commands_options = {
            "Software Updates (List)": "softwareupdate --list",
            "Software Updates (Install All)": "sudo softwareupdate --install --all --restart", # May require restart
            "List Disks and Partitions": "diskutil list",
            "Verify Startup Disk": "diskutil verifyVolume /",
            "Repair Disk Permissions (Older macOS)": "sudo diskutil repairPermissions /", # Less relevant in modern macOS
            "Battery Status (Laptops)": "pmset -g batt",
            "System Information": "system_profiler SPSoftwareDataType",
            "Hardware Diagnostics": "system_profiler SPDiagnosticsDataType",
            "Stream System Logs": "log stream --predicate 'processID == 0' --info", # Example, can be very verbose
            "Flush DNS Cache": "sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder",
            "List All Hardware Ports": "networksetup -listallhardwareports",
            "Ping Google": "ping -c 4 google.com",
            "Reset Spotlight Index": "sudo mdutil -E /",
            "Check for Broken Homebrew Packages": "brew doctor", # Requires Homebrew
            "Clean Homebrew Cache": "brew cleanup", # Requires Homebrew
            "View Running Processes (Top)": "top -l 1 | head -n 10",
            "Force Quit Application (Example: Safari)": "killall Safari", # Replace Safari with app name
            "Show Network Configuration": "ifconfig", # or ipconfig for newer macOS
            "List Installed Applications": "ls /Applications"
        }
        self.selected_macos_command = tk.StringVar()
        self.command_combobox = ttk.Combobox(self.main_frame, textvariable=self.selected_macos_command, values=list(self.macos_commands_options.keys()), state="readonly", font=('Segoe UI', 11), width=70)
        self.command_combobox.set("Select a command")
        self.command_combobox.pack(pady=5, anchor=tk.W, padx=15)

        # Run Command Button
        run_btn = ttk.Button(self.main_frame, text="Run Selected Command", command=self.run_selected_command, style='TButton')
        run_btn.pack(pady=25)
        
        # Create and pack the loading label here for this menu
        self.loading_label = ttk.Label(self.main_frame, text="", font=('Segoe UI', 11, 'italic'), foreground=self.accent_color, background=self.primary_bg)
        self.loading_label.pack(pady=5)

        # Output area
        ttk.Label(self.main_frame, text="Command Output:", style='TLabel').pack(pady=(10, 5), anchor=tk.W, padx=15)
        
        # Frame for output text and copy button
        output_frame = ttk.Frame(self.main_frame, style='TFrame')
        output_frame.pack(expand=True, fill=tk.BOTH, padx=15)

        # Increased height for output text area
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=80, height=20, font=('Consolas', 10), background=self.output_bg, foreground=self.output_fg, insertbackground=self.output_fg)
        self.output_text.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(0, 10))
        self.output_text.config(state=tk.DISABLED) # Make it read-only
        
        copy_btn = ttk.Button(output_frame, text="Copy Output", command=self.copy_output, style='TButton')
        copy_btn.pack(side=tk.RIGHT, anchor=tk.N, pady=5)


    def run_selected_command(self):
        """Executes the selected command in a separate thread."""
        selected_command_name = ""
        actual_command = ""
        current_os_menu = ""

        # Determine which menu is currently active to get the correct command
        # Find the first Heading.TLabel widget in main_frame and get its text
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, ttk.Label) and widget.cget('style') == 'Heading.TLabel':
                current_os_menu = widget.cget("text")
                break

        if not current_os_menu: # Fallback if heading label not found
            # Try to infer from current OS if no menu title is found
            current_platform_system = platform.system()
            if current_platform_system == "Windows":
                current_os_menu = "Windows Fix Kit"
            elif current_platform_system == "Linux":
                current_os_menu = "Linux Fix Kit"
            elif current_platform_system == "Darwin": # macOS
                current_os_menu = "macOS Fix Kit"


        if "Windows" in current_os_menu:
            version = self.selected_windows_version.get()
            selected_command_name = self.selected_windows_command.get()
            actual_command = self.windows_commands_options.get(version, {}).get(selected_command_name, "")
            
            # Explicit warning if sudo is found in a Windows command
            if platform.system() == "Windows" and actual_command.strip().startswith("sudo"):
                messagebox.showerror("Invalid Command for Windows", 
                                     "The 'sudo' command is for Linux/Unix/macOS systems and cannot be run on Windows.\n"
                                     "Please select a Windows-specific command or ensure you are on the correct OS.\n\n"
                                     "If this command requires Administrator privileges, please ensure the WLFK Tool itself is run as Administrator.")
                return

        elif "Linux" in current_os_menu:
            distro = self.selected_linux_distro.get()
            selected_command_name = self.selected_linux_command.get()
            actual_command = self.linux_commands_options.get(distro, {}).get(selected_command_name, "")
            
            # Explicit warning if a Linux command is run on non-Linux OS
            if platform.system() != "Linux":
                messagebox.showwarning("Platform Mismatch", 
                                      f"You are on {platform.system()} but attempting to run a Linux command. "
                                      "This command will likely fail. Please ensure you are running the WLFK Tool on Linux "
                                      "if you wish to use Linux-specific commands.\n\n"
                                      "If this command requires root privileges, please ensure the WLFK Tool itself is run with 'sudo'.")
                # Do not return, let the command attempt to run and show the error in output
                
        elif "macOS" in current_os_menu:
            selected_command_name = self.selected_macos_command.get()
            actual_command = self.macos_commands_options.get(selected_command_name, "")
            
            # Explicit warning if a macOS command is run on non-macOS OS
            if platform.system() != "Darwin":
                messagebox.showwarning("Platform Mismatch",
                                      f"You are on {platform.system()} but attempting to run a macOS command. "
                                      "This command will likely fail. Please ensure you are running the WLFK Tool on macOS "
                                      "if you wish to use macOS-specific commands.\n\n"
                                      "If this command requires root privileges, please ensure the WLFK Tool itself is run with 'sudo'.")
                # Do not return, let the command attempt to run and show the error in output


        if not actual_command or actual_command == "Select a command":
            messagebox.showwarning("No Command Selected", "Please select a command to run.")
            return

        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Executing: {selected_command_name}\n")
        self.output_text.insert(tk.END, f"Command: {actual_command}\n\n")
        self.output_text.config(state=tk.DISABLED)
        
        # Start loading animation
        self.loading_dots_count = 0
        self._animate_loading_dots()

        # Run command in a separate thread to keep GUI responsive
        threading.Thread(target=self._execute_command, args=(actual_command,)).start()

    def _animate_loading_dots(self):
        """Animates the loading dots."""
        dots = "." * (self.loading_dots_count % 4)
        self.loading_label.config(text=f"Executing command{dots} Please wait.")
        self.loading_dots_count += 1
        self.loading_animation_id = self.master.after(300, self._animate_loading_dots) # Update every 300ms

    def _stop_loading_animation(self):
        """Stops the loading dots animation."""
        if self.loading_animation_id:
            self.master.after_cancel(self.loading_animation_id)
            self.loading_animation_id = None
        self.loading_label.config(text="") # Clear the loading text

    def _execute_command(self, command):
        """Internal method to execute the command using subprocess."""
        try:
            shell_needed = True # Generally safer to use shell=True for complex commands or if on Windows

            # For commands that launch a new GUI window, use subprocess.Popen to not wait for their completion.
            gui_apps_windows = ["rstrui.exe", "msdt.exe", "msinfo32", "dxdiag", "cleanmgr.exe", "msconfig.exe", "eventvwr.msc", "services.msc", "devmgmt.msc"]
            gui_apps_linux = ["gnome-disks"] # Add more as needed
            gui_apps_macos = [] # macOS GUI apps are typically launched by 'open -a "App Name"' or just 'open /Applications/App.app'

            current_platform = platform.system()

            if current_platform == "Windows":
                if any(app in command for app in gui_apps_windows):
                    subprocess.Popen(command, shell=shell_needed) 
                    self.master.after(0, self._update_output, f"\nLaunched '{command}'. Check for a new window or prompt.\n")
                    self.master.after(0, self._stop_loading_animation) # Stop loading animation
                    return
            elif current_platform == "Linux":
                if any(app in command for app in gui_apps_linux):
                    subprocess.Popen(command, shell=shell_needed)
                    self.master.after(0, self._update_output, f"\nLaunched '{command}'. Check for a new window or prompt.\n")
                    self.master.after(0, self._stop_loading_animation) # Stop loading animation
                    return
            # No specific GUI app handling for macOS yet, commands are mostly terminal-based

            # For other commands, use subprocess.run to capture output.
            process = subprocess.run(
                command,
                shell=shell_needed,
                capture_output=True,
                text=True, # Capture output as text (decoded)
                check=False # Don't raise exception for non-zero exit codes; we'll handle returncode manually
            )

            output = process.stdout
            error = process.stderr

            self.master.after(0, self._stop_loading_animation) # Stop loading animation

            if output:
                self.master.after(0, self._update_output, output)
            if error:
                self.master.after(0, self._update_output, f"\nERROR:\n{error}")
            if process.returncode != 0:
                self.master.after(0, self._update_output, f"\nCommand exited with code: {process.returncode}\n")
                # Provide a more specific hint for permission errors
                if ("Access is denied" in error or "requested operation requires elevation" in error or 
                    "Operation not permitted" in error or "Permission denied" in error or 
                    "EACCES" in error or "Permission denied" in process.stderr or 
                    "sudo: command not found" in error): # Explicitly catch sudo not found
                    self.master.after(0, self._update_output, "\n--- NOTE: This command likely requires Administrator/root privileges. Please ensure the WLFK Tool itself is run as Administrator (Windows) or with 'sudo' (Linux/macOS) for full functionality. ---\n")
                elif "command not found" in error or "is not recognized as an internal or external command" in error or "No such file or directory" in error:
                    self.master.after(0, self._update_output, f"\n--- ERROR: Command '{command.split(' ')[0]}' not found or invalid. Ensure it's correctly typed and available in your system's PATH. Also, verify you selected the correct OS type (Windows, Linux, macOS) for your current system. ---\n")


        except FileNotFoundError:
            self.master.after(0, self._stop_loading_animation) # Stop loading animation
            self.master.after(0, self._update_output, f"\nError: Command '{command.split(' ')[0]}' not found. Make sure it's in your system's PATH.\n")
        except Exception as e:
            self.master.after(0, self._stop_loading_animation) # Stop loading animation
            self.master.after(0, self._update_output, f"\nAn unexpected error occurred: {e}\n")

    def _update_output(self, text):
        """Updates the ScrolledText widget from the main thread."""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END) # Scroll to the end
        self.output_text.config(state=tk.DISABLED)

    def copy_output(self):
        """Copies the content of the output text area to the clipboard."""
        try:
            self.master.clipboard_clear()
            self.master.clipboard_append(self.output_text.get(1.0, tk.END))
            messagebox.showinfo("Copy to Clipboard", "Command output copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Copy Error", f"Failed to copy to clipboard: {e}")


# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = WLFKTool(root)
    root.mainloop()
