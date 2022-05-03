import random
import itertools

from otree.api import *

doc = """
Welcome page with consent form and instructions.
"""


class Constants(BaseConstants):
    name_in_url = 'test_instructions'
    players_per_group = None
    num_rounds = 1
    removal_decisions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    treatments = ['SECO_I_T', 'SECO_I_P', 'SECO_G_T', 'SECO_G_P', 'Control_I_T', 'Control_I_P', 'Control_G_T', 'Control_G_P']

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.IntegerField(
        choices=[
            [1, 'I consent, I would like to participate.']
        ], widget = widgets.RadioSelect)
    treatment = models.StringField()
    forest = models.IntegerField(label="How many trees are there in the forest at the start?")
    regrowth = models.IntegerField(label="How many trees will regrow at the end of a round if the forest is still alive?")
    rounds = models.IntegerField(
        choices=[
        [1, '5 rounds'],
        [2, 'it depends: either 10 or when the forest is dead'],
        [3, '10 rounds'],
        ],
        label="For how many rounds will this part last?",
        )
    rounds_example = models.IntegerField(
        choices=[
        [1, '1'],
        [2, '2'],
        [3, '3'],
        [4, '4'],
        [5, '5'],
        [6, '6'],
        [7, '7'],
        [8, '8'],
        [9, '9'],
        [10, '10'],
          ],
        label="Imagine a group of 4 participants: 2 participants always cut down 20 trees each, 1 participant always cuts down 10 trees, and the last person always cuts down 15 trees. In which round does the forest die?",
        )
    check_points = models.FloatField(label="You have removed, 15 trees in round 1, 20 trees in round 2, and 7 trees in round 3. How many points (not euros) would you have after round 3?")
    check_eco = models.IntegerField(
        choices=[
        [1, 'still have it'],
        [2, 'lost in round 5'],
        [3, 'lost in round 3'],
        ],
        label="Imagine you have removed the following number of trees: 10 trees in round 1, 5 trees in round 2, 12 trees in round 3, 10 trees in round 4, 20 trees in round 5. Do you still have the eco-label or if not, in which round did you lose it?",
        )
    trees_player_total = models.IntegerField(min=0, max=40)
    trees_group_total = models.IntegerField()
    points_player_total = models.FloatField()
    points_group_total = models.FloatField()
    eco_status = models.StringField()
    eco_status_p2 = models.StringField()
    eco_status_p3 = models.StringField()
    eco_status_p4 = models.StringField()
    practice_round = models.IntegerField(label="How many trees do you want to cut down?")


def creating_session(subsession):
    if subsession.round_number == 1:
        for player in subsession.get_players():
            participant = player.participant
            participant.treatment = random.choice(Constants.treatments) #dividing treatments
            print(participant.treatment)


# PAGES
class Welcome(Page):
    form_model = 'player'
    form_fields = ['consent']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        player.treatment = participant.treatment


class InstructionsSECO(Page):
    form_model = 'player'
    form_fields = ['forest', 'regrowth', 'rounds', 'rounds_example', 'check_points', 'check_eco']

    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return participant.treatment == 'SECO_I_T' or participant.treatment == 'SECO_I_P' or participant.treatment == 'SECO_G_T' or participant.treatment == 'SECO_G_P' #selects treatment

    @staticmethod
    def error_message(player, values):
        print('values is', values)
        if values['forest'] != 100 or values['regrowth'] != 40  or values['rounds'] != 2 or values['rounds_example'] != 3 or values['check_points'] != 42 or values['check_eco'] != 3:
            return 'One or more of your answers are not correct. Please try again!'

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.trees_player_total = 0
        player.points_player_total = 0
        player.eco_status = "Yes"
        player.eco_status_p2 = "Yes"  # participant or player?
        player.eco_status_p3 = "Yes"
        player.eco_status_p4 = "Yes"
        participant = player.participant
        participant.forest = player.forest
        participant.trees_group_total = 0
        participant.points_group_total = 0
        participant.trees_player_total = player.trees_player_total
        participant.points_player_total = player.points_player_total
        participant.eco_status = player.eco_status
        participant.eco_status_p2 = player.eco_status_p2
        participant.eco_status_p3 = player.eco_status_p3
        participant.eco_status_p4 = player.eco_status_p4
        participant.eco_labels_total = 4 #or 0?
        


