import random
from teams.helper_function import Troops, Utils

team_name = "Code Crusaders"
# Our team has eight troop types but we’ll focus on using these frequently:
troops = [
    Troops.wizard, Troops.minion, Troops.knight, Troops.valkyrie,
    Troops.dragon, Troops.giant, Troops.prince, Troops.skeleton
]
deploy_list = Troops([])
# Original team signal remains unchanged at start.
team_signal = "h, Prince, Knight, Barbarian, Princess"

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def get_deploy_position(troop):
    """Return a (x,y) position based on the troop type."""
    if troop == Troops.giant:
        return (random_x(-5, 5), 0)  # Tank position (centered)
    elif troop == Troops.wizard:
        return (random_x(-15, 15), 5)  # Backline support
    elif troop == Troops.dragon:
        return (random_x(-15, 15), 10)  # Sky support position
    elif troop == Troops.prince:
        return (random_x(-20, 20), 5)  # Prince in better attacking space 
    elif troop == Troops.skeleton:
        random_xfix = random.choice([-20, 20])
        return (random_xfix, random.randint(45, 50))  # Skeleton advanced deployment 
    else:
        return (random_x(-10, 10), 0)  # Default fallback

def deploy(arena_data: dict):
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    global team_signal
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    time_remaining = arena_data.get("Time", 180)
    
    # --- Early Game Group Deployment (Only at Game Start) ---
    # Trigger early deployment only if time_remaining is exactly 180 seconds and the team_signal remains at its original value.
    if time_remaining == 180 and team_signal == "h, Prince, Knight, Barbarian, Princess":
        starting_units = []
        for troop in [Troops.wizard, Troops.prince, Troops.dragon, Troops.skeleton,Troops.minion,Troops.valkyrie]:
            if troop in my_tower.deployable_troops:
                starting_units.append(troop)
                if len(starting_units) == 4:
                    break
        if starting_units:
            tower_x, tower_y = my_tower.position
            spacing = 5  # Fixed horizontal spacing between troops.
            start_x = tower_x - ((len(starting_units) - 1) * spacing) / 2
            deployments = []
            for i, unit in enumerate(starting_units):
                pos = (start_x + i * spacing, tower_y)
                deployments.append((unit, pos))
            deploy_list.list_ = deployments
            team_signal = "Early Game Group Deployment"
            return  # Exit after early deployment

    # --- Opponent Analysis ---
    enemy_forces = {}
    heavy_tank = False
    balloon_present = False
    balloon_pos = None
    for troop in opp_troops:
        enemy_forces[troop.name] = enemy_forces.get(troop.name, 0) + 1
        if troop.name in ["Giant"]:
            heavy_tank = True
        if troop.name.lower() == "balloon":
            balloon_present = True
            if balloon_pos is None:
                balloon_pos = troop.position

    swarm_threat = sum(enemy_forces.values()) > 5 or any(count > 3 for count in enemy_forces.values())
    
    # --- Strong Defense Check ---
    tower_pos = my_tower.position
    nearby_opponents = []
    for troop in opp_troops:
        dx = troop.position[0] - tower_pos[0]
        dy = troop.position[1] - tower_pos[1]
        distance = (dx**2 + dy**2) ** 0.5
        if distance < 20:
            nearby_opponents.append(troop)
    
    strong_defense = False
    if len(nearby_opponents) >= 3:
        strong_defense = True
        avg_x = sum(t.position[0] for t in nearby_opponents) / len(nearby_opponents)
        avg_y = sum(t.position[1] for t in nearby_opponents) / len(nearby_opponents)
        defense_y = avg_y - 10 if (avg_y - 10) > 0 else 0
    
    # --- Mode Selection / Formation Setup ---
    if strong_defense:
        # Instead of waiting for a giant due to low elixir, check if giant is deployable.
        if Troops.giant not in my_tower.deployable_troops:
            # Backup order when giant isn't available: best possible defense.
            formation_order = [
                Troops.wizard, Troops.prince, Troops.skeleton, Troops.dragon, Troops.giant,
                Troops.wizard, Troops.prince, Troops.skeleton, Troops.dragon, Troops.giant
            ]
            team_signal = "Strong Defense Mode (No Giant): Wizard, Prince, Skeleton, Dragon, Giant"
        else:
            formation_order = [
                Troops.wizard, Troops.prince, Troops.dragon, Troops.skeleton, Troops.giant,
                Troops.wizard, Troops.prince, Troops.dragon, Troops.skeleton, Troops.giant
            ]
            team_signal = "Strong Defense Mode: Wizard, Prince, Dragon, Skeleton, Giant"
    elif balloon_present:
        formation_order = [
            Troops.wizard, Troops.minion, Troops.dragon,
            Troops.wizard, Troops.minion, Troops.dragon
        ]
        team_signal = "Air Counter Mode: Wizard, Minion, Dragon"
    else:
        mode = "defense" if (heavy_tank or swarm_threat) else "attack"
        if mode == "defense":
            formation_order = [
                Troops.giant, Troops.wizard, Troops.dragon, Troops.prince, Troops.skeleton,
                Troops.giant, Troops.wizard, Troops.dragon, Troops.prince, Troops.skeleton
            ]
        else:
            formation_order = [
                Troops.wizard, Troops.prince, Troops.skeleton, Troops.dragon, Troops.giant,
                Troops.wizard, Troops.prince, Troops.skeleton, Troops.dragon, Troops.giant
            ]
    
    deployable = my_tower.deployable_troops
    
    # --- Rotation Rule and Deployment ---
    recent_deployed = []
    deployments = []
    max_deployments = 6
    
    i = 0
    while len(deployments) < max_deployments and i < len(formation_order) * 2:
        candidate = formation_order[i % len(formation_order)]
        i += 1
        if candidate not in deployable:
            continue
        if not strong_defense and balloon_present and candidate == Troops.giant:
            continue
        if candidate in recent_deployed and not (not strong_defense and candidate == Troops.giant):
            continue
        
        if strong_defense:
            pos = (avg_x, defense_y)
        elif balloon_present and balloon_pos is not None:
            deploy_y = balloon_pos[1] - 10 if (balloon_pos[1] - 10) > 0 else 0
            pos = (balloon_pos[0], deploy_y)
        else:
            pos = get_deploy_position(candidate)
        
        deployments.append((candidate, pos))
        recent_deployed.append(candidate)
        if len(recent_deployed) > 4:
            recent_deployed.pop(0)
    
    # --- Final Wave Override ---
    if time_remaining < 30:
        big_units = [t for t in [Troops.giant, Troops.wizard, Troops.prince, Troops.dragon] if t in deployable]
        if big_units:
            extra_deploys = []
            for unit in big_units:
                if strong_defense:
                    pos = (avg_x, defense_y)
                elif balloon_present and balloon_pos is not None:
                    deploy_y = balloon_pos[1] - 10 if (balloon_pos[1] - 10) > 0 else 0
                    pos = (balloon_pos[0], deploy_y)
                else:
                    pos = (random_x(-10, 10), random_x(0, 5))
                extra_deploys.append((unit, pos))
            deployments.extend(extra_deploys)
    
    # --- Fallback ---
    if not deployments and deployable:
        deployments.append((random.choice(deployable), (0, 0)))
    
    deploy_list.list_ = deployments