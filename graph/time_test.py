# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 10:45:54 2021

@author: B
"""

import time

from alchemy import *

start = time.time()
IntraGraphJSON('babak')
end = time.time()
print('IntraGraphJSON', end - start)

start = time.time()
IntraGraphJSON_v2('babak')
end = time.time()
print('IntraGraphJSON', end - start)