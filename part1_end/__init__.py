from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'part1_end'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    BREAK_DURATION = "three days" # adapt accordingly


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class End_Part1(Page):
    pass


page_sequence = [End_Part1]