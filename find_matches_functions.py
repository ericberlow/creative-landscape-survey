# -*- coding: utf-8 -*-
"""
Functions to process raw respondent data from new survey
Convert that to habits
Find top n best matches from 'archetypes' of original survey of 10K people.
Generate habit lists to see overlap with best cluster, unique habits, etc.
Clean habit naming for consisntency.

"""

import sys
sys.path.append("../CommonFunctions")
import pandas as pd
import pathlib as pl #path library
import params as param
pd.set_option('display.expand_frame_repr', False) # expand display of data columns if screen is wide

#

def process_archetypes(df_arch, df_clus):
    # convert archetype habit tags to list
    df_arch['habit_list'] = df_arch['Creative_Habits'].apply(lambda x: str(x).split("|"))
 
    # add to archetypes a list of top style habits for each style 
    df_top_habits = df_clus.groupby('Cluster_ID')['Creative_Habits'].apply(list).reset_index()
    df_top_habits.columns = ['Cluster_ID', 'Clus_Top_Habits']
    df_arch = df_arch.merge(df_top_habits, on='Cluster_ID')
    # get list of habits that are in reference dataset:  top cluster habits and arch habits (42)
    topHabits, archHabits = get_reference_habit_lists(df_arch, df_clus) 

    
    return df_arch, archHabits, topHabits


def get_score_thresholds(origCols, newCols):
    df = pd.read_excel("data/Archetypes_Network.xlsx" , sheet_name ='nodes', engine='openpyxl')
    # map each ordinal column to one of 3 threshold senarios
    # return dictionary of column by type
    threshDict = {}
    for col in origCols:
        if df[col].median() == 3:
            threshDict[col] = "mid" # low = 1,2, high = 4,5
        elif df[col].median() > 3:
            threshDict[col] = "high" # low = 1,2, high = 5
        elif df[col].median() < 3:
            threshDict[col] = "low" # low = 1 high = 4,5
    for col in newCols: 
        threshDict[col] = "mid" # low = 1,2, high = 4,5
    return threshDict        

def get_habits_from_scores_new(df, orig_ordCols, new_ordCols, habitDict):
    # convert responses to habits innew survey
    # ordinalCols = all columns in dataframe that are 1-5 scale
    # habitDict = dictionary mapping column name to enpoint habit tuple
    
    # get value thresholds for each ordinal column based on distribution in full dataset
    threshDict = get_score_thresholds(orig_ordCols, new_ordCols)
    
    # map score to habit endpoints for each ordinal column 
    # define places to put the results - a list of tag lists, one for each row in the dataset
    allTagLists = []  # includes tags from ordinal responses and biorhythm tag attribte

    for i in df.index:  # loop over rows in the dataframe
        if i %100 == 0: # print row number every 100 rows to show progress
            print("Processing row %d"%i)
        Tags = []    # build taglist for current row here
        row = df.loc[i] # get the row data
    
        ordCols = orig_ordCols + new_ordCols
        # loop over all ordinal row headers
        for col in ordCols:
            val = row[col]
            tg = None
            if threshDict[col] == "mid":
                if val == 1 or val == 2:
                    tg = habitDict[col][0]
                elif val == 5 or val == 4:
                    tg = habitDict[col][1]
                if tg != None:
                    Tags.append(tg)    
            elif threshDict[col] == "high":
                if val == 1 or val == 2:
                    tg = habitDict[col][0]
                elif val == 5:
                    tg = habitDict[col][1]
                if tg != None:
                    Tags.append(tg)    
            elif threshDict[col] == "low":
                if val == 1:
                    tg = habitDict[col][0]
                elif val == 5 or val == 4:
                    tg = habitDict[col][1]
                if tg != None:
                    Tags.append(tg)  
        # add biorhythm tag to current list
        val = row['Biorhythm']
        if isinstance(val, str) and len(val) > 0:    # make sure it's not empty
            if val == "Early Morning":
                Tags.append("Early Bird")
            elif val == "Late Night":
                Tags.append("Night Owl")
        # add creative process tag to current list
        val = row['Creative_Process']
        if isinstance(val, str) and len(val) > 0:    # make sure it's not empty
            if val == "Seeing the big picture & framing the problem":
                Tags.append("Problem Definer")
            elif val == "Generating lots of ideas or possible solutions":
                Tags.append("Ideator")
            elif val == "Picking the winning solutions from the options":
                Tags.append("Evaluator")
            elif val == "Executing & getting things done":
                Tags.append("Implementer") 

        allTagLists.append(Tags)    # combine taglists for each row
        

    return allTagLists # list of taglists for each row in the dataset

