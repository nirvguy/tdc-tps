#!/usr/bin/python3
import math

class Fuente:
    def __init__(self, simbolos):
        self.muestras = {s: 0 for s in simbolos}
        self.cantidad_muestras = 0
    
    def __str__(self):
        return "\n".join("{}: {}".format(s, p) for s, p in self.probabilidades())

    def probabilidades(self):
        if self.cantidad_muestras == 0 or len(self.muestras) == 0:
            raise Exception("No se registraron muestras en la fuente")
        return {(s, c / self.cantidad_muestras) for s, c in self.muestras.items()}

    def informacion(self):
        return {s: -math.log2(p) for s, p in self.probabilidades()}

    def entropia(self):
        return -sum(p * math.log2(p) for _, p in self.probabilidades())

    def agregar_muestra(self, simbolo):
        self.cantidad_muestras += 1
        c = self.muestras.get(simbolo) or 0
        self.muestras[simbolo] = c + 1
