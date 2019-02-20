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
import requests 

def is_absolute(url):
    """Determine whether url is absolute or not."""
    return bool(urlparse(url).netloc)

def bfs(graph, start, end):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # path found
        if node == end:
            return path
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in graph.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)

def find_connection(start_url,end_url,layer_cap = 7):
    base_url = 'https://en.wikipedia.org'

    internal_link = re.compile('/wiki/\S+')
    file = re.compile('\S*:\S*')
    
    linked_sites = {start_url:0}
    visited_sites = {}

    q = queue.Queue()
    q.put((start_url,0))
    hitler_found = False
    max_layer = 0
    print('Layer: %i' %max_layer)
    while not hitler_found:
        url_tuple = q.get()
        url = url_tuple[0]
        url_layer = url_tuple[1]
        
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
            
                if u in linked_sites.keys():
                    linked_sites[u] += 1
                else:
                    linked_sites[u] = 1
                    q.put((u,url_layer + 1))
                    dict_links.append(u)

            if end_url == u:
                hitler_found = True
                print('Connection Found!')
                break
        visited_sites[url] = dict_links
    results = bfs(visited_sites, start_url, end_url)
    i = 0
    print('Degrees to end site: %i' %(len(results)-2))
    for result in results:
        print('%i: %s'  %(i,result))
        i += 1