#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 12:43:37 2020

@author: NickBrown
"""

# ncaa import assignment
import numpy as np
import pandas as pd

def ncaaimport(a):
    # reading in data
    a = str(a)
    url = "http://homepages.cae.wisc.edu/~dwilson/rsfc/history/howell/cf"+a+"gms.txt"
    df = pd.read_fwf(url, [(0,10), (11,38), (39,41), (42,70), (71,73),(74,92)], header = None, names = ["date", "awayteam", "awayscore", "hometeam", "homescore", "location"])
    
    # grouping data by away team, and putting it into a data frame
    away_df = df.groupby("awayteam").size()
    away_df = pd.DataFrame(away_df)
    away_df.reset_index(level=0, inplace = True)
    away_df = away_df.rename(columns={"awayteam": "team", 0 : "awaygames"})
    
    # grouping data by home team, and putting it into a data frame
    home_df = df.groupby("hometeam").size()
    home_df = pd.DataFrame(home_df)
    home_df.reset_index(level=0, inplace = True)
    home_df = home_df.rename(columns = {"hometeam": "team", 0: "homegames"})
    
    # merging the two data frames on team, and getting a total df
    totalgames_df = pd.merge(away_df, home_df, how="outer")
    totalgames_df["awaygames"] = totalgames_df["awaygames"].fillna(0)
    totalgames_df["homegames"] = totalgames_df["homegames"].fillna(0)
    totalgames_df["total_games"] = totalgames_df.awaygames + totalgames_df.homegames
    # removing teams with less than 6 games, also getting list of teams to remove 
    totalgames_df = totalgames_df[totalgames_df.total_games > 5]
    df_1 = df[df.awayteam.isin(totalgames_df.team) & df.hometeam.isin(totalgames_df.team)]
    
    # finding ties and removing ties in new dataframe 
    df_2 = df_1[df_1.awayscore != df_1.homescore]
    
    # getting new total games df, accounting for the removal of D-2 teams and ties
    away_df2 = df_2.groupby("awayteam").size()
    away_df2 = pd.DataFrame(away_df2)
    away_df2.reset_index(level=0, inplace = True)
    away_df2 = away_df2.rename(columns={"awayteam": "team", 0 : "awaygames"})
    
    # grouping data by home team, and putting it into a data frame
    home_df2 = df_2.groupby("hometeam").size()
    home_df2 = pd.DataFrame(home_df2)
    home_df2.reset_index(level=0, inplace = True)
    home_df2 = home_df2.rename(columns = {"hometeam": "team", 0: "homegames"})
    
    # merging the two data frames on team, and getting a total df
    totalgames_df2 = pd.merge(away_df2, home_df2, how="outer")
    totalgames_df2["awaygames"] = totalgames_df2["awaygames"].fillna(0)
    totalgames_df2["homegames"] = totalgames_df2["homegames"].fillna(0)
    totalgames_df2["total_games"] = totalgames_df2.awaygames + totalgames_df2.homegames
    
    
    
    df_2['awaywin'] = df_2.awayteam[df_2.awayscore > df_2.homescore]
    df_2['homewin'] = df_2.hometeam[df_2.homescore > df_2.awayscore]
    df_2.reset_index(level=0, inplace = True)
    
    
    # A dataframe of wins by the away team
    awaywins_df = df_2.groupby("awaywin").size()
    awaywins_df = pd.DataFrame(awaywins_df)
    awaywins_df.reset_index(level=0, inplace = True)
    awaywins_df = awaywins_df.rename(columns={"awaywin": "team", 0 : "awaywin"})
    
    # a dataframe of wins by the home team
    homewins_df = df_2.groupby("homewin").size()
    homewins_df = pd.DataFrame(homewins_df)
    homewins_df.reset_index(level=0, inplace = True)
    homewins_df = homewins_df.rename(columns = {"homewin": "team", 0: "homewin"})
    
    # combining those two data frames
    totalwins_df = pd.merge(awaywins_df, homewins_df, how="outer")
    totalwins_df = totalwins_df.fillna(0)
    totalwins_df["total_wins"] = totalwins_df.awaywin + totalwins_df.homewin
    
    # merge the new total games and wins data frames
    final_df = pd.merge(totalgames_df2, totalwins_df, how="outer")
    final_df = final_df.drop(columns=(["awaygames", "homegames","awaywin","homewin"]))
    final_df = final_df.fillna(0)
    # calculate losses by subtracting the total games by wins
    final_df['losses'] = final_df.total_games - final_df.total_wins
    final_df = final_df.drop(columns=("total_games"))
    final_df = final_df.rename(columns=({"total_wins": "wins"}))
    
    # Getting Index Values for home and away teams instead
    s = pd.Series(final_df.team.index, index = final_df.team)
    t = pd.Series(final_df.team)
    df_2['hometeam'] = df_2.hometeam.map(s)
    df_2['awayteam'] = df_2.awayteam.map(s)
    
    # away teams opponents
    away_opp = df_2.groupby("awayteam").agg({"hometeam": list})
    away_opp = pd.DataFrame(away_opp)
    away_opp.reset_index(level=0, inplace = True)
    away_opp = away_opp.rename(columns = {"awayteam": "team", "hometeam": "home_opponent"})
    
    
    # home team opponents
    home_opp = df_2.groupby("hometeam").agg({"awayteam": list})
    home_opp = pd.DataFrame(home_opp)
    home_opp.reset_index(level=0, inplace = True)
    home_opp = home_opp.rename(columns = {"hometeam": "team", "awayteam": "away_opponent"})
    
    # merging home and away team opponent data frames, then concatenating the lists
    opponents_col = pd.merge(away_opp, home_opp, on = "team")
    opponents_col["opponents"] = opponents_col.home_opponent + opponents_col.away_opponent
    opponents_col = opponents_col.drop(columns = (["home_opponent", "away_opponent"]))
    # changing numerical values back to team names for team column before merge
    opponents_col['team'] = opponents_col.team.map(t)
    
    # merging with final df
    final_df = pd.merge(final_df, opponents_col, on = "team")
    
    
    return final_df 




