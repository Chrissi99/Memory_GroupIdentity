from otree.api import *
import pandas as pd
import random

df = pd.read_excel('_static/global/groups_scores.xlsx', keep_default_na=False, engine='openpyxl')


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'prior_beliefs'
    PLAYERS_PER_GROUP = None
    NUM_TASKS = "two"
    NUM_ROUNDS = 2
    NUM_GROUPMEMBERS = 6
    NUM_MEMBERS_W = "six"
    BONUS_REL = 1
    PRIZE = 2



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    prior_logic = models.IntegerField()
    prior_luck = models.IntegerField()
    procedure_click_prior = models.IntegerField(initial=0)
    procedure_time_prior = models.FloatField(initial=0.0)
    pagetime_instr_prior = models.FloatField(initial=0.0)
    pagetime_prior_logic = models.FloatField(initial=0.0)
    pagetime_prior_luck = models.FloatField(initial=0.0)
    unfocused_prior_instr = models.FloatField(initial=0.0)
    unfocused_prior_logic = models.FloatField(initial=0.0)
    unfocused_prior_luck = models.FloatField(initial=0.0)
    focus_data_prior_instr = models.LongStringField(blank=True)
    focus_data_prior_logic = models.LongStringField(blank=True)
    focus_data_prior_luck = models.LongStringField(blank=True)


# PAGES
class Instructions(Page):
    form_model = 'player'
    form_fields = ['procedure_click_prior', 'procedure_time_prior', 'pagetime_instr_prior', 'focus_data_prior_instr']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        print("Clicks:", player.procedure_click_prior)
        print("Time spent:", player.procedure_time_prior)
        import json
        raw = player.focus_data_prior_instr or ""
        try:
            events = json.loads(raw) if raw else []
            if not isinstance(events, list):
                events = []
        except (ValueError, TypeError):
            events = []
        total_unfocused = sum(e.get('unfocused_duration_ms', 0) for e in events)
        player.unfocused_prior_instr = total_unfocused / 1000
        print(f"{player.participant.code} unfocused for {total_unfocused / 1000:.1f}s")


class Prior_Logic(Page):
    form_model = 'player'
    form_fields = ['prior_logic', 'pagetime_prior_logic', 'focus_data_prior_logic']

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.task1 == 'logic':
            return player.round_number == 1
        if participant.task2 == 'logic':
            return player.round_number == 2

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if participant.belief_ref == "outgroup":
            player.prior_logic = 100 - player.prior_logic
        print("prior logic:", player.prior_logic)
        import json
        raw = player.focus_data_prior_logic or ""
        try:
            events = json.loads(raw) if raw else []
            if not isinstance(events, list):
                events = []
        except (ValueError, TypeError):
            events = []
        total_unfocused = sum(e.get('unfocused_duration_ms', 0) for e in events)
        player.unfocused_prior_logic = total_unfocused / 1000
        print(f"{player.participant.code} unfocused for {total_unfocused / 1000:.1f}s")


class Prior_Luck(Page):
    form_model = 'player'
    form_fields = ['prior_luck', 'pagetime_prior_luck', 'focus_data_prior_luck']

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.task1 == 'luck':
            return player.round_number == 1
        if participant.task2 == 'luck':
            return player.round_number == 2

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if participant.belief_ref == "outgroup":
            player.prior_luck = 100 - player.prior_luck
        print("prior luck:", player.prior_luck)
        participant = player.participant
        ingroup = df[df['group'] == participant.group]
        outgroup = df[df['group'] == participant.outgroup]
        sample_ing1 = ingroup.sample(n=6, replace=False)
        sample_outg1 = outgroup.sample(n=6, replace=False)
        print(sample_ing1)
        print(sample_outg1)
        participant.sample1_r1 = sample_ing1['score_1'].sum()
        participant.sample2_r1 = sample_outg1['score_1'].sum()
        sample_ing2 = ingroup.sample(n=6, replace=False)
        sample_outg2 = outgroup.sample(n=6, replace=False)
        participant.sample1_r2 = sample_ing2['score_2'].sum()
        participant.sample2_r2 = sample_outg2['score_2'].sum()
        if participant.sample1_r1 > participant.sample2_r1:
            participant.logic_result = '>'
            participant.r1_sign = random.choices(['>', '<'], weights=[2, 1], k=1)[
                0]  # random draw between > and <, but with 70% probability for >
        elif participant.sample1_r1 < participant.sample2_r1:
            participant.logic_result = '<'
            participant.r1_sign = random.choices(['>', '<'], weights=[1, 2], k=1)[0]
        else:
            participant.logic_result = random.choice(['>', '<'])
            participant.r1_sign = participant.logic_result
        if participant.sample1_r2 > participant.sample2_r2:
            participant.luck_result = '>'
            participant.r2_sign = random.choices(['>', '<'], weights=[2, 1], k=1)[0]
        elif participant.sample1_r2 < participant.sample2_r2:
            participant.luck_result = '<'
            participant.r2_sign = random.choices(['>', '<'], weights=[1, 2], k=1)[0]
        else:
            participant.luck_result = random.choice(['>', '<'])
            participant.r2_sign = participant.luck_result
        if participant.belief_ref == "outgroup":
            participant.logic_sign_shown = '<' if participant.r1_sign == '>' else '>'
            participant.luck_sign_shown = '<' if participant.r2_sign == '>' else '>'
        else:
            participant.logic_sign_shown = participant.r1_sign
            participant.luck_sign_shown = participant.r2_sign
        print("logic:", participant.logic_result, participant.r1_sign, participant.logic_sign_shown)
        print("luck:", participant.luck_result, participant.r2_sign, participant.luck_sign_shown)
        participant.beliefs_example_order = random.choice(['low_high', 'high_low'])
        print(participant.beliefs_example_order)
        import json
        raw = player.focus_data_prior_luck or ""
        try:
            events = json.loads(raw) if raw else []
            if not isinstance(events, list):
                events = []
        except (ValueError, TypeError):
            events = []
        total_unfocused = sum(e.get('unfocused_duration_ms', 0) for e in events)
        player.unfocused_prior_luck = total_unfocused / 1000
        print(f"{player.participant.code} unfocused for {total_unfocused / 1000:.1f}s")



page_sequence = [Instructions, Prior_Logic, Prior_Luck]
