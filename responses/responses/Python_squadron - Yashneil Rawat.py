import random
from teams.helper_function import Troops, Utils
import time
team_name = "Python Squadron"
troops = [
    Troops.wizard, Troops.minion, Troops.giant, Troops.archer,
    Troops.dragon, Troops.skeleton, Troops.barbarian, Troops.prince
]
deploy_list = Troops([])
team_signal = "h, Prince, Knight, Barbarian, Princess"

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
    attack_troops=[Troops.wizard,Troops.dragon,Troops.prince, Troops.minion, Troops.archer]
    global team_signal
    troops_data = Troops.troops_data
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    my_troops = arena_data["MyTroops"]
    my_elixir = arena_data["MyTower"].total_elixir
    # --- Update Team Signal ---
    # Add new opponent troop names (avoid duplicates).
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
        if troop.name not in current_names:
            team_signal = team_signal + ", " + troop.name if team_signal else troop.name
    # --- Analyze Opponent's Deck Composition ---
    # Define opponent categories.
    opponent_air = {"Minion", "Dragon", "Balloon"}
    opponent_ground = {"Prince", "Knight", "Barbarian", "Princess","Musketeer","Valkyrie","Wizard","Archer","Giant","Skeleton"}
    
    tokens = [token.strip() for token in team_signal.split(",") if token.strip() != "h"]

    deployable = my_tower.deployable_troops
    # Define base scores and categories for our troops.
    troop_data = {
        Troops.wizard:    {"score": 5, "category": "air",    "name": "Wizard"},
        Troops.minion:    {"score": 3, "category": "air",    "name": "Minion"},
        Troops.prince:    {"score": 5, "category": "ground", "name": "Prince"},
        Troops.archer: {"score": 3, "category": "air", "name": "Archer"},
        Troops.dragon:    {"score": 5, "category": "air",    "name": "Dragon"},
        Troops.skeleton:  {"score": 3, "category": "ground", "name": "Skeleton"},
        Troops.barbarian: {"score": 3, "category": "ground", "name": "Barbarian"},
        Troops.giant:  {"score": 5, "category": "ground",    "name": "Giant"}
    }
    feasible_troop = None
    min_cost = float('inf')
    for troop in deployable:
        if troop in troop_data:
            cost = troop_data[troop]["score"]
            if cost < min_cost:
                min_cost = cost
                feasible_troop = troop

    recommended_counter = None
    giant = None
    my_troop_names=[]
    opp_troop_names=[]
    for my_troop in my_troops:
        my_troop_names.append(my_troop.name)
        if my_troop.name == "Giant":
            giant = my_troop
    for opp_troop in opp_troops:
        opp_troop_names.append(opp_troop.name)
        if opp_troop.name == "Prince":
            prince = opp_troop
        if opp_troop.name == "Wizard":
            wizard = opp_troop

    #Defense
    nearest_troop = None
    leftest_troop = None
    rightest_troop = None
    send_attack_position = (0,0)
    giant_support_position = (0,5)
    deploy_extreme = (25,50)
    if opp_troops:
        nearest_troop = min(opp_troops, key=lambda t: t.position[1])
        leftest_troop = min(opp_troops, key=lambda t: t.position[0])
        rightest_troop = max(opp_troops, key=lambda t: t.position[0])
        if (abs(leftest_troop.position[0])<=abs(rightest_troop.position[0])):
            send_attack_position = leftest_troop.position
            deploy_extreme = (-25,50)
        else:
            send_attack_position = rightest_troop.position
            deploy_extreme = (25,50)
    if "Giant" in my_troop_names and giant != None and nearest_troop != None:
        giant_support_position = (giant.position[0],giant.position[1]-abs(giant.position[1]-nearest_troop.position[1]))
    if nearest_troop and nearest_troop.position[1]<50 and (nearest_troop.name != "Giant" or "Skeleton" in my_troop_names):
        troop = nearest_troop
        if "Prince" in opp_troop_names and prince.position[1]<50:
            if Troops.skeleton in deployable and my_elixir>=3:
                deploy_list.list_.append((Troops.skeleton,prince.position))           
            if Troops.wizard in deployable and my_elixir>=5:
                deploy_list.list_.append((Troops.wizard,(prince.position[0],prince.position[1]-20)))
            if Troops.prince in deployable and my_elixir>=5:
                deploy_list.list_.append((Troops.prince,prince.position))               
            if Troops.barbarian in deployable and my_elixir>=3:
                deploy_list.list_.append((Troops.barbarian,prince.position))
            if Troops.archer in deployable and my_elixir>=3:
                    deploy_position = (prince.position[0]-15 if prince.position[0]>=15 else prince.position[0]+15  ,prince.position[1]-20 if prince.position[1]>=20 else prince.position[1]+7)        
            if Troops.minion in deployable and my_elixir>=3:
                deploy_list.list_.append((Troops.minion,prince.position))
            if Troops.dragon in deployable and my_elixir>=4:
                deploy_list.list_.append((Troops.dragon,prince.position))
        if "Wizard" in opp_troop_names and wizard.position[1]<50:
            if Troops.skeleton in deployable and my_elixir>=3:
                deploy_list.list_.append((Troops.skeleton,wizard.position))
            if Troops.prince in deployable and my_elixir>=5:
                deploy_list.list_.append((Troops.prince,wizard.position))
            if Troops.wizard in deployable and my_elixir>=5:
                deploy_list.list_.append((Troops.wizard,wizard.position))    
            if Troops.barbarian in deployable and my_elixir>=3:
                deploy_list.list_.append((Troops.barbarian,wizard.position))
            if Troops.minion in deployable and my_elixir>=3:
                deploy_list.list_.append((Troops.minion,wizard.position))
            


        if troop.type=="air":
                if Troops.minion in deployable and my_elixir>=3:
                    feasible_troop=Troops.minion
                    deploy_position = troop.position
                    deploy_list.list_.append((feasible_troop,troop.position))
                elif Troops.archer in deployable and my_elixir>=3:
                    feasible_troop=Troops.archer
                    deploy_position = (troop.position[0]+15,troop.position[1])
                    deploy_list.list_.append((feasible_troop,troop.position))
                elif Troops.wizard in deployable and my_elixir>=5:
                    feasible_troop=Troops.wizard
                    deploy_position = troop.position
                    deploy_list.list_.append((feasible_troop,(troop.position[0]-5,troop.position[1]-15)))
                elif Troops.dragon in deployable and my_elixir>=4:
                    feasible_troop=Troops.dragon
                    deploy_position = troop.position
                    deploy_list.list_.append((feasible_troop,troop.position))
                #break
        elif troop.type == "ground":
                if Troops.skeleton in deployable and my_elixir>=3:
                    feasible_troop=Troops.skeleton
                    deploy_position = troop.position
                    deploy_list.list_.append((feasible_troop,troop.position))                                   
                elif Troops.wizard in deployable and my_elixir>=5:
                    feasible_troop=Troops.wizard
                    deploy_position = troop.position
                    deploy_list.list_.append((feasible_troop,(troop.position[0]-5,troop.position[1]-15)))
                elif Troops.dragon in deployable and my_elixir>=4 and troop.name =="Skeleton":
                    feasible_troop=Troops.dragon
                    deploy_position = troop.position
                    deploy_list.list_.append((feasible_troop,troop.position))
                elif Troops.prince in deployable and my_elixir>=5 and troop.name != "Skeleton":
                    feasible_troop=Troops.prince
                    deploy_position = troop.position
                elif Troops.barbarian in deployable and my_elixir>=3:
                    feasible_troop=Troops.barbarian
                    deploy_position = troop.position
                    deploy_list.list_.append((feasible_troop,troop.position))
                elif Troops.archer in deployable and my_elixir>=3:
                    feasible_troop=Troops.archer
                    deploy_position = (troop.position[0]-15 if troop.position[0]>=15 else troop.position[0]+15  ,troop.position[1]-20 if troop.position[1]>=20 else troop.position[1]+7)
                    deploy_list.list_.append((feasible_troop,troop.position))
                elif Troops.minion in deployable and my_elixir>=3:
                    feasible_troop=Troops.minion
                    deploy_position = troop.position
                elif Troops.prince in deployable and my_elixir>=5:
                    feasible_troop=Troops.prince
                    deploy_position = troop.position
                    deploy_list.list_.append((feasible_troop,troop.position))
                elif Troops.giant in deployable and my_elixir>=5:
                    feasible_troop=Troops.giant
                    deploy_position = troop.position
                    deploy_list.list_.append((feasible_troop,troop.position))
                elif Troops.dragon in deployable and my_elixir>=4:
                    feasible_troop=Troops.dragon
                    deploy_position = troop.position
                    deploy_list.list_.append((feasible_troop,troop.position))
            
        return
            

    if my_troops and "Giant" in my_troop_names:
        for troop in attack_troops :
            if troop in deployable and my_elixir>=4:#troop_data_new[troop.name]["score"] :
                deploy_list.list_.append((troop, giant_support_position))
                return
    
     #Attack
    if Troops.giant in deployable and my_elixir>=7:
        for troop in attack_troops :
            if troop in deployable :
                deploy_list.list_.append((Troops.giant,(0,20)))
                return
    if Troops.prince in deployable and my_elixir>=5 :
        if nearest_troop and nearest_troop.position[1]>=55:
            deploy_list.list_.append((Troops.prince,deploy_extreme))
            return
        else :
            deploy_list.list_.append((Troops.prince,send_attack_position))
            return
    if Troops.wizard in deployable and my_elixir>=5:
        if nearest_troop and nearest_troop.position[1]>=55:
            deploy_list.list_.append((Troops.wizard,deploy_extreme))
            return
        else :
            deploy_list.list_.append((Troops.wizard,send_attack_position))
            return
    if Troops.skeleton in deployable and my_elixir>=3 and "Wizard" not in opp_troop_names and "Dragon" not in opp_troop_names and "Valkyrie" not in opp_troop_names:
        if nearest_troop and nearest_troop.position[1]>=55:
            deploy_list.list_.append((Troops.skeleton,deploy_extreme))
            return
        else :
            deploy_list.list_.append((Troops.skeleton,send_attack_position))
            return
    if Troops.dragon in deployable and my_elixir>=4:
        if nearest_troop and nearest_troop.position[1]>=55:
            deploy_list.list_.append((Troops.dragon,deploy_extreme))
            return
        else :
            deploy_list.list_.append((Troops.dragon,send_attack_position))
            return