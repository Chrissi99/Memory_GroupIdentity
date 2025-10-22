from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'post_beliefs_old'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 18
    ROUNDS_P_Q = 6
    NUM_TASKS = 3
    NUM_TASKS_W = "three"
    TASKS_SEC = "two"
    NUM_GROUPMEMBERS = 6
    NUM_MEMBERS_W = "six"
    NUM_QUESTIONS = 8
    MAX_DIST_ABS = 5
    BONUS_ABS = "0.50"
    BONUS_REL = 1
    MAX_TOTAL_GROUP = NUM_GROUPMEMBERS * NUM_QUESTIONS
    BREAK_DURATION = 'one week'
    one_up_two_down = [99, 93, 87, 81, 67, 61, 55, 49, 43, 37, 31, 17, 11, 5]
    two_up_one_down = [95, 89, 83, 69, 63, 57, 51, 45, 39, 33, 19, 13, 7, 1]
    two_up_two_down = [77, 73, 27, 23]
    EXAMPLE_CHECK_1 = "70%"
    EXAMPLE_CHECK_2 = "30%"
    BELIEFS_CHECK_ANSWER = 'Option B'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    choice_logic_post = models.StringField(choices=['Lottery', 'Team Competition'],
                                      widget=widgets.RadioSelect,
                                      verbose_name="",
                                        blank=True,
                                      )
    #prob_logic_post = models.IntegerField(initial=50)
    choice_effort_post = models.StringField(choices=['Lottery', 'Team Competition'],
                                       widget=widgets.RadioSelect,
                                       verbose_name="",
                                        blank=True,
                                       )
    #prob_effort_post = models.IntegerField(initial=50)
    choice_luck_post = models.StringField(choices=['Lottery', 'Team Competition'],
                                     widget=widgets.RadioSelect,
                                     verbose_name="",
                                      blank=True,
                                     )
    #prob_luck_post = models.IntegerField(initial=50)
    beliefs_check2 = models.StringField(verbose_name="",
                                        blank=True,
                                        )
    belief_check_attempts2 = models.IntegerField(initial=0)


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