class InstructionsControl(Page):
    form_model = 'player'
    form_fields = ['forest', 'regrowth', 'rounds', 'rounds_example', 'check_points']

    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return participant.treatment == 'Control_I_T' or participant.treatment == 'Control_I_P' or participant.treatment == 'Control_G_T' or participant.treatment == 'Control_G_P'  #selects treatment

    @staticmethod
    def error_message(player, values):
        print('values is', values)
        if values['forest'] != 100 or values['regrowth'] != 40  or values['rounds'] != 2 or values['rounds_example'] != 3 or values['check_points'] != 42:            return 'One or more of your answers are not correct. Please try again!'

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.trees_player_total = 0
        player.points_player_total = 0
        player.eco_status = "Yes"
        player.eco_status_p2 = "Yes"  # participant or player?
        player.eco_status_p3 = "Yes"
        player.eco_status_p4 = "Yes"
        participant = player.participant
        participant.forest = player.forest
        participant.trees_group_total = 0
        participant.points_group_total = 0
        participant.trees_player_total = player.trees_player_total
        participant.points_player_total = player.points_player_total
        participant.eco_status = player.eco_status
        participant.eco_status_p2 = player.eco_status_p2
        participant.eco_status_p3 = player.eco_status_p3
        participant.eco_status_p4 = player.eco_status_p4
        participant.eco_labels_total = 4 #or 0?

class ExampleScreen(Page):
    pass

class ExampleControlGP(Page):
    form_model = 'player'
    form_fields = ['practice_round']

    @staticmethod
    def is_displayed(player):
       participant = player.participant
       return participant.treatment == 'Control_G_P'

    @staticmethod
    def error_message(player, values):
        if values['practice_round'] not in Constants.removal_decisions:
            return 'Please fill in a number in between 0 and 20'
            #I removed an error message here, and I removed the eyetracking script in the pages

  
class ExampleControlGT(Page):
    form_model = 'player'
    form_fields = ['practice_round']

    @staticmethod
    def is_displayed(player):
       participant = player.participant
       return (participant.treatment == 'Control_G_T')

    @staticmethod
    def error_message(player, values):
        if values['practice_round'] not in Constants.removal_decisions:
            return 'Please fill in a number in between 0 and 20'


class ExampleControlIP(Page):
    form_model = 'player'
    form_fields = ['practice_round']

    @staticmethod
    def is_displayed(player):
       participant = player.participant
       return (participant.treatment == 'Control_I_P')

    @staticmethod
    def error_message(player, values):
        if values['practice_round'] not in Constants.removal_decisions:
            return 'Please fill in a number in between 0 and 20'
            #removed error message and deleted mousetracking info on pages

   
class ExampleControlIT(Page):
    form_model = 'player'
    form_fields = ['practice_round']

    @staticmethod
    def is_displayed(player):
       participant = player.participant
       return (participant.treatment == 'Control_I_T')

    @staticmethod
    def error_message(player, values):
        if values['practice_round'] not in Constants.removal_decisions:
            return 'Please fill in a number in between 0 and 20'


class ExampleEcoGP(Page):
    form_model = 'player'
    form_fields = ['practice_round'] 

    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return (participant.treatment == 'SECO_G_P')

    @staticmethod
    def error_message(player, values):
        if values['practice_round'] not in Constants.removal_decisions:
            return 'Please fill in a number in between 0 and 20'


class ExampleEcoGT(Page):
    form_model = 'player'
    form_fields = ['practice_round'] 

    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return (participant.treatment == 'SECO_G_T')

    @staticmethod
    def error_message(player, values):
        if values['practice_round'] not in Constants.removal_decisions:
            return 'Please fill in a number in between 0 and 20'


class ExampleEcoIP(Page):
    form_model = 'player'
    form_fields = ['practice_round'] 

    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return (participant.treatment == 'SECO_I_P')

    @staticmethod
    def error_message(player, values):
        if values['practice_round'] not in Constants.removal_decisions:
            return 'Please fill in a number in between 0 and 20'


class ExampleEcoIT(Page):
    form_model = 'player'
    form_fields = ['practice_round'] 

    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return (participant.treatment == 'SECO_I_T')

    @staticmethod
    def error_message(player, values):
        if values['practice_round'] not in Constants.removal_decisions:
            return 'Please fill in a number in between 0 and 20'

class StartExperiment(Page):
    pass


page_sequence = [Welcome, InstructionsSECO, InstructionsControl, ExampleScreen, ExampleControlGP, ExampleControlGT,ExampleControlIP, ExampleControlIT, ExampleEcoGP, ExampleEcoGT, ExampleEcoIP, ExampleEcoIT, StartExperiment]
