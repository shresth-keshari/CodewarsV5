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

def update_team_signal(opp_troops):
    """Updates the team signal dynamically based on enemy troops."""
    global team_signal
    current_names = set(team_signal.split(", ")) if team_signal else set()
    for troop in opp_troops:
        if troop.name not in current_names:
            current_names.add(troop.name)
    team_signal = ", ".join(current_names)

def deploy_troop(name, position, deployable):
    """Deploys a troop if available."""
    if name in deployable:
        deploy_list.list_.append((name, position))

def logic(arena_data: dict):
    global team_signal
    troops_data = Troops.troops_data
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]

    # Update Team Signal
    update_team_signal(opp_troops)

    # Define troop categories
    tank_troops = {"Giant", "Knight", "Prince"}
    swarm_troops = {"Barbarian", "Skeleton"}
    support_troops = {"Wizard", "Musketeer", "Archer"}
    
    enemy_tanks = [t for t in opp_troops if t.name in tank_troops]
    enemy_swarms = [t for t in opp_troops if t.name in swarm_troops]
    enemy_supports = [t for t in opp_troops if t.name in support_troops]
    
    deployable = my_tower.deployable_troops  # Available troops to deploy

    # --- Defense Strategies ---
    if enemy_tanks and enemy_supports:
        deploy_troop("Valkyrie", enemy_supports[0].position, deployable)
        deploy_troop("Skeleton", enemy_tanks[0].position, deployable)
        deploy_troop("Minions", enemy_tanks[0].position, deployable)

    elif enemy_tanks and enemy_swarms:
        centroid_x = sum(t.position[0] for t in enemy_swarms) // len(enemy_swarms)
        centroid_y = sum(t.position[1] for t in enemy_swarms) // len(enemy_swarms)
        deploy_troop("Valkyrie", (centroid_x, centroid_y), deployable)
        deploy_troop("Wizard", (random_x(-10, 10), 0), deployable)
        deploy_troop("Minions", (random_x(-5, 5), 0), deployable)

    elif enemy_swarms and enemy_supports:
        deploy_troop("Wizard", (random_x(-10, 10), 0), deployable)
        deploy_troop("Baby Dragon", (random_x(-10, 10), 0), deployable)
        deploy_troop("Giant", (random_x(-10, 10), 0), deployable)
        deploy_troop("Knight", (random_x(-5, 5), 0), deployable)

    elif enemy_supports:
        deploy_troop("Knight", enemy_supports[0].position, deployable)
        deploy_troop("Giant", (random_x(-10, 10), 0), deployable)
        deploy_troop("Wizard", (random_x(-10, 10), 0), deployable)

    # --- Heavy Push Handling ---
    if any(t.name in tank_troops for t in opp_troops):
        for troop in ["Giant", "Knight", "Wizard", "Baby Dragon"]:
            deploy_troop(troop, (random_x(-10, 10), 0), deployable)
        deploy_troop("Minions", (random_x(-10, 10), 0), deployable)

    # --- Continuous Spamming in Failsafe Mode ---
    while not deploy_list.list_:
        for troop in ["Giant", "Balloon", "Baby Dragon", "Wizard", "Minions"]:
            deploy_troop(troop, (random_x(-10, 10), 0), deployable)

    # --- Retaliation Handling ---
    if any(t[0] in {"Giant", "Knight", "Valkyrie"} for t in deploy_list.list_):
        deploy_troop("Baby Dragon", (random_x(-5, 5), 0), deployable)
        deploy_troop("Wizard", (random_x(-5, 5), 0), deployable)

    print(deploy_list)
