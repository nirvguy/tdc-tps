#!/usr/bin/python3
import sys
import argparse
import json
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
    parser.add_argument('-f', "--fuente", type=str, choices=('u_m'), default='u_m')
    parser.add_argument('-j', "--use-json", dest='use_json', action='store_true')
    parser.add_argument("--no-use-json", dest='use_json', action='store_false')
    parser.set_defaults(use_json=False)
    args = parser.parse_args()
    if args.iface:
        sniff(iface=args.iface, prn=packet_callback, store=0, timeout=args.timeout)
    else:
        sniff(prn=packet_callback, store=0, timeout=args.timeout)
    result = {'probabilities': dict(fuente.probabilidades()),
              'information': dict(fuente.informacion()),
              'entropy': fuente.entropia()}
    if args.use_json:
        print(json.dumps(result, indent=4))
    else:
        def print_dict(dicc):
            for x, y in dicc.items():
                print("\t{}: {}".format(x,y))
        print("Probabilidades: ")
        print_dict(result['probabilities'])
        print("Informacion: ")
        print_dict(result['information'])
        print("Entropía: ",result['entropy'])


if __name__ == '__main__':
    main()
