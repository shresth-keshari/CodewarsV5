import random
from teams.helper_function import Troops, Utils

team_name = "The Bug Hunters"
troops = [
    Troops.minion, Troops.skeleton, Troops.knight, Troops.archer, Troops.dragon,
    Troops.barbarian, Troops.valkyrie, Troops.wizard
]
deploy_list = Troops([])
team_signal = "h"

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def deploy(arena_data: dict):
    """
    DON'T TAMPER WITH DEPLOY FUNCTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    global team_signal
    my_tower = arena_data["MyTower"]
    deployable = my_tower.deployable_troops

    defense_priority = [
        Troops.valkyrie,
        Troops.wizard,
        Troops.archer, 
        Troops.knight,
        Troops.skeleton,
        Troops.minion,
        Troops.barbarian,
        Troops.dragon,
    ]

    for troop in defense_priority:
        if troop in deployable:
            deploy_list.list_.append((troop, (random_x(-10, 10), 0)))
            return

    cycle_options = [Troops.archer, Troops.minion, Troops.skeleton]
    for troop in cycle_options:
        if troop in deployable:
            deploy_list.list_.append((troop, (random_x(-10, 10), 0)))
            return
