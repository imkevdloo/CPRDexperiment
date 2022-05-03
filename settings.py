from os import environ

SESSION_CONFIGS = [
    dict(
        name='test_crsd',
        app_sequence=['test_instructions', 'test_crsd', 'test_survey'],
        num_demo_participants=1,
    ),

]

ROOMS = [
    dict(
        name='PSY2022',
        display_name='MSc Psychology Thesis Experiment',
        #use_secure_urls=True
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['treatment', 'trees_player_round', 'eco_status', 'trees_player_total', 'trees_p2', 'trees_p3', 'trees_p4', 'trees_group_round', 'trees_group_total',
                        'forest', 'points_player_round', 'points_player_total', 'points_group_round', 'points_group_total', 'eco_status_p2', 'eco_status_p3', 'eco_status_p4', 'eco_labels_total', 'game_over', 'sButtonClick', 'sTimeClick', 'profit_player_total']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'LizzyDRB'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = 'LizzyDRBoTree'

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '1085033898779'

EXTENSION_APPS = ['otree_tools']
