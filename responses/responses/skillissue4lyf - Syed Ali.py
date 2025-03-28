from teams.helper_function import Troops, Utils


team_name = "giant"
troops = [Troops.giant,Troops.giant,Troops.giant,Troops.giant,Troops.giant,Troops.giant,Troops.giant,Troops.giant]
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

    print(arena_data["OppTroops"])
    global team_signal
    deploy_list.list_.append((arena_data["MyTower"].deployable_troops[0],(0,0)))
    deploy_list.list_.append((arena_data["MyTower"].deployable_troops[1],(0,0)))