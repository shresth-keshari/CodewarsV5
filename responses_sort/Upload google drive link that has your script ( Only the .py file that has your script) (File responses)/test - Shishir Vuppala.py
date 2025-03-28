from teams.helper_function import Troops, Utils

team_name = "Da Donesparces"
troops = [
    Troops.wizard, Troops.giant, Troops.skeleton, Troops.minion,
    Troops.knight, Troops.valkyrie, Troops.prince, Troops.barbarian
]
deploy_list = Troops([])
team_signal="hello"

def scorer(x):
    return 1

def deploy(arena_data:dict):
    """
    DON'T TEMPER DEPLOY FUCNTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data:dict):
    print("logic!!!")
    global team_signal
    troops_data = Troops.troops_data
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]

    deployable = my_tower.deployable_troops

    trooptypes = {
        "tanks" : ["Knight","Valkyrie","Giant"],
        "attackers" : ["Wizard","Muskeeter","Prince"],
        "counter" : ["Skeleton","Minion"]
    }

    counters = {
        "Archer": ["knight","barbarians","skeleton","valkyrie","prince","wizard"],
        "Wizard" : ["knight","barbarians","skeleton","valkyrie","prince","wizard"],
        "Barbarian" : ["knight","barbarians","skeleton","valkyrie","prince","wizard"],
        "Balloon" : ["knight","barbarians","skeleton","valkyrie","prince","wizard"],
        "Dragon" : ["knight","barbarians","skeleton","valkyrie","prince","wizard"],
        "Minion" : ["knight","barbarians","skeleton","valkyrie","prince","wizard"],
        "Skeleton" : ["knight","barbarians","skeleton","valkyrie","prince","wizard"],
        "Prince" : ["knight","barbarians","skeleton","valkyrie","prince","wizard"],
        "Musketeer" : ["knight","barbarians","skeleton","valkyrie","prince","wizard"],
        "Knight" : ["knight","barbarians","skeleton","valkyrie","prince","wizard"],
        "Giant" : ["knight","barbarians","skeleton","valkyrie","prince","wizard"],
        "Valkyrie" : ["knight","barbarians","skeleton","valkyrie","prince","wizard"]
    }

    danger = False

    for opp in arena_data["OppTroops"]:
        if opp.position[1] <= 70:
            danger=True
    
    if(danger):
        print("657465746574657465")
        maxopp = max(arena_data["OppTroops"],key=scorer)
        for troop in counters[maxopp.name]:
            if troop in deployable:
                x = maxopp.position[0]
                y = maxopp.position[1]
                if(y>=60):
                    y = 60
                if(y<=10):
                    y=10
                print("why am i trash")
                deploy_list.list_.append((troop,(30,y-10)))
        if arena_data["MyTower"].total_elixir > 7:
            deploy_list.list_.append((deployable[0], (-10, 0)))
    else:
        tankpresent = False
        currenttank = ""
        for troop in arena_data["MyTroops"]:
            if troop.name in trooptypes["tanks"]:
                tankpresent=True
                currenttank = troop
        if(tankpresent):
            for troop in deployable:
                if troop in trooptypes["attackers"]:
                    x = currenttank.position[0]
                    y = currenttank.position[1]
                    if y>50:
                        y=50
                    deploy_list.list_.append((troop,(x,y)))
        else:
            tankplaced = False
            for troop in deployable:
                if troop in trooptypes["tanks"]:
                    deploy_list.list_.append((troop,(-10,0)))
                    tankplaced = True
            if(not tankplaced):
                if arena_data["MyTower"].total_elixir > 7:
                    deploy_list.list_.append((deployable[0], (-10, 0)))
