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
    treatment = itertools.cycle(['BeliefsNoMemory', 'Recall', 'BeliefsMemory'])
    treatment = itertools.cycle(['BeliefsNoMemory'])
    for p in subsession.get_players():
        if p.round_number == 1:
            p.participant.treatment = next(treatment)
            print(p.participant.treatment)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    focus_data = models.LongStringField(blank=True)
    total_unfocused_ms = models.FloatField(initial=0)
    total_unfocused_sec = models.FloatField(initial=0)


# PAGES
class Instructions(Page):
    form_model = 'player'
    form_fields = ['focus_data']

    @staticmethod
    def before_next_page(player, timeout_happened):
        import json
        raw = player.focus_data or ""
        try:
            events = json.loads(raw) if raw else []
            if not isinstance(events, list):
                events = []
        except (ValueError, TypeError):
            events = []

        total_unfocused = sum(e.get('unfocused_duration_ms', 0) for e in events)
        player.total_unfocused_ms = total_unfocused
        player.total_unfocused_sec = total_unfocused / 1000

        print(f"{player.participant.code} unfocused for {total_unfocused / 1000:.1f}s")
        print(events)


page_sequence = [Instructions]
