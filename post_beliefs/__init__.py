from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'post_beliefs'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2
    NUM_GROUPMEMBERS = 6
    NUM_MEMBERS_W = "six"
    BONUS_REL = 1
    PRIZE = 2
    NUM_TASKS = "two"
    INSTRUCTIONS_PROCEDURE = "post_beliefs/SnippetProcedure.html"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    post_direct_logic = models.IntegerField()
    post_direct_luck = models.IntegerField()
    procedure_click_post1 = models.IntegerField(initial=0)
    procedure_time_post1 = models.FloatField(initial=0.0)
    pagetime_instr_post1 = models.FloatField(initial=0.0)
    pagetime_post1_logic = models.FloatField(initial=0.0)
    pagetime_post1_luck = models.FloatField(initial=0.0)
    unfocused_post_instr = models.FloatField(initial=0.0)
    unfocused_post_logic = models.FloatField(initial=0.0)
    unfocused_post_luck = models.FloatField(initial=0.0)
    focus_data_post_instr = models.LongStringField(blank=True)
    focus_data_post_logic = models.LongStringField(blank=True)
    focus_data_post_luck = models.LongStringField(blank=True)


# PAGES
class Instructions(Page):
    form_model = 'player'
    form_fields = ['procedure_click_post1', 'procedure_time_post1', 'pagetime_instr_post1', 'focus_data_post_instr']

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == 1 and participant.treatment == "BeliefsNoMemory"

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import json
        raw = player.focus_data_post_instr or ""
        try:
            events = json.loads(raw) if raw else []
            if not isinstance(events, list):
                events = []
        except (ValueError, TypeError):
            events = []
        total_unfocused = sum(e.get('unfocused_duration_ms', 0) for e in events)
        player.unfocused_post_instr = total_unfocused / 1000
        print(f"{player.participant.code} unfocused for {total_unfocused / 1000:.1f}s")

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        belief_example_value = participant.belief_example_value
        if belief_example_value == 'low':
            belief_example = 34
            belief_example_compl = 66
            prob_r1 = 56.44
            prob_r0 = 88.44
            prob_avg = 77.56
            more_likely = 'losing (R=0)'
        else:
            belief_example = 68
            belief_example_compl = 32
            prob_r1 = 89.76
            prob_r0 = 53.76
            prob_avg = 78.24
            more_likely = 'winning (R=1)'
        belief_example_direction = participant.belief_example_direction
        if belief_example_direction == 'over':
            deviation = "overreport"
            r1_direction = 'higher'
            r0_direction = 'lower'
            if belief_example_value == 'low':
                deviation_example = 60
                dev_r1 = 84
                dev_r0 = 64
                dev_avg = 70.8
            else:
                deviation_example = 90
                dev_r1 = 99
                dev_r0 = 19
                dev_avg = 73.4
        else:
            deviation = "underreport"
            r1_direction = 'lower'
            r0_direction = 'higher'
            if belief_example_value == 'low':
                deviation_example = 10
                dev_r1 = 19
                dev_r0 = 99
                dev_avg = 71.8
            else:
                deviation_example = 40
                dev_r1 = 64
                dev_r0 = 84
                dev_avg = 70.4
        return {
            'belief_example': belief_example,
            'belief_example_compl': belief_example_compl,
            'deviation': deviation,
            'deviation_example': deviation_example,
            'prob_r1': prob_r1,
            'prob_r0': prob_r0,
            'prob_avg': prob_avg,
            'dev_r1': dev_r1,
            'dev_r0': dev_r0,
            'dev_avg': dev_avg,
            'r1_direction': r1_direction,
            'r0_direction': r0_direction,
            'more_likely': more_likely,
        }


