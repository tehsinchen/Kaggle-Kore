from kore_act_api import kore_launch_fleet, kore_spawn_ships
import math
import random


class GetInfoUtility:

    def __init__(self):
        self.max_plan_len = 0

    @staticmethod
    def _required_ship(plan):
        return math.ceil(math.exp((len(plan)-1) / 2))

    @staticmethod
    def _get_interval(e, b):
        interval = (e - b)
        e_edge = (21 - e) if e > 10 else e
        b_edge = (21 - b) if b > 10 else b
        edge_interval = (e_edge + b_edge)
        if edge_interval < abs(interval):
            interval = edge_interval if interval < 0 else -edge_interval
        return interval

    def _pos_to_plan(self, pos_begin, pos_end):
        """Arrive to the destination with the shortest flight plan"""

        x_interval = self._get_interval(pos_end[0], pos_begin[0])
        y_interval = self._get_interval(pos_end[1], pos_begin[1])

        forward_x, backward_y = "", ""
        if x_interval > 0:
            forward_x, backward_x = "E", "W"
        if x_interval < 0:
            forward_x, backward_x = "W", "E"
        forward_y, backward_y = "", ""
        if y_interval > 0:
            forward_y, backward_y = "N", "S"
        if y_interval < 0:
            forward_y, backward_y = "S", "N"

        flight_plan = ""
        if (random.randint(0, 50) % 2) == 0:
            forward_plan = forward_x + \
                str(x_interval) + forward_y + str(y_interval)
            backward_plan = backward_y + str(y_interval) + backward_x
        else:
            forward_plan = forward_y + \
                str(y_interval) + forward_x + str(x_interval)
            backward_plan = backward_x + str(x_interval) + backward_y
        flight_plan += (forward_plan + backward_plan)
        flight_plan = flight_plan.replace("-", "")
        if len(flight_plan) <= self.max_plan_len:
            return self._required_ship(flight_plan), flight_plan
        return ""

    def greedy_kore_search(self, shipyard_pos, board_kore, ship_cnt):
        """Get the path which contains the most kore"""

        self.max_plan_len = (math.floor(2*math.log(ship_cnt)) + 1)

        candidate_dict = {}

        # should consider the most number of kore throughout the path

        # num_kore, , kore_pos = 0, (0, 0), (0, 0)
        # for kore in candidate_dict.keys():
        #     if kore > num_kore:
        #         num_kore = kore
        #         shipyard_pos = candidate_dict[0]
        #         kore_pos[1]

        return self._pos_to_plan(shipyard_pos, kore_pos)


class HeadQuarter:

    def __init__(self, message):
        self.me = message['me']
        if message['num_enemies'] == 1:
            self.enemy1 = message['enemy_1']
        if message['num_enemies'] == 3:
            self.enemy1 = message['enemy_1']
            self.enemy2 = message['enemy_2']
            self.enemy3 = message['enemy_3']
        self.board_kore = message['board_kore']
        self.turn = message['turn']
        self.spawn_cost = message['spawn_cost']
        self.convert_cost = message['convert_cost']
        self.episodes = message['episodes']
        self.num_enemies = message['num_enemies']

        self.utility = GetInfoUtility()

    def launch_fleet(self, shipyard_id, ship_count, flight_plan):
        if flight_plan != "":
            return {shipyard_id: kore_launch_fleet(ship_count, flight_plan)}
        return {}

    def spawn(self, shipyard_id, num):
        if self.me['kore'] > self.spawn_cost:
            return {shipyard_id: kore_spawn_ships(num)}
        return {}

    def get_command(self):
        # greedy search -> build shipyard -> 
        # shipyards which far away from enemies are responsible for collection, sent ship to front
        # the one near the enemies responsible for attack, defense
        for shipyard_id in self.me['shipyard'].keys():
            ship_cnt = self.me['shipyard'][shipyard_id]['ship_count']
            if ship_cnt > 20:
                num_ship, plan = self.utility.greedy_kore_search(
                    self.me['shipyard'][shipyard_id]['position'], self.board_kore, ship_cnt)
                return self.launch_fleet(shipyard_id, num_ship, plan)
            return self.spawn(shipyard_id, 2)
        # return {}
