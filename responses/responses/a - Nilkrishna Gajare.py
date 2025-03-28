import random
import math
from teams.helper_function import Troops, Utils

team_name = "nand"

troops = [
    Troops.archer, Troops.knight, Troops.skeleton, Troops.wizard,
    Troops.dragon, Troops.musketeer, Troops.minion, Troops.barbarian
]

deploy_list = Troops([])
team_signal = "h"

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def calculate_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])*2 + (pos1[1] - pos2[1])*2)

def deploy(arena_data: dict):
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    

    global team_signal
    my_troop = arena_data["MyTroops"]
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    opp_tower = arena_data.get("OppTower")
    deployable = getattr(my_tower, "deployable_troops", [])
    
    under_attack = any(
        calculate_distance(troop.position, my_tower.position) < 8 for troop in opp_troops if hasattr(troop, "position")
    )
    air_threat = any(troop.type == "Air" for troop in opp_troops if hasattr(troop, "type"))
    ground_threat = any(troop.type == "Ground" for troop in opp_troops if hasattr(troop, "type"))
    swarm_threat = any(troop.name in ["Skeleton", "Barbarian"] for troop in opp_troops if hasattr(troop, "name"))
    x=random.random()*10
    
    if Troops.wizard in deployable:
        if not under_attack:
             y=40
        else:
             y=10
        deploy_list.list_.append((Troops.wizard,( 10,y )))
    else:
        if under_attack:
            for priority in [Troops.dragon, Troops.archer, Troops.minion, Troops.musketeer, Troops.skeleton, Troops.knight, Troops.barbarian]:
                    if priority in deployable:
                        deploy_list.list_.append((priority, (x, 10)))
                    # Cheap distraction
        else:
           for priority in [Troops.dragon, Troops.archer, Troops.minion, Troops.musketeer, Troops.skeleton, Troops.knight, Troops.barbarian]:
                    if priority in deployable:
                        deploy_list.list_.append((priority, (x, 50)))
    if not deploy_list.list_ and deployable:
        for priority in [Troops.wizard, Troops.dragon, Troops.archer, Troops.minion, Troops.musketeer, Troops.skeleton, Troops.knight, Troops.barbarian]:
            if priority in deployable:
                deploy_list.list_.append((priority, (x, 0)))
                break

