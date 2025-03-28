import random
import math
from teams.helper_function import Troops, Utils

team_name = "Atrocian10"
troops = [
    Troops.wizard, Troops.prince, Troops.archer, Troops.musketeer,
    Troops.dragon, Troops.valkyrie, Troops.balloon, Troops.skeleton
]
deploy_list = Troops([])

# Initialize team signal with default elixir values
team_signal = "0,0,0,0"  # Format: "h,prev_attack_elixir,prev_defense_elixir"

def deploy(arena_data: dict):
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    global team_signal
    my_tower = arena_data["MyTower"]
    opp_tower = arena_data["OppTower"]
    my_troops = arena_data["MyTroops"]
    opp_troops = arena_data["OppTroops"]
    total_elixir = my_tower.total_elixir
    team_signal_list=[float(signal) for signal in team_signal.split(",") if signal]    
    # Parse previous frame's elixir values from team_signal
    opp_side_threat=0
    my_side_threat=0
    tower_in_range=team_signal_list[2:4]
    for troop in my_troops:
        if  math.sqrt((troop.position[0])*2 + (troop.position[1] - 100)*2)<=troop.size+opp_tower.size+troop.attack_range:
            tower_in_range[1]+= 1/(troop.attack_range+1)
    for troop in opp_troops:
        if troop.position[1] < 50:  # Only react when they cross a certain vertical threshold
            my_side_threat+=1
        if troop.position[1] > 50: 
            opp_side_threat+=1
        if  math.sqrt((troop.position[0])*2 + (troop.position[1])*2)<=troop.size+opp_tower.size+troop.attack_range:
            tower_in_range[0]+= 1/(troop.attack_range+1)
   
   
   
  # Extract elixir values  
    prev_attack_elixir = float(team_signal_list[0])
    prev_defense_elixir = float(team_signal_list[1])
    
    # Calculate elixir change
    elixir_gain = total_elixir - (prev_attack_elixir + prev_defense_elixir)
       
        # *Dynamic Elixir Allocation*
    attack_elixir = prev_attack_elixir + (0.4 * elixir_gain)
    defense_elixir = prev_defense_elixir + (0.6 * elixir_gain)

    # for troop in opp_troops:
    #     current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
    #     if troop.name not in current_names:
    #         team_signal = team_signal + ", " + troop.name if team_signal else troop.name
    # Score Calculation
    condition = 0
    if my_tower.health == opp_tower.health:
      if tower_in_range[1]>tower_in_range[0]:
        condition=1
        print("Winning",my_tower.health,opp_tower.health)
      elif tower_in_range[1]<tower_in_range[0]:
        condition=-1
        print("Losing",my_tower.health,opp_tower.health)
    if my_tower.health > opp_tower.health:
        condition = 1
        print("Winning",my_tower.health,opp_tower.health)
    elif my_tower.health < opp_tower.health:
        condition = -1
        print("Losing",my_tower.health,opp_tower.health)
        # Opponent's score is the inverse of ours
    attack_defense_mode=False
    # Mode Selection
    attack_mode = condition==-1 or condition==0  # Attack if enemy has equal or more score
    defense_mode = not attack_mode         # Defense if we are leading    
    if my_side_threat>4:
        attack_defense_mode=True
    if defense_mode:
        attack_elixir = 0
        defense_elixir = total_elixir  # Use all elixir for defense

    # *Tracking Enemy Troop Positions*
    enemy_positions = {troop.position for troop in opp_troops}
    attacking_enemy_positions = {troop.position for troop in opp_troops if troop.position[1] < 30 and troop.position[1] >50}
    
    # for troop in opp_troops:
    #     current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
    #     if troop.name not in current_names:
    #         team_signal = team_signal + ", " + troop.name if team_signal else troop.name
    # opponent_air = {"Minion", "Dragon", "Musketeer"}
    # opponent_ground = {"Prince", "Knight", "Barbarian", "Princess"}
    # tokens = [token.strip() for token in team_signal.split(",") if token.strip() != "h"]
    # count_air = sum(1 for token in tokens if token in opponent_air)
    # count_ground = sum(1 for token in tokens if token in opponent_ground)
    # recommended_counter = "air" if count_ground > count_air else "ground" if count_air > count_ground else None

    # deployable = my_tower.deployable_troops
    # # Adjusted troop scores for a more aggressive stance.
    # troop_data = {
    #     Troops.wizard:    {"score": 10, "category": "air"},
    #     Troops.minion:    {"score": 5,  "category": "air"},
    #     Troops.archer:    {"score": 4,  "category": "ground"},
    #     Troops.musketeer: {"score": 7,  "category": "ground"},
    #     Troops.dragon:    {"score": 12, "category": "air"},
    #     Troops.valkyrie:  {"score": 9,  "category": "ground"},
    #     Troops.skeleton:     {"score": 15, "category": "ground"},
    #     Troops.balloon:    {"score": 6, "category": "air"}
    # }

    # # --- Best Troop Selection Based on Enemy Composition ---
    # best_troop = None
    # best_score = -1
    # bonus = 3  # Bonus for matching the recommended counter
    # for troop in troops:
    #     if troop not in deployable:
    #         continue
    #     base = troop_data[troop]["score"]
    #     cat = troop_data[troop]["category"]
    #     score = base + (bonus if recommended_counter and cat == recommended_counter else 0)
    #     if score > best_score:
    #         best_score = score
    #         best_troop = troop

    # if best_troop is not None:
    #     selected_category = troop_data[best_troop]["category"]
    #     pos = (random.randint(-25, 25), 0) if selected_category == "air" else (random.randint(-20, 20), 0)
    #     deploy_list.list_.append((best_troop, pos))

    # threat_count = len(opp_troops)

    def random_safe_position(y_pos,enemy_positions,enemy_range):
       """Generate a random position away from enemy troops."""
       while True:
        a=0
        ck=False
        position = (random.randint(-25,25), y_pos)
        for i in attacking_enemy_positions:
            a+=1
            if (math.floor(position[0]) in range(math.floor(i[0]) - math.ceil(enemy_range), math.floor(i[0]) + math.ceil(enemy_range))) or a == len(enemy_positions):
                ck=True
                break
        if not ck:
            break
       return position
    attack_elixir_used=0
    defense_elixir_used=0   
       # *Attack Handling* 
    if attack_mode:
        print("Attack Mode-----------------------------")
        print("attack elixir--",attack_elixir)
        print("defence elixir--",defense_elixir)

        for troop in opp_troops:
            if attack_elixir>=5:
                 if Troops.prince in my_tower.deployable_troops and attack_elixir>=troop.elixir:
                  attack_elixir_used+=troop.elixir
                  deploy_list.deploy_prince(random_safe_position(50,enemy_positions,troop.attack_range+troop.size+Troops.troops_data['Dragon'].size))
                 if Troops.skeleton in my_tower.deployable_troops and attack_elixir>=troop.elixir:
                  attack_elixir_used+=troop.elixir
                  deploy_list.deploy_skeleton(random_safe_position(50,enemy_positions,troop.attack_range+troop.size+Troops.troops_data['Skeleton'].size))
            if troop.position[1] < 80 and troop.position[1] >45 and opp_side_threat<3:
                if Troops.prince in my_tower.deployable_troops and attack_elixir>=troop.elixir:
                    attack_elixir_used+=troop.elixir
                    deploy_list.deploy_prince(random_safe_position(50,enemy_positions,troop.attack_range+troop.size+Troops.troops_data['Prince'].size))
                
            if troop.position[1] < 80 and troop.position[1] >45 and opp_side_threat<4:  # Only react when they cross a certain vertical threshold
                
               if Troops.balloon in my_tower.deployable_troops and attack_elixir>=troop.elixir:
                  attack_elixir_used+=troop.elixir
                  deploy_list.deploy_balloon(random_safe_position(50,enemy_positions,troop.attack_range+troop.size+Troops.troops_data['Balloon'].size))
               if Troops.prince in my_tower.deployable_troops and attack_elixir>=troop.elixir:
                    attack_elixir_used+=troop.elixir
                    deploy_list.deploy_prince(random_safe_position(50,enemy_positions,troop.attack_range+troop.size+Troops.troops_data['Prince'].size))
               if Troops.dragon in my_tower.deployable_troops and attack_elixir>=troop.elixir:
                  attack_elixir_used+=troop.elixir
                  deploy_list.deploy_dragon(random_safe_position(50,enemy_positions,troop.attack_range+troop.size+Troops.troops_data['Dragon'].size))  
               if Troops.skeleton in my_tower.deployable_troops and attack_elixir>=troop.elixir:
                  attack_elixir_used+=troop.elixir
                  deploy_list.deploy_skeleton(random_safe_position(50,enemy_positions,troop.attack_range+troop.size+Troops.troops_data['Skeleton'].size))
               
               
            if troop.position[1] < 45:  # Only react when they cross a certain vertical threshold    
                defending_position=(troop.position[0],abs((troop.position[0]))*2)
                
                if Troops.wizard in my_tower.deployable_troops and defense_elixir>=troop.elixir:
                    deploy_list.deploy_wizard(defending_position)
                    defense_elixir_used+=troop.elixir
                    continue
                if Troops.archer in my_tower.deployable_troops and defense_elixir>=troop.elixir:
                    deploy_list.deploy_archer(defending_position)
                    defense_elixir_used+=troop.elixir
                    continue
                if Troops.musketeer in my_tower.deployable_troops and defense_elixir>=troop.elixir:
                    deploy_list.deploy_musketeer(defending_position)
                    defense_elixir_used+=troop.elixir
                    continue
                if Troops.valkyrie in my_tower.deployable_troops and defense_elixir>=troop.elixir:
                    deploy_list.deploy_valkyrie(defending_position)
                    defense_elixir_used+=troop.elixir
                    continue
   
    # *Defense Handling*
    if defense_elixir > 0 and defense_mode or attack_defense_mode:
        print("Defense Mode-----------------------------")
        print("attack elixir--",attack_elixir)
        print("defence elixir--",defense_elixir)
        if attack_defense_mode:
           defense_elixir=defense_elixir+attack_elixir*0.5
           attack_elixir=attack_elixir*0.5 
        for troop in opp_troops:
            # Deploy defenders near own tower but away from enemy troops
          if troop.position[1] < 60:  # Only react when they cross a certain vertical threshold
            defending_position=(troop.position[0],(troop.position[1])/2)
            if Troops.wizard in my_tower.deployable_troops and defense_elixir>=troop.elixir:
                  deploy_list.deploy_wizard(defending_position)
                  defense_elixir_used+=troop.elixir
                  continue
            if Troops.musketeer in my_tower.deployable_troops and defense_elixir>=troop.elixir:
                    deploy_list.deploy_musketeer(defending_position)
                    defense_elixir_used+=troop.elixir
                    continue
            if Troops.valkyrie in my_tower.deployable_troops and defense_elixir>=troop.elixir:
                  deploy_list.deploy_valkyrie(defending_position)
                  defense_elixir_used+=troop.elixir
                  continue
            if Troops.archer in my_tower.deployable_troops and defense_elixir>=troop.elixir:
                    deploy_list.deploy_archer(defending_position)
                    defense_elixir_used+=troop.elixir
                    continue   
            if Troops.dragon in my_tower.deployable_troops and defense_elixir>=troop.elixir:
                    deploy_list.deploy_dragon(defending_position) 
                    defense_elixir_used+=troop.elixir
                    continue   
    
    print("Attack Elixir Used:",attack_elixir_used)
    print("Defense Elixir Used:",defense_elixir_used)
    # Update team_signal with new elixir values for the next frame
    team_signal = f"{attack_elixir-attack_elixir_used},{defense_elixir-defense_elixir_used},{tower_in_range[0]},{tower_in_range[1]}"