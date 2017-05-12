#!/usr/bin/python3
import sys
import json
from graphviz import Graph

def plot(dot, graph):
    for u in graph['nodes']:
        dot.node(u, "", color='blue', pos="0,0!")
    for u, v, c in graph['edges']:
        dot.edge(u, v)


def main():
    if len(sys.argv) < 2:
        print("Se esperaba el archivo json de entrada", file=sys.stderr)
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, 'r') as json_file:
        str_json = json_file.read()
        data = json.loads(str_json)

        if 'graph' not in data or \
           'nodes' not in data['graph'] or \
           'edges' not in data['graph']:
            raise Exception("Archivo json invalido!")

        dot = Graph(comment='Graph')
        plot(dot, data['graph'])
        dot.render(filename + '.pdf', view=True)

if __name__ == '__main__':
    main()
