#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 17:02:50 2019

@author: marcogancitano
"""
from connection_finder import ConnectionFinder

run_again = 'y'
while run_again == 'y' or run_again == 'yes':
    start_url = input('Enter starting wikipage: ')
    end_url = input('Enter ending wikipage: ')
    max_layers = input('Max layers to check (Default = 7): ')
    
    if max_layers == '':
        connection_finder = ConnectionFinder(
            start_url=start_url,
            end_url=end_url
        )
    else:
        connection_finder = ConnectionFinder(
            start_url=start_url,
            end_url=end_url,
            max_layers=max_layers
        )

    connection_finder.find_connection()
    connection_finder.get_shortest_path()
    print(connection_finder.path)

    run_again = input('Run another connection? (y/n): ').lower()