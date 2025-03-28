from teams.helper_function import Troops, Utils

import random

team_name = "Priyam"
troops = [Troops.knight, Troops.wizard, Troops.archer, Troops.valkyrie, Troops.prince, Troops.minion, Troops.barbarian, Troops.skeleton]
deploy_list = Troops([])
team_signal = "a"

def deploy(arena_data:dict):
    """
    DON'T TEMPER DEPLOY FUCNTION
    """
    deploy_list.list_ = []
    logic(arena_data, deploy_list)
    return deploy_list.list_, team_signal

def logic(arena_data, deploy_list):
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    opp_tower = arena_data["OppTower"]
    my_troops = arena_data["MyTroops"]
    troops_data = Troops.troops_data
    opp8 = arena_data["OppTower"].deployable_troops
    our4 = arena_data["MyTower"].deployable_troops[:4]

    if my_troops == [] and my_tower.total_elixir >= 7:
        for troops in our4:
            if(troops == "Wizard"):
                deploy_list.list_.append(("Wizard", (random.randint(-25,25),0)))
            elif(troops == "Valkyrie"):
                deploy_list.list_.append(("Valkyrie", (random.randint(-25,25),0)))
            elif(troops == "Knight"):
                deploy_list.list_.append(("Knight", (random.randint(-25,25),0)))
            elif(troops == "Archer"):
                deploy_list.list_.append(("Archer", (random.randint(-25,25),0)))
            elif(troops == "Barbarian"):
                deploy_list.list_.append(("Barbarian", (random.randint(-25,25),0)))

    def counter(name, our4, a=-15):  # 'a' is the constant displacement for "far" placements
        counters = {
            "Prince": [("Skeleton", (0, 0)), ("Wizard", (0, a)), ("Barbarian", (0, 0)), ("Knight", (0, 0)), ("Valkyrie", (0, 0))],
            "Skeleton": [("Valkyrie", (0, a)), ("Wizard", (0, a)), ("Barbarian", (0, 0))],
            "Wizard": [("Skeleton", (0, 0)), ("Knight", (0, 0)), ("Valkyrie", (0, 0)), ("Prince", (0, 0))],
            "Giant": [("Minion", (0, a)), ("Skeleton", (0, 0)), ("Barbarian", (0, 0)), ("Knight", (0, 0)), ("Valkyrie", (0, 0))],
            "Balloon": [("Archer", (0, a)),("Minion", (0, a)), ("Wizard", (0, a)), ("Barbarian", (0, 0)), ("Knight", (0, 0))],
            "Valkyrie": [("Knight", (0, 0)), ("Barbarian", (0, 0)), ("Wizard", (0, a)), ("Minion", (0, a)), ("Prince", (0, a))],
            "Knight": [("Skeleton", (0, 0)), ("Valkyrie", (0, 0)), ("Prince", (0, a)), ("Wizard", (0, 0)), ("Minion", (0, a))],
            "Dragon": [("Minion", (0, 0)), ("Wizard", (0, a)), ("Archer", (0, a)), ("Barbarian", (0, 0)), ("Knight", (0, 0))],
            "Barbarian": [("Knight", (0, a)), ("Wizard", (0, a)), ("Skeleton", (0, 0)), ("Barbarian", (0, a)), ("Prince", (0, a))],
            "Musketeer": [("Barbarian", (0, 0)), ("Knight", (0, 0)), ("Valkyrie", (0, 0)), ("Skeleton", (0, 0)), ("Minion", (0, a))],
            "Minion": [("Wizard", (0, a)), ("Minion", (0, a)), ("Archer", (0, a)), ("Barbarian", (0, 0)), ("Knight", (0, 0))],
            "Archer": [("Valkyrie", (0, 0)), ("Barbarian", (0, 0)), ("Knight", (0, 0)), ("Skeleton", (0, 0)), ("Minion", (0, a))]
        }

        if name in counters:
            for counter_card, (x, y) in counters[name]:
                if counter_card in our4:
                    return (counter_card, (x, y))  # Returns both counter and (x, y) placement

    for troop in opp_troops:
        if troop and counter(troop.name, our4):
            if troop.target == None:
                pos = troop.position
                cname = counter(troop.name, our4)[0]
                cx = counter(troop.name, our4)[1][0]
                cy = counter(troop.name, our4)[1][1]
#                print(cname, cx, cy)
                nx = pos[0] + cx
                ny = pos[1] + cy
                deploy_list.list_.append((cname,(nx, ny)))
    
    def synergy(name, elixir, our4):

        list = {
            "Prince": ["Wizard", "Skeleton", "Valkyrie", "Barbarian"],
            "Valkyrie": ["Prince", "Wizard", "Minion", "Skeleton"],
            "Skeleton": [],
            "Wizard": ["Prince", "Skeleton", "Archer"],
            "Archer": [],
            "Knight": ["Skeleton", "Valkyrie", "Archer"],
            "Barbarian": [],
            "Minion": []
        }
        
        if name in list:
            for sname in list[name]:
                if sname in our4 and elixir >= 5:
                    return(sname)
                else:
                    return None
        
    for troop in my_troops:
        if synergy(troop.name, my_tower.total_elixir, our4):
            deploy_list.list_.append((synergy(troop.name, my_tower.total_elixir, our4),(troop.position[0], 50)))



    
                
    
                

    
