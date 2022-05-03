import random

from otree.api import *
from otree.models import player
import itertools

doc = """
Test CRSD
"""


class Constants(BaseConstants):
    name_in_url = 'test_crsd'
    players_per_group = None
    num_rounds = 10
    regrowth_rate = 40
    removal_decisions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] #extra for conditional?
    sustainable_decisions = [5, 6, 7 , 8, 9, 10]   #8 vs 9 
    not_sustainable_decisions = [15, 16, 17, 18, 19, 20] #18 vs 19
    treatments = ['SECO_I_T', 'SECO_I_P', 'SECO_G_T', 'SECO_G_P', 'Control_I_T', 'Control_I_P', 'Control_G_T', 'Control_G_P']


class Subsession(BaseSubsession): 
    pass #change treatments here, or change the picture per participant.


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment               = models.CharField()
    trees_player_round      = models.IntegerField(label="How many trees do you want to cut down?") # Number of trees cut down in that round of player
    eco_status              = models.StringField() # Whether trees_player_round satisfies sustainability/eco-label standards
    trees_player_total      = models.IntegerField(min=0, max=200)  # Total accumulated number of trees cut down of player
    trees_p2                = models.IntegerField(min=0, max=20) # Trees cut down p2 (always sustainable)
    trees_p3                = models.IntegerField(min=0, max=20) # Trees cut down p3 (depends on rest of group)
    trees_p4                = models.IntegerField(min=0, max=20) # Trees cut down p4 (always selfish)
    eco_status_p2           = models.StringField() # Whether trees_p2 satisfies sustainability/eco-label standards
    eco_status_p3           = models.StringField() # Whether trees_p3 satisfies sustainability/eco-label standards
    eco_status_p4           = models.StringField() # Whether trees_p4 satisfies sustainability/eco-label standards
    trees_group_round       = models.IntegerField(min=0, max=80) # Number of trees cut down in round n of group in total
    trees_group_total       = models.IntegerField() # Total accumulated number of trees cut down of group
    forest                  = models.IntegerField(min=100, max=100, label="Please indicate of how many trees the forest consists.")
    points_player_round     = models.FloatField()  # Points of player in round n
    points_player_total     = models.FloatField()  # Total accumulated points of player 
    points_group_round      = models.FloatField() # Total points of group for round n
    points_group_total      = models.FloatField() # Total accumulated points of group
    profit_player_total     = models.FloatField()
    eco_labels_total        = models.FloatField() #Total eco-labels in group
    game_over               = models.IntegerField(min=0, max=1)
    sButtonClick            = models.StringField(blank=True)
    sTimeClick              = models.StringField(blank=True) 
    sButtonsPressed         = models.LongStringField()
    sTimesPressed           = models.LongStringField()


#def creating_session(subsession):  #delete?
 #   if subsession.round_number == 1:
  #      for player in subsession.get_players():
   #         participant = player.participant
    #        participant.subtreatment = random.choice(Constants.treatments) #dividing treatments (12/04)
     #       print(participant.subtreatment)


# FUNCTIONS
def set_trees_group_round(player):
    participant = player.participant
    participant.trees_player_round = participant.trees_player_round
    participant.trees_p2 = random.choice(Constants.sustainable_decisions) # Always sustainable player, start with 10
    participant.trees_p4 = random.choice(Constants.not_sustainable_decisions) # Always selfish player, start with 20
    if participant.forest < 41:
        participant.trees_p3 = random.choice(Constants.not_sustainable_decisions)
    elif (participant.trees_p2 + participant.trees_p4 + participant.trees_player_round) > 10: 
        participant.trees_p3 = random.choice(Constants.not_sustainable_decisions) # Not sustainable if rest of group trees > 10
    else:
        participant.trees_p3 = random.choice(Constants.sustainable_decisions) # Sustainable if rest of group trees < 10
    participant.trees_group_round = participant.trees_p2 + participant.trees_p3 + participant.trees_p4 + participant.trees_player_round
    return participant.trees_group_round

