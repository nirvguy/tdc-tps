#!/usr/bin/python3
import sys
import argparse
import json
from scapy.all import *
from fuente import Fuente

def main():
    parser = argparse.ArgumentParser(description='Modelado de fuente unicast/broadcast')
    parser.add_argument('outfile', type=str, help='Captura')
    parser.add_argument('-t', "--timeout", type=int, default=600)
    parser.add_argument('-f', "--filter", type=str, default='')
    parser.add_argument('-i', "--iface", type=str)
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
