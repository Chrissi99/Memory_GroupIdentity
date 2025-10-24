from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'self_confidence_post'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    NUM_QUESTIONS = 6
    SAMPLE_RANKING_TOT = 10
    SAMPLE_RANKING_OTHER = 9
    BONUS_SELF = '1'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ranking_post = models.IntegerField(
        label="Which rank in the score ranking of the randomly drawn sample of participants do you think you have?",
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelect
    )
    own_score_post = models.IntegerField(
        label="",
        min=0,
        max=10,
    )
    pagetime_selfconf = models.FloatField(initial=0.0)
    unfocused_selfconf = models.FloatField(initial=0.0)
    focus_data_selfconf = models.LongStringField(blank=True)


# PAGES
class SelfEstimationPost(Page):
    form_model = 'player'
    form_fields = ['ranking_post', 'own_score_post', 'pagetime_selfconf', 'focus_data_selfconf']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import json
        raw = player.focus_data_selfconf or ""
        try:
            events = json.loads(raw) if raw else []
            if not isinstance(events, list):
                events = []
        except (ValueError, TypeError):
            events = []
        total_unfocused = sum(e.get('unfocused_duration_ms', 0) for e in events)
        player.unfocused_selfconf = total_unfocused / 1000
        print(f"{player.participant.code} unfocused for {total_unfocused / 1000:.1f}s")

page_sequence = [SelfEstimationPost]
