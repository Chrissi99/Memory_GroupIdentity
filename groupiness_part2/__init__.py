from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'groupiness_part2'
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
class TaskBreak(Page):
    form_model = 'player'
    form_fields = ['give_outgroup']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.give_ingroup = C.BUDGET - player.give_outgroup
        print('ingroup:', player.give_ingroup)
        print('outgroup:', player.give_outgroup)
        participant = player.participant
        # calculate belief bonus
        logic_refgroup_win = 1 if participant.logic_result == '>' else 0
        luck_refgroup_win = 1 if participant.luck_result == '>' else 0
        logic_winning_prob = 100 - 100 * (logic_refgroup_win - participant.post2_logic / 100) ** 2
        luck_winning_prob = 100 - 100 * (luck_refgroup_win - participant.post2_luck / 100) ** 2
        participant.post2_bonus_task = random.choice(['logic', 'luck'])
        if participant.post2_bonus_task == 'logic':
            participant.post2_bonus = 2 if random.random() < (logic_winning_prob*0.01) else 0
        else:
            participant.post2_bonus = 2 if random.random() < (luck_winning_prob*0.01) else 0
        print(f"Post belief bonus task: {participant.post2_bonus_task}, bonus: {participant.post2_bonus}")


page_sequence = [TaskBreak]