def get_habits_from_scores_orig(df, ordinalCols, habitDict):
    # convert responses into habits from original survey
    # ordinalCols = all columns in dataframe that are 1-5 scale
    # habitDict = dictionary mapping column name to enpoint habit tuple
    
    # get value thresholds for each ordinal column based on response distribution
    newCols = []
    threshDict = get_score_thresholds(ordinalCols,newCols)
    
    # map score to habit endpoints for each ordinal column 
    # define places to put the results - a list of tag lists, one for each row in the dataset
    allTagLists = []  # includes tags from ordinal responses and biorhythm tag attribte

    for i in df.index:  # loop over rows in the dataframe
        if i %100 == 0: # print row number every 100 rows to show progress
            print("Processing row %d"%i)
        Tags = []    # build taglist for current row here
        row = df.loc[i] # get the row data
    
        # loop over all ordinal row headers
        for col in threshDict:
            val = row[col]
            tg = None
            if threshDict[col] == "mid":
                if val == 1 or val == 2:
                    tg = habitDict[col][0]
                elif val == 5 or val == 4:
                    tg = habitDict[col][1]
                if tg != None:
                    Tags.append(tg)    
            elif threshDict[col] == "high":
                if val == 1 or val == 2:
                    tg = habitDict[col][0]
                elif val == 5:
                    tg = habitDict[col][1]
                if tg != None:
                    Tags.append(tg)    
            elif threshDict[col] == "low":
                if val == 1:
                    tg = habitDict[col][0]
                elif val == 5 or val == 4:
                    tg = habitDict[col][1]
                if tg != None:
                    Tags.append(tg)  
        # add biorhythm tag to current list
        val = row['Creative_Habits']
        if isinstance(val, str) and len(val) > 0:    # make sure it's not empty
            for biorhythm in ["Early Bird", "Night Owl"]:
                if biorhythm in val:
                    Tags.append(biorhythm)

        allTagLists.append(Tags)    # combine taglists for each row

    return allTagLists # list of taglists for each row in the dataset

def get_similarity(habits1, habits2, metric='jaccard'): # other metrics: 'sorensen', 'frac_1_in_2'
    # compare two lists of habits 
    habit1_set = set(habits1)
    habit2_set = set(habits2) # reference habits
    # jaccard is intersection over union
    jaccard = float(len(habit1_set.intersection(habit2_set)))/len(habit1_set.union(habit2_set))
    # sorensen is the average fraction overlap or 2* intersection / sum of elements in each
    sorensen = (2*float(len(habit1_set.intersection(habit2_set))))/(len(habit1_set) + len(habit2_set))
    # asymmetric fraction of habits in set 1 tht are in set 2
    frac_1in2 = float(len(habit1_set.intersection(habit2_set)))/len(habit1_set)

    # check: conversipn of jaccard to sorensen
    # sorensen = (2*jaccard)/(1+jaccard) 

    if metric == 'jaccard':
        sim = jaccard
    elif metric == 'sorensen':
        sim = sorensen
    elif metric == 'frac_1_in_2':
        sim = frac_1in2
    else:
        print('no metric specified')
    return sim

       
