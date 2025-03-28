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
import random


team_name = "TryHards"
troops = [Troops.wizard,Troops.knight,Troops.prince,Troops.giant,Troops.dragon,Troops.skeleton,Troops.minion,Troops.archer]
deploy_list = Troops([])
team_signal = "{\"E\":10,\"deck\":[]}"

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

def attri(name):
    dick = {
        "Archer": {"Elixir": 3, "Max Health": 334, "Discovery Range": 8, "Attack Range": 5, "Size": 0.15},
        "Minion": {"Elixir": 5, "Max Health": 252, "Discovery Range": 4, "Attack Range": 2, "Size": 0.15},
        "Knight": {"Elixir": 3, "Max Health": 1938, "Discovery Range": 7, "Attack Range": 0, "Size": 0.3},
        "Skeleton": {"Elixir": 3, "Max Health": 89, "Discovery Range": 4, "Attack Range": 0, "Size": 0.15},
        "Dragon": {"Elixir": 4, "Max Health": 1267, "Discovery Range": 5, "Attack Range": 3.5, "Size": 0.4},
        "Valkyrie": {"Elixir": 4, "Max Health": 2097, "Discovery Range": 7, "Attack Range": 0, "Size": 0.2},
        "Musketeer": {"Elixir": 4, "Max Health": 792, "Discovery Range": 8, "Attack Range": 6, "Size": 0.2},
        "Giant": {"Elixir": 5, "Max Health": 5423, "Discovery Range": 7, "Attack Range": 0, "Size": 0.5},
        "Prince": {"Elixir": 5, "Max Health": 1920, "Discovery Range": 5, "Attack Range": 0, "Size": 0.3},
        "Barbarian": {"Elixir": 3, "Max Health": 736, "Discovery Range": 5, "Attack Range": 0, "Size": 0.25},
        "Balloon": {"Elixir": 5, "Max Health": 2226, "Discovery Range": 5, "Attack Range": 0, "Size": 0.4},
        "Wizard": {"Elixir": 5, "Max Health": 1100, "Discovery Range": 8, "Attack Range": 5.5, "Size": 0.25},
        "Princess": {"Elixir": 3, "Max Health": 287, "Discovery Range": 10, "Attack Range": 9, "Size": 0.15},
        "": {"Elixir": 0, "Max Health": 0, "Discovery Range": 0, "Attack Range": 0, "Size": 0}
    }

    return dick.get(name,{"Elixir": 0, "Max Health": 0, "Discovery Range": 0, "Attack Range": 0, "Size": 0})

def troop_is_deployable(name):
    print(eval(team_signal)["deck"])
    return name in eval(team_signal)["deck"] and attri(name)["Elixir"] <= eval(team_signal)["E"]

def nearest_troop_data(arena_data):
    Z = ""
    P = (0, 0)
    H = 1
    w = 100
    H_ = 1
    for i in arena_data["OppTroops"]:
        x,y=i.position
        if calculate_distance((x,y),(0,0)) < w:
            w = calculate_distance((x,y),(0,0))
            Z = i.name
            P = (x, y)
            H = i.health
            H_ = attri(i.name)["Max Health"]
    data = [w, Z, P, H, H_]
    return data

def second_nearest_troop_data(arena_data):
    Z = ""
    P = (0, 0)
    H = 1
    w = 100
    H_ = 1
    for i in arena_data["OppTroops"]:
        NTD = nearest_troop_data(arena_data)
        if i.name==NTD[1]:
            continue
        else:
            x,y=i.position
            if calculate_distance((x,y),(0,0)) < w:
                w = calculate_distance((x,y),(0,0))
                Z = i.name
                P = (x, y)
                H= i.health
                H_= attri(i.name)["Max Health"]
    data = [w, Z, P, H, H_]
    return data

def third_nearest_troop_data(arena_data):
    Z = ""
    P = (0, 0)
    H = 1
    w = 100
    H_ = 1
    for i in arena_data["OppTroops"]:
        NTD = nearest_troop_data(arena_data)
        SNTD = second_nearest_troop_data(arena_data)
        if i.name == NTD[1] or i.name == SNTD[1]:
            continue
        else:
            x, y = i.position
            if calculate_distance((x, y), (0, 0)) < w:
                w = calculate_distance((x, y), (0, 0))
                Z = i.name
                P = (x, y)
                H = i.health
                H_ = attri(i.name)["Max Health"]

    data = [w, Z, P, H, H_]
    return data

