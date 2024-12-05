import os
import tkinter as tk
from tkinter import scrolledtext
from netmiko import ConnectHandler
import threading

# SSH device details
ssh_device = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.101',  # Primary SSH target
    'username': 'cisco',
    'password': 'cisco123!',
}

# Function to configure interfaces
def configure_interfaces():
    output_box.insert(tk.END, "Connecting to the router to configure interfaces...\n")
    try:
        connection = ConnectHandler(**ssh_device)
        output_box.insert(tk.END, "Successfully connected to the router!\n")
        
        # Configuration commands
        commands = [
            'hostname ConfiguredRouter',
            'interface GigabitEthernet2',
            'ip address 192.168.57.102 255.255.255.0',
            'no shutdown',
            'interface Loopback0',
            'ip address 10.0.0.1 255.255.255.255',
            'no shutdown',
        ]
        output_box.insert(tk.END, "Sending interface configuration commands...\n")
        config_output = connection.send_config_set(commands)
        output_box.insert(tk.END, f"{config_output}\n")
        
        connection.disconnect()
        output_box.insert(tk.END, "Configuration complete! Connection closed.\n")
    except Exception as e:
        output_box.insert(tk.END, f"Error: {e}\n")

# Function to configure OSPF
def configure_ospf():
    output_box.insert(tk.END, "Connecting to the router to configure OSPF...\n")
    try:
        connection = ConnectHandler(**ssh_device)
        output_box.insert(tk.END, "Successfully connected to the router!\n")
        
        # OSPF Configuration
        commands = [
            'router ospf 1',
            'network 192.168.57.0 0.0.0.255 area 0',
            'network 10.0.0.0 0.0.0.255 area 0',
        ]
        output_box.insert(tk.END, "Sending OSPF configuration commands...\n")
        ospf_output = connection.send_config_set(commands)
        output_box.insert(tk.END, f"{ospf_output}\n")
        
        connection.disconnect()
        output_box.insert(tk.END, "OSPF configuration complete! Connection closed.\n")
    except Exception as e:
        output_box.insert(tk.END, f"Error: {e}\n")

# Function for manual SSH access
def manual_access():
    output_box.insert(tk.END, "Opening a manual SSH session...\n")
    try:
        # Use os.system to open an SSH session
        os.system(f"ssh {ssh_device['username']}@{ssh_device['host']}")
        output_box.insert(tk.END, "SSH session closed.\n")
    except Exception as e:
        output_box.insert(tk.END, f"Error: {e}\n")

# GUI setup
def create_gui():
    global output_box

    root = tk.Tk()
    root.title("Router Configuration Tool")
    root.geometry("800x600")
    root.configure(bg="lightblue")

    # Title label
    title_label = tk.Label(
        root,
        text="Router Configuration Tool",
        font=("Arial", 20, "bold"),
        bg="lightblue",
        fg="darkblue",
    )
    title_label.pack(pady=20)

    # Buttons for actions
    button_configure_interfaces = tk.Button(
        root,
        text="Configure Interfaces",
        command=lambda: threading.Thread(target=configure_interfaces).start(),
        bg="green",
        fg="white",
        font=("Arial", 14),
        width=20,
    )
    button_configure_interfaces.pack(pady=10)

    button_configure_ospf = tk.Button(
        root,
        text="Configure OSPF",
        command=lambda: threading.Thread(target=configure_ospf).start(),
        bg="orange",
        fg="white",
        font=("Arial", 14),
        width=20,
    )
    button_configure_ospf.pack(pady=10)

    button_manual_access = tk.Button(
        root,
        text="Manual SSH Access",
        command=lambda: threading.Thread(target=manual_access).start(),
        bg="blue",
        fg="white",
        font=("Arial", 14),
        width=20,
    )
    button_manual_access.pack(pady=10)

    # Output box for logs
    output_box = scrolledtext.ScrolledText(root, width=80, height=20, font=("Arial", 12))
    output_box.pack(pady=20)

    # Start the GUI event loop
    root.mainloop()


# Start the application
if __name__ == "__main__":
    create_gui()

