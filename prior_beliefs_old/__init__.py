from otree.api import *
import pandas as pd
import random
import json


df = pd.read_excel('_static/global/groups_scores.xlsx', keep_default_na=False, engine='openpyxl')
# df2 = pd.read_excel('_static/global/groups_scores_alt.xlsx', keep_default_na=False, engine='openpyxl')


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'prior_beliefs_old'
    PLAYERS_PER_GROUP = None
    NUM_TASKS = 3
    NUM_TASKS_W = "three"
    #NUM_ROUNDS = 18
    ROUNDS_P_Q = 6
    NUM_GROUPMEMBERS = 6
    NUM_MEMBERS_W = "six"
    NUM_QUESTIONS = 8
    MAX_DIST_ABS = 5
    BONUS_ABS = "0.50"
    BONUS_REL = 1
    NUM_SIGNALS = 3
    MAX_TOTAL_GROUP = NUM_GROUPMEMBERS*NUM_QUESTIONS
    minbelief_diff = -90
    maxbelief_diff = 90
    SAMPLE_QUESTIONS = 5
    POPULATION = "100"
    POPULATION_GROUP = "50"
    one_up_two_down = [99, 93, 87, 81, 67, 61, 55, 49, 43, 37, 31, 17, 11, 5]
    two_up_one_down = [95, 89, 83, 69, 63, 57, 51, 45, 39, 33, 19, 13, 7, 1]
    two_up_two_down = [77, 73, 27, 23]
    BELIEFS_CHECK_ANSWER = 'Option A'
    EXAMPLE_CHECK_1 = "70%"
    EXAMPLE_CHECK_2 = "30%"



class Subsession(BaseSubsession):
    pass



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    choice_logic = models.StringField(choices=['Lottery', 'Team Competition'],
                                widget=widgets.RadioSelect,
                                verbose_name="",
                                blank=True,
                                )
    #probability_logic = models.IntegerField(initial=50)
    choice_effort = models.StringField(choices=['Lottery', 'Team Competition'],
                                widget=widgets.RadioSelect,
                                verbose_name="",
                                blank = True,
                                )
    #probability_effort = models.IntegerField(initial=50)
    choice_luck = models.StringField(choices=['Lottery', 'Team Competition'],
                                widget=widgets.RadioSelect,
                                verbose_name="",
                                blank = True,
                                )
    #probability_luck = models.IntegerField(initial=50)
    beliefs_check1 = models.StringField(verbose_name="",
                                        blank = True,
                                )
    belief_check_attempts1 = models.IntegerField(initial=0)

"""
def calculate_new_probability(old_probability, choice, num_rounds):
    if num_rounds <= 6:
        adjustment = 50 / (2 ** num_rounds)
    elif 7 <= num_rounds <= 12:
        adjustment = 50 / (2 ** (num_rounds - 6))
    elif 13 <= num_rounds <= 18:
        adjustment = 50 / (2 ** (num_rounds - 12))
    if choice == 'Lottery':
        return round(old_probability - adjustment)
    elif choice == 'Team Competition':
        return round(old_probability +adjustment)
"""


