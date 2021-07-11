# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 16:17:16 2021

@author: B
"""

from wikidata.client import Client

from wiki_api import *

def get_instance(SEARCHPAGE):
    out = {}
    for k, v in get_links_withQ(SEARCHPAGE).items():
        print(k, v)
        client = Client()  # doctest: +SKIP
        entity = client.get(v[0], load=False)
        
        instance_prop = client.get('P31')
        instance = entity[instance_prop].label
        out[k] = instance
        print(instance)
        
    return out