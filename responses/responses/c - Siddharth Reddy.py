# from teams.helper_function import Troops, Utils

# team_name = "DELHI"
# troops = [Troops.dragon,Troops.skeleton,Troops.wizard,Troops.minion,Troops.archer,Troops.wizard,Troops.balloon,Troops.barbarian]
# deploy_list = Troops([])
# team_signal = ""

# def deploy(arena_data:dict):
#     """
#     DON'T TEMPER DEPLOY FUCNTION
#     """
#     deploy_list.list_ = []
#     logic(arena_data)
#     return deploy_list.list_, team_signal

# def logic(arena_data:dict):
#     global team_signal
#     deploy_list.deploy_dragon((-16,0))

from teams.helper_function import Troops, Utils
import random
def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)
team_name = "Priyam"
troops = [Troops.wizard,Troops.balloon,Troops.dragon,Troops.minion,Troops.knight,Troops.valkyrie,Troops.barbarian,Troops.musketeer]
deploy_list = Troops([])
team_signal = ""
def deploy(arena_data:dict):
    """
    DON'T TEMPER DEPLOY FUCNTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data:dict):
    global team_signal
    my_tower = arena_data["MyTower"]
    my_troops = arena_data["MyTroops"]
    opp_troops = arena_data["OppTroops"]
    deployable = my_tower.deployable_troops 
    best_troop = None
    support_troop = None
    best_position_x = 0
    best_position_y = 0
    # print (deployable)
    # Earlygame_strategy 
    
    if my_tower.game_timer < 20 :
        if "Wizard" not in deployable and "Balloon" not in deployable :
            for troop in ["valkyrie","knight","dragon"] :
                if troop in deployable:
                    best_troop = troop
                 
                    break
        if "Wizard" not in [troop.name for troop in my_troops] and "Balloon" not in [troop.name for troop in my_troops] :
            for troop in deployable:
                if troop == "Balloon":
                    best_troop = Troops.balloon
                    break

            for troop in deployable:
                if troop == "Wizard":
                    best_troop = Troops.wizard
                    break
        
        for troop in my_troops:
            current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
            if troop.name not in current_names:
                team_signal = team_signal + ", " + troop.name if team_signal else troop.name
               
        for troop in my_troops :
            if troop.name == "Wizard" or troop.name == "Balloon":
                troop_stats = {
                    "Minion": {"damage": 129, "attack_speed": "Fast", "splash": 0},
                    "Knight": {"damage": 221, "attack_speed": "Fast", "splash": 0},
                    "Dragon": {"damage": 176, "attack_speed": "Fast", "splash": 1.875},
                    "Valkyrie": {"damage": 195, "attack_speed": "Fast", "splash": 1.875},
                    "Musketeer": {"damage": 239, "attack_speed": "Medium", "splash": 0},
                    "Barbarian": {"damage": 161, "attack_speed": "Medium", "splash": 0}
                }

                # Define multipliers for the attack speeds.
                attack_speed_multiplier = {
                    "Fast": 1.0,
                    "Medium": 0.6
                }

                def calculate_score(troop_name):
                    if troop_name not in troop_stats:
                        return 0
                    stats = troop_stats[troop_name]
                    multiplier = attack_speed_multiplier.get(stats["attack_speed"], 1.0)
                    # Calculate DPS and add the splash bonus.
                    score = (stats["damage"] * multiplier) 
                    return score

                best_score = -1
                # Calculate  scores for each troop.
                for troop in deployable:
                    score = calculate_score(troop)
                    if score > best_score:
                        best_score = score
                        best_troop = troop
                        deploy_list.list_.append((best_troop,(0,0)))

            break    
        
    # Midgame_strategy
    # Define opponent categories.
    # Create scenarios 
    #assign score to trooops based on scenarios
    #select best troop
    #elif my_tower.game_timer <120 and my_tower.game_timer > 20:
    else:
        for troop in opp_troops:
            current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
            if troop.name not in current_names:
              team_signal = team_signal + ", " + troop.name if team_signal else troop.name
        def calculate_battle_score(troops):
    
            total_troops = len(troops)
            total_health = sum(troop.health for troop in troops)
            total_damage = sum(troop.damage for troop in troops)
            
            score = (10 * total_troops) + (0.1 * total_health) + (0.2 * total_damage)
            return score

        def are_we_winning(arena_data: dict) -> bool:

            mytroops = arena_data.get("MyTroops", [])
            opptroops = arena_data.get("OppTroops", [])
            
            my_score = calculate_battle_score(mytroops)
            opp_score = calculate_battle_score(opptroops)
            
            return my_score > opp_score
        def get_best_support_troop(deployable, team_signal):
    
            troop_stats = {
                "Minion":    {"damage": 129, "attack_speed": "Fast",   "splash": 0,     "category": "air"},
                "Knight":    {"damage": 221, "attack_speed": "Fast",   "splash": 0,     "category": "ground"},
                "Dragon":    {"damage": 176, "attack_speed": "Fast",   "splash": 1.875, "category": "air"},
                "Valkyrie":  {"damage": 195, "attack_speed": "Fast",   "splash": 1.875, "category": "ground"},
                "Musketeer": {"damage": 239, "attack_speed": "Medium", "splash": 0,     "category": "ground"},
                "Barbarian": {"damage": 161, "attack_speed": "Medium", "splash": 0,     "category": "ground"}
            }
            
            attack_speed_multiplier= {
                "Fast": 1.0,
                "Medium": 0.5
            }   
            
            # Opponent categories to determine recommended counter from team signal.
            opponent_air = {"Minion", "Dragon","Balloon"}
            opponent_ground = {"Knight", "Skeleton", "Valkyrie", "Musketeer", "Barbarian","Archer","Wizard","Prince","Wizard"}

            # Process team_signal tokens, filtering out any extras.
            tokens = [token.strip() for token in team_signal.split(",") if token.strip() and token.strip() != "h"]
            count_air = sum(1 for token in tokens if token in opponent_air)
            count_ground = sum(1 for token in tokens if token in opponent_ground)
            
            # If opponents are stronger in one category, we want to counter with the opposite.
            recommended_counter = None
            if count_ground > count_air:
                recommended_counter = "air"    # Counter ground with air.
            elif count_air > count_ground:
                recommended_counter = "ground" # Counter air with ground.
                
            bonus = -300  # Bonus score if troop category matches recommended counter.
            
            best_troop = None
            best_score = -100

            
            for troop in deployable:
                name = troop  # Assuming troop.name is a string matching our keys.
                if name not in troop_stats:  # Skip unknown troops.
                    continue
                stats = troop_stats[name]
                base = stats["damage"] * attack_speed_multiplier.get(stats["attack_speed"], 1.0)
                score = base + stats["splash"]
             
                if recommended_counter and stats["category"] == recommended_counter:
                    score += bonus
                if score > best_score:
                    best_score = score
                    best_troop = troop
                    
            return best_troop
        def get_best_defensive_troop(deployable):
    # Define defensive priorities where a higher value is better.
            defensive_priority = {
                "Minion": 1,
                "Barbarian": 4,
                "Dragon": 3,
                "Valkyrie": 5
            }
            
            best_troop = None
            best_score = -1
            for troop in deployable:
                # Assume troop.name matches one of the keys above.
                score = defensive_priority.get(troop, 0)
                if score > best_score:
                    best_score = score
                    best_troop = troop
            return best_troop
        
        if are_we_winning(arena_data):
            best_troop = get_best_support_troop(deployable, team_signal)
        elif not are_we_winning(arena_data):
            best_troop = get_best_defensive_troop(deployable)
        else:
            best_troop = deployable[0]

        if "Wizard" in deployable :
            best_troop = "Wizard"
        # Endgame_strategy
    
    deploy_list.list_.append((best_troop,(random_x(-25, 25),0)))
