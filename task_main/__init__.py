from otree.api import *
import random
import itertools
import json
import time
import numpy as np
import time
from otree import settings
from .image_utils import encode_image
import pandas as pd


doc = """
Your app description
"""


def get_task_module(player):
    """
    This function is only needed for demo mode, to demonstrate all the different versions.
    You can simplify it if you want.
    """
    from . import task_matrix
    session = player.session
    task = session.config.get("task")
    return task_matrix


class C(BaseConstants):
    NAME_IN_URL = 'task_main'
    PLAYERS_PER_GROUP = None
    TASKS = ['logic', 'luck']
    NUM_ROUNDS = len(TASKS)
    NUM_TASK = 2
    NUM_TASKS_W = "two"
    NUM_MEMBERS_W = "six"
    Q_NUM_LOGIC = 6 # 8
    DICE_ROLLS = 10
    TIME_PER_QUESTION = 30
    BONUS_LOGIC = "0.10"
    POINTS_SIX = "two"
    POINTS_FIVE = "one"
    BONUS_DICE = "0.10"
    BONUS_SIX = "0.20"
    BONUS_FIVE = "0.10"
    MAX_BONUS_LOGIC = "0.60" # adapt depending on number of questions
    QUESTIONS_LOGIC = ['global/inductive_5.jpg',
                       'global/inductive_3.jpg',
                       'global/inductive_1.jpg',
                       'global/ravens_2.jpg',
                       'global/inductive_7.jpg',
                       'global/inductive_4.jpg',
                       'global/inductive_9.jpg',
                       'global/inductive_11.jpg',
                       ]
    SOLUTIONS_LOGIC = ['A', 'C', 'A', 'B', 'C', 'B', 'B', 'D',]
    EXAMPLE_RAVENS = 'global/inductive_13.jpg'
    EXAMPLE_SOLUTION = 'E'
    TIMER_TEXT = "Time left to complete this question:"

    instructions_template = __name__ + "/instructions.html"
    captcha_length = 3



class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    session = subsession.session
    defaults = dict(
        retry_delay=1.0, puzzle_delay=1.0, attempts_per_puzzle=1, max_iterations=None
    )
    session.params = {}
    for param in defaults:
        session.params[param] = session.config.get(param, defaults[param])

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    score_logic = models.IntegerField(initial=0)
    logic_q1  = models.StringField(
        label="Please select the correct answer",
        choices=['A', 'B', 'C', 'D', 'E'],
        widget=widgets.RadioSelectHorizontal
    )
    logic_q2 = models.StringField(
        label="Please select the correct answer",
        choices=['A', 'B', 'C', 'D', 'E'],
        widget=widgets.RadioSelectHorizontal
    )
    logic_q3 = models.StringField(
        label="Please select the correct answer",
        choices=['A', 'B', 'C', 'D', 'E'],
        widget=widgets.RadioSelectHorizontal
    )
    logic_q4 = models.StringField(
        label="Please select the correct answer",
        choices=['A', 'B', 'C', 'D', 'E'],
        widget=widgets.RadioSelectHorizontal
    )
    logic_q5 = models.StringField(
        label="Please select the correct answer",
        choices=['A', 'B', 'C', 'D', 'E'],
        widget=widgets.RadioSelectHorizontal
    )
    logic_q6 = models.StringField(
        label="Please select the correct answer",
        choices=['A', 'B', 'C', 'D', 'E'],
        widget=widgets.RadioSelectHorizontal
    )
    """
    logic_q7 = models.StringField(
        label="Please select the correct answer",
        choices=['A', 'B', 'C', 'D', 'E'],
        widget=widgets.RadioSelectHorizontal
    )
    logic_q8 = models.StringField(
        label="Please select the correct answer",
        choices=['A', 'B', 'C', 'D', 'E'],
        widget=widgets.RadioSelectHorizontal
    )
    """
    rolls = models.LongStringField()
    score_luck = models.IntegerField()
    #focus_data = models.LongStringField(blank=True)
    #total_unfocused_ms = models.FloatField(initial=0)
    pagetime_background = models.FloatField(initial=0.0)
    attention1 = models.StringField(label="It is important for us that you pay attention. To show this please select '<u>strongly disagree</u>' in this question.",
                                    choices=["strongly agree", "agree", "disagree", "strongly disagree"],
                                    widget=widgets.RadioSelectHorizontal)
    attention1_passed = models.BooleanField(initial=True)
    unfocused_background = models.FloatField(initial=0.0)
    focus_data_background = models.LongStringField(blank=True)
    background_click_example = models.IntegerField(initial=0)
    background_time_example = models.FloatField(initial=0.0)



