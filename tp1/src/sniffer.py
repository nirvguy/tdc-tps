#!/usr/bin/python3
import sys
import argparse
import json
from scapy.all import *
from fuente import Fuente

def main():
    parser = argparse.ArgumentParser(description='Captura el trafico de la red. Correr con privilegios de administrador (sudo)')
    parser.add_argument('outfile', type=str, help='Captura')
    parser.add_argument('-t', "--timeout", type=int, default=600, help="Tiempo tiemeout de captura, por defecto 10 minutos")
    parser.add_argument('-f', "--filter", type=str, help='Filtro, por defecto ninguno')
    parser.add_argument('-i', "--iface", type=str, help='Interfaz en la cual se realiza la captura')
    args = parser.parse_args()

    sniff_extra_params = dict()

    if args.iface:
        sniff_extra_params['iface'] = args.iface

    packets = sniff(timeout=args.timeout,
                    filter=args.filter,
                    **sniff_extra_params)

    wrpcap(args.outfile, packets)

if __name__ == '__main__':
    main()
