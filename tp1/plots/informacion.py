#!/usr/bin/python3

import sys
import json
import matplotlib.pyplot as plt
import operator
import math

def plot(information, entropy):
    fig, ax = plt.subplots()
    n = len(information)
    max_entropy = math.log2(n)
    ind = range(n)
    if n > 30:
        max_label = 1
    else:
        max_label = n
    labels = list(map(lambda x: x[0], information[:max_label])) + ['' for x in information[max_label:]]
    bar_width = 0.3
    information = list(map(lambda x: x[1], information))
    ax.bar(ind, information, bar_width)
    size_x = ax.get_xlim()[1] # size in pixels
    ax.axhline(y=entropy, color='orange')
    ax.text(0.5, entropy + 0.1, 'Entropía', color='orange', fontsize=20)
    ax.axhline(y=max_entropy, color='red')
    ax.text(size_x/2.0, max_entropy + 0.1, 'Entropía max.', color='red', fontsize=20)
    ax.set_xticks(ind)
    ax.set_ylabel('Información')
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

        if 'information' not in data or 'entropy' not in data:
            raise Exception("Archivo json invalido!")

        informacion = sorted(data['information'].items(), key=operator.itemgetter(1), reverse=False)
        plot(informacion, data['entropy'])

if __name__ == '__main__':
    main()
