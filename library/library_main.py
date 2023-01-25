import wordclouds as wc
import wordcount_sankey as sk
import sentiment_plot as sp
from screeNLPlays import *


def main():

    # create and gather the data for our three character based screenplays
    ted_lasso = screenNLPlays("Ted Lasso", ['Ted', 'Rebecca', 'Higgins', 'Roy', 'Nate',
                                            'Sam', 'Beard', 'Jamie', 'Keeley'],
                              ['lasso', 'script', 'may', 'final', 'shooting', 'goldenrod',
                               '15112019', '101', '2021', '17th', '205', 'november', '15', 't1216351',
                               '2019', 'nate', 'isaac', 'nathan', 'ext', 'int', 'jade', 'george'])
    ted_lasso.get_char_data()
    west_wing = screenNLPlays("The West Wing", ['Sam', 'Billy', 'Leo', 'C.J.', 'Laurie', 'Donna',
                                                'Josh', 'Ainsley', 'Bonnie', 'Margaret'],
                              ['continued'])
    west_wing.get_char_data()
    modern_family = screenNLPlays("Modern Family", ['Claire', 'Phil', 'Haley', 'Alex', 'Luke', 'Jay', 'Gloria',
                                                    'Manny', 'Mitchell', 'Cameron', 'Lily'],
                                  ['81209', 'draft', 'shooting', 'dunphy', '82609', '12908', '82009', '81109',
                                   'contd', 'continued'])
    modern_family.get_char_data()

    # create and gather data for our over time based screenplays
    breaking_bad = screenNLPlays("Breaking Bad")
    rick_and_morty = screenNLPlays("Rick and Morty")
    doctor_who = screenNLPlays("Doctor Who", [], ['bbc', 'int', 'script', 'clara', 'bill', '2015', 'continueddw9',
                                                  'moffat', 'ep', 'contd', 'production'])

    # create and plot a sankey diagram with each of the three shows
    sk.wordcount_sankey(ted_lasso, west_wing, modern_family, word_list=[], k=15)

    # create and plot wordclouds for each of the shows as subplots
    wc.wordcloud_subplots(ted_lasso, doctor_who, modern_family)

    # create and plot a line chart comparing sentiment analysis over time for the three shows
    sp.sentiment_plot([breaking_bad, rick_and_morty, doctor_who])


main()
