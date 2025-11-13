from otree.api import *
import random
import itertools


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'groupassignment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    TASKS = ['logic', 'luck']
    NUM_TASKS = 2
    BELIEF_REF = ['ingroup', 'outgroup']


class Subsession(BaseSubsession):
    pass



def creating_session(subsession: Subsession):
    belief_refs = itertools.cycle(['ingroup', 'outgroup'])
    for p in subsession.get_players():
        if p.round_number == 1:
            task_numbers = list(range(1, C.NUM_TASKS + 1))
            random.shuffle(task_numbers)
            task_order = dict(zip(C.TASKS, task_numbers))
            p.participant.task_order = task_order
            print('task_order is', task_order)
            p.participant.task1 = 'logic' if task_order['logic'] == 1 else 'luck'
            print('task1 is', p.participant.task1)
            p.participant.task2 = 'logic' if task_order['logic'] == 2 else 'luck'
            print('task2 is', p.participant.task2)
            p.participant.score_logic = 0
            prior = ["logic", "luck"]
            random.shuffle(prior)
            #p.participant.belief_ref = random.choice(C.BELIEF_REF)
            p.participant.belief_ref = next(belief_refs)
            print('belief_ref is', p.participant.belief_ref)
            p.participant.group_ref_background = random.choice(['Democrat', 'Republican'])
            p.participant.belief_example_value = random.choice(['low', 'high'])
            print('belief_example_value is', p.participant.belief_example_value)
            p.participant.belief_example_direction = random.choice(['over', 'under'])
            print('belief_example_direction is', p.participant.belief_example_direction)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    political_affiliation = models.StringField(initial=None)
    political_orientation = models.StringField(
        choices=['Democrat','Republican', "Neither/ I don't have a preference"],
        label='Which political side do you tend to favor (more than the other)?',
        widget=widgets.RadioSelectHorizontal(),
        blank=True,
    )
    click_count_ga = models.IntegerField(initial=0)
    avg_click_interval_ga = models.FloatField(initial=0.0)



# PAGES
class Politics(Page):
    form_model = 'player'
    form_fields = ['political_affiliation', 'political_orientation', 'click_count_ga', 'avg_click_interval_ga']

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        if player.political_affiliation == "Independent" or player.political_affiliation == "Other":
            if player.field_maybe_none('political_orientation') == 'Democrat' or player.field_maybe_none('political_orientation') == 'Republican':
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
        print('group:',participant.group)
        print(participant.group_state)
        print('outgroup:', participant.outgroup)


page_sequence = [Politics]
