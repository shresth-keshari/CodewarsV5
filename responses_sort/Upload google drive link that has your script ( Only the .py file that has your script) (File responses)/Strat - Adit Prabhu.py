from teams.helper_function import Troops, Utils
import numpy as np
import math

team_name = "Mathematical_Adit"
troops = [Troops.wizard, Troops.minion, Troops.archer, Troops.valkyrie, Troops.dragon, Troops.skeleton, Troops.knight, Troops.prince]
deploy_list = Troops([])
team_signal = "[['', '', '', '', '', '', '', ''], ['', '', '', ''], 10, 0, ['']]"

def deploy(arena_data:dict):
    """
    DON'T TEMPER DEPLOY FUCNTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def update_signal(team_signal, arena_data):
    troop_names = {'A': 'Archer', 'm': 'Minion', 'K': 'Knight', 'S': 'Skeleton', 'D': 'Dragon', 'V': 'Valkyrie', 'M': 'Musketeer', 'G': 'Giant', 'P': 'Prince', 'b': 'Barbarian', 'B': 'Balloon', 'W': 'Wizard', '': ''}
    troop_codes = {c: t for (t, c) in troop_names.items()}
    troop_elixirs = {"Archer": 3, "Minion": 3, "Knight": 3, "Skeleton": 3, "Dragon": 4, "Valkyrie": 4, "Musketeer": 4, "Giant": 5, "Prince": 5, "Barbarian": 3, "Balloon": 5, "Wizard": 5}
    opp_data = eval(team_signal)
    for troop in arena_data['OppTroops']:
        if troop_codes[troop.name] not in opp_data[0]:
            for i in range(8):
                if opp_data[0][i] == '':
                    opp_data[0][i] = troop_codes[troop.name]
                    break       
        if (troop.uid > opp_data[3]) and (troop_codes[troop.name] not in opp_data[1]):
            opp_data[1] = [troop_codes[troop.name] if (i == 0) else opp_data[1][i-1] for i in range(4)]
            opp_data[2] -= troop_elixirs[troop.name]
    opp_data[3] = arena_data['OppTroops'][-1].uid if arena_data['OppTroops'] else 0
    curr_cards = [troop_names[troop] for troop in opp_data[0] if (troop not in opp_data[1] and troop != '')] + ([''] * (4 - len([troop_names[troop] for troop in opp_data[0] if (troop not in opp_data[1] and troop != '')])))
    if(arena_data['MyTower'].game_timer % (20 - (10 * (arena_data['MyTower'].game_timer > 1200))) == 0):
        opp_data[2] = opp_data[2] + (opp_data[2] < 10)
    return str(opp_data), curr_cards

def get_distance(pos1, pos2):
    """Calculate Euclidean distance between two positions"""
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def determine_range_type(my_type, opp_type, my_pos, opp_pos, troop_stats):
    """Determine which range index to use based on distance"""
    distance = get_distance(my_pos, opp_pos) - troop_stats[my_type]['size'] - troop_stats[opp_type]['size']
    my_arange = troop_stats[my_type]['attack_range']
    opp_arange = troop_stats[opp_type]['attack_range']
    my_drange = troop_stats[my_type]['discovery_range']
    opp_drange = troop_stats[opp_type]['discovery_range']
    my_v = troop_stats[my_type]['velocity']
    opp_v = troop_stats[opp_type]['velocity']

    if (distance < my_arange and distance > opp_arange):
        return "Long", (distance - opp_arange)/opp_v
    elif (distance > my_arange and distance < opp_arange):
        return "Bad", (distance - my_arange)/my_v
    elif (distance < my_arange and distance < opp_arange):
        return "Short", 0
    elif (distance < my_drange):
        return "VLong", (distance - my_arange)/my_v
    elif (distance < opp_drange):
        return "Distract", (distance - opp_arange)/opp_v
    else:
        t = -1
        if (my_pos[1] > opp_pos[1] or math.fabs(my_pos[0] - opp_pos[0]) > max(my_drange, opp_drange)):
            t = -1
        else:
            t = (opp_pos[1] - my_pos[1] - math.sqrt(max(my_drange, opp_drange)**2 - (my_pos[0] - opp_pos[0])**2))/(my_v + opp_v)
        return "Irrelavant", t

def get_troop_stats():
    troop_stats = {
    "Archer": {"attack_range": 5 * 1.875, "splash": 0, "targets": ["Air", "Ground", "Building"], "health": 334, "damage": 118, "velocity": 0.36, "elixir": 3, "num_troops": 2, "attack_speed": 1, "discovery_range": 8 * 1.875, "size": 0.15 * 9.375, "type" : "Ground"},
    "Minion": {"attack_range": 2 * 1.875, "splash": 0, "targets": ["Air", "Ground", "Building"], "health": 252, "damage": 129, "velocity": 0.6, "elixir": 3, "num_troops": 3, "attack_speed": 1, "discovery_range": 4 * 1.875, "size": 0.15 * 9.375, "type" : "Air"},
    "Knight": {"attack_range": 0 * 1.875, "splash": 0, "targets": ["Ground", "Building"], "health": 1938, "damage": 221, "velocity": 0.36, "elixir": 3, "num_troops": 1, "attack_speed": 1, "discovery_range": 7 * 1.875, "size": 0.3 * 9.375, "type" : "Ground"},
    "Skeleton": {"attack_range": 0 * 1.875, "splash": 0, "targets": ["Ground", "Building"], "health": 89, "damage": 89, "velocity": 0.6, "elixir": 3, "num_troops": 10, "attack_speed": 1, "discovery_range": 4 * 1.875, "size": 0.15 * 9.375, "type" : "Ground"},
    "Dragon": {"attack_range": 3.5 * 1.875, "splash": 1.875, "targets": ["Air", "Ground", "Building"], "health": 1267, "damage": 176, "velocity": 0.6, "elixir": 4, "num_troops": 1, "attack_speed": 1, "discovery_range": 5 * 1.875, "size": 0.4 * 9.375, "type" : "Air"},
    "Valkyrie": {"attack_range": 0 * 1.875, "splash": 1.875, "targets": ["Ground", "Building"], "health": 2097, "damage": 195, "velocity": 0.36, "elixir": 4, "num_troops": 1, "attack_speed": 1, "discovery_range": 7 * 1.875, "size": 0.2 * 9.375, "type" : "Ground"},
    "Musketeer": {"attack_range": 6 * 1.875, "splash": 0, "targets": ["Air", "Ground", "Building"], "health": 792, "damage": 239, "velocity": 0.36, "elixir": 4, "num_troops": 1, "attack_speed": 2, "discovery_range": 8 * 1.875, "size": 0.2 * 9.375, "type" : "Ground"},
    "Giant": {"attack_range": 0 * 1.875, "splash": 0, "targets": ["Building"], "health": 5423, "damage": 337, "velocity": 0.12, "elixir": 5, "num_troops": 1, "attack_speed": 3, "discovery_range": 7 * 1.875, "size": 0.5 * 9.375, "type" : "Ground"},
    "Prince": {"attack_range": 0 * 1.875, "splash": 0, "targets": ["Ground", "Building"], "health": 1920, "damage": 392, "velocity": 0.6, "elixir": 5, "num_troops": 1, "attack_speed": 1, "discovery_range": 7 * 1.875, "size": 0.3 * 9.375, "type" : "Ground"},
    "Barbarian": {"attack_range": 0 * 1.875, "splash": 0, "targets": ["Ground", "Building"], "health": 736, "damage": 161, "velocity": 0.36, "elixir": 3, "num_troops": 3, "attack_speed": 2, "discovery_range": 5 * 1.875, "size": 0.25 * 9.375, "type" : "Ground"},
    "Balloon": {"attack_range": 0 * 1.875, "splash": 0, "targets": ["Building"], "health": 2226, "damage": 424, "velocity": 0.36, "elixir": 5, "num_troops": 1, "attack_speed": 2, "discovery_range": 5 * 1.875, "size": 0.4 * 9.375, "type" : "Air"},
    "Wizard": {"attack_range": 5.5 * 1.875, "splash": 1.875, "targets": ["Air", "Ground", "Building"], "health": 1100, "damage": 410, "velocity": 0.36, "elixir": 5, "num_troops": 1, "attack_speed": 1, "discovery_range": 8 * 1.875, "size": 0.25 * 9.375, "type" : "Ground"},
    }

    return troop_stats

def calc_troopvtroop_adv(our_name, opp_name, our_pos, opp_pos, troop_stats):
    range_type, time_to_encounter = determine_range_type(our_name, opp_name, our_pos, opp_pos, troop_stats)

    our_health = troop_stats[our_name]["health"]
    opp_health = troop_stats[opp_name]["health"]
    our_num = troop_stats[our_name]["num_troops"]
    opp_num = troop_stats[opp_name]["num_troops"]

    if range_type == "Irrelavant" or range_type == "Distract":
        return 0
    elif range_type == "VLong":
        if troop_stats[our_name]["attack_range"] > troop_stats[opp_name]["attack_range"]:
            range_type = "Long"
            time_to_encounter = (troop_stats[our_name]["attack_range"] - troop_stats[opp_name]["attack_range"])/troop_stats[opp_name]["velocity"]
        else:
            range_type = "Bad"
            time_to_encounter = (troop_stats[opp_name]["attack_range"] - troop_stats[our_name]["attack_range"])/troop_stats[our_name]["velocity"]

    if troop_stats[opp_name]["type"] in troop_stats[our_name]["targets"] and troop_stats[our_name]["type"] in troop_stats[opp_name]["targets"]:
        if range_type == "Bad":
            our_health = our_health - (time_to_encounter * troop_stats[opp_name]["damage"] / troop_stats[opp_name]["attack_speed"])
        elif range_type == "Long":
            opp_health = opp_health - (time_to_encounter * troop_stats[our_name]["damage"] / troop_stats[our_name]["attack_speed"])

        if troop_stats[our_name]["splash"]:
            opp_num = math.sqrt(opp_num)
        if troop_stats[opp_name]["splash"]:
            our_num = math.sqrt(our_num)
        
        num_killed = 1
        if our_health <= 0:
            num_killed = 1/256
        elif opp_health <= 0:
            num_killed = 256
        else:
            our_hits = opp_num * math.ceil(opp_health / (our_num * troop_stats[our_name]["damage"]))
            opp_hits = our_num * math.ceil(our_health / (opp_num * troop_stats[opp_name]["damage"]))

            num_killed = (opp_hits / troop_stats[opp_name]["attack_speed"]) / (our_hits / troop_stats[our_name]["attack_speed"])

            if num_killed > 256:
                num_killed = 256
            elif num_killed < 1/256:
                num_killed = 1/256
    
        return math.log2(num_killed) / troop_stats[opp_name]["num_troops"]
    
    else:
        rev = 1
        num = troop_stats[opp_name]["num_troops"]
        if troop_stats[opp_name]["type"] not in troop_stats[our_name]["targets"]:
            rev = -1
            opp_name, our_name = our_name, opp_name
            opp_pos, our_pos = our_pos, opp_pos
        
        our_health = troop_stats[our_name]["health"]
        opp_health = troop_stats[opp_name]["health"]
        our_num = troop_stats[our_name]["num_troops"]
        opp_num = troop_stats[opp_name]["num_troops"]

        if troop_stats[our_name]["splash"]:
            opp_num = math.sqrt(opp_num)
        elif troop_stats[opp_name]["splash"]:
            our_num = math.sqrt(our_num)
        
        if troop_stats[opp_name]["targets"] == ["Building"]:
            time = 50 / troop_stats[opp_name]["velocity"]
            our_hits = opp_num * math.ceil(opp_health / (our_num * troop_stats[our_name]["damage"]))
            num_killed = our_hits / troop_stats[our_name]["attack_speed"] * time
        else:
            time = 25 / troop_stats[opp_name]["velocity"]
            our_hits = opp_num * math.ceil(opp_health / troop_stats[our_name]["damage"]) / our_num
            num_killed = our_hits / troop_stats[our_name]["attack_speed"] * time
        
        ans =  rev * (math.log2(num_killed) / num) / 4
        if ans > 5:
            ans = 5
        elif ans < -5:
            ans = -5

        return ans
    

def calc_troop_scores(arena_data, troop_stats, strategy):
    troop_powers = {troop : (troop_stats[troop]["num_troops"] * troop_stats[troop]["health"] * troop_stats[troop]["damage"] / troop_stats[troop]["attack_speed"]) for troop in sorted(list(troop_stats.keys())) }
    
    # Check each position in the grid
    troop_scores = {}

    for our_troop in arena_data["MyTower"].deployable_troops:
        best_score = -float('inf')
        best_pos = (0, 0)
        for x in range(-25, 25, 1):
            for y in range(0, 50, 1):

                if strategy == "Danger" and get_distance((x, y), (0, 0)) > 30:
                    continue

                pos_score = 0
                splash_bonus = 0
                for opp_troop in arena_data["OppTroops"]:

                    if strategy == "Danger" and get_distance((0, 0), opp_troop.position) - troop_stats[opp_troop.name]["size"] - arena_data["MyTower"].size > 25:
                        continue

                    troop_adv = calc_troopvtroop_adv(our_troop, opp_troop.name, (x, y), opp_troop.position, troop_stats)

                    if (troop_stats[our_troop]["splash"] and (get_distance((x, y), opp_troop.position) - troop_stats[opp_troop.name]["size"] - troop_stats[our_troop]["size"] < troop_stats[our_troop]["attack_range"])):
                        splash_bonus += 0.1 * troop_powers[opp_troop.name] / math.sqrt(troop_stats[opp_troop.name]["num_troops"])
                    
                    pos_score += troop_adv * troop_powers[opp_troop.name] / math.sqrt(opp_troop.position[1] + 5)
                    pos_score += splash_bonus

                
                if pos_score > best_score:
                    best_score = pos_score
                    best_pos = (x, y)
                elif pos_score == best_score and (math.fabs(best_pos[0]) > math.fabs(x)):
                    best_score = pos_score
                    best_pos = (x, y)
        
        troop_scores[our_troop] = {'pos' : best_pos, 'score' : best_score}

    return troop_scores

def less_side(arena_data):
    left = 0
    right = 0
    for troop in arena_data["OppTroops"]:
        if troop.position[0] > 0:
            right += 1
        else:
            left += 1
    
    if right > left:
        return -1
    else:
        return 1

def aggressive_strategy(arena_data, troop_stats):
    """
    This strategy aggressively pushes troops towards the enemy tower,
    ensuring we don't deploy duplicate tanks or support troops unnecessarily.
    """
    tanks = ["Knight", "Giant", "Valkyrie"]
    area_damage_troops = ["Wizard", "Dragon", "Valkyrie"]
    fast_attackers = [ "Prince", "Minion", "Archer"]
    spam_troops = ["Skeleton"]

    deploy_positions = {
        "front": (less_side(arena_data) * 25, 50),  # Fast attackers
        "mid": (less_side(arena_data) * 25, 30),    # Area damage troops
        "back": (less_side(arena_data) * 25, 20)    # Tanks
    }

    elixir = arena_data["MyTower"].total_elixir

    position = deploy_positions["front"]

    # Check what is already deployed
    deployed_troops = {troop.name for troop in arena_data["MyTroops"]}

    # Deploy a tank first if not already deployed
    if not any(tank in deployed_troops for tank in tanks):
        for tank in tanks:
            if tank in arena_data["MyTower"].deployable_troops and elixir >= troop_stats[tank]["elixir"]:
                deploy_list.list_.append((tank, deploy_positions["front"]))
                elixir -= troop_stats[tank]["elixir"]
                break  # Only one tank at a time
    else:
        for troop in arena_data["MyTroops"]:
            if troop.name in tanks:
                position = troop.position

    # Deploy area damage troops behind the tank if not already deployed
    if not any(troop in deployed_troops for troop in area_damage_troops):
        for troop in area_damage_troops:
            if troop in arena_data["MyTower"].deployable_troops and elixir >= troop_stats[troop]["elixir"]:
                deploy_list.list_.append((troop, (position[0], position[1] - 15)))
                elixir -= troop_stats[troop]["elixir"]
    else:
        for troop in arena_data["MyTroops"]:
            if troop.name in area_damage_troops:
                position = troop.position

    # Deploy fast attackers at the front if not already deployed
    if not any(troop in deployed_troops for troop in fast_attackers):
        for troop in fast_attackers:
            if troop in arena_data["MyTower"].deployable_troops and elixir >= troop_stats[troop]["elixir"]:
                deploy_list.list_.append((troop, (position[0], position[1] - 10)))
                elixir -= troop_stats[troop]["elixir"]

    # Spam skeletons when elixir is high
    if position == deploy_positions["front"]:
        position = deploy_positions["mid"]

    if elixir >= 3:
        for troop in spam_troops:
            if troop in arena_data["MyTower"].deployable_troops:
                deploy_list.list_.append((troop, (position[0], position[1] - 5)))
                break  # Only deploy one spam unit per cycle



def logic(arena_data:dict):
    global team_signal
    team_signal, curr_cards = update_signal(team_signal, arena_data)
    stored_data = eval(team_signal)[4]
    
    strategy = stored_data[0]
    troop_stats = get_troop_stats()
    for opp_troop in arena_data["OppTroops"]:
        # ##print(opp_troop.position, get_distance((0, 0), opp_troop.position) - troop_stats[opp_troop.name]["size"] - arena_data["MyTower"].size)
        if (get_distance((0, 0), opp_troop.position) - troop_stats[opp_troop.name]["size"] - arena_data["MyTower"].size) < 15:
            strategy = "Danger"
            break
        else:
            strategy = "Normal"
    
    if strategy == "Normal" and arena_data["MyTower"].total_elixir >= 7:
        strategy = "Aggressive"
    
    if strategy != "Aggressive":
        troop_scores = calc_troop_scores(arena_data, troop_stats, strategy)

        max_score = -float('inf')
        best_troop = ""
        best_pos = (0, 0)
        for troop in sorted(list(troop_scores.keys())):
            if strategy == "Danger" and arena_data["MyTower"].total_elixir < troop_stats[troop]["elixir"]:
                continue
            elif troop_scores[troop]['score'] > max_score:
                max_score = troop_scores[troop]['score']
                best_troop = troop
                best_pos = troop_scores[troop]['pos']
        
        ##print(strategy, max_score)
        
        # ##print(strategy, best_troop, best_pos)
        
        if best_troop and strategy == "Danger":
            deploy_list.list_.append((best_troop, best_pos))
        elif max_score > 575000:
            deploy_list.list_.append((best_troop, best_pos))
            
        stored_data[0] = strategy
        team_signal = str(eval(team_signal)[:4] + [stored_data])
    
    else:
        #print(strategy)
        aggressive_strategy(arena_data, troop_stats)
