import random
from teams.helper_function import Troops, Utils

team_name = "byteme"
troops = [
    Troops.wizard, Troops.minion, Troops.knight, Troops.balloon,
    Troops.dragon, Troops.skeleton, Troops.valkyrie, Troops.giant
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
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
        if troop.name not in current_names:
            team_signal = team_signal + ", " + troop.name if team_signal else troop.name

    # --- Troop Categories ---
    tank_troops = {"Giant", "Knight", "Prince"}
    swarm_troops = {"Barbarian", "Skeleton"}
    support_troops = {"Wizard", "Musketeer", "Archer"}
    exception_troops = {"Valkyrie", "Minions", "Balloon", "Baby Dragon"}

    # --- Identify Enemy Strategy ---
    enemy_tanks = [troop for troop in opp_troops if troop.name in tank_troops]
    enemy_swarms = [troop for troop in opp_troops if troop.name in swarm_troops]
    enemy_supports = [troop for troop in opp_troops if troop.name in support_troops]

    # --- Check Available Defenders ---
   # --- Check Available Defenders ---
    deployable = my_tower.deployable_troops  # ✅ Fixed typo

    # --- Defense Strategy ---
    if enemy_tanks and enemy_supports:
        # 🛡️ Tank + Support Defense
        if "Valkyrie" in deployable and "Valkyrie" in Troops.__dict__:
            deploy_list.list_.append((Troops.__dict__["Valkyrie"], enemy_supports[0].position))
            if "Skeleton" in deployable and "Skeleton" in Troops.__dict__:
                deploy_list.list_.append((Troops.__dict__["Skeleton"], enemy_tanks[0].position))
            elif "Minions" in deployable and "Minions" in Troops.__dict__:
                deploy_list.list_.append((Troops.__dict__["Minions"], enemy_tanks[0].position))
        elif "Giant" in deployable and "Giant" in Troops.__dict__:
            deploy_list.list_.append((Troops.__dict__["Giant"], (random_x(-20, 20), 0)))
            if "Wizard" in deployable and "Wizard" in Troops.__dict__:
                deploy_list.list_.append((Troops.__dict__["Wizard"], (random_x(-5, 5), 0)))
        else:
            deploy_list.list_.append((Troops.__dict__["Giant"], (random_x(-10, 10), 0)))
            deploy_list.list_.append((Troops.__dict__["Balloon"], (random_x(-10, 10), 0)))

    elif enemy_tanks and enemy_swarms:
        # 🛡️ Tank + Swarm Defense
        if "Valkyrie" in deployable and "Valkyrie" in Troops.__dict__:
            centroid_x = sum(t.position[0] for t in enemy_swarms) // len(enemy_swarms)
            centroid_y = sum(t.position[1] for t in enemy_swarms) // len(enemy_swarms)
            deploy_list.list_.append((Troops.__dict__["Valkyrie"], (centroid_x, centroid_y)))
        elif "Wizard" in deployable and "Wizard" in Troops.__dict__:
            deploy_list.list_.append((Troops.__dict__["Wizard"], (random_x(-10, 10), 0)))
        else:
            deploy_list.list_.append((Troops.__dict__["Knight"], (random_x(-10, 10), 0)))
            deploy_list.list_.append((Troops.__dict__["Minions"], (random_x(-5, 5), 0)))

    elif enemy_swarms and enemy_supports:
        # 🛡️ Swarm + Support Defense
        if "Wizard" in deployable and "Wizard" in Troops.__dict__:
            deploy_list.list_.append((Troops.__dict__["Wizard"], (random_x(-10, 10), 0)))
        elif "Baby Dragon" in deployable and "Baby Dragon" in Troops.__dict__:
            deploy_list.list_.append((Troops.__dict__["Baby Dragon"], (random_x(-10, 10), 0)))
        elif "Giant" in deployable and "Giant" in Troops.__dict__:
            deploy_list.list_.append((Troops.__dict__["Giant"], (random_x(-10, 10), 0)))
            if "Knight" in deployable and "Knight" in Troops.__dict__:
                deploy_list.list_.append((Troops.__dict__["Knight"], (random_x(-5, 5), 0)))

    elif enemy_supports:
        # 🛡️ Support Only Defense
        if "Knight" in deployable and "Knight" in Troops.__dict__:
            deploy_list.list_.append((Troops.__dict__["Knight"], enemy_supports[0].position))
        elif "Giant" in deployable and "Giant" in Troops.__dict__:
            deploy_list.list_.append((Troops.__dict__["Giant"], (random_x(-10, 10), 0)))
        else:
            print(deployable)
            deploy_list.list_.append((Troops.__dict__["Wizard"], (random_x(-10, 10), 0)))

    # --- Heavy Push Handling ---
    enemy_push_from_back = any(troop.name in tank_troops for troop in opp_troops)
    if enemy_push_from_back:
        for troop in ["Giant", "Knight", "Wizard", "Baby Dragon"]:
            if troop in deployable and troop in Troops.__dict__:
                deploy_list.list_.append((Troops.__dict__[troop], (random_x(-10, 10), 0)))
                return
        if "Minions" in deployable and "Minions" in Troops.__dict__:
            deploy_list.list_.append((Troops.__dict__["Minions"], (random_x(-10, 10), 0)))

    # --- Failsafe Handling (Push if No Defenders) ---
    if len(deploy_list.list_) == 0:
        if {"Giant", "Balloon", "Wizard", "Baby Dragon"} <= set(deployable) and \
        {"Giant", "Balloon", "Wizard", "Baby Dragon"} <= Troops.__dict__.keys():
            deploy_list.list_.append((Troops.__dict__["Giant"], (random_x(-10, 10), 0)))
            deploy_list.list_.append((Troops.__dict__["Balloon"], (random_x(-10, 10), 0)))
            deploy_list.list_.append((Troops.__dict__["Baby Dragon"], (random_x(-10, 10), 0)))
        elif "Minions" in deployable and "Minions" in Troops.__dict__:
            deploy_list.list_.append((Troops.__dict__["Minions"], (random_x(-10, 10), 0)))

    # --- Retaliation Handling ---
    if any(t[0].name in {"Giant", "Knight", "Valkyrie"} for t in deploy_list.list_):
        if "Baby Dragon" in deployable and "Baby Dragon" in Troops.__dict__:
            deploy_list.list_.append((Troops.__dict__["Baby Dragon"], (random_x(-5, 5), 0)))
        elif "Wizard" in deployable and "Wizard" in Troops.__dict__:
            deploy_list.list_.append((Troops.__dict__["Wizard"], (random_x(-5, 5), 0)))