import random
import numpy as np
from numpy.ma.extras import average

from teams.helper_function import Troops, Utils

team_name = "Lisan-Al-Coders"
troops = [
    Troops.musketeer, Troops.minion, Troops.prince, Troops.giant,
    Troops.dragon, Troops.barbarian, Troops.wizard, Troops.valkyrie
]
deploy_list = Troops([])
team_signal = ""


def deploy(arena_data: dict):
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal


def logic(arena_data: dict):
    current_elixir = arena_data["MyTower"].total_elixir
    global team_signal
    my_troops = arena_data["MyTroops"]
    opp_troops = arena_data["OppTroops"]
    deployable = arena_data["MyTower"].deployable_troops
    enemies = []
    deploy_troop = ""
    deploy_pos = (0, 0)
    imm_deploy_list=(())
    opp_posx_air = 0
    opp_posx_ground = 0
    has_wizard = False
    
    opp_count_air = 0
    opp_count_ground = 0
    danger_score = 0
    for troop in opp_troops:
        #print(troop.type)
        if troop.name == "Wizard":
            has_wizard = True
        if(troop.position[1] < 35):
            danger_score += 1
        if(troop.type == "air"):
            opp_count_air += 1
            opp_posx_air = average([troop.position[0]])
            #print(troop.position[0])
        else:
            opp_count_ground += 1
            opp_posx_ground = average([troop.position[0]])

    no_troops = len(my_troops)
    if opp_posx_air > 25: opp_posx_air = 25
    if opp_posx_air < -25: opp_posx_air = -25
    if opp_posx_ground > 25: opp_posx_ground = 25
    if opp_posx_ground < -25: opp_posx_ground = -25
    #print(f"Air : {opp_posx_air}")
    #print(f"Ground : {[opp_troop.position[0] for opp_troop in opp_troops if opp_troop.type == "Ground"]}")
    opp_posx = average( [opp_troop.position[0] for opp_troop in opp_troops])
    opp_troop_names = [opp_troop.name for opp_troop in opp_troops]
    threat = "Wizard" if "Wizard" in opp_troop_names else "Dragon" if "Dragon" in opp_troop_names else "Valkyrie" if "Valkyrie" in opp_troop_names else "Prince" if "Prince" in opp_troop_names else ""
    threat_pos = (0,0)
    for opp_troop in opp_troops:
        if opp_troop.name == threat:
            threat_pos = opp_troop.position
    opp_posy = average( [opp_troop.position[0] for opp_troop in opp_troops ])

    danger_x = average([opp_troop.position[0] for opp_troop in opp_troops if opp_troop.position[1] < 40])
    #if opp_troops:
        #print(opp_troops[0].position[0])
        #print(opp_troops[0].position[1])
    special_case = False
    #print(f"Danger score : {danger_score}")
    for opp_troop in opp_troops:
        if opp_troop.name == "Wizard" and opp_troop.position[1] <= 50:
            if not((danger_score is 0) or (danger_score >0 and opp_troop.position[1]<35)):
                break
            special_case = True
            reinforcement = True
            for troop in deployable:
                if troop == "Valkyrie" or troop == "Prince" or troop == "Barbarian":
                    deploy_troop = "Valkyrie" if "Valkyrie" in deployable else "Prince" if "Prince" in deployable else "Barbarian" if "Barbarian" else ""
                    deploy_list.list_.append((deploy_troop, opp_troop.position))
                    reinforcement = "Wizard" if "Wizard" in deployable else "Dragon" if "Dragon" in deployable else "Musketeer" if "Musketeer" in deployable else ""
                    deploy_list.list_.append((reinforcement, (opp_troop.position[0]+2, opp_troop.position[1])))
                    #print("a")
                else:
                    if(Utils.calculate_distance(arena_data["MyTower"], opp_troop) < 14):
                        deploy_troop = "Dragon" if "Dragon" in deployable else "Wizard" if "Wizard" in deployable else "Giant" if "Giant" in deployable else "Musketeer"
                        deploy_list.list_.append((deploy_troop, opp_troop.position))
                        #print("b")

    if not special_case:
        if (my_troops) and ("Giant" in [troop.name for troop in my_troops]):
            #print([troop.name for troop in my_troops])
            if "Wizard" or "Dragon" or "Musketeer" in deployable:
                deploy_troop = "Wizard" if "Wizard" in deployable else "Dragon" if "Dragon" in deployable else "Musketeer" if "Musketeer" in deployable else "Barbarian" if "Barbarian" in deployable else "Minion"
                if danger_score>0:
                    deploy_pos = (danger_x, 7)
                    deploy_troop = "Barbarian" if "Barbarian" in deployable else "Minion" if "Minion" in deployable else "Musketeer" if "Musketeer" in deployable else "Valkyrie"
                    #print("c")
                else:
                    posx = average([troop.position[0] for troop in my_troops if troop.name == "Giant"])
                    posy = max([troop.position[1] for troop in my_troops if troop.name == "Giant"] if [troop.position[1] for troop in my_troops if troop.name == "Giant"] else [10])
                    if posy<60:
                        deploy_troop = ""
                    if np.isnan(posx): posx = 0
                    posx = int(posx)
                    posy = int(posy)
                    deploy_pos = (posx, 50)
                    #print("d")
                    #print(deploy_pos)
            else:
                deploy_troop = "Barbarian" if "Barbarian" in deployable else "Minion" if "Minion" in deployable else "Valkyrie" if "Valkyrie" in deployable else "Musketeer"
                if danger_score>0:
                    deploy_pos = (danger_x, 7)
                    deploy_troop = "Barbarian" if "Barbarian" in deployable else "Minion" if "Minion" in deployable else "Musketeer" if "Musketeer" in deployable else "Valkyrie"
                    #print("e")
                else:
                    posx = average([troop.position[0] for troop in my_troops if troop.name == "Giant" or troop.name == "Prince"])*1.25
                    posy = min([troop.position[1] for troop in my_troops if troop.name == "Giant" or troop.name == "Prince"] if [troop.position[1] for troop in my_troops if troop.name == "Giant" or troop.name == "Prince"] else [10]) - 12
                    if posy > 50 : posy = 50
                    if np.isnan(posx): posx = 0
                    posx = int(posx)
                    posy = int(posy)
                    deploy_pos = (posx, posy)
                    #print("f")
        else:
            deploy_troop = "Giant" if "Giant" in deployable else ""
            if deploy_troop:
                if danger_score > 0:
                    deploy_troop = "Prince" if "Prince" in deployable else "Barbarian" if "Barbarian" in deployable else "Minion" if "Minion" in deployable else "Valkyrie" if "Valkyrie" in deployable else "Giant"
                    deploy_pos = (opp_posx, 6)
                    deploy_list.list_.append((deploy_troop, deploy_pos))
                    #print("g")
                elif threat and current_elixir > 8:
                    if (threat_pos[0] < 0):
                        deploy_pos = (18,45)
                    else:
                        deploy_pos = (-18,45)
                elif not(opp_troops):
                    deploy_pos = (0,50)
                else:
                    deploy_pos = (np.nan, np.nan)
                #print(deploy_pos)
            elif current_elixir > 7 and not(has_wizard):
                if opp_count_air >= opp_count_ground:
                    deploy_troop = "Dragon" if "Dragon" in deployable else "Minion" if "Minion" in deployable else "Wizard" if "Wizard" in deployable else "Musketeer" if "Musketeer" in deployable else "Barbarian"
                    deploy_pos = (opp_posx_air, 50)
                    #print("h")
                else:
                    deploy_troop = "Valkyrie" if "Valkyrie" in deployable else "Barbarian" if "Barbarian" in deployable else "Wizard" if "Wizard" in deployable else "Minion" if "Minion" in deployable else "Musketeer"
                    deploy_pos = (opp_posx_ground, 50)
                    #print("j")
            else:
                deploy_troop = "Barbarian" if "Barbarian" in deployable else "Minion" if "Minion" in deployable else "Musketeer" if "Musketeer" in deployable else "Valkyrie"
                deploy_pos = (0,50)


    #print(opp_posx_air)
    #print(opp_posx_ground)


    #print(f"Deploy troop: {deploy_troop}  Position: {deploy_pos}")

    for troop in opp_troops:
        if(troop.type == "air"):
            danger_score = sum(1 for opp_troop in opp_troops if (opp_troop.position[1] < 40))

    if(danger_score>0):
        for troop in opp_troops:
            if(troop.type == "air"):
                deploy_troop = "Dragon" if "Dragon" in deployable else "Musketeer" if "Musketeer" in deployable else "Minion" if "Minion" in deployable else  "Wizard" if "Wizard" in deployable else "Barbarian"
                deploy_pos = (0,5)
                if(deploy_troop == "Wizard"):
                    deploy_pos = (deploy_pos[0],(deploy_pos[1]-10) if (deploy_pos[1] > 10) else 0)
                    #print("k")

    for troop in opp_troops:
        if(troop.name == "Dragon" and troop.position[1] < 45):
            deploy_troop = "Dragon" if "Dragon" in deployable else "Minion" if "Minion" in deployable else "Wizard" if "Wizard" in deployable else "Musketeer" if "Musketeer" in deployable else "Barbarian"
            deploy_pos = (troop.position[0], 6)
            #print("l")
        if(troop.name == "Minion" and troop.position[1] < 60):
            deploy_troop = "Dragon" if "Dragon" in deployable else "Minion" if "Minion" in deployable else "Wizard" if "Wizard" in deployable else "Musketeer" if "Musketeer" in deployable else "Barbarian"
            deploy_pos = (troop.position[0], 6)
            #print("m")
        if(troop.name == "Valkyrie" and troop.position[1] < 30):
            deploy_troop = "Barbarian" if "Barbarian" in deployable else "Minion" if "Minion" in deployable else "Musketeer" if "Musketeer" in deployable else "Prince" if "Prince" in deployable else "Giant"
            deploy_pos = (troop.position[0]/2, 5)
            #print("n")
        if(troop.name == "Wizard" and troop.position[1] < 25):
            deploy_troop == "Prince" if "Prince" in deployable else "Wizard" if "Wizard" in deployable else "Dragon" if "Dragon" in deployable else "Valkyrie" if "Valkyrie" in deployable else "Barbarian"
            deploy_pos = troop.position

    if deploy_troop != "" and not(special_case):
        deploy_list.list_.append((deploy_troop, deploy_pos))