#def set_trees_group_round(player):
 #   participant = player.participant
  #  participant.trees_player_round = participant.trees_player_round
   # if participant.num_rounds = 1: #try profit group total = 0 #player.round_number #subsession.round_number == 1
      #  participant.trees_p2 = 10 
    #else: participant.trees_p2 = random.choice(Constants.sustainable_decisions) # Always sustainable player, start with 10
  #  if participant.num_rounds = 1: 
   #     participant.trees_p4 = 20
    #else: participant.trees_p4 = random.choice(Constants.not_sustainable_decisions) # Always selfish player, start with 20
    #if participant.num_rounds = 1: 
     #   participant.trees_p3 = 10   #Starts with 10
    #elif participant.forest < 41:
     #   participant.trees_p3 = 
    #elif (participant.trees_p2 + participant.trees_p4 + participant.trees_player_round) > 10: 
     #   participant.trees_p3 = random.choice(Constants.not_sustainable_decisions) # Not sustainable if rest of group trees > 10
    #else:
     #   participant.trees_p3 = random.choice(Constants.sustainable_decisions) # Sustainable if rest of group trees < 10
    #participant.trees_group_round = participant.trees_p2 + participant.trees_p3 + participant.trees_p4 + participant.trees_player_round
    #return participant.trees_group_round


def set_trees_group_total(player):
    participant = player.participant
    participant.trees_group_total = participant.trees_group_total + participant.trees_group_round
    return participant.trees_group_total


def set_forest(player):
    participant = player.participant
    participant.forest = participant.forest - participant.trees_group_round + Constants.regrowth_rate
    if participant.forest < 0:
        participant.forest = 0
    return participant.forest


def set_eco_status(player):
    participant = player.participant
    if participant.treatment == 'SECO_I_T' or participant.treatment == 'SECO_I_P' or participant.treatment == 'SECO_G_T' or participant.treatment == 'SECO_G_P':
        if participant.eco_status == "Yes":
            if participant.trees_player_round <= 10:
                participant.eco_status = "Yes"
            else:
                participant.eco_status = "No"
        else:
            participant.eco_status = "No"
    else:
        participant.eco_status = " "
    return participant.eco_status

def set_eco_status_p2(player):
    participant = player.participant
    if participant.treatment == 'SECO_I_T' or participant.treatment == 'SECO_I_P' or participant.treatment == 'SECO_G_T' or participant.treatment == 'SECO_G_P':
        if participant.eco_status_p2 == "Yes":
            if participant.trees_p2 <= 10:
                participant.eco_status_p2 = "Yes"
            else:
                participant.eco_status_p2 = "No"
        else:
            participant.eco_status_p2 = "No"
    else:
        participant.eco_status_p2 = " " #put "No" here?
    return participant.eco_status_p2

def set_eco_status_p3(player):
    participant = player.participant
    if participant.treatment == 'SECO_I_T' or participant.treatment == 'SECO_I_P' or participant.treatment == 'SECO_G_T' or participant.treatment == 'SECO_G_P':
        if participant.eco_status_p3 == "Yes":
            if participant.trees_p3 <= 10:
                participant.eco_status_p3 = "Yes"
            else:
                participant.eco_status_p3 = "No"
        else:
            participant.eco_status_p3 = "No"
    else:
        participant.eco_status_p3 = " " #put "No" here?
    return participant.eco_status_p3

def set_eco_status_p4(player):
    participant = player.participant
    if participant.treatment == 'SECO_I_T' or participant.treatment == 'SECO_I_P' or participant.treatment == 'SECO_G_T' or participant.treatment == 'SECO_G_P':
        if participant.eco_status_p4 == "Yes":
            if participant.trees_p4 <= 10:
                participant.eco_status_p4 = "Yes"
            else:
                participant.eco_status_p4 = "No"
        else:
            participant.eco_status_p4 = "No"
    else:
        participant.eco_status_p4 = " " #put "No" here?
    return participant.eco_status_p4


def set_trees_player_total(player):
    participant = player.participant
    participant.trees_player_total = participant.trees_player_total + participant.trees_player_round
    return participant.trees_player_total


def set_points_player_round(player):
    participant = player.participant
    participant.points_player_round = participant.trees_player_round
    return participant.points_player_round


def set_points_player_total(player):
    participant = player.participant
    participant.points_player_total = participant.points_player_total + participant.points_player_round
    return participant.points_player_total


def set_points_group_round(player):
    participant = player.participant
    participant.points_group_round = participant.trees_group_round
    return participant.points_group_round


def set_points_group_total(player):
    participant = player.participant
    participant.points_group_total = participant.points_group_total + participant.points_group_round
    return participant.points_group_total


