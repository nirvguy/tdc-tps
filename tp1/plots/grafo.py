#!/usr/bin/python3
import sys
import json
import networkx as nx
import matplotlib.pyplot as plt
 

def plot(graph):
    G = nx.Graph()
    G.add_nodes_from(graph['nodes'])
    for u, v, c in graph['edges']:
        G.add_edge(u, v, cost=str(c)) 
    edge_labels = nx.get_edge_attributes(G, 'cost')
    pos = nx.spring_layout(G)
    nx.draw(G,pos=pos, node_size=24, alpha=0.5)
    nx.draw_networkx_edge_labels(G,pos=pos, edge_labels=edge_labels, alpha=0.5)


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
        plt.savefig(sys.stdout.buffer)

if __name__ == '__main__':
    main()
