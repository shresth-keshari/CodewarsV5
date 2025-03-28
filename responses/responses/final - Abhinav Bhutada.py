# from teams.helper_function import Troops, Utils

# team_name = "DELHI"
# troops = [Troops.dragon,Troops.skeleton,Troops.wizard,Troops.minion,Troops.archer,Troops.giant,Troops.balloon,Troops.barbarian]
# deploy_list = Troops([])
# team_signal = ""

# def deploy(arena_data:dict):
#     """
#     DON'T TEMPER DEPLOY FUCNTION
#     """
#     deploy_list.list_ = []
#     logic(arena_data)
#     return deploy_list.list_, team_signal

# def logic(arena_data:dict):
#     global team_signal
#     deploy_list.deploy_dragon((-16,0))

from teams.helper_function import Troops, Utils
import random, math


team_name = "Warriors of Code"
troops = [Troops.wizard,Troops.knight,Troops.prince,Troops.giant,Troops.dragon,Troops.skeleton,Troops.minion,Troops.valkyrie]
deploy_list = Troops([])
team_signal = "{\"E\":10,\"deck\":[],\"bool\":0}"



def deploy(arena_data:dict):
    """
    DON'T TEMPER DEPLOY FUCNTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def calculate_distance(pos1:tuple,pos2:tuple):
    return ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)**0.5

def sgn(x):
    if x>0:
        return 1
    if x<0:
        return -1
    return 0

def in_deploy_area(position,area):
    if (position[0]-area[0])*(position[0]-area[1])<=0 and (position[1]-area[2])*(position[1]-area[3])<=0:
        return True

def convert_player2(position,display_size):  # convert player2 perspective to player1 (game engine) perspective
    x = display_size[0] - position[0]
    y = display_size[1] - position[1]
    return (x,y)  

def nearest_r_opp_troop(arena_data):
    x, y, Z, r, H = 0, 100, "", 125, 1
    for i in arena_data["OppTroops"]:
        x_, y_ = i.position
        if calculate_distance((x_, y_), (0, 0)) < r:
            x, y = i.position
            Z, H = i.name, i.health
            r = calculate_distance((x, y), (0, 0))
    return x, y, Z, r, H

def second_nearest_r_opp_troop(arena_data):
    x, y, Z, r, H = 0, 100, "", 125, 1
    for i in arena_data["OppTroops"]:
        x_, y_ = i.position
        if calculate_distance((x_, y_), (0, 0)) < r and i.name != nearest_r_opp_troop(arena_data)[2]:
            x, y = i.position
            Z, H = i.name, i.health
            r = calculate_distance((x, y), (0, 0))
    return x, y, Z, r, H

def third_nearest_r_opp_troop(arena_data):
    x, y, Z, r, H = 0, 100, "", 125, 1
    for i in arena_data["OppTroops"]:
        x_, y_ = i.position
        if calculate_distance((x_, y_), (0, 0)) < r and i.name != nearest_r_opp_troop(arena_data)[2] and i.name != second_nearest_r_opp_troop(arena_data)[2]:
            x, y = i.position
            Z, H = i.name, i.health
            r = calculate_distance((x, y), (0, 0))
    return x, y, Z, r, H

def nearest_y_opp_troop(arena_data):
    x, y, Z, r, H = 0, 100, "", 125, 1
    for i in arena_data["OppTroops"]:
        x_, y_ = i.position
        if y_ < y:
            Z, H = i.name, i.health
            r = calculate_distance((x_, y_), (0, 0))
            x, y = x_, y_
    return x, y, Z, r, H


def second_nearest_y_opp_troop(arena_data):
    x, y, Z, r, H = 0, 100, "", 125, 1
    for i in arena_data["OppTroops"]:
        x_, y_ = i.position
        if y_ < y and i.name != nearest_y_opp_troop(arena_data)[2]:
            Z, H = i.name, i.health
            r = calculate_distance((x_, y_), (0, 0))
    return x, y, Z, r, H

def third_nearest_y_opp_troop(arena_data):
    x, y, Z, r, H = 0, 100, "", 125, 1
    for i in arena_data["OppTroops"]:
        x_, y_ = i.position
        if y_ < y and i.name != nearest_y_opp_troop(arena_data)[2] and i.name!=second_nearest_y_opp_troop(arena_data)[2]:
            Z, H = i.name, i.health
            r = calculate_distance((x_, y_), (0, 0))
    return x, y, Z, r, H


def farthest_my_troop(arena_data):
    x, y, Z, r, H = 0, 0, "", 0, 1
    for i in arena_data["MyTroops"]:
        x_, y_ = i.position
        if y_ > y:
            Z, H = i.name, i.health
            r = calculate_distance((x_, y_), (0, 0))
            x, y = x_, y_
    return x, y, Z, r, H


def second_farthest_my_troop(arena_data):
    x, y, Z, r, H = 0, 0, "", 0, 1
    for i in arena_data["MyTroops"]:
        x_, y_ = i.position
        if y_ > y and i.name != farthest_my_troop(arena_data)[2]:
            Z, H = i.name, i.health
            r = calculate_distance((x_, y_), (0, 0))
            x, y = x_, y_
    return x, y, Z, r, H


def third_farthest_my_troop(arena_data):
    x, y, Z, r, H = 0, 0, "", 0, 1
    for i in arena_data["MyTroops"]:
        x_, y_ = i.position
        if y_ > y and i.name != farthest_my_troop(arena_data)[2] and i.name != second_farthest_my_troop(arena_data)[2]:
            Z, H = i.name, i.health
            r = calculate_distance((x_, y_), (0, 0))
            x, y = x_, y_
    return x, y, Z, r, H


def dick(name):
    dicky = {
        "Archer": {"Elixir": 3, "Max Health": 334, "Discovery Range": 15, "Attack Range": 9.375, "Size": 1.40625},
        "Minion": {"Elixir": 5, "Max Health": 252, "Discovery Range": 7.5, "Attack Range": 3.75, "Size": 1.40625},
        "Knight": {"Elixir": 3, "Max Health": 1938, "Discovery Range": 13.125, "Attack Range": 0, "Size": 2.8125},
        "Skeleton": {"Elixir": 3, "Max Health": 89, "Discovery Range": 7.5, "Attack Range": 0, "Size": 1.40625},
        "Dragon": {"Elixir": 4, "Max Health": 1267, "Discovery Range": 9.375, "Attack Range": 6.5625, "Size": 3.75},
        "Valkyrie": {"Elixir": 4, "Max Health": 2097, "Discovery Range": 13.125, "Attack Range": 0, "Size": 1.875},
        "Musketeer": {"Elixir": 4, "Max Health": 792, "Discovery Range": 15, "Attack Range": 11.25, "Size": 1.875},
        "Giant": {"Elixir": 5, "Max Health": 5423, "Discovery Range": 13.125, "Attack Range": 0, "Size": 4.6875},
        "Prince": {"Elixir": 5, "Max Health": 1920, "Discovery Range": 9.375, "Attack Range": 0, "Size": 2.8125},
        "Barbarian": {"Elixir": 3, "Max Health": 736, "Discovery Range": 9.375, "Attack Range": 0, "Size": 2.34375},
        "Balloon": {"Elixir": 5, "Max Health": 2226, "Discovery Range": 9.375, "Attack Range": 0, "Size": 3.75},
        "Wizard": {"Elixir": 5, "Max Health": 1100, "Discovery Range": 15, "Attack Range": 10.3125,
                   "Size": 2.34375},
        "Princess": {"Elixir": 3, "Max Health": 287, "Discovery Range": 18.75, "Attack Range": 16.875,
                     "Size": 1.40625},
        "": {"Elixir": 0, "Max Health": 0, "Discovery Range": 0, "Attack Range": 0, "Size": 0}
    }
    return dicky.get(name, {"Elixir": 0, "Max Health": 0, "Discovery Range": 0, "Attack Range": 0, "Size": 0})

def opp_elixir(arena_data):
    global team_signal
    current_elixir = int(team_signal[:2]) + float(team_signal[2:4]) / 100

    game_timer = arena_data["MyTower"].game_timer

    if game_timer < 1200:  # First 2 minutes (120s * 10fps)
        elixir_rate = 0.05
    else:  # Last 1 minute (60s * 10fps)
        elixir_rate = 0.1

    # Calculate elixir gained
    if current_elixir < 10:
        current_elixir += elixir_rate
    latest_uid = int(team_signal[4:7])
    max_uid = 0
    elixir_deployed = 0
    unique_troops = set([])
    for troop in arena_data["OppTroops"]:
        if troop.uid > latest_uid:
            if troop.name not in unique_troops:
                unique_troops.add(troop.name)
                elixir_deployed += troop.elixir
        max_uid = max(max_uid, troop.uid)

    current_elixir -= elixir_deployed

    int_part = int(current_elixir)
    float_part = int((current_elixir - int_part) * 100)
    team_signal = f"{int_part:02d}" + f"{float_part:02d}" + team_signal[4:]
    team_signal = team_signal[:4] + f"{max_uid:03d}" + team_signal[7:]

    return current_elixir + 0.3


def deploy_troop(tup):
    name, position = tup
    if troop_is_deployable(name):
        deploy_list.list_.append((name, position))
        eval(team_signal)['E'] -= dick(name)["Elixir"]
        eval(team_signal)["deck"].remove(name)


def counter_map(name):
    counter = {
        "Giant": ["Skeleton", "Knight", "Wizard", "Prince", "Minion"],
        "Skeleton": ["Valkyrie", "Dragon", "Skeleton"],
        "Dragon": ["Dragon", "Wizard", "Minion"],
        "Minion": ["Wizard", "Dragon", "Minion"],
        "Wizard": ["Skeleton", "Knight", "Valkyrie", "Wizard"],
        "Valkyrie": ["Knight", "Valkyrie", "Barbarian"],
        "Knight": ["Skeleton", "Minion"],
        "Prince": ["Skeleton", "Prince"],
        "Balloon": ["Wizard", "Dragon", "Minion"],
        "Musketeer": ["Skeleton", "Knight", "Minion"],
        "Barbarian": ["Skeleton", "Wizard", "Dragon"],
        "Archer": ["Skeleton", "Knight"]
    }
    return counter[name]

def counter_map_2(name):  # keep maximum no of elements in the list # done
    counter = {
        "Giant": ["Skeleton", "Prince", "Wizard", "Minion", "Knight", "Valkyrie", "Dragon"],  # done
        "Skeleton": ["Valkyrie", "Wizard", "Skeleton", "Dragon", "Minion", "Prince", "Knight"],  # done
        "Dragon": ["Wizard", "Dragon", "Minion"],  # done
        "Minion": ["Wizard", "Dragon", "Minion"],  # done
        "Wizard": ["Valyirie", "Wizard", "Prince", "Knight", "Dragon", "Skeleton", "Minion"],  # done
        "Valkyrie": ["Knight", "Valkyrie", "Wizard", "Prince", "Skeleton", "Minion", "Dragon"],  # done
        "Knight": ["Skeleton", "Barbarian", "Knight", "Wizard", "Prince", "Dragon", "Minion"],
        "Prince": ["Skeleton", "Wizard", "Prince", "Knight", "Minion", "Valkyrie", "Dragon"],
        "Balloon": ["Wizard", "Minion", "Dragon"],
        "Musketeer": ["Skeleton", "Knight", "Wizard", "Dragon"],
        "Barbarian": ["Skeleton", "Valkyrie", "Wizard", "Dragon", "Knight"],
        "Archer": ["Skeleton", "Wizard", "Valkyrie", "Dragon", "Knight"]
    }
    return counter[name]


def my_troop_health(arena_data, name):
    for i in arena_data["MyTroops"]:
        if i.name == name:
            return i.health


def pref(L, arena_data):
    i = 0
    for i in range(len(L)):
        if L[i] in eval(team_signal)["deck"] and dick(L[i])["Elixir"] <= eval(team_signal)["E"]:
            return L[i]
    return ""

def my_troop_position(arena_data, name):
    for i in arena_data["MyTroops"]:
        if i.name == name:
            return i.position
    return (0, 0)

def troops_in_number(arena_data, name=""):
    if name != "":
        count = 0
        for i in arena_data["MyTroops"]:
            if i.name == name:
                count += 1
        return count
    else:
        L = []
        for i in arena_data["MyTroops"]:
            if i.name not in L:
                L.append(i.name)
        return len(L)


def good_health(name, arena_data):
    for i in arena_data["MyTroops"]:
        if i.name == "Minion":
            return troops_in_number(arena_data, "Minion") == 3
        elif i.name == "Skeleton":
            return troops_in_number(arena_data, "Skeleton") >= 6
        elif i.name == "Archer":
            return troops_in_number(arena_data, "Archer") == 3
        elif i.name == "Barbarian":
            return troops_in_number(arena_data, "Barbarian") >= 2
        elif i.name == name:
            return my_troop_health(arena_data, name) >= 500 or my_troop_health(arena_data, name) >= dick(name)["Max Health"]


def number_air_defense(arena_data):
    air_attacking_troops = {"Minion", "Wizard", "Dragon"}
    count = 0
    for i in arena_data["MyTower"].deployable_troops:
        if i in air_attacking_troops:
            count += 1
    return count


def troop_is_deployable(name):
    return name in eval(team_signal)["deck"] and dick(name)["Elixir"] <= eval(team_signal)["E"]


def calculate_distance(pos1: tuple, pos2: tuple):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

def nearest_entity_for_opp_with_status(arena_data, opptroop):
    name = opptroop.name
    pos = opptroop.position
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    tower_pos = my_tower.position
    my_entities = [('Tower', tower_pos)]
    for i in arena_data["MyTroops"]:
        my_entities.append((i.name, i.position))

    def compare_tup(t_a, t_b):
        if calculate_distance(t_a[1], pos) < calculate_distance(t_b[1], pos):
            return -1
        else:
            return 1

    nearest_entity = sorted(my_entities, key=cmp_to_key(compare_tup))[0]

    def is_in_range(entity, range_):
        """Checks if an entity is within the troop's discovery or attack range."""
        return calculate_distance(entity[1], pos) <= range_ + dick(name)['Size'] + dick(entity[0])['Size']

    if is_in_range(nearest_entity, dick(name)["Attack Range"]):
        return nearest_entity, "Attack"
    if is_in_range(nearest_entity, dick(name)["Discovery Range"]):
        return nearest_entity, "Discovery"


