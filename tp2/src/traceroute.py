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

        if not ips:
            continue

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

table_t = [None,       # n = 0
           None,       # n = 1
           None,       # n = 2
           1.1511,     # n = 3
           1.4250,     # n = 4
           1.5712,     # n = 5
           1.6563,     # n = 6
           1.7110,     # n = 7
           1.7491,     # n = 8
           1.7770,     # n = 9
           1.7984,     # n = 10
           1.8153,     # n = 11
           1.8290,     # n = 12
           1.8403,     # n = 13
           1.8498,     # n = 14
           1.8579,     # n = 15
           1.8649,     # n = 16
           1.8710,     # n = 17
           1.8764,     # n = 18
           1.8811,     # n = 19
           1.8853,     # n = 20
           1,8891,     # n = 21
           1.8926,     # n = 22
           1,8957,     # n = 23
           1.8985,     # n = 24
           1.9011,     # n = 25
           1.9035,     # n = 26
           1.9057,     # n = 27
           1.9078,     # n = 28
           1.9096,     # n = 29
           1.9114,     # n = 30
           ]

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
    rtts = [e['rtt'] for e in trace]
    print(rtts)

    mu_rtt = mean(rtts)
    print(mu_rtt)
    std_rtt = std(rtts, mu_rtt)
    print(std_rtt)
    for i, h in enumerate(trace):
        n = (h['rtt'] - mu_rtt) / std_rtt
        trace[i]['norm_rtt'] = n
        trace[i]['intercontinental'] = abs(n)>table_t[len(trace)]

    if args.use_json:
        print(json.dumps({'trace' : trace}, indent=6))
    else:
        for t in trace:
            print("{} \t {:3.3f} ms \t {:3.3f} intercontinental={}".format(t['ip'],
                                                                           t['rtt'] * 1000,
                                                                           t['norm_rtt'],
                                                                           t['intercontinental']))

if __name__ == '__main__':
    main()
