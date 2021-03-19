# -*- coding: utf-8 -*-
"""
Find creative species of website team  - 
using new survey results and matching to archetypes from original survey

"""

import sys
sys.path.append("../CommonFunctions")
import pandas as pd
import pathlib as pl #path library
import find_matches_functions as fm
pd.set_option('display.expand_frame_repr', False) # expand display of data columns if screen is wide
import params as param

# paths
wd = pl.Path.cwd()
datapath = wd/"data"
resultspath = wd/"results"


def get_topN_matches(df, df_arch, keepCols, resultspath, topN=10, sortby=['top_habits_sim','habits_sim'], write=False):
    '''
    # loop thru dataframe of new respondents, find topN  most similar archetype and their cluster and position
    df : dataframe of new survey respondents
    df_arch : dataframe of reference population (cluster archetypes from origional survey)
    keepCols : columns to keep in processed results 
    topN : number of top matches to find. The default is 10.
    sortby : strategy for finding best match - default is- first  find best overlap with top cluster habits, then find most similar individual within

    Returns - dataframe with topN matches, their clusters 

    '''
   
    respondents = []    # list of dataframes for each respondent
    for i in df.index:  # loop over rows in the dataframe
        if i %10 == 0: # print row number every 10 rows to show progress
            print("Processing row %d"%i)
        row = df.loc[i] # get the data for the individual respondent
        df_top_matches = fm.find_top_n_matches(row, df_arch, keepCols, topN =topN, sortby=sortby)
        respondents.append(df_top_matches) 
    # combine top matches for all respondents into one dataframe
    df_top_n_matches = pd.concat(respondents) 
    df_top_n_matches['Clus_Top_Habits_match'] = df_top_n_matches.Clus_Top_Habits_match.apply(lambda x: "|".join(x)) # convert list to string for grouping
    
    if write:
        # write file of all matches for each sortyby strategy run
        df_top_n_matches.to_csv(resultspath/('team_top_n_matches_' + str(sortby) + '.csv'), index=False)
    return df_top_n_matches
       

def process_topN_matches(df_top_n_matches, df_survey_responses, topN, sortby, resultspath, write=True):
    '''
    Aggregate results of top N matches to get single best match and x, y position
    Add final listls of unique habits and overlap of habits with final cluster
    Add back raw survey results
    Clean and rename columns
    Add Rare Breed if not enough responses
    Clean and rename habits
    
    df_top_n_matches : top N matches in the reference database for each respondent
    df_survey_responses : oritginal raw responses

    Returns final dataframe of best match and metadata for each respondent
    '''

    ## aggregate and summarize > get single best match
    groupVars = ['id', 'Habits_All','Habits_Orig','Top_Habits','n_habits_all', 'n_habits_orig', 'Cluster_ID_match', 'Clus_Top_Habits_match']
    df_best_match = fm.get_best_match(df_top_n_matches, groupVars)
    
    # convert habits to list
    habit_attrs = ['Habits_All','Habits_Orig','Top_Habits', 'Clus_Top_Habits_match']
    for attr in habit_attrs:
        df_best_match[attr] =  df_best_match[attr].apply(lambda x: x.split("|")) 
        
    # add list of unique (original) habits not in top cluster habits                               
    df_best_match['Habits_Orig_unique'] = df_best_match.apply(lambda x: list(set(x['Habits_Orig']).difference(set(x['Clus_Top_Habits_match']))), axis=1)
    df_best_match['Habits_All_unique'] = df_best_match.apply(lambda x: list(set(x['Habits_All']).difference(set(x['Clus_Top_Habits_match']))), axis=1)
    df_best_match['Habits_TopClus_overlap'] = df_best_match.apply(lambda x: list(set(x['Habits_Orig']).intersection(set(x['Clus_Top_Habits_match']))), axis=1)
    df_best_match['n_orig_unique'] = df_best_match['Habits_Orig_unique'].apply(lambda x: len(x)) 
    df_best_match['n_all_unique'] = df_best_match['Habits_All_unique'].apply(lambda x: len(x)) 
    df_best_match['n_clus_overlap'] = df_best_match['Habits_TopClus_overlap'].apply(lambda x: len(x)) 
    df_best_match['sortby_strategy'] = str(sortby)
    df_best_match['frac_top_'+str(topN)] = df_best_match['count']/float(topN)
    
    # clean columns
    finalCols = ['id', 'Habits_All', 'Habits_Orig', 'Top_Habits', 'n_habits_all', 'n_habits_orig',
                 'Cluster_ID_match', 'Clus_Top_Habits_match','frac_top_habits', #'top_habits_sim','habits_sim',
                 'Habits_All_unique','Habits_Orig_unique', 'Habits_TopClus_overlap', 
                 'n_orig_unique', 'n_all_unique', 'n_clus_overlap','x_tsne', 'y_tsne']#  , 'sortby_strategy',  'count', 'frac_top_'+str(topN) ] 

    # add raw survey responses back to the processed results
    df_best_match = df_best_match[finalCols]
    df_best_match = df_best_match.merge(df_survey_responses, on='id')
    
    # add Rare Breed if 3 or fewer original survey habits
    fm.add_rare_breed(df_best_match, 3)
        
    # rename columns
    df_best_match.rename(columns = {'frac_top_habits': 'Cluster_Affinity',
                                      'x_tsne': 'x',
                                      'y_tsne': 'y'}, inplace=True)
    df_best_match.rename(columns = param.ordCol_renameDict, inplace=True) 
    
    # rename habits in habit lists
    habitCols = ['Habits_All', 'Habits_Orig', 'Top_Habits','Clus_Top_Habits_match','Habits_Orig_unique', 'Habits_All_unique','Habits_TopClus_overlap']
    for col in habitCols:
        df_best_match[col] = df_best_match[col].apply(lambda x: fm.rename_habits(x))
        
    if write:
        # write results file
        df_best_match.to_csv(resultspath/("best_match.csv"), index=False)
    
    return df_best_match

