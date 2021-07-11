# -*- coding: utf-8 -*-

from graph.wiki_api import *
from graph.sparql import *

def Graph(SEARCHPAGE):
    
    nodes = [{"id": 0, "label": SEARCHPAGE, "group": "root"}]
    edges = []
    id_dict = {}
    relations = get_links_withQ(SEARCHPAGE)
    Q = get_wikidata(relations)
    id = 1
    for s_node in relations:
        id_dict[s_node] = id
        nodes.append({"id": id_dict[s_node], "label": s_node, "group": Q.get(relations[s_node], "None")})
        edges.append({"from": 0, "to": id_dict[s_node]})
        id += 1
        
    return nodes, edges

def IntraGraph_v2(SEARCHPAGE):
    
    nodes = []
    edges = []
    id_dict = {}
    _relations = get_links_withQ(SEARCHPAGE)
    relations = [SEARCHPAGE] + list(_relations.keys())
    # return relations
    in_relations = intra_relations_v2(SEARCHPAGE)
    Q = get_wikidata(_relations)
    # return Q
    _relations[SEARCHPAGE] = None
    id = 0
    
    for s_node in relations:
        id_dict[s_node] = id
        nodes.append({"id": id_dict[s_node], "label": s_node, "group": Q.get(_relations[s_node], "None")})
        id += 1
    print(id_dict)
    for k, v in in_relations.items():
        for target in v:
            try:
                edges.append({"from": id_dict[k], "to": id_dict[target]})
            except KeyError:
                continue

    return nodes, edges