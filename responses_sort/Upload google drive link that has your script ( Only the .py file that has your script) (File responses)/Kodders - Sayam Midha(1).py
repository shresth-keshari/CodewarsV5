from teams.helper_function import Troops, Utils
import random

team_name = "Kodders"
troops = [
    Troops.wizard, Troops.minion, Troops.archer, Troops.prince,
    Troops.dragon, Troops.skeleton, Troops.valkyrie, Troops.barbarian
]
deploy_list = Troops([])
team_signal = ""


def deploy(arena_data: dict):
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal


def defense_logic(arena_data: dict, TROOP_DATA_2, categories):
    global team_signal
    my_elixir = arena_data["MyTower"].total_elixir
    opp_troops = arena_data["OppTroops"]
    my_troops = arena_data["MyTower"].deployable_troops
    counters = best_counter(opp_troops, my_troops, my_elixir, TROOP_DATA_2, categories)
    # enemy, counter, score =  counters
    for enemy, counter, score in counters:
        deploy_list.list_.append((counter, (0,0)))

def attack_logic(arena_data: dict, categories, ATTACK_COMBOS):
    global team_signal
    my_troops = arena_data["MyTower"].deployable_troops
    my_elixir = arena_data["MyTower"].total_elixir
    enemy_troops = arena_data["OppTroops"]
    path = get_clear_path(enemy_troops)
    if path == "both":
        deploy_x = random.randint(-5, 5)
    elif path == "lane1":
        deploy_x = random.randint(-25, -10)
    elif path == "lane2":
        deploy_x = random.randint(10, 25)
    else:
        deploy_x = random.randint(-25, 25)
    
    my_troops_categories = {
        "damage_dealer": 0,
        "ranged": 0,
        "burst": 0,
        "splash": 0,
        "melee": 0,
        "swarm": 0,
        "tank": 0,
        "air": 0,
        "ground": 0,
        "attackAir": 0
    }
    troop_speed = {
        "Minion": 1,
        "Prince": 1,
        "Wizard": 0,
        "Barbarian": 0,
        "Archer": 0,
        "Skeleton": 1,
        "Dragon": 1,
        "Valkyrie": 0
    }
    for troop in my_troops:
        for category, troop_list in categories.items():
            if troop in troop_list:
                my_troops_categories[category] += 1

    chosen = choose_combo(my_troops, my_troops_categories, my_elixir, troop_speed, enemy_troops, categories, ATTACK_COMBOS)
    troop1_position, troop2_position = deploy_position_attack(chosen[0], chosen[1], troop_speed)
    deploy_list.list_.append((chosen[0], (deploy_x, troop1_position[1])))
    deploy_list.list_.append((chosen[1], (deploy_x, troop2_position[1])))

