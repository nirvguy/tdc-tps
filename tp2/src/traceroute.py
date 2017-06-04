#!/usr/bin/python3
import time
import operator
import argparse
import json
from scapy.all import *
from utils import *
from table_t import table_t

DEBUG = True

def print_debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs, file=sys.stderr)

def get_rtts(total_rtts, prev_mean_total_rtt):
    mean_total_rtt, std_total_rtt = mean_std(total_rtts)
    mean_rtt_e = mean_total_rtt - prev_mean_total_rtt
    return mean_total_rtt, std_total_rtt, mean_rtt_e

def traceroute(ipdst, packets_per_ttl=30, timeout=2, iface=None,
               verbose=False, max_ttl=30):
    """ Traceroute mediante el metodo de ttl seeder
        @param ipdst Ip de destino
        @param packets_per_ttl Cuantos paquetes se envían
                                para el mismo ttl
        @param iface  Interface
        @timeout Timeout de cada paquete
    """
    discarded = []
    result = []

    extra_args = {}
    if iface:
        extra_args = {'iface' : iface}

    # RTTS
    mean_total_rtt = None # Promedio RTTs totales
    std_total_rtt = None # Desviacion estandar RTTS totales
    mean_rtt_e = None # Promedio de RTT del enlace

    ttl = 1
    bounded = False

    no_time_exceeded = 0

    while ttl <= max_ttl and not bounded:
        # Diccionario con las ips que van apareciendo para el mismo ttl
        ips = dict()

        # RTTS totales que van apareciendo para el mismo TTL
        total_rtt = []

        for i in range(packets_per_ttl):
            # Envia el paquete cronometrando cuanto tiempo tarda
            # entre que se envia y se recibe para conseguir
            # un RTT aproximado
            packet = sr(IP(dst=ipdst, ttl=ttl)/ICMP(),
                        timeout=timeout,
                        verbose=verbose,
                        **extra_args)

            # Si no llego respuesta descarta este paquete
            if len(packet[0][ICMP]) == 0:
                continue

            tx, rx = packet[0][ICMP][0]

            assert(rx.type == 0 or rx.type == 11)
            if rx.type == 0:
                bounded = True

            ip_recv = rx.src
            ips[ip_recv] = ips.get(ip_recv, 0) + 1

            total_rtt.append(rx.time-tx.sent_time)


        print_debug("--------------------------------------------")
        print_debug("TTL: {}".format(ttl))
        print_debug("IPS: {}".format(ips))
        print_debug("RTTS: {}".format(total_rtt))
        print_debug("--------------------------------------------")

        if not ips:
            no_time_exceeded += 1
            ttl += 1
            continue

        # Extrae de todas las ips la que mas aparecio
        ip = max(ips.items(),key=operator.itemgetter(1))[0]

        # Mide el RTT del salto actual restando
        # el RTT total actual y el RTT total anterior
        if result:
            mean_total_rtt, std_total_rtt, mean_rtt_e = get_rtts(total_rtt,
                                                                 result[-1]['mean_total_rtt'])
        else: # Si es el primer salto, rtt total = rtt salto
            mean_total_rtt, std_total_rtt, mean_rtt_e = get_rtts(total_rtt,
                                                                 0)

        print_debug("MEAN_RTT_E: ", mean_rtt_e)

        if mean_rtt_e < 0:
            discarded.append({'ttl': ttl,
                              'ip':ip})
            ttl += 1
            continue

        result.append({'ttl': ttl,
                       'ip':ip,
                       'mean_total_rtt' : mean_total_rtt,
                       'std_total_rtt' : std_total_rtt,
                       'mean_rtt_e': mean_rtt_e})
        ttl += 1

    return result, discarded, no_time_exceeded/ttl


def main():
    parser = argparse.ArgumentParser(description='Traceroute')
    parser.add_argument('ip', type=str, help='Ip de destino')
    parser.add_argument('--iface', type=str, default='', help="Interfaz de red")
    parser.add_argument('--packets-per-ttl', type=int, default=30, help="Paquetes por ttl")
    parser.add_argument('--timeout', type=int, default=2, help="Timeout de cada paquete en segundos")
    parser.add_argument('--max-ttl', type=int, default=30, help="Max ttl")
    parser.add_argument('-j', "--use-json", dest='use_json', action='store_true', help="Establece la salida en formato json")
    parser.add_argument("--no-use-json", dest='use_json', action='store_false', help="No imprime la salida en formato json. Por defecto.")
    parser.set_defaults(use_json=False)
    args = parser.parse_args()
    trace, discarded, p_ttl_no_time_exceeded = traceroute(args.ip,
                                                          iface=args.iface,
                                                          timeout=args.timeout,
                                                          max_ttl=args.max_ttl,
                                                          packets_per_ttl=args.packets_per_ttl)
    delta_rtts = [e['mean_rtt_e'] for e in trace]

    mu_delta_rtts, std_delta_rtts = mean_std(delta_rtts)

    value_table = table_t[len(trace)]

    print_debug("n: " + str(len(trace)))
    print_debug("% HOPs No time exceeded: {:3.2f}".format(p_ttl_no_time_exceeded * 100))
    print_debug("% discarded: {:3.2f}%".format(len(discarded) / (len(trace) + len(discarded)) * 100))
    print_debug("Table: " + str(table_t[len(trace)]))

    for i, delta_rtt in enumerate(delta_rtts):
        z = abs((delta_rtt - mu_delta_rtts) / std_delta_rtts)
        trace[i]['norm_rtt'] = z
        trace[i]['intercontinental'] = z > value_table

    if args.use_json:
        print(json.dumps({'trace' : trace,
                          'discarded' : discarded,
                          'value_table': value_table }, indent=6))
    else:
        print("TTL \t IP \t Total RTT \t Std Total RTT \t Delta RTT \t Z Delta RTT \t Intercontinental ")
        for t in trace:
            print("{} \t {} \t {:3.3f} ms \t {:3.3f} ms \t {:3.3f} ms \t {:1.3f} \t {}".format(t['ttl'], t['ip'],
                                                                                               t['mean_total_rtt'] * 1000,
                                                                                               t['std_total_rtt'] * 1000,
                                                                                               t['mean_rtt_e'] * 1000,
                                                                                               t['norm_rtt'],
                                                                                               t['intercontinental']))
        print("Valor Table t: ", value_table)

        print("Descartados:")
        print("TTL \t IP")
        for d in discarded:
            print("{} \t {}".format(d['ttl'], d['ip']))

if __name__ == '__main__':
    main()
