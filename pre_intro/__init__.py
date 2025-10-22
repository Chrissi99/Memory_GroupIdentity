from otree.api import *
import random
import itertools


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'pre_intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    NUM_TASKS = 3
    NUM_TASKS_W = "three"
    TASKS = ['logic', 'effort', 'luck']


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    task = itertools.cycle(['logic', 'effort', 'luck'])
    for p in subsession.get_players():
        if p.round_number == 1:
            task_numbers = list(range(1, C.NUM_TASKS + 1))
            random.shuffle(task_numbers)
            task_order = dict(zip(C.TASKS, task_numbers))
            p.participant.task_order = task_order
            print('task_order is', task_order)
            p.participant.task1 = 'logic' if task_order['logic'] == 1 else 'effort' if task_order['effort'] == 1 else 'luck'
            print('task1 is', p.participant.task1)
            p.participant.task2 = 'logic' if task_order['logic'] == 2 else 'effort' if task_order['effort'] == 2 else 'luck'
            print('task2 is', p.participant.task2)
            p.participant.task3 = 'logic' if task_order['logic'] == 3 else 'effort' if task_order['effort'] == 3 else 'luck'
            print('task3 is', p.participant.task3)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.BooleanField()
    political_affiliation = models.StringField(initial=None)
    political_orientation = models.StringField(
        choices=['Democrat', 'Republican'],
        # choices=['Democrat', 'Republican', "Neither/ I don't have a preference"],
        label='Which political side do you tend to favor (more than the other)?',
        widget=widgets.RadioSelectHorizontal(),
        blank=True,
    )


# PAGES
class Consent(Page):
    form_model = 'player'
    form_fields = ['consent']


class Politics(Page):
    form_model = 'player'
    form_fields = ['political_affiliation', 'political_orientation']

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        if player.political_affiliation == "Independent" or player.political_affiliation == "Other":
            if player.field_maybe_none('political_orientation') == 'Democrat' or player.field_maybe_none(
                    'political_orientation') == 'Republican':
                participant.group = player.field_maybe_none('political_orientation')
                participant.group_state = "weak"
            else:
                participant.group = random.choice(['Democrat', 'Republican'])
                participant.group_state = "none"
        else:
            participant.group = player.political_affiliation
            participant.group_state = "strong"
        if participant.group == 'Democrat':
            participant.outgroup = 'Republican'
        else:
            participant.outgroup = 'Democrat'
        print('group:', participant.group)
        print(participant.group_state)
        print('outgroup:', participant.outgroup)
        participant.test_id = participant.label


class Instructions(Page):
    pass


page_sequence = [Consent, Politics, Instructions]
