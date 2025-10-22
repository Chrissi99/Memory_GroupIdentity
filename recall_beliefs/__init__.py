from otree.api import *
import random
import pandas as pd


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'recall_beliefs'
    PLAYERS_PER_GROUP = None
    TASKS = ['RECALL', 'BELIEFS']
    # NUM_ROUNDS = len(TASKS)
    NUM_ROUNDS = 3
    NUM_Q_BELIEFS = 18
    ROUNDS_P_Q = 6
    NUM_TASKS = 2
    NUM_TASKS_W = "two"
    TASKS_SEC = "two"
    NUM_GROUPMEMBERS = 6
    NUM_MEMBERS_W = "six"
    NUM_QUESTIONS = 8
    BONUS_RECALL = "1" # or 0.5? or varying?
    BONUS_RECALL_VALUE = 1
    MAX_DIST_ABS = 5
    BONUS_ABS = "0.50"
    BONUS_REL = 1
    MAX_TOTAL_GROUP = NUM_GROUPMEMBERS * NUM_QUESTIONS
    BELIEF_SAMPLE = 3
    SAMPLE_W = "three"
    NUM_SIGNALS = 3
    SAMPLE_QUESTIONS = 5
    TOTAL_QUESTIONS = 15
    SIGNAL_ACCURACY = "70"
    SIGNAL_WRONG = "30"
    PARTS_MEMORY = "six"
    BLOCKS_FIRST = "four"
    BLOCKS_SECOND = "two"
    SIGNAL_ACC_FQ = 2
    SIGNAL_TOT_FQ = 3
    SIGNAL_WRONG_FQ = 1
    EXAMPLE_CHECK_1 = "70%"
    EXAMPLE_CHECK_2 = "30%"
    BELIEFS_CHECK_ANSWER = 'Option B'
    PRIZE = 2
    creatures_true = 20
    creatures_false = 10


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        for p in subsession.get_players():
            participant = p.participant
            df_id = pd.read_excel('_static/global/ids_party.xlsx', keep_default_na=False, engine='openpyxl')


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    recall_logic = models.StringField(
        label='',
        blank=True,
    )
    recall_luck = models.StringField(
        label='',
        blank=True,
    )
    recall_confidence_logic = models.IntegerField(blank=True)
    recall_confidence_luck = models.IntegerField(blank=True)
    post_memory_logic = models.IntegerField()
    post_memory_luck = models.IntegerField()
    prolific_id = models.StringField(
        label='Before we start, please enter your Prolific ID',
        blank=True,
    )
    procedure_click_post2 = models.IntegerField(initial=0)
    procedure_time_post2 = models.FloatField(initial=0.0)
    pagetime_instr_post2 = models.FloatField(initial=0.0)
    pagetime_post2_logic = models.FloatField(initial=0.0)
    pagetime_post2_luck = models.FloatField(initial=0.0)
    pagetime_instr_recall = models.FloatField(initial=0.0)
    pagetime_recall = models.FloatField(initial=0.0)
    pagetime_recall_conf = models.FloatField(initial=0.0)



# PAGES
# ONLY FOR TESTING --> delete later
"""
class TestBreak(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == 1
"""


