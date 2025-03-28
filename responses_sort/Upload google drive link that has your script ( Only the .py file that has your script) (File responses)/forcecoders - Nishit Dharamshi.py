import random
from teams.helper_function import Troops, Utils

team_name = "FORCECODERS"
troops = [
    Troops.wizard, Troops.minion, Troops.archer, Troops.barbarian,
    Troops.dragon, Troops.skeleton, Troops.valkyrie, Troops.prince
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
    my_troops = arena_data["MyTroops"]
    
    # --- Update Team Signal ---
    # Add new opponent troop names (avoid duplicates).
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
        if troop.name not in current_names:
            team_signal = team_signal + ", " + troop.name if team_signal else troop.name
    # print(f"Team Signal: {team_signal}")
    
    # --- Analyze Opponent's Deck Composition ---
    # Define opponent categories.
    horde = {"Minion", "Skeleton", "Barbarian"}
    counter_isFlying = {"Prince", "Knight", "Barbarian", "Valkyrie", "Giant", "Skeleton", "Balloon"}
    horde_counter = {"Wizard", "Dragon", "Archer"}
    counter_isValkyrie = {"Wizard", "Skeleton", "Archer", "Barbarian"}
    counter_isSkeleton = {"Prince", "Giant", "Knight", "Musketer"}
    
    # --- Score Our Troops (only from deployable troops) ---
    deployable = my_tower.deployable_troops
    # Define base scores and categories for our troops.
    troop_data = {
        Troops.wizard:    {"score": 9, "category": "ground",    "name": "Wizard", "attack_range": "long", "target": "air"},
        Troops.minion:    {"score": 8, "category": "flying",    "name": "Minion", "attack_range": "short", "target": "air"},
        Troops.archer:    {"score": 5, "category": "ground", "name": "Archer", "attack_range": "long", "target": "air"},
        Troops.barbarian:     {"score": 3, "category": "ground", "name": "Barbarian", "attack_range": "short", "target": "ground"}, 
        Troops.dragon:    {"score": 7, "category": "flying",    "name": "Dragon", "attack_range": "long", "target": "air"},
        Troops.skeleton:  {"score": 2, "category": "ground", "name": "Skeleton", "attack_range": "short", "target": "ground"},
        Troops.valkyrie:   {"score": 6, "category": "ground",    "name": "Valkyrie", "attack_range": "short", "target": "ground"},
        Troops.prince: {"score": 4, "category": "ground", "name": "Prince", "attack_range": "short", "target": "ground"}
    }
    flying_troops = [t for t in deployable if troop_data[t]["category"] == "flying"]
    
    #deploying wizard whenever possible
    for troop in deployable:
        if troop == Troops.wizard:
            for opptroop in opp_troops:
                deploy_list.list_.append((Troops.wizard, (opptroop.position[0], 10)))

    #counter for specific troop types
    for troop in opp_troops:
        if troop.name in counter_isFlying:
            nexttroop = next((y for y in flying_troops if y in deployable), None)
            deploy_list.list_.append((nexttroop,(troop.position[0], 0)))
        if troop.name in horde:
            nexttroop = next((h for h in horde_counter if h in deployable), None)
            deploy_list.list_.append((nexttroop,(troop.position[0],0)))
        if troop.name in counter_isSkeleton:
            if troop.position[1] <= 50:
                nexttroop = Troops.skeleton if Troops.skeleton in deployable else None
                nexttroop = Troops.barbarian if Troops.barbarian in deployable else None
                deploy_list.list_.insert(0, (nexttroop, troop.position))
        if troop.name in counter_isValkyrie:
            if troop.position[1] <= 50:
                if Troops.valkyrie in deployable:
                    deploy_list.list_.insert(0, (Troops.valkyrie, troop.position))
                if troop == Troops.wizard and my_tower.total_elixir >= 5:
                    deploy_list.list_.append((Troops.prince, troop.position))
        if troop == Troops.valkyrie and troop.position[1] <= 50 and Troops.prince in deployable:
            deploy_list.list_.append((Troops.prince, troop.position))
        if troop.type == "air" and troop.position[1] <= 50:
            for u in deployable:
                if troop_data[u]["target"] == "air":
                    deploy_list.list_.append((u, (troop.position[0], 5)))
            


    #preventing elixir leak
    if my_tower.total_elixir >= 9:
        for troop in troop_data:
            if troop_data[troop]["attack_range"] == "long" and troop in deployable:
                for opptroop in opp_troops:
                    if opptroop.position[1] <= 50:
                        deploy_list.list_.append((troop, (opptroop.position[0], 0)))
                        break
                    else:
                        last_x = my_troops[-1].position[0] if my_troops else random_x(-10, 10)
                        deploy_list.list_.append((troop, (last_x, 0)))
                        break            
            else:
                last_x = my_troops[-1].position[0] if my_troops else random_x(-10, 10)
                deploy_list.list_.append((deployable[0], (last_x, 0)))    