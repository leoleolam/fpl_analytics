# -*- coding: utf-8 -*-
"""
fpl_analytics._fpl_data

This contains all utils for fpl data analyzer
"""
from . _fpl_process import score_detail, opp_next_map

def filter_score_min_play(ts, minutes=10):
    """
    only mask those play no less than the minutes inputed
    """
    return ts[[l for l in list(ts.index) if l[-1]>minutes]]

def scoring_to_mean(ts):
    """
    provide mean of scoring to info
    """
    return ts.groupby(level=["team", "pos"]).mean().unstack()
    
def scoring_to_max(ts):
    """
    provide max of scoring to info
    """
    return ts.groupby(level=["team", "pos"]).max().unstack()

def scoring_from_mean(ts):
    """
    provide mean of scoring from info
    """
    return ts.groupby(level=["opp", "pos"]).mean().unstack()
    
def scoring_from_max(ts):
    """
    provide max of scoring from info
    """
    return ts.groupby(level=["opp", "pos"]).max().unstack()

def mean_plot(fpl_data, minutes=5):
    """
    plot a mean grap
    and return dataframe data
    """
    dd=score_detail(fpl_data)
    dd=filter_score_min_play(dd, 5)
    df=(scoring_to_mean(dd)/2 +scoring_from_mean(dd).rename(
            index=opp_next_map(fpl_data))/2)
    ax=df.plot()
    ax.set_xticks(range(20))
    ax.set_xticklabels(scoring_to_mean(dd).index, rotation=90)
    return df

def max_plot(fpl_data, minutes=5):
    """
    plot a max grap
    and return dataframe data
    """    
    dd=score_detail(fpl_data)
    dd=filter_score_min_play(dd, 5)
    df=(scoring_to_max(dd)/2 +scoring_from_max(dd).rename(
            index=opp_next_map(fpl_data))/2)
    ax=df.plot()
    ax.set_xticks(range(20))
    ax.set_xticklabels(scoring_to_mean(dd).index, rotation=90)
    return df