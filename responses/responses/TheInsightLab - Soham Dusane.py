import random
from teams.helper_function import Troops, Utils

team_name = "THE INSIGHT LAB"

troops = [
    Troops.wizard, Troops.minion, Troops.knight, Troops.valkyrie,
    Troops.dragon, Troops.giant, Troops.prince, Troops.skeleton,
]

deploy_list = Troops([])
team_signal = "h, Prince, Knight, Barbarian, Princess"

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def get_deploy_position(troop, is_defense=False):
    """
    Return a (x, y) position based on the troop type.
    Uses a preset rule-set for key troop types.
    """
    if is_defense:
        if troop == Troops.dragon:
            return (0, 10)  # Force Dragon to center in defense.
        if troop == Troops.knight:
            return (random_x(-10, 10), 5)  # Knight at y=5 for quicker engagement.
        return (0, 0)
    else:
        if troop == Troops.giant:
            return (random_x(-5, 5), 0)
        elif troop == Troops.wizard:
            return (random_x(-15, 15), 5)
        elif troop == Troops.dragon:
            return (random_x(-5, 5), 10)
        elif troop == Troops.prince:
            return (random_x(-20, 20), 5)
        elif troop == Troops.skeleton:
            return (random.choice([-20, 20]), random.randint(45, 50))
        else:
            return (random_x(-10, 10), 0)

