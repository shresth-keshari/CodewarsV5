from teams.helper_function import Troops, Utils
# arena_data dataflow game.py tower.py
team_name = "Jyotirya"
troops = [Troops.prince,Troops.minion,Troops.archer,Troops.knight,Troops.dragon,Troops.skeleton,Troops.wizard,Troops.valkyrie]
deploy_list = Troops([])
team_signal = "h"

def deploy(arena_data:dict):
    """
    DON'T TEMPER DEPLOY FUCNTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal  
def calculate_score(troops1, troops_data={}, troops2={}, score=0,a=1):
    for troop in troops1:
        data = troops_data[troop["name"]]
        for ourtroop in troops2:
            if ourtroop["name"] in data["Extreme Danger"]:
                score += 2/a
            elif ourtroop["name"] in data["Danger"]:
                score += 1/a
            elif ourtroop["name"] in data["Extreme Danger From"]:
                score -= 2/a 
            elif ourtroop["name"] in data["Danger From"]:
                score -= 1/a
            elif ourtroop["name"] in data["No Effect"]:
                score -= 0.5/a
    return score
def combine(positions):
    if not positions:
        return []
    positions.sort()
    merged = [positions[0]]
    for current in positions[1:]:
        prev = merged[-1]
        if current[0] <= prev[1]:  
            merged[-1] = (prev[0], max(prev[1], current[1]))
        else:
            merged.append(current)
    return merged

def in_interval(n, intervals):
    for start, end in intervals:
        if start <= n <= end:
            return True
    return False
def calculate_initial_score(troops):
    score = 0
    for troop in troops :
        if troop["name"] == "Archer":
            score += 3
        elif troop["name"] == "Minion":
            score += 3
        elif troop["name"] == "Knight":
            score += 3
        elif troop["name"] == "Skeleton":
            score += 3
        elif troop["name"] == "Barbarian":
            score += 3
        elif troop["name"] == "Dragon":
            score += 4
        elif troop["name"] == "Valkyrie":
            score += 4
        elif troop["name"] == "Musketeer":
            score += 4
        elif troop["name"] == "Giant":
            score += 5
        elif troop["name"] == "Prince":
            score += 5
        elif troop["name"] == "Balloon":
            score += 5
        elif troop["name"] == "Wizard":
            score += 6
    return score
def indentifyfightregions(ourcenter_positions,center_positions):
    fight_regions = ourcenter_positions + center_positions
    fight_regions = combine(fight_regions)
    return fight_regions
def logic(arena_data:dict):
    deployable = arena_data["MyTower"].deployable_troops
    opponent_troops = []
    troops_data = {
    "Archer": {
        "Extreme Danger": {"Ballon"},
        "Danger": {"Barbarian", "Giant"},
        "Extreme Danger From": {"Wizard", "Valkyrie", "Prince", "Skeleton"},
        "Danger From": {"Knight", "Dragon"},
        "Equal Fight": {"Archer", "Minion", "Musketeer"},
        "No Effect": set()
    },
    "Minion": {
        "Extreme Danger": {"Knight", "Skeleton", "Ballon", "Prince", "Barbarian", "Valkyrie"},
        "Danger": {"Giant"},
        "Extreme Danger From": {"Wizard"},
        "Danger From": {"Dragon"},
        "Equal Fight": {"Minion", "Archer", "Musketeer"},
        "No Effect": set()
    },
    "Knight": {
        "Extreme Danger": set(),
        "Danger": {"Giant", "Archer", "Musketeer"},
        "Extreme Danger From": {"Skeleton", "Minion", "Dragon"},
        "Danger From": set(),
        "Equal Fight": {"Prince", "Valkyrie", "Barbarian", "Knight", "Wizard"},
        "No Effect": {"Ballon"}
    },
    "Skeleton": {
        "Extreme Danger": {"Archer", "Knight", "Musketeer", "Prince"},
        "Danger": {"Giant", "Barbarian"},
        "Extreme Danger From": {"Wizard", "Valkyrie", "Minion", "Dragon"},
        "Danger From": set(),
        "Equal Fight": {"Skeleton"},
        "No Effect": {"Ballon"}
    },
    "Barbarian": {
        "Extreme Danger": set(),
        "Danger": {"Archer", "Musketeer", "Giant"},
        "Extreme Danger From": {"Minion", "Dragon"},
        "Danger From": {"Skeleton", "Wizard", "Valkyrie"},
        "Equal Fight": {"Barbarian", "Knight", "Prince"},
        "No Effect": {"Ballon"}
    },
    "Dragon": {
        "Extreme Danger": {"Ballon", "Knight", "Prince", "Valkyrie", "Skeleton", "Barbarian"},
        "Danger": {"Archer", "Minion", "Giant", "Musketeer"},
        "Extreme Danger From": set(),
        "Danger From": {"Wizard"},
        "Equal Fight": {"Dragon"},
        "No Effect": set()
    },
    "Valkyrie": {
        "Extreme Danger": {"Skeleton", "Archer"},
        "Danger": {"Giant", "Barbarian", "Musketeer"},
        "Extreme Danger From": {"Minion", "Dragon"},
        "Danger From": set(),
        "Equal Fight": {"Knight", "Prince", "Valkyrie", "Wizard"},
        "No Effect": {"Ballon"}
    },
    "Musketeer": {
        "Extreme Danger": {"Ballon"},
        "Danger": {"Giant"},
        "Extreme Danger From": {"Skeleton"},
        "Danger From": {"Wizard", "Valkyrie", "Prince", "Knight", "Barbarian", "Dragon"},
        "Equal Fight": {"Minion", "Archer", "Musketeer"},
        "No Effect": set()
    },
    "Giant": {
        "Extreme Danger": set(),
        "Danger": set(),
        "Extreme Danger From": set(),
        "Danger From": {"Archer", "Minion", "Knight", "Skeleton", "Barbarian", "Dragon", "Valkyrie", "Musketeer", "Prince", "Wizard"},
        "Equal Fight": set(),
        "No Effect": {"Ballon", "Giant"}
    },
    "Prince": {
        "Extreme Danger": {"Archer", "Musketeer"},
        "Danger": {"Giant"},
        "Extreme Danger From": set(),
        "Danger From": {"Minion", "Dragon", "Skeleton"},
        "Equal Fight": {"Barbarian", "Prince", "Knight", "Valkyrie", "Wizard"},
        "No Effect": {"Ballon"}
    },
    "Balloon": {
        "Extreme Danger": set(),
        "Danger": set(),
        "Extreme Danger From": set(),
        "Danger From": {"Wizard", "Dragon", "Minion", "Archer", "Musketeer"},
        "Equal Fight": set(),
        "No Effect": {"Ballon", "Giant", "Skeleton", "Knight", "Prince", "Barbarian", "Valkyrie"}
    },
    "Wizard": {
        "Extreme Danger": {"Archer", "Minion", "Skeleton", "Ballon"},
        "Danger": {"Barbarian", "Musketeer", "Giant", "Dragon"},
        "Extreme Danger From": set(),
        "Danger From": {"Prince", "Knight", "Valkyrie"},
        "Equal Fight": { "Wizard"},
        "No Effect": set()
    }
    }
    specific_troop_positions= {
        "Minion": "Center",
        "Knight": "Front",
        "Wizard": "Back",
        "Dragon": "Center",
        "Prince": "Front",
        "Archer": "Back",
        "Balloon": "Center",
        "Giant": "Front",
        "Musketeer": "Back",
        "Skeleton": "Center",
        "Valkyrie": "Front",
        "Barbarian": "Center"
        }
    troops_score= {
        "Minion": 3,
        "Knight": 3,
        "Wizard": 6,
        "Dragon": 4,
        "Prince": 5,
        "Archer": 3,
        "Balloon": 5,
        "Giant": 5,
        "Musketeer": 4,
        "Skeleton": 3,
        "Valkyrie": 4,
        "Barbarian": 3
    }
    for troop in arena_data["OppTroops"]:
        opponent_troops.append({ 'name' : troop.name, 'position' : troop.position})
        
    our_troops = []
    for troop in arena_data["MyTroops"]:
        our_troops.append({ 'name' : troop.name, 'position' : troop.position})

    region = [" Attack "," Center ", " Defend "]
    current_region = region[0]
    for troop in opponent_troops:
        ycoordinate = troop["position"][1]
        if ycoordinate < 25:
            current_region = region[2]
            break 
        elif ycoordinate < 80:
            current_region = region[1]


    if current_region == region[2]:
        center_positions = []
        for troop in opponent_troops:
            posy = troop["position"][1]
            pos = troop["position"][0]
            if posy < 25:
                center_positions.append((pos-5 if pos-5 >= -25 else -25 , pos+5 if pos+5 <= 25 else 25))
        center_positions = combine(center_positions)
        ourcenter_positions = []
        for troop in our_troops:
            posy = troop["position"][1]
            pos = troop["position"][0]
            if posy >= 0 and posy < 25:
                ourcenter_positions.append((pos-5 if pos-5 >= -25 else -25 , pos+5 if pos+5 <= 25 else 25))
        ourcenter_positions = combine(ourcenter_positions)
        fight_regions = indentifyfightregions(ourcenter_positions,center_positions)
        weakest_regions= None
        opponent_troops_in_weak_regions = []
        our_troops_in_weak_regions = []
        for region in fight_regions:
            opponent_troops_in_region = [troop for troop in opponent_troops if region[0] <= troop["position"][0] <= region[1] and troop["position"][1] <= 25]
            our_troops_in_region = [troop for troop in our_troops if region[0] <= troop["position"][0] <= region[1] and troop["position"][1] <= 25]
            opponent_score = calculate_initial_score(opponent_troops_in_region)
            our_score = calculate_initial_score(our_troops_in_region)
            opponent_score = calculate_score(opponent_troops_in_region, troops_data, our_troops_in_region, opponent_score,1)    
            our_score = calculate_score(our_troops_in_region, troops_data, opponent_troops_in_region, our_score,1)
            result = our_score - opponent_score
            if weakest_regions is None:
                weakest_regions = {"result":result, "region":region}
                opponent_troops_in_weak_regions = opponent_troops_in_region
                our_troops_in_weak_regions = our_troops_in_region
            elif weakest_regions["result"] > result:
                weakest_regions = {"result":result, "region":region}
                opponent_troops_in_weak_regions = opponent_troops_in_region
                our_troops_in_weak_regions = our_troops_in_region
        #which troop to deploy
        troop_data={}
        for troop in troops:
            score = 0
            score=calculate_score([{"name" : troop}], troops_data, opponent_troops_in_weak_regions, score,1)
            troop_data[troop] = score
        for troop in troops:
            if troops_score[troop] > arena_data["MyTower"].total_elixir:
                troop_data[troop] -= 2
        sorted_troops = sorted(troop_data, key=troop_data.get, reverse=True)
        best_troop = None
        for troop in sorted_troops:
            if troop in deployable:
                best_troop = troop
                break
        #where to deploy
        Deploy_position=(0,25)
        if our_troops_in_weak_regions == []:
            for opponent_troop in opponent_troops_in_weak_regions:
                if opponent_troop["position"][1] < Deploy_position[1]:
                    if(opponent_troop["position"][1] > 50):
                        Deploy_position = (opponent_troop["position"][0],0)
                    else: 
                        Deploy_position = opponent_troop["position"]                   
        else :
            for our_troop in our_troops_in_weak_regions:
                if our_troop["position"][1] < Deploy_position[1] : 
                    Deploy_position = our_troop["position"]
    
        if specific_troop_positions[best_troop] == "Center":
            Deploy_position = (Deploy_position[0], Deploy_position[1])
        elif specific_troop_positions[best_troop] == "Front":
            Deploy_position = (Deploy_position[0], Deploy_position[1]+3)
        elif specific_troop_positions[best_troop] == "Back":
            Deploy_position = (Deploy_position[0], Deploy_position[1]-6)
        for troop in opponent_troops:
            if troop["position"][1] < 25:
                if troop["name"] == "Wizard":
                    Deploy_position = troop["position"]
                    tmplist = ["Knight", "Skeletion", "Barbarian", "Valkyrie", "Dragon", "Wizard", "Prince", "Archer", "Minion", "Giant", "Musketeer", "Balloon"]
                    best_troop = None
                    for troop in tmplist:
                        if troop in deployable:
                            best_troop = troop
                    break
        deploy_list.list_.append((best_troop, Deploy_position))

    elif current_region == region[1]:
        center_positions = []
        for troop in opponent_troops:
            posy = troop["position"][1]
            pos = troop["position"][0]
            if posy > 25 and posy < 80:
                center_positions.append((pos-5 if pos-5 >= -25 else -25 , pos+5 if pos+5 <= 25 else 25))
        center_positions = combine(center_positions)
        ourcenter_positions = []
        for troop in our_troops:
            posy = troop["position"][1]
            pos = troop["position"][0]
            if posy > 0 and posy < 80:
                ourcenter_positions.append((pos-5 if pos-5 >= -25 else -25 , pos+5 if pos+5 <= 25 else 25))
        ourcenter_positions = combine(ourcenter_positions)
        fight_regions = indentifyfightregions(ourcenter_positions,center_positions)
        weakest_regions={}
        opponent_troops_in_weak_regions = []
        our_troops_in_weak_regions = []
        for region in fight_regions:
            opponent_troops_in_region = [troop for troop in opponent_troops if region[0] <= troop["position"][0] <= region[1] and troop["position"][1] <= 80]
            our_troops_in_region = [troop for troop in our_troops if region[0] <= troop["position"][0] <= region[1] and troop["position"][1] <= 80]
            opponent_score = calculate_initial_score(opponent_troops_in_region)
            our_score = calculate_initial_score(our_troops_in_region)
            opponent_score = calculate_score(opponent_troops_in_region, troops_data, our_troops_in_region, opponent_score,1)    
            our_score = calculate_score(our_troops_in_region, troops_data, opponent_troops_in_region, our_score,1)
            result = our_score - opponent_score
            if weakest_regions == {}:
                weakest_regions = {"result":result, "region":region}
                opponent_troops_in_weak_regions = opponent_troops_in_region
                our_troops_in_weak_regions = our_troops_in_region
            elif weakest_regions["result"] > result:
                weakest_regions = {"result":result, "region":region}
                opponent_troops_in_weak_regions = opponent_troops_in_region
                our_troops_in_weak_regions = our_troops_in_region
        #which troop to deploy
        troop_data={}
        for troop in troops:
            score = 0
            score=calculate_score([{"name" : troop}], troops_data, opponent_troops_in_weak_regions, score,1)
            troop_data[troop] = score
        sorted_troops = sorted(troop_data, key=troop_data.get, reverse=True)
        best_troop = None

        for troop in sorted_troops:
            if troop in deployable:
                best_troop = troop
                break
        #where to deploy
        Deploy_position=(0,80)
        if our_troops_in_weak_regions == []:
            for opponent_troop in opponent_troops_in_weak_regions:
                if opponent_troop["position"][1] < Deploy_position[1]:
                    if(opponent_troop["position"][1] > 50):
                        Deploy_position = (opponent_troop["position"][0],0)
                    else:
                        Deploy_position = opponent_troop["position"]                   
        else :
            for our_troop in our_troops_in_weak_regions:
                if our_troop["position"][1] < Deploy_position[1] : 
                    Deploy_position = our_troop["position"]
        if Deploy_position[1] > 50:
            Deploy_position = (Deploy_position[0],50)

        if specific_troop_positions[best_troop] == "Center":
            Deploy_position = (Deploy_position[0], Deploy_position[1])
        elif specific_troop_positions[best_troop] == "Front":
            Deploy_position = (Deploy_position[0], Deploy_position[1]+3)
        elif specific_troop_positions[best_troop] == "Back":
            Deploy_position = (Deploy_position[0], Deploy_position[1]-6)
        deploy_list.list_.append((best_troop, Deploy_position))
    else :
        troopinattackregion = [troop for troop in our_troops if troop["position"][1] > 50]
        scoree = calculate_initial_score(troopinattackregion)
        if scoree < 5:
            center_positions = []
            if opponent_troops == []:
                Deploy_position = (25,0)
                #which troop to deploy
                attacktroops = ["Balloon", "Giant", "Prince", "Wizard", "dragon" , "Minion","Knight","Valkyrie", "Skeleton", "barbarian", "Archer", "Musketeer"]
                best_troop = None
                for troop in attacktroops:
                    if troop in deployable:
                        best_troop = troop
                        break
                if best_troop == "Giant":
                    Deploy_position = (0, Deploy_position[1])
                deploy_list.list_.append((best_troop, Deploy_position))
            for troop in opponent_troops:
                posy = troop["position"][1]
                pos = troop["position"][0]
                if posy > 80:
                    center_positions.append((pos-5 if pos-5 >= -25 else -25 , pos+5 if pos-5 <= 25 else 25))
            center_positions = combine(center_positions)
            center_positions.sort()
            ourcenter_positions = []
            for troop in our_troops:
                pos = troop["position"][0]
                ourcenter_positions.append((pos-5 if pos-5 >= -25 else -25 , pos+5 if pos+5 <= 25 else 25))
            ourcenter_positions = combine(ourcenter_positions)
            fight_regions = indentifyfightregions(ourcenter_positions,center_positions)
            weakest_regions={}
            opponent_troops_in_weak_regions = []
            our_troops_in_weak_regions = []
            for region in fight_regions:
                opponent_troops_in_region = [troop for troop in opponent_troops if region[0] <= troop["position"][0] <= region[1] and troop["position"][1] > 80]
                our_troops_in_region = [troop for troop in our_troops if region[0] <= troop["position"][0] <= region[1] and troop["position"][1] > 0]
                opponent_score = calculate_initial_score(opponent_troops_in_region)
                our_score = calculate_initial_score(our_troops_in_region)
                opponent_score = calculate_score(opponent_troops_in_region, troops_data, our_troops_in_region, opponent_score,1)    
                our_score = calculate_score(our_troops_in_region, troops_data, opponent_troops_in_region, our_score,1)
                result = our_score - opponent_score
                if weakest_regions == {}:
                    weakest_regions = {"result":result, "region":region}
                    opponent_troops_in_weak_regions = opponent_troops_in_region
                    our_troops_in_weak_regions = our_troops_in_region
                elif weakest_regions["result"] > result:
                    weakest_regions = {"result":result, "region":region}
                    opponent_troops_in_weak_regions = opponent_troops_in_region
                    our_troops_in_weak_regions = our_troops_in_region
            #which troop to deploy
            troop_data={}
            for troop in troops:
                score = 0
                score=calculate_score([{"name" : troop}], troops_data, opponent_troops_in_weak_regions, score,1)
                troop_data[troop] = score
            sorted_troops = sorted(troop_data, key=troop_data.get, reverse=True)
            best_troop = None
            for troop in sorted_troops:
                if troop in deployable:
                    best_troop = troop
                    break
            #where to deploy
            Deploy_position=(0,80)
            if our_troops_in_weak_regions == []:
                for opponent_troop in opponent_troops_in_weak_regions:
                    if opponent_troop["position"][1] < Deploy_position[1]:
                        if(opponent_troop["position"][1] > 50):
                            Deploy_position = (opponent_troop["position"][0],0)
                        else:
                            Deploy_position = opponent_troop["position"]                   
            else :
                for our_troop in our_troops_in_weak_regions:
                    if our_troop["position"][1] < Deploy_position[1] : 
                        Deploy_position = our_troop["position"]
            
            deploy_list.list_.append((best_troop, Deploy_position))
        else :
            Deploy_position = (troopinattackregion[0]["position"][0],50)
            #which troop to deploy
            attacktroops = ["Balloon", "Prince", "Giant", "Wizard", "dragon" , "Minion","Knight","Valkyrie", "Skeleton", "barbarian", "Archer", "Musketeer"]
            best_troop = None
            for troop in attacktroops:
                if troop in deployable:
                    best_troop = troop
                    break
            if best_troop == "Giant":
                Deploy_position = (0, Deploy_position[1])
            deploy_list.list_.append((best_troop, Deploy_position))