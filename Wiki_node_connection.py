#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 17:02:50 2019

@author: marcogancitano
"""
import functions

run_again = 'y'
while run_again == 'y' or run_again == 'yes':
    start_url = input('Enter starting wikipage: ')
    end_url = input('Enter ending wikipage: ')
    layer_cap = input('Max layers to check (Default = 7): ')
    
    if layer_cap == '':
        functions.find_connection(start_url,end_url)
    else:
        functions.find_connection(start_url,end_url,layer_cap)

    run_again = input('Run another connection? (y/n): ').lower()