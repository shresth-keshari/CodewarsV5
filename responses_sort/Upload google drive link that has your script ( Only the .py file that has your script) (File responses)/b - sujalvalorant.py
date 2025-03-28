import random
from teams.helper_function import Troops, Utils

team_name = "Sujal"
troops = [
    Troops.wizard, Troops.minion, Troops.musketeer,
    Troops.dragon, Troops.barbarian, Troops.valkyrie,
    Troops.prince, Troops.giant
]
deploy_list = Troops([])
team_signal = "h, Prince, Knight, Barbarian, Princess"

def deploy(arena_data: dict):
    """
    Deployment function that determines the best troop to deploy
    based on the current state of the arena.
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    global team_signal
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    
    # Update Team Signal with new opponent troop names
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
        if troop.name not in current_names:
            team_signal = f"{team_signal}, {troop.name}" if team_signal else troop.name
    
    # Analyze Opponent's Deck Composition
    opponent_air = {"Minion", "Dragon", "Musketeer"}
    opponent_ground = {"Prince", "Knight", "Barbarian", "Princess"}
    
    tokens = [token.strip() for token in team_signal.split(",") if token.strip() != "h"]
    count_air = sum(1 for token in tokens if token in opponent_air)
    count_ground = sum(1 for token in tokens if token in opponent_ground)
    
    if count_ground > count_air:
        recommended_counter = "air"    # Counter ground with air units
    elif count_air > count_ground:
        recommended_counter = "ground" # Counter air with ground units
    else:
        recommended_counter = None     # No clear preference
    
    # Score Our Troops (only from deployable troops)
    deployable = my_tower.deployable_troops
    troop_data = {
        Troops.wizard:    {"score": 3, "category": "air",    "name": "Wizard"},
        Troops.minion:    {"score": 4, "category": "air",    "name": "Minion"},
        Troops.musketeer: {"score": 3, "category": "ground", "name": "Musketeer"},
        Troops.dragon:    {"score": 5, "category": "air",    "name": "Dragon"},
        Troops.barbarian: {"score": 4, "category": "ground", "name": "Barbarian"},
        Troops.valkyrie:  {"score": 4, "category": "air",    "name": "Valkyrie"},
        Troops.prince:    {"score": 5, "category": "ground", "name": "Prince"},
        Troops.giant:     {"score": 4, "category": "ground", "name": "Giant"}
    }
    
    bonus = 3  # Bonus for matching the recommended counter strategy
    best_troop = None
    best_score = -1
    
    # Loop over our full troop list, but only consider those that are deployable
    for troop in troops:
        if troop not in deployable:
            continue
        base = troop_data[troop]["score"]
        cat = troop_data[troop]["category"]
        score = base + (bonus if recommended_counter and cat == recommended_counter else 0)
        if score > best_score:
            best_score = score
            best_troop = troop

    # **ALL TROOPS DEPLOY AT CENTER (0,0)**
    if best_troop is not None:
        deploy_list.list_.append((best_troop, (0, 0)))
    else:
        # **Fallback:** Deploy the first available troop at center (0,0)
        if deployable:
            deploy_list.list_.append((deployable[0], (0, 0)))
