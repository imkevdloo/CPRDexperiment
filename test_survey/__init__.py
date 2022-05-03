import random

from otree.api import *


doc = """
Concluding survey of the experiment
"""


class Constants(BaseConstants):
    name_in_url = 'test_survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label="Please enter your age:", min=18, max=100)
    gender = models.IntegerField(
        choices=[
        [1, 'Female'],
        [2, 'Male'],
        [3, 'Non-binary'],
        [4, 'Prefer not to say'],
        [5, 'Other']
        ],
        label="Please select your gender:",
        )
    nationality = models.StringField(label="Please enter your nationality:")
    education = models.IntegerField(
        choices=[
        [1, 'Primary school'],
        [2, 'High school or equivalent'],
        [3, 'Bachelor degree'],
        [4, 'Master degree'],
        [5, 'PhD or Doctorate degree'],
        [6, 'Other']
        ],
        label="What is the highest level of education that you have completed?:",
        )
    occupation = models.IntegerField(
        choices=[
        [1, 'Student'],
        [2, 'Working'],
        [3, 'Other'],
        ],
        label="Which of the following best describes your current employment situation?:",
        )
    environment_knowledge = models.IntegerField(
        choices=[
        [1, 'Very high'],
        [2, 'Above average'],
        [3, 'Average'],
        [4, 'Below average'],
        [5, 'Very low']
        ],
        label="My knowledge about the environment is:",
        #widget=widgets.RadioSelect
        )
    deforestation_knowledge = models.IntegerField(
        choices=[
            [1, 'Very high'],
            [2, 'Above average'],
            [3, 'Average'],
            [4, 'Below average'],
            [5, 'Very low']
        ],
        label="My knowledge about deforestation is:",
        #widget=widgets.RadioSelect
    )
    environment_importance = models.IntegerField(
        choices=[
        [1, 'Very important'],
        [2, 'Important'],
        [3, 'Moderately important'],
        [4, 'Slightly important'],
        [5, 'Not important']
        ],
        label="I find the environment:",
        #widget=widgets.RadioSelect
        )
    environment_behavior = models.IntegerField(
        choices=[
            [1, 'Never'],
            [2, 'Rarely'],
            [3, 'Sometimes'],
            [4, 'Often'],
            [5, 'Always']
            ],
        label="My daily-life behaviour is environmently friendly: ",
        #widget=widgets.RadioSelect
    )
    tree_certificate = models.StringField(
        label="If you would like to receive a certificate of the trees planted, please provide your e-mail address:", blank=True)
    profit_certificate = models.StringField(
        label="If you would like participate i the lottery draw to receive your profit, please provide your e-mail address:", blank=True)
    happy_past = models.IntegerField(
        choices=[
        [1, 'Very slightly or not at all'],
        [2, 'A little'],
        [3, 'Moderately'],
        [4, 'Quite a bit'],
        [5, 'Extremely']
        ],
        label="Happy",
        )
    excited_past = models.IntegerField(
        choices=[
            [1, 'Very slightly or not at all'],
            [2, 'A little'],
            [3, 'Moderately'],
            [4, 'Quite a bit'],
            [5, 'Extremely']
        ],
        label="Excited",
    )
    enthusiastic_past = models.IntegerField(
        choices=[
            [1, 'Very slightly or not at all'],
            [2, 'A little'],
            [3, 'Moderately'],
            [4, 'Quite a bit'],
            [5, 'Extremely']
        ],
        label="Enthusiastic",
    )
    proud_past = models.IntegerField(
        choices=[
            [1, 'Very slightly or not at all'],
            [2, 'A little'],
            [3, 'Moderately'],
            [4, 'Quite a bit'],
            [5, 'Extremely']
        ],
        label="Proud",
    )
    inspired_past = models.IntegerField(
        choices=[
            [1, 'Very slightly or not at all'],
            [2, 'A little'],
            [3, 'Moderately'],
            [4, 'Quite a bit'],
            [5, 'Extremely']
        ],
        label="Inspired",
    )
    sad_past = models.IntegerField(
        choices=[
            [1, 'Very slightly or not at all'],
            [2, 'A little'],
            [3, 'Moderately'],
            [4, 'Quite a bit'],
            [5, 'Extremely']
        ],
        label="Sad",
    )
    afraid_past = models.IntegerField(
        choices=[
            [1, 'Very slightly or not at all'],
            [2, 'A little'],
            [3, 'Moderately'],
            [4, 'Quite a bit'],
            [5, 'Extremely']
        ],
        label="Afraid",
    )
    angry_past = models.IntegerField(
        choices=[
            [1, 'Very slightly or not at all'],
            [2, 'A little'],
            [3, 'Moderately'],
            [4, 'Quite a bit'],
            [5, 'Extremely']
        ],
        label="Angry",
    )
    ashamed_past = models.IntegerField(
        choices=[
            [1, 'Very slightly or not at all'],
            [2, 'A little'],
            [3, 'Moderately'],
            [4, 'Quite a bit'],
            [5, 'Extremely']
        ],
        label="Ashamed",
    )
    anxious_past = models.IntegerField(
        choices=[
            [1, 'Very slightly or not at all'],
            [2, 'A little'],
            [3, 'Moderately'],
            [4, 'Quite a bit'],
            [5, 'Extremely']
        ],
        label="Anxious",
    )
    happy_during = models.IntegerField(
        choices=[
        [1, 'Very slightly or not at all'],
        [2, 'A little'],
        [3, 'Moderately'],
        [4, 'Quite a bit'],
        [5, 'Extremely']
        ],
        label="Happy",
        )
    excited_during = models.IntegerField(
        choices=[
            [1, 'Very slightly or not at all'],
            [2, 'A little'],
            [3, 'Moderately'],
            [4, 'Quite a bit'],
            [5, 'Extremely']
        ],
        label="Excited",
    )
    enthusiastic_during = models.IntegerField(
        choices=[
            [1, 'Very slightly or not at all'],
            [2, 'A little'],
            [3, 'Moderately'],
            [4, 'Quite a bit'],
            [5, 'Extremely']
        ],
        label="Enthusiastic",
    )
    proud_during = models.IntegerField(
        choices=[
            [1, 'Very slightly or not at all'],
            [2, 'A little'],
            [3, 'Moderately'],
            [4, 'Quite a bit'],
            [5, 'Extremely']
        ],
        label="Proud",
    )
    inspired_during = models.IntegerField(
        choices=[
            [1, 'Very slightly or ot at all'],
            [2, 'A little'],
            [3, 'Moderately'],
            [4, 'Quite a bit'],
            [5, 'Extremely']
        ],
        label="Inspired",
    )
    sad_during = models.IntegerField(
        choices=[
            [1, 'Very slightly or not at all'],
            [2, 'A little'],
            [3, 'Moderately'],
            [4, 'Quite a bit'],
            [5, 'Extremely']
        ],
        label="Sad",
    )
    afraid_during = models.IntegerField(
        choices=[
            [1, 'Very slightly or not at all'],
            [2, 'A little'],
            [3, 'Moderately'],
            [4, 'Quite a bit'],
            [5, 'Extremely']
        ],
        label="Afraid",
    )
    angry_during = models.IntegerField(
        choices=[
            [1, 'Very slightly or not at all'],
            [2, 'A little'],
            [3, 'Moderately'],
            [4, 'Quite a bit'],
            [5, 'Extremely']
        ],
        label="Angry",
    )
    ashamed_during = models.IntegerField(
        choices=[
            [1, 'Very slightly or not at all'],
            [2, 'A little'],
            [3, 'Moderately'],
            [4, 'Quite a bit'],
            [5, 'Extremely']
        ],
        label="Ashamed",
    )
    anxious_during = models.IntegerField(
        choices=[
            [1, 'Very slightly or not at all'],
            [2, 'A little'],
            [3, 'Moderately'],
            [4, 'Quite a bit'],
            [5, 'Extremely']
        ],
        label="Anxious",
    )
    comments = models.StringField(
        label="If you have any comments on the experiment, you can leave them here:", blank=True)
    decision_info = models.IntegerField(
        choices=[
                [1, 'own points'],
            [2, 'other participants behavior'],
            [3, 'how many trees were left'],
            
        ],
        label="What information was most important for you?",
    )
    effect_sustainable = models.IntegerField(
        choices=[
                [1, 'yes'],
            [2, 'sometimes'],
            [3, 'no'],
            
        ],
        label="Did you try to be sustainable (try not to cut down more than 10 trees)?",
    )
    effect_label = models.IntegerField(
        choices=[
                [1, 'yes'],
            [2, 'sometimes'],
            [3, 'no'],
            
        ],
        label="Did the eco-label affect your choices?",
     )
    multiplier_eco = models.FloatField(
        label="At which multiplier would you have tried to keep the eco-label?", blank=False)

    read_politics = models.IntegerField(
        choices=[
              [1, 'Never'],
            [2, 'Rarely'],
            [3, 'Sometimes'],
            [4, 'Often'],
            [5, 'Always']
        ],
        label="How often do you read up on politics?",
     )
    spectrum_politics = models.IntegerField(
        choices=[
              [1, 'Left'],
            [2, 'In between left and center'],
            [3, 'center'],
            [4, 'In between right and center'],
            [5, 'Right']
        ],
        label="Where would you place yourself in the political spectrum?",
     )