def set_profit(player):
    participant = player.participant
    participant.profit_player_total = participant.points_player_total * 0.1
    return participant.profit_player_total

def set_eco_labels_total(player): #number of eco-labels in the group, DOESNT WORK YET
    participant = player.participant
    if participant.treatment == 'SECO_I_T' or participant.treatment == 'SECO_I_P' or participant.treatment == 'SECO_G_T' or participant.treatment == 'SECO_G_P' :
        if (participant.eco_status == 'Yes' and participant.eco_status_p2 == 'Yes' and participant.eco_status_p3 == 'Yes' and participant.eco_status_p4 == 'Yes') :
            participant.eco_labels_total = 4
        elif (participant.eco_status == 'No' and participant.eco_status_p2 == 'Yes' and participant.eco_status_p3 == 'Yes' and participant.eco_status_p4 == 'Yes') or (participant.eco_status == 'Yes' and participant.eco_status_p2 == 'No' and participant.eco_status_p3 == 'Yes' and participant.eco_status_p4 == 'Yes') or (participant.eco_status == 'Yes' and participant.eco_status_p2 == 'Yes' and participant.eco_status_p3 == 'No' and participant.eco_status_p4 == 'Yes') or (participant.eco_status == 'Yes' and participant.eco_status_p2 == 'Yes' and participant.eco_status_p3 == 'Yes' and participant.eco_status_p4 == 'No'):
            participant.eco_labels_total = 3
        elif (participant.eco_status == 'No' and participant.eco_status_p2 == 'No' and participant.eco_status_p3 == 'Yes' and participant.eco_status_p4 == 'Yes') or (participant.eco_status == 'No' and participant.eco_status_p2 == 'Yes' and participant.eco_status_p3 == 'No' and participant.eco_status_p4 == 'Yes') or (participant.eco_status == 'No' and participant.eco_status_p2 == 'Yes' and participant.eco_status_p3 == 'Yes' and participant.eco_status_p4 == 'No') or (participant.eco_status == 'Yes' and participant.eco_status_p2 == 'No' and participant.eco_status_p3 == 'No' and participant.eco_status_p4 == 'Yes') or (participant.eco_status == 'Yes' and participant.eco_status_p2 == 'No' and participant.eco_status_p3 == 'Yes' and participant.eco_status_p4 == 'No') or (participant.eco_status == 'Yes' and participant.eco_status_p2 == 'Yes' and participant.eco_status_p3 == 'No' and participant.eco_status_p4 == 'No'):
            participant.eco_labels_total = 2
        elif (participant.eco_status == 'Yes' and participant.eco_status_p2 == 'No' and participant.eco_status_p3 == 'No' and participant.eco_status_p4 == 'No') or (participant.eco_status == 'No' and participant.eco_status_p2 == 'Yes' and participant.eco_status_p3 == 'No' and participant.eco_status_p4 == 'No') or (participant.eco_status == 'No' and participant.eco_status_p2 == 'No' and participant.eco_status_p3 == 'Yes' and participant.eco_status_p4 == 'No') or (participant.eco_status == 'No' and participant.eco_status_p2 == 'No' and participant.eco_status_p3 == 'No' and participant.eco_status_p4 == 'Yes'):
                participant.eco_labels_total = 1
        else: 
            participant.eco_labels_total = 0
    else:
        participant.eco_labels_total = " "  #fill out "No" here?
    return participant.eco_labels_total  #when to use participant and when player 

#def creating_sessions(subsession):
 #   if subsession.round_number == 1 
  #  for player in subsession.get_

# PAGES 

