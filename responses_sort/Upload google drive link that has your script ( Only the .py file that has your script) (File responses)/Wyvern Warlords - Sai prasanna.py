
import random
from teams.helper_function import Troops, Utils

team_name = "Wyvern Warlords"
troops = [
    Troops.wizard, Troops.minion, Troops.knight, Troops.musketeer,
    Troops.dragon, Troops.skeleton, Troops.archer, Troops.barbarian
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

    speed_giant= 1.34
    speed_wizard=4
    speed_prince=6.67
    x_pos = 0
    y_pos = 0
    global team_signal
    troops_data = Troops.troops_data
    my_tower = arena_data["MyTower"]
    opp_tower = arena_data["OppTower"]
    opp_troops = arena_data["OppTroops"]
    my_troops = arena_data["MyTroops"]
    lowest_y = 50
    for troop in opp_troops:
        if troop.position[1] <= lowest_y:
            lowest_y = troop.position[1]
            lowest_y_x= troop.position[0]
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

    if count_ground > count_air:
        recommended_counter = "air"    # Counter ground with air units.
    elif count_air > count_ground:
        recommended_counter = "ground" # Counter air with ground units.
    else:
        recommended_counter = None     # No clear preference.

    # --- Score Our Troops (only from deployable troops) ---
    deployable = my_tower.deployable_troops
    # Define base scores and categories for our troops.
    troop_data = {
        Troops.wizard:    {"score": 6, "category": "ground",    "name": "Wizard"},
        Troops.minion:    {"score": 3, "category": "air",    "name": "Minion"},
        Troops.knight:    {"score": 3, "category": "ground", "name": "Knight"},
        Troops.musketeer:     {"score": 3, "category": "ground", "name": "Musketeer"},
        Troops.archer:    {"score": 5, "category": "ground",    "name": "Archer"},
        Troops.skeleton:  {"score": 4, "category": "ground", "name": "Skeleton"},
        Troops.dragon:   {"score": 5, "category": "air",    "name": "Dragon"},
        Troops.barbarian: {"score": 4, "category": "ground", "name": "Barbarian"}
    }

    bonus = 4  # Bonus for matching the recommended counter strategy.
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
    if(lowest_y<30):
        if "Knight" or "Skeleton" or "Giant" or "Barbarian" or "Valkyrie" or "Prince" in opp_troops:
            if my_tower.health <= opp_tower.health:
                deploy_list.list_.append(("Minion", ((lowest_y_x/2), (lowest_y/2))))
            else :
                deploy_list.list_.append(("Dragon", ((lowest_y_x/2), (lowest_y/2))))
        if best_troop is not None:
            selected_category = troop_data[best_troop]["category"]
            if selected_category == "air":
                # Deploy air units further forward.
                deploy_position = ((lowest_y_x/2), (lowest_y/2))
            else:
                # Deploy ground units slightly closer for support.
                deploy_position = ((lowest_y_x/2), (lowest_y/2))
            deploy_list.list_.append((best_troop, deploy_position))
        else:
            # Fallback: If no deployable troop meets criteria, deploy the first available troop.
            if deployable:
                deploy_list.list_.append((deployable[0], ((lowest_y_x/2), (lowest_y/2))))

    if "Wizard" in deployable:
        if(lowest_y>50):
            deploy_list.list_.append(("Wizard", (0,40)))
        elif(lowest_y > 30):
            deploy_list.list_.append(("Wizard", (0,lowest_y-12)))
    if(lowest_y>30):
        for troop in my_troops:
            if troop.name == "Skeleton":
                y_pos = troop.position[1]
                x_pos = troop.position[0]
                if(y_pos>50):
                    y_pos=50
                if "Minion" in deployable:
                    best_troop = "Minion"
                    deploy_list.list_.append((best_troop, (random_x(-15,15), y_pos)))
                elif "Knight" in deployable:
                    best_troop = "Knight"
                    deploy_list.list_.append((best_troop, (random_x(-15,15), y_pos)))
                elif "Skeleton" in deployable:
                    best_troop = "Skeleton"
                    deploy_list.list_.append((best_troop, (random_x(-15,15), y_pos)))
                elif "Barbarian" in deployable:
                    best_troop = "Barbarian"
                    deploy_list.list_.append((best_troop, (random_x(-15,15), y_pos)))
                elif "Dragon" in deployable:
                    best_troop = "Dragon"
                    deploy_list.list_.append((best_troop, (random_x(-15,15), y_pos)))
    for troop in opp_troops:
        if troop.name == "Wizard":
            y_pos = troop.position[1]
            x_pos = troop.position[0]
            if(x_pos == -25 ):
                x_pos=-24
            if(y_pos == 0 ):
                y_pos=1
            if y_pos < 50 and (lowest_y > 30 or lowest_y == y_pos):
                if "Skeleton" in deployable:
                    best_troop = "Skeleton"
                    deploy_list.list_.append((best_troop, (x_pos - 1, y_pos - 1)))

                if "Barbarian" in deployable:   # Fixed typo
                    best_troop = "Barbarian"
                    deploy_list.list_.append((best_troop, (x_pos - 1, y_pos - 1)))

                if "Wizard" in deployable:
                    best_troop = "Wizard"       # Added missing assignment
                    deploy_list.list_.append((best_troop, (x_pos - 1, y_pos - 1)))

                if "Minion" in deployable:
                    best_troop = "Minion"
                    deploy_list.list_.append((best_troop, (x_pos - 1, y_pos - 1)))

                if "Musketeer" in deployable:
                    best_troop = "Musketeer"
                    deploy_list.list_.append((best_troop, (x_pos - 1, y_pos - 1)))

    for troop in opp_troops:
        if troop.name == "Prince":
            y_pos = troop.position[1]
            x_pos = troop.position[0]
            if(x_pos == -25 ):
                x_pos=-24
            if(y_pos == 0 ):
                y_pos=1
        if "Skeleton" in deployable:
            best_troop = "Skeleton"
            deploy_list.list_.append((best_troop, (x_pos - 1, y_pos - 1)))
        if "Minion" in deployable:
            best_troop = "Minion"
            deploy_list.list_.append((best_troop, (x_pos - 1, y_pos - 1)))
        if "Dragon" in deployable:
            best_troop = "Dragon"
            deploy_list.list_.append((best_troop, (x_pos - 1, y_pos - 1)))
    # Loop over our full troop list, but only consider those that are deployable.
    for troop in troops:
        if troop not in deployable:
            continue
        base = troop_data[troop]["score"]
        cat = troop_data[troop]["category"]
        score = base + (bonus if recommended_counter and cat == recommended_counter else 0)
        if score > best_score:
            best_score = score
            best_troop = troop

    # --- Deployment Position ---
    if "Knight" or "Skeleton" or "Giant" or "Barbarian" or "Valkyrie" or "Prince" in opp_troops:
        if my_tower.health <= opp_tower.health:
            deploy_list.list_.append(("Minion", (0, 0)))
        else :
            deploy_list.list_.append(("Dragon", (0, 10)))
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