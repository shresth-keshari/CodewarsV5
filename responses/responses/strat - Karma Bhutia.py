from teams.helper_function import Troops, Utils

team_name = "momo.cyclone.petha.dhokla"
troops = [Troops.wizard,Troops.minion,Troops.archer,Troops.prince,Troops.dragon,Troops.knight,Troops.musketeer,Troops.valkyrie]
deploy_list = Troops([])
team_signal = "Wizard,Prince,Valkyrie,Knight"

def deploy(arena_data:dict):
    """
    DON'T TEMPER DEPLOY FUCNTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data:dict):
    global team_signal 
    strat = team_signal.strip(',')
    Opptroops = []
    oppdistances = []
    deployable = []
    combo = ["wizard","Dragon"]
    wizpos = 5
    flag = 5
    meelee= ["Valkyrie","Knight","Prince"]
    for i in range(len(arena_data["MyTower"].deployable_troops)): 
        deployable.append(arena_data["MyTower"].deployable_troops[i].strip())
    for i in range(len(deployable)):
        if (Troops.wizard == deployable[i]):
            wizpos = i
        if (Troops.knight == deployable[i]):
            flag = i
        if (Troops.valkyrie == deployable[i] ):
            flag = i 
        if (Troops.dragon == deployable[i]):
            flag = i 
    avgopdistance = 0.0 
    c=0
    for i in range(len(arena_data["OppTroops"])):
        Opptroops.append(arena_data["OppTroops"][i].name.strip())
        oppdistances.append(Utils.calculate_distance(arena_data["OppTroops"][i], arena_data["MyTower"]))
        avgopdistance += Utils.calculate_distance(arena_data["OppTroops"][i], arena_data["MyTower"])
    if(len(oppdistances)>0):
        avgopdistance /= len(oppdistances)
    no_of_opptroops = len(oppdistances)
    for i in range(len(Opptroops)):
        if(Opptroops[i] in combo):
            c+=1
    if(arena_data["MyTower"].health>arena_data["OppTower"].health):
        if(no_of_opptroops >= 3 and avgopdistance<70) or (Troops.wizard in Opptroops and avgopdistance<50):
            if ((flag != 5 and wizpos!=5) or (c==2 and flag!=5 )):
                deploy_list.list_.append((deployable[flag],(0,12)))
                deploy_list.deploy_wizard((5,0))
            elif (flag !=5):
                deploy_list.list_.append((deployable[flag],(12,2)))
                deploy_list.list_.append((deployable[0],(-12,2)))
            else :
                deploy_list.list_.append((deployable[0],(0,0)))
        elif(no_of_opptroops>=3 and avgopdistance<30):
            if(wizpos!=5):
                deploy_list.deploy_wizard((0,0))
            if(deployable[0] not in meelee or deployable[1] not in meelee):
                deploy_list.list_.append((deployable[0],(-25,10)))
                deploy_list.list_.append((deployable[1],(25,10)))
            
        elif (arena_data["MyTower"].game_timer > 120):
            deploy_list.list_.append((deployable[0],(-50,25)))
            deploy_list.list_.append((deployable[1],(50,25)))
        else:
            if(Troops.wizard in deployable):
                deploy_list.deploy_wizard((5,5))
            elif arena_data["MyTower"].game_timer > 120:
                deploy_list.list_.append((deployable[0],(-12,0)))
                deploy_list.list_.append((deployable[1],(12,0)))
    else :
        strategy = team_signal.strip(',')
        deployable = list([])
        available_from_strat =[]
        for i in range(len(arena_data["MyTower"].deployable_troops)): 
            deployable.append(arena_data["MyTower"].deployable_troops[i].strip())
        opptroops =[]
        for i in range (len (deployable)):
            if deployable[i] == Troops.wizard :
                available_from_strat.append(i)
        for i in range(len(arena_data["OppTroops"])):
            opptroops.append(arena_data["OppTroops"][i].name.strip())
        if(Troops.prince in deployable and len(available_from_strat)==1):
            deploy_list.list_.append((Troops.prince,(0,20)))
            deploy_list.deploy_wizard((0,30))
        else :
            if(Troops.wizard in deployable):
                deploy_list.deploy_wizard((5,10))
            else:
                deploy_list.list_.append((deployable[0],(-12,0)))
                deploy_list.list_.append((deployable[1],(12,0)))
            
            
    
    
            


