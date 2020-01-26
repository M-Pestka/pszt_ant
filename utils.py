import re
import pandas as pd

def extract_node(node_string):
    name = node_string.split('(')[0].strip()
    lat_and_lon = node_string.split('(')[-1].split(')')[0].strip()
    lon = float(lat_and_lon.split(' ')[0].strip())
    lat = float(lat_and_lon.split(' ')[1].strip())

    return {
        'name': name,
        'lat': lat,
        'lon': lon
    }

def extract_link(link_string):
    cost = re.findall('.*\((.*?)\)', link_string)[0].strip()
    cost = cost.split(' ')[-1]
    st = re.findall('.*?\((.*?)\)', link_string)[0].strip()
    source, target = st.split(' ')

    return {
        'source': source,
        'target': target,
        'cost': cost
    }

def load_network(path):
    with open(path, 'r') as file:
        text = file.read()

    # lines = text.split('\n')
    # for l in lines:
    #     if('NODES' in lines):
    nodes = re.findall('NODES \(\n([\s\S]*?)\n\)\n', text)
    nodes = pd.DataFrame(list(map(extract_node, filter(lambda x: x!='', nodes[0].split('\n')))))

    links =re.findall('LINKS \(\n([\s\S]*?)\n\)\n', text)
    links = pd.DataFrame(list(map(extract_link, filter(lambda x: x != '', links[0].split('\n')))))
    return nodes, links

if(__name__ == '__main__'):
    print(load_network('/home/pestka/Documents/studia/pszt/proj3/siec1.txt'))
