from kaggle_environments.envs.kore_fleets.helpers import ShipyardAction


def kore_launch_fleet(ship_count, flight_plan):
    return ShipyardAction.launch_fleet_with_flight_plan(ship_count, flight_plan).name


def kore_spawn_ships(num):
    return ShipyardAction.spawn_ships(num).name
