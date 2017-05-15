#!/usr/bin/python3

import sys
import json
import math

def main():
    if len(sys.argv) < 2:
        print("Se esperaba el archivo json de entrada", file=sys.stderr)
        sys.exit(1)

    print("\\hline")
    print('Red & Entropía & Entropía Max & $\eta_{C}$ \\\\')
    print("\\hline")
    for filename in sys.argv[1:]:
        with open(filename, 'r') as json_file:
            str_json = json_file.read()
            data = json.loads(str_json)

            if 'entropy' not in data:
                raise Exception("Archivo json invalido!")

            entropia = data['entropy']
            n = len(data['information'])
            entropia_max = math.log2(n)
            eta_c = (entropia_max-entropia)/entropia
            print('{} & {:2.3f} & {:2.3f} & {:1.3f} \\\\'.format(filename, entropia,entropia_max,eta_c))
            print("\\hline")


if __name__ == '__main__':
    main()
