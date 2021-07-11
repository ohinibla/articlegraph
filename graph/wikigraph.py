# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 10:15:30 2021

@author: B
"""
from scrap_wikipedia import *
from graphvis import *
from wiki_api import *


def graph_scr(_URL):
    url = _URL
    base_url = 'https://en.wikipedia.org'
    
    scr = Site(url)
    s_title = scr.get_title()
    links = scr.get_links_info()
    
    # construct the base graph
    G = GraphVisualization()
    
    # add the relations between links   
    links_ref = links.values()  
    objs = [Site(base_url + i) for i in links_ref] + [scr]
    for obj in objs:
        for i in links:
            if obj.soup.find('a', {'href': links[i]}):
                _t = obj.get_title()
                if _t != i:
                    G.addEdge(_t, i)
        
    G.visualize()
    
def graph_api(SEARCHPAGE):

    src_node = SEARCHPAGE 
    dest_nodes = get_links(src_node)
    
    # construct the base graph
    G = GraphVisualization()
    
    # add the main relations between parent node and links
    for n in dest_nodes:
        G.addEdge(src_node, n)
        
    # add the relations between links   
    for node in dest_nodes:
        for rel in relations(node, dest_nodes):
            G.addEdge(rel[0], rel[1])
    
    G.visualize()
