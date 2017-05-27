#!/usr/bin/python3

import sys
import json
import matplotlib.pyplot as plt
import operator
import math

def plot(trace):
    fig, ax = plt.subplots()
    n = len(trace)
    ind = range(n)
    ind_labels = range(n+1)
    labels = []
    for i in ind_labels:
        if i == 0:
            labels.append("")
        else:
            labels.append(trace[i-1]['ip'])
    # for i in ind:
    #     if i == 0:
    #         labels.append(trace[i]['ip'])
    #     else:
    #         labels.append("{} - {}".format(trace[i-1]['ip'],trace[i]['ip']))
    rtts = list(map(lambda x: x['rtt'] * 1000, trace))
    bar_width = 0.3
    ax.bar(ind, rtts, bar_width)
    ax.set_xticks(list(map(lambda x:x-0.5, ind_labels)))
    ax.set_ylabel('RTT enlace (ms)')
    ax.set_xticklabels(labels, rotation=90)
    fig.tight_layout()
    fig.savefig(sys.stdout.buffer)

def main():
    if len(sys.argv) < 2:
        print("Se esperaba el archivo json de entrada", file=sys.stderr)
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, 'r') as json_file:
        str_json = json_file.read()
        data = json.loads(str_json)

        if 'trace' not in data:
            raise Exception("Archivo json invalido!")

        plot(data['trace'])

if __name__ == '__main__':
    main()
