# -*- coding: utf-8 -*-
"""
Find creative species of website team  -
using new survey results and matching to archetypes from original survey

"""

import sys
sys.path.append("../CommonFunctions")
import pandas as pd
#import pathlib as pl #path library
import find_match_functions as fm
pd.set_option('display.expand_frame_repr', False) # expand display of data columns if screen is wide
import params as param


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

def process_respondent(df):

    # file names
    archnw = param.datapath/"Archetypes_Network.xlsx"
    top_habits = param.datapath/"Cluster_Metadata.xlsx"
    team = param.datapath/"Team_Survey_Responses.xlsx"

    # params
    topN = 10 # number of top matches to find
    sortby= ['top_habits_sim','habits_sim'] # first find archetype with highest average overlap in cluster top habits, then pick most similar archetype within
    # other options tested - sorty by 'frac_top_habits', then 'habits_sim' ; sort by 'habits_sim', then by 'frac_top_habits'


    print ('reading files')
    df_arch = pd.read_excel(archnw, sheet_name ='nodes', engine='openpyxl')
    df_arch.drop(['Discipline'], axis=1, inplace=True )
    df_clus = pd.read_excel(top_habits, engine='openpyxl')
    # add cluster metadata to archetypes
    df_arch_meta, df_clus_meta, archHabits, topHabits = fm.process_archetypes_cluster_metadata(df_arch, df_clus)

    # for new respndents, convert ordinal scores to list of habits
    df['habits_all'] = fm.get_habits_from_scores(df,  param.orig_OrdCols, param.new_OrdCols, param.habitDict)
    # add lists of original habits, top clus habits, and habit counts for each person.
    df = fm.add_habit_lists_counts(df, archHabits, topHabits)

    # get separate df of raw responses to add back
    raw_response_cols = param.orig_OrdCols + param.new_OrdCols + param.new_CatCols
    df_survey_responses = df[['id']+raw_response_cols]

    # clean columns
    respondent_keepCols = ['id', 'Habits_All', 'Habits_Orig', 'Top_Habits','n_habits_all', 'n_habits_orig'] + ['Name'] #+ raw_response_cols
    df = df[respondent_keepCols]

    ##### find top N matches for each respondent
    df_top_n_matches = fm.get_topN_matches_rowByrow(df, df_arch_meta, topN=topN, sortby=sortby, write=False)

    ######  summarize best match for each respondent and add habit lists comparisons #####
    df_best_match = fm.process_topN_matches(df_top_n_matches, df_clus_meta, groupVars = param.topN_groupVars)


    ##### add final best match metadata:
        # Creative Species name, Clus size, affinities to all other creative species, original raw responses
    df_best_match = fm.add_final_bestMatch_metadata(df_best_match, df_clus_meta, df_survey_responses)


    ##### write final best match file:
    return df_best_match

################################################################

if __name__ == '__main__':
    team = param.datapath/"Team_Survey_Responses.xlsx"
    df =  pd.read_excel(team, engine='openpyxl') # team survey results
    match_result = process_respondent(df)
    match_result.to_csv(param.resultspath/("best_match.csv"), index=False)