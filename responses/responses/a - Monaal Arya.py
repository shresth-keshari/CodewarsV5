
import random
import math
from teams.helper_function import Troops, Utils

team_name = "Pratyaksh"
troops = [
    Troops.wizard, Troops.archer, Troops.valkyrie,Troops.giant,
    Troops.dragon, Troops.skeleton, Troops.knight, Troops.prince
]
deploy_list = Troops([])
team_signal = " "*101 + "  0"

def deploy(arena_data: dict):
    """
    DON'T TEMPER DEPLOY FUNCTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal


def check_counter_bool(arena_data:dict,troop_mapping:dict,counter_weight:dict, troop):
    my_weight_in_area = 0
    opp_weight_in_area = 0
    for troop2 in arena_data["OppTroops"]:
        dist = math.dist(troop.position,troop2.position)
        if dist<=5:
            troop_weight = (counter_weight[troop_mapping[troop.name]]["weight"])*troop.health/counter_weight[troop_mapping[troop.name]]["max_hp"]
            opp_weight_in_area+=troop_weight
            
    for troop2 in arena_data["MyTroops"]:
        dist = math.dist(troop.position,troop2.position)
        if dist<=5:
            troop_weight = (counter_weight[troop_mapping[troop.name]]["weight"])*troop.health/counter_weight[troop_mapping[troop.name]]["max_hp"]
            my_weight_in_area+=troop_weight
    
    if abs(opp_weight_in_area-my_weight_in_area)<=2:
        return False
    else:
        return True
        
def search_high_priority_troop(arena_data:dict,troop_mapping:dict,counter_weight:dict):
    opp_weight = 0
    high_priority_troop = None
    high_priority_troop_x = None
    high_priority_troop_y = None
    max_weight = 0
    high_priority_troop,high_priority_troop_x,high_priority_troop_y = find_high_priority_troop_tower_region(arena_data=arena_data,
                                                                                                             troop_mapping=troop_mapping,
                                                                                                             counter_weight=counter_weight)
    for troop in arena_data["OppTroops"]:
        if troop.position[1]<50:
            troop_weight = (counter_weight[troop_mapping[troop.name]]["weight"])*troop.health/counter_weight[troop_mapping[troop.name]]["max_hp"]
            opp_weight+=troop_weight
    
    if high_priority_troop is None and opp_weight<9:
        for troop in arena_data["OppTroops"]:
            if troop.name =="Wizard" and troop.target is not None and troop.position[1]<50 and check_counter_bool(troop=troop,
                                                                                                                  troop_mapping=troop_mapping,
                                                                                                                  arena_data=arena_data,
                                                                                                                  counter_weight=counter_weight):
                
                high_priority_troop = troop_mapping[troop.name]
                high_priority_troop_x,high_priority_troop_y = troop.position
    
    if high_priority_troop is None and opp_weight<=6:
        for troop in arena_data["OppTroops"]:
            if troop.position[1]<50:
                troop_weight = (counter_weight[troop_mapping[troop.name]]["weight"])*troop.health/counter_weight[troop_mapping[troop.name]]["max_hp"]
                if troop_weight>max_weight and check_counter_bool(troop=troop,
                                                                  arena_data = arena_data,
                                                                  counter_weight=counter_weight,
                                                                  troop_mapping=troop_mapping):
                    max_weight = troop_weight
                    high_priority_troop = troop_mapping[troop.name]
                    high_priority_troop_x,high_priority_troop_y= troop.position
    else:
        pass     
    
    return [opp_weight,high_priority_troop,high_priority_troop_x,high_priority_troop_y]

def calculate_tower_region_weight(arena_data:dict,troop_mapping:dict,counter_weight:dict):
    tower_position= arena_data["MyTower"].position
    weight = 0
    for troop in arena_data["OppTroops"]:
        dist = math.dist(troop.position,tower_position)
        if dist<=25:
            troop_weight = (counter_weight[troop_mapping[troop.name]]["weight"])*troop.health/counter_weight[troop_mapping[troop.name]]["max_hp"]
            weight+= troop_weight
    
    return weight

def find_counter_to_high_priority_troop(high_priority_troop,
                                        counter_weight:dict,
                                        deployable,
                                        elixir_map:dict):
    best_troop = None
    min_elixir = 10
    for troop in counter_weight[high_priority_troop]["counters"]:
        if (troop in deployable):
            if elixir_map[troop]<min_elixir:
                min_elixir = elixir_map[troop]
                best_troop = troop
    return best_troop

def check_for_giant(arena_data:dict):
    giantx = None
    gianty = None
    for troop in arena_data["MyTroops"]:
        if troop.name =="Giant" and -25<=troop.position[1]<=25 and troop.health>=3700:
            giantx = troop.position[0]
            gianty = troop.position[1]
            break
    return [giantx,gianty]
    
def find_attack_column(arena_data:dict):
    i = 0
    free_columns_x = None
    free_columns = [True,True,True,True,True]
    while i<=4:
        for troop in arena_data["OppTroops"]:
            if i*10-25<=troop.position[0]<i*10-15:
                free_columns[i] = False
        i+=1
    if all(free_columns):
        free_columns_x = 0
    else:
        for index, column_free in enumerate(free_columns):
            if column_free == False:
                free_columns_x = index*10 -20
                break
    return free_columns_x

def find_free_Columns(arena_data:dict):
    i = 0
    free_columns_x = None
    free_columns = [True,True,True,True,True]
    while i<=4:
        for troop in arena_data["OppTroops"]:
            if i*10-25<=troop.position[0]<i*10-15:
                free_columns[i] = False
        i+=1
    if all(free_columns):
        free_columns_x = 0
    else:
        for index, column_free in enumerate(free_columns):
            if column_free == True:
                free_columns_x = index*10 -20
                break
    return free_columns_x

def check_for_air_targetting_troop(arena_data:dict,troop_mapping:dict,counter_weight:dict):
    not_air_targetting_troop = True
    target_troop = None
    max_weight = 0
    not_air_targetting_troop = [
        Troops.knight,
        Troops.giant,
        Troops.prince,
        Troops.skeleton,
        Troops.barbarian ,
        Troops.valkyrie
    ]
    
    for troop in arena_data["OppTroops"]:
        if troop.position[1]<=50 and troop_mapping[troop.name] not in not_air_targetting_troop:
            not_air_targetting_troop = False
            break
        elif troop.position[1]<=50:
            troop_weight = (counter_weight[troop_mapping[troop.name]]["weight"])*troop.health/counter_weight[troop_mapping[troop.name]]["max_hp"]
            if troop_weight>=max_weight:
                max_weight=troop_weight
                target_troop = troop
    if not_air_targetting_troop:
        return target_troop
    else:
        return None
    
def check_troop_in_area(position,arena_data:dict):
    for troop in arena_data["MyTroops"]:
        dist = math.dist(position,troop.position)
        if dist<=2:
            return True
    return False

def find_best_troop_case2(arena_data:dict,
                          deployable,
                          opp_weight_half_court,
                          opp_weight_tower_region,
                          high_priority_troop,
                          counter_weight:dict,
                          elixir_map:dict,):
    
    giantx = None
    gianty = None
    best_troop = None
    
    giant_compatibility = [
        Troops.wizard,
        Troops.prince,
        Troops.dragon,
        Troops.archer
    ]
                
    [giantx,gianty] = check_for_giant(arena_data=arena_data)
    if opp_weight_half_court>=8 and arena_data["MyTower"].total_elixir<4 and opp_weight_tower_region==0:
        pass
        
    elif high_priority_troop:
        best_troop = find_counter_to_high_priority_troop(high_priority_troop=high_priority_troop,
                                                    deployable=deployable,
                                                    counter_weight=counter_weight,
                                                    elixir_map=elixir_map)
        
    elif giantx is not None:
        
        for troop in giant_compatibility:
            if troop in deployable:
                
                best_troop = troop
                break
                
    return [giantx,gianty,best_troop]

def detect_rush(arena_data:dict, troop_mapping:dict,counter_weight:dict):
    rush_detected = False
    current_weight = 0
    for troop in arena_data["OppTroops"]:
        current_weight += (counter_weight[troop_mapping[troop.name]]["weight"])*troop.health/counter_weight[troop_mapping[troop.name]]["max_hp"]
        for troop2 in arena_data["OppTroops"]:
            dist = math.dist(troop.position,troop2.position)
            if dist <=10:
                current_weight += (counter_weight[troop_mapping[troop.name]]["weight"])*troop.health/counter_weight[troop_mapping[troop.name]]['max_hp']
        if current_weight>=8:
            rush_detected = True
            break
    
    return rush_detected       
  
def deploy_high_elixir_troop(arena_data:dict,high_elixir_priority:list,deployable):
    best_troop = None
    troopx = None
    troopy = None
    if arena_data["MyTower"].total_elixir>=9:
        for troop in high_elixir_priority:
            if troop in deployable:
                best_troop = troop
                troopx = 0
                troopy = 0
                break
                
    return best_troop, troopx,troopy
                         
def defend_wizard(arena_data:dict, deployable):
    wizard_defenders_mid_range = {
        Troops.valkyrie:5,
        Troops.prince:1,
        Troops.dragon:1,
        Troops.knight:5,
    }
    
    wizard_defenders_low_range = {
        Troops.valkyrie:5,
        Troops.knight:5,
        Troops.prince:0,
    }
    
    wizard_x = None
    wizard_y= None
    
    defending_troop = None
    
    for troop in arena_data["MyTroops"]:
        if troop.name =="Wizard":
            if 30<troop.position[1]<=45:
                for troop2 in wizard_defenders_mid_range:
                    if troop2 in deployable:
                        defending_troop= troop2
                        wizard_x = troop.position[0]
                        wizard_y =troop.position[1]+ wizard_defenders_mid_range[troop2]
                                
                        break
            if troop.position[1]<=30:
                for troop2 in wizard_defenders_low_range:
                    if troop2 in deployable:
                        defending_troop = troop2
                        wizard_x = max(-25,min(25,troop.position[0]+random.choice([4,-4])))
                        wizard_y =troop.position[1]+ wizard_defenders_low_range[troop2]
                        break
                    
    return defending_troop, wizard_x,wizard_y

def find_high_priority_troop_tower_region(arena_data:dict,troop_mapping:dict,counter_weight:dict):
    max_weight = 0
    high_priority_troop = None
    high_priority_troop_x  = None
    high_priority_troop_y = None
    for troop in arena_data["OppTroops"]:
        dist  = math.dist(troop.position,(0,0))
        if dist<=30:
            weight =  (counter_weight[troop_mapping[troop.name]]["weight"])*troop.health/counter_weight[troop_mapping[troop.name]]["max_hp"]
            if weight>max_weight:
                high_priority_troop = troop_mapping[troop.name]
                high_priority_troop_x, high_priority_troop_y = troop.position
    return high_priority_troop, high_priority_troop_x,high_priority_troop_y

def calculater_elixir(elixir_exhausted:int,game_time:int):
    if game_time<120:
        return max(1,min(10+int(game_time/2)-elixir_exhausted,10))
    else:
        return max(1,min(70+ int((game_time-120)) - elixir_exhausted,10))
    
def check_for_rush(arena_data:dict,
                   opp_weight_half_court:int,
                   troop_mapping:dict,
                   counter_weight:dict,
                   enemy_elixir:int):
    opp_weight_on_opp_side = 0
    for troop in arena_data["OppTroops"]:
        if troop.position[1]>50:
            troop_weight = (counter_weight[troop_mapping[troop.name]]["weight"])*troop.health/counter_weight[troop_mapping[troop.name]]["max_hp"]
            opp_weight_on_opp_side +=troop_weight

    if opp_weight_on_opp_side<=4 and enemy_elixir<=3 and opp_weight_half_court<=4 and arena_data["MyTower"].total_elixir>=8:
        return True
    else: return False
    
def change_x_coord_to_disperse(x_coord:int,y_coord:int,arena_data:dict):
    i=0
    while check_troop_in_area(position=[x_coord,y_coord],arena_data=arena_data):
        if i>=10:
            break
        if x_coord<0:
            x_coord+=3
        else:
            x_coord-=3
        i+=1
    return x_coord
        

def logic(arena_data: dict):
    global team_signal
    my_tower = arena_data["MyTower"]
    
   
    
    # --- Score Our Troops (only from deployable troops) ---
    deployable = my_tower.deployable_troops
    # Define base scores and categories for our troops.
    troop_data = {
        Troops.wizard:     {"category": "ground", "name": "Wizard","speed":"medium"},
        Troops.archer:     {"category": "ground", "name": "Archer",   "speed":"medium"},
        Troops.musketeer:  {"category": "ground", "name": "Musketeer","speed":"medium"},
        Troops.giant:      {"category":"ground",  "name":"Giant",       "speed":"slow"},
        Troops.dragon:     {"category": "air",    "name": "Dragon",    "speed":"fast"},
        Troops.skeleton:   {"category": "ground", "name": "Skeleton", "speed":"fast"},
        Troops.knight:     {"category": "ground", "name": "Knight",   "speed":"medium"},
        Troops.prince:     {"category": "ground", "name": "Prince",   "speed":"fast"},
        Troops.valkyrie:   {"category": "ground", "name":"Valkyrie",  "speed":"medium"},
        Troops.minion:     {"category": "air",    "name":"Minions",   "speed":"fast"},
        Troops.balloon:    {"category": "air",    "name":"Balloon",   "speed":"medium"}
    }
    
    counter_weight = {
    Troops.wizard: {
        "max_hp":1100,
        "weight": 6,  
        "counters": [Troops.valkyrie,Troops.prince, Troops.knight,Troops.dragon]
    },
    Troops.balloon: {
        "max_hp":2226,
        "weight": 5,  
        "counters": [ Troops.wizard, Troops.minion,Troops.archer, Troops.dragon]
    },
    Troops.giant: {
        "max_hp":5423,
        "weight": 5,  
        "counters": [Troops.skeleton, Troops.wizard,Troops.minion,Troops.prince, Troops.valkyrie]
    },
    Troops.prince: {
        "max_hp":1920,
        "weight": 5,  
        "counters": [Troops.skeleton, Troops.knight, Troops.prince, Troops.minion, Troops.archer]
    },
    Troops.dragon: {
        "max_hp":1267,
        "weight": 4,  
        "counters": [ Troops.dragon, Troops.wizard,Troops.archer,Troops.minion,]
    },
    Troops.musketeer: {
        "max_hp":792,
        "weight": 3,  
        "counters": [Troops.prince, Troops.valkyrie, Troops.skeleton, Troops.knight, ],
    },
    Troops.knight: {
        "max_hp":1938,
        "weight": 3,  
        "counters": [Troops.knight, Troops.skeleton, Troops.archer,Troops.minion,Troops.dragon,]
    },
    
    Troops.valkyrie: {
        "max_hp":2097,
        "weight": 3,  
        "counters": [ Troops.prince, Troops.dragon,Troops.knight, Troops.minion,Troops.archer,]
    },
    
    Troops.minion: {
        "max_hp": 252,
        "weight": 2/3,  
        "counters": [Troops.archer, Troops.dragon, Troops.wizard,  Troops.minion, ]
    },
    Troops.barbarian: {
        "max_hp":736,
        "weight": 2/3,  
        "counters": []
    },
    
    Troops.archer: {
        "max_hp":334,
        "weight": 1,  
        "counters": [Troops.valkyrie,Troops.skeleton]
    },
  
    
    Troops.skeleton: {
        "max_hp":89,
        "weight": 0.1, 
        "counters": [Troops.archer, Troops.valkyrie,Troops.minion,Troops.wizard,Troops.skeleton]
        }
    }
    
    ranged_troop = [
        Troops.archer,
        Troops.musketeer,
        Troops.wizard,
        Troops.dragon,
    ]
    
    troop_mapping = {
        "Knight": Troops.knight,
        "Archer": Troops.archer,
        "Musketeer": Troops.musketeer,
        "Giant": Troops.giant,
        "Dragon": Troops.dragon,
        "Skeleton": Troops.skeleton,
        "Prince": Troops.prince,
        "Balloon": Troops.balloon,
        "Barbarian": Troops.barbarian,
        "Minion": Troops.minion,
        "Valkyrie": Troops.valkyrie,
        "Wizard": Troops.wizard,
    }
    
    elixir_map = {
        Troops.knight:3,
        Troops.archer:3,
        Troops.musketeer:4,
        Troops.giant:5,
        Troops.dragon:4,
        Troops.skeleton:3,
        Troops.prince:5,
        Troops.balloon:5,
        Troops.barbarian:3,
        Troops.minion:3,
        Troops.valkyrie:4,
        Troops.wizard:5
    }
    elixir_map_single = {
        Troops.knight:3,
        Troops.archer:1.5,
        Troops.musketeer:4,
        Troops.giant:5,
        Troops.dragon:4,
        Troops.skeleton:0.3,
        Troops.prince:5,
        Troops.balloon:5,
        Troops.barbarian:1,
        Troops.minion:3,
        Troops.valkyrie:4,
        Troops.wizard:5
    }

    my_weight = 0
    opp_weight_half_court = 0
    opp_weight_tower_region = 0
    
    high_elixir_priority = [
        Troops.wizard,
        Troops.knight,
        Troops.valkyrie,
        Troops.archer,
        Troops.dragon,
        Troops.giant
    ]
    
    air_attack_priority = [
        Troops.minion,
        Troops.dragon,
    ]
    
    shortcut_name_mapping = {
        "a":"Archer",
        "b":"Barbarian",
        "B":"Balloon",
        "d":"Dragon",
        "k":"Knight",
        "g":"Giant",
        "m":"Musketeer",
        "M":"minion",
        "p":"Prince",
        "s":"Skeleton",
        "v":"Valkyrie",
        "w":"Wizard"
    }
    
    name_shortcut_mapping  = {
        "Archer":"a",
        "Barbarian":"b",
        "Balloon":"B",
        "Dragon":"d",
        "Knight":"k",
        "Giant":"g",
        "Musketeer":"m",
        "Minion":"M",
        "Prince":"p",
        "Skeleton":"s",
        "Valkyrie":"v",
        "Wizard":"w"
    }
    
    
    troopx= None
    troopy = None
    
    best_troop = None
    high_priority_troop = None
    high_priority_troop_x = None
    high_priority_troop_y = None
    rush_mode = False
    
    giantx = None
    gianty = None 
    
    rushx = None
    rushy = None
    
    wizard_y = None
    wizard_x = None
    non_air_targetting_troop = None
    
    current_troops_opp = []
    for troop in arena_data["OppTroops"]:
        current_troops_opp.append(troop_mapping[troop.name])
    if team_signal[:101].strip() != "":
        prev_troops_opp = [troop_mapping[shortcut_name_mapping[troop]] for troop in team_signal[:101].strip().split(",")]
    else:
        prev_troops_opp = []
        
    elixir_exhausted = int(team_signal[101:])
    
    for troop in troop_data:
        prev_count= prev_troops_opp.count(troop)
        current_count = current_troops_opp.count(troop)
        if current_count>prev_count:
            elixir_exhausted += (current_count-prev_count)*elixir_map_single[troop]
    
    team_signal_start = ""
    for troop in current_troops_opp[:-1]:
        team_signal_start += name_shortcut_mapping[troop_data[troop]["name"]]
        team_signal_start +=","
    if current_troops_opp:
        team_signal_start += name_shortcut_mapping[troop_data[current_troops_opp[-1]]["name"]]
    team_signal_start += " "*(101-len(team_signal_start))
    team_signal = team_signal_start + " "*(3-len(str(elixir_exhausted)))+ str(round(elixir_exhausted))
    
    rush_combos = [
        [Troops.wizard,Troops.valkyrie],
        [Troops.wizard,Troops.skeleton],
        [Troops.dragon,Troops.prince],
        [Troops.knight,Troops.wizard],
    ]
    
    enemy_elixir = calculater_elixir(game_time=int(arena_data["MyTower"].game_timer/10),elixir_exhausted=elixir_exhausted)
        
    
    
    if Troops.wizard in deployable and (Troops.wizard not in [troop_mapping[troop.name] for troop in arena_data["OppTroops"] if troop.position[1]<50]):
        best_troop = Troops.wizard
    else:
        best_troop,wizard_x,wizard_y = defend_wizard(arena_data=arena_data,deployable=deployable)
        
    if best_troop is None:
        opp_weight_half_court,high_priority_troop,high_priority_troop_x,high_priority_troop_y = search_high_priority_troop(arena_data=arena_data,
                                                                                                                    troop_mapping=troop_mapping,
                                                                                                                    counter_weight=counter_weight,)
            
        opp_weight_tower_region = calculate_tower_region_weight(arena_data=arena_data,troop_mapping=troop_mapping,counter_weight=counter_weight)
            
        rush_mode = check_for_rush(arena_data=arena_data,
                                   opp_weight_half_court=opp_weight_half_court,
                                   troop_mapping=troop_mapping,
                                   counter_weight=counter_weight,
                                   enemy_elixir=enemy_elixir)    
        
        for troop in arena_data["MyTroops"]:
            if troop.position[1]>=0:
                my_weight += counter_weight[troop_mapping[troop.name]]["weight"]*troop.health/counter_weight[troop_mapping[troop.name]]["max_hp"]

        if rush_mode:
            for troop_combo in rush_combos:
                if all([troop in deployable for troop in troop_combo]):
                    best_troop = troop_combo
            
        else:
            non_air_targetting_troop = check_for_air_targetting_troop(arena_data=arena_data,counter_weight=counter_weight,troop_mapping=troop_mapping)
        
        
        if best_troop is None:
            giantx,gianty,best_troop = find_best_troop_case2(arena_data=arena_data,
                                                             deployable=deployable,
                                                             opp_weight_half_court=opp_weight_half_court,
                                                             opp_weight_tower_region=opp_weight_tower_region,
                                                             high_priority_troop=high_priority_troop,
                                                             counter_weight=counter_weight,
                                                             elixir_map=elixir_map)
            
        if best_troop is None:
            best_troop,troopx,troopy = deploy_high_elixir_troop(arena_data=arena_data,
                                                                high_elixir_priority=high_elixir_priority,
                                                                deployable=deployable)
        
            
        
        for troop in arena_data["OppTroops"]:
            if troop.position[1]<=-1 and troop.name =="Wizard":
                for counter_troop in counter_weight[Troops.wizard]["counters"]:
                    if counter_troop in deployable:
                        best_troop = counter_troop
                        high_priority_troop = troop_mapping[troop.name]
                        high_elixir_priority_x,high_elixir_priority_y= troop.position
                        high_elixir_priority_y = 100 + high_elixir_priority_y
                        high_elixir_priority_y /= 2
          


    if isinstance(best_troop, list):
        free_column_x = find_free_Columns(arena_data=arena_data)
        if free_column_x:
            for troop in best_troop:
                free_column_x = change_x_coord_to_disperse(x_coord=free_column_x,y_coord=30,arena_data=arena_data)
                deploy_list.list_.append((troop,(free_column_x,30)))
        else:
            pass
            
    elif wizard_x is not None:
        wizard_x = change_x_coord_to_disperse(x_coord=wizard_x,y_coord=wizard_y,arena_data=arena_data)
        deploy_list.list_.append((best_troop,(wizard_x,wizard_y)))
    
    elif rushx is not None:
        rushx = change_x_coord_to_disperse(x_coord=rushx,y_coord=rushy,arena_data=arena_data)
        deploy_list.list_.append((best_troop,(rushx,rushy)))
        
    elif troopx is not None:
        troopx = change_x_coord_to_disperse(x_coord=troopx,y_coord=troopy,arena_data=arena_data)
        deploy_list.list_.append((best_troop,(troopx,troopy)))
            
    elif best_troop is Troops.wizard and (giantx is None):
        deploy_list.list_.append((best_troop,(0,0)))
        
    elif non_air_targetting_troop is not None and best_troop in air_attack_priority:
        deploy_position = (non_air_targetting_troop.position[0],((non_air_targetting_troop.position[1]))-10)
            
        deploy_list.list_.append((best_troop,deploy_position))
        
    elif high_priority_troop:
        
        if best_troop == Troops.giant:
            deploy_list.list_.append((best_troop,(0,10)))
            
        elif giantx is not None:
            giantx = change_x_coord_to_disperse(x_coord=giantx,
                                                y_coord=gianty,
                                                arena_data=arena_data)
            deploy_list.list_.append((best_troop,(giantx,gianty)))
            
        elif(best_troop in ranged_troop):
            high_priority_troop_x = change_x_coord_to_disperse(
                x_coord=high_priority_troop_x,
                y_coord=high_priority_troop_y,
                arena_data=arena_data
            )
            deploy_list.list_.append((best_troop,(high_priority_troop_x,high_priority_troop_y-15)))
            
        else:
            high_priority_troop_x= change_x_coord_to_disperse(
                x_coord=high_priority_troop_x,
                y_coord=high_priority_troop_y,
                arena_data=arena_data
            )
            deploy_list.list_.append((best_troop,(high_priority_troop_x,high_priority_troop_y)))
            
    elif best_troop is not None:
        
        column = find_attack_column(arena_data=arena_data)
        if column:
            column = change_x_coord_to_disperse(x_coord=column,y_coord=0,arena_data=arena_data)
            deploy_position = (column,0)
            deploy_list.list_.append((best_troop,deploy_position))
        else:
            pass
    else:
        pass
    
