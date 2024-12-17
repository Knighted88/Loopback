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
    user_choice = input('---Enter 1 to configure and access the router\n---or 0 to exit: ')
    print('=============================================================')
    
    if user_choice == '1':
        # Establish SSH connection
        connection = ConnectHandler(**ssh_device)
        print("Connected to Router By SSH!")

        # Commands to configure Gig1 and Loopback
        ssh_commands = [
            'hostname SSHRouter',  # Set hostname
            'interface GigabitEthernet1',  # Inside interface
            'ip address 192.168.56.101 255.255.255.0',
            'no shutdown',
            'interface GigabitEthernet2',
            'ip address 192.168.57.101 255.255.255.0',
            'no shutdown',
            'interface Loopback0',  # Loopback interface
            'ip address 10.0.0.1 255.255.255.255',
            'no shutdown',
            'router rip',
            'network 192.168.56.0',  # Advertise the 192.168.56.0 network
            'network 192.168.57.0',  # Advertise the 192.168.57.0 network
            'network 10.0.0.0', 
        ]

        # Send configuration commands to the router
        print("Configuring interfaces and loopback...")
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
        print("Configuration complete!!")

        # Open manual SSH session
        os.system("ssh cisco@" + ssh_device['host'])
        break  # Exit the loop after a successful connection

    elif user_choice == '0':
        print("No connection selected. Exiting.")
        break

    else:
        print("Invalid input. Please enter 1 to configure and access, or 0 to exit.")
