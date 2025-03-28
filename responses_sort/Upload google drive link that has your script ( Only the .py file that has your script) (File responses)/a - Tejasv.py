import random
from teams.helper_function import Troops, Utils

team_name = "V-TAS Velocity"
troops = [
    Troops.knight, Troops.minion, Troops.giant, Troops.prince,
    Troops.dragon, Troops.skeleton, Troops.valkyrie, Troops.wizard
]

deploy_list = Troops([]) 
team_signal = "h, Prince, Knight, Barbarian, Princess"

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
    
    # Track if we're waiting for wizard (local variable instead of global)
    waiting_for_wizard = any(troop.name == "Giant" for troop in my_troops) and \
                        not any(troop.name == "Wizard" for troop in my_troops)
    
    # Update team_signal based on enemy troops
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
        if troop.name not in current_names:
            team_signal = team_signal + ", " + troop.name if team_signal else troop.name
    
    deployable = my_tower.deployable_troops
    if not deployable:
        return

    # If waiting for Wizard, check if Wizard is available before deploying anything else
    if waiting_for_wizard:
        if Troops.wizard in deployable:
            deploy_position = (random_x(-5, 5), 0)
            deploy_list.list_.append((Troops.wizard, deploy_position))
            return
        else:
            return  # Wait until Wizard is available

    # Custom Counter Logic for Specific Enemy Troops
    counter_dict = {
        "Knight": [Troops.prince, Troops.valkyrie],
        "Giant": [Troops.giant, Troops.knight],
        "Minion": [Troops.dragon, Troops.archer],
        "Dragon": [Troops.dragon, Troops.minion],
        "Balloon": [Troops.minion, Troops.minion],
        "Skeleton": [Troops.valkyrie, Troops.prince],
        "Valkyrie": [Troops.prince, Troops.dragon],
        "Musketeer": [Troops.knight, Troops.prince],
        "Prince": [Troops.skeleton, Troops.knight],
        "Barbarian": [Troops.valkyrie, Troops.dragon],
        "Archer": [Troops.skeleton, Troops.knight],
        "Wizard": [Troops.wizard, Troops.knight, Troops.minion]
    }
    
    best_troop = None
    for enemy in opp_troops:
        if enemy.name in counter_dict:
            for counter in counter_dict[enemy.name]:
                if counter in deployable:
                    best_troop = counter
                    break
        if best_troop:
            break
    
    # If no direct counter is found, revert to general strategy
    if not best_troop:
        air_counters = {Troops.minion, Troops.wizard}
        ground_counters = {Troops.giant, Troops.wizard}
    
        opp_air_units = sum(1 for t in opp_troops if t.name in {"Minion", "Dragon", "Balloon"})
        opp_ground_units = sum(1 for t in opp_troops if t.name in {"Knight", "Barbarian", "Giant", "Wizard"})
    
        preferred_category = air_counters if opp_air_units > opp_ground_units else ground_counters
    
        for troop in deployable:
            if troop in preferred_category:
                best_troop = troop
                break
    
        if not best_troop:
            for troop in deployable:
                best_troop = troop
                break
    
    # Attack Priority (Wizard > Knight > Dragon)
    attack_priority = [Troops.wizard, Troops.knight, Troops.dragon, Troops.valkyrie, Troops.prince, Troops.skeleton, Troops.minion, Troops.giant]
    attack_priority_troop = next((troop for troop in attack_priority if troop in deployable), None)
    
    # Adjusting Attack and Defense Strategy Based on Enemy Count
    enemy_count = len(opp_troops)
    attack = False
    
    if enemy_count < 2:
        attack = True  # Always attack if less than 2 enemy troops
    elif 2 <= enemy_count <= 3:
        attack = random.random() < 0.60 # Attack with 50% probability
    else:
        attack = False  # Only counter if more than 4 enemy troops
    
    # If no effective defense is available, deploy skeletons as a last resort
    if not best_troop and Troops.skeleton in deployable:
        best_troop = Troops.skeleton

    # Deploy troop based on attack or defense logic
    best_troop = attack_priority_troop if attack else best_troop
    
    if best_troop:
        deploy_position = (random_x(-15, 15), 0) if best_troop in {Troops.knight, Troops.skeleton} else (random_x(-5, 5), 0)
        deploy_list.list_.append((best_troop, deploy_position))