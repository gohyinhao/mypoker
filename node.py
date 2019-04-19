# Build a minimax search tree
# For simplicity, ignore whether players have sufficient money and whether max no. of raises have been reached
# Round ends only if both players have bet the same amount

import random as rand
from myEval import evalFunction


class Node(object):
    def __init__(self, action, isTerminal, depth, node_type, hole_cards, community_cards, valid_actions, small_blind_player, current_street, weights, num_of_raise_in_street, num_of_raise_by_max, num_of_raise_by_min, own_currBetAmount, opponent_currBetAmount, own_totalBetAmount, opponent_totalBetAmount):
        self.action = action
        self.isTerminal = isTerminal
        self.depth = depth
        self.node_type = node_type  # 0 if chance node, 1 if MAX_PLAYER, 2 if MIN_PLAYER
        self.hole_cards = hole_cards
        self.community_cards = community_cards
        self.valid_actions = valid_actions
        self.small_blind_player = small_blind_player  # 1 if MAX_PLAYER, 2 if MIN_PLAYER
        self.current_street = current_street
        self.weights = weights
        self.num_of_raise_in_street = num_of_raise_in_street
        self.num_of_raise_by_max = num_of_raise_by_max
        self.num_of_raise_by_min = num_of_raise_by_min
        self.own_currBetAmount = own_currBetAmount
        self.opponent_currBetAmount = opponent_currBetAmount
        self.own_totalBetAmount = own_totalBetAmount
        self.opponent_totalBetAmount = opponent_totalBetAmount
        self.children = []
        if (not isTerminal):
            self.generateChildren()

    def generateChildren(self):

        # self.print_node()
        RAISE_AMOUNT = 20

        if self.depth > 0:  # and len(self.community_cards) < 5:

            # MAX_PLAYER node
            if self.node_type == 1:
                for i in self.valid_actions:
                    action = i["action"]
                    # print("============== If MAX_PLAYER {} ==============".format(action))

                    if action == "fold":
                        # Represents a terminal node (MIN_PLAYER wins the pot)
                        self.children.append(Node("fold", True, self.depth - 1, 0, self.hole_cards, self.community_cards, self.valid_actions, self.small_blind_player,
                                                  self.current_street, self.weights, self.num_of_raise_in_street, self.num_of_raise_by_max, self.num_of_raise_by_min, self.own_currBetAmount, self.opponent_currBetAmount, self.own_totalBetAmount, self.opponent_totalBetAmount))
                    elif action == "raise":
                        # if max number of raise is reached, do not generate node for raise action
                        if (self.num_of_raise_by_max == 4 or self.num_of_raise_in_street == 4):
                            continue

                        amount_added = self.opponent_currBetAmount - \
                            self.own_currBetAmount + RAISE_AMOUNT
                        # If all five community cards are revealed, generate terminal node
                        if len(self.community_cards) == 5:
                            self.children.append(Node("raise", True, self.depth - 1, 2, self.hole_cards, self.community_cards, self.valid_actions, self.small_blind_player,
                                                      self.current_street, self.weights, self.num_of_raise_in_street + 1, self.num_of_raise_by_max + 1, self.num_of_raise_by_min, self.own_currBetAmount + amount_added, self.opponent_currBetAmount, self.own_totalBetAmount, self.opponent_totalBetAmount + amount_added))
                        # Else generate MIN node (MIN_PLAYER's turn)
                        else:
                            self.children.append(Node("raise", False, self.depth - 1, 2, self.hole_cards, self.community_cards, self.valid_actions, self.small_blind_player,
                                                      self.current_street, self.weights, self.num_of_raise_in_street + 1, self.num_of_raise_by_max + 1, self.num_of_raise_by_min, self.own_currBetAmount + amount_added, self.opponent_currBetAmount, self.own_totalBetAmount, self.opponent_totalBetAmount + amount_added))
                    elif action == "call":
                        amount_added = self.opponent_currBetAmount - self.own_currBetAmount
                        # If all five community cards are revealed, generate terminal node
                        if len(self.community_cards) == 5:
                            self.children.append(Node("call", True, self.depth - 1, 0, self.hole_cards, self.community_cards, self.valid_actions, self.small_blind_player,
                                                      self.current_street, self.weights, self.num_of_raise_in_street, self.num_of_raise_by_max, self.num_of_raise_by_min, self.own_currBetAmount + amount_added, self.opponent_currBetAmount, self.own_totalBetAmount, self.opponent_totalBetAmount + amount_added))
                        # Else generate a chance node (Round has ended, reveal community cards next)
                        else:
                            self.children.append(Node("call", False, self.depth - 1, 0, self.hole_cards, self.community_cards, self.valid_actions, self.small_blind_player,
                                                      self.current_street, self.weights, self.num_of_raise_in_street, self.num_of_raise_by_max, self.num_of_raise_by_min, self.own_currBetAmount + amount_added, self.opponent_currBetAmount, self.own_totalBetAmount, self.opponent_totalBetAmount + amount_added))

            # MIN_PLAYER node
            elif self.node_type == 2:
                for i in self.valid_actions:
                    action = i["action"]
                    # print("============== If MIN_PLAYER {} ==============".format(action))

                    if action == "fold":
                        # Represents a terminal node (MAX_PLAYER wins the pot)
                        self.children.append(Node("fold", True, self.depth - 1, 0, self.hole_cards, self.community_cards, self.valid_actions,
                                                  self.small_blind_player, self.current_street, self.weights, self.num_of_raise_in_street, self.num_of_raise_by_max, self.num_of_raise_by_min, self.own_currBetAmount, self.opponent_currBetAmount, self.own_totalBetAmount, self.opponent_totalBetAmount))
                    elif action == "raise":
                        # if max number of raise is reached, do not generate node for raise action
                        if (self.num_of_raise_by_min == 4 or self.num_of_raise_in_street == 4):
                            continue

                        amount_added = self.own_currBetAmount - \
                            self.opponent_currBetAmount + RAISE_AMOUNT
                        # If all five community cards are revealed, generate terminal node
                        if len(self.community_cards) == 5:
                            self.children.append(Node("raise", True, self.depth - 1, 1, self.hole_cards, self.community_cards, self.valid_actions, self.small_blind_player,
                                                      self.current_street, self.weights, self.num_of_raise_in_street + 1, self.num_of_raise_by_max, self.num_of_raise_by_min + 1, self.own_currBetAmount + amount_added, self.opponent_currBetAmount, self.own_totalBetAmount, self.opponent_totalBetAmount + amount_added))
                        # Else generate MIN node (MAX_PLAYER's turn)
                        else:
                            self.children.append(Node("raise", False, self.depth - 1, 1, self.hole_cards, self.community_cards, self.valid_actions, self.small_blind_player,
                                                      self.current_street, self.weights, self.num_of_raise_in_street + 1, self.num_of_raise_by_max, self.num_of_raise_by_min + 1, self.own_currBetAmount + amount_added, self.opponent_currBetAmount, self.own_totalBetAmount, self.opponent_totalBetAmount + amount_added))
                    elif action == "call":
                        amount_added = self.own_currBetAmount - self.opponent_currBetAmount
                        # If all five community cards are revealed, generate terminal node
                        if len(self.community_cards) == 5:
                            self.children.append(Node("call", True, self.depth - 1, 0, self.hole_cards, self.community_cards, self.valid_actions, self.small_blind_player,
                                                      self.current_street, self.weights, self.num_of_raise_in_street, self.num_of_raise_by_max, self.num_of_raise_by_min, self.own_currBetAmount + amount_added, self.opponent_currBetAmount, self.own_totalBetAmount, self.opponent_totalBetAmount + amount_added))
                        # Else generate a chance node (Round has ended, reveal community cards next)
                        else:
                            self.children.append(Node("call", False, self.depth - 1, 0, self.hole_cards, self.community_cards, self.valid_actions, self.small_blind_player,
                                                      self.current_street, self.weights, self.num_of_raise_in_street, self.num_of_raise_by_max, self.num_of_raise_by_min, self.own_currBetAmount + amount_added, self.opponent_currBetAmount, self.own_totalBetAmount, self.opponent_totalBetAmount + amount_added))

            # Chance node
            elif self.node_type == 0:
                # print("============== Reveal community cards ==============")
                new_community_cards = self.community_cards[:]
                isTerminal = False
                if len(self.community_cards) == 0:
                    for i in range(0, 3):
                        pickedCard_suit = rand.choice(['C', 'D', 'H', 'S'])
                        pickedCard_number = rand.choice(
                            ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'])
                        pickedCard = pickedCard_suit + pickedCard_number
                        # check if pickedCard already out
                        while pickedCard in (self.hole_cards or new_community_cards):
                            pickedCard_suit = rand.choice(['C', 'D', 'H', 'S'])
                            pickedCard_number = rand.choice(
                                ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'])
                            pickedCard = pickedCard_suit + pickedCard_number
                        new_community_cards.append(pickedCard)
                else:
                    pickedCard_suit = rand.choice(['C', 'D', 'H', 'S'])
                    pickedCard_number = rand.choice(
                        ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'])
                    pickedCard = pickedCard_suit + pickedCard_number
                    # check if pickedCard already out
                    while pickedCard in (self.hole_cards or new_community_cards):
                        pickedCard_suit = rand.choice(['C', 'D', 'H', 'S'])
                        pickedCard_number = rand.choice(
                            ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'])
                        pickedCard = pickedCard_suit + pickedCard_number
                    new_community_cards.append(pickedCard)
                    if (len(new_community_cards) == 5):
                        isTerminal = True

                next_street = ""
                if self.current_street == "preflop":
                    next_street = "flop"
                elif self.current_street == "flop":
                    next_street = "turn"
                elif self.current_street == "turn":
                    next_street = "river"
                if self.current_street == "river" or self.current_street == "showdown":
                    next_street = "showdown"

                self.children.append(Node(None, isTerminal, self.depth - 1, self.small_blind_player, self.hole_cards, new_community_cards, self.valid_actions,
                                          self.small_blind_player, next_street, self.weights, 0, self.num_of_raise_by_max, self.num_of_raise_by_min, 0, 0, self.own_totalBetAmount, self.opponent_totalBetAmount))

    def evaluate(self):
        value = evalFunction(
            self.hole_cards, self.community_cards, self.current_street, self.weights, self.own_totalBetAmount, self.action)
        return value.baseValue() + value.pairValue() + value.flushValue() + value.straightValue() + value.streetValue() + value.potValue()

    def print_node(self):
        print("=== Printing node ===")
        print("Depth: {}".format(self.depth))
        print("Node Type: {}".format(self.node_type))
        print("Hole Cards: {}".format(self.hole_cards))
        print("Community Cards: {}".format(self.community_cards))
        print("Valid actions: {}".format(self.valid_actions))

    def print_children(self):
        for i in self.children:
            if type(i) == int:
                print("=== Printing terminal node === ")
                print(i)
            else:
                i.print_node()
