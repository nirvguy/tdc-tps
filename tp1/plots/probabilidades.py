#!/usr/bin/python3

import sys
import json
import matplotlib.pyplot as plt

def plot(information):
    labels = information.keys()
    sizes = [ i * 100 for i in information.values() ]
    fig, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    fig.savefig(sys.stdout.buffer)

def main():
    if len(sys.argv) < 2:
        print("Se esperaba el archivo json de entrada", file=sys.stderr)
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, 'r') as json_file:
        str_json = json_file.read()
        data = json.loads(str_json)

        if 'information' not in data:
            raise Exception("Archivo json invalido!")

        plot(data['information'])

if __name__ == '__main__':
    main()