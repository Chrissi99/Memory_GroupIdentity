from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'groupidentification'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2


class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        for p in subsession.get_players():
            participant = p.participant
            #order_venn = C.identity_groups.copy()
            #random.shuffle(order_venn)
            #participant.order_venn = order_venn


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    venn_identity = models.IntegerField()
    click_count_gi = models.IntegerField(initial=0)
    avg_click_interval_gi = models.FloatField(initial=0.0)


# PAGES
class InstructionsGI(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class VennGI(Page):
    form_model = 'player'
    form_fields = ['venn_identity', 'click_count_gi', 'avg_click_interval_gi']

    @staticmethod
    def error_message(player, values):
        print('Slider value is', values)
        if values['venn_identity'] is None:
            return 'Please click on the sliders to make a decision.'
        return None

    @staticmethod
    def vars_for_template(player):
        participant = player.participant
        group_label = "Democrats" if participant.group == "Democrat" else "Republicans"
        #if player.round_number == 1:
            #group_label = participant.order_venn[0]
        #elif player.round_number == 2:
            #group_label = participant.order_venn[1]
        return dict(
            group_label = group_label,
        )

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 #and player.participant.group_state != "none"



page_sequence = [VennGI]
