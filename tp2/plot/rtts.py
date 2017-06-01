#!/usr/bin/python3

import sys
import json
import matplotlib.pyplot as plt
import operator
import numpy as np
import math

def plot(trace, value_table):
    length = len(trace)
    ind_labels = range(length)
    labels = []
    for i in ind_labels:
        labels.append(trace[i-1]['ip'])

    plt.rc('text', usetex=True)

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    # Carga datos apartir de trace
    mean_rtts = list(map(lambda x: x['mean_total_rtt'] * 1000, trace))
    std_rtts = list(map(lambda x: x['std_total_rtt'] * 1000,trace))
    norm_rtts = list(map(operator.itemgetter('norm_rtt'),trace))
    colors = np.array(['teal' if n < value_table else 'orange' for n in norm_rtts])

    ##############################################
    ##                                          ##
    ##  Barplot con los delta RTTS normalizados ##
    ##                                          ##
    ##############################################
    bar_width = 0.2
    # Eje X
    ax1.set_xticks(ind_labels)
    ax1.set_xlabel('IPS', fontsize=20)
    ax1.set_xticklabels(labels, rotation=90)
    # Eje Y
    ax1.set_ylabel('$\\frac{\\Delta RTT-\\mu}{\\sigma}$', color='teal', fontsize=20)
    ax1.bar(range(length), norm_rtts, bar_width, color=colors)
    # Linea de corte
    ax1.axhline(y=value_table, color='orange')
    ax1.text(0.5, value_table + 0.1, 'Nivel de corte', color='orange', fontsize=20)

    ##############################################
    ##                                          ##
    ##     Grafico con los RTTs totales         ##
    ##                                          ##
    ##############################################
    ax2.errorbar(range(length), mean_rtts, std_rtts, marker='.', color='red')
    ax2.grid(color='gray', linewidth=1)
    ax2.set_ylabel('Total RTT (ms)', color='r', fontsize=20)

    plt.tight_layout()
    plt.show()

def main():
    if len(sys.argv) < 2:
        # print("Se esperaba el archivo json de entrada", file=sys.stderr)
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, 'r') as json_file:
        str_json = json_file.read()
        data = json.loads(str_json)

        if 'trace' not in data:
            raise Exception("Archivo json invalido!")

        plot(data['trace'], data['value_table'])

if __name__ == '__main__':
    main()
