from pypokerengine.api.game import setup_config, start_poker
from randomplayer import RandomPlayer
from raise_player import RaisedPlayer
from minimax_player import MinimaxPlayer

# TODO:config the config as our wish
config = setup_config(max_round=10, initial_stack=10000, small_blind_amount=20)


config.register_player(name="f1", algorithm=MinimaxPlayer(
    [0.5, 0.5, 0.5, 0.5, 1, 0.5]))
config.register_player(name="FT2", algorithm=RaisedPlayer())


game_result = start_poker(config, verbose=0)
