# LMAO! TS BASED ON CHEAP WIZARD CYCLE
import random
from teams.helper_function import Troops, Utils

team_name = "Spash Royale"
troops = [
    Troops.wizard, Troops.minion, Troops.archer, Troops.musketeer,
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

def logic(arena_data: dict):
    global team_signal
    troops_data = Troops.troops_data
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    
    troop_data = {
        Troops.wizard:    {"score": 3, "category": "air",    "name": "Wizard", "elixir": 5},
        Troops.minion:    {"score": 2, "category": "air",    "name": "Minion", "elixir": 3},
        Troops.archer:    {"score": 4, "category": "ground", "name": "Archer", "elixir": 3},
        Troops.musketeer:     {"score": 3, "category": "ground", "name": "Musketeer", "elixir": 4},
        Troops.dragon:    {"score": 5, "category": "air",    "name": "Dragon", "elixir": 4},
        Troops.skeleton:  {"score": 2, "category": "ground", "name": "Skeleton", "elixir": 3},
        Troops.valkyrie:   {"score": 4, "category": "air",    "name": "Valkyrie", "elixir": 4},
        Troops.barbarian: {"score": 3, "category": "ground", "name": "Barbarian", "elixir": 3}
    }

    if "Wizard" in my_tower.deployable_troops:
        deploy_list.deploy_wizard(((random.random() - 0.5) * 40, 20))
    else:
        # Loop over our full troop list, but only consider those that are deployable.
        min_elixir = 10
        for troop in troops:
            if troop not in my_tower.deployable_troops:
                continue
            if (troop_data[troop]["elixir"] < min_elixir):
                min_elixir = troop_data[troop]["elixir"]
                best_troop = troop

        # --- Deployment Position ---
        if best_troop is not None:
            selected_category = troop_data[best_troop]["category"]
            if selected_category == "air":
                # Deploy air units further forward.
                deploy_position = (random_x(-20, 20), 0)
            else:
                # Deploy ground units slightly closer for support.
                deploy_position = (random_x(-10, 10), 0)
            deploy_list.list_.append((best_troop, deploy_position))
