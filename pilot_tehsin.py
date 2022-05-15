from kaggle_environments.envs.kore_fleets.helpers import Board

from messanger import get_info
from headquarter_tehsin import HeadQuarter


def pilot(obs, config):
    message = get_info(Board(obs, config))
    hq = HeadQuarter(message)
    return hq.get_command()
