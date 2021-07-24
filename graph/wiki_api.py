# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 08:48:58 2021

@author: B
"""


import requests
import json
import re

URL = "https://en.wikipedia.org/w/api.php"

def get_search_result(SEARCHPAGE):

    S = requests.Session()
    # URL = "https://en.wikipedia.org/w/api.php"
    
    PARAMS = {
        "action": "query",
        "generator": "search",
        "format": "json",
        "gsrsearch": SEARCHPAGE,
        "prop": "info",
        "inprop": "url",
        "gsrprop": "snippet"
    }
    
    R = S.get(url=URL, params=PARAMS)
    
    DATA = R.json()
    links = []
    # return DATA
    for i in DATA['query']['pages']:
        links.append((DATA['query']['pages'][i]['title'],
                      DATA['query']['pages'][i]['fullurl'],
                      # re.sub('<span.*?</span>', '', DATA['query']['pages'][i]['snippet'])))
                      DATA['query']['pages'][i]['snippet']))
    return links

def get_randompage():
    
    S = requests.Session()
    
    PARAMS = {
    	"action": "query",
    	"format": "json",
    	"prop": "info",
    	"generator": "random",
    	"inprop": "url",
    	"grnnamespace": "0"
    }
    
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    
    pages = DATA['query']['pages']
    for k, v in pages.items():
        r_name = pages[k]['title']
        r_address = pages[k]['fullurl']
    return (r_name, r_address)

def get_links(SEARCHPAGE):
    
    S = requests.Session()
    
    PARAMS = {
    	"action": "query",
    	"format": "json",
    	"prop": "links",
    	"titles": SEARCHPAGE,
    	"plnamespace": "0",
    	"pllimit": "max"
        }
    
    out = []
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    pages = DATA['query']['pages']
    for i in pages:
        try:
            for j in pages[i]['links']:
                out.append(j['title'])
        except KeyError:
            continue
   
    while 'continue' in DATA:
        PARAMS['plcontinue'] = DATA['continue']['plcontinue']
        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()
        for i in DATA['query']['pages']:
            for j in DATA['query']['pages'][i]['links']:
                out.append(j['title'])
                
    return out

def get_links_length(SEARCHPAGE):
    
    S = requests.Session()

    PARAMS = {
    	"action": "query",
    	"format": "json",
    	"prop": "info",
    	"continue": "gplcontinue||",
    	"titles": SEARCHPAGE,
    	"generator": "links",
    	"gpllimit": "max",
        "redirects": 1,
        "gplnamespace": 0
    }
        
    out = {}
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    # print(json.dumps(DATA, indent=4))
    # return DATA
    pages = DATA['query']['pages']

    for v in pages.values():
        out[v['title']] = v['length']

    while 'continue' in DATA:
        PARAMS['gplcontinue'] = DATA['continue']['gplcontinue']
        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()
        for v in pages.values():
            out[v['title']] = v['length']
                
    return out
    
def get_links_withQ(SEARCHPAGE):
    
    S = requests.Session()
    
    PARAMS = {
    	"action": "query",
    	"format": "json",
    	"prop": "pageviews|pageprops",
    	"titles": SEARCHPAGE,
    	"generator": "links",
    	"redirects": 1,
    	"pvipdays": "1",
    	"ppprop": "wikibase_item",
    	"gplnamespace": "0",
    	"gpllimit": "max"
        }
    
    out = {}
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    # with open('testDump/test.json', 'w') as f:
    #     json.dump(DATA, f)
    # print(json.dumps(DATA, indent=4))
    redirects = DATA['query'].get('redirects', {})
    red_dic = {}
    for i in redirects:
        red_dic[i['to']] = i['from']
    # return redirects
    pages = DATA['query']['pages']
    None_handle = {'first_iter': 0, 'wikibase_item': None}
    for v in pages.values():
        yesterday_view = next(iter(v.get('pageviews', None_handle).values()))
        if yesterday_view != None:
            out[red_dic.get(v['title'], v['title'])] = [v.get('pageprops', None_handle)['wikibase_item'],
                                                        yesterday_view]
        else:
            out[red_dic.get(v['title'], v['title'])] = [v.get('pageprops', None_handle)['wikibase_item'], 0]
                                                        
    # gpllimit max is already at 5000
    '''
    while 'continue' in DATA:
        PARAMS['pvipcontinue'] = DATA['continue']['pvipcontinue']
        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()
    pages = DATA['query']['pages']
    for v in pages.values():
        if v.get('pageviews', None_handle)[yesterday] != None:
            out[red_dic.get(v['title'], v['title'])] = [v.get('pageprops', None_handle)['wikibase_item'],
                                                        v.get('pageviews', None_handle)[yesterday]]
        else:
            out[red_dic.get(v['title'], v['title'])] = [v.get('pageprops', None_handle)['wikibase_item'], 0]
    '''
    return out

def get_links_withurl(SEARCHPAGE):
    
    S = requests.Session()
    PARAMS = {
        "action": "query",
        "generator": "search",
        "format": "json",
        "gsrsearch": SEARCHPAGE,
        "prop": "info",
        "inprop": "url",
        "gsrlimit": "max",
        "gsrnamespace": "0"
    }
    
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    return DATA
    out = {}
    for i in DATA['query']['pages']:
        out[DATA['query']['pages'][i]['title']] = DATA['query']['pages'][i]['fullurl']

def get_extract_image(SEARCHPAGE):
    S = requests.session()
    PARAMS = {
    	"action": "query",
    	"format": "json",
    	"prop": "extracts|pageimages",
    	"titles": SEARCHPAGE,
    	"exintro": 1,
    	"piprop": "original",
    }
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    out = {}
    # return DATA
    try:
        for i in DATA['query']['pages']:
            out['extract'] = DATA['query']['pages'][i]['extract']
            out['image'] = DATA['query']['pages'][i]['original']['source']
    except KeyError:
        out['image'] = '/static/graph/logo.webp'
    return out

def relations(src_node, dest_nodes_list):
    outer = []
    dest_len = len(dest_nodes_list) // 50
    for i in range(dest_len + 1):
        dest_part = dest_nodes_list[50*i: 50*(i+1)]
        S = requests.Session()
        dest_nodes = '|'.join(dest_part)

        PARAMS = {
            "action": "query",
            "format": "json",
            "titles": src_node,
            "prop": "links",
            "pltitles": dest_nodes,
            "pllimit": "max",
            "plnamespace": "0"
            }
        
        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()
        inner = []
        try:
            for i in DATA['query']['pages']:
                for j in DATA['query']['pages'][i]['links']:
                    inner.append([DATA['query']['pages'][i]['title'], j['title']])
        except KeyError:
            pass
        outer += inner
    return outer

def relations_v2(src_nodes_list, dest_nodes_list):
    final = {}
    dest_len = len(dest_nodes_list) // 50
    src_len = len(src_nodes_list) // 50
    for i in range(src_len + 1):
        src_part = src_nodes_list[50*i: 50*(i+1)]
        src_nodes = '|'.join(src_part)
        for j in range(dest_len + 1):
            dest_part = dest_nodes_list[50*j: 50*(j+1)]
            S = requests.Session()
            dest_nodes = '|'.join(dest_part)

            PARAMS = {
                "action": "query",
                "format": "json",
                "titles": src_nodes,
                "prop": "links",
                "pltitles": dest_nodes,
                "pllimit": "max",
                "plnamespace": "0"
                }
            
            R = S.get(url=URL, params=PARAMS)
            DATA = R.json()
            # with open('./testDump/test'+str(j)+'.json', 'w') as f:
            #     json.dump(DATA, f)
                
            # if 'batchcomplete' not in DATA: 
            pages = DATA['query']['pages']
            for i in pages:
                title = DATA['query']['pages'][i]['title']
                links = DATA['query']['pages'][i].get('links', False)
                if links:
                    for j in links:
                        try:
                            final[title].append(j['title'])
                        except KeyError:
                                final[title] = [j['title']]
    return final

def intra_relations(SEARCHPAGE):
    
    dest_nodes = [SEARCHPAGE] + get_links(SEARCHPAGE)
    out = {}
    # add the relations between links   
    for node in dest_nodes:
        for inner_node in relations(node, dest_nodes):
            try:
                out[inner_node[0]].append(inner_node[1])
            except KeyError:
                out[inner_node[0]] = [inner_node[1]]
    return out

def intra_relations_v2(SEARCHPAGE):
    
    dest_nodes = [SEARCHPAGE] + get_links(SEARCHPAGE)
    return relations_v2(dest_nodes, dest_nodes)


def intra_relations_dumb(SEARCHPAGE):
    
    dest_nodes = [SEARCHPAGE] + get_links(SEARCHPAGE)
    out = {}
    
    for node in dest_nodes:
        for inner_node in get_links(node):
            try:
                if inner_node in dest_nodes:
                    out[node].append(inner_node)
            except KeyError:
                out[node] = [inner_node]
    return out