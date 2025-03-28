from teams.helper_function import Troops, Utils
import math
team_name = "Royal syntax"
troops = [
    Troops.wizard, Troops.minion, Troops.archer, Troops.musketeer,
    Troops.dragon, Troops.skeleton, Troops.valkyrie, Troops.barbarian
]
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
    troops_data = Troops.troops_data
    (d_x, d_y, should) = find_safe_deploy_position(arena_data)
    if should:
        deploy_list.list_.append((arena_data["MyTower"].deployable_troops[0], (d_x, d_y)))

def defense(arena_data:dict):
    opp_troop = arena_data["OppTroops"]
    target = arena_data["MyTower"].target
    tower = arena_data["MyTower"]
    
    should = False
    if target is not None:
        tower_attk = tower.size + tower.attack_range + target.size
        dist = Utils.calculate_distance(tower.position,target.position, False)
        safe_dist = tower_attk - target.attack_range - target.size - tower.size
        my_troop = Troops.troops_data[arena_data["MyTower"].deployable_troops[0]]
        circ1 = target.size + my_troop.size + my_troop.attack_range - 3 # when enem attack more
        circ2 = target.size + my_troop.size + target.discovery_range - 3 # when my attack more
        #print(target.position)
        if dist <= tower_attk - safe_dist +  3:
            should = True
        
        deploy_x = target.position[0]
        if target.attack_range > my_troop.attack_range:
            deploy_y = target.position[1] + target.size + my_troop.size + my_troop.attack_range - 3
        else: 
            deploy_y = target.position[1] + target.size + my_troop.size + target.discovery_range - 3 
        return (deploy_x, deploy_y, should)
    return (0, 0, False)

    # if target is not None:
    #     tower_attk = tower.size + tower.attack_range + target.size
    #     dist = Utils.calculate_distance(tower.position,target.position, False)
    #     safe_dist = tower_attk - target.attack_range - target.size - tower.size
    #     my_troop = Troops.troops_data[arena_data["MyTower"].deployable_troops[0]]
    #     #print(target.position)
    #     if dist <= tower_attk - safe_dist +  3:
    #         should = True
        
    #     deploy_x = target.position[0]
    #     deploy_y = target.position[1]
    #     return (deploy_x, deploy_y, should)
    # return (0, 0, False)


def find_safe_deploy_position(arena_data: dict):
    """
    Find a safe deployment position around the target troop that avoids
    discovery by other opponent troops.
    """
    opp_troops = arena_data["OppTroops"]
    target = arena_data["MyTower"].target
    my_troop_type = arena_data["MyTower"].deployable_troops[0]
    my_troop = Troops.troops_data[my_troop_type]
    best_deploy = []
    # If no target, can't find a position
    if target is None:
        return (0, 0, False)
    
    if target is not None:
        tower = arena_data["MyTower"]
        tower_attk = tower.size + tower.attack_range + target.size
        dist = Utils.calculate_distance(tower.position,target.position, False)
        safe_dist = tower_attk - target.attack_range - target.size - tower.size
        my_troop = Troops.troops_data[arena_data["MyTower"].deployable_troops[0]]
        #print(target.position)
        if dist <= tower_attk - safe_dist +  3:
            should = True
        
        deploy_x = target.position[0]
        deploy_y = target.position[1]
        return (deploy_x, deploy_y, should)
    
    # Calculate circle radii
    circ1 = target.size + my_troop.size + my_troop.attack_range - 3  # when enemy attack more
    circ2 = target.size + my_troop.size + target.discovery_range - 3  # when my attack more
    
    # Choose radius based on attack ranges
    radius = circ1 if target.attack_range > my_troop.attack_range else circ2
    
    # Check points around the circle for safe deployment
    best_position = None
    min_exposure = float('inf')  # Lower means fewer other troops can discover us
    
    # Try 36 positions around the circle (every 10 degrees)
    for angle_deg in range(0, 360, 10):
        angle_rad = math.radians(angle_deg)
        
        # Calculate position on the circle around target
        deploy_x = target.position[0] + radius * math.cos(angle_rad)
        deploy_y = target.position[1] + radius * math.sin(angle_rad)
        
        # Count how many other troops can discover us at this position
        exposure_count = 0
        for troop in opp_troops:
            if troop is not target:  # Skip our intended target
                dist = Utils.calculate_distance((deploy_x, deploy_y), troop.position, False)
                # Check if we're within discovery range of this troop
                if dist <= (troop.discovery_range + troop.size + my_troop.size):
                    exposure_count += 1
        
        # If this position has less exposure than our current best, update it
        if exposure_count < min_exposure:
            min_exposure = exposure_count
            best_position = (deploy_x, deploy_y)
            
            # If we found a position with zero exposure, no need to check more
            if min_exposure == 0:
                best_deploy.append((deploy_x, deploy_y))
    
    # Determine if we should deploy based on whether we found a reasonable position
    should_deploy = min_exposure < 2  # Deploy if exposed to at most 1 other troop
    
    # If we couldn't find any position, fall back to default
    if best_position is None:
        deploy_x = target.position[0]
        deploy_y = target.position[1] + radius
        return (deploy_x, deploy_y, should_deploy)
    d = 10000
    if len(best_deploy) > 1:
        for i in best_deploy:
            if abs(i[0] - target.position[0]) < d:
                d = abs(i[0] - target.position[0])
        for i in best_deploy:
            if abs(i[0] - target.position[0]) == d:
                return (i[0], i[1], should_deploy)
    return (best_position[0], best_position[1], should_deploy)