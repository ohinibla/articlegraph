# -*- coding: utf-8 -*-

from .scrap_wikipedia import *
from .models import Site, Link

def run(site_obj, site_scraper_obj):
    for link in site_scraper_obj.get_links_info():
        l_title = link[0]
        l_site = site_obj
        l_address = link[1]
        l, created = Link.objects.get_or_create(title=l_title, site=l_site, address=l_address)
        l.save()