def opp_has_balloon(arena_data):
    for i in arena_data["OppTroops"]:#deck niklane pe change rule
        if i.name=="Balloon":
            return True
    return False

def opp_troop_already_set_target_on_my_troop(arena_data, name):
    for i in arena_data["OppTroops"]:
        if name==i.name:   #doubt
            return i.target!=None and i.target.name!=arena_data["MyTower"].name
    return False

def opp_troop_already_set_target_on_my_tower(arena_data, name):
    for i in arena_data["OppTroops"]:
        if name==i.name:
            if i.target!=None:
                if i.target.name==arena_data["MyTower"].name:
                    return True
    return False

def my_troop_already_set_target_on_opp_troop(arena_data, Z):
    for i in arena_data["MyTroops"]:
        if i.target!=None:
            if i.target.name==Z:
                return True
    return False

def multi_attack_at_position(arena_data, position):
    count = 0
    for i in arena_data["OppTroops"]:
        if i.name=="Balloon" or i.name=="Giant":
            continue
        if calculate_distance(i.position, position) < dick(i.name)["Discovery Range"]+dick(i.name)["Size"]+2:
            count += 1
    return count













def logic(arena_data:dict):
    global team_signal
    troops_data = Troops.troops_data
    my_tower = arena_data["MyTower"]
    game_timer = my_tower.game_timer
    opp_troops = arena_data["OppTroops"]
    E = arena_data["MyTower"].total_elixir
    deck = str(arena_data["MyTower"].deployable_troops)
    B = eval(team_signal)["bool"]
    team_signal = "{\"E\":" + str(E) + ",\"deck\":" + deck + ",\"bool\":" + str(0) + "}"
    air_troops = {'Minion', 'Dragon', 'Balloon'}
    air_attacking = {'Minion', 'Dragon', 'Wizard', 'Archer'}
    deployable = my_tower.deployable_troops

    x1, y1, z1, r1, h1 = nearest_r_opp_troop(arena_data)
    x2, y2, z2, r2, h2 = second_nearest_r_opp_troop(arena_data)
    x3, y3, z3, r3, h3 = third_nearest_r_opp_troop(arena_data)

    X1, Y1, Z1, R1, H1 = nearest_y_opp_troop(arena_data)
    X2, Y2, Z2, R2, H2 = second_nearest_y_opp_troop(arena_data)
    X3, Y3, Z3, R3, H3 = third_nearest_y_opp_troop(arena_data)

    a1, b1, c1, d1, e1 = farthest_my_troop(arena_data)
    a2, b2, c2, d2, e2 = second_farthest_my_troop(arena_data)
    a3, b3, c3, d3, e3 = third_farthest_my_troop(arena_data)

    is_opp_in = Y1 < 50
    is_opp_in_ = Y2 < 70 or Y1 < 70

    a = multi_attack_at_position(arena_data, (x1, y1)) > 2
    b = "Giant" in deck
    c = b or not a

    S1 = 9.375*dick(Z1)["Size"]
    S2 = 9.375*dick(Z2)["Size"]
    S3 = 9.375*dick(Z3)["Size"]
    TS = 9.375
    DR1 = 9.375*dick(Z1)["Discovery Range"]
    DR2 = 9.375*dick(Z2)["Discovery Range"]
    DR3 = 9.375*dick(Z3)["Discovery Range"]
    M1 = DR1+S1
    M2 = DR2+S2
    M3 = DR3+S3
    AR1 = dick(Z1)["Attack Range"]
    AR2 = dick(Z2)["Attack Range"]
    AR3 = dick(Z3)["Attack Range"]

    x_giant = my_troop_position(arena_data, "Giant")[0]
    y_giant = my_troop_position(arena_data, "Giant")[1]
    health_giant = my_troop_health(arena_data, "Giant")
    x_wizard = my_troop_position(arena_data, "Wizard")[0]
    y_wizard = my_troop_position(arena_data, "Wizard")[1]
    health_wizard = my_troop_health(arena_data, "Wizard")
    x_balloon = my_troop_position(arena_data, "Balloon")[0]
    y_balloon = my_troop_position(arena_data, "Balloon")[1]

    for i in arena_data["OppTroops"]:
        if i.target == arena_data["MyTower"].name:
            deploy_troop((pref(counter_map(i.name), arena_data), i.position)) if pref(counter_map(i.name),arena_data) != "" else deploy_troop((pref(counter_map_2(i.name), arena_data), i.position))
            deploy_troop((pref(counter_map(i.name), arena_data), i.position)) if pref(counter_map(i.name),arena_data) != "" else deploy_troop((pref(counter_map_2(i.name), arena_data), i.position))

    if TS+S1+DR1<r1<35 and TS+S2+DR2<r2<40 and r3<50 and opp_has_balloon(arena_data)==False:
        if opp_troop_already_set_target_on_my_troop(arena_data, Z1)==False:
            if opp_troop_already_set_target_on_my_troop(arena_data, Z2)==False:
                if opp_troop_already_set_target_on_my_troop(arena_data, Z3)==False:
                    deploy_troop(("Gaint", (0, 7)))
    
    if r1 < 26 + dick(z1)["Size"]:
        if pref(counter_map(z1), arena_data) != "":
            deploy_troop((pref(counter_map(z1), arena_data), (x1, y1)))
            deploy_troop((pref(counter_map(z1), arena_data), (x1, y1)))
            B=1
        else:
            if z1 != "Giant" and z1 != "Balloon":
                d = dick(z1)["Discovery Range"] + dick(z1)["Size"]
                theta = math.atan(x1 / y1)
                r = calculate_distance((x1, y1), (0, 0))
                alpha = 2 * sgn(x1) * math.asin(d / (2 * r))
                P = (r * math.sin(alpha + theta), r * math.cos(alpha + theta)-5)
                L = counter_map_2(z1)
                M = pref(L, arena_data)
                if (z1 in air_attacking or M not in air_troops) or (z1=="Wizard" and M=="Skeleton"):
                    deploy_troop((M, P))
                else:
                    L.remove(M)
                    M = pref(L, arena_data)
                    deploy_troop((M, P))
            elif z1 == "Giant":
                deploy_troop((pref(counter_map("Giant"), arena_data), (x1, y1)))
                deploy_troop((pref(counter_map("Giant"), arena_data), (x1, y1)))
                B=1
            elif z1 == "Balloon":
                deploy_troop((pref(counter_map("Balloon"), arena_data), (2 * x1 / 3, 2 * y1 / 3)))
                deploy_troop((pref(counter_map("Balloon"), arena_data), (2 * x1 / 3, 2 * y1 / 3)))
                B=1
                
    if r1 < 45 and B == 0:
        if r2 > 60 and pref(counter_map(z1), arena_data) != "":
            deploy_troop((pref(counter_map(z1), arena_data), (x1, y1)))
            eval(team_signal)["bool"] = 1
        else:
            deploy_troop((pref(counter_map_2(z1), arena_data), (x1, y1 - 20)))
            deploy_troop((pref(counter_map_2(z1), arena_data), (x1, y1 - 20)))
            eval(team_signal)["bool"] = 1




    if (Y1>70 or Y1==0) and eval(team_signal)["E"]>5 and game_timer>50:
        if troop_is_deployable("Giant") and y_giant<30 and Z1!="Skeleton" and Z2!="Skeleton" and H3==1 and (Y1>70 or Y1==0):
            if troop_is_deployable("Wizard") or troop_is_deployable("Prince"):
                deploy_troop(("Giant", (12*sgn(-x1), 50))) if x1!=0 else deploy_troop(("Giant", (12*sgn(-x2), 50))) if x2!=0 else deploy_troop(("Giant", (12, 50)))
        if y_giant > 55 and health_giant > 2500:
            if troop_is_deployable("Prince") and y_giant>65:
                deploy_troop(("Prince", (25*sgn(-x_giant), 50))) if x_giant!=0 else deploy_troop(("Prince", (25*sgn(-x1), 50))) if x1!=0 else deploy_troop("Prince", (25*sgn(-x2), 50))
            if troop_is_deployable("Wizard"):
                deploy_troop(("Wizard", (x_giant, 50))) #needed more options

    if Y1!=0 and eval(team_signal)["E"]==10 and len(arena_data["MyTroops"])==0 and (Y2==0 or Y2-Y1>20) and H3==1:
        if troop_is_deployable(Z1) and Z1!="Giant":
            deploy_troop((Z1, (X1, 100-Y1)))
        else:
            deploy_troop((counter_map_2(Z1, arena_data), (X1, 100-Y1)))
    if eval(team_signal)["E"]>8 and Y1>50 and Y1<80 and len(arena_data["MyTroops"])==0 and (Y2==0 or Y2-Y1>10) and H3==1:
        if troop_is_deployable(Z1):
            deploy_troop((Z1, (X1, 100-Y1)))
        else:
            deploy_troop((pref(counter_map_2(Z1), arena_data), (X1, 100-Y1)))
    if eval(team_signal)["E"]>5 and Y1>30 and Y1<50 and Y2<50 and len(arena_data["MyTroops"])<=1:   #gotta update this:
        if troop_is_deployable(Z2):
            deploy_troop((Z2, (x2, Y2)))
        else:
            deploy_troop((counter_map(Z2, arena_data), (x2, Y2)))
    
    if (y_giant>70 and health_giant>2000) or (70>y_giant>40 and health_giant>1200) or (40>y_giant>22 and health_giant>300):
        if opp_troop_already_set_target_on_my_troop(arena_data, Z1) and len(arena_data["MyTroops"])==1:
            deploy_troop((pref(counter_map_2(Z1), arena_data), (X1, min(50, y_giant-3))))
        if opp_troop_already_set_target_on_my_troop(arena_data, Z2) and len(arena_data["MyTroops"])<=2:
            deploy_troop((pref(counter_map_2(Z1), arena_data), (X1, min(50, y_giant-3))))
        if opp_troop_already_set_target_on_my_troop(arena_data, Z3) and len(arena_data["MyTroops"])<=3:
            deploy_troop((pref(counter_map_2(Z1), arena_data), (X1, min(50, y_giant-3))))

    
    if troop_is_deployable("Giant") and len(arena_data["MyTroops"])==0 and len(arena_data["OppTroops"])==0:
        deploy_troop(("Giant", (0, 40)))

    if len(deploy_list.list_) == 0:
        if is_opp_in and z1 not in air_troops and "Skeleton" not in eval(team_signal)["deck"]:
            for i in eval(team_signal)["deck"]:
                if dick(i)["Elixir"] == 3:
                    deploy_troop((i, (x1 - sgn(x1) * dick(z1)["Discovery Range"], 0)))
            if len(deploy_list.list_) == 0:
                for i in eval(team_signal)["deck"]:
                    if dick(i)["Elixir"] == 4:
                        deploy_troop((i, (x1 - sgn(x1) * dick(z1)["Discovery Range"], 0)))
        elif (z1 == "Minion" or z2 == "Minion") and is_opp_in_ and number_air_defense(arena_data) == 0:
            for i in eval(team_signal)["deck"]:
                if dick(i)["Elixir"] == 3:
                    deploy_troop((i, (5, 0)))
            if number_air_defense(arena_data) == 0:
                for i in eval(team_signal)["deck"]:
                    if dick(i)["Elixir"] == 3:
                        deploy_troop((i, (5, 0)))
                        
        elif (z1 == "Dragon" or z2 == "Dragon") and is_opp_in_ and number_air_defense(arena_data) == 0:
            for i in eval(team_signal)["deck"]:
                if dick(i)["Elixir"] == 3:
                    deploy_troop((i, (5, 0)))
            if number_air_defense(arena_data) == 0:
                for i in eval(team_signal)["deck"]:
                    if dick(i)["Elixir"] == 3:
                        deploy_troop((i, (5, 0)))
            
        elif (z1 == "Balloon" or z2 == "Balloon") and number_air_defense(arena_data) < 2:
            deploy_troop((deployable[0], (x1, 15))) if deployable[0] not in air_attacking else deploy_troop(
                (deployable[1], (x1, 15)))
            
        elif 100 > y1 > 70:
            if troops_in_number(arena_data) >= 2 and H2 == 1 and b1 > 70 and b2 > 70 and good_health(c1,
                                                                                                     arena_data) and good_health(
                    c2, arena_data):
                deploy_troop((pref(counter_map_2(z1), arena_data), (x1, 50)))
            elif troops_in_number(arena_data) == 0:
                deploy_troop((pref(counter_map_2(z1), arena_data), (x1, 90 - y1)))
            elif troops_in_number(arena_data) == 1:
                deploy_troop((pref(counter_map_2(z1), arena_data), (x1, 50))) if b1 > 50 else deploy_troop(
                    (pref(counter_map_2(z1), arena_data), (x1, b1)))
                
        elif len(opp_troops) == 0 and eval(team_signal)['E'] >= 7 and Y1 > 70 and game_timer > 10:
            if b2<40:
                x = (random.randint(0, 1) - 0.5) * 30
                deploy_troop((deployable[0], (x, 15))) if deployable[0] != "Skeleton" else deploy_troop(
                    (deployable[1], (x, 15)))
            else:
                x = (random.randint(0, 1) - 0.5) * 30
                deploy_troop(("Skeleton", (x, 15))) if (z1!="Wizard" or h1>400) and z1!="Valkyrie" else deploy_troop((pref(counter_map_2(z1), arena_data), (x, 50)))

    
    