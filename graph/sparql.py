# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 15:01:29 2021

@author: B
"""
from graph.wiki_api import *
import requests
import json
import re

def get_wikidata(Q):
    
    url = 'https://query.wikidata.org/sparql'
    
    _Q = ['wd:' + i for i in Q.values() if i != None]
    _Q = ' '.join(_Q)

    _query = """
    SELECT ?item ?itemLabel ?instance ?instanceLabel WHERE {
      VALUES ?item {%s}
      OPTIONAL { ?item wdt:P31/wdt:P279/wdt:P279/wdt:P279 ?instance. }
      OPTIONAL { ?item wdt:P279/wdt:P279/wdt:P279 ?instance. }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }"""
    
    query = _query %_Q   
    R = requests.get(url, params={'format': 'json', 'query': query})
    data = R.json()
    out = {}
    for v in data['results']['bindings']:
        try:
            Q_num = re.findall('Q.*', v['item']['value'])[0]
            out[Q_num] = v['instanceLabel']['value']
        except KeyError:
            out[re.findall('Q.*', v['item']['value'])[0]] = "None"
    return out
    