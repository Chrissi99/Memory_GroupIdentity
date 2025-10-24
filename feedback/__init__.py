from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'feedback'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    SAMPLE_BELIEFS = 2
    SAMPLE_W = "two"
    NUM_TASKS = 2
    NUM_TASKS_W = "two"
    NUM_GROUPMEMBERS = 6
    NUM_MEMBERS_W = "six"
    SIGNAL_ACCURACY_DEC = 0.667
    SIGNAL_WRONG_DEC = 0.333
    SIGNAL_ACC_FQ = 2
    SIGNAL_WRONG_FQ = 1
    SIGNAL_TOT_FQ = 3
    SIGNAL_TOT_WORD = "three"
    SIGNAL_ACC_WORD = "two"
    SIGNAL_WRONG_WORD = "one"
    creatures_true = 20
    creatures_false = 10




class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    rep_correct = models.BooleanField()
    rep_logic = models.StringField(
        label="",
        blank=True,
    )
    rep_effort = models.StringField(
        label="",
        blank=True,
    )
    rep_luck = models.StringField(
        label="",
        blank=True,
    )
    mistake_rep = models.IntegerField(
        initial=0,
    )
    check_probability = models.IntegerField(
        label="",
        blank=True,
    )
    mistake_prob = models.IntegerField(
        initial=0,
    )
    pagetime_feedback = models.FloatField(initial=0.0)
    pagetime_instr_feedback = models.FloatField(initial=0.0)
    unfocused_feedback_instr = models.FloatField(initial=0.0)
    focus_data_feedback_instr = models.LongStringField(blank=True)
    unfocused_feedback = models.FloatField(initial=0.0)
    focus_data_feedback = models.LongStringField(blank=True)


# PAGES
class InstructionsFeedback(Page):
    form_model = 'player'
    form_fields = ['pagetime_instr_feedback', 'focus_data_feedback_instr']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import json
        raw = player.focus_data_feedback_instr or ""
        try:
            events = json.loads(raw) if raw else []
            if not isinstance(events, list):
                events = []
        except (ValueError, TypeError):
            events = []
        total_unfocused = sum(e.get('unfocused_duration_ms', 0) for e in events)
        player.unfocused_feedback_instr = total_unfocused / 1000
        print(f"{player.participant.code} unfocused for {total_unfocused / 1000:.1f}s")


class Feedback(Page):
    form_model = 'player'
    form_fields = ['rep_logic', 'rep_luck', 'check_probability', 'pagetime_feedback', 'focus_data_feedback']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if player.rep_logic == participant.logic_sign_shown and player.rep_luck == participant.luck_sign_shown and player.check_probability == int(C.SIGNAL_WRONG_FQ):
            player.rep_correct = True
        else:
            player.rep_correct = False
        print('mistakes:', player.field_maybe_none('mistake_rep'))
        print('mistakes:', player.field_maybe_none('mistake_prob'))
        print('rep_correct:', player.rep_correct, 'logic:', player.rep_logic, 'luck:',
              player.rep_luck, 'check_probability:', player.check_probability)
        print('belief_ref is', participant.belief_ref)
        import json
        raw = player.focus_data_feedback or ""
        try:
            events = json.loads(raw) if raw else []
            if not isinstance(events, list):
                events = []
        except (ValueError, TypeError):
            events = []
        total_unfocused = sum(e.get('unfocused_duration_ms', 0) for e in events)
        player.unfocused_feedback = total_unfocused / 1000
        print(f"{player.participant.code} unfocused for {total_unfocused / 1000:.1f}s")

    @staticmethod
    def error_message(player: Player, values):
        participant = player.participant
        if values['rep_logic'] is None or values['rep_luck'] is None or values['check_probability'] is None:
            return 'Please answer all questions.'
        if values['rep_logic'] != participant.logic_sign_shown or values[
            'rep_luck'] != participant.luck_sign_shown and values['rep_logic'] is not None and values['rep_luck'] is not None:
            player.mistake_rep += 1
            return 'Your answer does not match the information you received. Please read the instructions carefully, check the table, and try again.'
        if values['check_probability'] != C.SIGNAL_WRONG_FQ and values['check_probability'] is not None:
            player.mistake_prob += 1
            return 'Your answer does not match the information you received. Please read the instructions carefully and try again.'


page_sequence = [InstructionsFeedback, Feedback]
    #[FeedbackNew, FeedbackSample