def logic(arena_data: dict):
    global team_signal
    
    # Define all constants/variables locally that were previously global
    TROOP_DATA_2 = {
        "Archer": {"health": 668/2, "DPS": 393.33/2, "attack_range": 5, "type": "Ground", "target_type": ["Air", "Ground", "Building"], "velocity": 3, "num": 2, "elixir": 3},
        "Minion": {"health": 756/3, "DPS": 645/3, "attack_range": 2, "type": "Ground", "target_type": ["Air", "Ground", "Building"], "velocity": 5, "num": 3, "elixir": 3},
        "Knight": {"health": 1938, "DPS": 368.33, "attack_range": 0, "type": "Ground", "target_type": ["Ground", "Building"], "velocity": 3, "num": 1, "elixir": 3},
        "Skeleton": {"health": 890/10, "DPS": 1483.33/10, "attack_range": 0, "type": "Ground", "target_type": ["Ground", "Building"], "velocity": 5, "num": 10, "elixir": 3},
        "Dragon": {"health": 1267, "DPS": 293.33, "attack_range": 3.5, "type": "Air", "target_type": ["Air", "Ground", "Building"], "velocity": 5, "num": 1, "elixir": 4},
        "Valkyrie": {"health": 2097, "DPS": 325, "attack_range": 0, "type": "Ground", "target_type": ["Ground", "Building"], "velocity": 3, "num": 1, "elixir": 4},
        "Musketeer": {"health": 792, "DPS": 199.167, "attack_range": 6, "type": "Ground", "target_type": ["Air", "Ground", "Building"], "velocity": 3, "num": 1, "elixir": 4},
        "Giant": {"health": 5423, "DPS": 187.22, "attack_range": 0, "type": "Ground", "target_type": ["Building"], "velocity": 1, "num": 1, "elixir": 5},
        "Prince": {"health": 1920, "DPS": 653.33, "attack_range": 0, "type": "Ground", "target_type": ["Ground", "Building"], "velocity": 5, "num": 1, "elixir": 5},
        "Barbarian": {"health": 2208/3, "DPS": 402.5/3, "attack_range": 0, "type": "Ground", "target_type": ["Ground", "Building"], "velocity": 3, "num": 3, "elixir": 3},
        "Balloon": {"health": 2226, "DPS": 353.33, "attack_range": 0, "type": "Air", "target_type": ["Building"], "velocity": 3, "num": 1, "elixir": 5},
        "Wizard": {"health": 1100, "DPS": 683.33, "attack_range": 5.5, "type": "Ground", "target_type": ["Air", "Ground", "Building"], "velocity": 3, "num": 1, "elixir": 5},
        "MyTower": {"health": 7032, "DPS": 263.33 , "attack_range": 12.5, "type": "Building", "target_type": ["Air", "Ground"], "velocity": 0, "num": 1},
        "OppTower": {"health": 7032, "DPS": 263.33 , "attack_range": 12.5, "type": "Building", "target_type": ["Air", "Ground"], "velocity": 0, "num": 1}
    }

    damage_dealers = ["Wizard", "Skeleton", "Minion", "Balloon", "Barbarian", "Archer"]
    ranged = ["Wizard", "Archer", "Dragon", "Musketeer"]
    burst = ["Wizard", "Skeleton", "Barbarian", "Prince"]
    splash = ["Wizard", "Dragon", "Valkyrie"]
    melee = ["Skeleton", "Barbarian", "Knight", "Prince", "Valkyrie"]
    swarm = ["Skeleton", "Minion", "Barbarian", "Archer"]
    tanks = ["Giant"]
    air = ["Minion", "Balloon", "Dragon"]
    ground = ["Wizard", "Skeleton", "Barbarian", "Archer", "Musketeer", "Knight", "Prince", "Valkyrie", "Giant"]
    attackAir = ["Minion", "Dragon", "Musketeer", "Wizard", "Archer"]

    categories = {
        "damage_dealer": damage_dealers,
        "ranged": ranged,
        "burst": burst,
        "splash": splash,
        "melee": melee,
        "swarm": swarm,
        "tank": tanks,
        "air": air,
        "ground": ground,
        "attackAir": attackAir
    }

    ATTACK_COMBOS = {
        "air_based": ["air","attackAir"],
        "melee_ranged": ["melee","ranged"],
        "splash_burst": ["splash","burst"],
        "swarm_damage": ["swarm","damage_dealer"],
        "spash_damage": ["splash","damage_dealer"],
        "air_ranged": ["air","ranged"],
        "air_splash": ["air","splash"],
    }
    
    ############## Game Setup ################

    ####### Don't modify this section ########
    my_tower_health = arena_data["MyTower"].health
    opp_tower_health = arena_data["OppTower"].health
    my_elixir = arena_data["MyTower"].total_elixir
    opp_troops = arena_data["OppTroops"]
    my_troops = arena_data["MyTower"].deployable_troops

    if my_tower_health < 500 or len(opp_troops) > 3:
        defense_logic(arena_data, TROOP_DATA_2, categories)
    else:
        attack_logic(arena_data, categories, ATTACK_COMBOS)
        
def best_counter(opp_troops, my_troops, my_elixir, TROOP_DATA_2, categories):
    counters = []
    
    for enemy_troop in opp_troops:
        enemy_name = enemy_troop.name 
        enemy_tags = [tag for tag, troop_list in categories.items() if enemy_name in troop_list]

        best_match = None
        best_score = float('-inf')

        for my_troop_name in my_troops:  # my_troops is a list of strings
            my_tags = [tag for tag, troop_list in categories.items() if my_troop_name in troop_list]

            # Countering logic
            score = 0
            if "ground" in enemy_tags and "air" in my_tags:
                score += 3  
            if "melee" in enemy_tags and "ranged" in my_tags:
                score += 2  
            if "tank" in enemy_tags and "burst" in my_tags:
                score += 2  
            if "swarm" in enemy_tags and "splash" in my_tags:
                score += 2  
            if "air" in enemy_tags and "ranged" in my_tags:
                score += 2  
            if "damage_dealer" in enemy_tags and "tank" in my_tags:
                score += 2
            if "attackAir" not in enemy_tags and "attackAir" in my_tags:
                score += 3
            # Simulate combat
            result, remaining_health = combat_result(
                my_troop_name, enemy_name,
                TROOP_DATA_2[my_troop_name]["health"], TROOP_DATA_2[enemy_name]["health"],
                TROOP_DATA_2
            )

            if result == 1:
                score += 3  
            elif result == 0:
                score += 1  
            else:
                score -= 2  

            if score > best_score:
                best_score = score
                best_match = my_troop_name  

        if best_match:
            counters.append((enemy_name, best_match, best_score))

    return sorted(counters, key=lambda x: -x[2])  

