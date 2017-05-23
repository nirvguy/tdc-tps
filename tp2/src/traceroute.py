#!/usr/bin/python3
import time
import operator
from scapy.all import *
from utils import mean_std, cov

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
    prev_total_rtt = None
    for ttl in range(1, max_ttl+1):
        # Diccionario con las ips que van apareciendo para el mismo ttl
        ips = dict()
        total_rtt = []
        for i in range(packets_per_host):
            # Envia el paquete cronometrando cuanto tiempo tarda
            # entre que se envia y se recibe para conseguir
            # un RTT aproximado
            t1 = time.time()
            packet = sr(IP(dst=ipdst, ttl=ttl)/ICMP(),
                        timeout=timeout,
                        verbose=verbose)
            t2 = time.time()

            # Si no llego respuesta descarta este paquete
            if len(packet[0][ICMP]) == 0:
                continue

            icmp_response = packet[0][ICMP][0][1]

            ip_recv = icmp_response.src
            ips[ip_recv] = ips.get(ip_recv, 0) + 1

            total_rtt.append(t2-t1)

        # Extrae de todas las ips la que mas aparecio
        ip = max(ips.items(),key=operator.itemgetter(1))[0]

        # Mide el RTT del salto actual restando
        # el RTT total actual y el RTT total anterior
        if prev_total_rtt:
            mean_total_rtt, std_total_rtt = mean_std(total_rtt)
            mean_prev_total_rtt, std_prev_total_rtt = mean_std(prev_total_rtt)
            mean_rtt = mean_total_rtt - mean_prev_total_rtt
            # TODO: Verificar esto
            std_rtt = math.sqrt(std_total_rtt**2 +
                                std_prev_total_rtt**2)
        else: # Si es el primer salto, rtt total = rtt salto
            mean_rtt, std_rtt = mean_std(total_rtt)

        prev_total_rtt = list(total_rtt)

        result.append({'ip':ip,
                       'rtt':(mean_rtt, std_rtt)})

        # Termina si alcanza la ip de destino
        if ip == ipdst:
            break
    return result