# PAGES
class EndGameControl(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.treatment == 'Control_I_T' or player.participant.treatment == 'Control_I_P' or player.participant.treatment == 'Control_G_T' or player.participant.treatment == 'Control_G_P' #and (player.round_number == 10 or player.participant.forest <= 0)


class EndGameEco(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.treatment == 'SECO_I_T' or player.participant.treatment == 'SECO_I_P' or player.participant.treatment == 'SECO_G_T' or player.participant.treatment == 'SECO_G_P' #and (player.round_number == 10 or player.participant.forest <= 0)


class Decision_info_eco(Page):
    form_model = 'player'
    form_fields = ['decision_info', 'effect_label', 'multiplier_eco']

    @staticmethod
    def is_displayed(player):
        return player.participant.treatment == 'SECO_I_T' or player.participant.treatment == 'SECO_I_P' or player.participant.treatment == 'SECO_G_T' or player.participant.treatment == 'SECO_G_P' #and (player.round_number == 10 or player.participant.forest <= 0)


    @staticmethod
    def before_next_page(player, timeout_happened):
        player.decision_info = player.decision_info
        player.effect_label = player.effect_label
        player.multiplier_eco = player.multiplier_eco

class Decision_info_control(Page):
    form_model = 'player'
    form_fields = ['decision_info', 'effect_sustainable']

    @staticmethod
    def is_displayed(player):
        return player.participant.treatment == 'Control_I_T' or player.participant.treatment == 'Control_I_P' or player.participant.treatment == 'Control_G_T' or player.participant.treatment == 'Control_G_P' #and (player.round_number == 10 or player.participant.forest <= 0)


    @staticmethod
    def before_next_page(player, timeout_happened):
        player.decision_info = player.decision_info
        player.effect_sustainable = player.effect_sustainable

class EmotionsPast(Page):
    form_model = 'player'
    form_fields = ['happy_past', 'excited_past', 'enthusiastic_past', 'proud_past', 'inspired_past', 'sad_past', 'afraid_past', 'angry_past', 'ashamed_past', 'anxious_past']
    #random.shuffle(form_fields)

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.happy_past = player.happy_past
        player.excited_past = player.excited_past
        player.enthusiastic_past = player.enthusiastic_past
        player.proud_past = player.proud_past
        player.inspired_past = player.inspired_past
        player.sad_past = player.sad_past
        player.afraid_past = player.afraid_past
        player.angry_past = player.angry_past
        player.ashamed_past = player.ashamed_past
        player.anxious_past = player.anxious_past

class EmotionsDuring(Page):
    form_model = 'player'
    form_fields = ['happy_during', 'excited_during', 'enthusiastic_during', 'proud_during', 'inspired_during', 'sad_during', 'afraid_during', 'angry_during', 'ashamed_during', 'anxious_during']
    #random.shuffle(form_fields)

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.happy_during = player.happy_during
        player.excited_during = player.excited_during
        player.enthusiastic_during = player.enthusiastic_during
        player.proud_during = player.proud_during
        player.inspired_during = player.inspired_during
        player.sad_during = player.sad_during
        player.afraid_during = player.afraid_during
        player.angry_during = player.angry_during
        player.ashamed_during = player.ashamed_during
        player.anxious_during = player.anxious_during


class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['environment_knowledge', 'deforestation_knowledge', 'environment_importance', 'environment_behavior', 'read_politics', 'spectrum_politics']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.environment_knowledge = player.environment_knowledge
        player.deforestation_knowledge = player.deforestation_knowledge
        player.environment_importance = player.environment_importance
        player.environment_behavior = player.environment_behavior
        player.read_politics = player.read_politics
        player.spectrum_politics = player.spectrum_politics


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'nationality', 'gender', 'education', 'occupation', 'tree_certificate', 'profit_certificate', 'comments']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.age = player.age
        player.nationality = player.nationality
        player.gender = player.gender
        player.education = player.education
        player.occupation = player.occupation
        player.tree_certificate = player.tree_certificate
        player.profit_certificate = player.profit_certificate
        player.comments = player.comments



class Thankyou(Page):
    pass


page_sequence = [EndGameControl, EndGameEco, Decision_info_eco, Decision_info_control, EmotionsPast, EmotionsDuring, Questionnaire, Demographics, Thankyou]
