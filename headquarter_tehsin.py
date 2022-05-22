from kore_act_api import kore_launch_fleet, kore_spawn_ships
import math
import random

import numpy as np


class GetInfoUtility:

    def __init__(self, board_kore):
        self.board_kore = board_kore
        self.max_plan_len = 0

    def _get_path_kore(self, start, plan):
        num = 0
        cur = list(start)
        path_plan = []
        for idx, p in enumerate(plan):
            if isinstance(p, str):
                path_plan.append(p)
            else:
                for i in range(p):
                    path_plan.append(plan[idx-1])
        for p in path_plan:
            if p == "N":
                cur[1] = (cur[1]+1) if cur[1] < 20 else 0
            elif p == "S":
                cur[1] = (cur[1]-1) if cur[1] > 0 else 20
            elif p == "W":
                cur[0] = (cur[0]-1) if cur[0] > 0 else 20
            elif p == "E":
                cur[0] = (cur[0]+1) if cur[0] < 20 else 0
            num += self.board_kore[cur[1]][cur[0]]
        return num

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
        return (interval-1)

    def _pos_to_plan(self, pos_begin, pos_end):
        """Arrive to the destination with the shortest flight plan"""

        x_interval = self._get_interval(pos_end[0], pos_begin[0])
        y_interval = self._get_interval(pos_end[1], pos_begin[1])

        forward_x, backward_x = "", ""
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
        x_interval, y_interval = abs(x_interval), abs(y_interval)
        if (random.randint(0, 50) % 2) == 0:
            forward_plan = forward_x + \
                str(x_interval) + forward_y + str(y_interval)
            backward_plan = backward_y + str(y_interval) + backward_x
            kore_plan = [forward_x, x_interval, forward_y,
                         y_interval, backward_y, y_interval, backward_x]
        else:
            forward_plan = forward_y + \
                str(y_interval) + forward_x + str(x_interval)
            backward_plan = backward_x + str(x_interval) + backward_y
            kore_plan = [forward_y, y_interval, forward_x,
                         x_interval, backward_x, x_interval, backward_y]
        flight_plan += (forward_plan + backward_plan)
        if len(flight_plan) <= self.max_plan_len and isinstance(flight_plan, str) and flight_plan[0].isalpha():
            return self._required_ship(flight_plan), self._get_path_kore(pos_begin, kore_plan), flight_plan
        return 0, 0, ""

    def _get_search_pos(self, me_pos, enemy_pos):
        """Remove the position that around enemies (+5~-5)"""
        res = []
        size = len(self.board_kore)
        search_pos = np.ones((size, size))
        h_list, v_list = [], []
        for pos in enemy_pos:
            for i in range(-5, 6, 1):
                if (pos[0]+i) < 0:
                    x = (21+(pos[0]+i))
                elif (pos[0]+i) > 20:
                    x = ((pos[0]+i)-21)
                else:
                    x = (pos[0]+i)

                if (pos[1]+i) < 0:
                    y = (21+(pos[1]+i))
                elif (pos[1]+i) > 20:
                    y = ((pos[1]+i)-21)
                else:
                    y = (pos[1]+i)
                h_list.append(x)
                v_list.append(y)
        for i in h_list:
            for j in v_list:
                search_pos[j, i] = 0
        search_pos[me_pos[1], me_pos[0]] = 0

        for i in range(size):
            for j in range(size):
                if search_pos[i, j] == 1 and self.board_kore[i][j] > 10:
                    res.append([i, j])
        return res

    def greedy_kore_search(self, shipyard_pos, ship_cnt, enemy_pos):
        """Get the path which contains the most kore"""

        self.max_plan_len = (math.floor(2*math.log(ship_cnt)) + 1)

        search_pos = self._get_search_pos(shipyard_pos, enemy_pos)
        res_ship, res_plan, max_kore = 0, "", 0
        for pos in search_pos:
            num_ship, num_kore, plan = self._pos_to_plan(shipyard_pos, pos)
            if num_kore > max_kore:
                max_kore = num_kore
                res_ship = num_ship
                res_plan = plan
        return res_ship, res_plan


class HeadQuarter:

    def __init__(self, message):
        self.me = message['me']
        self.enemy_shipyard_pos = []
        if message['num_enemies'] == 1:
            self.enemy1 = message['enemy_1']
            self.enemy_shipyard_pos = [self.enemy1['shipyard'][shipyard]['position']
                                       for shipyard in self.enemy1['shipyard'].keys()]
        if message['num_enemies'] == 3:
            self.enemy1 = message['enemy_1']
            self.enemy2 = message['enemy_2']
            self.enemy3 = message['enemy_3']
            self.enemy_shipyard_pos += [self.enemy1['shipyard'][shipyard]['position']
                                        for shipyard in self.enemy1['shipyard'].keys()]
            self.enemy_shipyard_pos += [self.enemy2['shipyard'][shipyard]['position']
                                        for shipyard in self.enemy2['shipyard'].keys()]
            self.enemy_shipyard_pos += [self.enemy3['shipyard'][shipyard]['position']
                                        for shipyard in self.enemy3['shipyard'].keys()]
        self.board_kore = message['board_kore']
        self.turn = message['turn']
        self.spawn_cost = message['spawn_cost']
        self.convert_cost = message['convert_cost']
        self.episodes = message['episodes']
        self.num_enemies = message['num_enemies']

        self.utility = GetInfoUtility(self.board_kore)

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
            if ship_cnt > 15:
                num_ship, plan = self.utility.greedy_kore_search(
                    self.me['shipyard'][shipyard_id]['position'], ship_cnt, self.enemy_shipyard_pos)
                if len(plan) > 0:
                    return self.launch_fleet(shipyard_id, num_ship, plan)
                return self.spawn(shipyard_id, self.me['shipyard'][shipyard_id]['max_spawn']) 
            return self.spawn(shipyard_id, self.me['shipyard'][shipyard_id]['max_spawn'])
        # return {}
