#!/usr/bin/python3

import sys
import json
import matplotlib.pyplot as plt

def plot(information, entropy):
    fig, ax = plt.subplots()
    ind = range(len(information))
    labels = information.keys()
    bar_width = 0.3
    information = information.values()
    ax.bar(ind, information, bar_width)
    ax.axhline(y=entropy, color='orange')
    ax.text(0.5, entropy + 0.1, 'Entropía', color='orange', fontsize=20)
    ax.set_xticks(ind)
    ax.set_ylabel('Información')
    ax.set_xticklabels(labels, rotation=45)
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

        plot(data['information'], data['entropy'])

if __name__ == '__main__':
    main()