def combat_result(my_troop_name, opp_troop_name, my_troop_health, opp_troop_health, TROOP_DATA_2, my_troop_num=1, opp_troop_num=1):
    my_data = TROOP_DATA_2[my_troop_name]
    opp_data = TROOP_DATA_2[opp_troop_name]
    my_troop_health = my_troop_health*TROOP_DATA_2[my_troop_name]["num"]
    opp_troop_health = opp_troop_health*TROOP_DATA_2[opp_troop_name]["num"]
    approach_distance = my_data["attack_range"] - opp_data["attack_range"]
    if approach_distance > 0:
        my_approach_damage = (my_data["DPS"]*my_troop_num) * approach_distance / (my_data["velocity"]+opp_data["velocity"])
        opp_approach_damage = 0
    else:
        opp_approach_damage = (opp_data["DPS"]*my_troop_num) * approach_distance / (my_data["velocity"]+opp_data["velocity"])
        my_approach_damage = 0

    if my_data["type"] not in opp_data["target_type"]:
        return 1, my_troop_health
    if opp_data["type"] not in my_data["target_type"]:
        return -1, opp_troop_health
    my_kill_time = ((opp_troop_health - my_approach_damage) / my_data["DPS"]) - 0.6
    opp_kill_time = ((my_troop_health -  opp_approach_damage) / opp_data["DPS"]) - 0.6
    max_time = max(my_kill_time, opp_kill_time)
    time_diff_percent = abs(my_kill_time - opp_kill_time) / max_time * 100 if max_time > 0 else 0
    # Determine winner
    if time_diff_percent < 20:
        # Too close to call
        result = 0
        # Return health of whoever would technically win
        remaining_health = my_troop_health - opp_kill_time * opp_data["DPS"]*opp_troop_num if my_kill_time < opp_kill_time else opp_troop_health - my_kill_time * my_data["DPS"]*my_troop_num
    elif my_kill_time < opp_kill_time:
        # My troop wins
        result = 1
        remaining_health = my_troop_health - opp_approach_damage - max(0, (my_kill_time * opp_data["DPS"]*opp_troop_num))
    else:
        # Opponent's troop wins
        result = -1
        remaining_health = opp_troop_health - my_approach_damage - max(0, opp_kill_time * my_data["DPS"]*my_troop_num)
    
    return result, remaining_health

def choose_combo(my_troops, my_troops_categories, my_elixir, troop_speed, enemy_troops, categories, ATTACK_COMBOS):
    troop_weights = {
        "Minion": 8,
        "Prince": 10,
        "Wizard": 9,
        "Barbarian": 8,
        "Archer": 7,
        "Skeleton": 8,
        "Dragon": 7,
        "Valkyrie": 8
    }
    troop_elixir = {
        "Minion": 3,
        "Prince": 5,
        "Wizard": 5,
        "Barbarian": 3,
        "Archer": 3,
        "Skeleton": 3,
        "Dragon": 4,
        "Valkyrie": 4
    }
    
    # Add the rest of the function code here
    for enemy in enemy_troops:
        if enemy.name not in categories['attackAir'] and "Minion" in my_troops and "Dragon" in my_troops:
            return ("Minion", "Dragon")
            
    combo_troops = []
    for combo in ATTACK_COMBOS:
        category1, category2 = ATTACK_COMBOS[combo]
        troops1 = [troop for troop in my_troops if troop in categories[category1]]
        troops2 = [troop for troop in my_troops if troop in categories[category2]]
        if troops1 and troops2:
            combo_score = sum(troop_weights[t] for t in set(troops1 + troops2))
            same_speed = all(troop_speed[t1] == troop_speed[t2] for t1 in troops1 for t2 in troops2)
            if same_speed:
                combo_score += 3
            combo_troops.append((combo, combo_score))
    
    if combo_troops:
        best_combo = max(combo_troops, key=lambda x: x[1])
        category1, category2 = ATTACK_COMBOS[best_combo[0]]
        
        # Get the highest weighted troops from each category of the best combo
        troop1 = max((t for t in my_troops if t in categories[category1]), key=lambda x: troop_weights[x])
        troop2 = max((t for t in my_troops if t in categories[category2]), key=lambda x: troop_weights[x])
        
        # Check if troops are different and we have enough elixir
        if troop1 != troop2 and troop_elixir[troop1] + troop_elixir[troop2] <= my_elixir:
            return (troop1, troop2)
    
    return ("Minion", "Archer") # Default

def get_clear_path(opp_troops):
    lane1_weak = False
    lane2_weak = False
    
    for enemy in opp_troops:
        lane_1x = (-25, -10)
        lane_2x = (10, 25)
        
        if lane_1x[0] <= enemy.position[0] <= lane_1x[1]:
            if enemy.health < 300:
                lane1_weak = True
                
        if lane_2x[0] <= enemy.position[0] <= lane_2x[1]:
            if enemy.health < 300:
                lane2_weak = True
    
    if lane1_weak and lane2_weak:
        return "both"
    elif lane1_weak:
        return "lane1"
    elif lane2_weak:
        return "lane2"
    return None
    

def deploy_position_attack(troop1, troop2, troop_speed):
    if isinstance(troop1, str) and troop1 == "default":
        return [(-5, 30), (5, 30)]
    if not isinstance(troop1, str) or not isinstance(troop2, str):
        return [(-5, 30), (5, 30)]
    if troop1 not in troop_speed or troop2 not in troop_speed:
        return [(-5, 30), (5, 30)]
    if troop_speed[troop1] == troop_speed[troop2]:
        return [(-5, 30), (5, 30)]
    # Deploy faster troop at (0, 0) and slower troop at (0, 5)
    elif troop_speed[troop1] > troop_speed[troop2]:
        return [(-5, 30), (5, 50)]
    else:
        return [(-5, 50), (5, 30)]
    