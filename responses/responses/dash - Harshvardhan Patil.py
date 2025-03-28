import random
from teams.helper_function import Troops, Utils

team_name = "DASH"
troops = ["Archer", "Giant", "Knight", "Minion", "Valkyrie", "Wizard", "Dragon", "Skeleton"]
deploy_list = Troops([])
team_signal = ""

def deploy(arena_data: dict):
    """
    DON'T TEMPER DEPLOY FUNCTION
    """
    deploy_list.list_.clear()
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    global team_signal

    # Define troop rankings inside the logic function
    troop_rankings = {
        "Archer": ["Knight", "Skeleton", "Dragon", "Valkyrie", "Wizard", "Archer", "Giant", "Minion"],
        "Minion": ["Archer", "Dragon", "Wizard", "Minion", "Knight", "Skeleton", "Valkyrie", "Giant"],
        "Knight": ["Skeleton", "Dragon", "Minion", "Wizard", "Knight", "Valkyrie", "Giant", "Archer"],
        "Skeleton": ["Dragon", "Valkyrie", "Minion", "Wizard", "Skeleton", "Giant", "Archer", "Knight"],
        "Dragon": ["Wizard", "Dragon", "Archer", "Minion", "Knight", "Skeleton", "Valkyrie", "Giant"],
        "Valkyrie": ["Dragon", "Minion", "Knight", "Valkyrie", "Wizard", "Giant", "Archer", "Skeleton"],
        "Wizard": ["Wizard", "Giant", "Valkyrie", "Giant", "Dragon", "Knight", "Archer", "Skeleton"],
        "Giant": ["Skeleton", "Wizard", "Minion", "Archer", "Valkyrie", "Dragon", "Knight", "Giant"],
        "Prince": ["Skeleton", "Dragon", "Minion", "Wizard", "Giant", "Knight", "Archer", "Valkyrie"],
        "Barbarian": ["Archer", "Knight", "Skeleton", "Valkyrie", "Dragon", "Minion", "Wizard", "Giant"],
        "Balloon": ["Minion", "Wizard", "Archer", "Dragon", "Knight", "Skeleton", "Valkyrie", "Giant"],
        "Musketeer": ["Archer", "Knight", "Skeleton", "Valkyrie", "Dragon", "Minion", "Wizard", "Giant"]
    }

    my_tower = arena_data["MyTower"]
    opp_tower = arena_data["OppTower"]
    my_troops = arena_data["MyTroops"]
    opp_troops = arena_data["OppTroops"]
    available_elixir = my_tower.total_elixir
    deployable_troops = my_tower.deployable_troops

    # Define custom troop weights
    troop_weights = {
        "Archer": 1, "Giant": 3, "Knight": 1, "Minion": 2, "Valkyrie": 2,
        "Wizard": 4, "Balloon": 3, "Skeleton": 1, "Dragon": 2, "Musketeer": 1,
        "Prince": 3, "Barbarian": 1
    }

    # --- Update Team Signal --- (Track enemy troop names)
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
        if troop.name not in current_names:
            team_signal = team_signal + ", " + troop.name if team_signal else troop.name

    # Compute center of mass (COM) for opponent and my troops
    def compute_com(troops):
        if not troops:
            return (0, 0)
        total_weight = sum(troop_weights[t.name] for t in troops)  # Access troop name
        x_com = sum(t.position[0] * troop_weights[t.name] for t in troops) / total_weight  # Access troop name
        y_com = sum(t.position[1] * troop_weights[t.name] for t in troops) / total_weight  # Access troop name
        return (x_com, y_com)

    opp_com = compute_com(opp_troops)
    my_com = compute_com(my_troops)

    # Determine Best Weighted Counter (BWC) using your provided ranking
    def get_bwc():
        scores = {troop: 0 for troop in troops}
        for opp_troop in opp_troops:
            if opp_troop.name in troop_rankings:
                ranking = troop_rankings[opp_troop.name]
                for i, my_troop in enumerate(ranking):
                    if my_troop in troops:
                        scores[my_troop] += 8 - i  # Higher rank gets higher points
        sorted_troops = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for troop, _ in sorted_troops:
            if troop in deployable_troops:
                return troop
        return None

    bwc = get_bwc()

    # Determine average troop type
    def get_avg_troop_type(my_troops):
        type_counts = {"Horde": 0, "Medium": 0, "Tank": 0, "Wizard": 0}
        horde_types = {"Skeleton", "Archer", "Minion"}
        medium_types = {"Dragon", "Knight", "Valkyrie"}
        tank_types = {"Giant", "Balloon"}
        wizard_types = {"Wizard"}

        for troop in my_troops:
            if troop.name in horde_types:
                type_counts["Horde"] += 1
            elif troop.name in medium_types:
                type_counts["Medium"] += 1
            elif troop.name in tank_types:
                type_counts["Tank"] += 1
            elif troop.name in wizard_types:
                type_counts["Wizard"] += 1

        return max(type_counts, key=type_counts.get)

    avg_type = get_avg_troop_type(my_troops)

    deploy_x = random.randint(int(opp_com[0]) - 5, int(opp_com[0]) + 5)
    meploy_x = random.randint(int(my_com[0]) - 5, int(my_com[0]) + 5)


    # Check if enemy is damaging our tower
    def is_enemy_damaging_tower():
        for opp_troop in opp_troops:
            if opp_troop.position[1] < 25:  # Check if enemy troop is close enough to damage the tower
                return True
        return False

    # Deployment logic
    if is_enemy_damaging_tower():
        # Deploy offensive troops at (0, 0) when enemy is damaging our tower
        if available_elixir >= 5:
            if "Minion" in deployable_troops:
                deploy_list.list_.append(("Minion", (0, 0)))
            elif "Wizard" in deployable_troops:
                deploy_list.list_.append(("Wizard", (0, 0)))
            elif "Archer" in deployable_troops:
                deploy_list.list_.append(("Archer", (0, 0)))
    elif not opp_troops:
        if available_elixir >= 8:
            if "Giant" in deployable_troops and "Wizard" in deployable_troops:
                deploy_list.list_.append(("Giant", (0, 0)))
                deploy_list.list_.append(("Wizard", (0, 0)))
            elif "Valkyrie" in deployable_troops and "Dragon" in deployable_troops:
                deploy_list.list_.append(("Valkyrie", (0, 0)))
                deploy_list.list_.append(("Dragon", (0, 0)))
            elif "Knight" in deployable_troops and "Archer" in deployable_troops:
                deploy_list.list_.append(("Knight", (0, 0)))
                deploy_list.list_.append(("Archer", (0, 0)))
    else:
        if not my_troops:
            if 0 <= opp_com[1] <= 50:
                deploy_list.list_.append((bwc, (0, 0)))
            elif 50 < opp_com[1] <= 70:
                deploy_list.list_.append((bwc, (deploy_x, 20)))
            elif 70 < opp_com[1] <= 100:
                if any(t.name == "Wizard" for t in opp_troops):
                    deploy_list.list_.append((bwc, (deploy_x, 20)))
                elif bwc in ["Skeleton", "Archer", "Minion"]:
                    if any(t.name in ["Wizard", "Valkyrie", "Dragon"] for t in opp_troops):
                        deploy_list.list_.append((bwc, (deploy_x, 10)))
                    else:
                        deploy_list.list_.append((bwc, (0, 50)))
                elif bwc == "Wizard":
                    deploy_list.list_.append((bwc, (deploy_x, 10)))
                elif bwc == "Giant":
                    deploy_list.list_.append((bwc, (deploy_x, 30)))
                elif bwc in ["Valkyrie", "Knight"]:
                    if any(t.name in ["Minion", "Balloon"] for t in opp_troops):
                        deploy_list.list_.append((bwc, (0, 10)))
                    else:
                        deploy_list.list_.append((bwc, (deploy_x, 50)))
                elif bwc == "Dragon":
                    deploy_list.list_.append((bwc, (deploy_x, 50)))

        else:
            if avg_type == "Horde":
                if bwc in ["Dragon", "Giant", "Knight", "Valkyrie"]:
                    if 100 >= my_com[1] > 70:
                        deploy_list.list_.append((bwc, (meploy_x, 30)))
                    elif 70 >= my_com[1] > 50:
                        deploy_list.list_.append((bwc, (meploy_x, my_com[1] - 20)))
                    elif 50 >= my_com[1] > 40:
                        deploy_list.list_.append((bwc, (meploy_x, my_com[1])))
                    elif 40 >= my_com[1] > 0:
                        deploy_list.list_.append((bwc, (meploy_x, my_com[1] + 10)))    
                else:
                    deploy_list.list_.append((bwc, (deploy_x, 10)))
            elif avg_type in ["Medium", "Tank", "Wizard"]:
                if my_com[1] > 50:
                    deploy_list.list_.append((bwc, (meploy_x, 50)))
                elif 50 >= my_com[1] > 10:
                    deploy_list.list_.append((bwc, (meploy_x, my_com[1] - 10)))
                else:
                    deploy_list.list_.append((bwc, (meploy_x, my_com[1])))
