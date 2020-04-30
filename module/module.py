import json
import traceback
import subprocess
import re

# cmd = "wmic nic get Name, Installed, MACAddress, PowerManagementSupported, Speed"
# wmic nic where Name='Realtek PCIe GbE Family Controller' get name, NetEnabled, NetConnectionID
# result = check_output(cmd, shell=True).decode("Big5", "ignore")
# netsh interface show interface name="Wi-Fi"
# Intel(R) Wireless-AC 9560 160MHz
# Realtek RTL8192CU Wireless LAN 802.11n USB 2.0 Network Adapter
# TP-Link Wireless USB Adapter

# netsh interface set interface "YOUR-ADAPTER-NAME" disable/enable

# print(result)
# Microsoft Hosted Network Virtual Adapter                        分享網路          TRUE
# Realtek RTL8192CU Wireless LAN 802.11n USB 2.0 Network Adapter  Wi-Fi 2          FALSE
# Intel(R) Wireless-AC 9560 160MHz                                Wi-Fi            FALSE

net_interface = {
    "Realtek PCIe GbE Family Controller": False,
    "Bluetooth Device (Personal Area Network)": False,
    "Intel(R) Wireless-AC 9560 160MHz": False,
    "Realtek RTL8192CU Wireless LAN 802.11n USB 2.0 Network Adapter": False,
    "TP-Link Wireless USB Adapter": False,
    "Realtek RTL8821CE 802.11ac PCIe Adapter": False
}

def load_config(config_file):
    try:
        with open(config_file, "r", encoding='utf8') as f:
            data = json.load(f)
        config = data
        print(config)
        return config
    except:
        print(traceback.format_exc())

def save_config(config_file, ssid='default-wifi', pwd='password'):
    try:
        data = dict()
        with open(config_file, 'w') as fp:
            data['ap'] = {}
            data['ap']['ssid'] = ssid
            data['ap']['pwd'] = pwd
            json.dump(data, fp, indent=4)
        return True
    except:
        print(traceback.format_exc())

def get_all_net_interface_status():
    try:
        for nwi, status in net_interface.items():
            cmd = "wmic nic where Name='{}' get name".format(nwi)
            # result = check_output(cmd, shell=True)
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            result = result.stdout.decode("Big5")

            if result.find(nwi) > 0:
                is_enable = check_net_interface_status(nwi)
                net_interface[nwi] = is_enable
            else:
                net_interface[nwi] = None
        print(net_interface)
        return net_interface
    except:
        print(traceback.format_exc())

def check_net_interface_status(name):
    try:
        for nwi, status in net_interface.items():
            cmd = "wmic nic where Name='{}' get NetEnabled".format(name)
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            result = result.stdout.decode("Big5")
            if result.find("TRUE") > 0:
                return True
            else:
                return False
    except:
        print(traceback.format_exc())

def net_interface_switch(nic_name, enable):
    try:
        print("{} : {}".format(nic_name, enable))
        interface_name = get_interface_name(nic_name)
        value = "enable" if enable else "disable"
        cmd = "netsh interface set interface \"{}\" {}".format(interface_name, value)
        print(cmd)
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        result = result.stdout.decode("Big5")
        print(result)
    except:
        print(traceback.format_exc())

def get_interface_name(nic_name):
    try:
        cmd = "wmic nic where Name=\"{}\" get NetConnectionID".format(nic_name)
        print(cmd)
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        result = result.stdout.decode("Big5")
        interface_name = re.sub('NetConnectionID', '', result)
        interface_name = interface_name.strip().rstrip()
        return interface_name
    except:
        print(traceback.format_exc())

def set_wifi_data(config_file):
    config = load_config(config_file)
    ssid = config['ap']['ssid']
    password = config['ap']['pwd']

    cmd = "netsh wlan set hostednetwork mode=allow ssid={} key={}".format(ssid, password)
    print(cmd)
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    result = result.stdout.decode("Big5")
    return result

def wifi_on():
    cmd = "netsh wlan start hostednetwork"
    print(cmd)
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    result = result.stdout.decode("Big5")
    return result

def wifi_off():
    cmd = "netsh wlan stop hostednetwork"
    print(cmd)
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    result = result.stdout.decode("Big5")
    return result