################################################################
def process_respondent(df):
    '''
    df - team survey results
    '''
    df_arch, archHabits, topHabits, topN, sortBy = prepare_data()

    # rename noew response columns 
    df.rename(columns = param.newCol_renameDict, inplace=True)
    
    # for new respndents, convert ordinal scores to list of habits
    df['habits_all'] = fm.get_habits_from_scores_new(df,  param.orig_OrdCols, param.new_OrdCols, param.habitDict)
    # add lists of original habits, top clus habits, and habit counts for each person.
    df = fm.add_habit_lists_counts(df, archHabits, topHabits)
    
    # clean columns
    raw_response_cols = param.orig_OrdCols + param.new_OrdCols + param.new_CatCols
    keepCols = ['id','Habits_All', 'Habits_Orig', 'Top_Habits','n_habits_all', 'n_habits_orig'] + raw_response_cols
    df = df[keepCols] 
    
    # get separate df of raw responses to add back 
    responseCols = param.orig_OrdCols + param.new_OrdCols + param.new_CatCols
    df_survey_responses = df[['id']+responseCols]

    
    ##### find top N matches
    df_top_n_matches = get_topN_matches(df, df_arch, keepCols, resultspath, topN, sortBy, write=False)
    
    ######  find best matches for each respondent ##### 
    df_best_match = process_topN_matches(df_top_n_matches, df_survey_responses,topN, sortBy, resultspath, write=True)
    return df_best_match

################################################################
# methods for API
def process_single_respondent(respondent_data):
    items = respondent_data.items()
    data = dict()
    for k, v in items:
        data[k] = [v]
    frame = pd.DataFrame(data)
    res_data = process_respondent(frame)
    res_dict = res_data.to_dict()

    result = dict()
    for k, v in res_dict.items():
        result[k] = v[0]

    return result

def prepare_data():
    wd = pl.Path.cwd()
    datapath = wd/"data"
    
    # file names
    archnw = datapath/"Archetypes_Network.xlsx"
    top_habits = datapath/"Cluster_Top_Habits.xlsx"
    
    # params
    topN = 10 # number of top matches to find              
    sortby= ['top_habits_sim','habits_sim'] # first find cluster with highest average overlap in top habits, then pick most similar person within
               
    print ('reading files')
    df_arch = pd.read_excel(archnw, sheet_name ='nodes', engine='openpyxl')
    df_arch.drop(['Discipline'], axis=1, inplace=True )
    df_clus = pd.read_excel(top_habits, engine='openpyxl')

    # add habit list and top cluster habit list to archetypes
    df_arch, archHabits, topHabits = fm.process_archetypes(df_arch, df_clus)
    return df_arch, archHabits, topHabits, topN, sortby
    
if __name__ == '__main__':
    # file names
    team = datapath/"Test_Survey_Responses.xlsx"   
    
    process_respondent(pd.read_excel(team, engine='openpyxl'))