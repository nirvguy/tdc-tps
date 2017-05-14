#!/usr/bin/python3

import sys
import json
import matplotlib.pyplot as plt

def plot(probabilidades):
    def destacados():
        max_prob = None
        for _, p in probabilidades.items():
            if max_prob is None:
                max_prob = p
            elif max_prob < p:
                max_prob = p
        return [0.1 if p == max_prob else 0.0 for _, p in probabilidades.items()]

    explode = destacados()
    labels = ["{} ({:3.2f}%)".format(s, p * 100.0) for s, p in probabilidades.items()]
    sizes = [ i * 100 for i in probabilidades.values() ]
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.legend(labels=labels, loc="best")
    patches = ax.pie(sizes, autopct='%1.1f%%', startangle=90, shadow=True, explode=explode)
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

        plot(data['probabilities'])

if __name__ == '__main__':
    main()
