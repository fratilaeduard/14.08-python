import os
import subprocess

# if os.geteuid() != 0:
#     exit("Root required!")

# cmd = 'sudo airodump-ng wlan2 --berlin 90000 --output-format csv -w rawCapture --manufacturer --band a'

def get_alfa_device():
    network_interafaces = os.listdir('/sys/class/net')
    wireless_interfaces = []

    UNAME_DRIVER_PATH = '/device/uevent'
    SEARCHED_DRIVER_NAME = 'rtl8814au'

    for device in network_interafaces:
        if device.find('wlan') != -1:
            wireless_interfaces.append(device)

    for device in wireless_interfaces:
        driver_data = {}
        driver_name_path = '/sys/class/net/'+str(device)+UNAME_DRIVER_PATH
        uevent = open(driver_name_path)

        #read driver data as json
        for line in uevent:
            line = line.strip()
            if not line:
                continue
            if '=' not in line:
                continue
            key, value = line.split('=', 1)
            driver_data[key.lower()] = value

        #check for matching driver
        if driver_data['driver'] == SEARCHED_DRIVER_NAME:
            return device
    
    return -1

# def get_tplink_device():
#     network_interafaces = os.listdir('/sys/class/net')
#     wireless_interfaces = []

#     UNAME_DRIVER_PATH = '/device/uevent'
#     SEARCHED_DRIVER_NAME = 'rtl88x2bu'

#     for device in network_interafaces:
#         if device.find('wlan') != -1:
#             wireless_interfaces.append(device)

#     for device in wireless_interfaces:
#         driver_data = {}
#         driver_name_path = '/sys/class/net/'+str(device)+UNAME_DRIVER_PATH
#         uevent = open(driver_name_path)

#         #read driver data as json
#         for line in uevent:
#             line = line.strip()
#             if not line:
#                 continue
#             if '=' not in line:
#                 continue
#             key, value = line.split('=', 1)
#             driver_data[key.lower()] = value

#         #check for matching driver
#         if driver_data['driver'] == SEARCHED_DRIVER_NAME:
#             return device
    
#     return -1




def external_capture():
    if os.geteuid() != 0:
        raise Exception("Root required!")
    
    if get_alfa_device() == -1:
        raise Exception("Alfa cards missing!")

    capture_command_band_a = 'sudo airodump-ng ' + str(get_alfa_device()) + ' --berlin 90000 --output-format csv -w rawCapture --manufacturer --band ab'

    # subprocess.run([str(capture_command_band_a)], shell=True, capture_output=True, text=True, timeout=None)
    subprocess.run([str(capture_command_band_a)], shell=True, text=True)