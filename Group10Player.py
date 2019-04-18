from pypokerengine.players import BasePokerPlayer
# import random as rand
import pprint
from Group10Node import Node


class Group10Player(BasePokerPlayer):

    def __init__(self):
        self.weights = [0.5719561761732826, 0.06875975502152562, 0.5162121322003739, 0.6633226510229807]

    def declare_action(self, valid_actions, hole_card, round_state):
        # valid_actions format => [raise_action_pp = pprint.PrettyPrinter(indent=2)
        # pp = pprint.PrettyPrinter(indent=2)
        # print("------------ROUND_STATE(RANDOM)--------")
        # pp.pprint(round_state)
        # print("------------HOLE_CARD----------")
        # pp.pprint(hole_card)
        # print("------------VALID_ACTIONS----------")
        # pp.pprint(valid_actions)
        # print("-------------------------------")

        # r = rand.random()
        # if r <= 0.5:
        #   call_action_info = valid_actions[1]
        # elif r<= 0.9 and len(valid_actions ) == 3:
        #   call_action_info = valid_actions[2]
        # else:
        #   call_action_info = valid_actions[0]
        # action = call_action_info["action"]
        # return action  # action returned here is sent to the poker engine

        depth = 50  # ! Need to change this value for optimisation
        community_cards = round_state['community_card']
        current_street = round_state['street']
        small_blind_player = checkSmallBlind(round_state, current_street)

        # get number of raises in this street by checking against action history in this street
        num_of_raise_in_street = 0
        street_action_history = round_state['action_histories'][current_street]
        for action in street_action_history:
            if (action['action'] == 'RAISE' or action['action'] == 'BIGBLIND'):
                num_of_raise_in_street = num_of_raise_in_street + 1

        # get number of raises by MAX_PLAYER and MIN_PLAYER in entire round by checking against entire action history
        max_player_id = round_state['seats'][0]['uuid']
        min_player_id = round_state['seats'][1]['uuid']
        num_of_raise_by_max = 0
        num_of_raise_by_min = 0
        action_history = round_state['action_histories']
        for street in action_history:
            street_action_history = action_history[street]
            for action in street_action_history:
                if (action['action'] == 'RAISE'):
                    if (action['uuid'] == max_player_id):
                        num_of_raise_by_max = num_of_raise_by_max + 1
                    elif (action['uuid'] == min_player_id):
                        num_of_raise_by_min = num_of_raise_by_min + 1

        node = Node(None, False, depth, 1, hole_card, community_cards, valid_actions, small_blind_player,
                    current_street, self.weights, num_of_raise_in_street, num_of_raise_by_max, num_of_raise_by_min)
        print("Built minimax tree")
        max = -1 * float('inf')
        best_action = None
        for child_node in node.children:
            curr_value = find_minimax(
                child_node, -1 * float('inf'), float('inf'))
            if curr_value > max:
                max = curr_value
                best_action = child_node.action

        return best_action

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


def find_minimax(node, alpha, beta):
    if type(node) == int:
        return node
    elif node.depth == 0 or node.isTerminal:
        return node.evaluate()
    else:
        if node.node_type == 1:  # MAX_PLAYER node
            max = -1 * float('inf')
            for child_node in node.children:
                curr_value = find_minimax(child_node, alpha, beta)
                if (curr_value > max):
                    max = curr_value
                if (curr_value > alpha):  # pruning
                    alpha = curr_value
                if (beta <= alpha):
                    break
            return max
        elif node.node_type == 2:  # MIN_PLAYER node
            min = 1 * float('inf')
            for child_node in node.children:
                curr_value = find_minimax(child_node, alpha, beta)
                if (curr_value < min):
                    min = curr_value
                if (curr_value < alpha):  # pruning
                    alpha = curr_value
                if (beta <= alpha):
                    break
            return min
        elif node.node_type == 0:  # Chance node
            # Take average of all chance nodes
            sum = 0
            num_nodes = 0
            for child_node in node.children:
                curr_value = find_minimax(child_node, alpha, beta)
                sum += curr_value
                num_nodes += 1
            return sum / num_nodes


def get_opponentTotalBetAmount(round_state, current_street, small_blind_player):
    totalBet = 0
    for street, values in round_state["action_histories"].items():
        if street == current_street:
            # both players have just placed initial bets
            if street == "preflop" and len(values) == 2:
                totalBet += 20
            else:
                if (len(values) == 0):  # opponent is big blind and has not bet in current street
                    pass
                else:
                    totalBet += values[-1]['amount']
        else:
            if small_blind_player == 2:  # opponent is small blind
                if len(values) % 2 == 1:
                    # Street ended with small blind move
                    totalBet += values[-1]['amount']
                else:
                    # Street ended with big blind move
                    totalBet += values[-2]['amount']
            else:  # opponent is big blind
                if len(values) % 2 == 1:
                    # Street ended with small blind move
                    totalBet += values[-2]['amount']
                else:
                    # Street ended with big blind move
                    totalBet += values[-1]['amount']
    return totalBet


def checkSmallBlind(round_state, current_street):
    # opponent is small blind
    if len(round_state['action_histories'][current_street]) % 2 == 1:
        return 2
    else:
        return 1


def get_opponentCurrBetAmount(round_state, current_street):
    if current_street == "preflop" and len(round_state['action_histories'][current_street]) == 2:
        return 10  # MIN_PLAYER is big blind and has not increased bet in preflop
    else:
        if len(round_state['action_histories'][current_street]) == 0:
            return 0  # MIN_PLAYER is big_blind and has not bet in current street
        else:
            return round_state['action_histories'][current_street][-1]['amount']


def get_ownCurrBetAmount(round_state, current_street):
    if current_street == "preflop":
        if len(round_state['action_histories'][current_street]) == 2:
            return 10  # MAX_PLAYER is small blind and has not increased bet in preflop
        elif len(round_state['action_histories'][current_street]) == 3:
            return 20  # MAX_PLAYER is big blind and has not increased bet in preflop
        else:
            return round_state['action_histories'][current_street][-2]['amount']
    else:
        if len(round_state['action_histories'][current_street]) == 0:
            return 0  # MAX_PLAYER is small_blind and has not bet in current street
        elif len(round_state['action_histories'][current_street]) == 1:
            return 0  # MAX_PLAYER is big_blind and has not bet in current street
        elif len(round_state['action_histories'][current_street]) == 2:
            # MAX_PLAYER is small_blind and has bet once in current street
            return round_state['action_histories'][current_street][-1]['amount']
        else:
            # print(round_state)
            return round_state['action_histories'][current_street][-2]['amount']


def setup_ai():
    return Group10Player()
