import random
from teams.helper_function import Troops, Utils

team_name = "13unreg"

troops = [
    Troops.wizard, Troops.minion, Troops.knight, Troops.valkyrie,
    Troops.dragon, Troops.giant, Troops.prince, Troops.skeleton
]
deploy_list = Troops([])
team_signal = "h, Prince, Knight, Barbarian, Princess"

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def get_deploy_position(troop):
    """Return a (x, y) position based on the troop type."""
    if troop == Troops.giant:
        return (random_x(-5, 5), 0)  # Tank position (centered)
    elif troop == Troops.wizard:
        return (random_x(-15, 15), 5)  # Backline support
    elif troop == Troops.dragon:
        return (random_x(-25, 25), 10)  # Sky support position
    elif troop == Troops.prince:
        return (random_x(-20, 20), 5)  # Prince in better attacking space
    elif troop == Troops.skeleton:
        random_xfix = random.choice([-20, 20])  # Skeletons in advanced deployment space
        return (random_xfix, random.randint(40, 45))  # Slightly adjusted for better deployment
    else:
        return (random_x(-10, 10), 0)  # Default fallback position

def deploy(arena_data: dict):
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    global team_signal
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    time_remaining = arena_data.get("Time", 180)
    
    # --- Opponent Analysis ---
    enemy_forces = {}
    heavy_tank = False
    for troop in opp_troops:
        enemy_forces[troop.name] = enemy_forces.get(troop.name, 0) + 1
        if troop.name in ["Giant", "P.E.K.K.A"]:
            heavy_tank = True
    swarm_threat = sum(enemy_forces.values()) > 5 or any(count > 3 for count in enemy_forces.values())
    
    # --- Mode Selection ---
    # In defense mode (if enemy shows heavy units or swarm), we want our Giant as tank.
    mode = "defense" if (heavy_tank or swarm_threat) else "attack"
    
    # --- Deployment Rotation Setup ---
    if mode == "defense":
        formation_order = [
            Troops.giant , Troops.wizard, Troops.dragon, Troops.prince, Troops.skeleton,
            Troops.giant, Troops.wizard, Troops.dragon, Troops.prince, Troops.skeleton
        ]
    else:
        formation_order = [
            Troops.wizard, Troops.prince, Troops.skeleton, Troops.dragon, Troops.giant,
            Troops.wizard, Troops.prince, Troops.skeleton, Troops.dragon, Troops.giant
        ]
    
    deployable = my_tower.deployable_troops  # available units (assumed to be a list of troop types)
    
    # --- Rotation Rule ---
    # A troop, once deployed, cannot be redeployed until four other deployments occur.
    recent_deployed = []  # holds the last 4 deployed troop types
    deployments = []
    max_deployments = 6  # You may adjust how many units to deploy per wave
    
    i = 0
    # Iterate over formation_order (allowing repeated cycles) until we reach our max deployments.
    while len(deployments) < max_deployments and i < len(formation_order) * 2:
        candidate = formation_order[i % len(formation_order)]
        i += 1
        if candidate not in deployable:
            continue
        
        # Ensure Giant is deployed even in defense mode despite the rotation.
        if candidate in recent_deployed and not (mode == "defense" and candidate == Troops.giant):
            continue
        
        # Deploy the candidate.
        pos = get_deploy_position(candidate)
        deployments.append((candidate, pos))
        
        # Update the rotation: add this candidate; if more than 4 deployments in rotation, remove the oldest.
        recent_deployed.append(candidate)
        if len(recent_deployed) > 4:
            recent_deployed.pop(0)
    
    # --- Final Wave Override ---
    if time_remaining < 30:
        big_units = [t for t in [Troops.giant, Troops.wizard, Troops.prince, Troops.dragon] if t in deployable]
        if big_units:
            deployments.extend([
                (unit, (random_x(-10, 10), random_x(0, 5)))
                for unit in big_units
            ])
    
    # --- Fallback Mechanism ---
    if not deployments and deployable:
        deployments.append((random.choice(deployable), (0, 0)))
    
    deploy_list.list_ = deployments

