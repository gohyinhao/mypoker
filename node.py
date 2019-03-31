# Build a minimax search tree
# For simplicity, ignore whether players have sufficient money and whether max no. of raises have been reached
# Round ends only if both players have bet the same amount 
 
import random as rand
from myEval import evalFunction

class Node(object):
    def __init__(self, depth, node_type, hole_cards, community_cards, own_currBetAmount, opponent_currBetAmount, own_totalBetAmount, opponent_totalBetAmount, valid_actions, small_blind_player, current_street, weights):
        self.depth = depth
        self.node_type = node_type # 0 if chance node, 1 if MAX_PLAYER, 2 if MIN_PLAYER
        self.hole_cards = hole_cards
        self.community_cards = community_cards
        self.own_currBetAmount = own_currBetAmount
        self.opponent_currBetAmount = opponent_currBetAmount
        self.own_totalBetAmount = own_totalBetAmount
        self.opponent_totalBetAmount = opponent_totalBetAmount
        self.valid_actions = valid_actions
        self.small_blind_player = small_blind_player # 1 if MAX_PLAYER, 2 if MIN_PLAYER
        self.current_street = current_street
        self.weights = weights
        self.children = []
        self.generateChildren()
    
    def generateChildren(self):

        # self.print_node()
        
        if self.depth > 0 and len(self.community_cards) < 5:
            
            # MAX_PLAYER node
            if self.node_type == 1: 
                for i in self.valid_actions:
                    action = i["action"]
                    # print("============== If MAX_PLAYER {} ==============".format(action))
                    
                    if action == "fold":
                        # Represents a terminal node (MIN_PLAYER wins the pot)
                        self.children.append(-1*self.own_totalBetAmount) 
                    elif action == "raise":
                        # Generate MIN node (MIN_PLAYER's turn)
                        amount_added = self.opponent_currBetAmount + 10 - self.own_currBetAmount
                        self.children.append(Node(self.depth-1, 2, self.hole_cards, self.community_cards, self.opponent_currBetAmount+10, self.opponent_currBetAmount, self.own_totalBetAmount+amount_added, self.opponent_totalBetAmount, self.valid_actions, self.small_blind_player, self.current_street, self.weights))
                    elif action == "call":
                        # Generate a chance node (Round has ended, reveal community cards next)
                        amount_added = self.opponent_currBetAmount - self.own_currBetAmount
                        self.children.append(Node(self.depth-1, 0, self.hole_cards, self.community_cards, self.opponent_currBetAmount, self.opponent_currBetAmount, self.own_totalBetAmount+amount_added, self.opponent_totalBetAmount, self.valid_actions, self.small_blind_player, self.current_street, self.weights))
            
            # MIN_PLAYER node
            elif self.node_type == 2:     
                for i in self.valid_actions:
                    action = i["action"]
                    # print("============== If MIN_PLAYER {} ==============".format(action))

                    if action == "fold":
                        # Represents a terminal node (MAX_PLAYER wins the pot)
                        self.children.append(1*self.opponent_totalBetAmount) 
                    elif action == "raise":
                        # Generate MIN node (MAX_PLAYER's turn)
                        amount_added = self.own_currBetAmount + 10 - self.opponent_currBetAmount
                        self.children.append(Node(self.depth-1, 1, self.hole_cards, self.community_cards, self.own_currBetAmount, self.own_currBetAmount+10, self.own_totalBetAmount, self.opponent_totalBetAmount+amount_added, self.valid_actions, self.small_blind_player, self.current_street, self.weights))
                    elif action == "call":
                        # Generate a chance node (Round has ended, reveal community cards next)
                        amount_added = self.own_currBetAmount - self.opponent_currBetAmount
                        self.children.append(Node(self.depth-1, 0, self.hole_cards, self.community_cards, self.own_currBetAmount, self.own_currBetAmount, self.own_totalBetAmount, self.opponent_totalBetAmount+amount_added, self.valid_actions, self.small_blind_player, self.current_street, self.weights))

            # Chance node
            elif self.node_type == 0:
                # print("============== Reveal community cards ==============")
                # ! Simply picks random card(s) at random without checking (to be improved later) 
                new_community_cards = self.community_cards[:]
                if len(self.community_cards) == 0:
                    for i in range(0, 3):
                        pickedCard_suit = rand.choice(['C', 'D', 'H', 'S'])
                        pickedCard_number = rand.choice(['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'])
                        pickedCard = pickedCard_suit + pickedCard_number
                        new_community_cards.append(pickedCard)
                else:
                    pickedCard_suit = rand.choice(['C', 'D', 'H', 'S'])
                    pickedCard_number = rand.choice(['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'])
                    pickedCard = pickedCard_suit + pickedCard_number
                    new_community_cards.append(pickedCard)
                
                self.children.append(Node(self.depth-1, self.small_blind_player, self.hole_cards, new_community_cards, 0, 0, self.own_totalBetAmount, self.opponent_totalBetAmount, self.valid_actions, self.small_blind_player, self.current_street, self.weights))

    def evaluate(self):
        #return rand.randint(1, 100)        

        value = evalFunction(self.hole_cards, self.community_cards, self.current_street, self.weights)
        return value.baseValue() + value.pairValue() + value.flushValue() + value.straightValue()

    def print_node(self):
        print("=== Printing node ===")
        print("Depth: {}".format(self.depth))
        print("Node Type: {}".format(self.node_type))
        print("Hole Cards: {}".format(self.hole_cards))
        print("Community Cards: {}".format(self.community_cards))
        print("Own Bet Amount (in this street): {}".format(self.own_currBetAmount))
        print("Opponent Bet Amount (in this street): {}".format(self.opponent_currBetAmount))
        print("Own Bet Amount (in this round): {}".format(self.own_totalBetAmount))
        print("Opponent Bet Amount (in this round): {}".format(self.opponent_totalBetAmount))
        print("Valid actions: {}".format(self.valid_actions))

    def print_children(self):
        for i in self.children:
            if type(i) == int:
                print("=== Printing terminal node === ")
                print(i)
            else:
                i.print_node()
