from os import environ

SESSION_CONFIGS = [
    #dict(
     #    name='TEST',
      #   app_sequence=['welcome', 'instructions', 'groupassignment', 'task_main',
       #                'prior_beliefs_old', 'feedback',
        #               'recall_beliefs', 'groupiness_part2', 'survey_main'],
         #num_demo_participants=20,
     #),
    dict(
        name='pre_experiment',
        display_name='pre_experiment',
        num_demo_participants=20,
        app_sequence=['pre_intro', 'task_pre', 'pre_survey'],
    ),
    dict(
        name='main_part1',
         app_sequence=['welcome', 'instructions', 'groupassignment', 'groupidentification', 'task_main',# 'task_logic','task_knowledge', 'task_verbal',
                       'prior_beliefs', 'feedback', 'post_beliefs', 'part1_end'],
         num_demo_participants=20,
     ),
    #dict(
     #   name='part1_self',
      #   app_sequence=['welcome', 'instructions', 'groupassignment', 'task_main',# 'task_logic','task_knowledge', 'task_verbal',
       #                'self_confidence', 'prior_beliefs_old', 'feedback', 'post_beliefs_old', 'self_confidence_direct', 'survey_direct', 'part1_end'],
        # num_demo_participants=20,
     #),
#    dict(
 #       name='part1_beliefs',
  #      app_sequence=['welcome', 'instructions', 'groupassignment', 'prior_beliefs_old', 'feedback', 'post_beliefs_old',
  #                     'survey_direct', 'part1_end'],
   #     num_demo_participants=20,
  #  ),
    dict(
        name='main_part2',
        app_sequence=['recall_beliefs','groupiness_part2', 'self_confidence_post', 'survey_main'], #self_confidence?
        num_demo_participants=20,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']


ROOMS = [
    dict(
        name='pilot',
        display_name='pilot',
        # participant_label_file='_rooms/your_study.txt',
        # use_secure_urls=True,
    ),
    dict(
        name='main',
        display_name='main',
    )
]


SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['test_id', 'id_worked',
                      'treatment', 'group', 'outgroup', 'group_state', 'order_venn',
                      'belief_ref', 'group_ref_background',
                      'task_rounds', 'treat_first', 'task_order',
                        'task1', 'task2',
                      'score_logic', 'score_luck',
                      'expiry',
                      'beliefs_example_order',
                      'prior_sel_q', 'prior_bonus',
                        'post_sel_q', 'post_bonus',
                      'post2_logic_lb', 'post2_logic_ub', 'post2_effort_lb','post2_effort_ub', 'post2_luck_lb', 'post2_luck_ub',
                        'prob_logic_post2', 'prob_effort_post2', 'prob_luck_post2',
                        'post2_first', 'post2_second', 'post2_third',
                        'post2_sel_q', 'post2_bonus',
                      'post2_prob_path_logic', 'post2_prob_path_effort', 'post2_prob_path_luck',
                       'sample1_r1', 'sample2_r1', 'sample1_r2', 'sample2_r2',
                      'r1_sign', 'r2_sign', 'signals_pos', 'signals_neg',
                      'logic_result', 'luck_result',
                      'logic_sign_shown', 'luck_sign_shown',
                        'group2', 'outgroup2', 'group_state2',
                      'recall_logic', 'recall_effort', 'recall_luck',
                      'recall_logic_correct', 'recall_effort_correct', 'recall_luck_correct',
                      'recall_sel_q', 'recall_bonus',
                  ]
SESSION_FIELDS = ['params']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '2521714225624'
