#!/usr/bin/python3

from mpl_toolkits.basemap import Basemap
import sys
import numpy as np
import matplotlib.pyplot as plt

def parse_longlat(line):
    str_ip, str_coord = line.strip().split("\t")
    str_lat, str_long=str_coord.strip().split(",")
    return str_ip, float(str_lat.strip()), float(str_long.strip())

coords = map(parse_longlat,sys.stdin.readlines())


# create new figure, axes instances.
fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])

# setup mercator map projection.
m = Basemap(width=1024,height=768,projection='kav7', lon_0=-90)

x = []
y = []

for i in range(len(coords)-1):
    ip0, lat0, long0 = coords[i]
    x.append(long0)
    y.append(lat0)
    if i == 0:
        rx, ry = m(long0-5, lat0-5)
        ax.annotate(ip0, (rx, ry), color="g")
    ip1, lat1, long1 = coords[i+1]
    x.append(long1)
    y.append(lat1)
    rx, ry = m(long1-5, lat1-5)
    ax.annotate(ip1, (rx, ry), color="g")
    m.drawgreatcircle(long0, lat0, long1, lat1, linewidth=1, color='r')

m.scatter(x,y, color='b', latlon=True)# ,latlong=True)

# m.bluemarble()
m.drawcoastlines()
m.drawmapboundary()
m.drawcountries()
# draw parallels
ax.set_title('')
fig.savefig('mapa.png')
