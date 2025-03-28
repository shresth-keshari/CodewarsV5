from teams.helper_function import Troops, Utils
import numpy as np

team_name = "Code Nerds"
troops = [Troops.wizard,Troops.prince,Troops.musketeer,Troops.knight,Troops.dragon,Troops.skeleton,Troops.valkyrie,Troops.minion]
deploy_list = Troops([])
team_signal = "h, Prince, Knight, Wizard"

def deploy(arena_data:dict):
    """
    DON'T TEMPER DEPLOY FUCNTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def random_x(min_val=-25, max_val=25):
    return np.random.randint(min_val, max_val)

def logic(arena_data: dict):
    global team_signal
    troops_data = Troops.troops_data
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
        if troop.name not in current_names:
            team_signal = team_signal + ", " + troop.name if team_signal else troop.name

    opponent_air = {"Minion", "Dragon", "Musketeer", "Balloon"}
    opponent_ground = {"Prince", "Knight", "Barbarian", "Princess", "Giant", "Archer", "Skeleton", "Wizard", "Valkyrie"}
    
    tokens = [token.strip() for token in team_signal.split(",") if token.strip() != "h"]
    count_air = sum(1 for token in tokens if token in opponent_air)
    count_ground = sum(1 for token in tokens if token in opponent_ground)
    
    if count_ground > count_air:
        recommended_counter = "air"
    elif count_air > count_ground:
        recommended_counter = "ground"
    else:
        recommended_counter = "air"
    

    deployable = my_tower.deployable_troops

    troop_data = {
        Troops.wizard:    {"score": 4, "category": "air",    "name": "Wizard"},
        Troops.prince:    {"score": 4, "category": "air",    "name": "Skeleton"},
        Troops.musketeer:    {"score": 4, "category": "ground", "name": "Musketeer"},
        Troops.knight:     {"score": 3, "category": "ground", "name": "Knight"},
        Troops.dragon:    {"score": 3, "category": "air",    "name": "Dragon"},
        Troops.skeleton:  {"score": 2, "category": "ground", "name": "Skeleton"},
        Troops.valkyrie:   {"score": 4, "category": "air",    "name": "Valkyrie"},
        Troops.minion: {"score": 2, "category": "ground", "name": "Minion`"}
    }
    
    bonus = 2
    best_troop = None
    best_score = -1
    
    for troop in troops:
        if troop not in deployable:
            continue
        base = troop_data[troop]["score"]
        cat = troop_data[troop]["category"]
        score = base + (bonus if recommended_counter and cat == recommended_counter else 0)
        if score > best_score:
            best_score = score
            best_troop = troop

    if best_troop is not None:
        selected_category = troop_data[best_troop]["category"]
        if selected_category == "air":
            deploy_position = (random_x(-25, 25), 0)
        else:
            # if best_troop == "Valkyrie":
            #     deploy_position = (0, 25)
            # else:
            deploy_position = (random_x(-10, 10), 0)
        deploy_list.list_.append((best_troop, deploy_position))
        # print(best_troop, best_score)
    else:
        if deployable:
            deploy_list.list_.append((deployable[0], (0, 0)))