def troop_deployed(tup):
    name, position = tup
    if troop_is_deployable(name):
        deploy_list.list_.append((name, position))
        eval(team_signal)['E'] -= attri(name)["Elixir"]
        eval(team_signal)["deck"].remove(name)

def multi_attack_at_position(arena_data, position):
    count = 0
    for i in arena_data["OppTroops"]:
        if i.name=="Balloon" or i.name=="Giant":
            continue
        if calculate_distance(i.position, position) < attri(i.name)["Discovery Range"]+attri(i.name)["Size"]+2:
            count += 1
    return count

def pref(L, arena_data):
    i=0
    for i in range(len(L)):
        if L[i] in arena_data["MyTower"].deployable_troops and attri(L[i])["Elixir"] <= arena_data["MyTower"].total_elixir:
            return L[i]

def my_troop_position(arena_data, name):
    for i in arena_data["MyTroops"]:
        if i.name == name:
            return i.position
    return (0, 0)

def my_troop_health(arena_data, name):
    for i in arena_data["MyTroops"]:
        if i.name == name:
            return i.health
    return 0

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

def troop_attack(Z, arena_data, Z2=""):
    attack_priority = {
        "Knight": ["Wizard","Skeleton", "Dragon","Prince", "Minion", "Archer", "Knight"],#done
        "Skeleton": ["Wizard", "Dragon","Skeleton", "Archer", "Minion", "Prince","Knight"], #done
        "Valkyrie": ["Wizard","Dragon", "Archer", "Prince","Minion", "Skeleton","Knight"], #done
        "Musketeer": ["Wizard", "Dragon","Skeleton", "Prince","Minion","Archer","Knight"], #done
        "Giant": ["Skeleton", "Wizard", "Dragon","Minion","Prince",  "Archer","Knight"], #done
        "Prince": ["Wizard", "Skeleton", "Dragon", "Archer", "Minion", "Prince","Knight"], #done
        "Barbarian": ["Wizard", "Dragon", "Skeleton", "Minion", "Archer", "Prince","Knight"],#done
        "Wizard": ["Wizard", "Skeleton","Dragon", "Prince","Minion", "Archer","Knight"],  #done
        "Archer": ["Wizard","Dragon","Skeleton","Prince", "Minion", "Archer","Knight"],#done
        "Dragon": ["Wizard","Dragon","Minion","Archer", "Prince","Knight"],#done
        "Minion": ["Wizard", "Dragon", "Minion", "Archer","Skeleton","Knight"],#done
        "Balloon": ["Wizard", "Minion", "Dragon", "Archer","Knight"]#done
    }
    L = attack_priority.get(Z, ["Wizard", "Dragon", "Skeleton", "Minion", "Archer"])
    return pref(L, arena_data)

