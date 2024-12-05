import os
from netmiko import ConnectHandler
import difflib
import tkinter as tk
from tkinter import messagebox, ttk

# SSH device details
ssh_device = {
    'device_type': 'cisco_ios',
    'host': '192.168.57.101',  # Update this as needed
    'username': 'cisco',
    'password': 'cisco123!',
}

# Router Configuration Functions
def configure_interfaces():
    """Configure loopback and other interfaces."""
    try:
        connection = ConnectHandler(**ssh_device)
        commands = [
            'hostname ConfiguredRouter',
            'interface GigabitEthernet1',
            'ip address 192.168.57.101 255.255.255.0',
            'no shutdown',
            'interface GigabitEthernet2',
            'ip address 192.168.57.102 255.255.255.0',
            'no shutdown',
            'interface Loopback0',
            'ip address 10.0.0.1 255.255.255.255',
            'no shutdown',
        ]
        connection.send_config_set(commands)
        connection.disconnect()
        messagebox.showinfo("Success", "Interfaces configured successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to configure interfaces: {str(e)}")

def configure_ospf():
    """Configure OSPF protocol."""
    try:
        connection = ConnectHandler(**ssh_device)
        commands = [
            'router ospf 1',
            'network 192.168.57.0 0.0.0.255 area 0',
            'network 10.0.0.0 0.0.0.255 area 0',
        ]
        connection.send_config_set(commands)
        connection.disconnect()
        messagebox.showinfo("Success", "OSPF configured successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to configure OSPF: {str(e)}")

def configure_acl():
    """Configure Access Control Lists."""
    try:
        connection = ConnectHandler(**ssh_device)
        commands = [
            'ip access-list extended BLOCK_HTTP',
            'deny tcp any any eq 80',
            'permit ip any any',
            'interface GigabitEthernet1',
            'ip access-group BLOCK_HTTP in',
        ]
        connection.send_config_set(commands)
        connection.disconnect()
        messagebox.showinfo("Success", "ACL configured successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to configure ACL: {str(e)}")

def configure_ipsec():
    """Configure IPSec VPN (partial)."""
    try:
        connection = ConnectHandler(**ssh_device)
        commands = [
            'crypto isakmp policy 10',
            'encryption aes',
            'hash sha256',
            'authentication pre-share',
            'group 14',
            'crypto isakmp key MY_SECRET_KEY address 0.0.0.0',
            'crypto ipsec transform-set TRANS_SET esp-aes esp-sha256-hmac',
            'crypto map VPN_MAP 10 ipsec-isakmp',
            'set peer 192.168.57.200',
            'set transform-set TRANS_SET',
            'match address 101',
            'ip access-list extended 101',
            'permit ip 192.168.57.0 0.0.0.255 10.0.0.0 0.0.0.255',
            'interface GigabitEthernet1',
            'crypto map VPN_MAP',
        ]
        connection.send_config_set(commands)
        connection.disconnect()
        messagebox.showinfo("Success", "IPSec VPN configured successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to configure IPSec: {str(e)}")

def open_ssh_terminal():
    """Open a manual SSH session."""
    try:
        os.system(f"ssh {ssh_device['username']}@{ssh_device['host']}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open SSH terminal: {str(e)}")

# GUI Design
def main():
    root = tk.Tk()
    root.title("Router Management Dashboard")
    root.geometry("700x500")
    root.configure(bg="#e6f7ff")

    # Title
    title_label = tk.Label(
        root,
        text="Router Management Dashboard",
        font=("Arial", 24, "bold"),
        bg="#e6f7ff",
        fg="#00509e",
    )
    title_label.pack(pady=20)

    # Interface Configuration Button
    interface_button = ttk.Button(
        root, text="Configure Interfaces", command=configure_interfaces
    )
    interface_button.pack(pady=10)

    # OSPF Configuration Button
    ospf_button = ttk.Button(root, text="Configure OSPF", command=configure_ospf)
    ospf_button.pack(pady=10)

    # ACL Configuration Button
    acl_button = ttk.Button(root, text="Configure ACL", command=configure_acl)
    acl_button.pack(pady=10)

    # IPSec Configuration Button
    ipsec_button = ttk.Button(root, text="Configure IPSec VPN", command=configure_ipsec)
    ipsec_button.pack(pady=10)

    # SSH Terminal Button
    ssh_button = ttk.Button(root, text="Open SSH Terminal", command=open_ssh_terminal)
    ssh_button.pack(pady=10)

    # Quit Button
    quit_button = ttk.Button(root, text="Exit Application", command=root.quit)
    quit_button.pack(pady=20)

    # Footer
    footer_label = tk.Label(
        root,
        text="© 2024 Router Management Tool",
        font=("Arial", 10),
        bg="#e6f7ff",
        fg="#333333",
    )
    footer_label.pack(side="bottom", pady=10)

    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    main()
