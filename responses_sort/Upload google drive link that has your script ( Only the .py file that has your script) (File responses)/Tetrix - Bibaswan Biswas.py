

import random
from teams.helper_function import Troops, Utils

team_name = "Tetrix"
troops = [
    Troops.wizard, Troops.minion, Troops.prince, Troops.musketeer,
    Troops.dragon, Troops.skeleton, Troops.valkyrie, Troops.knight
]
deploy_list = Troops([])
team_signal = "Check"

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def deploy(arena_data: dict):
    """
    DON'T TEMPER DEPLOY FUNCTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    global team_signal
    print(team_signal)
    my_tower = arena_data["MyTower"]
    opp_tower = arena_data["OppTower"]
    opp_troops = arena_data["OppTroops"]
    my_troops = arena_data["MyTroops"]
    elixir = my_tower.total_elixir
    health = my_tower.health
    time = my_tower.game_timer
    opp_health=opp_tower.health

    deployable = my_tower.deployable_troops
    eli={
        "Wizard":5,"Minion":3,"Prince":5,"Musketeer":4,"Valkyrie":4,"Skeleton":3,"Knight":3,"Dragon":4
    }
    type_air = {"Minion", "Dragon", "Balloon"}
    type_ground = {"Prince", "Knight", "Barbarian", "Archer", "Skeleton", "Valkyrie", "Musketeer", "Giant", "Wizard"}
    air={"Archer","Minion","Dragon","Musketeer","Wizard"}
    ground={"Wizard","Minion","Prince","Musketeer","Valkyrie","Skeleton","Knight","Dragon"}

    # Identify Opponent Troops
    opp = {troop.uid: [troop.name, troop.position, troop.health, troop.type] for troop in opp_troops}
    my = {troop.uid: [troop.name, troop.position, troop.health] for troop in my_troops}
    nameop=[troop.name for troop in opp_troops]
    if "Valkyrie" not in nameop and "Wizard" not in nameop and "Dragon" not in nameop:
       if "Dragon" in deployable:
        deploy_list.deploy_dragon((25,50))
       elif "Skeleton" in deployable:
           deploy_list.deploy_skeleton((25,50))

    def defend_tower():
        for counter in ["Wizard","Dragon","Musketeer","Minion","Knight"]:
            if counter in deployable and eli[counter]<=elixir:
                getattr(deploy_list, f"deploy_{counter.lower()}")((0,0))
                
    def defend_troop(opp_name,opp_pos):
                dep=1
                deploy_x, deploy_y = opp_pos
                if opp_name == "Archer":
                    for counter in ["Knight", "Valkyrie","Dragon","Skeleton"]:
                        if counter in deployable and eli[counter]<=my_tower.total_elixir:
                            getattr(deploy_list, f"deploy_{counter.lower()}")((deploy_x,min(50,deploy_y)))
                            break
                        else:
                            dep=0
                elif opp_name == "Minion":
                    for counter in ["Wizard","Dragon","Musketeer", "Minion"]:
                        if counter in deployable and eli[counter]<=my_tower.total_elixir:
                            deploy_x, deploy_y = opp_pos
                            if counter == "Musketeer" and eli[counter]<=my_tower.total_elixir:  # Deploy at a safe distance
                                deploy_y = min(50,max(deploy_y - 12, 5))  # Keeping it at least 12 units away
                            getattr(deploy_list, f"deploy_{counter.lower()}")((deploy_x, deploy_y))
                            break
                        else:
                            dep=0  

                elif opp_name == "Knight":
                    for counter in ["Knight","Valkyrie","Musketeer","Prince"]:
                        if counter in deployable and eli[counter]<=my_tower.total_elixir:
                            deploy_x, deploy_y = opp_pos
                            if counter == "Musketeer":  # Deploy at a safe distance
                                deploy_y = min(50,max(deploy_y - 12, 5))
                            getattr(deploy_list, f"deploy_{counter.lower()}")((deploy_x, deploy_y))
                            break
                        else:
                            dep=0
                elif opp_name=="Skeleton":
                    deploy_x, deploy_y = opp_pos
                    if "Valkyrie" in deployable and my_tower.total_elixir>=4:
                        deploy_list.deploy_valkyrie((deploy_x,min(50,deploy_y)))
                    elif "Dragon" in deployable and my_tower.total_elixir>=4:
                        deploy_list.deploy_dragon((deploy_x,min(50,max(deploy_y - 7,0))))
                    elif "Minion" in deployable and my_tower.total_elixir>=4:
                        deploy_list.deploy_minion((deploy_x,min(50,max(deploy_y-4))))
                    elif "Wizard" in deployable and my_tower.total_elixir>=5:
                        deploy_list.deploy_wizard((deploy_x,min(50,max(deploy_y-10,0))))
                    elif "Skeleton" in deployable and my_tower.total_elixir>=3:
                        deploy_list.deploy_skeleton((deploy_x,min(50,deploy_y))) 
                    else:
                            dep=0
                elif opp_name =="Dragon":
                    deploy_x, deploy_y = opp_pos
                    if "Musketeer" in deployable and my_tower.total_elixir>=4:
                        deploy_list.deploy_musketeer((deploy_x,min(50,max(deploy_y - 12,0))))
                    elif "Dragon" in deployable and my_tower.total_elixir>=4:
                        deploy_list.deploy_dragon((deploy_x,min(50,deploy_y)))
                    elif "Wizard" in deployable and my_tower.total_elixir>=5:
                        deploy_list.deploy_wizard((deploy_x,min(50,max(deploy_y-10,0))))
                    elif "Minion" in deployable:
                        deploy_list.deploy_minion((deploy_x,min(50,deploy_y)))
                    else:
                        dep=0
                elif opp_name =="Valkyrie":
                    deploy_x, deploy_y=opp_pos
                    if "Prince" in deployable and my_tower.total_elixir>=5 :
                        deploy_list.deploy_prince((deploy_x,min(50,deploy_y)))
                    elif "Dragon" in deployable and my_tower.total_elixir>=4:
                        deploy_list.deploy_dragon((deploy_x,min(50,max(deploy_y - 7,0))))
                    elif "Musketeer" in deployable and my_tower.total_elixir>=4:
                        deploy_list.deploy_musketeer((deploy_x,min(50,max(deploy_y - 12,0))))
                    elif "Valkyrie" in deployable and my_tower.total_elixir>=4:
                        deploy_list.deploy_valkyrie((deploy_x,min(50,deploy_y)))
                    elif "Wizard" in deployable and my_tower.total_elixir>=5:
                        deploy_list.deploy_wizard((deploy_x,min(50,max(deploy_y - 10,0))))
                    
                    else:
                            dep=0
                elif opp_name == "Musketeer":
                    for counter in ["Knight", "Valkyrie", "Musketeer","Wizard","Dragon"]:
                        if counter in deployable and eli[counter]<=my_tower.total_elixir:
                            getattr(deploy_list, f"deploy_{counter.lower()}")((deploy_x,min(50,deploy_y)))
                            break
                        else:
                            dep=0
                elif opp_name == "Giant" :
                  if deploy_y<=50:
                    for counter in ["Skeleton","Minion","Wizard","Musketeer","Dragon"]:
                        if counter in deployable and eli[counter]<=my_tower.total_elixir:
                            if counter == "Musketeer" or counter == "Wizard":  # Deploy at a safe distance
                                deploy_y = min(50,max(deploy_y - 12, 5))
                            getattr(deploy_list, f"deploy_{counter.lower()}")((deploy_x,min(50,deploy_y)))
                            break
                        else:
                            dep=0
                elif opp_name == "Prince":
                    deploy_x, deploy_y=opp_pos
                    if "Skeleton" in deployable and my_tower.total_elixir>=3:
                        deploy_list.deploy_skeleton((deploy_x,min(50,deploy_y)))
                    elif "Minion" in deployable and my_tower.total_elixir>=4:
                        deploy_list.deploy_minion((deploy_x,min(50,max(deploy_y-4,0))))
                    elif "Wizard" in deployable and my_tower.total_elixir>=5 :
                        deploy_list.deploy_wizard((deploy_x,min(50,max(deploy_y - 10,0))))
                    elif "Knight" in deployable and my_tower.total_elixir>=3:
                        deploy_list.deploy_knight((deploy_x,min(50,deploy_y)))
                    elif "Valkyrie" in deployable and my_tower.total_elixir>=4:
                        deploy_list.deploy_valkyrie((deploy_x,min(50,deploy_y)))
                    elif "Musketeer" in deployable and my_tower.total_elixir>=4:
                        deploy_list.deploy_musketeer((deploy_x,min(50,max(deploy_y - 12,0))))
                    elif "Dragon" in deployable and my_tower.total_elixir>=4:
                        deploy_list.deploy_dragon((deploy_x,min(50,max(deploy_y - 7,0))))
                    else:
                            dep=0
                elif opp_name == "Barbarian":
                    deploy_x, deploy_y=opp_pos
                    if "Valkyrie" in deployable and my_tower.total_elixir>=4:
                        deploy_list.deploy_valkyrie((deploy_x,min(50,deploy_y)))
                    elif "Wizard" in deployable and my_tower.total_elixir>=5:
                        deploy_list.deploy_wizard((deploy_x,min(50,max(deploy_y - 10,0))))
                    elif "Skeleton" in deployable and my_tower.total_elixir>=3:
                        deploy_list.deploy_skeleton((deploy_x,min(50,deploy_y)))
                    elif "Dragon" in deployable and my_tower.total_elixir>=4:
                        deploy_list.deploy_dragon((deploy_x,min(50,max(deploy_y-7,0))))
                    elif "Minion" in deployable:
                        deploy_list.deploy_minion((deploy_x,min(50,max(deploy_y-4,0))))
                    else:
                            dep=0
                elif opp_name == "Wizard":
                    deploy_x, deploy_y = opp_pos
                    if "Prince" in deployable and my_tower.total_elixir>=5:
                        deploy_list.deploy_prince((deploy_x,min(50,deploy_y)))
                    elif "Wizard" in deployable and my_tower.total_elixir>=5:
                        deploy_list.deploy_wizard((deploy_x,min(50,max(deploy_y - 10,0))))
                    elif "Valkyrie" in deployable and my_tower.total_elixir>=4:
                        deploy_list.deploy_valkyrie((deploy_x,min(50,deploy_y)))
                    elif "Knight" in deployable and my_tower.total_elixir>=3:
                        deploy_list.deploy_knight((deploy_x,min(50,deploy_y)))
                    elif "Musketeer" in deployable and my_tower.total_elixir>=4:
                        deploy_list.deploy_musketeer((deploy_x,min(50,deploy_y)))
                    else:
                            dep=0
                elif opp_name == "Balloon":
                    deploy_x, deploy_y = opp_pos
                    if "Minion" in deployable:
                        deploy_list.deploy_minion((deploy_x,min(50,max(deploy_y-4,0))))
                    elif "Musketeer" in deployable and my_tower.total_elixir>=4:
                        deploy_list.deploy_musketeer((deploy_x,min(50,max(deploy_y-12,0))))
                    elif "Dragon" in deployable and my_tower.total_elixir>=4:
                        deploy_list.deploy_dragon((deploy_x,min(50,max(deploy_y-7,0))))
                    elif "Wizard" in deployable and my_tower.total_elixir>=5:
                        deploy_list.deploy_wizard((deploy_x,min(50,deploy_y)))
                    else:
                            dep=0
                if dep ==0:
                    deploy_list.list_.append((arena_data["MyTower"].deployable_troops[0],opp_pos))
    def attack():
     global team_signal
     if team_signal in ["PrinceWizard", "superattack"]:
        if "Prince" in deployable and my_tower.total_elixir >=5 and ("Wizard" in deployable or "Dragon" in deployable):
            deploy_list.deploy_prince((15,50))
            team_signal = "Wizard"
        else:
            team_signal = "ValkyrieWizard"
     elif team_signal == "Wizard":
        if "Wizard" in deployable and my_tower.total_elixir >=5:
            deploy_list.deploy_wizard((15,40))
            team_signal = "Check"
        elif "Dragon" in deployable and my_tower.total_elixir >=4:
            deploy_list.deploy_dragon((15,40))
        elif "Skeleton" in deployable and my_tower.total_elixir >=3:
            deploy_list.deploy_skeleton((15,40))
        else:
            team_signal="Skeleton"
     elif team_signal == "ValkyrieWizard":
        if "Valkyrie" in deployable and my_tower.total_elixir >=3 and ("Skeleton" in deployable or "Minion" in deployable):
            deploy_list.deploy_knight((-20,50))
            team_signal = "Wizard"
     elif team_signal == "Skeleton":
        if "Dragon" in deployable:
            deploy_list.deploy_dragon((-20,50))
        if "Skeleton" in deployable and my_tower.total_elixir >=3:
            deploy_list.deploy_skeleton((-20,40))
            team_signal = "Check"
        elif "Minion" in deployable and my_tower.total_elixir >=3:
            deploy_list.deploy_minion((-20,40))
            team_signal = "Check"
    def superattack():
        global team_signal
        for counter in ["Prince","Wizard","Dragon","Valkyrie"]:
            if counter in deployable:
                getattr(deploy_list, f"deploy_{counter.lower()}")((random.randint(-25,25),50))
        if(team_signal=="superattack"):
            team_signal="phase2"
        elif(team_signal=="phase2"):
            team_signal="Check"
    if team_signal in ["Wizard","ValkyrieSkeleton","Skeleton","PrinceWizard"]:
            attack()
    if(time<5) :
        superattack()
    if(True):
        defending_found = False
        for opp_uid, (opp_name, opp_pos, opp_health, opp_type) in opp.items():
            opp_x, opp_y = opp_pos
        # If the opponent troop is on my side (y < 50)
            

            # Check if I have a defending troop within radius 15
            for my_uid, (my_name, my_pos, my_health) in my.items():
                my_x, my_y = my_pos
                if Utils.calculate_distance(opp_pos, my_pos, type_troop=False) <= 5 and (opp_type=="ground" or (opp_type=="air" and my_name in air)):
                    defending_found = True
                    break  # Stop checking if we already have a defender
            if defending_found== False:
                if len(opp)>len(my) or opp_y<40 :
                    defend_tower()
                else:
                    defend_troop(opp_name,opp_pos)
        if len(opp)<3:
            if(team_signal=="phase2"):
                superattack()
            else:
                team_signal="superattack"
                superattack()
        elif (defending_found==True or len(opp)<=5)and team_signal==("Check" or "superattack"):
            team_signal="PrinceWizard"
        attack()


            
    

                