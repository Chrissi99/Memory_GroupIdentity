from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'survey_direct'
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
    """ --> reinclude if sample feedback; maybe change: beliefs about true news/ fake news scoure
    feedback_trust = models.StringField(
        choices=["yes", "no", "I don't know"],
        label="Do you think that the information you received on the teams' performances in the three competitions was true?",
        widget=widgets.RadioSelect,
        # open free text if "no" is clicked?
        # problem: no could be part of motivated reasoning?
    )
    """
    # for testing:
    #understand = models.LongStringField(initial = None,
     #                                   blank=True,
      #                                  verbose_name="Did you understand the instructions? If not, what was unclear?")
    #beliefs_decision = models.LongStringField(initial=None,
     #                                       blank=True,
      #                                      verbose_name="In block 4 and 5 where you had to choose several times between the lottery "
       #                                                  "and the team competition for the chance of receiving $1: How did "
        #                                                    "you decide which option to choose?")
    purpose = models.LongStringField(initial=None,
                                     blank=True,
                                     verbose_name="What do you think this study is about?")
    comment = models.LongStringField(initial=None,
                                     blank=True,
                                     verbose_name="Do you have any further comments?")


# PAGES
class SurveyDirect(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'race', 'education', 'risk_aversion','competitiveness', 'SOI',
                   #'understand',
                  # 'beliefs_decision',
                    'purpose', 'comment']

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return participant.treatment == "BeliefsNoMemory"


class ThankYou(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return participant.treatment == "BeliefsNoMemory"


page_sequence = [SurveyDirect, ThankYou]
