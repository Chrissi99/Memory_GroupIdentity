from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'self_confidence'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    NUM_QUESTIONS = 15
    SAMPLE_RANKING_TOT = 10
    SAMPLE_RANKING_OTHER = 9
    BONUS_SELF = '1'
    RANGE_RANKING = 10
    RANKS_RANGE = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ranking = models.IntegerField(
        label="Which rank in the randomly drawn sample of participants do you think you have?",
        choices=[1, 2, 3, 4, 5, 6,7,8,9,10],
        widget=widgets.RadioSelect
    )
    # gives quantile (decentile) of ranking
    own_score = models.IntegerField(
        label="",
        min=0,
        max=15,
    )


# PAGES
class SelfEstimation(Page):
    form_model = 'player'
    form_fields = ['ranking', 'own_score']

page_sequence = [SelfEstimation]