def troop_defense(Z, arena_data, Z2=""):
    L = []
    splash_troops = {"Valkyrie", "Wizard", "Dragon"}
    is_splash = Z2 in splash_troops
    is_balloon_z2 = (Z2 == "Balloon")

    # Prioritization rules
    skeleton_position_splash = 3  # Moves from 1st to 3rd/4th when splash exists
    default_order = ["Skeleton", "Wizard", "Minion", "Archer"]  # Base priority

    # Individual troop logic
    if Z == "Knight":
        if not is_splash:
            # No splash troop threatening Skeleton, so we can keep them near top.
            L = ["Wizard","Knight","Skeleton","Minion","Dragon","Archer","Prince","Giant"]
        else:
            # Splash present, move Skeleton down a bit, but not to the bottom.
            L = ["Wizard","Knight","Minion","Skeleton","Dragon","Archer","Prince","Giant"]

        if opp_troop_already_set_target_on_my_tower(arena_data, Z):
            # Example tweak: maybe we move Skeleton slightly lower if tower is already targeted
            # (you can adjust as you see fit).
            L = ["Wizard","Knight","Minion","Dragon","Skeleton","Archer","Prince","Giant"]

    elif Z == "Skeleton":
        if not is_splash:
            # Skeleton is quite good vs. single-target units
            L = ["Skeleton","Wizard","Knight","Minion","Dragon","Archer","Prince","Giant"]
        else:
            # There's a splash troop (Z2), so Skeleton goes down a bit
            # but stays mid-list, not at the very bottom.
            L = ["Wizard","Knight","Minion","Skeleton","Dragon","Archer","Prince","Giant"]

        if opp_troop_already_set_target_on_my_tower(arena_data, Z):
            # Slight reorder
            L = ["Wizard","Knight","Minion","Dragon","Skeleton","Archer","Prince","Giant"]

    elif Z == "Valkyrie":
        # Valkyrie is a splash unit herself, but let's keep the same logic style:
        if not is_splash:
            L = ["Wizard","Knight","Skeleton","Minion","Dragon","Archer","Prince","Giant"]
        else:
            L = ["Wizard","Knight","Minion","Skeleton","Dragon","Archer","Prince","Giant"]

        if opp_troop_already_set_target_on_my_tower(arena_data, Z):
            L = ["Wizard","Knight","Minion","Dragon","Skeleton","Archer","Prince","Giant"]

    elif Z == "Musketeer":
        if not is_splash:
            L = ["Wizard","Knight","Skeleton","Minion","Dragon","Archer","Prince","Giant"]
        else:
            L = ["Wizard","Knight","Minion","Skeleton","Dragon","Archer","Prince","Giant"]

        if opp_troop_already_set_target_on_my_tower(arena_data, Z):
            L = ["Wizard","Knight","Minion","Dragon","Skeleton","Archer","Prince","Giant"]

    elif Z == "Giant":
        if not is_splash:
            L = ["Wizard","Knight","Skeleton","Minion","Dragon","Archer","Prince","Giant"]
        else:
            L = ["Wizard","Knight","Minion","Skeleton","Dragon","Archer","Prince","Giant"]

        if opp_troop_already_set_target_on_my_tower(arena_data, Z):
            L = ["Wizard","Knight","Minion","Dragon","Skeleton","Archer","Prince","Giant"]

    elif Z == "Prince":
        if not is_splash:
            L = ["Skeleton","Wizard","Knight","Minion","Dragon","Archer","Prince","Giant"]
        else:
            L = ["Wizard","Knight","Minion","Skeleton","Dragon","Archer","Prince","Giant"]

        if opp_troop_already_set_target_on_my_tower(arena_data, Z):
            L = ["Wizard","Knight","Minion","Dragon","Skeleton","Archer","Prince","Giant"]

    elif Z == "Barbarian":
        if not is_splash:
            L = ["Wizard","Knight","Skeleton","Minion","Dragon","Archer","Prince","Giant"]
        else:
            L = ["Wizard","Knight","Minion","Skeleton","Dragon","Archer","Prince","Giant"]

        if opp_troop_already_set_target_on_my_tower(arena_data, Z):
            L = ["Wizard","Knight","Minion","Dragon","Skeleton","Archer","Prince","Giant"]

    elif Z == "Wizard":
        # He is splash, so if is_splash is True, it means there's a second splash from Z2, etc.
        if not is_splash:
            L = ["Wizard","Knight","Skeleton","Minion","Dragon","Archer","Prince","Giant"]
        else:
            L = ["Wizard","Knight","Minion","Skeleton","Dragon","Archer","Prince","Giant"]

        if opp_troop_already_set_target_on_my_tower(arena_data, Z):
            L = ["Wizard","Knight","Minion","Dragon","Skeleton","Archer","Prince","Giant"]

    elif Z == "Archer":
        if not is_splash:
            L = ["Wizard","Knight","Skeleton","Minion","Dragon","Archer","Prince","Giant"]
        else:
            L = ["Wizard","Knight","Minion","Skeleton","Dragon","Archer","Prince","Giant"]

        if opp_troop_already_set_target_on_my_tower(arena_data, Z):
            L = ["Wizard","Knight","Minion","Dragon","Skeleton","Archer","Prince","Giant"]

    elif Z == "Dragon":
        if not is_splash:
            L = ["Wizard","Knight","Skeleton","Minion","Dragon","Archer","Prince","Giant"]
        else:
            # If Z is Dragon, is_splash is always True, but we keep the same logic:
            L = ["Wizard","Knight","Minion","Skeleton","Dragon","Archer","Prince","Giant"]

        if opp_troop_already_set_target_on_my_tower(arena_data, Z):
            L = ["Wizard","Knight","Minion","Dragon","Skeleton","Archer","Prince","Giant"]

    elif Z == "Minion":
        if not is_splash:
            L = ["Wizard","Knight","Skeleton","Minion","Dragon","Archer","Prince","Giant"]
        else:
            L = ["Wizard","Knight","Minion","Skeleton","Dragon","Archer","Prince","Giant"]

        if opp_troop_already_set_target_on_my_tower(arena_data, Z):
            L = ["Wizard","Knight","Minion","Dragon","Skeleton","Archer","Prince","Giant"]

    elif Z == "Balloon":
        # For Balloon, same approach. Often you'd want air-targeting troops first:
        if not is_splash:
            L = ["Wizard","Knight","Skeleton","Minion","Dragon","Archer","Prince","Giant"]
        else:
            L = ["Wizard","Knight","Minion","Skeleton","Dragon","Archer","Prince","Giant"]

        if opp_troop_already_set_target_on_my_tower(arena_data, Z):
            L = ["Wizard","Knight","Minion","Dragon","Skeleton","Archer","Prince","Giant"]

    else:
        # Fallback if troop not recognized
        L = ["Wizard","Knight","Minion","Dragon","Archer","Skeleton","Prince","Giant"]

    return pref(L, arena_data)


