#!/usr/bin/python3
import argparse
from scapy.all import *
from fuente import Fuente

UNICAST = 'unicast'
MULTICAST = 'multicast'
TIMEOUT_DEFAULT = 60 * 10

fuente = Fuente(simbolos=(UNICAST, MULTICAST))

def packet_callback(packet):
    if packet.dst == 'ff:ff:ff:ff:ff:ff':
        fuente.agregar_muestra(MULTICAST)
    else:
        fuente.agregar_muestra(UNICAST)

def main():
    parser = argparse.ArgumentParser(description='Modelado de fuente unicast/broadcast')
    parser.add_argument('-t', "--timeout", type=int, default=TIMEOUT_DEFAULT, help='Tiempo de sniffeo')
    parser.add_argument('-i', "--iface", type=str, help='Interface de sniffeo')
    args = parser.parse_args()
    if args.iface:
        sniff(iface=args.iface, prn=packet_callback, store=0, timeout=args.timeout)
    else:
        sniff(prn=packet_callback, store=0, timeout=args.timeout)
    print(fuente)
    print("Entropia : {}".format(fuente.entropia()))
    print("Informacion: \n{}".format(str(fuente.informacion())))


if __name__ == '__main__':
    main()
