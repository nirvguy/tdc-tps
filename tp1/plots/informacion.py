#!/usr/bin/python3

import sys
import json
import matplotlib.pyplot as plt
import operator

def plot(information, entropy):
    fig, ax = plt.subplots()
    n = len(information)
    ind = range(n)
    if n > 30:
        max_label = 1
    else:
        max_label = n
    labels = list(map(lambda x: x[0], information[:max_label])) + ['' for x in information[max_label:]]
    bar_width = 0.3
    information = list(map(lambda x: x[1], information))
    ax.bar(ind, information, bar_width)
    ax.axhline(y=entropy, color='orange')
    ax.text(0.5, entropy + 0.1, 'Entropía', color='orange', fontsize=20)
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
