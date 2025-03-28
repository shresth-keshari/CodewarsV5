import random, math
from teams.helper_function import Troops, Utils

team_name = "while ( true )"
troops = [Troops.dragon, Troops.giant, Troops.wizard, Troops.minion, Troops.prince, Troops.valkyrie, Troops.skeleton, Troops.knight]
deploy_list = Troops([])

team_signal = "10__----------------_000000000000_None_None_0_0___"

# Don't tamper
def deploy(arena_data: dict):
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

# Use to decompress Unicode string (see compress() function below) 
def decompress(compressed):  
    base = 65536

    # Check for the special case where the original number was all zeros.
    # In that case, the compression returns U+0000 repeated (leading_zero_count + 1) times.
    if all(ch == '\u0000' for ch in compressed):
        # The length of the compressed string is (leading_zero_count + 1)
        # so the original string had (len(compressed) - 1) zeros.
        return '0' * (len(compressed) - 1)
    
    # The first character encodes the number of leading zeros.
    leading_zero_count = ord(compressed[0])
    
    # The rest of the string is the base-65536 representation of the number.
    encoded_part = compressed[1:]
    num = 0
    for ch in encoded_part:
        num = num * base + ord(ch)
    
    # Convert the number back to a decimal string and reattach the leading zeros.
    original_str = '0' * leading_zero_count + str(num)
    return original_str

# Use to compress a string of integers like '0234028481090240'. Achieves >4 times compression. 
def compress(num_str):
    # Count leading zeros
    leading_zero_count = len(num_str) - len(num_str.lstrip('0'))
    
    # Handle the "all zero" case.
    if num_str.lstrip('0') == '':
        # All zeros: represent as (leading_zero_count + 1) zero characters (U+0000)
        return '\u0000' * (leading_zero_count + 1)
    
    num = int(num_str)
    base = 65536
    encoded_chars = []
    while num:
        num, rem = divmod(num, base)
        encoded_chars.append(chr(rem))
    encoded_str = ''.join(reversed(encoded_chars))
    
    # Prefix with a character encoding the count of leading zeros.
    prefix = chr(leading_zero_count)
    return prefix + encoded_str

# team_signal is a _ separated string. This gets us the ith substring (0 indexed), with optional decompression
def get(i, decomp=False):
    global team_signal
    try:
        elem = team_signal.split('_')[i]
        return decompress(elem) if decomp else elem
    except:
        return ''

# team_signal is a _ separated string. This sets the ith substring (0 indexed), with optional compression
# Change the default team_signal value on top of page if you want to add any substrings by adding team_signal += '_default_substr'
def put(string, i, comp=False):
    global team_signal
    li = team_signal.split('_')
    try:
        li[i] = compress(string) if comp else string
    except IndexError:
        li.append([compress(string)] if comp else string)
    team_signal = '_'.join(li)

# Keeps count of opponent elixir. Must be called each frame. Don't use directly (see logic())
def opp_elixir(arena_data, TROOP_DATA):
    elixir = int(get(0))
    OppTroops_UID = get(1, True)
    elapsed_frames = arena_data["MyTower"].game_timer
    elixir += 1 if (elapsed_frames <=1200 and elapsed_frames % 20 == 0) or (elapsed_frames > 1200 and elapsed_frames % 10 == 0) else 0
    elixir = 10 if elixir > 10 else elixir
    new_troops = [x for x in arena_data["OppTroops"] if f'{x.uid:02d}' not in map(''.join, zip(*[iter(OppTroops_UID)]*2))]
    elixir -= sum([TROOP_DATA[troop.name][1] for troop in new_troops])
    OppTroops_UID = ''.join(map(lambda x: f'{x.uid:02d}', arena_data["OppTroops"]))
    put(f"{int(elixir):02d}", 0)
    put(OppTroops_UID, 1, True)
    return int(elixir)

