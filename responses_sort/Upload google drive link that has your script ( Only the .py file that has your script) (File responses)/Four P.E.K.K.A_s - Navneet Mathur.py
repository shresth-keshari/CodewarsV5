import random
from teams.helper_function import Troops, Utils

team_name = "Four P.E.K.K.A.s"
troops = [
    Troops.minion, Troops.skeleton, Troops.barbarian, Troops.dragon, Troops.prince,
    Troops.giant, Troops.valkyrie, Troops.wizard
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
    opp_troops = arena_data["OppTroops"]

    # --- Update Team Signal with Opponent's Troops ---
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
        if troop.name not in current_names:
            team_signal += ", " + troop.name if team_signal else troop.name

    deployable = my_tower.deployable_troops

    # --- CYCLE FAST--
    cycle_options = [Troops.dragon, Troops.minion, Troops.skeleton]
    for troop in cycle_options:
        if troop in deployable:
            deploy_list.list_.append((troop, (random_x(-10, 10), 0)))
            return    

    # --- DEFENSE ---
    defense_priority = [
        (Troops.wizard, ["air", "swarms"]),
        (Troops.dragon, ["air"]),
        (Troops.prince, ["single-target", "prince","tanks"]),
        (Troops.valkyrie, ["swarms"]),
        (Troops.archer, ["tanks"]),
        (Troops.skeleton, ["single-target", "prince"]),
        (Troops.minion, ["air"]),
    ]

    for troop, counters in defense_priority:
        if troop in deployable:
            deploy_list.list_.append((troop, (random_x(-10, 10), 0)))
            return  # **Deploy ONLY ONE troop per defense cycle.**

    # --- ATTACK: GIANT + VALKYRIE PUSH ---
    if Troops.giant in deployable:
        deploy_list.list_.append((Troops.giant, (random_x(-10, 10), 0)))
    if Troops.valkyrie in deployable:
        deploy_list.list_.append((Troops.valkyrie, (random_x(-10, 10), 0)))

       
       
        return  # **No need to deploy more after attacking.**