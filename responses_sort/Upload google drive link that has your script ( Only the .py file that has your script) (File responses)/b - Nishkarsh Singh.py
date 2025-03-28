import random
from teams.helper_function import Troops, Utils

team_name = "Synapse"
troops = [Troops.wizard,Troops.minion,Troops.musketeer,Troops.giant,Troops.dragon,Troops.skeleton,Troops.balloon,Troops.valkyrie]
deploy_list = Troops([])
team_signal = ""

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def deploy(arena_data:dict):
    """
    DON'T TEMPER DEPLOY FUCNTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    global team_signal
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    game_time = arena_data["MyTower"].game_timer
    elixir = arena_data["MyTower"].total_elixir  # Get available elixir

    # --- Update Team Signal ---
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
        if troop.name not in current_names:
            team_signal = team_signal + ", " + troop.name if team_signal else troop.name

    # --- Define Counter Strategies ---
    counters = {
        "Giant": [Troops.skeleton, Troops.minion],  # Swarm counters
        "Balloon": [Troops.archer, Troops.minion],  # Anti-air units
        "Prince": [Troops.skeleton, Troops.valkyrie],  # Disrupt charge
        "Dragon": [Troops.wizard, Troops.archer],  # Anti-air single-target
    }

    # --- Deploy Based on Time ---
    deployable = my_tower.deployable_troops
    deploy_position = (random_x(-10, 10), 20)  # Default deploy position

    for troop in deployable:
        if troop == Troops.wizard:
            deploy_list.list_.append((Troops.wizard, deploy_position))

    for troop in deployable:
        if troop == Troops.musketeer:
            deploy_list.list_.append((Troops.musketeer, deploy_position))

    if game_time < 40:  # Defense Mode
        for enemy in opp_troops:
            if enemy.name in counters:
                for counter_troop in counters[enemy.name]:
                    if counter_troop in deployable:
                        deploy_list.list_.append((counter_troop, deploy_position))
                       
        # If no specific counter, deploy a defensive unit
        for troop in [Troops.minion, Troops.musketeer, Troops.skeleton]:
            if troop in deployable:
                deploy_list.list_.append((troop, deploy_position))
               

    else:  
        for enemy in opp_troops:
            if enemy.name in counters:
                for counter_troop in counters[enemy.name]:
                    if counter_troop in deployable:
                        deploy_list.list_.append((counter_troop, deploy_position))
        
        for troop in deployable:
         if troop == Troops.musketeer:
            deploy_list.list_.append((Troops.musketeer, deploy_position))

        for troop in [Troops.giant,Troops.wizard,Troops.balloon,Troops.skeleton, Troops.dragon,Troops.minion,Troops.musketeer,Troops.skeleton]:
            if troop in deployable:
                deploy_list.list_.append((troop, deploy_position))
               
