#!/usr/bin/python3

import sys
import json
import matplotlib.pyplot as plt

def plot(probabilidades):
    labels = ["{} ({:3.2f}%)".format(s, p * 100.0) for s, p in probabilidades.items()]
    sizes = [ i * 100 for i in probabilidades.values() ]
    fig, ax = plt.subplots()
    patches = ax.pie(sizes, autopct='%1.1f%%', startangle=90, shadow=True)
    ax.legend(labels=labels, loc="best")
    plt.axis('equal')
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
