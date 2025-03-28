import random
import math
from teams.helper_function import Troops, Utils

team_name = "I_sell_kids"

troops = [
    Troops.musketeer, Troops.prince, Troops.skeleton, Troops.wizard,
    Troops.dragon, Troops.valkyrie, Troops.knight, Troops.giant
]

deploy_list = Troops([])
team_signal = "h"

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def calculate_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def deploy(arena_data: dict):
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    return 