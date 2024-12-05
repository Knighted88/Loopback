import os
from netmiko import ConnectHandler
import difflib  # Library for showing differences between configurations

# SSH device details
ssh_device = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.101',  # SSH IP (CSR1000v)
    'username': 'cisco',
    'password': 'cisco123!',
}

def compare_configs(running_config, startup_config):
    """Compare the running configuration with the startup configuration and return differences."""
    diff = difflib.unified_diff(
        running_config.splitlines(),
        startup_config.splitlines(),
        fromfile='Running Config',
        tofile='Startup Config',
        lineterm=''
    )
    return '\n'.join(diff)

while True:
    print('=============================================================')
    user_choice = input('---Enter 1 to configure and access the CSR1000v router\n---or 0 to exit: ')
    print('=============================================================')
    
    if user_choice == '1':
        # Establish SSH connection
        connection = ConnectHandler(**ssh_device)
        print("Connected to CSR1000v Router via SSH!")

        # Commands to configure interfaces and loopback
        ssh_commands = [
            'hostname SSHRouter',  # Set hostname
            'interface GigabitEthernet1',  # Inside interface
            'ip address 192.168.56.101 255.255.255.0',
            'no shutdown',
            'interface GigabitEthernet2',  # Outside interface
            'ip address 192.168.57.101 255.255.255.0',
            'no shutdown',
            'interface Loopback0',  # Loopback interface
            'ip address 10.0.0.1 255.255.255.255',
            'no shutdown',
            'router ospf 1',  # OSPF configuration
            'network 192.168.56.0 0.0.0.255 area 0',
            'network 192.168.57.0 0.0.0.255 area 0',
            'network 10.0.0.0 0.0.0.0 area 0',
            'ip access-list extended BLOCK_WEBSITES',  # ACL configuration
            'deny tcp any any eq 80',
            'deny tcp any any eq 443',
            'permit ip any any',
            'interface GigabitEthernet1',
            'ip access-group BLOCK_WEBSITES in',
            'crypto isakmp policy 10',  # IPSec ISAKMP policy
            'encryption aes',
            'hash sha256',
            'authentication pre-share',
            'group 14',
            'crypto isakmp key cisco123 address 192.168.57.102',  # Peer router's IP
            'crypto ipsec transform-set TRANS1 esp-aes esp-sha-hmac',  # IPSec transform set
            'crypto map VPNMAP 10 ipsec-isakmp',  # Crypto map for VPN
            'set peer 192.168.57.102',  # Peer router's IP
            'set transform-set TRANS1',
            'match address 101',
            'ip access-list extended 101',  # ACL for VPN traffic
            'permit ip 192.168.56.0 0.0.0.255 192.168.57.0 0.0.0.255',
            'interface GigabitEthernet2',
            'crypto map VPNMAP',  # Apply crypto map to the outside interface
        ]

        # Send configuration commands to the router
        print("Configuring interfaces, routing, ACLs, and VPN...")
        connection.send_config_set(ssh_commands)

        # Retrieve and save running and startup configurations
        running_config = connection.send_command('show running-config')
        with open('running_config.txt', 'w') as running_config_file:
            running_config_file.write(running_config)

        startup_config = connection.send_command('show startup-config')
        with open('startup_config.txt', 'w') as startup_config_file:
            startup_config_file.write(startup_config)

        # Compare running and startup configurations
        print("\n=============== Comparing Running Config with Startup Config ===================")
        diff_startup = compare_configs(running_config, startup_config)
        if diff_startup:
            print(diff_startup)
            with open('config_differences.txt', 'w') as diff_file:
                diff_file.write(diff_startup)
                print("Differences saved to config_differences.txt")
        else:
            print("No differences found.")
            with open('config_differences.txt', 'w') as diff_file:
                diff_file.write("No differences found between Running and Startup Configurations.")

        # Close the Netmiko connection
        connection.disconnect()
        print("Configuration complete. Disconnecting Netmiko session.")

        # Open manual SSH session
        os.system("ssh cisco@" + ssh_device['host'])
        break  # Exit the loop after a successful connection

    elif user_choice == '0':
        print("No connection selected. Exiting.")
        break

    else:
        print("Invalid input. Please enter 1 to configure and access, or 0 to exit.")
