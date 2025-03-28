from teams.helper_function import Troops, Utils
import random

team_name = "bugsinbrains"
troops = [
    Troops.giant, Troops.dragon, Troops.valkyrie, Troops.wizard,
    Troops.minion, Troops.musketeer, Troops.archer, Troops.barbarian
]
deploy_list = Troops([])
team_signal = "Defend and Push"

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def deploy(arena_data: dict):
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    global team_signal
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    my_elixir = my_tower.total_elixir
    deployable = my_tower.deployable_troops
    my_troops = arena_data["MyTroops"]
    tower_pos = my_tower.position

    # Function to calculate distance
    def distance(a, b):
        return Utils.calculate_distance(a, b, type_troop=False)

    # Check for immediate threats to our tower
    threat_radius = 20
    for enemy in opp_troops:
        if distance(enemy.position, tower_pos) < threat_radius:
            # Determine counter based on enemy type
            if enemy.type == "air":
                if Troops.musketeer in deployable and my_elixir >= 4:
                    deploy_list.deploy_musketeer((random_x(), 0))
                    return
                elif Troops.archer in deployable and my_elixir >= 3:
                    deploy_list.deploy_archer((random_x(), 0))
                    return
                elif Troops.minion in deployable and my_elixir >= 3:
                    deploy_list.deploy_minion((random_x(), 0))
                    return
            else:
                if Troops.valkyrie in deployable and my_elixir >= 4:
                    deploy_list.deploy_valkyrie((random_x(), 0))
                    return
                elif Troops.wizard in deployable and my_elixir >= 5:
                    deploy_list.deploy_wizard((random_x(), 0))
                    return
                elif Troops.barbarian in deployable and my_elixir >= 3:
                    deploy_list.deploy_barbarian((random_x(), 0))
                    return
            break  # Handle the first threat found

    # Build a push with Giant as tank if possible
    if Troops.giant in deployable and my_elixir >= 5:
        deploy_list.deploy_giant((-20, 0))
        return

    # Support existing Giant with ranged/splash troops
    has_giant = any(t.name == "Giant" for t in my_troops)
    if has_giant:
        support_troops = [
            (Troops.dragon, 4), (Troops.wizard, 5),
            (Troops.valkyrie, 4), (Troops.musketeer, 4)
        ]
        for troop, cost in support_troops:
            if troop in deployable and my_elixir >= cost:
                deploy_list.deploy_dragon((-15, 0)) if troop == Troops.dragon else \
                deploy_list.deploy_wizard((-15, 0)) if troop == Troops.wizard else \
                deploy_list.deploy_valkyrie((-15, 0)) if troop == Troops.valkyrie else \
                deploy_list.deploy_musketeer((-15, 0))
                return

    # Deploy other high-value troops if possible
    high_value = [
        (Troops.dragon, 4), (Troops.valkyrie, 4),
        (Troops.wizard, 5), (Troops.musketeer, 4)
    ]
    for troop, cost in high_value:
        if troop in deployable and my_elixir >= cost:
            deploy_list.deploy_dragon((0, 0)) if troop == Troops.dragon else \
            deploy_list.deploy_valkyrie((0, 0)) if troop == Troops.valkyrie else \
            deploy_list.deploy_wizard((0, 0)) if troop == Troops.wizard else \
            deploy_list.deploy_musketeer((0, 0))
            return

    # Deploy cheapest available troop to cycle and maintain pressure
    cheap_troops = [
        (Troops.minion, 3), (Troops.barbarian, 3),
        (Troops.archer, 3)
    ]
    for troop, cost in cheap_troops:
        if troop in deployable and my_elixir >= cost:
            deploy_list.deploy_minion((random_x(), 0)) if troop == Troops.minion else \
            deploy_list.deploy_barbarian((random_x(), 0)) if troop == Troops.barbarian else \
            deploy_list.deploy_archer((random_x(), 0))
            return

    # Fallback: deploy first available troop if elixir permits
    for troop in deployable:
        cost = 5 if troop == Troops.giant or troop == Troops.wizard else \
               4 if troop == Troops.dragon or troop == Troops.valkyrie or troop == Troops.musketeer else \
               3
        if my_elixir >= cost:
            deploy_list.deploy_giant((random_x(), 0)) if troop == Troops.giant else \
            deploy_list.deploy_dragon((random_x(), 0)) if troop == Troops.dragon else \
            deploy_list.deploy_valkyrie((random_x(), 0)) if troop == Troops.valkyrie else \
            deploy_list.deploy_wizard((random_x(), 0)) if troop == Troops.wizard else \
            deploy_list.deploy_minion((random_x(), 0)) if troop == Troops.minion else \
            deploy_list.deploy_musketeer((random_x(), 0)) if troop == Troops.musketeer else \
            deploy_list.deploy_archer((random_x(), 0)) if troop == Troops.archer else \
            deploy_list.deploy_barbarian((random_x(), 0))
            return