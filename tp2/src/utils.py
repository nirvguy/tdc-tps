#!/usr/bin/python3
import math

def mean_std(xs):
    mean = sum(xs)/len(xs)
    std = math.sqrt(sum((x-mean)**2 for x in xs)/len(xs))
    return mean, std

def cov(xs, ys):
    mean_xs = sum(xs)/len(xs)
    mean_ys = sum(ys)/len(ys)
    return sum((x-mean_xs)*(y-mean_ys) for x,y in zip(xs, ys))/len(xs)