#DecisionControlGP
class DecisionControlGP(Page):
    form_model = 'player'
    form_fields = ['trees_player_round', 'sButtonClick', 'sTimeClick']

    @staticmethod
    def is_displayed(player):
       participant = player.participant
       return participant.forest > 0 and (participant.treatment == 'Control_G_P')

    @staticmethod
    def error_message(player, values):
        if len(values['sButtonClick']) == 0:
            return 'Please hover your mouse over at least one block to reveal information.'
        elif values['trees_player_round'] not in Constants.removal_decisions:
            return 'Please fill in a number in between 0 and 20'
            #I removed an error message here, and I removed the eyetracking script in the pages

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        player.treatment = participant.treatment
        participant.trees_player_round = player.trees_player_round
        player.trees_group_round = set_trees_group_round(player)
        player.forest = set_forest(player)
        player.trees_group_total = set_trees_group_total(player)
        player.eco_status = set_eco_status(player)
        player.eco_status_p2 = set_eco_status_p2(player)
        player.eco_status_p3 = set_eco_status_p3(player)
        player.eco_status_p4 = set_eco_status_p4 (player)
        player.trees_player_total = set_trees_player_total(player)
        player.points_player_round = set_points_player_round(player)
        player.points_player_total = set_points_player_total(player)
        player.points_group_round = set_points_group_round(player)
        player.points_group_total = set_points_group_total(player)
        player.profit_player_total = set_profit(player)
        #player.eco_labels_total = set_eco_labels_total(player)
        player.participant.game_over = 0
        participant.sButtonClick = player.sButtonClick
        participant.sTimeClick = player.sTimeClick

#DecisionControlGT
class DecisionControlGT(Page):
    form_model = 'player'
    form_fields = ['trees_player_round', 'sButtonClick', 'sTimeClick']

    @staticmethod
    def is_displayed(player):
       participant = player.participant
       return participant.forest > 0 and (participant.treatment == 'Control_G_T')

    @staticmethod
    def error_message(player, values):
        if len(values['sButtonClick']) == 0:
            return 'Please hover your mouse over at least one block to reveal information.'
        elif values['trees_player_round'] not in Constants.removal_decisions:
            return 'Please fill in a number in between 0 and 20'

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        player.treatment = participant.treatment
        participant.trees_player_round = player.trees_player_round
        player.trees_group_round = set_trees_group_round(player)
        player.forest = set_forest(player)
        player.trees_group_total = set_trees_group_total(player)
        player.eco_status = set_eco_status(player)
        player.eco_status_p2 = set_eco_status_p2(player)
        player.eco_status_p3 = set_eco_status_p3(player)
        player.eco_status_p4 = set_eco_status_p4 (player)
        player.trees_player_total = set_trees_player_total(player)
        player.points_player_round = set_points_player_round(player)
        player.points_player_total = set_points_player_total(player)
        player.points_group_round = set_points_group_round(player)
        player.points_group_total = set_points_group_total(player)
        player.profit_player_total = set_profit(player)
        #player.eco_labels_total = set_eco_labels_total(player)
        player.participant.game_over = 0
        participant.sButtonClick = player.sButtonClick
        participant.sTimeClick = player.sTimeClick

#DecisionControlIP
class DecisionControlIP(Page):
    form_model = 'player'
    form_fields = ['trees_player_round', 'sButtonClick', 'sTimeClick']

    @staticmethod
    def is_displayed(player):
       participant = player.participant
       return participant.forest > 0 and (participant.treatment == 'Control_I_P')

    @staticmethod
    def error_message(player, values):
        if len(values['sButtonClick']) == 0:
            return 'Please hover your mouse over at least one block to reveal information.'
        elif values['trees_player_round'] not in Constants.removal_decisions:
            return 'Please fill in a number in between 0 and 20'
            #removed error message and deleted mousetracking info on pages

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        player.treatment = participant.treatment
        participant.trees_player_round = player.trees_player_round
        player.trees_group_round = set_trees_group_round(player)
        player.forest = set_forest(player)
        player.trees_group_total = set_trees_group_total(player)
        player.eco_status = set_eco_status(player)
        player.eco_status_p2 = set_eco_status_p2(player)
        player.eco_status_p3 = set_eco_status_p3(player)
        player.eco_status_p4 = set_eco_status_p4 (player)
        player.trees_player_total = set_trees_player_total(player)
        player.points_player_round = set_points_player_round(player)
        player.points_player_total = set_points_player_total(player)
        player.points_group_round = set_points_group_round(player)
        player.points_group_total = set_points_group_total(player)
        player.profit_player_total = set_profit(player)
        #player.eco_labels_total = set_eco_labels_total(player)
        player.participant.game_over = 0
        participant.sButtonClick = player.sButtonClick
        participant.sTimeClick = player.sTimeClick