# PAGES
class Beliefs_Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.probability_logic = 50
        participant.probability_effort = 50
        participant.probability_luck = 50
        participant.prior_prob_path_logic = [50]
        participant.prior_prob_path_effort = [50]
        participant.prior_prob_path_luck = [50]
        #seed = 27
        #np.random.seed(seed)
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
        sample_ing3 = ingroup.sample(n=6, replace=False)
        sample_outg3 = outgroup.sample(n=6, replace=False)
        participant.sample1_r3 = sample_ing3['score_3'].sum()
        participant.sample2_r3 = sample_outg3['score_3'].sum()
        if participant.sample1_r1 > participant.sample2_r1:
            participant.logic_result = '>'
            participant.r1_sign = random.choices(['>', '<'], weights=[0.7, 0.3], k=1)[0]    # random draw between > and <, but with 70% probability for >
        elif participant.sample1_r1 < participant.sample2_r1:
            participant.logic_result = '<'
            participant.r1_sign = random.choices(['>', '<'], weights=[0.3, 0.7], k=1)[0]
        else:
            participant.logic_result = random.choice(['>', '<'])
            participant.r1_sign = participant.logic_result
        if participant.sample1_r2 > participant.sample2_r2:
            participant.effort_result = '>'
            participant.r2_sign = random.choices(['>', '<'], weights=[0.7, 0.3], k=1)[0]
        elif participant.sample1_r2 < participant.sample2_r2:
            participant.effort_result = '<'
            participant.r2_sign = random.choices(['>', '<'], weights=[0.3, 0.7], k=1)[0]
        else:
            participant.effort_result = random.choice(['>', '<'])
            participant.r2_sign = participant.effort_result
        if participant.sample1_r3 > participant.sample2_r3:
            participant.luck_result = '>'
            participant.r3_sign = random.choices(['>', '<'], weights=[0.7, 0.3], k=1)[0]
        elif participant.sample1_r3 < participant.sample2_r3:
            participant.luck_result = '<'
            participant.r3_sign = random.choices(['>', '<'], weights=[0.3, 0.7], k=1)[0]
        else:
            participant.luck_result = random.choice(['>', '<'])
            participant.r3_sign = participant.luck_result
        print("logic:", participant.logic_result, participant.r1_sign)
        print("effort:", participant.effort_result, participant.r2_sign)
        print("luck:", participant.luck_result, participant.r3_sign)
        participant.beliefs_example_order = random.choice(['low_high', 'high_low'])
        print(participant.beliefs_example_order)


        """
        group1 = random.sample(range(1, 11), 6) # change 11 to num. of workers per group?
        group2 = random.sample(range(1, 11), 6) # change 11 to num. of workers per group?
        print(df)
        sample_df1 = df[(df['group'] == participant.group) & (df['member'].isin(group1))]
        print(sample_df1)
        sample_rows1 = sample_df1.sample(n=6)
        belief_sample1 = sample_rows1.to_dict(orient='records')
        print(belief_sample1)
        sample_df2 = df[(df['group'] == participant.outgroup) & (df['member'].isin(group2))]
        sample_rows2 = sample_df2.sample(n=6)
        belief_sample2 = sample_rows2.to_dict(orient='records')
        print(belief_sample2)
        participant.sample1_r1 = belief_sample1[0]['score_1'] + belief_sample1[1]['score_1'] + belief_sample1[2]['score_1'] + belief_sample1[3]['score_1'] + belief_sample1[4]['score_1'] + belief_sample1[5]['score_1']
        participant.sample1_r2 = belief_sample1[0]['score_2'] + belief_sample1[1]['score_2'] + belief_sample1[2]['score_2'] + belief_sample1[3]['score_2'] + belief_sample1[4]['score_2'] + belief_sample1[5]['score_2']
        participant.sample1_r3 = belief_sample1[0]['score_3'] + belief_sample1[1]['score_3'] + belief_sample1[2]['score_3'] + belief_sample1[3]['score_3'] + belief_sample1[4]['score_3'] + belief_sample1[5]['score_3']
        participant.sample2_r1 = belief_sample2[0]['score_1'] + belief_sample2[1]['score_1'] + belief_sample2[2]['score_1'] + belief_sample2[3]['score_1'] + belief_sample2[4]['score_1'] + belief_sample2[5]['score_1']
        participant.sample2_r2 = belief_sample2[0]['score_2'] + belief_sample2[1]['score_2'] + belief_sample2[2]['score_2'] + belief_sample2[3]['score_2'] + belief_sample2[4]['score_2'] + belief_sample2[5]['score_2']
        participant.sample2_r3 = belief_sample2[0]['score_3'] + belief_sample2[1]['score_3'] + belief_sample2[2]['score_3'] + belief_sample2[3]['score_3'] + belief_sample2[4]['score_3'] + belief_sample2[5]['score_3']
        print('Ingroup',  participant.sample1_r1, participant.sample1_r2, participant.sample1_r3)
        print('Outgroup', participant.sample2_r1, participant.sample2_r2, participant.sample2_r3)
        if participant.sample1_r1 > participant.sample2_r1:
            # random choice between > and <, but with 70% probability for >
            participant.r1_sign = random.choices(['>', '<'], weights=[0.7, 0.3], k=1)[0]
            participant.logic_result = '>'
            # participant.r1_sign = '>'
        elif participant.sample1_r1 < participant.sample2_r1:
            participant.r1_sign = random.choices(['>', '<'], weights=[0.3, 0.7], k=1)[0]
            participant.logic_result = '<'
            # participant.r1_sign = '<'
        else:
            # if equal: random draw between > and <
            participant.r1_sign = random.choice(['>', '<'])
            participant.logic_result = participant.r1_sign # result of competition
        if participant.sample1_r2 > participant.sample2_r2:
            participant.r2_sign = random.choices(['>', '<'], weights=[0.7, 0.3], k=1)[0]
            participant.effort_result = '>'
            # participant.r2_sign = '>'
        elif participant.sample1_r2 < participant.sample2_r2:
            participant.r2_sign = random.choices(['>', '<'], weights=[0.3, 0.7], k=1)[0]
            participant.effort_result = '<'
            # participant.r2_sign = '<'
        else:
            # if equal: random draw between > and <
            participant.r2_sign = random.choice(['>', '<'])
            participant.effort_result = participant.r2_sign
        if participant.sample1_r3 > participant.sample2_r3:
            participant.r3_sign = random.choices(['>', '<'], weights=[0.7, 0.3], k=1)[0]
            participant.luck_result = '>'
            # participant.r3_sign = '>'
        elif participant.sample1_r3 < participant.sample2_r3:
            participant.r3_sign = random.choices(['>', '<'], weights=[0.3, 0.7], k=1)[0]
            participant.luck_result = '<'
            # participant.r3_sign = '<'
        else:
            # if equal: random draw between > and <
            participant.r3_sign = random.choice(['>', '<'])
            participant.luck_result = participant.r3_sign
        print("logic:", participant.logic_result, participant.r1_sign)
        print("effort:", participant.effort_result, participant.r2_sign)
        print("luck:", participant.luck_result, participant.r3_sign)
        """

        # number of positive comparisons (>):
        signals_pos = 0
        if participant.r1_sign == '>':
            signals_pos += 1
        if participant.r2_sign == '>':
            signals_pos += 1
        if participant.r3_sign == '>':
            signals_pos += 1
        participant.signals_pos = signals_pos
        participant.signals_neg = C.NUM_SIGNALS - signals_pos
        participant.prior_sel_q = random.randint(1, 18)
        print("bonus relevant question", participant.prior_sel_q)



