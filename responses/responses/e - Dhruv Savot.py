from teams.helper_function import Troops, Utils
import random

team_name = "Dhruv"
troops = [Troops.wizard,Troops.minion,Troops.archer,Troops.barbarian,Troops.dragon,Troops.skeleton,Troops.valkyrie,Troops.knight]
deploy_list = Troops([])
team_signal = ""
# Add persistent variables at the global scope

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
    global team_signal, deployment_timer, current_phase, last_deployment_time, max_elixir_reached
    
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    my_troops = arena_data["MyTroops"]
    elixir = my_tower.total_elixir
    deployment_history = []
    current_phase = "wait"
    deployment_timer = 0
    last_deployment_time = 0
    max_elixir_reached = 0

    
    # Increment deployment timer instead of resetting it
    deployment_timer += 1
    force_deploy = deployment_timer > 10  # Arbitrary threshold to ensure regular deployment

    if elixir > max_elixir_reached:
        max_elixir_reached = elixir
    elixir_efficiency = (deployment_timer - last_deployment_time) * elixir

    troop_data = {
        Troops.wizard: {"name": "Wizard","elixir": 5, "anti_air": True, "tank": False, "range": 5.5, "type": "ground", "strength": "splash"},
        Troops.minion: {"elixir": 3, "anti_air": True, "tank": False, "range": 2, "type": "air", "strength": "swarm"},
        Troops.archer: {"elixir": 3, "anti_air": True, "tank": False, "range": 5, "type": "ground", "strength": "range"},
        Troops.musketeer: {"elixir": 4, "anti_air": True, "tank": False, "range": 6, "type": "ground", "strength": "range"},
        Troops.dragon: {"elixir": 4, "anti_air": True, "tank": False, "range": 3.5, "type": "air", "strength": "splash"},
        Troops.skeleton: {"elixir": 3, "anti_air": False, "tank": False, "range": 0, "type": "ground", "strength": "swarm"},
        Troops.valkyrie: {"elixir": 4, "anti_air": False, "tank": True, "range": 0, "type": "ground", "strength": "splash"},
        Troops.barbarian: {"elixir": 3, "anti_air": False, "tank": False, "range": 0, "type": "ground", "strength": "melee"},
        Troops.giant: {"elixir": 5, "anti_air": False, "tank": True, "range": 0, "type": "ground"},
        Troops.knight: {"elixir": 3, "anti_air": False, "tank": True, "range": 0, "type": "ground"},
    }
    
    # --- Update Team Signal with enemy troops ---
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
        if troop.name not in current_names:
            team_signal = team_signal + ", " + troop.name if team_signal else troop.name
    
    # --- First priority: Check if we can deploy wizards ---
    deployable = my_tower.deployable_troops[:4]  # Only the first 4 are deployable
    wizards_available = Troops.wizard in deployable and troop_data[Troops.wizard]["elixir"] <= elixir
    
    # --- Analyze field situation ---
    air_threats_count = sum(1 for troop in opp_troops if troop.type == "air")
    ground_threats_count = sum(1 for troop in opp_troops if troop.type == "ground")
    
    # Count our troops by type
    my_air_count = sum(1 for troop in my_troops if troop.type == "air")
    my_ground_count = sum(1 for troop in my_troops if troop.type == "ground")
    my_tanks = sum(1 for troop in my_troops if troop.name in ["Valkyrie", "Barbarian"])
    my_wizards = sum(1 for troop in my_troops if troop.name == "Wizard")
    
    # --- Check if our tower is under threat ---
    tower_threatened = False
    closest_threat = None
    min_distance = 1000
    
    for troop in opp_troops:
        distance = Utils.calculate_distance(troop, my_tower)
        if distance < min_distance:
            min_distance = distance
            closest_threat = troop
        
        if distance < 15:  # Arbitrary threat distance
            tower_threatened = True
    
    affordable_troops = [troop for troop in deployable if troop in troop_data and troop_data[troop]["elixir"] <= elixir]
    
    if not affordable_troops:
        return
    
    # Check if we have a giant in play
    my_giants = [troop for troop in my_troops if troop.name == "Giant"]
    has_giant = len(my_giants) > 0
    
    # ----- PRIORITY 1: DEPLOY WIZARD WHENEVER POSSIBLE -----
    if wizards_available:
        # If we have enough elixir, deploy a wizard
        if tower_threatened:
            # Deploy wizard to counter threats if tower is threatened
            if closest_threat:
                # Position to counter based on threat type
                dx = closest_threat.position[0] - my_tower.position[0]
                direction = 1 if dx > 0 else -1
                wizard_pos = (
                    closest_threat.position[0] - (direction * (troop_data[Troops.wizard]["range"] - 1)),
                    closest_threat.position[1] + 2
                )
                deploy_list.list_.append((Troops.wizard, wizard_pos))
                deployment_history.append({"troop": Troops.wizard, "position": wizard_pos, "time": deployment_timer})
                last_deployment_time = deployment_timer
                return
        elif has_giant:
            # Deploy wizard behind giant for support
            giant = my_giants[0]
            giant_pos = giant.position
            wizard_pos = (giant_pos[0], giant_pos[1] + 3)  # 3 units behind giant
            deploy_list.list_.append((Troops.wizard, wizard_pos))
            deployment_history.append({"troop": Troops.wizard, "position": wizard_pos, "time": deployment_timer})
            last_deployment_time = deployment_timer
            return
        else:
            # Deploy wizard at a strategic position if no threats or giants
            # Alternate between offensive and defensive positions
            if deployment_timer % 2 == 0:
                # Offensive position
                wizard_pos = (random_x(-20, 20), -20)
            else:
                # Defensive position (closer to our tower)
                wizard_pos = (random_x(-15, 15), 10)
            
            deploy_list.list_.append((Troops.wizard, wizard_pos))
            deployment_history.append({"troop": Troops.wizard, "position": wizard_pos, "time": deployment_timer})
            last_deployment_time = deployment_timer
            return
    
    # If we can't deploy a wizard yet, save elixir for wizard unless we need to counter threats
    if not wizards_available and elixir < 5 and not tower_threatened:
        # Save elixir for wizard unless tower is threatened
        return
    
    # ----- PRIORITY 2: WAIT FOR OPPONENT TROOPS -----
    # Initially, don't play anything until opponent troops are in tower range
    if current_phase == "wait":
        # Check if enemy troops are in tower range
        tower_threatened = False
        for troop in opp_troops:
            distance = Utils.calculate_distance(troop, my_tower)
            if distance < 25:  # Tower range - wait until they're close
                tower_threatened = True
                break
        
        if tower_threatened:
            current_phase = "counter"  # Move to counter phase
        else:
            # ----- ELIXIR MANAGEMENT: PREVENT WASTE -----
            # If we're almost at max elixir, deploy something
            if elixir >= 9:
                # Try to deploy a wizard if close to having enough elixir
                if elixir >= 9 and Troops.wizard in deployable and elixir < 10:
                    # Wait for wizard
                    return
                # Otherwise deploy something cheap at the back
                cheap_units = sorted([t for t in affordable_troops], key=lambda t: troop_data[t]["elixir"])
                if cheap_units:
                    # Deploy at back of our side to build up forces without engaging
                    deploy_pos = (random_x(-15, 15), 15)  # Back position
                    deploy_list.list_.append((cheap_units[0], deploy_pos))
                    deployment_history.append({"troop": cheap_units[0], "position": deploy_pos, "time": deployment_timer})
                    last_deployment_time = deployment_timer
            return
    
    # ----- PRIORITY 3: COUNTER OPPONENT TROOPS -----
    if current_phase == "counter":
        # Find closest threat to counter
        closest_threat = None
        min_distance = float('inf')
        
        for troop in opp_troops:
            distance = Utils.calculate_distance(troop, my_tower)
            if distance < min_distance:
                min_distance = distance
                closest_threat = troop
        
        if closest_threat:
            # Check if we can deploy a wizard as priority counter
            if Troops.wizard in affordable_troops:
                counter_troop = Troops.wizard
            else:
                # If not, use other ranged units
                ranged_counters = [troop for troop in affordable_troops if troop_data[troop]["range"] > 2]
                if ranged_counters:
                    counters = ranged_counters
                else:
                    # Fall back to any appropriate counter if no ranged available
                    if hasattr(closest_threat, 'type') and closest_threat.type == "air":
                        counters = [troop for troop in affordable_troops if troop_data[troop]["anti_air"]]
                    else:
                        counters = affordable_troops
                
                if not counters:
                    return
                counter_troop = counters[0]
            
            # Position to counter based on threat type
            if troop_data[counter_troop]["range"] > 2:
                # Ranged counter - stay at a distance
                dx = closest_threat.position[0] - my_tower.position[0]
                direction = 1 if dx > 0 else -1
                counter_pos = (
                    closest_threat.position[0] - (direction * (troop_data[counter_troop]["range"] - 1)),
                    closest_threat.position[1] + 2
                )
            else:
                # Melee counter - deploy on top
                counter_pos = closest_threat.position
            
            deploy_list.list_.append((counter_troop, counter_pos))
            deployment_history.append({"troop": counter_troop, "position": counter_pos, "time": deployment_timer})
            last_deployment_time = deployment_timer
            
            if counter_troop != Troops.wizard:
                # If we couldn't deploy a wizard, move to giant deployment
                current_phase = "deploy_giant"
            else:
                # If we used a wizard, wait for more elixir
                current_phase = "wait"
            return
        else:
            # No threats to counter, move to deploy_giant phase
            current_phase = "deploy_giant"
    
    # ----- PRIORITY 4: DEPLOY GIANT AS TANK FOR WIZARDS -----
    if current_phase == "deploy_giant":
        # Only deploy a giant if we don't already have one and have enough wizards
        giants = [troop for troop in affordable_troops if troop == Troops.giant]
        
        if giants and not has_giant and (my_wizards > 0 or Troops.wizard not in deployable):
            # Deploy giant at the edge of deployment area
            edge_x = random_x(-25, 25)
            edge_y = -25  # Edge of deployment area
            
            deploy_list.list_.append((giants[0], (edge_x, edge_y)))
            deployment_history.append({"troop": giants[0], "position": (edge_x, edge_y), "time": deployment_timer})
            last_deployment_time = deployment_timer
            
            current_phase = "support"
            return
        else:
            # If no giant available or we already have one, move to support phase
            current_phase = "support"

    # ----- PRIORITY 5: SUPPORT EXISTING GIANT WITH WIZARDS OR OTHER TROOPS -----
    if current_phase == "support":
        # Only provide support if we actually have a giant in play
        if has_giant:
            # First check if wizard is available for support
            if Troops.wizard in affordable_troops:
                support_troop = Troops.wizard
            else:
                # If wizard not available, use other ranged support
                support_troops = [troop for troop in affordable_troops if troop_data[troop]["range"] > 2]
                if not support_troops:
                    # If no ranged support available, use any troop
                    support_troops = affordable_troops
                
                if not support_troops:
                    return
                support_troop = support_troops[0]
            
            # Get giant position
            giant = my_giants[0]
            giant_pos = giant.position
            
            # Deploy support directly behind giant
            support_pos = (giant_pos[0], giant_pos[1] + 3)  # 3 units behind giant
            
            deploy_list.list_.append((support_troop, support_pos))
            deployment_history.append({"troop": support_troop, "position": support_pos, "time": deployment_timer})
            last_deployment_time = deployment_timer
            return
        else:
            # If we don't have a giant, reset to wait phase
            current_phase = "wait"
    
    # ----- RESET TO WAIT PHASE IF NO TROOPS IN PLAY -----
    if len(opp_troops) == 0 and len(my_troops) == 0:
        current_phase = "wait"
        return
    
    # ----- WIZARD DEPLOYMENT FALLBACK -----
    # If we've gone too long without deploying and have enough elixir for a wizard
    if elixir >= 5 and Troops.wizard in affordable_troops:
        wizard_pos = (random_x(-20, 20), 10)  # Deploy at a safer position
        deploy_list.list_.append((Troops.wizard, wizard_pos))
        deployment_history.append({"troop": Troops.wizard, "position": wizard_pos, "time": deployment_timer})
        last_deployment_time = deployment_timer
        return
    
    # ----- ELIXIR EFFICIENCY FALLBACK -----
    # If we've gone too long without deploying and have excess elixir but can't deploy wizard
    if elixir >= 8 and deployment_timer - last_deployment_time > 8 and Troops.wizard not in affordable_troops:
        # Find cheapest effective troop
        affordable_troops.sort(key=lambda t: troop_data[t]["elixir"])
        if affordable_troops:
            # Deploy at the back to prepare for next push
            conservative_pos = (random_x(-20, 20), 10)
            deploy_list.list_.append((affordable_troops[0], conservative_pos))
            deployment_history.append({"troop": affordable_troops[0], "position": conservative_pos, "time": deployment_timer})
            last_deployment_time = deployment_timer
            return
    
    # ----- FALLBACK: IF MAX ELIXIR, DEPLOY SOMETHING -----
    if elixir >= 9 and affordable_troops:
        # Find cheapest troop
        affordable_troops.sort(key=lambda t: troop_data[t]["elixir"])
        cheap_troop = affordable_troops[0]
        
        # Deploy at edge of area
        deploy_pos = (random_x(-25, 25), -25)
        deploy_list.list_.append((cheap_troop, deploy_pos))
        deployment_history.append({"troop": cheap_troop, "position": deploy_pos, "time": deployment_timer})
        last_deployment_time = deployment_timer
