#!/usr/bin/python3

from mpl_toolkits.basemap import Basemap
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects

def parse_longlat(line):
    str_ip, str_coord = line.strip().split("\t")
    str_lat, str_long=str_coord.strip().split("_")
    return str_ip, float(str_lat.strip()), float(str_long.strip())

coords = map(parse_longlat,sys.stdin.readlines())


# create new figure, axes instances.
fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])

# setup mercator map projection.
m = Basemap(width=1024,height=768,projection='kav7', lon_0=0)

x = []
y = []

for i in range(len(coords)-1):
    path_effects=[PathEffects.withStroke(linewidth=2,foreground="w")]
    ip0, lat0, long0 = coords[i]
    if i == 0:
        rx, ry = m(long0, lat0)
        x.append(rx)
        y.append(ry)
        ax.annotate(ip0, (rx, ry), color="purple", fontsize=8,
                    path_effects=path_effects)
    ip1, lat1, long1 = coords[i+1]
    rx, ry = m(long0, lat0)
    x.append(rx)
    y.append(ry)
    rx, ry = m(long1, lat1)
    ax.annotate(ip1, (rx, ry), color="purple", fontsize=8,
                path_effects=path_effects)
    m.drawgreatcircle(long0, lat0, long1, lat1, linewidth=1, color='r')

print(x)
print(y)

m.scatter(x,y, 40,color='green')

m.drawlsmask(land_color = "#ddaa66", 
               ocean_color="#7777ff",
               resolution = 'l')
m.drawcoastlines()
# m.drawmapboundary()
m.drawcountries()
# draw parallels
ax.set_title('')
fig.savefig('mapa.png')