class Beliefs_Check(Page):
    form_model = 'player'
    form_fields = ['beliefs_check1']

    @staticmethod
    def error_message(player, values):
        print(values['beliefs_check1'])
        if values['beliefs_check1'] == '' or values['beliefs_check1'] is None:
            return "Please answer the question."
        if values['beliefs_check1'] != C.BELIEFS_CHECK_ANSWER:
            player.belief_check_attempts1 += 1
            return "You did a mistake. Try again"


    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class BeliefsStart(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 or player.round_number == 7 or player.round_number == 13



class Beliefs_Prior_Logic(Page):
    form_model = 'player'
    form_fields = ['choice_logic']

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        return {
            'current_probability': participant.probability_logic, # player.probability,
            'round_number': player.round_number,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        old_probability = participant.probability_logic
        new_probability = calculate_new_probability(participant.probability_logic, player.choice_logic, player.round_number)
        # player.probability_logic = new_probability
        participant.probability_logic = new_probability
        # print(player.probability_logic)
        if player.round_number == participant.prior_sel_q:
            if player.choice_logic == 'Lottery':
                winning_prob = round(old_probability/100,2)
                print(winning_prob)
                participant.prior_bonus = random.choices([C.BONUS_REL, 0], weights=[winning_prob, 1-winning_prob], k=1)[0]
            elif player.choice_logic == 'Team Competition':
                if participant.logic_result == '>':
                    participant.prior_bonus = C.BONUS_REL
                elif participant.logic_result == '<':
                    participant.prior_bonus = 0
            else:
                print('Error!')
            print("Bonus:", participant.prior_bonus)
        if (player.round_number == 6 and participant.task1 == 'logic') or (player.round_number == 12 and participant.task2 == 'logic') or (player.round_number == 18 and participant.task3 == 'logic'):
            if player.choice_logic == 'Lottery':
                if old_probability in C.one_up_two_down:
                    participant.prior_logic_ub = old_probability
                    participant.prior_logic_lb = old_probability - 2
                elif old_probability in C.two_up_one_down:
                    participant.prior_logic_ub = old_probability
                    participant.prior_logic_lb = old_probability - 1
                elif old_probability in C.two_up_two_down:
                    participant.prior_logic_ub = old_probability
                    participant.prior_logic_lb = old_probability - 2
            elif player.choice_logic == 'Team Competition':
                if old_probability in C.one_up_two_down:
                    participant.prior_logic_lb = old_probability
                    participant.prior_logic_ub = old_probability + 1
                elif old_probability in C.two_up_one_down:
                    participant.prior_logic_lb = old_probability
                    participant.prior_logic_ub = old_probability + 2
                elif old_probability in C.two_up_two_down:
                    participant.prior_logic_lb = old_probability
                    participant.prior_logic_ub = old_probability + 2
            print ("Logic:", participant.prior_logic_lb, participant.prior_logic_ub)
        if (player.round_number <= 6 and participant.task1 == 'logic') or (7 <= player.round_number <= 12 and participant.task2 == 'logic') or (13 <= player.round_number <= 18 and participant.task3 == 'logic'):
            participant.prior_prob_path_logic.append(new_probability)
            print(participant.prior_prob_path_logic)


    @staticmethod
    def error_message(player, values):
        print(values['choice_logic'])
        if values['choice_logic'] == '' or values['choice_logic'] is None:
            return "Please select one of the options."


    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.task1 == 'logic':
            return 1 <= player.round_number <= 6
        elif participant.task2 == 'logic':
            return 7 <= player.round_number <= 12
        elif participant.task3 == 'logic':
            return 13 <= player.round_number <= 18
        else:
            print('Error!')


class Beliefs_Prior_Counting(Page):
    form_model = 'player'
    form_fields = ['choice_effort']

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        return {
            'current_probability': participant.probability_effort, # player.probability,
            'round_number': player.round_number,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        old_probability = participant.probability_effort
        new_probability = calculate_new_probability(participant.probability_effort, player.choice_effort, player.round_number)
        # player.probability_effort = new_probability
        participant.probability_effort = new_probability
        # print(player.probability_effort)
        if participant.prior_sel_q == player.round_number:
            if player.choice_effort == 'Lottery':
                winning_prob = round(old_probability / 100, 2)
                print(winning_prob)
                participant.prior_bonus = random.choices([C.BONUS_REL, 0], weights=[winning_prob, 1 - winning_prob], k=1)[0]
            elif player.choice_effort == 'Team Competition':
                if participant.effort_result == '>':
                    participant.prior_bonus = C.BONUS_REL
                elif participant.effort_result == '<':
                    participant.prior_bonus = 0
            print("Bonus:", participant.prior_bonus)
        if (player.round_number == 6 and participant.task1 == 'effort') or (player.round_number == 12 and participant.task2 == 'effort') or (player.round_number == 18 and participant.task3 == 'effort'):
            if player.choice_effort == 'Lottery':
                if old_probability in C.one_up_two_down:
                    participant.prior_effort_ub = old_probability
                    participant.prior_effort_lb = old_probability - 2
                elif old_probability in C.two_up_one_down:
                    participant.prior_effort_ub = old_probability
                    participant.prior_effort_lb = old_probability - 1
                elif old_probability in C.two_up_two_down:
                    participant.prior_effort_ub = old_probability
                    participant.prior_effort_lb = old_probability - 2
            elif player.choice_effort == 'Team Competition':
                if old_probability in C.one_up_two_down:
                    participant.prior_effort_lb = old_probability
                    participant.prior_effort_ub = old_probability + 1
                elif old_probability in C.two_up_one_down:
                    participant.prior_effort_lb = old_probability
                    participant.prior_effort_ub = old_probability + 2
                elif old_probability in C.two_up_two_down:
                    participant.prior_effort_lb = old_probability
                    participant.prior_effort_ub = old_probability + 2
            print ("Effort:", participant.prior_effort_lb, participant.prior_effort_ub)
        if (player.round_number <= 6 and participant.task1 == 'effort') or (7 <= player.round_number <= 12 and participant.task2 == 'effort') or (13 <= player.round_number <= 18 and participant.task3 == 'effort'):
            participant.prior_prob_path_effort.append(new_probability)
            print(participant.prior_prob_path_effort)



    @staticmethod
    def error_message(player, values):
        print(values['choice_effort'])
        if values['choice_effort'] == '' or values['choice_effort'] is None:
            return "Please select one of the options."


    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.task1 == 'effort':
            return 1 <= player.round_number <= 6
        elif participant.task2 == 'effort':
            return 7 <= player.round_number <= 12
        elif participant.task3 == 'effort':
            return 13 <= player.round_number <= 18
        else:
            print('Error!')


class Beliefs_Prior_Dice(Page):
    form_model = 'player'
    form_fields = ['choice_luck']

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        return {
            'current_probability': participant.probability_luck, # player.probability,
            'round_number': player.round_number,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        old_probability = participant.probability_luck
        new_probability = calculate_new_probability(participant.probability_luck, player.choice_luck, player.round_number)
        # player.probability_luck = new_probability
        participant.probability_luck = new_probability
        # print(player.probability_luck)
        if participant.prior_sel_q == player.round_number:
            if player.choice_luck == 'Lottery':
                winning_prob = round(old_probability / 100, 2)
                print(winning_prob)
                participant.prior_bonus = random.choices([C.BONUS_REL, 0], weights=[winning_prob, 1 - winning_prob], k=1)[0]
            elif player.choice_luck == 'Team Competition':
                if participant.luck_result == '>':
                    participant.prior_bonus = C.BONUS_REL
                elif participant.luck_result == '<':
                    participant.prior_bonus = 0
            print("Bonus:", participant.prior_bonus)
        if (player.round_number == 6 and participant.task1 == 'luck') or (player.round_number == 12 and participant.task2 == 'luck') or (player.round_number == 18 and participant.task3 == 'luck'):
            if player.choice_luck == 'Lottery':
                if old_probability in C.one_up_two_down:
                    participant.prior_luck_ub = old_probability
                    participant.prior_luck_lb = old_probability - 2
                elif old_probability in C.two_up_one_down:
                    participant.prior_luck_ub = old_probability
                    participant.prior_luck_lb = old_probability - 1
                elif old_probability in C.two_up_two_down:
                    participant.prior_luck_ub = old_probability
                    participant.prior_luck_lb = old_probability - 2
            elif player.choice_luck == 'Team Competition':
                if old_probability in C.one_up_two_down:
                    participant.prior_luck_lb = old_probability
                    participant.prior_luck_ub = old_probability + 1
                elif old_probability in C.two_up_one_down:
                    participant.prior_luck_lb = old_probability
                    participant.prior_luck_ub = old_probability + 2
                elif old_probability in C.two_up_two_down:
                    participant.prior_luck_lb = old_probability
                    participant.prior_luck_ub = old_probability + 2
            print ("Luck:", participant.prior_luck_lb, participant.prior_luck_ub)
        if (player.round_number <= 6 and participant.task1 == 'luck') or (7 <= player.round_number <= 12 and participant.task2 == 'luck') or (13 <= player.round_number <= 18 and participant.task3 == 'luck'):
            participant.prior_prob_path_luck.append(new_probability)
            print(participant.prior_prob_path_luck)



    @staticmethod
    def error_message(player, values):
        print(values['choice_luck'])
        if values['choice_luck'] == '' or values['choice_luck'] is None:
            return "Please select one of the options."


    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.task1 == 'luck':
            return 1 <= player.round_number <= 6
        elif participant.task2 == 'luck':
            return 7 <= player.round_number <= 12
        elif participant.task3 == 'luck':
            return 13 <= player.round_number <= 18
        else:
            print('Error!')



page_sequence = [Beliefs_Instructions, Beliefs_Check, BeliefsStart, Beliefs_Prior_Logic, Beliefs_Prior_Counting, Beliefs_Prior_Dice,
                #Background,
                 # Beliefs_Prior_Switch,
                 # Beliefs_Prior_Abs,
                 ]
