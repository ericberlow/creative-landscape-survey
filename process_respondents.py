# -*- coding: utf-8 -*-
"""
Find creative species of HC team - 
using new survey results and matching to archetypes from original survey
"""

import sys
sys.path.append("../CommonFunctions")
import pandas as pd
import pathlib as pl #path library
import find_creative_style as cs
pd.set_option('display.expand_frame_repr', False) # expand display of data columns if screen is wide
import params as param

    

################################################################

if __name__ == '__main__':
    # paths
    wd = pl.Path.cwd()
    datapath = wd/"data"
    resultspath = wd/"results"

    
    # file names
    archnw = datapath/"Archetypes_Network.xlsx"
    styles = datapath/"CreativeStyles_Tag_Summary.xlsx"
    team = datapath/"Team_Survey_Responses.xlsx"   
    
    # params
    topN = 10 # number of top matches to find              
    sortbylist = [
                  #['habits_sim', 'frac_top_habits'], # first find people with most similar (original) habits, if tie pick cluster with most overlap
                  ['top_habits_sim','habits_sim'], # first find cluster with highest average overlap in top habits, then pick most similar person within
                  #['frac_top_habits','habits_sim'] # first find cluster with highest fraction of top habits shared by respondent, then find most similar person within.
                  ]
               
    print ('reading files')
    df_arch = pd.read_excel(archnw, sheet_name ='nodes', engine='openpyxl')
    df_arch.drop(['Gender', 'Discipline', 'Creative Advice'], axis=1, inplace=True )
    df_clus = pd.read_excel(styles, engine='openpyxl')
    df =  pd.read_excel(team, engine='openpyxl') # team survey results

    # add habit list and top cluster habit list to archetypes
    df_arch, archHabits, topHabits = cs.process_archetypes(df_arch, df_clus)
    
    # rename team response columns 
    df.rename(columns = param.newCol_renameDict, inplace=True)

    
    # for new respndents, convert ordinal scores to list of habits
    df['habits_all'] = cs.get_habits_from_scores_new(df,  param.orig_OrdCols, param.new_OrdCols, param.habitDict)
    # add lists of original habits, top clus habits, and habit counts for each person.
    df = cs.add_habit_lists_counts(df, archHabits, topHabits)
    
    # clean columns
    raw_response_cols = param.orig_OrdCols + param.new_OrdCols + param.new_CatCols
    keepCols = ['id','Name', 'Habits_All', 'Habits_Orig', 'Top_Habits','n_habits_all', 'n_habits_orig'] + raw_response_cols
    df = df[keepCols] 
    
    # get separate df of raw responses to add back 
    responseCols = param.orig_OrdCols + param.new_OrdCols + param.new_CatCols
    df_survey_responses = df[['id']+responseCols]
    
    
    ######  find best matches for each respondent ##### 
 
    # get results for each or each search strategy 
    runs = [] # list of dataframes for each run
    for sortby in sortbylist:
        # for each respondent , find topN  most similar archetype
        respondents = []    # list of dataframes for each respondent
        for i in df.index:  # loop over rows in the dataframe
            if i %100 == 0: # print row number every 100 rows to show progress
                print("Processing row %d"%i)
            row = df.loc[i] # get the data for the individual respondent
            df_top_matches = cs.find_top_n_matches(row, df_arch, keepCols, topN =topN, sortby=sortby)
            respondents.append(df_top_matches) 
        # combine top matches for all respondents into one dataframe
        df_top_n_matches = pd.concat(respondents) 
        df_top_n_matches['Clus_Top_Habits_match'] = df_top_n_matches.Clus_Top_Habits_match.apply(lambda x: "|".join(x)) # convert list to string for grouping
        
        # write file of all matches for each sortyby strategy run
        df_top_n_matches.to_csv(resultspath/('team_top_n_matches_' + str(sortby) + '.csv'), index=False)
        
        ## aggregate and summarize > get single best match
        groupVars = ['id', 'Name', 'Habits_All','Habits_Orig','Top_Habits','n_habits_all', 'n_habits_orig', 'Cluster_ID_match', 'Clus_Top_Habits_match']
        df_best_match = cs.get_best_match(df_top_n_matches, groupVars)
        
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
        
        runs.append(df_best_match) # add each respondent dataframe to the list of dataframes  
    
    # combine top matches for all respondents into one dataframe
    df_best_matches = pd.concat(runs) 
    
    # clean columns
    finalCols = ['id', 'Name', 'Habits_All', 'Habits_Orig', 'Top_Habits', 'n_habits_all', 'n_habits_orig',
                 'Cluster_ID_match', 'Clus_Top_Habits_match','frac_top_habits', #'top_habits_sim','habits_sim',
                 'Habits_All_unique','Habits_Orig_unique', 'Habits_TopClus_overlap', 
                 'n_orig_unique', 'n_all_unique', 'n_clus_overlap','x_tsne', 'y_tsne']#  , 'sortby_strategy',  'count', 'frac_top_'+str(topN) ] 

    
    # add raw survey responses back to the processed results
    df_best_matches = df_best_matches[finalCols]
    df_best_matches = df_best_matches.merge(df_survey_responses, on='id')
    
    # add Rare Breed if 3 or fewer original survey habits
    cs.add_rare_breed(df_best_matches, 3)
        
    
    # rename columns
    df_best_matches.rename(columns = {'frac_top_habits': 'Cluster_Affinity',
                                      'x_tsne': 'x',
                                      'y_tsne': 'y'}, inplace=True)
    df_best_matches.rename(columns = param.ordCol_renameDict, inplace=True) 
    
    # rename habits in habit lists
    habitCols = ['Habits_All', 'Habits_Orig', 'Top_Habits','Clus_Top_Habits_match','Habits_Orig_unique', 'Habits_All_unique','Habits_TopClus_overlap']
    for col in habitCols:
        df_best_matches[col] = df_best_matches[col].apply(lambda x: cs.rename_habits(x))
        
    
    # write results file
    df_best_matches.to_csv(resultspath/('team_best_of_'+ str(topN) + "top_matches_" + str(len(sortbylist)) +'approaches.csv'), index=False)
    
    
