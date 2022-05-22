def get_info(board):
    msg = {}
    # board
    board_size = board.configuration.size
    msg['board_kore'] = [[0]*board_size]*board_size
    for i in range(board_size):
        for j in range(board_size):
            msg['board_kore'][i][j] = board.cells[(i, j)].kore
    # me
    msg['me'] = {
        "fleet": {},
        "shipyard": {},
        "kore": int(board.current_player.kore)
    }
    for fleet in board.current_player.fleets:
        msg['me']["fleet"][fleet.id] = {}
        msg['me']["fleet"][fleet.id]['kore'] = fleet.kore
        msg['me']["fleet"][fleet.id]['ship_count'] = fleet.ship_count
        msg['me']["fleet"][fleet.id]['flight_plan'] = fleet.flight_plan
        msg['me']["fleet"][fleet.id]['position'] = fleet.position
    for shipyard in board.current_player.shipyards:
        msg['me']["shipyard"][shipyard.id] = {}
        msg['me']["shipyard"][shipyard.id]["ship_count"] = shipyard.ship_count
        msg['me']["shipyard"][shipyard.id]["position"] = shipyard.position
        msg['me']["shipyard"][shipyard.id]["max_spawn"] = shipyard.max_spawn
    # enimies
    for opponent in board.opponents:
        e_id = f'enemy_{opponent.id}'
        msg[e_id] = {
            "fleet": {},
            "shipyard": {},
            "kore": int(opponent.kore)
        }
        for fleet in opponent.fleets:
            msg[e_id]["fleet"][fleet.id] = {}
            msg[e_id]["fleet"][fleet.id]['kore'] = fleet.kore
            msg[e_id]["fleet"][fleet.id]['ship_count'] = fleet.ship_count
            msg[e_id]["fleet"][fleet.id]['flight_plan'] = fleet.flight_plan
            msg[e_id]["fleet"][fleet.id]['position'] = fleet.position
        for shipyard in opponent.shipyards:
            msg[e_id]["shipyard"][shipyard.id] = {}
            msg[e_id]["shipyard"][shipyard.id]['ship_count'] = shipyard.ship_count
            msg[e_id]["shipyard"][shipyard.id]['position'] = shipyard.position
    # global val
    msg['num_enemies'] = len(board.opponents)
    msg['turn'] = board.step
    msg['spawn_cost'] = board.configuration.spawn_cost
    msg['convert_cost'] = board.configuration.convert_cost
    msg['episodes'] = board.configuration.episode_steps
    return msg
