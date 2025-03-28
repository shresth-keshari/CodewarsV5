from teams.helper_function import Troops, Utils
import numpy as np

team_name = "Rutu"
troops = [Troops.prince,Troops.minion,Troops.wizard,Troops.skeleton,Troops.dragon,Troops.barbarian,Troops.valkyrie,Troops.archer]
deploy_list = Troops([])
team_signal = ""

def deploy(arena_data:dict):
    """
    DON'T TEMPER DEPLOY FUCNTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def opp_troop_names(arena_data:dict):
    troop_names = {}
    for troop in arena_data["OppTroops"]:
        troop_names[troop.name] = troop
    return troop_names


#        DEFENSIVE TACTICS
# def defense(arena_data:dict, troop_number:int):


def general_tackle(arena_data, position):
    pause = True
    deployable = arena_data["MyTower"].deployable_troops
    if arena_data["MyTower"].total_elixir >= 5 and "Wizard" in deployable:
        deploy_list.deploy_wizard((position[0], position[1]-15))
        pause = False
    elif arena_data["MyTower"].total_elixir >= 4 and "Valkyrie" in deployable:
        deploy_list.deploy_valkyrie(position)
        pause = False
    elif arena_data["MyTower"].total_elixir >= 4 and "Dragon" in deployable:
        deploy_list.deploy_dragon(position)
        pause = False
    elif arena_data["MyTower"].total_elixir >= 3 and "Minion" in deployable:
        deploy_list.deploy_minion(position)
        pause = False
    elif arena_data["MyTower"].total_elixir >= 4:
        deploy_list.list_.append((arena_data["MyTower"].deployable_troops[0], position))
        pause = False

    return pause


def tackle_archer(arena_data):
    opp_troops_dict = opp_troop_names(arena_data)
    my_tower = arena_data["MyTower"]
    deployable = my_tower.deployable_troops
    pause = False

    if "Archer" in opp_troops_dict:
        troop = opp_troops_dict["Archer"]
        position = troop.position

        
        if Troops.barbarian in deployable:
            pause = True
            if my_tower.total_elixir >= 3:
                deploy_list.deploy_barbarian(position)
                pause = False
        elif Troops.valkyrie in deployable:
            pause = True
            if my_tower.total_elixir >= 4:
                deploy_list.deploy_valkyrie(position)
                pause = False
        elif Troops.dragon in deployable:
            pause = True
            if my_tower.total_elixir >= 4:
                deploy_list.deploy_dragon((position[0], position[1] - 15))
                pause = False
        elif Troops.wizard in deployable:
            pause = True
            if my_tower.total_elixir >= 5:
                deploy_list.deploy_wizard((position[0], position[1] - 15))
                pause = False
        else:
            pause = general_tackle(arena_data, position)

    return pause

def tackle_minion(arena_data):
    opp_troops_dict = opp_troop_names(arena_data)
    my_tower = arena_data["MyTower"]
    deployable = my_tower.deployable_troops
    pause = False

    if "Minion" in opp_troops_dict:
        troop = opp_troops_dict["Minion"]
        position = troop.position
        
        if Troops.dragon in deployable:
            pause = True
            if my_tower.total_elixir >= 4:
                deploy_list.deploy_dragon((position[0], position[1] - 15))
                pause = False
        elif Troops.wizard in deployable:
            pause = True
            if my_tower.total_elixir >= 5:
                deploy_list.deploy_wizard((position[0], position[1] - 15))
                pause = False
        else:
            pause = general_tackle(arena_data, position)

            return pause

def tackle_knight(arena_data):
    opp_troops_dict = opp_troop_names(arena_data)
    my_tower = arena_data["MyTower"]
    deployable = my_tower.deployable_troops
    pause = False

    if "Knight" in opp_troops_dict:
        troop = opp_troops_dict["Knight"]
        position = troop.position

        if Troops.minion in deployable:
            pause = True
            if my_tower.total_elixir >= 3:
                deploy_list.deploy_minion(position)
                pause = False
        elif Troops.barbarian in deployable:
            pause = True
            if my_tower.total_elixir >= 3:
                deploy_list.deploy_barbarian(position)
                pause = False
        elif Troops.archer in deployable:
            pause = True
            if my_tower.total_elixir >= 3:
                deploy_list.deploy_archer((position[0], position[1] - 15))
                pause = False
        elif Troops.dragon in deployable:
            pause = True
            if my_tower.total_elixir >= 4:
                deploy_list.deploy_dragon((position[0], position[1] - 15))
                pause = False
        else:
            pause = general_tackle(arena_data, position)

        return pause

def tackle_skeleton(arena_data):
    opp_troops_dict = opp_troop_names(arena_data)
    my_tower = arena_data["MyTower"]
    deployable = my_tower.deployable_troops
    pause = False

    if "Skeleton" in opp_troops_dict:
        troop = opp_troops_dict["Skeleton"]
        position = troop.position

        if Troops.valkyrie in deployable:
            pause = True
            if my_tower.total_elixir >= 4:
                deploy_list.deploy_valkyrie(position)
                pause = False
        elif Troops.dragon in deployable:
            pause = True
            if my_tower.total_elixir >= 4:
                deploy_list.deploy_dragon((position[0], position[1] - 15))
                pause = False
        elif Troops.wizard in deployable:
            pause = True
            if my_tower.total_elixir >= 5:
                deploy_list.deploy_wizard((position[0], position[1] - 15))
                pause = False
        else:
            pause = general_tackle(arena_data, position)
        
        return pause

def tackle_dragon(arena_data):
    opp_troops_dict = opp_troop_names(arena_data)
    my_tower = arena_data["MyTower"]
    deployable = my_tower.deployable_troops
    pause = False

    if "Dragon" in opp_troops_dict:
        troop = opp_troops_dict["Dragon"]
        position = troop.position

        if Troops.dragon in deployable:
            pause = True
            if my_tower.total_elixir >= 4:
                deploy_list.deploy_dragon(position)
                pause = False
        elif Troops.wizard in deployable:
            pause = True
            if my_tower.total_elixir >= 5:
                deploy_list.deploy_wizard((position[0], position[1] - 15))
                pause = False
        else:
            pause = general_tackle(arena_data, position)
        
        return pause

def tackle_valkyrie(arena_data):
    opp_troops_dict = opp_troop_names(arena_data)
    my_tower = arena_data["MyTower"]
    deployable = my_tower.deployable_troops
    pause = False

    if "Valkyrie" in opp_troops_dict:
        troop = opp_troops_dict["Valkyrie"]
        position = troop.position
        
        if Troops.minion in deployable:
            pause = True
            if my_tower.total_elixir >= 3:
                deploy_list.deploy_minion(position)
                pause = False
        elif Troops.dragon in deployable:
            pause = True
            if my_tower.total_elixir >= 4:
                deploy_list.deploy_dragon((position[0], position[1] - 15))
                pause = False
        elif Troops.wizard in deployable:
            pause = True
            if my_tower.total_elixir >= 5:
                deploy_list.deploy_wizard((position[0], position[1] - 15))
                pause = False
        else:
            pause = general_tackle(arena_data, position)
        
        return pause

def tackle_musketeer(arena_data):
    opp_troops_dict = opp_troop_names(arena_data)
    my_tower = arena_data["MyTower"]
    deployable = my_tower.deployable_troops
    pause = False

    if "Musketeer" in opp_troops_dict:
        troop = opp_troops_dict["Musketeer"]
        position = troop.position

        if Troops.barbarian in deployable:
            pause = True
            if my_tower.total_elixir >= 3:
                deploy_list.deploy_barbarian(position)
                pause = False
        elif Troops.valkyrie in deployable:
            pause = True
            if my_tower.total_elixir >= 4:
                deploy_list.deploy_valkyrie(position)
                pause = False
        elif Troops.dragon in deployable:
            pause = True
            if my_tower.total_elixir >= 4:
                deploy_list.deploy_dragon((position[0], position[1] - 15))
                pause = False
        else:
            pause = general_tackle(arena_data, position)
        
        return pause

def tackle_giant(arena_data):
    opp_troops_dict = opp_troop_names(arena_data)
    my_tower = arena_data["MyTower"]
    deployable = my_tower.deployable_troops
    pause = False

    if "Giant" in opp_troops_dict:
        troop = opp_troops_dict["Giant"]
        position = troop.position

        if Troops.minion in deployable:
            pause = True
            if my_tower.total_elixir >= 3:
                deploy_list.deploy_minion(position)
                pause = False
        elif Troops.barbarian in deployable:
            pause = True
            if my_tower.total_elixir >= 3:
                deploy_list.deploy_barbarian(position)
                pause = False
        elif Troops.wizard in deployable:
            pause = True
            if my_tower.total_elixir >= 5:
                deploy_list.deploy_wizard((position[0], position[1] - 15))
                pause = False
        else:
            pause = general_tackle(arena_data, position)
        
        return pause

def tackle_prince(arena_data):
    opp_troops_dict = opp_troop_names(arena_data)
    my_tower = arena_data["MyTower"]
    deployable = my_tower.deployable_troops
    pause = False

    if "Prince" in opp_troops_dict:
        troop = opp_troops_dict["Prince"]
        position = troop.position

        if Troops.minion in deployable:
            pause = True
            if my_tower.total_elixir >= 3:
                deploy_list.deploy_minion(position)
                pause = False
        elif Troops.barbarian in deployable:
            pause = True
            if my_tower.total_elixir >= 3:
                deploy_list.deploy_barbarian(position)
                pause = False
        elif Troops.wizard in deployable:
            pause = True
            if my_tower.total_elixir >= 5:
                deploy_list.deploy_wizard((position[0], position[1] - 15))
                pause = False
        elif Troops.dragon in deployable:
            pause = True
            if my_tower.total_elixir >= 4:
                deploy_list.deploy_dragon((position[0], position[1] - 15))
                pause = False
        else:
            pause = general_tackle(arena_data, position)
        
        return pause

def tackle_barbarian(arena_data):
    opp_troops_dict = opp_troop_names(arena_data)
    my_tower = arena_data["MyTower"]
    deployable = my_tower.deployable_troops
    pause = False

    if "Barbarian" in opp_troops_dict:
        troop = opp_troops_dict["Barbarian"]
        position = troop.position

        if Troops.valkyrie in deployable:
            pause = True
            if my_tower.total_elixir >= 4:
                deploy_list.deploy_valkyrie(position)
                pause = False
        elif Troops.dragon in deployable:
            pause = True
            if my_tower.total_elixir >= 4:
                deploy_list.deploy_dragon((position[0], position[1] - 15))
                pause = False
        elif Troops.wizard in deployable:
            pause = True
            if my_tower.total_elixir >= 5:
                deploy_list.deploy_wizard((position[0], position[1] - 15))
                pause = False
        else:
            pause = general_tackle(arena_data, position)
        
        return pause

def tackle_balloon(arena_data):
    opp_troops_dict = opp_troop_names(arena_data)
    my_tower = arena_data["MyTower"]
    deployable = my_tower.deployable_troops
    pause = False

    if "Balloon" in opp_troops_dict:
        troop = opp_troops_dict["Balloon"]
        position = troop.position

        
        if Troops.minion in deployable:
            pause = True
            if my_tower.total_elixir >= 3:
                deploy_list.deploy_minion(position)
                pause = False
        elif Troops.archer in deployable:
            pause = True
            if my_tower.total_elixir >= 3:
                deploy_list.deploy_archer((position[0], position[1] - 15))
                pause = False
        elif Troops.wizard in deployable:
            pause = True
            if my_tower.total_elixir >= 5:
                deploy_list.deploy_wizard((position[0], position[1] - 15))
                pause = False
        elif Troops.dragon in deployable:
            pause = True
            if my_tower.total_elixir >= 4:
                deploy_list.deploy_dragon((position[0], position[1] - 15))
                pause = False
        else:
            pause = general_tackle(arena_data, position)
        
        return pause

def tackle_wizard(arena_data):
    opp_troops_dict = opp_troop_names(arena_data)
    my_tower = arena_data["MyTower"]
    deployable = my_tower.deployable_troops
    pause = False

    if "Wizard" in opp_troops_dict:
        troop = opp_troops_dict["Wizard"]
        position = troop.position

        if Troops.prince in deployable:
            pause = True
            if my_tower.total_elixir >= 5:
                deploy_list.deploy_prince(position)
                pause = False
        elif Troops.valkyrie in deployable:
            pause = True
            if my_tower.total_elixir >= 4:
                deploy_list.deploy_valkyrie(position)
                pause = False
        elif Troops.wizard in deployable:
            pause = True
            if my_tower.total_elixir >= 5:
                deploy_list.deploy_wizard((position[0], position[1] - 15))
                pause = False
        else:
            pause = general_tackle(arena_data, position)
        
        return pause





def logic(arena_data:dict):
    pause = False
    global team_signal
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    deployable = arena_data["MyTower"].deployable_troops
    

    pause = False
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    deployable = my_tower.deployable_troops

    # Delete those uids from team_signal which are no longer alive
    opp_names = [str(troop.name) for troop in opp_troops]
    for name in team_signal.split(","):
        if name not in opp_names:
            team_signal = team_signal.replace(name + ",", "")
        

    

    # Deploy Prince for defense when no enemy in our land
    prince_deployed = False
    if Troops.prince in deployable:
        enemy_in_our_land = False
        for troop in opp_troops:
            if troop.position[1]<50:
                enemy_in_our_land = True
                break
        if enemy_in_our_land == False and my_tower.total_elixir >= 9:
            deploy_list.deploy_prince((50,0))
            prince_deployed = True
        if prince_deployed and Troops.dragon in deployable:
            deploy_list.deploy_dragon((50,0))

    
    troops_list = ["Wizard", "Dragon", "Valkyrie", "Minion", "Balloon", "Prince", "Knight", "Musketeer", "Barbarian", "Skeleton", "Archer", "Giant"]

    troop_number = -1
    troop_name = ""

    if len(opp_troops) > 0:
        closest_troop = None
        min_position = 150
        for troop in opp_troops:
            if troop.position[1] < min_position and str(troop.name) not in team_signal.split(","):
                min_position = troop.position[1]
                closest_troop = troop
        if closest_troop is not None:          
            troop_number = troops_list.index(closest_troop.name)
            troop_name = closest_troop.name

    if troop_number == 0:
        pause = tackle_wizard(arena_data)
        if pause == False:
            team_signal = team_signal + "," + str(troop_name) + ","
            
    elif troop_number == 1:
        pause = tackle_dragon(arena_data)
        if pause == False:
            team_signal = team_signal + "," + str(troop_name) + ","
            
    elif troop_number == 2:
        pause = tackle_valkyrie(arena_data)
        if pause == False:
            team_signal = team_signal + "," + str(troop_name) + ","
            
    elif troop_number == 3:
        pause = tackle_minion(arena_data)
        if pause == False:
            team_signal = team_signal + "," + str(troop_name) + ","
            
    elif troop_number == 4:
        pause = tackle_balloon(arena_data)
        if pause == False:
            team_signal = team_signal + "," + str(troop_name) + ","
            
    elif troop_number == 5:
        pause = tackle_prince(arena_data)
        if pause == False:
            team_signal = team_signal + "," + str(troop_name) + ","
            
    elif troop_number == 6:
        pause = tackle_knight(arena_data)
        if pause == False:
            team_signal = team_signal + "," + str(troop_name) + ","
            
    elif troop_number == 7:
        pause = tackle_musketeer(arena_data)
        if pause == False:
            team_signal = team_signal + "," + str(troop_name) + ","
            
    elif troop_number == 8:
        pause = tackle_barbarian(arena_data)
        if pause == False:
            team_signal = team_signal + "," + str(troop_name) + ","
            
    elif troop_number == 9:
        pause = tackle_skeleton(arena_data)
        if pause == False:
            team_signal = team_signal + "," + str(troop_name) + ","
            
    elif troop_number == 10:
        pause = tackle_archer(arena_data)
        if pause == False:
            team_signal = team_signal + "," + str(troop_name) + ","
            
    elif troop_number == 11:
        pause = tackle_giant(arena_data)
        if pause == False:
            team_signal = team_signal + "," + str(troop_name) + ","
            
        
    #      OFFENSE
    if pause == False:

        

    # Deploy Prince to distract more than 3 troops
        if Troops.prince in deployable and (Troops.dragon in deployable or Troops.wizard in deployable):
            if "Giant" not in opp_troop_names(arena_data): #TODO: check that giant is not one of them
                pause = True
                x_list = []
                y_list = []
                for troop in opp_troops:
                    x_list.append(troop.position[0])
                    y_list.append(troop.position[1])
                x = np.mean(x_list)
                y = np.mean(y_list)
                prince_deployed = False
                my_prince = None
                if y < 50 and my_tower.total_elixir >= 5:
                    deploy_list.list_.append((Troops.prince,(x,y)))
                    prince_deployed = True

                if prince_deployed:
                    for troop in arena_data["MyTroops"]:
                        if troop.name == "Prince":
                            my_prince = troop
                            break
                    if my_prince is not None:
                        for troop in opp_troops:
                            if Utils.calculate_distance(troop, my_prince) <= 10:
                                if Troops.dragon in deployable and my_tower.total_elixir >= 4:
                                    deploy_list.list_.append((Troops.dragon,(x,y-2)))
                                    pause = False
                                elif Troops.wizard in deployable and my_tower.total_elixir >= 5:
                                    deploy_list.list_.append((Troops.wizard,(x,y-2)))
                                    pause = False

        # Deploy Skeleton for Offense
        if Troops.skeleton in deployable and my_tower.total_elixir >= 6:
            x_list = []
            y_list = []
            for troop in opp_troops:
                x_list.append(troop.position[0])
                y_list.append(troop.position[1])
            x = np.mean(x_list)
            y = np.mean(y_list)
            
            if x > 0:
                deploy_list.deploy_skeleton((-20, 50))
                
            else:
                deploy_list.deploy_skeleton((20, 50))
                
                        
        # Deploy wizard for Offense
        elif Troops.wizard in deployable and my_tower.total_elixir >= 8:
            x_list = []
            y_list = []
            for troop in opp_troops:
                x_list.append(troop.position[0])
                y_list.append(troop.position[1])
            x = np.mean(x_list)
            y = np.mean(y_list)
            
            if x > 0:
                deploy_list.deploy_wizard((-20, 50))
            else:
                deploy_list.deploy_wizard((20, 50))

        # Deploy everything at the end
        if my_tower.game_timer >= 1750:
            deploy_list.list_.append((arena_data["MyTower"].deployable_troops[0],(-12, 50)))
            deploy_list.list_.append((arena_data["MyTower"].deployable_troops[1],(12, 50)))
            deploy_list.list_.append((arena_data["MyTower"].deployable_troops[2],(-20, 50)))
            deploy_list.list_.append((arena_data["MyTower"].deployable_troops[3],(20, 50)))