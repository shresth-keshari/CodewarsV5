import random
from teams.helper_function import Troops, Utils

team_name = "Vk"
troops = [
    Troops.wizard, Troops.balloon, Troops.archer, Troops.knight,
    Troops.dragon, Troops.skeleton, Troops.prince, Troops.barbarian
]

deploy_list = Troops([])  # Ensure correct deployment format.
team_signal = "h, Prince, Knight, Barbarian, Princess"

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def deploy(arena_data: dict):
    """
    DON'T TEMPER DEPLOY FUNCTION
    """
    deploy_list.list_ = []  # Reset deployment list.
    logic(arena_data)
    return deploy_list.list_, team_signal  # Return correctly formatted output.

def logic(arena_data: dict):
    global team_signal
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    
    # --- Update Team Signal ---
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
        if troop.name not in current_names:
            team_signal = team_signal + ", " + troop.name if team_signal else troop.name
    team_signal = team_signal[:200]  # Ensure team_signal does not exceed 200 characters

    # --- Analyze Opponent's Deck Composition ---
    opponent_air = {"Minion", "Dragon", "Musketeer"}
    opponent_ground = {"Prince", "Knight", "Barbarian", "Princess"}
    
    tokens = [token.strip() for token in team_signal.split(",") if token.strip() != "h"]
    count_air = sum(1 for token in tokens if token in opponent_air)
    count_ground = sum(1 for token in tokens if token in opponent_ground)
    
    if count_ground > count_air:
        recommended_counter = "air"
    elif count_air > count_ground:
        recommended_counter = "ground"
    else:
        recommended_counter = None

    # --- Check Game Time for Early Deployment ---
    # Assume arena_data["GameTime"] contains the elapsed seconds.
    game_time = arena_data.get("GameTime", 999)
    
    # Define troop data (including their "score" as a proxy for elixir cost)
    troop_data = {
        Troops.wizard:    {"score": 3, "category": "air",    "attack_range": 20, "name": "Wizard"},
        Troops.balloon:   {"score": 5, "category": "air",    "attack_range": 0,  "name": "Balloon", "splash": True},
        Troops.archer:    {"score": 4, "category": "ground", "attack_range": 25, "name": "Archer"},
        Troops.knight:    {"score": 3, "category": "ground", "name": "Knight", "splash": False, "attack_range": 0},
        Troops.dragon:    {"score": 5, "category": "air",    "attack_range": 30, "name": "Dragon"},
        Troops.skeleton:  {"score": 2, "category": "ground", "attack_range": 10, "name": "Skeleton"},
        Troops.prince:    {"score": 5, "category": "ground", "attack_range": 0,  "name": "Prince", "splash": False},
        Troops.barbarian: {"score": 3, "category": "ground", "attack_range": 12, "name": "Barbarian"}
    }
    
    deployable = my_tower.deployable_troops

    # --- Early Game Deployment: First 10 seconds, deploy as many low-cost troops as possible ---
    if game_time <= 10:
        # For early game, consider low-cost if score is less than 4.
        for troop in troops:
            if troop in deployable and troop_data[troop]["score"] < 4:
                deploy_list.list_.append((troop, (0, 50)))
        return  # End early game deployment.

    # --- Prioritize Defense: Select Enemy on Our Side ---
    enemy_on_our_side = sorted(
        [troop for troop in opp_troops if troop.position[1] <= 25],
        key=lambda troop: troop.position[1]
    )
    if enemy_on_our_side:
        target = enemy_on_our_side[0]
    else:
        target = min(opp_troops, key=lambda t: abs(t.position[1] - my_tower.position[1])) if opp_troops else None

    # Determine local target category if target is close (within 25 units).
    local_target_category = None
    if target:
        distance = abs(target.position[1] - my_tower.position[1])
        if distance <= 25:
            if target.name in opponent_air:
                local_target_category = "air"
            elif target.name in opponent_ground:
                local_target_category = "ground"
    
    bonus = 3

    # --- First, deploy the prioritized group ---
    prioritized = [Troops.prince, Troops.wizard, Troops.archer, Troops.knight, Troops.balloon, Troops.dragon]
    prioritized_deployed = []
    for troop in prioritized:
        if troop not in deployable:
            continue
        # Skip Balloon if there are 2+ enemy air attackers.
        if troop == Troops.balloon and count_air >= 2:
            continue
        # If a local target exists, deploy only troops matching that category.
        if local_target_category is not None and troop_data[troop]["category"] != local_target_category:
            continue
        attack_range = troop_data[troop]["attack_range"]
        if target:
            deploy_y = max(0, target.position[1] - attack_range)
            deploy_x = max(-attack_range, min(attack_range, target.position[0] - (target.position[0] // 2)))
        else:
            deploy_y, deploy_x = 50, 0  # Default position.
        deploy_list.list_.append((troop, (deploy_x, deploy_y)))
        prioritized_deployed.append(troop)

    # --- If none of the prioritized group were deployed, deploy the remaining troops ---
    if not prioritized_deployed:
        for troop in troops:
            # Skip troops that are already handled (if any)
            if troop in prioritized:
                continue
            if troop not in deployable:
                continue
            attack_range = troop_data[troop]["attack_range"]
            if target:
                deploy_y = max(0, target.position[1] - attack_range)
                deploy_x = max(-attack_range, min(attack_range, target.position[0] - (target.position[0] // 2)))
            else:
                deploy_y, deploy_x = 50, 0  # Default position.
            deploy_list.list_.append((troop, (deploy_x, deploy_y)))