# Update opponent's deck and surity whether troop is present. Don't use directly (see logic())
def update_oppDeck(arena_data, TROOP_DATA):
    surity = list(get(3))
    oppDeck = list(map(''.join, zip(*[iter(get(2))]*2)))
    new_troops = [x.name for x in arena_data["OppTroops"] if f'{x.uid:02d}' not in map(''.join, zip(*[iter(get(1, True))]*2))]
    for i in range(len(new_troops)):
        if surity[list(TROOP_DATA.keys()).index(new_troops[i])] == '0':
            troop = new_troops[i]
            surity[list(TROOP_DATA.keys()).index(troop)] = '1'
            if len(new_troops) > 0:
                oppDeck.pop(0)
                oppDeck.append(f'{list(TROOP_DATA.keys()).index(troop):02d}')

    put(''.join(oppDeck), 2)
    put(''.join(surity), 3)
    return oppDeck

# Helper function for getProbOf
def probability(n, k, r):
    """
    Calculate the probability that at least one of the k items
    is present in one of the r boxes, where:
    
      n: total number of distinct items
      k: number of items satisfying condition A
      r: number of boxes (each box receives one item)
    
    Returns the probability:
        P = 1 - (C(n-k, r) / C(n, r))
    """
    # Validate inputs
    if r > n:
        raise ValueError("The number of boxes (r) cannot be greater than the total number of items (n).")
    if k > n:
        raise ValueError("The number of items satisfying the condition (k) cannot be greater than n.")
    
    # When no items satisfy condition A, the probability is 0.
    if k == 0:
        return 0.0
    
    # When no boxes are chosen, the probability is 0.
    if r == 0:
        return 0.0

    # Calculate the binomial coefficients using math.comb (Python 3.8+)
    total_ways = math.comb(n, r)
    ways_without_k = math.comb(n - k, r) if (n - k) >= r else 0

    # Calculate probability that at least one of the k items is chosen
    prob = 1 - ways_without_k / total_ways
    return prob

def getProbOf(arena_data, condition, TROOP_DATA):
    oppDeck = list(map(''.join, zip(*[iter(get(2))]*2)))
    k, n ,r = 0, 0, 0
    for i in range(12):
        if f'{i:02d}' in oppDeck:
            if oppDeck.index(f'{i:02d}') < 4:
                if condition(list(TROOP_DATA.keys())[i]):
                    return 1
        else:
            if condition(list(TROOP_DATA.keys())[i]):
                k+=1

    for i in range(4):
        if oppDeck[i] == '--':
            r+=1
    for i in range(12):
        if get(3)[i] == '0':
            n += 1
    return probability(n, k, r)

def giant_distraction(arena_data, opponent_troops, TROOP_DATA_2):
    target_set = False
    if len(opponent_troops) > 0:
        target_set = False
        for troop in arena_data['OppTroops']:
            if troop.target != None and (troop.target.name == 'Giant'):
                target_set = True
                break
    # If no giant is deployed and we have one available, deploy it
    if any([t in ['Giant'] for t in arena_data["MyTower"].deployable_troops]) and not any([t.name in ['Giant'] for t in arena_data["MyTroops"]]):
        if "Giant" in arena_data["MyTower"].deployable_troops:
            deploy_list.list_.append((Troops.giant, (0, 25)))

    # If we have a giant, check if opponents are targeting it
    follow_up = False
    giant = None
    for troop in arena_data["MyTroops"]:
        if troop.name == 'Giant':
            giant = troop
            if troop.health > 500:
                follow_up = True
            break
    if follow_up and (target_set or giant.position[1] >= 50):
        priority_order = ["Wizard", "Minion", "Dragon", "Skeleton", "Prince", "Barbarian", "Valkyrie", "Knight", "Archer"]
        for troop in arena_data["MyTower"].deployable_troops:
            if troop in priority_order and arena_data["MyTower"].total_elixir >= TROOP_DATA_2[troop]["elixir"]:
                deploy_list.list_.append((troop, (giant.position[0], min(50, giant.position[1] - 10))))
                break
                
        
    # If no action was taken or the strategy is finished, return False
    return False

