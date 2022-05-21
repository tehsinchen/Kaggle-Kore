from kaggle_environments.envs.kore_fleets.helpers import *


def build_ships(obs, config):
    board = Board(obs, config)
    me = board.current_player

    me = board.current_player
    spawn_cost = board.configuration.spawn_cost
    kore_left = me.kore

    # loop through all shipyards you control
    for shipyard in me.shipyards:
        # build a ship!
        if kore_left >= spawn_cost:
            action = ShipyardAction.spawn_ships(1)
            shipyard.next_action = action

    return me.next_actions
