from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'instructions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    BREAK_DURATION = "three days" # adapt accordingly
    TASKS_MEMORY = "six" # 2 tasks, prior beliefs, recall + posterior beliefs + self-confidence
    TASKS_DIRECT = "seven" # 2 tasks, prior beliefs, posterior beliefs I, recall + posterior beliefs II + self-confidence
    TASKS_PART1_DIRECT = "four" # 2 tasks, prior beliefs, posterior beliefs I
    TASKS_PART1_MEMORY = "three" # 2 tasks, prior beliefs,
    TASKS_PART2 = "three" # recall, posterior beliefs II, self-confidence


class Subsession(BaseSubsession):
    pass



def creating_session(subsession):
    import itertools
    # treatment = itertools.cycle(['BeliefsNoMemory', 'Recall', 'BeliefsMemory']) # CHANGE? OR INCLUDE FOR MAIN
    # treatment = itertools.cycle(['Recall', 'BeliefsMemory']) # for testing --> reinclude BeliefsNoMemory for experiment (or different sessions anyway)
    # random.seed(10799)
    # treatments = ['BeliefsNoMemory', 'Recall', 'BeliefsMemory']
    # weights = [0.28, 0.36, 0.36]
    treatment = itertools.cycle(['BeliefsNoMemory', 'Recall', 'BeliefsMemory',
                                 'BeliefsNoMemory', 'Recall', 'BeliefsMemory',
                                 'Recall', 'BeliefsMemory',
                                 'BeliefsNoMemory', 'Recall', 'BeliefsMemory',
                                 'BeliefsNoMemory', 'Recall', 'BeliefsMemory',
                                 'BeliefsNoMemory', 'Recall', 'BeliefsMemory',
                                 'Recall', 'BeliefsMemory',
                                'BeliefsNoMemory', 'Recall', 'BeliefsMemory',
                                'BeliefsNoMemory', 'Recall', 'BeliefsMemory',
                                 'BeliefsNoMemory', 'Recall', 'BeliefsMemory',
                                 ])
    for p in subsession.get_players():
        if p.round_number == 1:
            p.participant.treatment = next(treatment)
            # p.participant.treatment = 'BeliefsNoMemory'
            # p.participant.treatment = random.choices(treatments, weights)[0]
            print(p.participant.treatment)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class Instructions(Page):
    pass


page_sequence = [Instructions]