class PostLogic(Page):
    form_model = 'player'
    form_fields = ['post_direct_logic', 'pagetime_post1_logic', 'focus_data_post_logic']

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.task1 == 'logic':
            return player.round_number == 1 and participant.treatment == "BeliefsNoMemory"
        if participant.task2 == 'logic':
            return player.round_number == 2 and participant.treatment == "BeliefsNoMemory"

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        if participant.belief_ref == "outgroup":
            player.post_direct_logic = 100 - player.post_direct_logic
        print("post logic:", player.post_direct_logic)
        import json
        raw = player.focus_data_post_logic or ""
        try:
            events = json.loads(raw) if raw else []
            if not isinstance(events, list):
                events = []
        except (ValueError, TypeError):
            events = []
        total_unfocused = sum(e.get('unfocused_duration_ms', 0) for e in events)
        player.unfocused_post_logic = total_unfocused / 1000
        print(f"{player.participant.code} unfocused for {total_unfocused / 1000:.1f}s")

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        belief_example_value = participant.belief_example_value
        if belief_example_value == 'low':
            belief_example = 34
            belief_example_compl = 66
            prob_r1 = 56.44
            prob_r0 = 88.44
            prob_avg = 77.56
            more_likely = 'losing (R=0)'
        else:
            belief_example = 68
            belief_example_compl = 32
            prob_r1 = 89.76
            prob_r0 = 53.76
            prob_avg = 78.24
            more_likely = 'winning (R=1)'
        belief_example_direction = participant.belief_example_direction
        if belief_example_direction == 'over':
            deviation = "overreport"
            r1_direction = 'higher'
            r0_direction = 'lower'
            if belief_example_value == 'low':
                deviation_example = 60
                dev_r1 = 84
                dev_r0 = 64
                dev_avg = 70.8
            else:
                deviation_example = 90
                dev_r1 = 99
                dev_r0 = 19
                dev_avg = 73.4
        else:
            deviation = "underreport"
            r1_direction = 'lower'
            r0_direction = 'higher'
            if belief_example_value == 'low':
                deviation_example = 10
                dev_r1 = 19
                dev_r0 = 99
                dev_avg = 71.8
            else:
                deviation_example = 40
                dev_r1 = 64
                dev_r0 = 84
                dev_avg = 70.4
        return {
            'belief_example': belief_example,
            'belief_example_compl': belief_example_compl,
            'deviation': deviation,
            'deviation_example': deviation_example,
            'prob_r1': prob_r1,
            'prob_r0': prob_r0,
            'prob_avg': prob_avg,
            'dev_r1': dev_r1,
            'dev_r0': dev_r0,
            'dev_avg': dev_avg,
            'r1_direction': r1_direction,
            'r0_direction': r0_direction,
            'more_likely': more_likely,
        }


class PostLuck(Page):
    form_model = 'player'
    form_fields = ['post_direct_luck', 'pagetime_post1_luck', 'focus_data_post_luck']

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.task1 == 'luck':
            return player.round_number == 1 and participant.treatment == "BeliefsNoMemory"
        if participant.task2 == 'luck':
            return player.round_number == 2 and participant.treatment == "BeliefsNoMemory"

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        if participant.belief_ref == "outgroup":
            player.post_direct_luck = 100 - player.post_direct_luck
        print("post luck:", player.post_direct_luck)
        import json
        raw = player.focus_data_post_luck or ""
        try:
            events = json.loads(raw) if raw else []
            if not isinstance(events, list):
                events = []
        except (ValueError, TypeError):
            events = []
        total_unfocused = sum(e.get('unfocused_duration_ms', 0) for e in events)
        player.unfocused_post_luck = total_unfocused / 1000
        print(f"{player.participant.code} unfocused for {total_unfocused / 1000:.1f}s")

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        belief_example_value = participant.belief_example_value
        if belief_example_value == 'low':
            belief_example = 34
            belief_example_compl = 66
            prob_r1 = 56.44
            prob_r0 = 88.44
            prob_avg = 77.56
            more_likely = 'losing (R=0)'
        else:
            belief_example = 68
            belief_example_compl = 32
            prob_r1 = 89.76
            prob_r0 = 53.76
            prob_avg = 78.24
            more_likely = 'winning (R=1)'
        belief_example_direction = participant.belief_example_direction
        if belief_example_direction == 'over':
            deviation = "overreport"
            r1_direction = 'higher'
            r0_direction = 'lower'
            if belief_example_value == 'low':
                deviation_example = 60
                dev_r1 = 84
                dev_r0 = 64
                dev_avg = 70.8
            else:
                deviation_example = 90
                dev_r1 = 99
                dev_r0 = 19
                dev_avg = 73.4
        else:
            deviation = "underreport"
            r1_direction = 'lower'
            r0_direction = 'higher'
            if belief_example_value == 'low':
                deviation_example = 10
                dev_r1 = 19
                dev_r0 = 99
                dev_avg = 71.8
            else:
                deviation_example = 40
                dev_r1 = 64
                dev_r0 = 84
                dev_avg = 70.4
        return {
            'belief_example': belief_example,
            'belief_example_compl': belief_example_compl,
            'deviation': deviation,
            'deviation_example': deviation_example,
            'prob_r1': prob_r1,
            'prob_r0': prob_r0,
            'prob_avg': prob_avg,
            'dev_r1': dev_r1,
            'dev_r0': dev_r0,
            'dev_avg': dev_avg,
            'r1_direction': r1_direction,
            'r0_direction': r0_direction,
            'more_likely': more_likely,
        }


page_sequence = [Instructions, PostLogic, PostLuck]