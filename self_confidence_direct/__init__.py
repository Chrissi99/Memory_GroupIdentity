from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'self_confidence_direct'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    NUM_QUESTIONS = 15
    SAMPLE_RANKING_TOT = 10
    SAMPLE_RANKING_OTHER = 9
    BONUS_SELF = '1'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ranking_direct = models.IntegerField(
        label="Which rank in the score ranking of the randomly drawn sample of participants do you think you have?",
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelect
    )
    own_score_direct = models.IntegerField(
        label="",
        min=0,
        max=15,
    )


# PAGES
class SelfEstimationDirect(Page):
    form_model = 'player'
    form_fields = ['ranking_direct', 'own_score_direct']

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return participant.treatment == "BeliefsNoMemory"


page_sequence = [SelfEstimationDirect]