#DecisionControlIT
class DecisionControlIT(Page):
    form_model = 'player'
    form_fields = ['trees_player_round', 'sButtonClick', 'sTimeClick']

    @staticmethod
    def is_displayed(player):
       participant = player.participant
       return participant.forest > 0 and (participant.treatment == 'Control_I_T')

    @staticmethod
    def error_message(player, values):
        if len(values['sButtonClick']) == 0:
            return 'Please hover your mouse over at least one block to reveal information.'
        elif values['trees_player_round'] not in Constants.removal_decisions:
            return 'Please fill in a number in between 0 and 20'

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        player.treatment = participant.treatment
        participant.trees_player_round = player.trees_player_round
        player.trees_group_round = set_trees_group_round(player)
        player.forest = set_forest(player)
        player.trees_group_total = set_trees_group_total(player)
        player.eco_status = set_eco_status(player)
        player.eco_status_p2 = set_eco_status_p2(player)
        player.eco_status_p3 = set_eco_status_p3(player)
        player.eco_status_p4 = set_eco_status_p4 (player)
        player.trees_player_total = set_trees_player_total(player)
        player.points_player_round = set_points_player_round(player)
        player.points_player_total = set_points_player_total(player)
        player.points_group_round = set_points_group_round(player)
        player.points_group_total = set_points_group_total(player)
        player.profit_player_total = set_profit(player)
       # player.eco_labels_total = set_eco_labels_total(player)
        player.participant.game_over = 0
        participant.sButtonClick = player.sButtonClick
        participant.sTimeClick = player.sTimeClick

#DecisionEcoGP


class DecisionEcoGP(Page):
    form_model = 'player'
    form_fields = ['trees_player_round', 'sButtonClick', 'sTimeClick'] 

    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return participant.forest > 0 and (participant.treatment == 'SECO_G_P')

    @staticmethod
    def error_message(player, values):
        if len(values['sButtonClick']) == 0:
            return 'Please hover your mouse over at least one block to reveal information.'
        elif values['trees_player_round'] not in Constants.removal_decisions:
            return 'Please fill in a number in between 0 and 20'

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        player.treatment = participant.treatment
        participant.trees_player_round = player.trees_player_round
        player.trees_group_round = set_trees_group_round(player)
        player.forest = set_forest(player)
        player.trees_group_total = set_trees_group_total(player)
        player.eco_status = set_eco_status(player)
        player.eco_status_p2 = set_eco_status_p2(player)
        player.eco_status_p3 = set_eco_status_p3(player)
        player.eco_status_p4 = set_eco_status_p4(player)
        player.trees_player_total = set_trees_player_total(player)
        player.points_player_round = set_points_player_round(player)
        player.points_player_total = set_points_player_total(player)
        player.points_group_round = set_points_group_round(player)
        player.points_group_total = set_points_group_total(player)
        player.profit_player_total = set_profit(player)
        player.participant.game_over = 0
        player.eco_labels_total = set_eco_labels_total(player)
        participant.sButtonClick = player.sButtonClick
        participant.sTimeClick = player.sTimeClick

#DecisionECOGT
class DecisionEcoGT(Page):
    form_model = 'player'
    form_fields = ['trees_player_round', 'sButtonClick', 'sTimeClick'] 

    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return participant.forest > 0 and (participant.treatment == 'SECO_G_T')

    @staticmethod
    def error_message(player, values):
        if len(values['sButtonClick']) == 0:
            return 'Please hover your mouse over at least one block to reveal information.'
        elif values['trees_player_round'] not in Constants.removal_decisions:
            return 'Please fill in a number in between 0 and 20'

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        player.treatment = participant.treatment
        participant.trees_player_round = player.trees_player_round
        player.trees_group_round = set_trees_group_round(player)
        player.forest = set_forest(player)
        player.trees_group_total = set_trees_group_total(player)
        player.eco_status = set_eco_status(player)
        player.eco_status_p2 = set_eco_status_p2(player)
        player.eco_status_p3 = set_eco_status_p3(player)
        player.eco_status_p4 = set_eco_status_p4(player)
        player.trees_player_total = set_trees_player_total(player)
        player.points_player_round = set_points_player_round(player)
        player.points_player_total = set_points_player_total(player)
        player.points_group_round = set_points_group_round(player)
        player.points_group_total = set_points_group_total(player)
        player.profit_player_total = set_profit(player)
        player.participant.game_over = 0
        player.eco_labels_total = set_eco_labels_total(player)
        participant.sButtonClick = player.sButtonClick
        participant.sTimeClick = player.sTimeClick

