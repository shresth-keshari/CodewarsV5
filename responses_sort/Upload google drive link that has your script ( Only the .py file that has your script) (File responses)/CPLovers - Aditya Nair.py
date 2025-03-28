# from teams.helper_function import Troops, Utils

# team_name = "MUMBAI"
# troops = [Troops.prince,Troops.minion,Troops.archer,Troops.giant,Troops.dragon,Troops.skeleton,Troops.balloon,Troops.barbarian]
# deploy_list = Troops([])
# team_signal = "h"

# def deploy(arena_data:dict):
#     """
#     DON'T TEMPER DEPLOY FUCNTION
#     """
#     deploy_list.list_ = []
#     logic(arena_data)
#     return deploy_list.list_, team_signal

# def logic(arena_data:dict):
#     global team_signal
#     deploy_list.deploy_prince((-16,0))
#     """
#     WRITE YOUR CODE HERE 
#     """
import random
from teams.helper_function import Troops, Utils

team_name = "a"
troops = [
    Troops.wizard, Troops.minion, Troops.knight, Troops.giant,
    Troops.dragon, Troops.skeleton, Troops.valkyrie, Troops.prince
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
    
    
    # --- Update Team Signal ---
    # Add new opponent troop names (avoid duplicates).
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
        if troop.name not in current_names:
            team_signal = team_signal + ", " + troop.name if team_signal else troop.name
    # print(f"Team Signal: {team_signal}")
    
    # --- Analyze Opponent's Deck Composition ---
    # Define opponent categories.
    opponent_air = {"Minion", "Dragon", "Musketeer", "Archer", "Balloon"}
    opponent_ground = {"Prince", "Knight", "Barbarian",""}
    opponent_tankers = {"Giant", "Prince", "Knight" , "Valkyrie" ,"Balloon"}
    opponent_supporters = {"Minions", "Wizard", "Archer", "Dragon", "Skeleton"}
    #opponent_no_splash = {"Prince", "Knight", "Giant", "Musketeer"}
    #opponent_splash = {"Valkyrie", "Wizard", "Dragon"}
    
    
    tokens = [token.strip() for token in team_signal.split(",") if token.strip() != "h"]
    count_air = sum(1 for token in tokens if token in opponent_air)
    count_ground = sum(1 for token in tokens if token in opponent_ground)
    count_tankers = sum(1 for token in tokens if token in opponent_tankers)
    count_supporters = sum(1 for token in tokens if token in opponent_supporters)
    #count_no_splash = sum(1 for token in tokens if token in opponent_no_splash)

    #if count_no_splash > 2:
    #    recommended_counter_splash = 1
    #else:
    #    recommended_counter_splash = 0
    if count_tankers > 1:
        recommended_counter_role = "s"
    else:
        recommended_counter_role = "t"
    if count_ground > count_air:
        recommended_counter_cat = "air"    # Counter ground with air units.
    elif count_air > count_ground:
        recommended_counter_cat = "ground" # Counter air with ground units.
    else:
        recommended_counter_cat = None     # No clear preference.
    
    # --- Score Our Troops (only from deployable troops) ---
    deployable = my_tower.deployable_troops
    # Define base scores and categories for our troops.
    troop_data = {
        Troops.wizard:    {"score": 5, "category": "air",    "name": "Wizard" , "role": "s", "splash":1, "elixir":5 },
        Troops.minion:    {"score": 4, "category": "air",    "name": "Minion", "role": "s", "splash":0, "elixir": 3},
        Troops.prince:    {"score": 3, "category": "ground", "name": "Prince", "role": "t", "splash":0, "elixir": 5},
        Troops.giant:     {"score": 2, "category": "ground", "name": "Giant", "role": "t", "splash":0, "elixir": 5},
        Troops.dragon:    {"score": 2, "category": "air",    "name": "Dragon", "role": "s", "splash":1, "elixir": 4},
        Troops.skeleton:  {"score": 3, "category": "ground", "name": "Skeleton", "role": "s", "splash":0, "elixir":3},
        Troops.valkyrie:  {"score": 4, "category": "ground",    "name": "Valkyrie", "role": "t", "splash":1, "elixir": 4},
        Troops.knight:    {"score": 3, "category": "ground", "name": "Knight", "role": "s", "splash":0, "elixir":3 }
    }
    
    bonus = 4  # Bonus for matching the recommended counter strategy.
    best_troop = None
    best_score = -1
    
    # Loop over our full troop list, but only consider those that are deployable.
    
    for troop in troops:
        if troop not in deployable:
            continue
        base = troop_data[troop]["score"]
        cat = troop_data[troop]["category"]
        role = troop_data[troop]["role"]
        #splash = troop_data[troop]["splash"]
        #elixir = troop_data[troop]["elixir"]
        #if my_elixir <=4:
         #   if elixir == 3:
          #      troop = best_troop
        #else:
        score = base + (bonus if recommended_counter_cat and cat == recommended_counter_cat or recommended_counter_role == role else 0)
        if score > best_score:
            best_score = score
            best_troop = troop

    # --- Deployment Position ---
    if best_troop is not None:
        
        selected_category = troop_data[best_troop]["category"]
        if selected_category == "air":
                # Deploy air units further forward.
            deploy_position = (random_x(-25, 25), 0)
        else:
                # Deploy ground units slightly closer for support.
            deploy_position = (random_x(-10, 10), 0)
        deploy_list.list_.append((best_troop, deploy_position))
    else:
        # Fallback: If no deployable troop meets criteria, deploy the first available troop.
        if deployable:
            deploy_list.list_.append((deployable[0], (0, 0)))