def melee_defense(arena_data, opponent_troop, myDeck, BATTLES_2, TROOP_DATA_2):
    troop1 = opponent_troop
    counters1 = []
    for battle in BATTLES_2:
        if battle[0] in myDeck and TROOP_DATA_2[battle[0]]["elixir"] <= arena_data['MyTower'].total_elixir:
            if battle[1] == troop1.name:
                counters1.append((battle[0], TROOP_DATA_2[battle[0]]["DPS"]))
    if counters1:
        if troop1.name in myDeck:
            counters1.append((troop1.name, TROOP_DATA_2[troop1.name]["DPS"]))
        counters1.sort(key=lambda x: (TROOP_DATA_2[x[0]]['elixir'], x[1]))
        for c in counters1:
            if TROOP_DATA_2[c[0]]['type'] in TROOP_DATA_2[opponent_troop.name]['target_type']:
                if TROOP_DATA_2[c[0]]['attack_range'] > 0:
                    deploy_list.list_.append((c[0], (troop1.position[0], max(0, troop1.position[1] - 15))))
                else:
                    deploy_list.list_.append((c[0], (troop1.position[0], troop1.position[1] - 2)))
                return c[0]
    else:   
        bestTroop = None
        bestElixir = float('inf')
        if TROOP_DATA_2[troop1.name]['type'] == 'Air':
            for troop in myDeck:
                if 'Air' in TROOP_DATA_2[troop]['target_type']:
                    if TROOP_DATA_2[troop]['elixir'] <= arena_data['MyTower'].total_elixir and TROOP_DATA_2[troop]['elixir'] < bestElixir:
                        bestElixir = TROOP_DATA_2[troop]['elixir']
                        bestTroop = troop
            if bestTroop != None:
                deploy_list.list_.append((bestTroop, (troop1.position[0], troop1.position[1] - 5)))
                return bestTroop
    canDeploy = []
    for troop in myDeck:
        if TROOP_DATA_2[troop]['elixir'] <= arena_data['MyTower'].total_elixir:
            canDeploy.append(troop)
    if canDeploy:
        deploy_list.list_.append((random.choice(canDeploy), (troop1.position[0], max(0, troop1.position[1] - 2))))
    return False

def air_attack(arena_data, TOWER_ORDER, TROOP_DATA_2, TROOP_DATA):
    # Organize opponents into lanes - only include unflagged troops with y > 50
    left_lane = {"opp_troops": [], "my_troops": []}
    center_lane = {"opp_troops": [], "my_troops": []}
    right_lane = {"opp_troops": [], "my_troops": []}
    
    # Categorize opponent troops
    for troop in arena_data["OppTroops"]:
        # Only include unflagged troops with y position > 50
        if troop.position[1] > 50:
            x_pos = troop.position[0]
            if x_pos < -8:  # Left lane
                left_lane["opp_troops"].append(troop)
            elif x_pos > 8:  # Right lane
                right_lane["opp_troops"].append(troop)
            else:  # Center lane
                center_lane["opp_troops"].append(troop)
    
    # Categorize my troops
    for troop in arena_data["MyTroops"]:
        x_pos = troop.position[0]
        if x_pos < -8:  # Left lane
            left_lane["my_troops"].append(troop)
        elif x_pos > 8:  # Right lane
            right_lane["my_troops"].append(troop)
        else:  # Center lane
            center_lane["my_troops"].append(troop)
    # i. Check if we have air troops in my deck, choose one with higher score in TOWER_ORDER
    my_air_troops = []
    for troop_name in arena_data["MyTower"].deployable_troops:
        if TROOP_DATA_2[troop_name]["type"] == "Air":
            my_air_troops.append(troop_name)
    
    if not my_air_troops:
        return False
        
    # Sort air troops based on TOWER_ORDER (lower index = higher priority)
    my_air_troops.sort(key=lambda t: TOWER_ORDER.index(t) if t in TOWER_ORDER else 999)
    best_air_troop = my_air_troops[0]
    
    
    # ii. Check if opponent has no unflagged air troops in specific lanes
    lanes_without_air = []
    for lane_name, lane_data in [("left", left_lane), ("center", center_lane), ("right", right_lane)]:
        has_air_troop = False
        for troop in lane_data["opp_troops"]:
            if TROOP_DATA_2[troop.name]["type"] == "Air":
                has_air_troop = True
                break
        
        if not has_air_troop:
            lanes_without_air.append(lane_name)
    
    if not lanes_without_air:
        return False
    
    # Check if any air troop is in opponent's deployable deck
    def is_air_troop(troop_name):
        return TROOP_DATA_2[troop_name]["type"] == "Air"
        
    air_prob = getProbOf(arena_data, is_air_troop, TROOP_DATA)
    
    # If probability is high, check elixir advantage
    if air_prob > 0.7:
        return False
    
    # iii-iv. Choose the lane with no air troops, if tie, choose by DPS difference
    lane_dps_diff = {}
    for lane_name in lanes_without_air:
        if lane_name == "left":
            lane_data = left_lane
        elif lane_name == "right":
            lane_data = right_lane
        else:
            lane_data = center_lane
            
        opp_dps = sum(TROOP_DATA_2[troop.name]["DPS"] for troop in lane_data["opp_troops"])
        my_dps = sum(TROOP_DATA_2[troop.name]["DPS"] for troop in lane_data["my_troops"])
        lane_dps_diff[lane_name] = opp_dps - my_dps
    
    # Choose lane with minimum DPS difference
    best_lane = min(lane_dps_diff, key=lane_dps_diff.get) if lane_dps_diff else lanes_without_air[0]
    
        
    # vi-vii. Deploy troops
    # Determine deployment positions based on lane
    if best_lane == "left":
        air_pos = (-25, 50)  # 10 points behind center
    elif best_lane == "right":
        air_pos = (25, 50)  # 10 points behind center
    else:  # center
        air_pos = (0, 50)  # 10 points behind center
    
    # Deploy air troop
    deploy_list.list_.append((best_air_troop, air_pos))   
    return True

