 # -*- coding: utf-8 -*-
"""
fpl_analytics._fpl_data

This contains all utils for fpl data process
"""

import pandas as pd

       
def get_player_id(fpl_data, name):
    """
    get player id from the first, second or web name
    """
    return {i:fpl_data["elements"][i]["first_name"]+
               fpl_data["elements"][i]["second_name"]
                   for i in range(len(fpl_data["elements"])) 
        if (fpl_data["elements"][i]["first_name"].upper()== name.upper() or
            fpl_data["elements"][i]["second_name"].upper()== name.upper() or
            fpl_data["elements"][i]["web_name"].upper()== name.upper())}
        
     
def team_map(fpl_data):
    """
    team mapping
    """
    return {team["id"]: team["name"] for team in fpl_data["teams"]}        

def pos_map(fpl_data):
    """
    positon mapping
    """
    return {team["id"]: team["singular_name"] 
                for team in fpl_data["element_types"]}  
        
def get_performance(fpl_data, pid):
    """
    get player performance (by player id) from fpl_data 
    """
    return fpl_data["elements"][pid]["history"]["history_summary"]

def opp_next_map(fpl_data):
    """
    get next opponent map
    """
    res = {}
    m = team_map(fpl_data)
    for d in fpl_data['next_event_fixtures']:
        res[m[d["team_a"]]] = m[d["team_h"]]
        res[m[d["team_h"]]] = m[d["team_a"]]
    return res

def achived_from(fpl_data, pid, minutes=False):
    """
    achieved points from fpl_data,
    
    fpl_data - dict
    pid - int
    minutes - True/False, 
        whether to include minutes in the output series index
    
    """
    p = fpl_data["elements"][pid]["history"]["history_summary"]
    m=team_map(fpl_data)
    if minutes:
        return pd.Series({(m[pp["opponent_team"]], 
                           pp["minutes"]):pp["total_points"] 
                        for pp in p}).sort_index()
    else:
        return pd.Series({m[pp["opponent_team"]]:pp["total_points"] 
                        for pp in p}).sort_index()
            
def score_detail(fpl_data):
    """
    convert fpl_data into Series
    Index- multi-index of team, pos, player, opp, minutes
    """
    l =[]
    basic_index = ["player", "opp", "minutes"]
    for i in range(len(fpl_data["elements"])):
        ts=achived_from(fpl_data, i, True)
        name = (fpl_data["elements"][i]["first_name"]+
               fpl_data["elements"][i]["second_name"])

        if len(ts)==0:
            continue
        ts=pd.concat([ts,], keys=[name], names=basic_index)
        ele = pos_map(fpl_data)[fpl_data["elements"][i]['element_type']]
        ts=pd.concat([ts,], keys=[ele], names=["pos"]+basic_index)
        team = team_map(fpl_data)[fpl_data["elements"][i]['team']]
        ts=pd.concat([ts,], keys=[team], names=["team", "pos"]+basic_index)
        l.append(ts)
    return pd.concat(l)
    