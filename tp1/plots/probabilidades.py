#!/usr/bin/python3

import sys
import json
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import operator
import random

def plot(probabilidades):
    def destacados():
        max_prob = None
        for _, p in probabilidades:
            if max_prob is None:
                max_prob = p
            elif max_prob < p:
                max_prob = p
        return [0.05 if p == max_prob else 0.0 for _, p in probabilidades]

    explode = destacados()
    colors = list(reversed(cm.rainbow(np.linspace(0, 1, len(probabilidades)))))
    labels = ["{} ({:3.2f}%)".format(s, p * 100.0) for s, p in probabilidades]
    sizes = [ p * 100 for _, p in probabilidades ]
    fig, ax = plt.subplots(figsize=(10, 10))
    patches = ax.pie(sizes, autopct='%1.1f%%', startangle=90, shadow=True, explode=explode, colors=colors)
    ax.legend(labels=labels, loc="best")
    # plt.axis('equal')
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

        if 'probabilities' not in data:
            raise Exception("Archivo json invalido!")

        probabilidades = sorted(data['probabilities'].items(), key=operator.itemgetter(1), reverse=True)
        plot(probabilidades)

if __name__ == '__main__':
    main()
