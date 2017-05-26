#!/usr/bin/python3
import math

def mean(xs):
    mean = sum(xs)/len(xs)
    return mean

def std(xs, mu=None):
    if mu is None:
        mu = mean(xs)
    return math.sqrt(sum((x-mu)**2 for x in xs))

def cov(xs, ys):
    mean_xs = sum(xs)/len(xs)
    mean_ys = sum(ys)/len(ys)
    return sum((x-mean_xs)*(y-mean_ys) for x,y in zip(xs, ys))/len(xs)

