from scapy.all import *
from threading import Thread
import pandas
import time
import os
import subprocess

def callback(packet):
    if packet.haslayer(Dot11Beacon):
        # extract the MAC address of the network
        bssid = packet[Dot11].addr2
        # get the name of it
        if set(map(ord, list(packet[Dot11Elt].info.decode()))) == {0}:
          ssid = "N/A"
        else:
          ssid = packet[Dot11Elt].info.decode()
        try:
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = "N/A"
        # extract network stats
        stats = packet[Dot11Beacon].network_stats()
        # get the channel of the AP
        channel = stats.get("channel")
        # get the crypto
        crypto = stats.get("crypto")
        if ssid is not None:
          networks.loc[bssid] = (ssid, dbm_signal, channel, crypto)

def print_all(sleep=1):
    while True:
        os.system("clear")
        networks.sort_values(by=['Channel','SSID'])
        print(networks)
        time.sleep(sleep)

def change_channel(sleep=1):
    ch = 1
    while True:
        os.system(f"iwconfig {interface} channel {ch}")
        # switch channel from 1 to 14 each 0.5s
        ch = ch % 14 + 1
        time.sleep(sleep)

def iface_set_monitor(iface="wlan1"):
    subprocess.run([
        "ifconfig", iface, "down"
    ])
    
    subprocess.run([
        "iwconfig", iface, "mode", "monitor"
    ])

    subprocess.run([
        "ifconfig", iface, "up"
    ])

networks = pandas.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Crypto"])
networks.set_index("BSSID", inplace=True)

if __name__ == "__main__":
    # interface name, check using iwconfig
    interface = "wlan1"
    # start the thread that prints all the networks
    printer = Thread(target=print_all)
    printer.daemon = True
    printer.start()
    # start the thread that changes channels
    channel_changer = Thread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start()
    # start sniffing
    sniff(prn=callback, iface=interface)
