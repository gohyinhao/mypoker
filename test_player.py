from pypokerengine.players import BasePokerPlayer
from time import sleep
import pprint
from myEval import evalFunction

class TestPlayer(BasePokerPlayer):

    def __init__(self, weights):
        self.weights = weights

    def declare_action(self, valid_actions, hole_card, round_state):

        community_cards = round_state['community_card']
        current_street = round_state['street']

        # check whether raise is a valid move
        is_raise_valid = False
        for i in valid_actions:
            action = i["action"]
            if (action == "raise"):
                is_raise_valid = True

        value = evalFunction(hole_card, community_cards, current_street, self.weights)
        evaluated_value = value.baseValue() + value.pairValue() + value.flushValue() + value.straightValue()

        if evaluated_value <= 0:
            return "fold"
        elif evaluated_value > self.weights[4] and is_raise_valid:
            return "raise"
        else:
            return "call"

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        # print("Street %s Started"%street)
        # print("-------------------------------")
        # print('\n')
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pprint.pprint(round_state)
        # while True:
        #   pass
        print("---------------")
        #pass

def setup_ai(weights):
    return TestPlayer(weights)
