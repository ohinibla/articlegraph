# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 09:58:03 2021

@author: B
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

class Scraper(object):
    def __init__(self, url):
        self.url = url
        self.base_url = self.url[: self.url.find('.org/') + 4]
        self.page = urlopen(url).read()
        self.soup = BeautifulSoup(self.page, 'html.parser')
    
    def get_title(self):
        return re.sub(' - Wikipedia', '', self.soup.title.text)
    
    def get_title_image(self):
        try:
            return 'https:' + self.soup.find_all('img', class_='thumbimage')[0]['src']
        except IndexError:
            return 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/800px-Wikipedia-logo-v2.svg.png'
            
class Site_info(Scraper):
    def __init__(self, url):
        Scraper.__init__(self, url)
        self.result = self.soup.find_all('div', 'mw-parser-output')
        self.paragraphs = self.result[0].find_all('p')
        
    def get_synopsis(self):
        for para in self.paragraphs:
            try:
                if 'mw-empty-elt' not in para['class']:
                    return para
            except KeyError:
                return para
        
    def get_synopsis_text(self):
        return re.sub('\[[\d]+\]', '', self.get_synopsis().text)
    
    def get_links(self):
        links = []
        for para in self.paragraphs:
            for link in para.find_all('a'):
                if (link != [] and not re.findall('\[[\d]+\]', link.text)):
                    links.append(link)
        return links, len(links)
    
    def get_links_info(self):
        links_info = []
        for link in self.get_links()[0]:
            if link['href'][0] == '/':
                links_info.append((link.text, self.base_url + link['href']))
            else:
                links_info.append((link.text, link['href']))
        return links_info
           
        