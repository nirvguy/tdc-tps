#!/usr/bin/python3
import math

def mean(xs):
    mean = sum(xs)/len(xs)
    return mean

def std(xs, mu=None):
    if mu is None:
        mu = mean(xs)
    return math.sqrt(sum((x-mu)**2 for x in xs)/len(xs))

def mean_std(xs):
    mu = mean(xs)
    return mu, std(xs, mu=mu)
