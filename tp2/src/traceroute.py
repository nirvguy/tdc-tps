#!/usr/bin/python3
import time
import operator
import argparse
import json
from scapy.all import *
from utils import mean, std

DEBUG = True

def print_debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs, file=sys.stderr)

def traceroute(ipdst, packets_per_host=30, timeout=20,
               verbose=False, max_ttl=100):
    """ Traceroute mediante el metodo de ttl seeder
        @param ipdst Ip de destino
        @param packets_per_host Cuantos paquetes se envían
                                para el mismo ttl
        @timeout Timeout de cada paquete
    """
    result = []
    # RTTs totales de cada paquete para el ttl anterior
    for ttl in range(1, max_ttl+1):
        # Diccionario con las ips que van apareciendo para el mismo ttl
        ips = dict()
        total_rtt = []
        for i in range(packets_per_host):
            # Envia el paquete cronometrando cuanto tiempo tarda
            # entre que se envia y se recibe para conseguir
            # un RTT aproximado
            packet = sr(IP(dst=ipdst, ttl=ttl)/ICMP(),
                        timeout=timeout,
                        verbose=verbose)

            # Si no llego respuesta descarta este paquete
            if len(packet[0][ICMP]) == 0:
                continue

            tx, rx = packet[0][ICMP][0]


            ip_recv = rx.src
            ips[ip_recv] = ips.get(ip_recv, 0) + 1

            total_rtt.append(rx.time-tx.sent_time)


        print_debug("--------------------------------------------")
        print_debug("TTL: {}".format(ttl))
        print_debug("IPS: {}".format(ips))
        print_debug("RTTS: {}".format(total_rtt))
        print_debug("--------------------------------------------")
        # Extrae de todas las ips la que mas aparecio
        ip = max(ips.items(),key=operator.itemgetter(1))[0]

        # Mide el RTT del salto actual restando
        # el RTT total actual y el RTT total anterior
        if result:
            avg = mean(total_rtt)
            prev_avg = result[-1]['rtt']
            mean_rtt = avg - prev_avg
        else: # Si es el primer salto, rtt total = rtt salto
            mean_rtt = mean(total_rtt)


        result.append({'ip':ip,
                       'rtt':mean_rtt})

        # Termina si alcanza la ip de destino
        if ip == ipdst:
            break
    return result

def main():
    parser = argparse.ArgumentParser(description='Traceroute')
    parser.add_argument('ip', type=str, help='Ip de destino')
    parser.add_argument('--packets-per-host', type=int, default=30, help="Packets por host")
    parser.add_argument('--timeout', type=int, default=20, help="Timeout de cada paquete en segundos")
    parser.add_argument('--max-ttl', type=int, default=60, help="Max ttl")
    parser.add_argument('-j', "--use-json", dest='use_json', action='store_true', help="Establece la salida en formato json")
    parser.add_argument("--no-use-json", dest='use_json', action='store_false', help="No imprime la salida en formato json. Por defecto.")
    parser.set_defaults(use_json=False)
    args = parser.parse_args()
    trace = traceroute(args.ip,
                       timeout=args.timeout,
                       max_ttl=args.max_ttl,
                       packets_per_host=args.packets_per_host)
    if args.use_json:
        json.dump({'trace' : trace})
    else:
        for t in trace:
            print("{} \t {:3.3f} ms".format(t['ip'],
                                             t['rtt'] * 1000))

if __name__ == '__main__':
    main()