def deploy(arena_data: dict):
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    """
    Aggressive unified deployment strategy with enhanced dynamic positioning:
      1. Update team signal.
      2. Analyze enemy forces and categorize opponent troop types.
      3. Set recommended counter (prefer "splash" if skeleton threat).
      4. Choose mode ("defense" if heavy tank or swarm threat; else "attack").
      5. Use rotation-based deployment.
      6. Use dynamic scoring fallback with improved positioning:
         - For air-category troops, deploy based on opponent skeleton flank:
             if opponent skeletons are on a flank, deploy our splash units on that same flank;
             otherwise, center them.
         - For Skeleton, deploy on the opposite flank of opponent splash troops.
         - For Knight, deploy at y=5.
         - Ensure deployed defenders are within attack range.
      7. In the final wave, deploy extra big units aggressively.
    """
    global team_signal
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    time_remaining = arena_data.get("Time", 180)
    deployments = []
    if len(team_signal) > 150:
        team_signal = ""


    
    # Local thresholds (defined as local variables only)
    min_y_threshold = 20
    max_y_threshold = 70
    rotation_limit = 2
    max_deployments = 6
    defense_override_y = 30
    center_range = 10
    attack_range_threshold = 10
    bonus = 3

    # --- Update Team Signal ---
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
        if troop.name not in current_names:
            team_signal = team_signal + ", " + troop.name

    # --- Opponent Analysis ---
    enemy_forces = {}
    heavy_tank = False
    skeleton_threat = False
    total_y = 0
    for troop in opp_troops:
        enemy_forces[troop.name] = enemy_forces.get(troop.name, 0) + 1
        total_y += troop.position[1]
        if troop.name == "Giant":
            heavy_tank = True
        if troop.name == "Skeleton" or getattr(troop, "type", "") == "skeleton_army":
            if enemy_forces[troop.name] > 2:
                skeleton_threat = True
    swarm_threat = (sum(enemy_forces.values()) > 5) or any(count > 3 for count in enemy_forces.values())
    avg_enemy_y = total_y / len(opp_troops) if opp_troops else 100

    # --- Opponent Air vs. Ground Categorization ---
    opponent_air = {"Minion", "Dragon", "Musketeer"}
    opponent_ground = {"Prince", "Knight", "Barbarian", "Princess"}
    tokens = [token.strip() for token in team_signal.split(",") if token.strip() != "h"]
    count_air = sum(1 for token in tokens if token in opponent_air)
    count_ground = sum(1 for token in tokens if token in opponent_ground)

    # --- Set Recommended Counter ---
    if skeleton_threat:
        recommended_counter = "splash"
    elif count_ground > count_air:
        recommended_counter = "air"
    elif count_air > count_ground:
        recommended_counter = "ground"
    else:
        recommended_counter = None
    # --- Balloon Counter Deployment ---
    # If an opponent Balloon is in our area (y < 50), then deploy in the order Wizard, Minion, Dragon.
    # The deployment uses the same x-coordinate as the Balloon and positions them at y equal to Balloon.y - 5 (i.e., 5 units closer to our tower).
    balloon_found = None
    for troop in opp_troops:
        if troop.name == "Balloon" and troop.position[1] < 50:
            balloon_found = troop
            break
    if balloon_found is not None:
        balloon_x = balloon_found.position[0]
        deploy_y = balloon_found.position[1] - 10
        # Append deployments in the order: Wizard, Minion, Dragon.
        deployments.extend([
            (Troops.wizard, (balloon_x, deploy_y)),
            (Troops.minion, (balloon_x, deploy_y)),
            (Troops.dragon, (balloon_x, deploy_y))
        ])
    # --- Set Mode (Defense vs. Attack) ---
    mode = "defense" if (heavy_tank or swarm_threat) else "attack"

    # --- Compute Overall Enemy X Distribution ---
    enemy_x_positions = [t.position[0] for t in opp_troops]
    avg_enemy_x = sum(enemy_x_positions) / len(enemy_x_positions) if enemy_x_positions else 0
    # Compute average x for opponent skeletons (splash troops).
    opp_skel_positions = [t.position[0] for t in opp_troops if t.name == "Skeleton" or getattr(t, "type", "") == "skeleton_army"]
    avg_skel = sum(opp_skel_positions) / len(opp_skel_positions) if opp_skel_positions else 0

    # --- Unified Rotation Deployment Setup ---
    if mode == "attack":
        formation_order = [
            Troops.wizard, Troops.prince, Troops.skeleton, Troops.dragon, Troops.giant,
            Troops.wizard, Troops.prince, Troops.skeleton, Troops.dragon, Troops.giant
        ]
    else:
        formation_order = [
            Troops.giant, Troops.wizard, Troops.dragon, Troops.knight, Troops.skeleton,
            Troops.giant, Troops.wizard, Troops.dragon, Troops.knight, Troops.skeleton
        ]
    deployable = my_tower.deployable_troops
    elixir_cost = {
        Troops.wizard: 5, Troops.minion: 3, Troops.knight: 3, Troops.valkyrie: 4,
        Troops.dragon: 4, Troops.giant: 5, Troops.prince: 5, Troops.skeleton: 3
    }

    # --- Rotation-Based Deployment ---
    
    recent_deployed = []
    i = 0
    while len(deployments) < max_deployments and i < len(formation_order) * 2:
        candidate = formation_order[i % len(formation_order)]
        i += 1
        if candidate not in deployable:
            continue
        if candidate in recent_deployed:
            continue
        pos = get_deploy_position(candidate, is_defense=(avg_enemy_y < defense_override_y))
        deployments.append((candidate, pos))
        recent_deployed.append(candidate)
        if len(recent_deployed) > 4:
            recent_deployed.pop(0)

    # --- Dynamic Troop Scoring Fallback ---
    troop_data = {
        Troops.wizard:    {"score": 6, "category": "air"},
        Troops.minion:    {"score": 4, "category": "air"},
        Troops.knight:    {"score": 3, "category": "ground"},
        Troops.valkyrie:  {"score": 4, "category": "air"},
        Troops.dragon:    {"score": 5, "category": "air"},
        Troops.giant:     {"score": 5, "category": "ground"},
        Troops.prince:    {"score": 5, "category": "ground"},
        Troops.skeleton:  {"score": 3, "category": "ground"}
    }
    best_troop = None
    best_score = -1
    for troop in troops:
        if troop not in deployable:
            continue
        base = troop_data.get(troop, {}).get("score", 0)
        cat = troop_data.get(troop, {}).get("category", "")
        score = base + (bonus if recommended_counter and cat == recommended_counter else 0)
        if score > best_score:
            best_score = score
            best_troop = troop

    # --- Dynamic Deployment Positioning ---
    if best_troop is not None and best_troop in deployable:
        y_min = min(t.position[1] for t in opp_troops) if opp_troops else max_y_threshold
        if y_min < min_y_threshold:
            y_pos = 0
        elif y_min > max_y_threshold:
            y_pos = 50
        else:
            y_pos = y_min - min_y_threshold

        # For air-category (splash) troops:
        if troop_data[best_troop]["category"] == "air":
            # If opponent skeletons are deployed on a flank, deploy our splash troop on that same flank.
            if abs(avg_skel) >= center_range:
                if avg_skel > 0:
                    deploy_position = (random_x(5, 20), y_pos)
                else:
                    deploy_position = (random_x(-20, -5), y_pos)
            else:
                deploy_position = (0, y_pos)
        # For Skeleton: deploy on the opposite flank of opponent splash troops.
        elif best_troop == Troops.skeleton:
            if abs(avg_skel) >= center_range:
                if avg_skel > 0:
                    deploy_position = (random_x(-20, -5), y_pos)
                else:
                    deploy_position = (random_x(5, 20), y_pos)
            else:
                deploy_position = (0, y_pos)
        # For Knight: deploy at y=5.
        elif best_troop == Troops.knight:
            deploy_position = (random_x(-10, 10), 5)
        else:
            deploy_position = (random_x(-10, 10), 0)

        # Ensure deployed unit is within attack range.
        if not any(abs(t.position[0] - deploy_position[0]) <= attack_range_threshold for t in opp_troops):
            deploy_position = (0, deploy_position[1])
        deployments.append((best_troop, deploy_position))
    else:
        if deployable:
            deployments.append((deployable[0], (0, 0)))
    
    # --- Final Wave Override ---
    if time_remaining < 30:
        enemy_x_positions = [t.position[0] for t in opp_troops]
        avg_enemy_x = sum(enemy_x_positions) / len(enemy_x_positions) if enemy_x_positions else 0
        if abs(avg_enemy_x) < 5:
            final_flank = 0
        elif avg_enemy_x > 0:
            final_flank = random_x(-20, -5)
        else:
            final_flank = random_x(5, 20)
        big_units = [t for t in [Troops.giant, Troops.wizard, Troops.prince, Troops.dragon] if t in deployable]
        if big_units:
            deployments.extend([(unit, (final_flank, random_x(0, 5))) for unit in big_units])
    

    
    deploy_list.list_ = deployments
