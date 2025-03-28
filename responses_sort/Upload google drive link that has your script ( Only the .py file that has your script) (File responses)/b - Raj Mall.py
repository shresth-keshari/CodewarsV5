import random
from teams.helper_function import Troops, Utils

team_name = "Kaju Katlis"
troops = [
    Troops.giant, Troops.balloon, Troops.wizard, Troops.musketeer,
    Troops.valkyrie, Troops.dragon, Troops.barbarian, Troops.skeleton
]
deploy_list = Troops([])

# Given team_signal (initial garbage values are allowed here)
team_signal = "h, Prince, Knight, Barbarian, Princess"

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def deploy(arena_data: dict):
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    global team_signal
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    
    # --- Update team_signal (append new opponent troop names, avoid duplicates) ---
    # Use the same approach as the sample: re-parse the full string every time.
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
        if troop.name not in current_names:
            team_signal = team_signal + ", " + troop.name if team_signal else troop.name
    
    # --- Analyze Opponent's Deck Composition ---
    # Define our opponent groups.
    TANK = {"Giant", "Valkyrie", "Prince", "Knight"}
    DPS = {"Musketeer", "Wizard", "Balloon", "Archer"}
    SWARM = {"Skeleton", "Minion", "Barbarian", "Dragon"}
    
    # Split team_signal into tokens, ignoring the placeholder "h"
    tokens = [token.strip() for token in team_signal.split(",") if token.strip() != "h"]
    
    enemy_tanks = sum(1 for token in tokens if token in TANK)
    enemy_dps   = sum(1 for token in tokens if token in DPS)
    enemy_swarm = sum(1 for token in tokens if token in SWARM)
    
    # --- Determine Recommended Counter Group ---
    # If enemy tanks dominate, counter with DPS;
    # if enemy DPS are most, counter with SWARM; otherwise, counter with TANK.
    if enemy_tanks > enemy_dps and enemy_tanks > enemy_swarm:
        recommended_group = DPS
    elif enemy_dps > enemy_swarm:
        recommended_group = SWARM
    else:
        recommended_group = TANK

    # --- Score Our Troops (only those deployable from our tower) ---
    deployable = my_tower.deployable_troops
    troop_data = {
        Troops.giant:     {"score": 5, "group": "TANK", "name": "Giant"},
        Troops.balloon:   {"score": 5, "group": "DPS",  "name": "Balloon"},
        Troops.wizard:    {"score": 3, "group": "DPS",  "name": "Wizard"},
        Troops.musketeer: {"score": 3, "group": "DPS",  "name": "Musketeer"},
        Troops.valkyrie:  {"score": 4, "group": "TANK", "name": "Valkyrie"},
        Troops.dragon:    {"score": 2, "group": "SWARM","name": "Dragon"},
        Troops.barbarian: {"score": 3, "group": "SWARM","name": "Barbarian"},
        Troops.skeleton:  {"score": 2, "group": "SWARM","name": "Skeleton"}
    }
    
    bonus = 3  
    best_troop = None
    best_score = -1

    # Loop over our full troop list but only consider deployable ones.
    for troop in troops:
        if troop not in deployable:
            continue
        base = troop_data[troop]["score"]
        # Add bonus if the troop's name is in the recommended group
        score = base + (bonus if troop_data[troop]["name"] in recommended_group else 0)
        if score > best_score:
            best_score = score
            best_troop = troop

    # --- Deployment Position ---
    if best_troop is not None:
        if best_troop == Troops.balloon:
            # Deploy balloon further forward (y=50)
            deploy_position = (random_x(-25, 25), 50)
        else:
            # Other troops deploy at y=0
            deploy_position = (random_x(-25, 25), 0)
        deploy_list.list_.append((best_troop, deploy_position))
    else:
        # Fallback: If no troop qualifies, deploy the first available troop.
        if deployable:
            deploy_list.list_.append((deployable[0], (0, 0)))
