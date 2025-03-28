from teams.helper_function import Troops, Utils
import random

team_name = "AlgoAvengers"
troops = [Troops.wizard, Troops.minion, Troops.archer, Troops.barbarian, Troops.dragon, Troops.valkyrie, Troops.prince,
          Troops.knight]
deploy_list = Troops([])
team_signal = ""

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def min_elixir(arena_data:dict):
    my_tower = arena_data["MyTower"]
    trp_data = Troops.troops_data
    min_ele = 10
    best_troop = my_tower.deployable_troops[0]
    for troop_str in trp_data:
        if troop_str not in my_tower.deployable_troops:
            continue
        elif trp_data[troop_str].elixir < min_ele:
            best_troop = troop_str
            min_ele = trp_data[troop_str].elixir
    return best_troop

def deploy_on_advantage(arena_data:dict):
    my_tower = arena_data["MyTower"]
    if my_tower.deployable_troops[0] not in [Troops.wizard, Troops.dragon]:
        deploy_list.list_.append((my_tower.deployable_troops[0], (random_x(-20, 20), 10)))
        return
    elif Troops.valkyrie in my_tower.deployable_troops:
        deploy_list.list_.append((Troops.knight, (random_x(-20, 20), 10)))
        return
    elif Troops.knight in my_tower.deployable_troops:
        deploy_list.list_.append((Troops.knight, (random_x(-20, 20), 10)))
        return

def deploy(arena_data: dict):
    """
    DON'T TEMPER DEPLOY FUCNTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def update_my_troops(arena_data: dict):
    my_troops = arena_data["MyTroops"]
    my_list = []
    for troop in my_troops:
        if troop not in my_list:
            my_list.append(troop)
    return my_list

def update_opp_troops(arena_data: dict):
    opp_troops = arena_data["OppTroops"]
    opp_list = []
    for troop in opp_troops:
        if troop not in opp_list:
            opp_list.append(troop)
    return opp_list

def logic(arena_data: dict):
    global team_signal
    my_tower = arena_data["MyTower"]
    my_troops = arena_data["MyTroops"]
    opp_troops = arena_data["OppTroops"]
    deployable = my_tower.deployable_troops

    # Counters to all troops
    counters = {
        Troops.wizard: [Troops.wizard, Troops.prince, Troops.dragon, Troops.musketeer, Troops.knight, Troops.valkyrie],
        Troops.dragon: [Troops.wizard, Troops.musketeer, Troops.dragon, Troops.archer],
        Troops.giant: [Troops.prince, Troops.wizard, Troops.dragon, Troops.minion, Troops.knight, Troops.barbarian],
        Troops.balloon: [Troops.wizard, Troops.dragon, Troops.minion, Troops.archer, Troops.musketeer],
        Troops.valkyrie: [Troops.dragon, Troops.wizard, Troops.minion, Troops.knight, Troops.prince],
        Troops.prince: [Troops.skeleton, Troops.knight, Troops.wizard, Troops.minion, Troops.barbarian],
        Troops.knight: [Troops.minion, Troops.knight, Troops.valkyrie, Troops.prince, Troops.wizard],
        Troops.skeleton: [Troops.minion, Troops.skeleton, Troops.dragon, Troops.valkyrie, Troops.wizard],
        Troops.minion: [Troops.archer, Troops.minion, Troops.dragon, Troops.musketeer, Troops.wizard],
        Troops.archer: [Troops.minion, Troops.knight, Troops.dragon, Troops.wizard],
        Troops.musketeer: [Troops.knight, Troops.valkyrie, Troops.prince, Troops.wizard, Troops.archer],
        Troops.barbarian: [Troops.valkyrie, Troops.dragon, Troops.minion, Troops.wizard, Troops.knight],
    }
    opp_list = update_opp_troops(arena_data)
    my_list = update_my_troops(arena_data)

    # Initialize counter_present from team_signal
    counter_present = {}
    if team_signal != "":
        for pair_str in team_signal.split(","):
            pair = pair_str.split(":")
            counter_present[pair[0]] = pair[1] if pair[1]!="" else None

    # Check for new troops deployed by opponent
    for opp_troop in opp_list:
        if opp_troop.name not in list(counter_present.keys()):
            counter_present.update({opp_troop.name : None})

    # Check for old troops of opponent are killed
    to_pop_key = []
    opp_list_names = [opp_troop.name for opp_troop in opp_list]
    for opp_troop_name in counter_present:
        if opp_troop_name not in opp_list_names:
            to_pop_key.append(opp_troop_name)
    for opp_troop_name in to_pop_key:
        counter_present.pop(opp_troop_name)

    # Check if my troops died to opponent
    to_pop_value = []
    my_list_names = [my_troop.name for my_troop in my_list]
    for opp_troop_name in counter_present:
        if counter_present[opp_troop_name] not in my_list_names:
            to_pop_value.append(counter_present[opp_troop_name])
    for my_troop_name in to_pop_value:
        all_values = list(counter_present.values())
        all_keys = list(counter_present.keys())
        key = all_keys[all_values.index(my_troop_name)]
        counter_present[key] = None

    # Initialize dictionary to add deployed counters
    new_counters = {}
    # Determine counter and deploy in front of the opponent's troop
    for opp_troop_name in counter_present:
        if counter_present[opp_troop_name] is not None:
            continue
        for counter_name in counters[opp_troop_name]:
            opp_troop = opp_list[opp_list_names.index(opp_troop_name)]
            counter_troop = Troops.troops_data[counter_name]
            if my_tower.total_elixir >= counter_troop.elixir and counter_name in deployable:
                x_coord = opp_troop.position[0]
                y_coord = 100-opp_troop.position[1] if opp_troop.position[1]>50 else opp_troop.position[1]
                if y_coord < 50 and counter_troop.attack_range > 0:
                    # Place ranged troops slightly back to take advantage of their range when opponent's troop is in our half
                    y_coord = y_coord - counter_troop.attack_range if y_coord - counter_troop.attack_range > 0 else 0
                if opp_troop_name == Troops.wizard and counter_troop.attack_range == 0:
                    if opp_troop.position[1] > 50:
                        continue
                deploy_position = (x_coord, y_coord)
                deploy_list.list_.append((counter_name, deploy_position))
                new_counters[opp_troop_name] = counter_name
                break

    # Update counter_present from deployed counters
    counter_present.update(new_counters)

    # If no troops are placed by opponent and I have almost full elixir, deploy min elixir troop from hand
    if len(opp_list) == 0 and my_tower.total_elixir >= 9 and my_tower.game_timer >= 40:
        deploy_list.list_.append((min_elixir(arena_data), (random_x(-15, 15), 15)))
    # Deploy extra troops when I have an advantage
    elif None not in counter_present.values() and my_tower.total_elixir >= 8 and my_tower.game_timer >= 40:
        deploy_on_advantage(arena_data)
        print("AT AN ADVANTAGE!!")

    # Update team_signal from counter_present
    team_signal = ""
    for key, value in counter_present.items():
        team_signal += "{}:{},".format(key, value if value is not None else "")
    team_signal = team_signal.strip(",")



