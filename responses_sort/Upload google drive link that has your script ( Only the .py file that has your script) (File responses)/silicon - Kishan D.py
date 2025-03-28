# this is the script in development

from teams.helper_function import Troops, Utils

team_name = "Silicon"
troops = [
    Troops.wizard, Troops.skeleton, Troops.knight, Troops.dragon,
    Troops.archer, Troops.minion, Troops.prince, Troops.valkyrie
]
deploy_list = Troops([])
team_signal = ""

def deploy(arena_data: dict):
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    global team_signal
    my_tower = arena_data["MyTower"]
    my_troops = arena_data["MyTroops"]
    opp_tower = arena_data["OppTower"]
    opp_troops = arena_data["OppTroops"]
    troops_data = Troops.troops_data

    # converting team_signal to list to extract opponent troops
    # in team_signal after the code m, we store troop we need to deploy
    elements = team_signal.split(',')
    current_opp_troops = []
    for element in elements:
        if element is 'm':
            break
        current_opp_troops.append(element)

    # check if opponent deployed new troops
    for troop in opp_troops:
        if troop.name not in current_opp_troops:
            current_opp_troops.append(troop.name)


    #take info from prev deployment
    #using team_signal
    #for example after giant
    #deploy wizard or pince
    troop_to_deploy = ''

    #analyze opponent's troops

    #check troops available

    # find troops in range of my_tower
    # opp_troop_in is a dict which
    # keeps count of opponent troops inside my_tower rangegit 
    # opp_troop_in = {}
    # opp_troop_near = {}
    # for troop in opp_troops:
    #     # if Utils.is_in_range(troop, my_tower, my_tower.attack_range):
    #     if troop.position[1] < 50:
    #         if troop.name in opp_troop_in:
    #             opp_troop_in[troop.name] += 1
    #         else:
    #             opp_troop_in[troop.name] = 1

    # for troop in opp_troops:
    #     if troop.position[1] < 25:
    #         if troop.name in opp_troop_near:
    #             opp_troop_near[troop.name] += 1
    #         else:
    #             opp_troop_near[troop.name] = 1

    def opp_troops_in(y):
        opp_in_y = []
        for troop in opp_troops:
            if troop.position[1] < y:
                if troop.name not in opp_in_y:
                    opp_in_y.append(troop.name)
        return opp_in_y
    
    opp_right = []
    for troop in opp_troops:
        if troop.type == "ground" and troop.position[1] > 50 and troop.position[0] > 5:
            if troop.name not in opp_right:
                opp_right.append(troop.name)
    opp_left = []
    for troop in opp_troops:
        if troop.type == "ground" and troop.position[1] > 50 and troop.position[0] < -5:
            if troop.name not in opp_left:
                opp_left.append(troop.name)

    opp_box = []
    for troop in opp_troops:
        if troop.position[0] > -15 and troop.position[0] < 15 and troop.position[1] > 50 and troop.position[1] < 65:
            if troop.name not in opp_box:
                opp_box.append(troop.name)
    


    opp_in_50 = opp_troops_in(50)
    opp_in_45 = opp_troops_in(45)
    opp_in_40 = opp_troops_in(40)
    opp_in_30 = opp_troops_in(30)
    opp_in_25 = opp_troops_in(25)
    opp_in_20 = opp_troops_in(20)

    # analyze opp_troops_in

    # function to check if a troop is deployable
    def deployable(troop):
        if troop in my_tower.deployable_troops:
            return my_tower.total_elixir >= troops_data[troop].elixir

    # convert current_opp_troops and troop to be deployed
    # back to team_signal
    team_signal = ""
    for troop in current_opp_troops:
        team_signal += troop + ','
    team_signal += 'm,'
    team_signal += troop_to_deploy + ','

    # final decision

    # first deployment (make it more strategic)
    if my_tower.game_timer == 0:
        if deployable(Troops.wizard):
            deploy_list.list_.append((Troops.wizard, (0,50)))
            if deployable(Troops.dragon):
                deploy_list.list_.append((Troops.dragon, (0,50)))
            elif deployable(Troops.prince):
                deploy_list.list_.append((Troops.prince, (0,40)))
            elif deployable(Troops.minion):
                deploy_list.list_.append((Troops.minion, (0,40)))
            else:
                deploy_list.list_.append((my_tower.deployable_troops[0], (0,15)))
        elif deployable(Troops.dragon):
            deploy_list.list_.append((Troops.dragon, (0, 50)))
            if deployable(Troops.wizard):
                deploy_list.list_.append((Troops.wizard, (0,50)))
            elif deployable(Troops.prince):
                deploy_list.list_.append((Troops.prince, (0,50)))
            elif deployable(Troops.minion):
                deploy_list.list_.append((Troops.minion, (0,40)))
            else:
                deploy_list.list_.append((my_tower.deployable_troops[0], (0,15)))
        else:
            deploy_list.list_.append((my_tower.deployable_troops[0], (0,15)))

    # if my_tower is in danger analyze and protect

    # i didnt check if troop is deployable or not
    # add code to check

    def defend (opponent, our_troops):
        if opponent in opp_in_50:
            for troop in opp_troops:
                if troop.name is opponent:
                    opp = troop
                    position = troop.position
            flag = True
            for x in my_troops:
                if Utils.calculate_distance(x, opp) < x.size + opp.size + 0.5:
                    flag = False
            if flag:
                if deployable(our_troops[0]):
                    deploy_list.list_.append((our_troops[0], position))
                elif opponent in opp_in_45:
                    if deployable(our_troops[1]):
                        deploy_list.list_.append((our_troops[1], position))
                    elif opponent in opp_in_40:
                        if deployable(our_troops[2]):
                            deploy_list.list_.append((our_troops[2], position))
                        elif opponent in opp_in_30:
                            if deployable(our_troops[3]):
                                deploy_list.list_.append((our_troops[3], position))
                            elif opponent in opp_in_25:
                                if deployable(our_troops[4]):
                                    deploy_list.list_.append((our_troops[4], position))
                                else:
                                    deploy_list.list_.append(((my_tower.deployable_troops[0] 
                                                               if my_tower.deployable_troops[0] is not Troops.prince 
                                                               else my_tower.deployable_troops[1]), (0, 15)))
    
    # if threat is near defend near origin
    # manage the threat correctly
    
    # if len(opp_in_20) > 0:
    #     if Troops.wizard in opp_in_20 or Troops.giant in opp_in_20 or Troops.prince in opp_in_20 or Troops.balloon in opp_in_20 or Troops.dragon in opp_in_20 or Troops.valkyrie in opp_in_20:
    #         if deployable(Troops.wizard):
    #             deploy_list.deploy_wizard((0, 10))
    #         elif deployable(Troops.dragon):
    #             deploy_list.deploy_dragon((0, 10))
    #         elif deployable(Troops.minion):
    #             deploy_list.deploy_minion((0, 15))
    #         else:
    #             deploy_list.list_.append((my_tower.deployable_troops[0], (0, 15)))
    #     else:
    #         if deployable(Troops.minion):
    #             deploy_list.deploy_minion((0, 15))
    #         elif deployable(Troops.minion):
    #             deploy_list.deploy_minion((0, 15))
    #         elif deployable(Troops.skeleton):
    #             deploy_list.deploy_skeleton((0, 17))
    #         else:
    #             deploy_list.list_.append((my_tower.deployable_troops[0], (0, 15)))

    if len(opp_in_20) > 0:
        deploy_list.deploy_wizard((0, 10))
    




    if my_tower.total_elixir > (7 if my_tower.game_timer < 1200 else 5):
        if deployable(Troops.wizard):
            if len(opp_box) > 0:
                deploy_list.deploy_wizard((0, 45))
            else:
                deploy_list.deploy_wizard((0, 50))
            if my_tower.game_timer > 1200:
                if deployable(Troops.minion):
                    deploy_list.deploy_minion((0, 45))
                elif deployable(Troops.archer):
                    deploy_list.deploy_archer((0, 45))
        elif deployable(Troops.prince):
            if len(opp_left) > 0:
                if len(opp_right) > 0:
                    pass
                else:
                    deploy_list.deploy_prince((20, 50))
            else:
                deploy_list.deploy_prince((-20, 50))
        elif deployable(Troops.dragon):
            deploy_list.deploy_dragon((0, 50))
        if deployable(Troops.knight) and deployable(Troops.archer) and my_tower.game_timer > 1200:
            deploy_list.deploy_knight((0, 50))
            deploy_list.deploy_archer((0, 45))

    defend(Troops.wizard, [Troops.knight, Troops.valkyrie, Troops.dragon, Troops.wizard, Troops.valkyrie])
    defend(Troops.valkyrie, [Troops.minion, Troops.dragon, Troops.knight, Troops.valkyrie, Troops.valkyrie])
    defend(Troops.dragon, [Troops.minion, Troops.archer, Troops.dragon, Troops.dragon, Troops.wizard])
    defend(Troops.minion, [Troops.archer, Troops.minion, Troops.minion, Troops.dragon, Troops.wizard])
    defend(Troops.giant, [Troops.skeleton, Troops.knight, Troops.minion, Troops.dragon, Troops.prince])
    defend(Troops.prince, [Troops.skeleton, Troops.valkyrie, Troops.knight, Troops.minion, Troops.dragon])
    defend(Troops.knight, [Troops.minion, Troops.minion, Troops.dragon, Troops.knight, Troops.valkyrie])
    defend(Troops.skeleton, [Troops.valkyrie, Troops.minion, Troops.dragon, Troops.wizard, Troops.minion])
    defend(Troops.archer, [Troops.skeleton, Troops.valkyrie, Troops.minion, Troops.dragon, Troops.wizard])
    defend(Troops.balloon, [Troops.dragon, Troops.minion, Troops.archer, Troops.archer, Troops.wizard])
    defend(Troops.barbarian, [Troops.dragon, Troops.minion, Troops.valkyrie, Troops.skeleton, Troops.skeleton])

    # check team_signal to deploy any of our troop


    # else continue with the strategy

# i got to know what is the mistake we are doing
# we found out a best troop to tackle the threat at 50 itself
# and there itself if that best troop if not available
# we were trying to choose other more valuable troops
# but in real game we choose lower options when the troop is very near like 25
# so we will use elixir in attack instead of wasting it in more valuable alternatives initially itself