"""
class Puzzle(ExtraModel):
    player = models.Link(Player)
    iteration = models.IntegerField(initial=0)
    attempts = models.IntegerField(initial=0)
    timestamp = models.FloatField(initial=0)
    # can be either simple text, or a json-encoded definition of the puzzle, etc.
    text = models.LongStringField()
    # solution may be the same as text, if it's simply a transcription task
    solution = models.LongStringField()
    response = models.LongStringField()
    response_timestamp = models.FloatField()
    is_correct = models.BooleanField()
"""
"""
def generate_puzzle(player: Player) -> Puzzle:
    task_module = get_task_module(player)
    fields = task_module.generate_puzzle_fields()
    player.iteration_effort += 1
    return Puzzle.create(
        player=player, iteration=player.iteration_effort, timestamp=time.time(), **fields
    )
"""
"""
def get_current_puzzle(player):
    puzzles = Puzzle.filter(player=player, iteration=player.iteration_effort)
    if puzzles:
        [puzzle] = puzzles
        return puzzle
"""
"""
def encode_puzzle(puzzle: Puzzle):
    task_module = get_task_module(puzzle.player)  # noqa
    # generate image for the puzzle
    image = task_module.render_image(puzzle)
    data = encode_image(image)
    return dict(image=data)
"""
"""
def get_progress(player: Player):
    return dict(
        num_trials=player.num_trials_effort,
        num_correct=player.num_correct_effort,
        num_incorrect=player.num_failed_effort,
        iteration=player.iteration_effort,
    )
"""
"""
#def play_game(player: Player, message: dict):
    Main game workflow
    Implemented as reactive scheme: receive message from vrowser, react, respond.

    Generic game workflow, from server point of view:
    - receive: {'type': 'load'} -- empty message means page loaded
    - check if it's game start or page refresh midgame
    - respond: {'type': 'status', 'progress': ...}
    - respond: {'type': 'status', 'progress': ..., 'puzzle': data} -- in case of midgame page reload

    - receive: {'type': 'next'} -- request for a next/first puzzle
    - generate new puzzle
    - respond: {'type': 'puzzle', 'puzzle': data}

    - receive: {'type': 'answer', 'answer': ...} -- user answered the puzzle
    - check if the answer is correct
    - respond: {'type': 'feedback', 'is_correct': true|false, 'retries_left': ...} -- feedback to the answer

    If allowed by config `attempts_pre_puzzle`, client can send more 'answer' messages
    When done solving, client should explicitely request next puzzle by sending 'next' message

    Field 'progress' is added to all server responses to indicate it on page.

    To indicate max_iteration exhausted in response to 'next' server returns 'status' message with iterations_left=0

    session = player.session
    my_id = player.id_in_group
    params = session.params
    task_module = get_task_module(player)

    now = time.time()
    # the current puzzle or none
    current = get_current_puzzle(player)

    message_type = message['type']

    # page loaded
    if message_type == 'load':
        p = get_progress(player)
        if current:
            return {
                my_id: dict(type='status', progress=p, puzzle=encode_puzzle(current))
            }
        else:
            return {my_id: dict(type='status', progress=p)}

    #if message_type == "cheat" and settings.DEBUG:
     #   return {my_id: dict(type='solution', solution=current.solution)}

    # client requested new puzzle
    if message_type == "next":
        if current is not None:
            if current.response is None:
                raise RuntimeError("trying to skip over unsolved puzzle")
            if now < current.timestamp + params["puzzle_delay"]:
                raise RuntimeError("retrying too fast")
            if current.iteration == params['max_iterations']:
                return {
                    my_id: dict(
                        type='status', progress=get_progress(player), iterations_left=0
                    )
                }
        # generate new puzzle
        z = generate_puzzle(player)
        p = get_progress(player)
        return {my_id: dict(type='puzzle', puzzle=encode_puzzle(z), progress=p)}

    # client gives an answer to current puzzle
    if message_type == "answer":
        if current is None:
            raise RuntimeError("trying to answer no puzzle")

        if current.response is not None:  # it's a retry
            if current.attempts >= params["attempts_per_puzzle"]:
                raise RuntimeError("no more attempts allowed")
            if now < current.response_timestamp + params["retry_delay"]:
                raise RuntimeError("retrying too fast")

            # undo last updation of player progress
            player.num_trials_effort -= 1
            if current.is_correct:
                player.num_correct_effort -= 1
            else:
                player.num_failed_effort -= 1

        # check answer
        answer = message["answer"]

        if answer == "" or answer is None:
            raise ValueError("bogus answer")

        current.response = answer
        current.is_correct = task_module.is_correct(answer, current)
        current.response_timestamp = now
        current.attempts += 1

        # update player progress
        if current.is_correct:
            player.num_correct_effort += 1
        else:
            player.num_failed_effort += 1
        player.num_trials_effort += 1

        retries_left = params["attempts_per_puzzle"] - current.attempts
        p = get_progress(player)
        return {
            my_id: dict(
                type='feedback',
                is_correct=current.is_correct,
                retries_left=retries_left,
                progress=p,
            )
        }

    raise RuntimeError("unrecognized message from client")
"""

