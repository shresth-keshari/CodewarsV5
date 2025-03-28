from teams.helper_function import Troops, Utils
import random


team_name = "Code Mavericks"
troops = [Troops.prince,Troops.dragon,Troops.valkyrie,Troops.wizard,Troops.balloon,Troops.musketeer,Troops.knight,Troops.archer]
deploy_list = Troops([])
team_signal = ""

def deploy(arena_data:dict):
    """
    DON'T TEMPER DEPLOY FUCNTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data:dict):
    global team_signal

    for troop in arena_data["OppTroops"]:
        curr_enemies = [name.strip() for name in team_signal.split(",")] if team_signal else []
        if troop.name not in curr_enemies:
            team_signal = team_signal + ", " + troop.name if team_signal else troop.name

    air_opps = {"Minion", "Dragon", "Balloon"}
    ground_opps = {"Archer", "Knight", "Skeleton", "Valkyrie", "Musketeer", "Giant", "Prince", "Barbarian", "Wizard"}

    curr_enemies = [en.strip() for en in team_signal.split(",")]

    if not curr_enemies or arena_data["MyTower"].game_timer < 31:
        max_dps = 0
        for troop in arena_data["MyTower"].deployable_troops:
            if Troops.troops_data[troop].damage * Troops.troops_data[troop].attack_speed > max_dps:
                max_damage = Troops.troops_data[troop].damage * Troops.troops_data[troop].attack_speed

        iteration = 0
        for troop in arena_data["MyTower"].deployable_troops:
            if Troops.troops_data[troop].damage * Troops.troops_data[troop].attack_speed == max_dps:
                iteration = arena_data["MyTower"].deployable_troops.index(troop)
        if Troops.troops_data[arena_data["MyTower"].deployable_troops[iteration]].elixir <= arena_data["MyTower"].total_elixir:
            deploy_list.list_.append((arena_data["MyTower"].deployable_troops[iteration], (0,49)))
        else:
            deployableiter = 100
            deployablemaxdps = 0
            for troop in arena_data["MyTower"].deployable_troops:
                if Troops.troops_data[troop].damage * Troops.troops_data[troop].attack_speed > deployablemaxdps and Troops.troops_data[troop].elixir <= arena_data["MyTower"].total_elixir and Troops.troops_data[troop].target_type["ground"]:
                    deployableiter = arena_data["MyTower"].deployable_troops.index(troop)
                    deployablemaxd = Troops.troops_data[troop].damage * Troops.troops_data[troop].attack_speed
            if deployableiter != 100:
                deploy_list.list_.append((arena_data["MyTower"].deployable_troops[deployableiter], (random.randint(-25,25),49)))

    else:
        defx = 0
        defy = 100
        truth = 0
        opp_troop = ""
        for token in curr_enemies:
            for troop in arena_data["OppTroops"]:
                if token == troop.name and Utils.calculate_distance(troop.position , (0,0) , False ) < 30:
                    truth = 1
                    opp_troop = troop.name
                    break
        
        if truth:
            max_3dps = 0
            max_dps_troop = ""
            dpiter = 0
            for troop in arena_data["MyTower"].deployable_troops:
                if Troops.troops_data[troop].damage * Troops.troops_data[troop].attack_speed > max_3dps and Troops.troops_data[troop].elixir <= arena_data["MyTower"].total_elixir and Troops.troops_data[troop].target_type[Troops.troops_data[opp_troop].type]:
                    max_dps_troop = troop
                    max_3dps = Troops.troops_data[troop].damage * Troops.troops_data[troop].attack_speed
                    dpiter = arena_data["MyTower"].deployable_troops.index(troop)

            deploy_list.list_.append((arena_data["MyTower"].deployable_troops[dpiter], (random.randint(-15,15),0)))

        else:
            t1 = 0
            for troop in arena_data["MyTower"].deployable_troops:
                if troop == "Balloon":
                    t1 = 1
            t2 = 1
            for troop in curr_enemies:
                for token in arena_data["OppTroops"]:
                    if troop == token.name and  Utils.calculate_distance(token.position , (0,0) , False ) > 71:
                        t2 = 0
                        break
                break


            
            if t1 and arena_data["MyTower"].total_elixir >= Troops.troops_data["Balloon"].elixir and t2:
                for troop in arena_data["MyTower"].deployable_troops:
                    if troop.name == "Balloon":
                        deploy_list.list_.append((arena_data["MyTower"].deployable_troops[arena_data["MyTower"].deployable_troops.index(troop)], (random.randint(-25,25),49)))
            
            else:
                max_4dps = 0
                max_4dps_troop = ""



                for token in curr_enemies:
                    if Troops.troops_data[token].damage * Troops.troops_data[token].attack_speed > max_4dps:
                        max_damage = Troops.troops_data[token].damage * Troops.troops_data[token].attack_speed
                        max_4dps_troop = token
                
                tr_type = Troops.troops_data[max_4dps_troop].type
                iteration = 0
                max_damage = 0
                for troop in arena_data["MyTower"].deployable_troops:
                    if Troops.troops_data[troop].damage *  Troops.troops_data[troop].attack_speed > max_damage and Troops.troops_data[troop].elixir <= arena_data["MyTower"].total_elixir and Troops.troops_data[troop].target_type[tr_type]:
                        max_damage = Troops.troops_data[troop].damage *  Troops.troops_data[troop].attack_speed
                        iteration = arena_data["MyTower"].deployable_troops.index(troop)
                
                x = 0
                y = 0

                for troop in arena_data["OppTroops"]:
                    if troop.name == max_4dps_troop:
                        x = troop.position[0]
                        y = troop.position[1]
                
                if y >= 50:
                    y = 49

                deploy_list.list_.append((arena_data["MyTower"].deployable_troops[iteration], (x,y)))

                max_2d_troop = ""
                max_2damage = 0

                for token in curr_enemies:
                    if Troops.troops_data[token].damage * Troops.troops_data[token].attack_speed > max_2damage and Troops.troops_data[token].damage *Troops.troops_data[token].attack_speed != max_damage:
                        max_2damage = Troops.troops_data[token].damage *Troops.troops_data[token].attack_speed
                        max_2d_troop = token
                
                tr_type = Troops.troops_data[max_2d_troop].type
                iteration = 0
                max_2damage = 0
                for troop in arena_data["MyTower"].deployable_troops:
                    if Troops.troops_data[troop].damage *  Troops.troops_data[troop].attack_speed> max_2damage and Troops.troops_data[troop].elixir <= arena_data["MyTower"].total_elixir and Troops.troops_data[troop].target_type[tr_type]:
                        max_2damage = Troops.troops_data[troop].damage *  Troops.troops_data[troop].attack_speed
                        iteration = arena_data["MyTower"].deployable_troops.index(troop)
                
                x = 0
                y = 0

                for troop in arena_data["OppTroops"]:
                    if troop.name == max_2d_troop:
                        x = troop.position[0]
                        y = troop.position[1]
                
                if y >= 50:
                    y = 49

                deploy_list.list_.append((arena_data["MyTower"].deployable_troops[iteration], (x,y)))







            
            


            

        


        


        





        
