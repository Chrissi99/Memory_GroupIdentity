from otree.api import *
import random
import json


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label="How old are you?")
    gender = models.StringField(
        choices=[[0, 'male'], [1, 'female'], [2, 'other'], [3, 'prefer not to say']],
        label='What is your gender?',
        widget=widgets.RadioSelect,
    )
    race = models.StringField(
        choices=["Hispanic or Latin", "Asian", "White", "Black or African American",
                 "other / prefer not to answer"],
                label='What is your ethnic group?',
        widgets=widgets.RadioSelect,
    )
    education = models.IntegerField(
        choices=[[0, 'did not graduate high school'], [1, 'High school or GED'], [2, 'began college, no degree yet'],
                 [3, 'Bachelor'], [4, 'Associate'], [5, 'Master'], [6, 'Doctoral'], [7, 'other']],
        label='What is the highest level of education you have completed?',
        widgets=widgets.RadioSelect,
    )
    """
    gpa_highschool = models.FloatField(
        label='What is your (current/ final) high school GPA?',
        blank=True,
    )
    gpa_college = models.FloatField(
        label='If applicable, what is your (current/ final) college GPA?',
        blank=True,
    )
    """
    # reinclude if not political party groups
    """
    political_affiliation = models.StringField(initial=None)
    political_orientation = models.IntegerField(
        choices=[[0, 'Democrat'], [1, 'Republican']],
        label='Which direction would you prefer if you had to vote today?',
        widget=widgets.RadioSelectHorizontal(),
        blank=True,
    )
    """
    risk_aversion = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[['1', '...strongly dislike risks.'], ['2', '...rather avoid risks.'], ['3', '...am neutral.'],
                 ['4', '...rather like risks.'], ['5', '...strongly like risks.']],
        label='',
    )
    competitiveness = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[['1', '...strongly dislike competitive situations'], ['2', '...rather avoid competitive situations'],
                    ['3', '...am neutral.'], ['4', '...rather like competitive situations'],
                    ['5', '...strongly like competitive situations']],
        label='',
    )
    SOI = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[['1', 'strongly agree'], ['2', 'agree'], ['3', 'neutral'],
                 ['4', 'disagree'], ['5', 'strongly disagree']],
        label="",
        blank = True,
    )
    information_search = models.StringField(
        choices=["yes", "no"],
        label="Between the two parts, did you search for information on the general performance of Democrats and Republicans in such tasks?",
        widget=widgets.RadioSelect,
    )
    information_source = models.LongStringField(
        label="Where did you search for information?",
        blank=True,
    )
    """
    feedback_trust = models.StringField(
        choices=["yes", "no", "I don't know"],
        label="Do you think that the information you received on the teams' performances in the three competitions was true?",
        widget=widgets.RadioSelect,
        # open free text if "no" is clicked?
        # problem: no could be part of motivated reasoning?
    )
    """
    # for testing:
    """
    recall_memory = models.StringField(initial = None,
                                blank=True,
                                choices = ["totally sure", "relatively sure", "quite uncertain",
                                           "I remembered the number of '>' and '<' signs, but not in which task",
                                           "I have guessed",
                                           ],
                                verbose_name="How sure are you that you have correctly recalled the three pieces of information from part I (i.e., the >/< "
                                             "signs for the three team competitions)?"
                                )
    """
    memory = models.StringField(initial = None,
                                # blank=True,
                                choices = ["I remember everything", "I remember most of it", "I remember it roughly, but not in detail",
                                           " I remember only a few things", "I don't remember anything at all"],
                                verbose_name="How well do you remember part I of the study (from four days ago) in general?"
                                )
    #understand = models.LongStringField(initial=None,
     #                               blank=True,
      #                              verbose_name="Did you understand the instructions? If not, what was unclear?")
    purpose = models.LongStringField(initial=None,
                                     blank=True,
                                     verbose_name="What do you think this study is about?")
    pasteAttempts = models.IntegerField(initial=0)
    comment = models.LongStringField(initial=None,
                                     blank=True,
                                     verbose_name="Do you have any further comments?")
    #logic_weight = models.IntegerField(label="")
    #effort_weight = models.IntegerField(label="")
    #luck_weight = models.IntegerField(label="")
    #order_domain_weights = models.StringField()
    attention_check = models.StringField(
        initial=None,
        choices=[
            ['false1', 'blue'], ['true', 'orange'], ['false2', 'red'], ['false3', 'yellow'], ['false4', 'green'],
            ['false5', 'black']
        ],
        label='It is important for us that you pay attention. To demonstrate this, please select the second option from the list below.',
        widget=widgets.RadioSelect(),
    )
    effort_report = models.StringField(
        initial=None,
        label='Honestly, did you really pay attention and make an effort to complete the study, or were you distracted by your surroundings, media, or other things going on around you? (You will get credit for this study no matter what, so please answer truthfully).',
        choices=[
            [1, "I was very distracted, didn't focus much on the study."],
            [2, 'I was a bit distracted.'],
            [3, 'I was largely focused, with a few minor distractions.'],
            [4, 'I was fully focused, no distractions at all.']
        ])
    pagetime_survey = models.FloatField(initial=0.0)
    unfocused_survey = models.FloatField(initial=0.0)
    focus_data_survey = models.LongStringField(blank=True)


# PAGES
"""
class Domains(Page):
    form_model = 'player'
    form_fields = ['logic_weight', 'effort_weight', 'luck_weight']

    @staticmethod
    def vars_for_template(player):
        domains = ['logic', 'effort', 'luck']
        random.shuffle(domains)
        player.order_domain_weights = json.dumps(domains)
        return {
            'domain1': domains[0],
            'domain2': domains[1],
            'domain3': domains[2],
        }

    @staticmethod
    def error_message(player, values):
        if values['logic_weight'] + values['effort_weight'] + values['luck_weight'] != 100:
            return 'The weights must add up to 100.'
        if values['logic_weight'] < 0 or values['effort_weight'] < 0 or values['luck_weight'] < 0:
            return 'Weights cannot be negative.'
"""


class Survey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'race', 'education', 'risk_aversion', 'competitiveness', 'SOI',
                   #'political_affiliation', 'political_orientation','feedback_trust',
                   'information_search', 'information_source',
                    'memory', #'understand', 'recall_memory'
                    'purpose', 'comment', 'attention_check', 'effort_report', 'pasteAttempts', 'pagetime_survey', 'focus_data_survey']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import json
        raw = player.focus_data_survey or ""
        try:
            events = json.loads(raw) if raw else []
            if not isinstance(events, list):
                events = []
        except (ValueError, TypeError):
            events = []
        total_unfocused = sum(e.get('unfocused_duration_ms', 0) for e in events)
        player.unfocused_survey = total_unfocused / 1000
        print(f"{player.participant.code} unfocused for {total_unfocused / 1000:.1f}s")


    #@staticmethod
    #def error_message(player, values):
     #   print('values is', values)
      #  if values['political_orientation'] == None and values['political_affiliation'] == 2:
       #     return 'Please choose your political orientation if you are independent'


class ThankYou(Page):
    pass


page_sequence = [Survey, ThankYou]