def find_top_n_matches(row, df_ref, rowCols, topN = 5, sortby=['top_habits_sim', 'habits_sim']):
    '''
    Decription: each signle respondent (row), find the top n most similar people in the reference database.
    Add cluster traits of each best matches to the focal respondent
    ----------
    row : focal individual's results to be matched
    df_ref : reference database (e.g. archetype network)
    rowCols : columns of respondent data to keep in final top matches dataframe
    topN : number of top matches to keep 
    sortby: list of 2 attributes to sort in descending order for gettin top n matches 
    ----------    
    Returns: a dataframe of topN matches and the target respondent data  (n rows)
    '''
    
    target_habits = row['Habits_Orig'].split("|") # respondent subset of habits that are among the 42 total of the original survey
    target_top_habits = row['Top_Habits'].split("|") # respondent subset of habits that are among the 36 top cluster habits
    
    
    # get sim in habits between each reference person and the target person   
    df_ref['habits_sim'] = df_ref['habit_list'].apply(lambda x: get_similarity(target_habits,x, metric='sorensen'))
     # get sim in cluster top habits between each reference person and the target person  
    df_ref['top_habits_sim'] = df_ref['Clus_Top_Habits'].apply(lambda x: get_similarity(target_top_habits,x, metric='sorensen'))
    # get fraction of cluster top habits that are present in target responednt
    df_ref['frac_top_habits'] = df_ref['Clus_Top_Habits'].apply(lambda x: get_similarity(x, target_habits, metric='frac_1_in_2'))
    #sort by most similar to target person - using chosen sortBy metric 
    df_ref.sort_values(sortby, ascending=[False,False], inplace=True)
    # convert cluster top habits list to string for later grouping
    #df_ref['Clus_Top_Habits'] = df_ref['Clus_Top_Habits'].apply(lambda x: "|".join(str(x)))
    df_ref = df_ref[['id','Creative_Habits', 'Cluster_ID', 'Creative_Style', 'Clus_Top_Habits', 
                     'habits_sim','top_habits_sim', 'frac_top_habits', 'x_tsne', 'y_tsne']]
    df_ref.columns = ['id_match','Habits_match', 'Cluster_ID_match', 'Creative_Style_match', 'Clus_Top_Habits_match', 
                      'habits_sim','top_habits_sim', 'frac_top_habits', 'x_tsne', 'y_tsne']
    
    # get topN rows of most similar archetypes to target respondent
    df_top_matches = df_ref.head(topN).reset_index(drop=True) 
    # add respondent data to top matches
    for col in rowCols:
        df_top_matches[col] = row[col]
    
    return df_top_matches # datafrme of target respondent with top n matches (n rows)
    

def get_best_match(df_topMatches, groupVars):
    ## aggregate and summarize  results of top N matches
    ## groupVars = grouping attributes (including ones to keep in final dataset)
    
    # build aggregation functions
    agg_data = {'id_match': 'count'} # get count of each matched cluster 
    agg_data.update({col: 'max' for col in ['habits_sim', 'top_habits_sim', 'frac_top_habits']}) # get max similarities of each cluster
    agg_data.update({col: 'mean' for col in ['x_tsne', 'y_tsne']}) # get cetroid of top matches by cluster
    # group and smmarize
    df_top_match_count = df_topMatches.groupby(groupVars).agg(agg_data).reset_index() 
    df_top_match_count.rename(columns = {'id_match': 'count'}, inplace=True) 
    
    # now get match with highest cluster count or if tied highest similarity
    df_top_match_count.sort_values(['id', 'count', 'top_habits_sim'], ascending=[True, False, False], inplace=True)
    df_best_match =  df_top_match_count.groupby(['id', 'Name']).first().reset_index()

    return df_best_match

    