class WelcomeBack(Page):
    form_model = 'player'
    form_fields = ['prolific_id']

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        #if participant.label is None:
         #   df_id = pd.read_excel('_static/global/ids_party.xlsx', keep_default_na=False, engine='openpyxl')
          #  participant.label = random.choice(df_id['prolificid'].values)  # only for testing
        if participant.label is None:
            label = 0
        else:
            label = 1
        group_first = random.choice(['Democrat', 'Republican'])
        group_second = 'Democrat' if group_first == 'Republican' else 'Republican'
        return {
            'label': label,
            'group_first': group_first,
            'group_second': group_second,
        }


    @ staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        df_id = pd.read_excel('_static/global/ids_party.xlsx', keep_default_na=False, engine='openpyxl')
        if participant.label is None: # only for testing
            participant.label = player.prolific_id
            #participant.label = random.choice(df_id['prolificid'].values) # only for testing
        #   participant.label = "60385064960cdb215931ab77" # only for testing
        if participant.label in df_id['prolificid'].values:
            participant.id_worked = True
            participant.group2 = df_id[df_id['prolificid'] == participant.label]['group'].values[0]
            participant.group_state2 = df_id[df_id['prolificid'] == participant.label]['group_state'].values[0]
            participant.treatment = df_id[df_id['prolificid'] == participant.label]['treatment'].values[0]
            participant.post2_first = df_id[df_id['prolificid'] == participant.label]['task1'].values[0]
            participant.post2_second = df_id[df_id['prolificid'] == participant.label]['task2'].values[0]
            participant.logic_result = df_id[df_id['prolificid'] == participant.label]['logic_result'].values[0]
            participant.luck_result = df_id[df_id['prolificid'] == participant.label]['luck_result'].values[0]
            participant.logic_sign_shown = df_id[df_id['prolificid'] == participant.label]['logic_sign_shown'].values[0]
            participant.luck_sign_shown = df_id[df_id['prolificid'] == participant.label]['luck_sign_shown'].values[0]
            participant.beliefs_example_order = df_id[df_id['prolificid'] == participant.label]['beliefs_example_order'].values[0]
            participant.belief_ref = df_id[df_id['prolificid'] == participant.label]['belief_ref'].values[0]
        else:
            participant.id_worked = False
            participant.group2 = random.choice(['Democrat', 'Republican'])
            participant.group_state2 = random.choice(['strong', 'weak'])
            participant.treatment = random.choice(['BeliefsMemory', 'Recall'])
            post2 = ["logic", "luck"]
            random.shuffle(post2)
            participant.post2_first = post2[0]
            participant.post2_second = post2[1]
            participant.logic_result = random.choice([">", "<"])
            participant.luck_result = random.choice([">", "<"])
            participant.logic_sign_shown = random.choice([">", "<"])
            participant.luck_sign_shown = random.choice([">", "<"])
            participant.beliefs_example_order = random.choice(["high_low", "low_high"])
            participant.belief_ref = random.choice(["ingroup", "outgroup"])
        participant.treat_first = 'RECALL' if participant.treatment == 'Recall' else 'BELIEFS'
        print('treat_first is', participant.treat_first)
        participant.outgroup2 = 'Democrat' if participant.group2 == 'Republican' else 'Republican'
        print(participant.group2, participant.outgroup2)
        print(participant.id_worked)
        print(participant.group_state2)
        # print(participant.label)
        print("results tests:", participant.logic_result, participant.luck_result)
        print("order of tasks:", participant.post2_first, participant.post2_second)
        print("signs of rounds:", participant.logic_sign_shown, participant.luck_sign_shown)
        # recall_sel_q: random choice between logic, luck
        participant.recall_sel_q = random.choice(['logic', 'luck'])
        print("recall bonus relevant:", participant.recall_sel_q)
        print("belief_ref is", participant.belief_ref)


    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == 1


class InstructionsRecall(Page):
    form_model = 'player'
    form_fields = ['pagetime_instr_recall']

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.treat_first == 'RECALL':
            return player.round_number == 1
        elif participant.treat_first == 'BELIEFS':
            return player.round_number == C.NUM_ROUNDS
        else:
            print('Error!')
        # return player.round_number == participant.task_rounds['RECALL']