#def get_timeout_seconds(player):
 #   participant = player.participant
  #  import time
   # return participant.expiry - time.time()


# PAGES
class InstructionsTask(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == 1


class InstructionsLogic(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == participant.task_order['logic']


class LogicTask1(Page):
    form_model = 'player'
    form_fields = ['logic_q1']
    timer_text = C.TIMER_TEXT
    timeout_seconds = C.TIME_PER_QUESTION
    # get_timeout_seconds = get_timeout_seconds

    @staticmethod
    def vars_for_template(player: Player):
        return {'image_path': C.QUESTIONS_LOGIC[0]}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.score_logic = 0
        if player.logic_q1 == C.SOLUTIONS_LOGIC[0]:
            participant.score_logic += 1
        player.score_logic = participant.score_logic


    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == participant.task_order['logic'] # and get_timeout_seconds(player) > 0

class LogicTask2(Page):
    form_model = 'player'
    form_fields = ['logic_q2']
    timer_text = C.TIMER_TEXT
    timeout_seconds = C.TIME_PER_QUESTION
    # get_timeout_seconds = get_timeout_seconds

    @staticmethod
    def vars_for_template(player: Player):
        return {'image_path': C.QUESTIONS_LOGIC[1]}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if player.logic_q2 == C.SOLUTIONS_LOGIC[1]:
            participant.score_logic += 1
        player.score_logic = participant.score_logic

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == participant.task_order['logic'] # and get_timeout_seconds(player) > 0


class LogicTask3(Page):
    form_model = 'player'
    form_fields = ['logic_q3']
    timer_text = C.TIMER_TEXT
    timeout_seconds = C.TIME_PER_QUESTION
    # get_timeout_seconds = get_timeout_seconds

    @staticmethod
    def vars_for_template(player: Player):
        return {'image_path': C.QUESTIONS_LOGIC[2]}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if player.logic_q3 == C.SOLUTIONS_LOGIC[2]:
            participant.score_logic += 1
        player.score_logic = participant.score_logic

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == participant.task_order['logic'] # and get_timeout_seconds(player) > 0


class LogicTask4(Page):
    form_model = 'player'
    form_fields = ['logic_q4']
    timer_text = C.TIMER_TEXT
    timeout_seconds = C.TIME_PER_QUESTION
    # get_timeout_seconds = get_timeout_seconds

    @staticmethod
    def vars_for_template(player: Player):
        return {'image_path': C.QUESTIONS_LOGIC[3]}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if player.logic_q4 == C.SOLUTIONS_LOGIC[3]:
            participant.score_logic += 1
        player.score_logic = participant.score_logic

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == participant.task_order['logic'] # and get_timeout_seconds(player) > 0

class LogicTask5(Page):
    form_model = 'player'
    form_fields = ['logic_q5']
    timer_text = C.TIMER_TEXT
    timeout_seconds = C.TIME_PER_QUESTION
    # get_timeout_seconds = get_timeout_seconds

    @staticmethod
    def vars_for_template(player: Player):
        return {'image_path': C.QUESTIONS_LOGIC[4]}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if player.logic_q5 == C.SOLUTIONS_LOGIC[4]:
            participant.score_logic += 1
        player.score_logic = participant.score_logic

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == participant.task_order['logic'] # and get_timeout_seconds(player) > 0


class LogicTask6(Page):
    form_model = 'player'
    form_fields = ['logic_q6']
    timer_text = C.TIMER_TEXT
    timeout_seconds = C.TIME_PER_QUESTION
    # get_timeout_seconds = get_timeout_seconds

    @staticmethod
    def vars_for_template(player: Player):
        return {'image_path': C.QUESTIONS_LOGIC[5]}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if player.logic_q6 == C.SOLUTIONS_LOGIC[5]:
            participant.score_logic += 1
        player.score_logic = participant.score_logic
        print('score logic:', player.score_logic)

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == participant.task_order['logic'] # and get_timeout_seconds(player) > 0


class InstructionsDice(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == participant.task_order['luck']


class DiceTask1(Page):
    form_model = 'player'
    form_fields = ['rolls', 'attention1']
    @staticmethod
    def vars_for_template(player: Player):
        if not player.field_maybe_none('rolls'):
            player.rolls = json.dumps([])  # Initialize as empty list
        return {}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.rolls:
            player.rolls = json.dumps(player.rolls)
        print('rolls:', player.rolls)
        player.score_luck = 0
        import ast
        player.rolls = ast.literal_eval(player.rolls)
        print('rolls:', player.rolls)
        # determine type of player.rolls
        for i in range(len(player.rolls)):
            if player.rolls[i] == "6":
                player.score_luck += 2
            elif player.rolls[i] == "5":
                player.score_luck += 1
        participant = player.participant
        if player.round_number == participant.task_order['luck']:
            participant.score_luck = player.score_luck
            print('score luck:', participant.score_luck)
        if player.attention1 != "strongly disagree":
            player.attention1_passed = False


    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == participant.task_order['luck']



class Background(Page):
    form_model = 'player'
    form_fields = ['pagetime_background', 'focus_data_background', 'background_click_example', 'background_time_example']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player):
        participant = player.participant
        ingroup_ref = participant.group_ref_background
        outgroup_ref = "Democrat" if ingroup_ref == "Republican" else "Republican"
        return {
            'ingroup_ref': ingroup_ref,
            'outgroup_ref': outgroup_ref,
        }


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import json
        raw = player.focus_data_background or ""
        try:
            events = json.loads(raw) if raw else []
            if not isinstance(events, list):
                events = []
        except (ValueError, TypeError):
            events = []

        total_unfocused = sum(e.get('unfocused_duration_ms', 0) for e in events)
        player.unfocused_background = total_unfocused / 1000

        print(f"{player.participant.code} unfocused for {total_unfocused / 1000:.1f}s")
        print(events)




page_sequence = [InstructionsLogic, LogicTask1, LogicTask2, LogicTask3, LogicTask4, LogicTask5, LogicTask6, # LogicTask7, LogicTask8,
                                 InstructionsDice, DiceTask1, Background]

