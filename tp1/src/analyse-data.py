#!/usr/bin/python3
import sys
import argparse
import json
from scapy.all import *
from fuente import Fuente

UNICAST = 'unicast'
MULTICAST = 'multicast'
MAC_MULTICAST = 'ff:ff:ff:ff:ff:ff'
TIMEOUT_DEFAULT = 60 * 10

fuente = Fuente()

def analize_uni_multi_cast(packet):
    if packet.dst == MAC_MULTICAST:
        fuente.agregar_muestra(MULTICAST)
    else:
        fuente.agregar_muestra(UNICAST)

def analize_arp(packet):
    fuente.agregar_muestra(packet.pdst)

def main():
    parser = argparse.ArgumentParser(description='Modelado de fuente unicast/broadcast')
    parser.add_argument('captura', type=str, help='Captura')
    parser.add_argument('-s', "--source", type=str, choices=('u_m', 'arp'), default='u_m')
    parser.add_argument('-j', "--use-json", dest='use_json', action='store_true')
    parser.add_argument("--no-use-json", dest='use_json', action='store_false')
    parser.set_defaults(use_json=False)
    args = parser.parse_args()

    sniff_extra_args = dict()

    packet_analyze = None

    if args.source == 'u_m':
        packet_analyze = analize_uni_multi_cast
    else:
        packet_analyze = analize_arp

    packets = sniff(offline=args.captura, prn=packet_analyze)

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