#DecisionEcoIP
class DecisionEcoIP(Page):
    form_model = 'player'
    form_fields = ['trees_player_round', 'sButtonClick', 'sTimeClick'] 

    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return participant.forest > 0 and (participant.treatment == 'SECO_I_P')

    @staticmethod
    def error_message(player, values):
        if len(values['sButtonClick']) == 0:
            return 'Please hover your mouse over at least one block to reveal information.'
        elif values['trees_player_round'] not in Constants.removal_decisions:
            return 'Please fill in a number in between 0 and 20'

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        player.treatment = participant.treatment
        participant.trees_player_round = player.trees_player_round
        player.trees_group_round = set_trees_group_round(player)
        player.forest = set_forest(player)
        player.trees_group_total = set_trees_group_total(player)
        player.eco_status = set_eco_status(player)
        player.eco_status_p2 = set_eco_status_p2(player)
        player.eco_status_p3 = set_eco_status_p3(player)
        player.eco_status_p4 = set_eco_status_p4(player)
        player.trees_player_total = set_trees_player_total(player)
        player.points_player_round = set_points_player_round(player)
        player.points_player_total = set_points_player_total(player)
        player.points_group_round = set_points_group_round(player)
        player.points_group_total = set_points_group_total(player)
        player.profit_player_total = set_profit(player)
        player.participant.game_over = 0
        player.eco_labels_total = set_eco_labels_total(player)
        participant.sButtonClick = player.sButtonClick
        participant.sTimeClick = player.sTimeClick

#DecisionEcoIT
class DecisionEcoIT(Page):
    form_model = 'player'
    form_fields = ['trees_player_round', 'sButtonClick', 'sTimeClick'] 

    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return participant.forest > 0 and (participant.treatment == 'SECO_I_T')

    @staticmethod
    def error_message(player, values):
        if len(values['sButtonClick']) == 0:
            return 'Please hover your mouse over at least one block to reveal information.'
        elif values['trees_player_round'] not in Constants.removal_decisions:
            return 'Please fill in a number in between 0 and 20'

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        player.treatment = participant.treatment
        participant.trees_player_round = player.trees_player_round
        player.trees_group_round = set_trees_group_round(player)
        player.forest = set_forest(player)
        player.trees_group_total = set_trees_group_total(player)
        player.eco_status = set_eco_status(player)
        player.eco_status_p2 = set_eco_status_p2(player)
        player.eco_status_p3 = set_eco_status_p3(player)
        player.eco_status_p4 = set_eco_status_p4(player)
        player.trees_player_total = set_trees_player_total(player)
        player.points_player_round = set_points_player_round(player)
        player.points_player_total = set_points_player_total(player)
        player.points_group_round = set_points_group_round(player)
        player.points_group_total = set_points_group_total(player)
        player.profit_player_total = set_profit(player)
        player.participant.game_over = 0
        player.eco_labels_total = set_eco_labels_total(player)
        participant.sButtonClick = player.sButtonClick
        participant.sTimeClick = player.sTimeClick


class RoundFeedback(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return participant.forest > 0

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        player.forest = player.forest

class GameOver(Page):
    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return participant.forest <= 0 and player.participant.game_over == 0

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.round_number = player.round_number
        player.participant.game_over = 1
        player.game_over = player.participant.game_over


class ResultsGP(Page): 
    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return participant.forest > 0 and (participant.treatment == 'SECO_G_P' or participant.treatment == 'Control_G_P')

class ResultsGT(Page): 
    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return participant.forest > 0 and (participant.treatment == 'SECO_G_T' or participant.treatment == 'Control_G_T')

class ResultsIP(Page): 
    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return participant.forest > 0 and (participant.treatment == 'SECO_I_P' or participant.treatment == 'Control_I_P')

class ResultsIT(Page): 
    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return participant.forest > 0 and (participant.treatment == 'SECO_I_T' or participant.treatment == 'Control_I_T')


page_sequence = [DecisionControlGP, DecisionControlGT, DecisionControlIP, DecisionControlIT, DecisionEcoGP, DecisionEcoGT, DecisionEcoIP, DecisionEcoIT, GameOver, ResultsGP, ResultsGT, ResultsIP, ResultsIT, RoundFeedback] 