def logic(arena_data: dict):
    # Update opponent's state
    global team_signal
    # Outcomes of all one v one battles [winner, loser, winner_remaining_health, winner_remaining_troops]
    BATTLES_2 = [
        ["Minion", "Archer", 252, 1],
        ["Knight", "Archer", 1112, 1],
        ["Skeleton", "Archer", 534, 6],
        ["Dragon", "Archer", 559, 1],
        ["Valkyrie", "Archer", 1153, 1],
        ["Archer", "Musketeer", 334, 1],
        ["Prince", "Archer", 1448, 1],
        ["Archer", "Barbarian", 12, 1],
        ["Wizard", "Archer", 746, 1],
        ["Minion", "Knight", 756, 3],
        ["Minion", "Skeleton", 756, 3],
        ["Minion", "Dragon", 252, 1],
        ["Minion", "Valkyrie", 756, 3],
        ["Minion", "Musketeer", 517, 3],
        ["Minion", "Prince", 756, 3],
        ["Minion", "Barbarian", 756, 3],
        ["Wizard", "Minion", 584, 1],
        ["Skeleton", "Knight", 623, 7],
        ["Dragon", "Knight", 1267, 1],
        ["Knight", "Valkyrie", 0, 1],
        ["Valkyrie", "Knight", 0, 1],
        ["Knight", "Musketeer", 1460, 1],
        ["Prince", "Knight", 815, 1],
        ["Knight", "Barbarian", 328, 1],
        ["Knight", "Wizard", 0, 1],
        ["Wizard", "Knight", 0, 1],
        ["Dragon", "Skeleton", 1267, 1],
        ["Skeleton", "Musketeer", 801, 9],
        ["Skeleton", "Prince", 623, 7],
        ["Skeleton", "Barbarian", 623, 7],
        ["Wizard", "Skeleton", 210, 1],
        ["Dragon", "Musketeer", 789, 1],
        ["Dragon", "Prince", 1267, 1],
        ["Dragon", "Barbarian", 1267, 1],
        ["Wizard", "Dragon", 396, 1],
        ["Prince", "Musketeer", 1681, 1],
        ["Barbarian", "Musketeer", 1491, 3],
        ["Wizard", "Musketeer", 861, 1],
        ["Prince", "Barbarian", 1276, 1],
        ["Prince", "Wizard", 690, 1],
        ["Wizard", "Barbarian", 939, 1],
        ["Dragon", "Valkyrie", 1267, 1],
        ["Valkyrie", "Skeleton", 1296, 1],
        ["Prince", "Valkyrie", 750, 1],
        ["Valkyrie", "Barbarian", 1131, 1],
        ["Valkyrie", "Wizard", 0, 1],
        ["Wizard", "Valkyrie", 0, 1],
        ["Valkyrie", "Musketeer", 1619, 1]
    ]
    # Scores of all troops based on BATTLE outcomes
    TOWER_ORDER = ['Prince', 'Skeleton', 'Wizard', 'Giant', 'Balloon', 'Valkyrie', 'Knight', 'Dragon', 'Barbarian', 'Minion', 'Musketeer', 'Archer']
    # Basic stats about troops
    TROOP_DATA = {
        "Archer": ("a", 1.5, 2, 196.66),
        "Dragon": ("d", 4, 1, 293.33),
        "Skeleton": ("e", 0.3, 10, 148.33),
        "Wizard": ("f", 5, 1, 683.333),
        "Minion": ("g", 5.0/3, 3, 215),
        "Giant": ("h", 5, 1, 187.22),
        "Balloon": ("b", 5, 1, 353.33),
        "Barbarian": ("c", 1, 3, 134.166),
        "Knight": ("k", 3, 1, 368.33),
        "Valkyrie": ("i", 4, 1, 325),
        "Musketeer": ("j", 4, 1, 199.166),
        "Prince": ("l", 5, 1, 326.66)
    }
    # Useful stats about troops
    TROOP_DATA_2 = {
        "Archer": {"health": 668/2, "DPS": 393.33/2, "attack_range": 5, "type": "Ground", "target_type": ["Air", "Ground", "Building"], "velocity": 3, "num": 2, "elixir": 3},
        "Minion": {"health": 756/3, "DPS": 645/3, "attack_range": 2, "type": "Air", "target_type": ["Air", "Ground", "Building"], "velocity": 5, "num": 3, "elixir": 3},
        "Knight": {"health": 1938, "DPS": 368.33, "attack_range": 0, "type": "Ground", "target_type": ["Ground", "Building"], "velocity": 3, "num": 1, "elixir": 3},
        "Skeleton": {"health": 890/10, "DPS": 1483.33/10, "attack_range": 0, "type": "Ground", "target_type": ["Ground", "Building"], "velocity": 5, "num": 10, "elixir": 3},
        "Dragon": {"health": 1267, "DPS": 293.33, "attack_range": 3.5, "type": "Air", "target_type": ["Air", "Ground", "Building"], "velocity": 5, "num": 1, "elixir": 4},
        "Valkyrie": {"health": 2097, "DPS": 325, "attack_range": 0, "type": "Ground", "target_type": ["Ground", "Building"], "velocity": 3, "num": 1, "elixir": 4},
        "Musketeer": {"health": 792, "DPS": 199.167, "attack_range": 6, "type": "Ground", "target_type": ["Air", "Ground", "Building"], "velocity": 3, "num": 1, "elixir": 4},
        "Giant": {"health": 5423, "DPS": 187.22, "attack_range": 0, "type": "Ground", "target_type": ["Building"], "velocity": 1, "num": 1, "elixir": 5},
        "Prince": {"health": 1920, "DPS": 653.33, "attack_range": 0, "type": "Ground", "target_type": ["Ground", "Building"], "velocity": 5, "num": 1, "elixir": 5},
        "Barbarian": {"health": 2208/3, "DPS": 402.5/3, "attack_range": 0, "type": "Ground", "target_type": ["Ground", "Building"], "velocity": 3, "num": 3, "elixir": 3},
        "Balloon": {"health": 2226, "DPS": 353.33, "attack_range": 0, "type": "Air", "target_type": ["Building"], "velocity": 3, "num": 1, "elixir": 5},
        "Wizard": {"health": 1100, "DPS": 683.33, "attack_range": 5.5, "type": "Ground", "target_type": ["Air", "Ground", "Building"], "velocity": 3, "num": 1, "elixir": 5},
        "MyTower": {"health": 7032, "DPS": 263.33 , "attack_range": 12.5, "type": "Building", "target_type": ["Air", "Ground"], "velocity": 0, "num": 1},
        "OppTower": {"health": 7032, "DPS": 263.33 , "attack_range": 12.5, "type": "Building", "target_type": ["Air", "Ground"], "velocity": 0, "num": 1},
        "DummyTower": {"health": 7032, "DPS": 0 , "attack_range": 0, "type": "Building", "target_type": ["Air", "Ground"], "velocity": 0, "num": 1}
    }

    oppDeck = update_oppDeck(arena_data, TROOP_DATA)
    oppElixir = opp_elixir(arena_data, TROOP_DATA)
    myElixir = arena_data["MyTower"].total_elixir
    game_timer = arena_data["MyTower"].game_timer
    high_threats = []
    low_threats = []
    done = []
    highest_threats = 0
    for troop in arena_data["OppTroops"]:
        if troop.name not in done and troop.health * TROOP_DATA_2[troop.name]['num'] > 300:
            score1 = TOWER_ORDER.index(troop.name) // 4
            score2 = troop.position[1] // 25
            if troop.target != None and troop.target.name.startswith('Tower'):
                high_threats.append((troop, 10*(score1 + score2)))
                highest_threats += 1
            elif (troop.position[1] <= 50 and troop.target == None) and troop.position[1] <= 25:
                high_threats.append((troop, score1 + score2))
            else:
                low_threats.append((troop, score1 + score2))
            done.append(troop.name)
    high_threats.sort(key = lambda x: x[1])
    low_threats.sort(key = lambda x: x[1])

    ############# DEFENSE STARTS HERE ##############

    myDeck = arena_data["MyTower"].deployable_troops
    if ((len(high_threats) >= 2 and any([t in ['Giant'] for t in arena_data["MyTower"].deployable_troops])) or any([x.name in ['Giant'] for x in arena_data["MyTroops"]])) and highest_threats == 0:
        giant_distraction(arena_data, arena_data["OppTroops"], TROOP_DATA_2)
    else:
        for troop in high_threats:
            temp = melee_defense(arena_data, troop[0], myDeck, BATTLES_2, TROOP_DATA_2)
            if temp != False:
                myDeck.remove(temp)

    ############# OFFENSE STARTS HERE ##############

    if (myElixir >= 9 and game_timer > 40 and (arena_data["MyTower"].health - arena_data["OppTower"].health < 3000) and len(low_threats) <= 3) or (len(low_threats) <= 1 and game_timer >= 40 and oppElixir <= 3):
        li = ['Prince', 'Wizard', 'Dragon', 'Valkyrie', 'Knight']
        if 'Dragon' in myDeck:
            air_attack(arena_data, TOWER_ORDER, TROOP_DATA_2, TROOP_DATA)
        for l in li:
            if l in myDeck:
                # Divide arena into two side lanes: left (-25 to -8) and right (8 to 25)
                lanes = {
                    "left": {"my_dps": 0, "opp_dps": 0, "position": (-25, 50)},
                    "right": {"my_dps": 0, "opp_dps": 0, "position": (25, 50)}
                }
                
                # Calculate opponent DPS in each lane (only for unflagged troops)
                for troop in arena_data["OppTroops"]:
                    x_pos = troop.position[0]
                    if -25 <= x_pos < -8:
                        lanes["left"]["opp_dps"] += TROOP_DATA_2[troop.name]["DPS"]
                    elif 8 < x_pos <= 25:
                        lanes["right"]["opp_dps"] += TROOP_DATA_2[troop.name]["DPS"]
                
                # Calculate my DPS in each lane
                for troop in arena_data["MyTroops"]:
                    x_pos = troop.position[0]
                    if -25 <= x_pos < -8:
                        lanes["left"]["my_dps"] += TROOP_DATA_2[troop.name]["DPS"]
                    elif 8 < x_pos <= 25:
                        lanes["right"]["my_dps"] += TROOP_DATA_2[troop.name]["DPS"]
                
                # Calculate lane scores (lower is better)
                for lane_name in lanes:
                    lanes[lane_name]["score"] = lanes[lane_name]["opp_dps"] - lanes[lane_name]["my_dps"]
                
                # Find the lane with the lowest score
                best_lane = min(lanes.keys(), key=lambda lane: lanes[lane]["score"])
                
                # Deploy the troop in the best lane
                deploy_list.list_.append((l, lanes[best_lane]["position"]))
                break

                    


    

