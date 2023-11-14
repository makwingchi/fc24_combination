import math
import copy
import pprint

import numpy as np


def calculate_overall_ratings(player_list):
    total_num = np.sum(player_list)
    assert total_num == 11, f"total number of player = {total_num}, which is not equal to 11!"

    rating_list = [i for i in range(80, 91)]

    player_arr = np.array(player_list)
    rating_arr = np.array(rating_list)

    ratings_avg = np.sum(player_arr * rating_arr) / 11

    ratings_diff = rating_arr - ratings_avg
    pos_diff = ratings_diff >= 0

    excess = ratings_diff * player_arr
    excess = np.sum(excess[pos_diff])

    total_plus_excess = round(ratings_avg * 11 + excess)
    avg_total_plus_excess = total_plus_excess / 11

    return math.floor(avg_total_plus_excess)


def generate_combinations(player_list, target):
    total_num = np.sum(player_list)
    assert total_num >= 11, f"total number of player = {total_num}, which is smaller than 11!"

    combinations = []
    curr_players = [0 for i in range(11)]

    helper(curr_players, player_list, combinations, 0)

    solid_combinations = []

    for combination in combinations:
        if calculate_overall_ratings(combination) == target:
            solid_combinations.append(combination)

    return solid_combinations


def helper(curr_players, player_list, combinations, idx):
    total_players = np.sum(curr_players)

    if total_players >= 11 or idx == len(curr_players):
        if total_players == 11:
            combinations.append(copy.deepcopy(curr_players))
        return

    for i in range(player_list[idx] + 1):
        curr_players[idx] = i
        helper(curr_players, player_list, combinations, idx + 1)
        curr_players[idx] = 0


def calculate_total_price(player_list, price_list):
    player_arr = np.array(player_list)
    price_arr = np.array(price_list)

    return np.sum(player_arr * price_arr)


def str_generator(combinations):
    rating_list = [i for i in range(80, 91)]
    ret = []

    for idx, combination in enumerate(combinations):
        ret.append(f"{rating_list[idx]}: {combination}")

    return ", ".join(ret).strip()


def sort_by_price(combinations, price_list):
    _map = {}
    for combination in combinations:
        formatted_str = str_generator(combination)
        _map[formatted_str] = calculate_total_price(combination, price_list)

    return sorted(_map.items(), key=lambda x: x[1], reverse=False)


def get_cheapest(player_list, price_list, target):
    comb = generate_combinations(player_list, target)
    return sort_by_price(comb, price_list)


if __name__ == "__main__":
    prices = [650, 650, 750, 1300, 3500, 7500, 13000, 17500, 25000, 37750, 51000]
    target_rating = 85

    num_80s = 10
    num_81s = 11
    num_82s = 17
    num_83s = 21
    num_84s = 5
    num_85s = 7
    num_86s = 6
    num_87s = 8
    num_88s = 6
    num_89s = 3
    num_90s = 0

    player_list = [num_80s, num_81s, num_82s, num_83s, num_84s, num_85s, num_86s, num_87s, num_88s, num_89s, num_90s]
    cheapest = get_cheapest(player_list, prices, target_rating)

    printer = pprint.PrettyPrinter(indent=0)
    printer.pprint(cheapest[:20])