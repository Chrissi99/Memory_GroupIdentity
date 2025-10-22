from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'pre_survey'
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
    SOI = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[['1', 'strongly agree'], ['2', 'agree'], ['3', 'neutral'],
                 ['4', 'disagree'], ['5', 'strongly disagree']],
        label="",
        blank = True,
    )
    #purpose = models.LongStringField(initial=None,
     #                                blank=True,
      #                               verbose_name="What do you think this study is about?")
    comment = models.LongStringField(initial=None,
                                     blank=True,
                                     verbose_name="Do you have any comments?")


# PAGES
class SurveyPre(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'race', 'education', 'SOI', 'comment']


class ThankYou(Page):
    pass


page_sequence = [SurveyPre, ThankYou]
