import random
from teams.helper_function import Troops, Utils

team_name = "Obsidian Reapers"
troops = [
    Troops.wizard, Troops.minion, Troops.balloon, Troops.musketeer,
    Troops.dragon, Troops.skeleton, Troops.valkyrie, Troops.barbarian
]
deploy_list = Troops([])
team_signal = ""

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def deploy(arena_data: dict):
    """
    DON'T TEMPER DEPLOY FUNCTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def select_best_troop(strategy, deployable):
    troops_data = Troops.troops_data
    strategy_scores = {
        "anti-air": lambda t: troops_data[t].damage if troops_data[t].target_type["air"] else 0,
        "anti-ground": lambda t: troops_data[t].damage if troops_data[t].target_type["ground"] else 0,
        "balanced": lambda t: troops_data[t].damage
    }
    return max(deployable, key=strategy_scores[strategy], default=None)

def select_support_troop(main_troop, deployable, strategy, troops_data):
    remaining_troops = [t for t in deployable if t != main_troop]
    if remaining_troops:
        if strategy == "anti-air":
            return max(remaining_troops, key=lambda t: troops_data[t].damage if troops_data[t].target_type in ["air", "all"] else 0)
        elif strategy == "anti-ground":
            return max(remaining_troops, key=lambda t: troops_data[t].damage if troops_data[t].target_type in ["ground", "all"] else 0)
        else:
            return max(remaining_troops, key=lambda t: troops_data[t].health / troops_data[t].elixir)
    return None

def logic(arena_data: dict):
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    deployable = my_tower.deployable_troops
    troops_data = Troops.troops_data

    # Analyze opponent's troops
    air_threats = [troop for troop in opp_troops if troop.type == "air"]
    ground_threats = [troop for troop in opp_troops if troop.type == "ground"]
    
    # Determine the best counter
    if len(air_threats) > len(ground_threats):
        strategy = "anti-air"
    elif len(ground_threats) > len(air_threats):
        strategy = "anti-ground"
    else:
        strategy = "balanced"

    # Select best troop based on strategy
    best_troop = select_best_troop(strategy, deployable)

    if best_troop:
        # Determine optimal deployment position
        deploy_position = get_optimal_position(best_troop, opp_troops, my_tower)
        deploy_list.list_.append((best_troop, deploy_position))

        # Select and deploy a support troop if possible
        support_troop = select_support_troop(best_troop, deployable, strategy, troops_data)
        if support_troop:
            support_position = (deploy_position[0] - 5, deploy_position[1] - 5)
            deploy_list.list_.append((support_troop, support_position))

def get_optimal_position(troop, opp_troops, my_tower):
    troops_data = Troops.troops_data
    x = 0
    y = 0
    
    # Calculate base X position
    if opp_troops:
        closest_opp_troop = min(opp_troops, key=lambda t: abs(t.position[0] - my_tower.position[0]))
        if troops_data[troop].target_type["air"]:
            x = min(max(closest_opp_troop.position[0], -25), 25)
        else:
            x = min(max(closest_opp_troop.position[0], -10), 10)

    # Calculate dynamic Y position based on battlefield conditions
    my_troops = []  # Ensure my_troops is defined
    enemy_half_troops = len([t for t in my_troops if t.position[1] > 25])
    safety_factor = min(1, (len(my_troops) - len(opp_troops)) * 0.5)
    
    if not opp_troops or (enemy_half_troops > 3 and safety_factor > 0):
        # Aggressive deployment in enemy territory
        y = random.randint(35, 45)  # Frontline deployment
    elif len(my_troops) > len(opp_troops) + 2:
        # Moderate push with numerical advantage
        y = random.randint(25, 35)
    else:
        # Default defensive positioning
        y = max(0, min(
            (closest_opp_troop.position[1] - troops_data[troop].attack_range) if opp_troops else 0,
            50
        ))

    # Adjust for ground clearance
    ground_threats = [t for t in opp_troops if t.type == "ground"]
    if not ground_threats and troops_data[troop].target_type["ground"]:
        y = min(y + 10, 50)  # Push ground troops forward

    return (x, max(0, min(y, 50)))