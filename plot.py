#!/usr/bin/python3
import utm
import pandas as pd
from utils import load_network
import matplotlib
import matplotlib.pyplot as plt

def convert_row(row):
    a, b, c, d = utm.from_latlon(row['lat'], row['lon'], force_zone_number = 1, force_zone_letter = 'S')
    row['lat'] = a
    row['lon'] = b
    return row



def to_utm(data ):
    return data.apply(convert_row, axis=1)


nodes, links = load_network('/home/pestka/Documents/studia/pszt/proj3/sndlib-networks-native/polska.txt')

# nodes = to_utm(nodes)


name_map = {r['name']:(r['lat'], r['lon']) for i, r in nodes.iterrows()}

MAX_COST = links.cost.map(float).max() / 3.
for i, row in links.iterrows():
    p1 = name_map[row['source']]
    p2 = name_map[row['target']]
    plt.plot([p1[1], p2[1]], [p1[0], p2[0]], c='gray', linewidth = float(row['cost']) / MAX_COST)

plt.scatter(x=nodes.lon, y=nodes.lat)
plt.show()
