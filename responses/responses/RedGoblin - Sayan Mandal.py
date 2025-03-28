import random
from teams.helper_function import Troops, Utils

team_name = "RedGoblin"
troops = [
    Troops.wizard, Troops.skeleton, Troops.minion, Troops.musketeer,
    Troops.dragon, Troops.giant, Troops.valkyrie, Troops.knight
]
deploy_list = Troops([])
team_signal = "h"

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def deploy(arena_data:dict):
    """
    DON'T TEMPER DEPLOY FUCNTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data:dict):
    global team_signal
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    my_troops = arena_data["MyTroops"]

    # --- Update Team Signal ---
    # Add new opponent troop names (avoid duplicates).
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
        #print(f"Opponent Troops: {troop.name}")
        if troop.name not in current_names:
            team_signal = team_signal + ", " + troop.name if team_signal else troop.name
    #print(f"Team Signal: {team_signal}")
    #print(f"Opponent Troops: {opp_troops}")
    
    # --- Score Our Troops (only from deployable troops) ---
    deployable = my_tower.deployable_troops
    # Define counter for opponent troops.
    troop_data = {
        "Wizard": [Troops.knight, Troops.valkyrie, Troops.wizard, Troops.musketeer, Troops.dragon],
        "Knight": [Troops.minion, Troops.dragon, Troops.skeleton, Troops.knight, Troops.valkyrie],
        "Skeleton": [Troops.valkyrie, Troops.dragon, Troops.minion, Troops.wizard, Troops.skeleton],
        "Musketeer": [Troops.knight, Troops.valkyrie, Troops.skeleton, Troops.musketeer, Troops.wizard],
        "Dragon": [Troops.wizard, Troops.dragon, Troops.musketeer, Troops.minion, Troops.skeleton],
        "Valkyrie": [Troops.minion, Troops.dragon, Troops.knight, Troops.musketeer, Troops.valkyrie],
        "Prince": [Troops.skeleton, Troops.knight, Troops.valkyrie, Troops.minion, Troops.musketeer],
        "Giant": [Troops.skeleton, Troops.minion, Troops.knight, Troops.wizard, Troops.musketeer],
        "Archer": [Troops.valkyrie, Troops.skeleton, Troops.knight, Troops.wizard, Troops.musketeer],
        "Minion": [Troops.wizard, Troops.dragon, Troops.musketeer, Troops.minion, Troops.skeleton],
        "Balloon": [Troops.minion,Troops.wizard, Troops.musketeer, Troops.dragon, Troops.skeleton],
        "Barbarian": [Troops.dragon, Troops.wizard,Troops.minion, Troops.skeleton, Troops.valkyrie]
    }
    # Loop over our full troop list, but only consider those that are deployable.
    opp_boundary=0

    numTroopMySide=0
    for troop in my_troops:
        if troop.position[1]<50:
            numTroopMySide+=1
    
    if(numTroopMySide==0):
        opp_boundary=-10

    numOpp=0
    for oppTroop in opp_troops:
        if (oppTroop.position[1]<opp_boundary):
            #print(f"{oppTroop.name}: {oppTroop.position}")   
            numOpp=1
            for counter in troop_data[oppTroop.name]:
                far=0
                if(counter in deployable):
                    if(counter == Troops.wizard or counter == Troops.musketeer or counter == Troops.dragon):
                        far=11
                    deploy_position = (oppTroop.position[0],(50+oppTroop.position[1]-far) if((50+oppTroop.position[1]-far)>0) else 0)
                    deploy_list.list_.append((counter, deploy_position))
                    #print(f"{counter}: {counter.position}")  
                    break

    attackingTroop=[Troops.wizard, Troops.dragon, Troops.musketeer, Troops.minion]

    for troop in my_troops:
        if(troop.name == "Giant" and troop.health>=2500 and troop.position[1]>0):
            for attack in attackingTroop:
                if(attack in deployable):
                    deploy_position = (0,45)
                    deploy_list.list_.append((attack, deploy_position))

    if(numOpp == 0) and (my_tower.total_elixir>=8):
        if(Troops.giant in deployable):
            deploy_list.list_.append((Troops.giant, (0,10)))
        elif(Troops.musketeer in deployable):
            deploy_list.list_.append((Troops.musketeer, (random_x(-10, 10),10)))
        elif(Troops.wizard in deployable):
            deploy_list.list_.append((Troops.wizard, (random_x(-10, 10),10))) 
        elif(Troops.valkyrie in deployable):
            deploy_list.list_.append((Troops.valkyrie, (random_x(-10, 10),10)))
        elif(Troops.knight in deployable):
            deploy_list.list_.append((Troops.knight, (random_x(-10, 10),10))) 

    