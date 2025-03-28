import random
import time
from teams.helper_function import Troops, Utils

team_name = "SyntaxGods"
troops = [
    Troops.wizard, Troops.minion, Troops.archer, Troops.musketeer,
    Troops.dragon, Troops.knight, Troops.prince, Troops.valkyrie
]
deploy_list = Troops([])
team_signal = "h"

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def deploy(arena_data: dict):
    """
    DON'T TEMPER DEPLOY FUNCTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    global team_signal
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    my_troops = arena_data["MyTroops"]
    current_time = time.time()

    # --- Update Team Signal ---
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
        if troop.name not in current_names:
            team_signal = team_signal + ", " + troop.name if team_signal else troop.name
            if len(team_signal) > 200:
                team_signal = team_signal[:200]

    # --- Score Our Troops (only from deployable troops) ---
    deployable = my_tower.deployable_troops

    if len(opp_troops)==0:
        if Troops.wizard in deployable:
            deploy_list.list_.append((Troops.wizard, (0, 40)))
        if Troops.prince in deployable:
            deploy_list.list_.append((Troops.prince, (0, 50)))

    # --- Defensive Strategy ---
    for opp_troop in opp_troops:
        if opp_troop.name == "Minion":
            counter_troops = [Troops.dragon, Troops.archer, Troops.musketeer, Troops.wizard]
        elif opp_troop.name == "Knight":
            counter_troops = [Troops.knight, Troops.musketeer, Troops.minion, Troops.wizard, Troops.valkyrie]
        elif opp_troop.name == "Skeleton":
            counter_troops = [Troops.wizard, Troops.dragon, Troops.valkyrie, Troops.minion, Troops.musketeer]
        elif opp_troop.name == "Dragon":
            counter_troops = [Troops.dragon, Troops.wizard, Troops.musketeer,Troops.minion]
        elif opp_troop.name == "Valkyrie":
            counter_troops = [Troops.wizard, Troops.minion, Troops.dragon, Troops.prince, Troops.musketeer]
        elif opp_troop.name == "Musketeer":
            counter_troops = [Troops.wizard, Troops.minion, Troops.valkyrie, Troops.knight,Troops.prince]
        elif opp_troop.name == "Prince":
            counter_troops = [Troops.wizard, Troops.knight, Troops.musketeer, Troops.archer, Troops.valkyrie, Troops.minion]
        elif opp_troop.name == "Barbarian":
            counter_troops = [Troops.wizard, Troops.prince, Troops.musketeer, Troops.valkyrie, Troops.knight]
        elif opp_troop.name == "Balloon":
            counter_troops = [Troops.wizard, Troops.dragon, Troops.archer, Troops.minion]
        elif opp_troop.name == "Archer":
            counter_troops = [Troops.wizard, Troops.musketeer, Troops.minion]
        else:
            counter_troops = []

        for troop in counter_troops:
            if troop in deployable:
                deploy_position = (random_x(-5, 5), 5)
                deploy_list.list_.append((troop, deploy_position))
                break

    # if len(opp_troops)==0:
    #     if Troops.wizard in deployable:
    #         deploy_list.list_.append((Troops.wizard, (0, 40)))
    #     if Troops.prince in deployable:
    #         deploy_list.list_.append((Troops.prince, (0, 50)))

    if random.random() < 0.75 or not opp_troops:
        attack_troops = [
            Troops.prince,  # Primary attacker
            Troops.dragon,  # Strong air unit
            Troops.wizard,  # Area damage
            Troops.valkyrie  # Melee splash
        ]

        for troop in attack_troops:
            if troop in deployable:
                x_pos = random.randint(-5, 5)  # Wider attack range
                deploy_list.list_.append((troop, (x_pos, 50)))  # Deeper in enemy territory
                return

    # --- Offensive Strategy ---
    if not deploy_list.list_:
        if Troops.wizard in deployable:
            deploy_list.list_.append((Troops.wizard, (0, 40)))
        elif Troops.prince in deployable:
            deploy_list.list_.append((Troops.prince, (0, 50)))
        else:
            for troop in deployable:
                deploy_list.list_.append((troop, (0, 50)))
                break

    # --- Deploy Troops Not Used for More Than 10 Seconds ---
    for troop in my_troops:
        if hasattr(troop, 'last_deployed_time') and current_time - troop.last_deployed_time > 15:
            deploy_list.list_.append((troop, (0, 25)))
            troop.last_deployed_time = current_time  # Update last deployed time
