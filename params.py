#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 07:33:05 2021

@author: ericberlow
"""


#TODO: rename habits


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
                    'Slow': 'Slow-Paced',
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