def get_reference_habit_lists(archdf, clusdf):
    # get list of unique habits in cluster top habits (36 habits)
    topHabits = list(clusdf.Creative_Habits.unique())
    # get list of unique habits in the archetype datasset (42 habits)
    archdf['habit_list'] = archdf['Creative_Habits'].apply(lambda x: str(x).split("|"))
    archHabits = list(set(archdf['habit_list'].agg(sum)))
    return topHabits, archHabits
    

def add_habit_lists_counts(df, archHabits, topHabits):
    '''
    get lists of all habits, original survey habits, and habits in the set of top cluster habits
    archHabits = full list of habits in the archetype dataset (42 total habits),
    topHabits = full list of habits that are included in top habits for each cluster (36 total habits)
    '''
    # trim habit list to those that were in original survey
    df['habits_orig'] = df['habits_all'].apply(lambda x: [h for h in x if h in archHabits])
    # get list of habits that are among the top habits of the clusters
    df['top_habits'] = df['habits_all'].apply(lambda x: [h for h in x if h in topHabits])
        # check - compare new habit list to ones in archetype list
    df['n_habits_all'] = df['habits_all'].apply(lambda x: len(x)) #habits from all survey response
    df['n_habits_orig'] = df['habits_orig'].apply(lambda x: len(x)) # habits from original survey
    
    # convert habit lists to pipe-seprated strings
    df['Habits_All'] = df['habits_all'].apply(lambda x: "|".join(x))
    df['Habits_Orig'] = df['habits_orig'].apply(lambda x: "|".join(x))
    df['Top_Habits'] = df['top_habits'].apply(lambda x: "|".join(x))
    return df
 
def add_rare_breed (df, mintags):
    df['Cluster_ID_match'] = df.apply(lambda x: "Rare Breed" if x['n_habits_orig'] <= mintags else x['Cluster_ID_match'], axis=1)
    df['Clus_Top_Habits_match'] = df.apply(lambda x: ["Rare Breed"] if x['n_habits_orig'] <= mintags else x['Clus_Top_Habits_match'], axis=1)
    df['Habits_TopClus_overlap'] = df.apply(lambda x: ['Rare Breed'] if x['n_habits_orig'] <= mintags else x['Habits_TopClus_overlap'], axis=1)
    df['Top_Habits'] = df.apply(lambda x: ['Rare Breed'] if x['n_habits_orig'] <= mintags else x['Top_Habits'], axis=1)
    df['Habits_Orig_unique'] = df.apply(lambda x: x['Habits_Orig'] if x['n_habits_orig'] <= mintags else x['Habits_Orig_unique'], axis=1)
    df['Habits_All_unique'] = df.apply(lambda x: x['Habits_All'] if x['n_habits_orig'] <= mintags else x['Habits_All_unique'], axis=1)
    
    df['x_tsne'] = df.apply(lambda x: 0 if x['n_habits_orig'] <= mintags else x['x_tsne'], axis=1)
    df['y_tsne'] = df.apply(lambda x: 0 if x['n_habits_orig'] <= mintags else x['y_tsne'], axis=1)
    df['n_clus_overlap'] =  df.apply(lambda x: 0 if x['n_habits_orig'] <= mintags else x['n_clus_overlap'], axis=1)
    df['n_orig_unique'] = df.apply(lambda x: x['n_habits_orig'] if x['n_habits_orig'] <= mintags else x['n_orig_unique'], axis=1)
    df['n_all_unique'] = df.apply(lambda x: x['n_habits_all'] if x['n_habits_orig'] <= mintags else x['n_all_unique'], axis=1)

def rename_habits(x, habitDict = param.habit_renameDict):
    '''
    x is a list of habits
    Rename habit tags from a renaming dictionary 
    If the habit is not in the dictionary, keep the old one
    Returns a new list of renamed habits
    '''
    newhabits = []
    for habit in x:
        if habit in habitDict:
            newhabits.append(habitDict[habit])
        else:
            newhabits.append(habit)
    return newhabits
       

################################################################

