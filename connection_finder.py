#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 2020 16:53:41 EST

@author: marcogancitano

Main module for wikipedia-connection-finder.
"""

import queue
import re
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
import networkx as nx
import requests

BASE_URL = 'https://en.wikipedia.org'
INTERNAL_LINK_REGEX = re.compile('/wiki/\S+')
FILE_REGEX = re.compile('\S*:\S*')


def is_absolute(url):
    """Determine whether url is absolute or not."""
    return bool(urlparse(url).netloc)


class ConnectionFinder:
    """Class for finding the shortest connection between two wikipedia articles."""

    def __init__(self, start_url, end_url, max_layers=7, verbose=False):
        """Instantiate ConnectionFinder class.

        Args:
            start_url (string): URL representing the Wikipedia article to start at
            end_url (string): URL representing the Wikipedia article to find
            max_layers (int, default=7): Maximum amount of layers to follow before giving up
            verbose (bool): Whether to print out debugging messages

        Raises:
            TypeError: If any parameters aren't the correct types
            ValueError: If max_layers isn't a positive integer

        """

        self.start_url = start_url
        self.end_url = end_url
        self.max_layers = max_layers
        self.verbose = verbose

        self.graph = nx.DiGraph()
        self.graph.add_node(start_url)

        self.q = queue.Queue()
        self.q.put((start_url, 0))

        self.current_layer = 0
        self.end_found = False
        self.shortest_path = []

    def find_connection(self):
        if self.verbose:
            print('Layer: 0')

        while not self.end_found:
            url, url_layer = self.q.get()

            if self.verbose:
                if url_layer > self.current_layer:
                    if url_layer <= self.max_layers:
                        self.current_layer = url_layer
                        print('Layer: %i' % self.current_layer)
                    else:
                        print("Max layer reached. No solution found.")
                        break

            links = self.get_links_from_page(url)

            for link in links:
                if self.end_found:
                    break

                self.update_queue_and_graph(link, url, url_layer)

    def get_shortest_path(self):
        self.shortest_path = nx.shortest_path(
            self.graph,
            source=self.start_url,
            target=self.end_url
        )

    def update_queue_and_graph(self, link, url, url_layer):

        u = link.get('href')
        if u is None:
            u = ""

        if INTERNAL_LINK_REGEX.match(u) and not FILE_REGEX.match(u):
            u = urljoin(BASE_URL, u)
            temp = urlparse(u)
            u = temp.scheme + "://" + temp.netloc + temp.path

            if not self.graph.has_node(u):
                self.q.put((u, url_layer + 1))

            self.graph.add_edge(url, u)

        if u == self.end_url:
            self.end_found = True

    @staticmethod
    def get_links_from_page(url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        links = soup.find_all('a')
        links = [link for link in links if link is not None]

        return links

    @property
    def path(self):
        if self.shortest_path:
            return "\n".join(self.shortest_path)

        return "No path found."


if __name__ == "__main__":

    start_url = "https://en.wikipedia.org/wiki/Chicago"
    end_url = "https://en.wikipedia.org/wiki/Amsterdam"

    connection_finder = ConnectionFinder(
        start_url=start_url,
        end_url=end_url
    )

    connection_finder.find_connection()
    connection_finder.get_shortest_path()
    print(connection_finder.path)

