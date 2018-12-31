# -*- coding: utf-8 -*-
"""
fpl_analytics._fpl_data

This contains all utils for fpl data io
"""

import requests
import json
from os.path import join


root_url = 'https://fantasy.premierleague.com'
static_url_ext = '/drf/bootstrap-static'
summary_url_ext = '/drf/element-summary/'

def fetch_data_url():
    """
    fetching fpl data from the official fantasy pl source
    
    2 type of data - 
    one more static from bookstrap-static
    another one is more dynamic data is from element-summary
    
    output is a joint dictionary
    """
    fpl_data = requests.get(root_url+static_url_ext).json()
    for i, player in enumerate(fpl_data['elements']):
        fpl_data['elements'][i]['history'] = requests.get(
                                                    root_url+
                                                    summary_url_ext+
                                                    str(player['id'])).json()
    return fpl_data    
 
def _json_name(sid):
    """
    internal func to define the json file name
    
    """
    return "fpl_week_{}.json".format(sid)

def save_fpl(fpl_data, loc=None, sid=None):
    """
    save fpl_data into a file
    
    fpl_data - dict
    loc - folder to save the json file
    sid - in (as of which week data)
    """
    if sid is None:
        sid = fpl_data["current-event"] + 1
    
    name = _json_name(sid) if loc is None else join(loc, _json_name(sid))
    print("saving to {}".format(name))
    
    with open(name, 'w') as f:
        json.dump(fpl_data, f)
        
def load_fpl(sid, loc=None):
    """
    load fp_data from a file,
    sid is int - as of which week data
    
    """
    name = _json_name(sid) if loc is None else join(loc, _json_name(sid))
    print("loading from {}".format(name))
    
    with open(name, 'r') as f:
        json1_str = f.read()
        fpl_data = json.loads(json1_str)    
        
    return fpl_data    
