#!/usr/bin/python3
from scapy.all import *
from fuente import Fuente

UNICAST = 'unicast'
MULTICAST = 'multicast'

fuente = Fuente(simbolos=(UNICAST, MULTICAST))

def packet_callback(packet):
    if packet.dst == 'ff:ff:ff:ff:ff:ff':
        fuente.agregar_muestra(MULTICAST)
    else:
        fuente.agregar_muestra(UNICAST)

def main():
    sniff(iface=config.EJ1_IFACE, prn=packet_callback, store=0, timeout=60)
    print(fuente)

if __name__ == '__main__':
    main()
