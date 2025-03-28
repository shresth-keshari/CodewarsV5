import random
import numpy as np
from numpy.ma.extras import average

from teams.helper_function import Troops, Utils

team_name = "Abhaysimha"
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

    no_troops = len(my_troops)
    danger_score = sum( 1 for opp_troop in opp_troops if  (opp_troop.position[1] < 35))
    opp_posx = average( [opp_troop.position[0] for opp_troop in opp_troops ])
    opp_posy = average( [opp_troop.position[0] for opp_troop in opp_troops ])

    #if opp_troops:
        #print(opp_troops[0].position[0])
        #print(opp_troops[0].position[1])
    special_case = False
    #print(f"Danger score : {danger_score}")
    for opp_troop in opp_troops:
        if opp_troop.name == "Wizard" and opp_troop.position[1] <= 50:
            if not((danger_score is 0) or (danger_score >0 and opp_troop.position[1]<30)):
                break
            special_case = True
            reinforcement = True
            for troop in deployable:
                if troop == "Valkyrie" or troop == "Prince" or troop == "Barbarian":
                    deploy_troop = "Valkyrie" if "Valkyrie" in deployable else "Prince" if "Prince" in deployable else "Barbarian" if "Barbarian" else ""
                    deploy_list.list_.append((deploy_troop, opp_troop.position))
                    reinforcement = "Wizard" if "Wizard" in deployable else "Dragon" if "Dragon" in deployable else "Musketeer" if "Musketeer" in deployable else ""
                    deploy_list.list_.append((reinforcement, (opp_troop.position[0]+2, opp_troop.position[1])))
                else:
                    if(Utils.calculate_distance(arena_data["MyTower"], opp_troop) < 14):
                        deploy_troop = "Dragon" if "Dragon" in deployable else "Musketeer"
                        deploy_list.list_.append((deploy_troop, opp_troop.position))

    if not special_case:
        if (my_troops) and ("Giant" in [troop.name for troop in my_troops] or "Prince" in [troop.name for troop in my_troops]):
            #print([troop.name for troop in my_troops])
            if "Wizard" or "Dragon" or "Musketeer" in deployable:
                deploy_troop = "Wizard" if "Wizard" in deployable else "Dragon" if "Dragon" in deployable else "Musketeer" if "Musketeer" in deployable else "Barbarian" if "Barbarian" in deployable else "Minion"
                if danger_score>0:
                    deploy_pos = (4, 3)
                    #print("a")
                else:
                    posx = average([troop.position[0] for troop in my_troops if troop.name == "Giant" or troop.name == "Prince"])
                    posy = min([troop.position[1] for troop in my_troops if troop.name == "Giant" or troop.name == "Prince"] if [troop.position[1] for troop in my_troops if troop.name == "Giant" or troop.name == "Prince"] else [10])
                    posy = 60 - (60-posy)*1.25
                    if posy > 50 : posy = 49
                    if np.isnan(posx): posx = 0
                    posx = int(posx)
                    posy = int(posy)
                    deploy_pos = (posx, posy)
                    #print("b")
                    #print(deploy_pos)
            else:
                deploy_troop = "Barbarian" if "Barbarian" in deployable else "Minion" if "Minion" in deployable else "Valkyrie"
                if danger_score>0:
                    deploy_pos = (4, 3)
                    #print("c")
                else:
                    posx = average([troop.position[0] for troop in my_troops if troop.name == "Giant" or troop.name == "Prince"])
                    posy = min([troop.position[1] for troop in my_troops if troop.name == "Giant" or troop.name == "Prince"] if [troop.position[1] for troop in my_troops if troop.name == "Giant" or troop.name == "Prince"] else [10]) - 3
                    if posy > 50 : posy = 50
                    if np.isnan(posx): posx = 0
                    posx = int(posx)
                    posy = int(posy)
                    deploy_pos = (posx, posy)
                    #print("d")
        else:
            #print("here")
            deploy_troop = "Giant" if "Giant" in deployable else "Prince" if "Prince" in deployable else "Barbarian" if "Barbarian" in deployable else "Minion" if "Minion" in deployable else "Valkyrie"
            if danger_score > 0:
                deploy_troop = "Prince" if "Prince" in deployable else "Barbarian" if "Barbarian" in deployable else "Minion" if "Minion" in deployable else "Valkyrie" if "Valkyrie" in deployable else "Giant"
                deploy_pos = (0, 6)
                #print("e")
            else:
                if no_troops > 1:
                    if deploy_troop == "Giant" or deploy_troop == "Prince":
                        deploy_pos = (0, 45)
                        #print("f")
                else:
                    deploy_pos = (opp_posx, 8)
                    #print("g")
    #print(f"Deploy troop: {deploy_troop}  Position: {deploy_pos}")

    for troop in opp_troops:
        if(troop.type == "Air"):
            danger_score = sum(1 for opp_troop in opp_troops if (opp_troop.position[1] < 40))

    if(danger_score>0):
        for troop in opp_troops:
            if(troop.type == "Air"):
                deploy_troop = "Dragon" if "Dragon" in deployable else "Musketeer" if "Musketeer" in deployable else "Minion" if "Minion" in deployable else  "Wizard" if "Wizard" in deployable else "Barbarian"
                deploy_pos = (0,2)
                if(deploy_troop == "Wizard"):
                    deploy_pos = (deploy_pos[0],(deploy_pos[1]-10) if (deploy_pos[1] > 10) else 0)

    for troop in opp_troops:
        if(troop.name == "Dragon" and troop.position[1] < 45):
            deploy_troop = "Dragon" if "Dragon" in deployable else "Minion" if "Minion" in deployable else "Wizard" if "Wizard" in deployable else "Musketeer" if "Musketeer" in deployable else "Barbarian"
            deploy_pos = troop.position
        if(troop.name == "Minion" and troop.position[1] < 60):
            deploy_troop = "Dragon" if "Dragon" in deployable else "Minion" if "Minion" in deployable else "Wizard" if "Wizard" in deployable else "Musketeer" if "Musketeer" in deployable else "Barbarian"
            deploy_pos = troop.position
        if(troop.name == "Valkyrie" and troop.position[1] < 30):
            deploy_troop = "Barbarian" if "Barbarian" in deployable else "Minion" if "Minion" in deployable else "Musketeer" if "Musketeer" in deployable else "Prince" if "Prince" in deployable else "Giant"
            deploy_pos = (troop.position[0]/2, troop.position[1]/2)

    if deploy_troop != "" and not(special_case):
        deploy_list.list_.append((deploy_troop, deploy_pos))