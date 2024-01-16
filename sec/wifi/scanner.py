from scapy.all import *
from threading import Thread
import pandas
import time
import os
import subprocess
from itertools import cycle

def callback(packet):
    if packet.haslayer(Dot11):
        #if packet.type == 0 and packet.subtype in (0, 2, 4):
            #print(f"Packet: {packet.summary()}")
            freq = packet[RadioTap].ChannelFrequency
            channel = list(filter(lambda x: x[1]['freq'] == freq, channels.items()))[0][0]
            signal = packet[RadioTap].dBm_AntSignal
            client_addr = packet.addr2

            if packet.haslayer(Dot11ProbeReq):
                client_addr = packet.addr2
                probe_req_ssid = packet[Dot11ProbeReq].info.decode()
                print(f"Got [Probe Request] cli: {client_addr}, ssid: {probe_req_ssid}, freq: {freq} ({channel}), signal: {signal}")

            if packet.haslayer(Dot11ProbeResp):
                bssid_addr = packet.addr2
                client_addr = packet.addr1
                probe_res_ssid = packet[Dot11ProbeResp].info.decode()
                print(f"Got [Probe Response] bssid: {bssid_addr}, cli: {client_addr}, ssid: {probe_res_ssid}, freq: {freq} ({channel}), signal: {signal}")

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
                    if bssid not in networks.index:
                        print(f"Got [Beacon] bssid: {bssid}, ssid: {ssid}, channel: {channel}, signal: {dbm_signal}, crypto: {crypto}")
                    networks.loc[bssid] = (ssid, dbm_signal, channel, crypto)


def print_all(sleep=1):
    while True:
        os.system("clear")
        networks.sort_values(by=['Channel','SSID'])
        print(networks)
        print("")
        print(clients)
        time.sleep(sleep)

def change_channel(sleep=1, iface="wlan1", channels=range(1, 15)):
    for ch in cycle(channels):
        os.system(f"iwconfig {iface} channel {ch}")
        time.sleep(sleep)

def iface_set_monitor(iface="wlan1"):
        os.system(f"ifconfig {iface} down;sleep 1")
        #"iw", "reg", "set", "GY"
        #os.system(f"iw reg set BZ")
        #os.system(f"iwconfig {iface} txpower 30")
        os.system(f"iwconfig {iface} mode monitor")
        os.system(f"ifconfig {iface} up;sleep 3")

networks = pandas.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Crypto"])
networks.set_index("BSSID", inplace=True)

clients = pandas.DataFrame(columns=["MAC", "Probe_SSID"])
clients.set_index("MAC", inplace=True)

probes = pandas.DataFrame(columns=["BSSID", "Info"])
probes.set_index("BSSID", inplace=True)

channels = {
        1: { 'freq': 2412},
        2: { 'freq': 2417},
        3: { 'freq': 2422},
        4: { 'freq': 2427},
        5: { 'freq': 2432},
        6: { 'freq': 2437},
        7: { 'freq': 2442},
        8: { 'freq': 2447},
        9: { 'freq': 2452},
        10: { 'freq': 2457},
        11: { 'freq': 2462},
        12: { 'freq': 2467},
        13: { 'freq': 2472},
        14: { 'freq': 2484},
}

if __name__ == "__main__":
    scan_iface = "wlan1"
    scan_channels = range(1, 15)
    # Set monitor mode
    iface_set_monitor(scan_iface)
    # start the thread that prints all the networks
    printer = Thread(target=print_all)
    printer.daemon = True
    #printer.start()
    # start the thread that changes channels
    channel_changer = Thread(target=change_channel, kwargs={'iface': scan_iface, 'channels': scan_channels, 'sleep': 1})
    channel_changer.daemon = True
    channel_changer.start()
    # start sniffing
    sniff(prn=callback, iface=scan_iface)
