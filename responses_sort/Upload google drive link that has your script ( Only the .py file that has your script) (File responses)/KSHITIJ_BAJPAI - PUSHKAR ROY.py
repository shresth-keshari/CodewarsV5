import random
from teams.helper_function import Troops, Utils

team_name = "KSHITIJ_BAJPAI"
troops = [
    Troops.wizard, Troops.archer,
    Troops.dragon, Troops.knight, Troops.skeleton,
    Troops.prince, Troops.giant, Troops.valkyrie
]
deploy_list = Troops([])
team_signal = ""

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
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]

    current_names = set(name.strip() for name in team_signal.split(","))
    for troop in opp_troops:
        if troop.name not in current_names:
            team_signal += f", {troop.name}"

    deployable = set(my_tower.deployable_troops)
    priority_queue = []
    
    # Deploy Skeleton Army directly on priority targets in our territory
    if Troops.skeleton in deployable:
        priority_targets = ["Prince", "Wizard", "Giant"]
        for target in priority_targets:
            for troop in opp_troops:
                if troop.name == target and troop.position[1] < 50:
                    priority_queue.insert(0, (Troops.skeleton, (troop.position[0], troop.position[1])))
                    break
            else:
                continue
            break
    
    # Initial rush
    if len(opp_troops) == 0:
        if Troops.knight in deployable and Troops.wizard in deployable:
            priority_queue.append((Troops.knight, (0,50)))
            priority_queue.append((Troops.wizard, (0,40)))
        elif Troops.valkyrie in deployable and Troops.archer in deployable:
            priority_queue.append((Troops.valkyrie, (0,50)))
            priority_queue.append((Troops.archer, (0,40)))
        elif Troops.knight in deployable and Troops.dragon in deployable:
            priority_queue.append((Troops.knight, (0,50)))
            priority_queue.append((Troops.dragon, (0,40)))
        elif Troops.valkyrie in deployable and Troops.wizard in deployable:
            priority_queue.append((Troops.valkyrie, (0,50)))
            priority_queue.append((Troops.wizard, (0,40)))
        elif Troops.giant in deployable and Troops.dragon in deployable:
            priority_queue.append((Troops.giant, (0,50)))
            priority_queue.append((Troops.dragon, (0,35)))
    
    # Deploy Knight or Valkyrie on an opponent Wizard in our territory
    for troop in opp_troops:
        if troop.name == "Wizard" and troop.position[1] < 50:
            if Troops.knight in deployable:
                priority_queue.insert(0, (Troops.knight, (troop.position[0], troop.position[1])))
            elif Troops.valkyrie in deployable:
                priority_queue.insert(0, (Troops.valkyrie, (troop.position[0], troop.position[1])))
    
    # Ensure occupied_columns is always assigned
    occupied_columns = {troop.position[0] for troop in opp_troops} if opp_troops else set()
    
    # Check if any opponent troop is in the range (0,0) to (0,60)
    opponent_in_range = any(troop.position[0] == 0 and 0 <= troop.position[1] <= 60 for troop in opp_troops)
    
    # Check if any opponent troop is within 70 tiles distance from our tower
    opponent_nearby = any(abs(troop.position[1] - my_tower.position[1]) <= 70 for troop in opp_troops)
    
    # Deploy Prince if conditions are met
    if Troops.prince in deployable and not opponent_in_range and opponent_nearby and (-25 not in occupied_columns or 25 not in occupied_columns):
        prince_x = -25 if -25 not in occupied_columns else 25
        priority_queue.append((Troops.prince, (prince_x, 50)))
    
    # Deploy counter troops based on their position
    for troop in opp_troops:
        if troop.name in ["Dragon", "Balloon"]:
            for counter_troop in [Troops.dragon, Troops.archer]:
                if counter_troop in deployable:
                    deploy_position = (0, 20)  # Always deploy from the middle
                    priority_queue.append((counter_troop, deploy_position))
    
    # Fallback: deploy something if nothing was chosen
    if not priority_queue:
        for troop in [Troops.archer, Troops.wizard, Troops.valkyrie]:
            if troop in deployable:
                priority_queue.append((troop, (0, 10)))
                break
    
    deploy_list.list_ = priority_queue
