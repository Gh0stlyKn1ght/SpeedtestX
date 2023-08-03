import os
import subprocess
import speedtest
import time
from tqdm import tqdm
import socket
import psutil
import sys

def get_network_device_name():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    network_device_name = socket.gethostbyaddr(ip_address)[0]
    return network_device_name

def get_network_card_info():
    net_card_info = []
    for interface, details in psutil.net_if_stats().items():
        if details.isup:
            card_name = interface
            card_model = psutil.net_if_addrs().get(interface)[0].family
            card_status = "Up"
            net_card_info.append((card_name, card_model, card_status))
    return net_card_info
def run_speed_test():
    st = speedtest.Speedtest()
    st.get_best_server()

    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    ping = st.results.ping
    server_info = st.results.server

    return download_speed, upload_speed, ping, server_info

def loading_animation():
    earth_images = ['   o   ', ' - o - ', '   o   ', '   |   ', '   o   ']
    for i in range(30):
        time.sleep(0.1)
        print(f"\rTesting your internet speed... {earth_images[i % len(earth_images)]}", end='', flush=True)
    print("\r", end='', flush=True)

def main():
    num_servers = 1  # Change this to the number of servers you want to test against
    download_speeds, upload_speeds, pings, server_info_list = [], [], [], []
 # ASCII Art Title
    print(r"""
 ___________ _____ ___________ _____ _____ _____ _______   __
/  ___| ___ \  ___|  ___|  _  \_   _|  ___/  ___|_   _\ \ / /
\ `--.| |_/ / |__ | |__ | | | | | | | |__ \ `--.  | |  \ V / 
 `--. \  __/|  __||  __|| | | | | | |  __| `--. \ | |  /   \ 
/\__/ / |   | |___| |___| |/ /  | | | |___/\__/ / | | / /^\ \
\____/\_|   \____/\____/|___/   \_/ \____/\____/  \_/ \/   \/
                                                             
                                                             
                   2023 by github/Gh0stlykn1ght 
    """)


# displaynetwork devices
    network_device_name = get_network_device_name()
    print(f"Network Device: {network_device_name}")

    network_card_info = get_network_card_info()
    if network_card_info:
        print("Active Network Card Information:")
        print("-------------------------------")
        for card_name, card_model, card_status in network_card_info:
            print(f"Interface: {card_name}, Model: {card_model}, Status: {card_status}")
    else:
        print("No active network cards found.")
    print("Running speed test... This may take a moment.")
    for _ in tqdm(range(30), ascii=True, unit='step', desc='Testing your internet speed', bar_format="{l_bar}{bar}{r_bar}", colour='green'):
        time.sleep(0.1)

    for _ in range(num_servers):
        with tqdm(total=100, ascii=True, unit='%', desc=f"Server {_ + 1} progress") as pbar:
            for _ in tqdm(range(100), ascii=True, unit='%', leave=False):
                time.sleep(0.05)
                pbar.update(1)

        download_speed, upload_speed, ping, server_info = run_speed_test()
        download_speeds.append(download_speed)
        upload_speeds.append(upload_speed)
        pings.append(ping)
        server_info_list.append(server_info)

    print("\nTest Results:")

    for i in range(num_servers):
        server_info = server_info_list[i]
        server_name = server_info['host']
        server_location = f"{server_info['name']}, {server_info['country']}"
        server_ip = server_info['sponsor']

        print(f" {i+1}: ↓: {download_speeds[i]:.2f} Mbps, ↑: {upload_speeds[i]:.2f} Mbps, Ping: {pings[i]} ms")
        print(f"   📍: {server_location}, IP: {server_ip}")


    print("\nFinished!")
    sys.exit()

if __name__ == "__main__":
  try:
        # Check if we are in the virtual environment and activate it if needed
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print("Activating the virtual environment...")
            activate_script = "activate" if os.name == "nt" else "source activate"
            os.system(f"{activate_script} myenv")  # Replace 'myenv' with your virtual environment name

        main()
  except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting gracefully.")
  except Exception as e:
        print(f"An error occurred: {e}")
  finally:
        sys.exit()
