import numpy as np
import random
from teams.helper_function import Troops, Utils 

team_name = "sedroc"
troops = [
    Troops.wizard, Troops.skeleton, Troops.archer, Troops.musketeer,
    Troops.dragon, Troops.prince, Troops.minion, Troops.valkyrie
]
deploy_list = Troops([])
team_signal = " "

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def logic(arena_data):
    global team_signal
    troops_data = Troops.troops_data
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    myTroops = arena_data["MyTroops"]
    elixir = my_tower.total_elixir
    time_s = my_tower.game_timer

    # Local constants (direct values)
    cell_radius = 5                # Check within 5 m for nearby enemy troops
    defense_hp_threshold = 300     # If friendly HP < 300, use splash defense
    our_elixir_threshold = 8       # Attack only if our elixir >= 8
    low_elixir_threshold = 3       # Opponent elixir is low if ≤ 3
    no_attack_time_threshold = 60  # 60 s inactivity triggers offensive push

    # Local timers
    last_opp_attack_time = arena_data.get("last_opp_attack_time", 0.0)
    last_big_push_time = arena_data.get("last_big_push_time", 0.0)

    # For my_tower, extract coordinates from 'position'
    if isinstance(my_tower, dict):
        tower_x, tower_y = my_tower.position[0], my_tower.position[1]
    else:
        tower_x, tower_y = my_tower.position[0], my_tower.position[1]
    available_cards = my_tower.deployable_troops

    # Update team_signal with enemy troop names
    for troop in opp_troops:
        if troop.name not in team_signal:
            team_signal = team_signal + ", " + troop.name if team_signal else troop.name
        # ----------------- Revised Offense Logic -----------------
    # ✅ Offense: If opponent has troops near king tower, deploy in same lane if elixir > 8
    
    
    
    enemy_crossed_bridge = [t for t in opp_troops if t.position[0] < 30]
    counter_options = []
    if enemy_crossed_bridge:
        for enemy in enemy_crossed_bridge:
            nearby_enemies = [t for t in opp_troops if np.linalg.norm(np.array(t.position) - np.array(enemy.position)) < 10]
            if nearby_enemies:
                strongest_enemies = sorted(nearby_enemies, key=lambda t: t.damage, reverse=True)[:2]

                deployed_count = 0  
                for strongest_enemy in strongest_enemies:
                    if strongest_enemy.health < 200:
                        continue  

                    air_troops = {"Minion", "Dragon","Balloon"}
                    
                    if strongest_enemy.name in air_troops:
                        counter_options = [ Troops.musketeer, Troops.dragon,Troops.minion ,Troops.wizard,Troops.archer]
                    elif strongest_enemy.name == "Wizard":
                        if Troops.skeleton in available_cards:
                            deploy_list.list_.append((Troops.skeleton, strongest_enemy.position))
                            deployed_count += 1
                        if deployed_count == 2:
                            break
                        else:
                            continue  
                    elif strongest_enemy.name in {"Musketeer", "Archer"}:
                        counter_options = [Troops.prince, Troops.valkyrie, Troops.musketeer, Troops.archer,Troops.dragon, Troops.wizard]
                    else:
                        counter_options = [Troops.valkyrie,Troops.minion, Troops.dragon,Troops.wizard,Troops.musketeer,Troops.archer]

                    # ✅ Handle Swarms: If >4 enemies detected, prioritize splash troops
                if len(nearby_enemies) > 4:
                    counter_options = [Troops.valkyrie,Troops.wizard, Troops.dragon, Troops.minion,Troops.archer]

                    # ✅ Adjust placement based on troop type
                for troop in counter_options:
                    if troop in available_cards:
                        if troop in [Troops.musketeer, Troops.archer, Troops.wizard]:
                            deploy_x, deploy_y = strongest_enemy.position[0]-6 ,strongest_enemy.position[1]-6
                        else:
                            deploy_x, deploy_y = strongest_enemy.position

                        deploy_list.list_.append((troop, (deploy_x, deploy_y)))
                        deployed_count += 1
                        break  

                if deployed_count == 2:
                    break

    # ----------------- Offense Logic -----------------
  # ✅ If Elixir > 9 and Prince + Wizard are both in deployable, deploy them at the bridge
    support_troop = Troops.prince
    if elixir > 9 and Troops.prince in available_cards and Troops.wizard in available_cards:
        deploy_list.list_.append((Troops.prince, (tower_x + 20, tower_y-10)))  # Prince in front
        deploy_list.list_.append((Troops.wizard, (tower_x + 20, tower_y-10)))  # Wizard behind

# ✅ If Wizard is deployed, support it with Prince or Barbarian in front
    elif Troops.wizard in available_cards:
        deploy_list.list_.append((Troops.wizard, (tower_x + 10, tower_y)))  # Deploy Wizard
    # Check if Prince or Barbarian is available for support
    if Troops.prince in available_cards:
        support_troop = Troops.prince
    elif Troops.musketeer in available_cards:
        support_troop = Troops.musketeer
    elif Troops.valkyrie in available_cards:
        support_troops = Troops.valkyrie
    # Deploy support troop in front of Wizard
    if support_troop:
        deploy_list.list_.append((support_troop, (tower_x + 25, tower_y)))  

# ✅ If no opponent troops are present, deploy any available troop near King Tower
    if elixir > 9 and not opp_troops and available_cards:
        deploy_list.list_.append((available_cards[0], (tower_x - 10, tower_y)))  # Deploy near King Tower

def deploy(arena_data: dict):
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal
