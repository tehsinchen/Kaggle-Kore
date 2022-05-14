from kaggle_environments.envs.kore_fleets.helpers import Board


def get_info(obs, config):
    msg = {}
    board = Board(obs, config)

    me = board.current_player_id
    num_enemy = (len(board.players) - 1)

    board_size = board.configuration.size
    # key init
    msg['board_kore'] = [[0]*board_size]*board_size
    msg['me_sh']
    for i in range(board_size):
        for j in range(board_size):
            msg['board_kore'][i][j] = board.cells[(i, j)].kore

    # me
    # enimies
    # board

    # global val
    msg['turn'] = board.step
    msg['spawn_cost'] = board.configuration.spawn_cost
    msg['convert_cost'] = board.configuration.convert_cost
    msg['episodes'] = board.configuration.episode_steps
    return msg, board.current_player
