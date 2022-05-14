from messanger import get_info
from headquarter_tehsin import get_strategy


def pilot(obs, config):
    message, me = get_info(obs, config)

    for shipyard in me.shipyards:
        shipyard.next_action = get_strategy(message)
    return me.next_actions
