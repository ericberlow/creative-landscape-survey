#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lists and dictionaries of column names
mappings of new columns to columns of original survey
mappings of column headers to creative habits
renaming dictionaries 
etc.

"""

import pathlib as pl

# paths
wd = pl.Path.cwd()
datapath = wd/"data"
resultspath = wd/"results"

## attribute lists for cleaning columns

   # variables from TopN matches to groupby and keep when summarizing top n matches. 
topN_groupVars = ['id', 'Habits_All','Habits_Orig','Top_Habits',  'n_habits_all', 'n_habits_orig', 'Cluster_ID', 'Clus_Top_Habits' ] + ['Name']
   # final attributes to keep in the best_match summary 
bestMatch_finalCols = ['id', 'Name','Cluster_ID', 'Habits_All', 'Habits_Orig','Top_Habits', 'Clus_Top_Habits', 
                       'Habits_unique', 'Habits_Clus_shared', 
                       'n_habits_all', 'n_habits_orig', 'frac_top_habits', 'top_habits_sim','habits_sim',
                       'n_unique', 'n_shared', 'x_tsne', 'y_tsne']
                 #  'sortby_strategy',  'count', 'frac_top_'+str(topN) ] 
finalCols = ['id','Name', 'Cluster_ID', 'Creative_Species', 'Clus_Percent','Cluster_Affinity', 'Clus_Top_Habits', 
             'Habits_All', 'Habits_Clus_shared', 'Habits_unique','n_habits_all', 'n_unique', 'n_shared',
             'x', 'y',  'Mono Routinus_affinity', 'Yolo Chaotis_affinity', 'Socialis Adventurous_affinity',
             'Focus Mononovous_affinity', 'Novo Gregarious_affinity', 'Sui Inspira_affinity', 'Solo Noctus_affinity',
             'Montasker -- Multitasker','Specialist -- Generalist','Solo Creator -- Collaborator','Self-Critical -- Self-Assured',
             'Distractible -- Focused','Inwardly vs Outwardly Inspired', 'Rational -- Intuitive', 'Internally vs Externally Motivated',
             'NonKinetic -- Kinetic', 'Controlled Chaos -- Organized', 'Slow -- Fast Paced', 'Pragmastist -- Perfectionist',
             'Risk Averse -- Risk Friendly','Make It Happen -- Let It Happen','Tenacious -- Reframer','Private vs Public Workspace',
             'Work in Silence vs Noise/Music', 'Urban -- Nature', 'Novetly Seeker -- Creature of Habit', 'Stifled_By vs Stimulated_By Constraints',
             'Happy -- Tortured', 'Non-Performer -- Performer', 'Solo-Ideator -- Group-Ideator', 'Consistent -- Inconsistent',
             'Creative_Process','Biorhythm']    

# list of ordinal columns
orig_OrdCols = ['Montasker -- Multitasker', # 'Monotasker -- Multitasker'
             'Specialist -- Generalist',
             'Solo Creator -- Collaborator',
             'Self-Critical -- Self-Assured',
             'Distractible -- Focused', # 'Like Distractions -- Dislike Distractions'
             'Inwardly vs Outwardly Inspired',  #'Inwardly -- Outwardly Inspired'
             'Rational -- Intuitive',
             'Internally vs Externally Motivated', #  'Internally -- Externally Motivated'
             'NonKinetic -- Kinetic',
             'Controlled Chaos -- Organized', # Comforting Mess -- Tidy
             'Slow -- Fast Paced', # Slow-Paced -- Fast-Paced',
             'Pragmastist -- Perfectionist',
             'Risk Averse -- Risk Friendly', # Risk-Averse -- Risk-Friendly 
             'Make It Happen -- Let It Happen',
             'Tenacious -- Reframer',
             'Private vs Public Workspace', # 'Private Spaces -- Public Spaces'
             'Work in Silence vs Noise/Music', # 'Quiet/Silence -- Noise/Music'
             'Urban -- Nature',   # 'Nature-Agnostic -- Nature Lover'
             'Novetly Seeker -- Creature of Habit', # 'Novely-Seeker -- Routine-Seeker'
             'Stifled_By vs Stimulated_By Constraints'] 


new_OrdCols = ['Happy -- Tortured',
               'Non-Performer -- Performer', 
               'Solo-Ideator -- Group-Ideator',
               'Consistent -- Inconsistent'  ]

new_CatCols = ['Creative_Process', 
               'Biorhythm'] # Early Bird vs Night Owl


BiorhythmResponses = {"Early Morning": "Early Bird",
                      "Late Night" : "Night Owl"}

CreativeProcessResponses = {"Seeing the big picture and defining the problem": "Problem Definer",
                            "Generating lots of ideas or possible solutions": "Ideator",
                            "Picking the winning solutions from the options": "Evaluator",
                            "Executing and getting things done": "Implementer"
                            }

# column name mapping:
newCol_renameDict = {'#': 'id', 
           'Please leave your name': 'Name', 
           # ordinal questions
           'What factors are most significant in motivating your creative work?': 'Internally vs Externally Motivated', #'Internally -- Externally Motivated'
           'When a significant risk is involved in my creative endeavors...': 'Risk Averse -- Risk Friendly',  # Risk-Averse -- Risk-Friendly        
           'How easy is it for you to do mediocre work if it seems prudent?': 'Pragmastist -- Perfectionist', 
           'Do you tend be more self-critical or more self-assured in your creative work?':'Self-Critical -- Self-Assured',
           'What is the breadth of your creative interests?': 'Specialist -- Generalist',
           'What do you regard as your strongest source of creative inspiration?': 'Inwardly vs Outwardly Inspired', #'Inwardly -- Outwardly Inspired'
           'How often do you engage in creative collaboration?': 'Solo Creator -- Collaborator',           
           'Compared to others, how rapidly do you tend to generate new ideas or possible solutions?': 'Slow -- Fast Paced', # Slow-Paced -- Fast-Paced',
           'To what degree does your creative work involve the element of chance?': 'Make It Happen -- Let It Happen',
           'How do you feel about the role of constraints in your creative process?': 'Stifled_By vs Stimulated_By Constraints', 
           'On average, how many creative projects do you work on simultaneously?': 'Montasker -- Multitasker', # 'Monotasker -- Multitasker'
           "When your initial plans for creative work don't pan out, how quickly do you typically move to Plan B?": 'Tenacious -- Reframer',
           'How do you envision and implement your creative projects?': 'Rational -- Intuitive',
           'Broadly speaking, how do you feel about the role of distractions in your creative process?': 'Distractible -- Focused', # 'Like Distractions -- Dislike Distractions'
           'How important do you think physical exercise and/or movement is to being creative in your work?': 'NonKinetic -- Kinetic',
           'How important to your creative process is it that you spend time outdoors in nature?': 'Urban -- Nature',  # Nature-Agnostic -- Nature Lover  
           'How compelled would you be to clean a messy workspace before beginning your creative work?': 'Controlled Chaos -- Organized', # Comforting Mess -- Tidy
           'What kind of space is most productive for you when you are working on a creative project?': 'Private vs Public Workspace', # Public Spaces -- Private Spaces
           "I'm most creative if my surroundings and routine are...": 'Novetly Seeker -- Creature of Habit', # Novely-Seeker -- Routine-Seeker
           'What noise level is most comfortable for you when you are working on a creative project?': 'Work in Silence vs Noise/Music', # 'Quiet/Silence -- Noise/Music'
           # new questions
           'How do you typically feel while your re creative problem solving or working on a creative project?':'Happy -- Tortured', 
           'Are you able to be creative when performing for others?': 'Non-Performer -- Performer', 
           'How do you feel about group brainstorming sessions?': 'Solo-Ideator -- Group-Ideator',
           'How much variation is there in the rate at which you do creative work?':  'Consistent -- Inconsistent', 
           # categorical questions
           'If you had to pick one, in which of the following stages of the creative process do you feel most confident?': 'Creative_Process', 
           'If you could choose, what time of day do you prefer to do creative work?': 'Biorhythm', 
            }


# dictionary of ordinal column names to endpoint habit tuples
habitDict = {'Montasker -- Multitasker': ("Monotasker", "Multitasker"),
             'Specialist -- Generalist': ("Specialist", "Generalist"),
             'Solo Creator -- Collaborator':  ("Solo Creator", "Collaborator"),
             'Self-Critical -- Self-Assured': ("Self-Critical", "Self-Assured"),
             'Distractible -- Focused': ("Love Distractions", "Hate Distractions"), # ('Like Distractions', 'Dislike Distractions'),
             'Inwardly vs Outwardly Inspired': ("Inwardly Inspired", "Outwardly Inspired"),  #'Internally -- Externally Inspired'
             'Rational -- Intuitive': ("Rational", "Intuitive"),
             'Internally vs Externally Motivated': ("Internally Motivated", "Externally Motivated"), #'Internally -- Externally Motivated'
             'NonKinetic -- Kinetic': ("NonKinetic", "Kinetic"),
             'Controlled Chaos -- Organized': ("Controlled Chaos", "Organized"), #("Comforting Mess", "Tidy Workspace"),
             'Slow -- Fast Paced': ("Slow Paced", "Fast Paced"),
             'Pragmastist -- Perfectionist': ("Pragmastist", "Perfectionist"),
             'Risk Averse -- Risk Friendly': ("Risk Averse", "Risk Friendly"),
             'Make It Happen -- Let It Happen': ("Make It Happen", "Let It Happen"), #("Make It Happen", "Let It Unfold"),
             'Tenacious -- Reframer': ("Tenacious", "Reframer"),
             'Private vs Public Workspace': ("Private", "Public"), #("Private Spaces", "Public Spaces"),
             'Work in Silence vs Noise/Music': ("Silence", "Noise/Music"), #("Quiet/Silence", "Noise/Music"),
             'Urban -- Nature': ("Urban", "Nature"), #("Nature-Agnostic", "Nature-Lover"),
             'Novetly Seeker -- Creature of Habit': ("Novelty Seeker", "Routine Seeker"), #("Novelty-Seeker", "Routine-Seeker")
             'Stifled_By vs Stimulated_By Constraints': ("Stifled By Constraints", "Stimulated By Constraints"),
             # new questions
             'Happy -- Tortured': ('Happy', 'Tortured') , 
             'Non-Performer -- Performer': ('Non-Performer', 'Performer'),
             'Solo-Ideator -- Group-Ideator': ('Solo-Ideator', 'Group-Ideator'),
             'Consistent -- Inconsistent': ('Consistent', 'Inconsistent'),
             }


#########################

#rename columns with updated habit endpoints
ordCol_renameDict = {'Montasker -- Multitasker':  'Monotasker -- Multitasker',
                     'Distractible -- Focused': "Like Distractions -- Dislike Distractions", 
                     'Inwardly vs Outwardly Inspired': 'Inwardly -- Outwardly Inspired', 
                     'Internally vs Externally Motivated': 'Internally -- Externally Motivated',
                     'Controlled Chaos -- Organized': "Comforting Mess -- Tidy",
                     'Slow -- Fast Paced': "Slow-Paced -- Fast-Paced", 
                     'Risk Averse -- Risk Friendly': "Risk-Averse -- Risk-Friendly", 
                     'Stifled_By vs Stimulated_By Constraints': 'Stifled By -- Stimulated By Constraints',
                     'Private vs Public Workspace': "Private Spaces -- Public Spaces", 
                     'Work in Silence vs Noise/Music': "Silence -- Noise", 
                     'Urban -- Nature': "Nature-Agnostic -- Nature Lover", 
                     'Novetly Seeker -- Creature of Habit': "Novely-Seeker -- Routine-Seeker"
                    }

habit_renameDict = {'Distractible': 'Like Distractions',
                    'Focused': 'Dislike Distractions',
                    'Controlled Chaos': 'Comforting Mess',
                    'Organized': 'Tidy',
                    'Slow Paced': 'Slow-Paced',
                    'Fast Paced': 'Fast-Paced',
                    'Risk Averse': 'Risk-Averse',
                    'Private': 'Private Spaces',
                    'Public': 'Public Spaces',
                    'Risk Friendly': 'Risk-Friendly',
                    "Silence": "Quiet/Silence", 
                    "Urban": "Nature-Agnostic" , 
                    "Nature": "Nature-Lover", 
                    "Novelty Seeker": "Novelty-Seeker", 
                    "Routine Seeker": "Routine-Seeker",
                    "Pragmastist": 'Pragmatist'
                    }
