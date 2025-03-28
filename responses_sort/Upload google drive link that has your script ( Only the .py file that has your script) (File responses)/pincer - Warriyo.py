import random
from teams.helper_function import Troops, Utils

team_name = "pincer2"
troops = [
    Troops.wizard, Troops.prince, Troops.minion, Troops.skeleton,
    Troops.dragon, Troops.giant, Troops.valkyrie, Troops.barbarian
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
    my_elixir=1
    # --- Update Team Signal ---
    # Add new opponent troop names (avoid duplicates).
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
        if troop.name not in current_names:
            team_signal = team_signal + ", " + troop.name if team_signal else troop.name
    # print(f"Team Signal: {team_signal}")
    
    # --- Analyze Opponent's Deck Composition ---
    # Define opponent categories.
    opponent_air = {"Minion", "Dragon", "Musketeer"}
    opponent_ground = {"Prince", "Knight", "Barbarian", "Princess"}
    
    tokens = [token.strip() for token in team_signal.split(",") if token.strip() != "h"]
    count_air = sum(1 for token in tokens if token in opponent_air)
    count_ground = sum(1 for token in tokens if token in opponent_ground)
    
    if count_ground < count_air:
        recommended_counter = "air"    # Counter ground with air units.
    elif count_air < count_ground:
        recommended_counter = "ground" # Counter air with ground units.
    else:
        recommended_counter = None     # No clear preference.
    
    # --- Score Our Troops (only from deployable troops) ---
    deployable = my_tower.deployable_troops
    # Define base scores and categories for our troops.
    troop_data = {
        Troops.wizard:    {"score": 3, "category": "air",    "name": "Wizard"},
        Troops.minion:    {"score": 2, "category": "air",    "name": "Minion"},
        Troops.prince:    {"score": 4, "category": "ground", "name": "Prince"},
        Troops.musketeer:     {"score": 3, "category": "ground", "name": "Musketeer"},
        Troops.dragon:    {"score": 5, "category": "air",    "name": "Dragon"},
        Troops.skeleton:  {"score": 2, "category": "ground", "name": "Skeleton"},
        Troops.valkyrie:   {"score": 4, "category": "air",    "name": "Valkyrie"},
        Troops.barbarian: {"score": 3, "category": "ground", "name": "Barbarian"}
    }
    troop_info = {
        Troops.wizard: {"elixir": 5, "health": 1100, "damage": 410, "velocity": 2, "type": "ground", "target_type": {"air": True, "ground": True, "building": True}, "splash_range": 1, "attack_speed": 1, "number": 1 },
        Troops.minion:    {"elixir": 3, "health": 252, "damage": 129, "velocity": 3, "type": "air", "target_type": {"air": True, "ground": True, "building": True}, "splash_range": 0, "attack_speed": 1, "number": 3 },
        Troops.prince:    {"elixir": 5, "health": 1920, "damage": 392, "velocity": 3, "type": "ground", "target_type": {"air": False, "ground": True, "building": False}, "splash_range": 0, "attack_speed": 1, "number": 1 },
        Troops.giant:     {"elixir": 5, "health": 5423, "damage": 337, "velocity": 1, "type": "ground", "target_type": {"air": False, "ground": False, "building": True}, "splash_range": 0, "attack_speed": 3, "number": 1 },
        Troops.dragon:    {"elixir": 4, "health": 1267, "damage": 176, "velocity": 3, "type": "air", "target_type": {"air": True, "ground": True, "building": True}, "splash_range": 0, "attack_speed": 1, "number": 1 },
        Troops.skeleton:  {"elixir": 3, "health": 89, "damage": 89, "velocity": 3, "type": "ground", "target_type": {"air": False, "ground": True, "building": True}, "splash_range": 0, "attack_speed": 1, "number": 10 },
        Troops.valkyrie:   {"elixir": 4, "health": 2097, "damage": 195, "velocity": 2, "type": "ground", "target_type": {"air": False, "ground": True, "building": False}, "splash_range": 1, "attack_speed": 1, "number": 1 },
        Troops.barbarian: {"elixir": 3, "health": 736, "damage": 161, "velocity": 2, "type": "ground", "target_type": {"air": False, "ground": True, "building": False}, "splash_range": 0, "attack_speed": 2, "number": 3 },
        Troops.archer: {"elixir": 3, "health": 334, "damage": 118, "velocity": 2, "type": "ground", "target_type": {"air": True, "ground": True, "building": True}, "splash_range": 0, "attack_speed": 1, "number": 2 },
        Troops.musketeer: {"elixir": 4, "health": 792, "damage": 239, "velocity": 2, "type": "ground", "target_type": {"air": True, "ground": True, "building": True}, "splash_range": 0, "attack_speed": 2, "number": 1 },
        Troops.balloon: {"elixir": 5, "health": 2226, "damage": 424, "velocity": 2, "type": "air", "target_type": {"air": False, "ground": False, "building": True}, "splash_range": 1, "attack_speed": 2, "number": 1 }
    }# Bonus for matching the recommended counter strategy.
    bonus=1.6
    best_troop = None
    best_score = -1
    # Loop over our full troop list, but only consider those that are deployable.
    for troop in troops:
        if troop not in deployable:
            continue
        c=troop_info[troop]
        score=c["damage"]*(c["velocity"]**0.5)/(c["attack_speed"]*(c["elixir"]**0.5))
        if c["target_type"][recommended_counter]: score=score*bonus
        if score > best_score:
            best_score = score
            best_troop = troop
    if len(arena_data["MyTroops"])-len(opp_troops)>3:
        p=0
        for troopc in arena_data["MyTroops"]:
            if troopc.name=="Giant": p=1
        if p==1 and Troops.prince in deployable: best_troop="Prince"
        elif Troops.giant in deployable: best_troop="Giant"
    k=0
    for troopo in opp_troops:
            if troopo.position[1]<40:
                k=1
                if troopo.type=="air":
                    if Troops.dragon in deployable: best_troop="Dragon"
                    elif Troops.minion in deployable: best_troop="Minion"
                    elif Troops.wizard in deployable: best_troop="Wizard"
                else:
                    if Troops.skeleton in deployable: best_troop="Skeleton"
                    elif Troops.valkyrie in deployable: best_troop="Valkyrie"
                    elif Troops.barbarian in deployable: best_troop="Barbarian"
    deploy_position=(0, 50)
    if best_troop=="Giant" or best_troop=="Prince":
        deploy_position=(0, 50)
    if(k==1):
        deploy_position=(0,0)
    if arena_data["OppTower"].health<500 and my_tower.health>5000: 
        if Troops.prince in deployable: best_troop="Prince"
        elif Troops.dragon in deployable: best_troop="Wizard"
        deploy_position=(0, 50)
    # --- Deployment Position ---
    if best_troop is not None:
        deploy_list.list_.append((best_troop, deploy_position))
    else:
        # Fallback: If no deployable troop meets criteria, deploy the first available troop.
        if deployable:
            deploy_list.list_.append((deployable[0], (0, 0)))