def logic(arena_data:dict):
    air_troops = {"Minion", "Dragon", "Balloon"}
    ground_troops = {"Archer", "Knight", "Skeleton", "Valkyrie", "Musketeer", "Giant", "Prince", "Barbarian", "Wizard"}
    air_attacking_troops = {"Minion", "Dragon", "Archer", "Wizard"}
    splash_damage_troops = {"Valkyrie", "Wizard", "Dragon"}

    global team_signal
    game_timer = arena_data["MyTower"].game_timer
    mu_me_le_e = arena_data["MyTower"].total_elixir
    mu_me_le_deck=str(arena_data["MyTower"].deployable_troops)
    team_signal="{\"E\":"+str(mu_me_le_e)+",\"deck\":"+mu_me_le_deck+"}"
    w, Z, (X, Y), H, H_ = nearest_troop_data(arena_data)
    w2, Z2, (X2, Y2), H2, H_2 = second_nearest_troop_data(arena_data)
    w3, Z3, (X3, Y3), H3, H_3 = third_nearest_troop_data(arena_data)
    print("game_timer =", game_timer)
    S = 9.375*attri(Z)["Size"]
    S2 = 9.375*attri(Z2)["Size"]
    S3 = 9.375*attri(Z3)["Size"]
    TS = 9.375
    DR = 9.375*attri(Z)["Discovery Range"]
    DR2 = 9.375*attri(Z2)["Discovery Range"]
    DR3 = 9.375*attri(Z3)["Discovery Range"]
    M = DR+S
    M2 = DR2+S2
    M3 = DR3+S3
    AR = attri(Z)["Attack Range"]
    AR2 = attri(Z2)["Attack Range"]
    AR3 = attri(Z3)["Attack Range"]

    a = multi_attack_at_position(arena_data, (X, Y)) > 2
    b = "Giant" in mu_me_le_deck
    c = b or not a

    x_giant = my_troop_position(arena_data, "Giant")[0]
    y_giant = my_troop_position(arena_data, "Giant")[1]
    health_giant = my_troop_health(arena_data, "Giant")
    x_wizard = my_troop_position(arena_data, "Wizard")[0]
    y_wizard = my_troop_position(arena_data, "Wizard")[1]
    health_wizard = my_troop_health(arena_data, "Wizard")
    x_balloon = my_troop_position(arena_data, "Balloon")[0]
    y_balloon = my_troop_position(arena_data, "Balloon")[1]

    if opp_troop_already_set_target_on_my_tower(arena_data, Z) or opp_troop_already_set_target_on_my_tower(arena_data, Z2):
        if opp_troop_already_set_target_on_my_tower(arena_data, Z):
            troop_deployed((troop_attack(Z, arena_data), (X, Y)))
            troop_deployed((troop_attack(Z, arena_data), (X, Y)))
            troop_deployed((troop_attack(Z, arena_data), (X, Y)))
        if opp_troop_already_set_target_on_my_tower(arena_data, Z2):
            troop_deployed((troop_attack(Z2, arena_data), (X2, Y2)))
            troop_deployed((troop_attack(Z2, arena_data), (X2, Y2)))
            troop_deployed((troop_attack(Z2, arena_data), (X2, Y2)))
        print(1)

    if 50>Y>30 and opp_troop_already_set_target_on_my_troop(arena_data, Z)==False:
        if Z=="Valkyrie" and c: #check all. increase options. priority also matters #done
            if troop_is_deployable("Giant") and (eval(team_signal)["E"]>7 or (b and a)):
                troop_deployed(("Giant", (X-5*sgn(X), min(Y+5, 50)))) if H2==1 else troop_deployed(("Giant", (X-3*sgn(X), Y-3)))
            elif troop_is_deployable("Knight"):
                troop_deployed(("Knight", (X, Y)))
            elif troop_is_deployable("Minion"):
                troop_deployed(("Minion", (X, Y-5)))
            elif troop_is_deployable("Dragon"):
                troop_deployed(("Dragon", (X, Y-7)))
            elif troop_is_deployable("Wizard"):
                troop_deployed(("Wizard", (X, Y-10)))

        if Z=="Giant" and c: #done
            if troop_is_deployable("Skeleton"):
                troop_deployed(("Skeleton", (X, Y))) if (H2==1 or Y2-Y>M2+5 or Z2 not in splash_damage_troops) else troop_deployed(("Skeleton", (X, Y-5)))
            elif troop_is_deployable("Wizard"):
                troop_deployed(("Wizard", (X, Y-12)))
            elif troop_is_deployable("Minion"):
                troop_deployed(("Minion", (X, Y-M-2.5)))
            elif troop_is_deployable("Prince") and Z2!="Skeleton":
                troop_deployed(("Prince", (X, Y)))
            elif troop_is_deployable("Knight") and Z2!="Skeleton":
                troop_deployed(("Knight", (X, Y)))

        if Z=="Dragon": #done
            if troop_is_deployable("Giant") and eval(team_signal)["E"]>8:
                troop_deployed(("Giant", (X-7*sgn(X), min(Y+7, 50)))) if H2==1 else troop_deployed(("Giant", (X-5*sgn(X), Y-8)))
            elif troop_is_deployable("Wizard"):
                troop_deployed(("Wizard", (X, Y-15)))
            elif troop_is_deployable("Dragon"):
                troop_deployed(("Dragon", (0, 0)))
            elif troop_is_deployable("Minion") and (H2==1 or Z2 not in air_attacking_troops):
                troop_deployed(("Minion", (X, Y)))

        if Z=="Wizard": #done?
            if troop_is_deployable("Giant") and eval(team_signal)["E"]>8:
                troop_deployed(("Giant", (X-8*sgn(X), Y-3)))
            elif troop_is_deployable("Knight") and (H2==1 or Y2-Y>M2+10):
                troop_deployed(("Knight", (X, Y)))
            elif troop_is_deployable("Skeleton") and (H2==1 or Y2-Y>M2+10 or Z2 not in splash_damage_troops): #check
                troop_deployed(("Skeleton", (X, Y)))
            elif troop_is_deployable("Wizard"):
                troop_deployed(("Wizard", (X, Y-14)))
            elif troop_is_deployable("Prince") and (H2==1 or Y2-Y>M2+10 or Z2 in ground_troops):
                troop_deployed(("Prince", (X, Y)))

        if Z=="Minion": #done
            if troop_is_deployable("Giant") and eval(team_signal)["E"]>8:
                troop_deployed(("Giant", (X-5*sgn(X), min(Y+5, 50)))) if H2==1 else troop_deployed(("Giant", (X-5*sgn(X), Y-5)))
            elif troop_is_deployable("Wizard"):
                troop_deployed(("Wizard", (X, Y-15)))
            elif troop_is_deployable("Dragon"):
                troop_deployed(("Dragon", (X, Y-11)))
            elif troop_is_deployable("Minion"):
                troop_deployed(("Minion", (X, Y))) if H2==1 or Z2 not in air_attacking_troops or Y2-Y>M2+7 else troop_deployed(("Minion", (X, Y-5)))

        if Z=="Prince": #done
            if troop_is_deployable("Giant") and eval(team_signal)["E"]>7:
                troop_deployed(("Giant", (X-5*sgn(X), Y-5)))
            elif troop_is_deployable("Skeleton"):
                troop_deployed(("Skeleton", (X, Y))) if (H2==1 or Y2-Y>M2+7 or Z2 not in splash_damage_troops) else troop_deployed(("Skeleton", (X, Y-10)))
            elif troop_is_deployable("Wizard"):
                troop_deployed(("Wizard", (X, Y-14)))
            elif troop_is_deployable("Prine"):
                troop_deployed(("Prince", (X, Y-5))) if (Y2==0 or Y2-Y>15) else troop_deployed(("Prince", (X, Y-10)))
            elif troop_is_deployable("Minion"):
                troop_deployed(("Minion", (X, Y-7)))

        if Z=="Archer":
            if troop_is_deployable("Wizard"):
                troop_deployed(("Wizard", (X, Y)))
            elif troop_is_deployable("Skeleton"):
                troop_deployed(("Skeleton", (X, Y)))
            elif troop_is_deployable("Archer") and eval(team_signal)["E"]>6:
                troop_deployed(("Archer", (X, Y)))
        if Z=="Skeleton":
            if troop_is_deployable("Wizard"):
                troop_deployed(("Wizard", (X, Y-10)))
            elif troop_is_deployable("Dragon"):
                troop_deployed(("Dragon", (X, Y-8)))
            elif troop_is_deployable("Skeleton"):
                troop_deployed(("Skeleton", (X, Y)))
        if Z=="Barbarian":
            if troop_is_deployable("Dragon"):
                troop_deployed(("Dragon", (X, Y-5)))
            elif troop_is_deployable("Minion"):
                troop_deployed(("Minion", (X, Y)))
        if Z=="Balloon":
            if troop_is_deployable("Wizard"):
                troop_deployed(("Wizard", (X, Y)))
            elif troop_is_deployable("Dragon"):
                troop_deployed(("Dragon", (X, Y)))
            elif troop_is_deployable("Minion"):
                troop_deployed(("Minion", (X, Y)))
            elif troop_is_deployable("Archer"):
                troop_deployed(("Archer", (X, Y)))
        if Z=="Knight":
            if troop_is_deployable("Dragon"):
                troop_deployed(("Dragon", (X, Y-8)))
            elif troop_is_deployable("Minion"):
                troop_deployed(("Minion", (X, Y-5)))
            elif troop_is_deployable("Knight"):
                troop_deployed(("Knight", (X, Y)))
            elif troop_is_deployable("Skeleton"):
                troop_deployed(("Skeleton", (X, Y)))
        if Z=="Musketeer":
            if troop_is_deployable("Giant") and eval(team_signal)["E"]>8:
                troop_deployed(("Giant", (X, Y)))
            elif troop_is_deployable("Skeleton"):
                troop_deployed(("Skeleton", (X, Y-5)))
            elif troop_is_deployable("Dragon"):
                troop_deployed(("Dragon", (X, Y-5)))

    if Z=="Wizard" and 50<Y<70:
        if troop_is_deployable("Wizard"):
            if H2==1 or Y2-Y>15:
                troop_deployed(("Wizard", (X, 100-Y)))
            print(-1)

    if TS+S+DR<w<35 and TS+S2+DR2<w2<40 and w3<50 and opp_has_balloon(arena_data)==False:
        if opp_troop_already_set_target_on_my_troop(arena_data, Z)==False:
            if opp_troop_already_set_target_on_my_troop(arena_data, Z2)==False:
                if opp_troop_already_set_target_on_my_troop(arena_data, Z3)==False:
                    troop_deployed(("Gaint", (0, 7)))
                    print(0)

    if TS+S+DR<w<35 and TS+S2+DR2<w2<40 and w3<50 and opp_has_balloon(arena_data)==True:
        if Z == "Balloon" and eval(team_signal)["E"]>7:
            troop_deployed((troop_attack(Z, arena_data), (3*sgn(X)+X/2, Y/2-3)))
        if opp_troop_already_set_target_on_my_troop(arena_data, Z)==False:
            if opp_troop_already_set_target_on_my_troop(arena_data, Z2)==False:
                if opp_troop_already_set_target_on_my_troop(arena_data, Z3)==False:
                    troop_deployed(("Gaint", (0, 7)))
        if Z2 == "Balloon":
            troop_deployed((troop_attack(Z2, arena_data), (3*sgn(X)+X/2, Y/2-3)))
        if Z3 == "Balloon":
            troop_deployed((troop_attack(Z3, arena_data), (3*sgn(X)+X/2, Y/2-3)))
        print(0)

    if Z!="Balloon":
        if w<TS+S+DR+5 and opp_troop_already_set_target_on_my_troop(arena_data, Z)==False:
            if w2>35:
                troop_deployed((troop_defense(Z, arena_data), (X/2, Y/2)))
                print(3)
            else:
                if w3>45:
                    deploy_position = (0, 8) if -10 < X2 < 10 else (5 * sgn(X), 8) if (X * X2 >= 0) else (X / 2, 8)
                    troop_deployed((troop_defense(Z, arena_data, Z2), deploy_position))
                    print(4)
                    if X * X2 < 0:
                        troop_deployed((troop_defense(Z2, arena_data), (X2 / 2, 8)))
                        print(5)
                else: 
                    if opp_troop_already_set_target_on_my_troop(arena_data, Z2)==False and X*X2>=0 and X2*X3>0:
                        troop_deployed((troop_defense(Z, arena_data, Z2), (5*sgn(X), 8)))
                    if opp_troop_already_set_target_on_my_troop(arena_data, Z2)==False and X*X2<0 and X2*X3>0:
                        troop_deployed((troop_defense(Z, arena_data, Z2), (4*sgn(X),8)))
                    if opp_troop_already_set_target_on_my_troop(arena_data, Z2)==False and X*X2<0 and X2*X3<0:
                        troop_deployed((troop_defense(Z, arena_data), (X2-2*sgn(X2),Y2)))
                    if X*X2>=0 and X2*X3<0:
                        troop_deployed((troop_defense(Z, arena_data, Z2), (5*sgn(X), 8)))
                    print(6)

        if w<TS+S+DR+5 and opp_troop_already_set_target_on_my_troop(arena_data, Z): 
            if w2<40:
                if w3>60:
                    if X*X2>=0:
                        troop_deployed((troop_defense(Z2, arena_data, Z), (X2, Y2)))
                    if X * X2 < 0:
                        troop_deployed((troop_defense(Z2, arena_data), (X2 / 2, 8)))
                else: 
                    if opp_troop_already_set_target_on_my_troop(arena_data, Z2)==False and X*X2>=0 and X2*X3>0:
                        troop_deployed((troop_defense(Z2, arena_data, Z3), (X2, Y2)))
                    if opp_troop_already_set_target_on_my_troop(arena_data, Z2)==False and X*X2<0 and X2*X3>0:
                        troop_deployed((troop_defense(Z2, arena_data, Z3), (5*sgn(X2),8)))
                    if opp_troop_already_set_target_on_my_troop(arena_data, Z2)==False and X*X2<0 and X2*X3<0:
                        troop_deployed((troop_defense(Z2, arena_data), (5*sgn(X2), 8)))
                    if X*X2>=0 and X2*X3<0:
                        if opp_troop_already_set_target_on_my_troop(arena_data, Z2)==False:
                            if w3<35:
                                troop_deployed((troop_defense(Z3, arena_data), (8*sgn(X3),8)))
                        else:
                            troop_deployed((troop_defense(Z3, arena_data), (X3,10)))
                print(7)
    if Z=="Balloon":
        if w<40 and (my_troop_already_set_target_on_opp_troop(arena_data, Z)==False or (H>800 and w<30)):
            if w2>35:
                troop_deployed((troop_defense(Z, arena_data), (X/2, Y/2)))
                print(3)
            else:
                if w3>45:
                    deploy_position = (0, 8) if -10 < X2 < 10 else (5 * sgn(X), 8) if (X * X2 >= 0) else (X / 2, 8)
                    troop_deployed((troop_defense(Z, arena_data, Z2), deploy_position))
                    print(4)
                    if X * X2 < 0:
                        troop_deployed((troop_defense(Z2, arena_data), (X2 / 2, 8)))
                        print(5)
                else: 
                    if opp_troop_already_set_target_on_my_troop(arena_data, Z2)==False and X*X2>=0 and X2*X3>0:
                        troop_deployed((troop_defense(Z, arena_data, Z2), (5*sgn(X), 8)))
                    if opp_troop_already_set_target_on_my_troop(arena_data, Z2)==False and X*X2<0 and X2*X3>0:
                        troop_deployed((troop_defense(Z, arena_data, Z2), (4*sgn(X),8)))
                    if opp_troop_already_set_target_on_my_troop(arena_data, Z2)==False and X*X2<0 and X2*X3<0:
                        troop_deployed((troop_defense(Z, arena_data), (X2-2*sgn(X2),Y2)))
                    if X*X2>=0 and X2*X3<0:
                        troop_deployed((troop_defense(Z, arena_data, Z2), (5*sgn(X), 8)))
                    print(6)



    if (Y>70 or Y==0) and eval(team_signal)["E"]>5 and game_timer>50:
        if troop_is_deployable("Giant") and y_giant<30 and Z!="Skeleton" and Z2!="Skeleton" and H3==1 and (Y>70 or Y==0):
            if troop_is_deployable("Wizard") or troop_is_deployable("Prince"):
                troop_deployed(("Giant", (12*sgn(-X), 50))) if X!=0 else troop_deployed(("Giant", (12*sgn(-X2), 50))) if X2!=0 else troop_deployed(("Giant", (12, 50)))
        if y_giant > 55 and health_giant > 2500:
            if troop_is_deployable("Prince") and y_giant>65:
                troop_deployed(("Prince", (25*sgn(-x_giant), 50))) if x_giant!=0 else troop_deployed(("Prince", (25*sgn(-X), 50))) if X!=0 else troop_deployed("Prince", (25*sgn(-X2), 50))
            if troop_is_deployable("Wizard"):
                troop_deployed(("Wizard", (x_giant, 50))) #needed more options
        print(16)

    if Y!=0 and eval(team_signal)["E"]==10 and len(arena_data["MyTroops"])==0 and (Y2==0 or Y2-Y>20) and H3==1:
        if troop_is_deployable(Z) and Z!="Giant":
            troop_deployed((Z, (X, 100-Y)))
        else:
            troop_deployed((troop_attack(Z, arena_data), (X, 100-Y)))
        print(9)
    if eval(team_signal)["E"]>8 and Y>50 and Y<80 and len(arena_data["MyTroops"])==0 and (Y2==0 or Y2-Y>10) and H3==1:
        if troop_is_deployable(Z):
            troop_deployed((Z, (X, 100-Y)))
        else:
            troop_deployed((troop_attack(Z, arena_data), (X, 100-Y)))
        print(10)
    if eval(team_signal)["E"]>5 and Y>30 and Y<50 and Y2<50 and len(arena_data["MyTroops"])<=1:   #gotta update this:
        if troop_is_deployable(Z2):
            troop_deployed((Z2, (X2, Y2)))
        else:
            troop_deployed((troop_defense(Z2, arena_data), (X2, Y2)))
        print(12)
    
    if (y_giant>70 and health_giant>2000) or (70>y_giant>40 and health_giant>1200) or (40>y_giant>22 and health_giant>300):
        if opp_troop_already_set_target_on_my_troop(arena_data, Z) and len(arena_data["MyTroops"])==1:
            troop_deployed((troop_attack(Z, arena_data), (X, min(50, y_giant-3))))
            print(13)
        if opp_troop_already_set_target_on_my_troop(arena_data, Z2) and len(arena_data["MyTroops"])<=2:
            troop_deployed((troop_attack(Z, arena_data), (X, min(50, y_giant-3))))
            print(14)
        if opp_troop_already_set_target_on_my_troop(arena_data, Z3) and len(arena_data["MyTroops"])<=3:
            troop_deployed((troop_attack(Z, arena_data), (X, min(50, y_giant-3))))
            print(15)

    if eval(team_signal)["E"]==10:
        troop_deployed((arena_data["MyTower"].deployable_troops[0], (0, 15)))
        print(17)

    

    """
    if Y==0 and len(arena_data["MyTroops"])==0:
        if troop_is_deployable("Wizard"):
            troop_deployed(("Wizard", (0, 40)))
        if troop_is_deployable("Giant"):
            troop_deployed(("Giant", (0, 40)))
        print(17)
    """

    print("OPP TROOP INFO")
    print("M =", M, "Z =", Z, "w =", w, "E =", eval(team_signal)["E"], "H_ =", H_)
    print("M2 =", M2, "Z2 =", Z2, "w2 =", w2, "H_2 =", H_2)
    for i in arena_data["OppTroops"]:
        print(i.name, i.position, i.health)
    for i in arena_data["OppTroops"]:
        if i.name == Z and i.target!=None:
            print(Z, "target is", i.target.name)
        if i.name == Z and i.target==None:
            print(Z, "target is None")
        if i.name == Z2 and i.target!=None:
            print(Z2, "target is", i.target.name)
        if i.name == Z2 and i.target==None:
            print(Z2, "target is None")
    print("MY TROOP INFO")
    for i in arena_data["MyTroops"]:
        print(i.name, i.position, i.health)
    
    # list pe kaam karna hai abhi bhi, troop attack ki bhi banani hai
    # different code for different time.***** --- 1200 se pehle aur baad me alag alag code --- change both when needed to
    # supply excess elixir in the end of the game
    # zero timer no employment of troops problem solve
    # kill balloon little early
    # imporve c.py and fight it with final code with different troops