class Beliefs_InstructionsPost(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == 1 and participant.treatment == 'BeliefsNoMemory'


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.prob_logic_post = 50
        participant.prob_effort_post = 50
        participant.prob_luck_post = 50
        participant.post_prob_path_logic = [50]
        participant.post_prob_path_effort = [50]
        participant.post_prob_path_luck = [50]
        participant.post_sel_q = random.randint(1, 18)
        print(participant.post_sel_q)


class Beliefs_Check_Post(Page):
    form_model = 'player'
    form_fields = ['beliefs_check2']

    @staticmethod
    def error_message(player, values):
        print(values['beliefs_check2'])
        if values['beliefs_check2'] == '' or values['beliefs_check2'] is None:
            return "Please answer the question."
        if values['beliefs_check2'] != C.BELIEFS_CHECK_ANSWER:
            player.belief_check_attempts2 += 1
            return "You did a mistake. Try again"


    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == 1 and participant.treatment == 'BeliefsNoMemory'


class BeliefsPostStart(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return (player.round_number == 1 or player.round_number == 7 or player.round_number == 13) and participant.treatment == 'BeliefsNoMemory'


class Beliefs_Post_Logic(Page):
    form_model = 'player'
    form_fields = ['choice_logic_post']

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        return {
            'current_probability': participant.prob_logic_post,
            'round_number': player.round_number,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        old_probability = participant.prob_logic_post
        new_probability = calculate_new_probability(participant.prob_logic_post, player.choice_logic_post, player.round_number)
        # player.prob_logic_post = new_probability
        participant.prob_logic_post = new_probability
        if player.round_number == participant.post_sel_q:
            if player.choice_logic_post == 'Lottery':
                winning_prob = round(old_probability / 100, 2)
                print(winning_prob)
                participant.post_bonus = random.choices([C.BONUS_REL, 0], weights=[winning_prob, 1 - winning_prob], k=1)[0]
            elif player.choice_logic_post == 'Team Competition':
                if participant.logic_result == '>':
                    participant.post_bonus = C.BONUS_REL
                elif participant.logic_result == '<':
                    participant.post_bonus = 0
            else:
                print('Error!')
            print("Bonus:", participant.post_bonus)
        if (player.round_number == 6 and participant.task1 == 'logic') or (player.round_number == 12 and participant.task2 == 'logic') or (player.round_number == 18 and participant.task3 == 'logic'):
            if player.choice_logic_post == 'Lottery':
                if old_probability in C.one_up_two_down:
                    participant.post_logic_ub = old_probability
                    participant.post_logic_lb = old_probability - 2
                elif old_probability in C.two_up_one_down:
                    participant.post_logic_ub = old_probability
                    participant.post_logic_lb = old_probability - 1
                elif old_probability in C.two_up_two_down:
                    participant.post_logic_ub = old_probability
                    participant.post_logic_lb = old_probability - 2
            elif player.choice_logic_post == 'Team Competition':
                if old_probability in C.one_up_two_down:
                    participant.post_logic_lb = old_probability
                    participant.post_logic_ub = old_probability + 1
                elif old_probability in C.two_up_one_down:
                    participant.post_logic_lb = old_probability
                    participant.post_logic_ub = old_probability + 2
                elif old_probability in C.two_up_two_down:
                    participant.post_logic_lb = old_probability
                    participant.post_logic_ub = old_probability + 2
            print ("Logic:", participant.post_logic_lb, participant.post_logic_ub)
        if (player.round_number <= 6 and participant.task1 == 'logic') or (7 <= player.round_number <= 12 and participant.task2 == 'logic') or (13 <= player.round_number <= 18 and participant.task3 == 'logic'):
            participant.post_prob_path_logic.append(new_probability)
            print(participant.post_prob_path_logic)


    @staticmethod
    def error_message(player: Player, values):
        if values['choice_logic_post'] is None:
            return 'Please select one of the options.'


    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.task1 == 'logic':
            return 1 <= player.round_number <= 6 and participant.treatment == 'BeliefsNoMemory'
        elif participant.task2 == 'logic':
            return 7 <= player.round_number <= 12 and participant.treatment == 'BeliefsNoMemory'
        elif participant.task3 == 'logic':
            return 13 <= player.round_number <= 18 and participant.treatment == 'BeliefsNoMemory'
        else:
            print('Error!')


class Beliefs_Post_Counting(Page):
    form_model = 'player'
    form_fields = ['choice_effort_post']

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        return {
            'current_probability': participant.prob_effort_post,
            'round_number': player.round_number,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        old_probability = participant.prob_effort_post
        new_probability = calculate_new_probability(participant.prob_effort_post, player.choice_effort_post, player.round_number)
        #player.prob_effort_post = new_probability
        participant.prob_effort_post = new_probability
        if player.round_number == participant.post_sel_q:
            if player.choice_effort_post == 'Lottery':
                winning_prob = round(old_probability / 100, 2)
                print(winning_prob)
                participant.post_bonus = random.choices([C.BONUS_REL, 0], weights=[winning_prob, 1 - winning_prob], k=1)[0]
            elif player.choice_effort_post == 'Team Competition':
                if participant.effort_result == '>':
                    participant.post_bonus = C.BONUS_REL
                elif participant.effort_result == '<':
                    participant.post_bonus = 0
            else:
                print('Error!')
            print("Bonus:", participant.post_bonus)
        if (player.round_number == 6 and participant.task1 == 'effort') or (player.round_number == 12 and participant.task2 == 'effort') or (player.round_number == 18 and participant.task3 == 'effort'):
            if player.choice_effort_post == 'Lottery':
                if old_probability in C.one_up_two_down:
                    participant.post_effort_ub = old_probability
                    participant.post_effort_lb = old_probability - 2
                elif old_probability in C.two_up_one_down:
                    participant.post_effort_ub = old_probability
                    participant.post_effort_lb = old_probability - 1
                elif old_probability in C.two_up_two_down:
                    participant.post_effort_ub = old_probability
                    participant.post_effort_lb = old_probability - 2
            elif player.choice_effort_post == 'Team Competition':
                if old_probability in C.one_up_two_down:
                    participant.post_effort_lb = old_probability
                    participant.post_effort_ub = old_probability + 1
                elif old_probability in C.two_up_one_down:
                    participant.post_effort_lb = old_probability
                    participant.post_effort_ub = old_probability + 2
                elif old_probability in C.two_up_two_down:
                    participant.post_effort_lb = old_probability
                    participant.post_effort_ub = old_probability + 2
            print ("Effort:", participant.post_effort_lb, participant.post_effort_ub)
        if (player.round_number <= 6 and participant.task1 == 'effort') or (7 <= player.round_number <= 12 and participant.task2 == 'effort') or (13 <= player.round_number <= 18 and participant.task3 == 'effort'):
            participant.post_prob_path_effort.append(new_probability)
            print(participant.post_prob_path_effort)


    @staticmethod
    def error_message(player: Player, values):
        if values['choice_effort_post'] is None:
            return 'Please select one of the options.'


    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.task1 == 'effort':
            return 1 <= player.round_number <= 6 and participant.treatment == 'BeliefsNoMemory'
        elif participant.task2 == 'effort':
            return 7 <= player.round_number <= 12 and participant.treatment == 'BeliefsNoMemory'
        elif participant.task3 == 'effort':
            return 13 <= player.round_number <= 18 and participant.treatment == 'BeliefsNoMemory'
        else:
            print('Error!')


class Beliefs_Post_Dice(Page):
    form_model = 'player'
    form_fields = ['choice_luck_post']

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        return {
            'current_probability': participant.prob_luck_post,
            'round_number': player.round_number,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        old_probability = participant.prob_luck_post
        new_probability = calculate_new_probability(participant.prob_luck_post, player.choice_luck_post, player.round_number)
        # player.prob_luck_post = new_probability
        participant.prob_luck_post = new_probability
        if player.round_number == participant.post_sel_q:
            if player.choice_luck_post == 'Lottery':
                winning_prob = round(old_probability / 100, 2)
                print(winning_prob)
                participant.post_bonus = random.choices([C.BONUS_REL, 0], weights=[winning_prob, 1 - winning_prob], k=1)[0]
            elif player.choice_luck_post == 'Team Competition':
                if participant.luck_result == '>':
                    participant.post_bonus = C.BONUS_REL
                elif participant.luck_result == '<':
                    participant.post_bonus = 0
            else:
                print('Error!')
            print("Bonus:", participant.post_bonus)
        if (player.round_number == 6 and participant.task1 == 'luck') or (player.round_number == 12 and participant.task2 == 'luck') or (player.round_number == 18 and participant.task3 == 'luck'):
            if player.choice_luck_post == 'Lottery':
                if old_probability in C.one_up_two_down:
                    participant.post_luck_ub = old_probability
                    participant.post_luck_lb = old_probability - 2
                elif old_probability in C.two_up_one_down:
                    participant.post_luck_ub = old_probability
                    participant.post_luck_lb = old_probability - 1
                elif old_probability in C.two_up_two_down:
                    participant.post_luck_ub = old_probability
                    participant.post_luck_lb = old_probability - 2
            elif player.choice_luck_post == 'Team Competition':
                if old_probability in C.one_up_two_down:
                    participant.post_luck_lb = old_probability
                    participant.post_luck_ub = old_probability + 1
                elif old_probability in C.two_up_one_down:
                    participant.post_luck_lb = old_probability
                    participant.post_luck_ub = old_probability + 2
                elif old_probability in C.two_up_two_down:
                    participant.post_luck_lb = old_probability
                    participant.post_luck_ub = old_probability + 2
            print ("Luck:", participant.post_luck_lb, participant.post_luck_ub)
        if (player.round_number <= 6 and participant.task1 == 'luck') or (7 <= player.round_number <= 12 and participant.task2 == 'luck') or (13 <= player.round_number <= 18 and participant.task3 == 'luck'):
            participant.post_prob_path_luck.append(new_probability)
            print(participant.post_prob_path_luck)


    @staticmethod
    def error_message(player: Player, values):
        if values['choice_luck_post'] is None:
            return 'Please select one of the options.'


    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.task1 == 'luck':
            return 1 <= player.round_number <= 6 and participant.treatment == 'BeliefsNoMemory'
        elif participant.task2 == 'luck':
            return 7 <= player.round_number <= 12 and participant.treatment == 'BeliefsNoMemory'
        elif participant.task3 == 'luck':
            return 13 <= player.round_number <= 18 and participant.treatment == 'BeliefsNoMemory'
        else:
            print('Error!')


page_sequence = [Beliefs_InstructionsPost, Beliefs_Check_Post, BeliefsPostStart, Beliefs_Post_Logic, Beliefs_Post_Counting, Beliefs_Post_Dice,]
    # Beliefs_Post_Switch, Beliefs_Post_Sec,
    #InstructionsPost, Beliefs_Post_Switch, Beliefs_Post_Sec,
                 #Beliefs_Post_Abs

