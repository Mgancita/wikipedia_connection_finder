#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 17:02:50 2019

@author: marcogancitano
"""

import queue
import re
from urllib.parse import urljoin,urlparse

from bs4 import BeautifulSoup
import networkx as nx
import requests 

def is_absolute(url):
    """Determine whether url is absolute or not."""
    return bool(urlparse(url).netloc)

def find_connection(start_url,end_url,layer_cap = 7):
    base_url = 'https://en.wikipedia.org'

    internal_link = re.compile('/wiki/\S+')
    file = re.compile('\S*:\S*')
    
    network_graph = nx.Graph()
    network_graph.add_node(start_url)

    q = queue.Queue()
    q.put((start_url,0))
    end_found = False
    max_layer = 0
    print('Layer: %i' %max_layer)
    while not end_found:
        url_tuple = q.get()
        url = url_tuple[0]
        url_layer = int(url_tuple[1])
        
        if(url_layer > max_layer):
            if(url_layer <= layer_cap):
                max_layer = url_layer
                print('Layer: %i' %max_layer)
            else:
                print("Max layer reached. No solution found.")
                break
        
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'html.parser')
        
        links = soup.find_all('a')
        links = [link for link in links if link is not None]
        dict_links = []
        for link in links:
            #If link is an absolute link put as normal, if not make absolute
            u = link.get('href')
            if u is None:
                u = ''
            if internal_link.match(u) and not file.match(u):
                u = urljoin(base_url,u)
                temp = urlparse(u)
                u = temp.scheme + "://" + temp.netloc + temp.path
            
                if not network_graph.has_node(u):
                    q.put((u,url_layer+1))
                
                network_graph.add_edge(url,u)

            if end_url == u:
                end_found = True
                print('Connection Found!')
                break
    shortest_path = nx.shortest_path(network_graph, source=start_url, target=end_url)  
    print('Degrees to end site: %i' %(len(shortest_path)-2))
    i = 0
    for node in shortest_path:
        print('%i: %s'  %(i,node))
        i += 1
    return network_graph