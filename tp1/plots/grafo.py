#!/usr/bin/python3
import sys
import json
import networkx as nx
import matplotlib.pyplot as plt
 

def plot(graph):
    G = nx.Graph()
    G.add_nodes_from(graph['nodes'])
    for u, v, c in graph['edges']:
        G.add_edge(u, v, label=str(c))
    nx.draw(G, with_labels=False, node_color="blue", alpha= 0.6, node_size=50,
            pos=nx.spring_layout(G))


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

        plot(data['graph'])
        plt.savefig(filename + ".png")
        plt.show()

if __name__ == '__main__':
    main()