class Recall(Page):
    form_model = 'player'
    form_fields = ['recall_logic', 'recall_luck', 'pagetime_recall']

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.treat_first == 'RECALL':
            return player.round_number == 1
        elif participant.treat_first == 'BELIEFS':
            return player.round_number == C.NUM_ROUNDS
        else:
            print('Error!')
        # return player.round_number == participant.task_rounds['RECALL']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.recall_logic = player.recall_logic
        participant.recall_luck = player.recall_luck
        print('recall_logic is', player.recall_logic)
        print('recall_luck is', player.recall_luck)
        if player.recall_logic == participant.logic_sign_shown:
            participant.recall_logic_correct = 1
            if participant.recall_sel_q == 'logic':
                participant.recall_bonus = C.BONUS_RECALL_VALUE
        else:
            participant.recall_logic_correct = 0
            if participant.recall_sel_q == 'logic':
                participant.recall_bonus = 0
        if player.recall_luck == participant.luck_sign_shown:
            participant.recall_luck_correct = 1
            if participant.recall_sel_q == 'luck':
                participant.recall_bonus = C.BONUS_RECALL_VALUE
        else:
            participant.recall_luck_correct = 0
            if participant.recall_sel_q == 'luck':
                participant.recall_bonus = 0
        print('recall_logic_correct is', participant.recall_logic_correct)
        print('recall_luck_correct is', participant.recall_luck_correct)
        print('recall_bonus is', participant.recall_bonus)


    @staticmethod
    def error_message(player: Player, values):
        if values['recall_logic'] is None or values['recall_luck'] is None:
            return 'Please answer all questions.'
        if not values['recall_logic'] or not values['recall_luck']:
            return 'Please answer all questions.'



class RecallCon(Page):
    form_model = 'player'
    form_fields = ['recall_confidence_logic', 'recall_confidence_luck', 'pagetime_recall_conf']

    @staticmethod
    def vars_for_template(player):
        participant = player.participant
        recall_NA_all = False
        recall_NA_some = False
        if participant.recall_logic == "?" and participant.recall_luck == "?":
            recall_NA_all = True
        if (participant.recall_logic == "?" or participant.recall_luck == "?") and recall_NA_all == False:
            recall_NA_some = True
        return {
            'recall_logic': participant.recall_logic,
            'recall_luck': participant.recall_luck,
            'recall_NA_all': recall_NA_all,
            'recall_NA_some': recall_NA_some,
        }

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.treat_first == 'RECALL':
            if participant.recall_logic == "?" and participant.recall_luck == "?":
                print("page not displayed")
            else:
                return player.round_number == 1
        elif participant.treat_first == 'BELIEFS':
            if player.round_number == C.NUM_ROUNDS:
                if participant.recall_logic == "?" and participant.recall_luck == "?":
                    print("page not displayed")
                else:
                    return player.round_number == C.NUM_ROUNDS
            else:
                print('round1')
        else:
            print('Error!')


class Beliefs_InstructionsPost2(Page):
    form_model = 'player'
    form_fields = ['procedure_click_post2', 'procedure_time_post2', 'pagetime_instr_post2']

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.treat_first == 'RECALL':
            return player.round_number == 2
        elif participant.treat_first == 'BELIEFS':
            return player.round_number == 1
        else:
            print('Error!')


class Post2Logic(Page):
    form_model = 'player'
    form_fields = ['post_memory_logic', 'pagetime_post2_logic']

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.treat_first == "BELIEFS":
            if participant.post2_first == 'logic':
                return player.round_number == 1
            elif participant.post2_second == 'logic':
                return player.round_number == 2
        elif participant.treat_first == "RECALL":
            if participant.post2_first == 'logic':
                return player.round_number == 2
            elif participant.post2_second == 'logic':
                return player.round_number == C.NUM_ROUNDS
        else:
            print('Error!')

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        if participant.belief_ref == "outgroup":
            player.post_memory_logic = 100 - player.post_memory_logic




class Post2Luck(Page):
    form_model = 'player'
    form_fields = ['post_memory_luck', 'pagetime_post2_luck']

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.treat_first == "BELIEFS":
            if participant.post2_first == 'luck':
                return player.round_number == 1
            elif participant.post2_second == 'luck':
                return player.round_number == 2
        elif participant.treat_first == "RECALL":
            if participant.post2_first == 'luck':
                return player.round_number == 2
            elif participant.post2_second == 'luck':
                return player.round_number == C.NUM_ROUNDS
        else:
            print('Error!')

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        if participant.belief_ref == "outgroup":
            player.post_memory_luck = 100 - player.post_memory_luck




page_sequence = [WelcomeBack, InstructionsRecall, Recall, RecallCon, Beliefs_InstructionsPost2, Post2Logic, Post2Luck]
#[TestBreak] for testing