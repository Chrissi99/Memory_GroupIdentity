from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'part1_end'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    BREAK_DURATION = "three days" # adapt accordingly


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    attention2 = models.StringField(label="How much do you agree to the following statement? <br> 'I can accurately predict the exact winning lottery numbers for the next 50 years.'",
                                    choices=["strongly agree", "agree", "disagree", "strongly disagree"],
                                    widget=widgets.RadioSelectHorizontal)
    attention2_passed = models.BooleanField(initial=True)
    unfocused_attention2 = models.FloatField(initial=0.0)
    focus_data_attention2  = models.LongStringField(blank=True)


# PAGES
class Attention(Page):
    form_model = 'player'
    form_fields = ['attention2', 'focus_data_attention2']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        correct_answers = ["strongly disagree", "disagree"]
        if player.attention2 not in correct_answers:
            player.attention2_passed = False
        import json
        raw = player.focus_data_attention2 or ""
        try:
            events = json.loads(raw) if raw else []
            if not isinstance(events, list):
                events = []
        except (ValueError, TypeError):
            events = []
        total_unfocused = sum(e.get('unfocused_duration_ms', 0) for e in events)
        player.unfocused_attention2 = total_unfocused / 1000
        print(f"{player.participant.code} unfocused for {total_unfocused / 1000:.1f}s")
        # calculate post belief bonus for treatment BeliefsNoMemory
        participant = player.participant
        logic_refgroup_win = 1 if participant.logic_result == '>' else 0
        luck_refgroup_win = 1 if participant.luck_result == '>' else 0
        if participant.treatment == 'BeliefsNoMemory':
            logic_winning_prob = 100 - 100 * (logic_refgroup_win - participant.post_logic / 100) ** 2
            luck_winning_prob = 100 - 100 * (luck_refgroup_win - participant.post_luck / 100) ** 2
            participant.post_bonus_task = random.choice(['logic', 'luck'])
            if participant.post_bonus_task == 'logic':
                participant.post_bonus = 2 if random.random() < logic_winning_prob else 0
            else:
                participant.post_bonus = 2 if random.random() < luck_winning_prob else 0
            print(f"Post belief bonus task: {participant.post_bonus_task}, bonus: {participant.post_bonus}")


class End_Part1(Page):
    pass


page_sequence = [Attention, End_Part1]