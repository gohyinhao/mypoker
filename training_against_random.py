from pypokerengine.api.game import setup_config, start_poker
from minimax_player import MinimaxPlayer
from randomplayer import RandomPlayer
import random

# note: need to implement attribute called weights in MinimaxPlayer class.
# weights should either be an array/list
NUMBER_OF_WEIGHTS = 4

# learning rate that will affect how fast agent learns.
# 1. leave it as a small constant
# 2. have it vary according to number of times trained, i.e. gets smaller after each round of training
learning_rate = 0.1

# max number of training iterations where weights remains unchanged
MAX_NUMBER_OF_ITERATIONS = 50

# randomly initialized starting weights
agent_weights = []
for x in range(NUMBER_OF_WEIGHTS):
    agent_weights.append(random.random())

# boolean variable to check whether to replay past opponent
replay = False
number_of_replays = 0
MAX_NUMBER_OF_REPLAYS_FOR_TIES = 100

number_of_iterations = 0
while number_of_iterations < MAX_NUMBER_OF_ITERATIONS:
    if not replay:
        # randomly initialize opponent weights if not replaying
        agent_weights = []
        for x in range(NUMBER_OF_WEIGHTS):
            agent_weights.append(random.random())

    # max_round: number of times players can play against each. set to be the same as number of rounds in actual assessment
    # initial_stack: starting money. set to be 1000 as per assessment
    # small_blind_amount: set to be 10 as per assessment
    config = setup_config(
        max_round=500, initial_stack=10000, small_blind_amount=20)

    config.register_player(
        name="my_agent", algorithm=MinimaxPlayer(agent_weights))
    config.register_player(name="opponent_agent",
                           algorithm=RandomPlayer())

    print("agent: ", agent_weights)

    game_result = start_poker(config, verbose=1)

    my_agent_end_stack = game_result["players"][0]["stack"]
    opponent_end_stack = game_result["players"][1]["stack"]

    print("agent stack: ", my_agent_end_stack)
    print("opponent stack: ", opponent_end_stack)

    if my_agent_end_stack > opponent_end_stack:
        # agent won so weights remains unchanged
        number_of_iterations = number_of_iterations + 1
        replay = False
        number_of_replays = 0
        continue
    elif my_agent_end_stack < opponent_end_stack:
        # agent lost so update weights and replay opponent
        number_of_iterations = 0
        replay = False
        number_of_replays = 0
        continue
    else:
        # tie so replay to eliminate randomness
        number_of_iterations = 0
        if number_of_replays < MAX_NUMBER_OF_REPLAYS_FOR_TIES:
            replay = True
            number_of_replays = number_of_replays + 1
            continue
        else:
            # tie MAX_NUMBER_OF_REPLAYS_FOR_TIES times consecutively. break
            print("Players are equally tied")
            break

print("final weights: ", agent_weights)
