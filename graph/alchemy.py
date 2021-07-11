# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 10:00:14 2021

@author: B
"""
from graph.wiki_api import *
import json

def IntraGraphJSON(SEARCHPAGE, file=False):
    
    graph_dict = {"nodes": [], "edges": []}
    id_dict = {}
    relations = [SEARCHPAGE] + get_links(SEARCHPAGE)
    in_relations = intra_relations(SEARCHPAGE)
    id = 0
    
    for s_node in relations:
        id_dict[s_node] = id
        graph_dict["nodes"].append({"caption": s_node, "id": id_dict[s_node]})
        id += 1

    for src in in_relations:
        for trg in in_relations[src]:
            graph_dict["edges"].append({"source": id_dict[src],
                                        "target": id_dict[trg]})
        
    if file:
        with open('graph/static/graph/graphJSON.json', 'w') as outfile:
            json.dump(graph_dict, outfile)
    else:
        return json.dumps(graph_dict)
    
def GraphJSON(SEARCHPAGE, file=False):
    
    graph_dict = {"nodes": [{'caption': SEARCHPAGE, "id": 0}], "edges": []}
    id_dict = {}
    relations = get_links(SEARCHPAGE)
    id = 1
    
    graph_dict['nodes'][0]['root'] = True
    
    for s_node in relations:
        id_dict[s_node] = id
        graph_dict["nodes"].append({"caption": s_node, "id": id_dict[s_node]})
        graph_dict["edges"].append({"source": 0, "target": id_dict[s_node]})
        id += 1
        
    
    
    if file:
        with open('graph/static/graph/graphJSON.json', 'w') as outfile:
            json.dump(graph_dict, outfile)
    else:
        return json.dumps(graph_dict)
    
def IntraGraphJSON_v2(SEARCHPAGE, file=False):
    
    graph_dict = {"nodes": [], "edges": []}
    id_dict = {}
    relations = [SEARCHPAGE] + get_links(SEARCHPAGE)
    in_relations = intra_relations_v2(SEARCHPAGE)
    id = 0
    
    for s_node in relations:
        id_dict[s_node] = id
        graph_dict["nodes"].append({"caption": s_node, "id": id_dict[s_node]})
        id += 1
        
    graph_dict['nodes'][0]['root'] = True
    
    for k, v in in_relations.items():
        for target in v:
            graph_dict["edges"].append({"source": id_dict[k],
                                        "target": id_dict[target]})
        
    if file:
        with open('graph/static/graph/graphJSON.json', 'w') as outfile:
            json.dump(graph_dict, outfile)
    else:
        return json.dumps(graph_dict)
    