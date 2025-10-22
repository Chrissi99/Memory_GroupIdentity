from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'groupiness'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    BUDGET = 10
    POINTS_TO_DOLLAR = "0.10"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    give_ingroup = models.IntegerField(
        min = 0,
        max = C.BUDGET,
        label = "",
    )
    give_outgroup = models.IntegerField(
        min = 0,
        max = C.BUDGET,
        label = "",
    )


# PAGES
class TaskDirect(Page):
    form_model = 'player'
    form_fields = ['give_outgroup']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.give_ingroup = C.BUDGET - player.give_outgroup
        print('ingroup:', player.give_ingroup)
        print('outgroup:', player.give_outgroup)

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return participant.treatment == "BeliefsNoMemory"


page_sequence = [TaskDirect]
