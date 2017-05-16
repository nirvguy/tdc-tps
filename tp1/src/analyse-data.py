#!/usr/bin/python3
import sys
import argparse
import json
from scapy.all import *
from fuente import Fuente
from grafo import Grafo

UNICAST = 'unicast'
MULTICAST = 'multicast'
MAC_MULTICAST = 'ff:ff:ff:ff:ff:ff'

fuente = Fuente()
grafo = Grafo()

def analize_uni_multi_cast(packet):
    # Si no es Ethernet o 802.11 descartarlo
    if (Ether not in packet) and (Dot11 not in packet):
        return

    # Si es ethernet
    if Ether in packet:
        dst = packet.dst
    else: # Si es 802.11 el 
        dst = packet.addr1

    if dst == MAC_MULTICAST:
        fuente.agregar_muestra(MULTICAST)
    else:
        fuente.agregar_muestra(UNICAST)

def analize_arp(packet):
    # Si no es Ethernet o 802.11 descartarlo
    if (Ether not in packet) and (Dot11 not in packet):
        return
    # Si no es ARP se descarta
    if ARP not in packet:
        return

    fuente.agregar_muestra(packet.pdst)

    if Ether in packet:
        p_src, p_dest = packet.src, packet.dst
    else:
        p_src, p_dest = packet.addr2, packet.addr1

    grafo.agregar_nodo(p_src)
    grafo.agregar_nodo(p_dest)
    grafo.agregar_arista(p_src, p_dest)

def main():
    parser = argparse.ArgumentParser(description='Modelado de fuente unicast/broadcast o de la fuente arp')
    parser.add_argument('captura', type=str, help='Archivo .pcap resultado de correr el sniffer')
    parser.add_argument('-s', "--source", type=str, choices=('u_m', 'arp'), default='u_m', help="Fuente de información, por defecto unicast/multicast")
    parser.add_argument('-j', "--use-json", dest='use_json', action='store_true', help="Establece la salida en formato json")
    parser.add_argument("--no-use-json", dest='use_json', action='store_false', help="No imprime la salida en formato json. Por defecto.")
    parser.set_defaults(use_json=False)
    args = parser.parse_args()

    sniff_extra_args = dict()

    packet_analyze = None

    if args.source == 'u_m':
        packet_analyze = analize_uni_multi_cast
    else:
        packet_analyze = analize_arp
        sniff_extra_args['filter'] = 'arp'

    packets = sniff(offline=args.captura, prn=packet_analyze, store=0, **sniff_extra_args)

    result = {'probabilities': dict(fuente.probabilidades()),
              'information': dict(fuente.informacion()),
              'entropy': fuente.entropia()}

    if args.source == 'arp':
        result['graph'] = dict({'nodes' : list(grafo.nodos),
                                'edges' : grafo.lista_aristas()})

    if args.use_json:
        print(json.dumps(result, indent=6))
    else:
        def print_dict(dicc):
            for x, y in dicc.items():
                print("\t{}: {}".format(x,y))

        print("Probabilidades: ")
        print_dict(result['probabilities'])
        print("Informacion: ")
        print_dict(result['information'])
        print("Entropia: ",result['entropy'])


if __name__ == '__main__':
    main()
