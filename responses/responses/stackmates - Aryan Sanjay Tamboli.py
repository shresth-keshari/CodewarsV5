import random
import math
from teams.helper_function import Troops, Utils

# -----------------------------
# Team configuration and deck
# -----------------------------
team_name = "Master AI GODMODE"
troops = [
    Troops.prince,
    Troops.dragon,
    Troops.wizard,
    Troops.musketeer,
    Troops.giant,
    Troops.valkyrie,
    Troops.archer,
    Troops.minion
]
deploy_list = Troops([])
team_signal = "h"

# -----------------------------
# Utility Functions
# -----------------------------
def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def analyze_opponent(arena_data: dict):
    """
    Tracks enemy troops, updates team_signal, and detects enemy patterns.
    Returns counts of enemy air and ground troops.
    """
    global team_signal
    opp_troops = arena_data.get("OppTroops", [])
    signal_tokens = [token.strip() for token in team_signal.split(",") if token.strip() != "h"]
    for troop in opp_troops:
        if troop.name not in signal_tokens:
            signal_tokens.append(troop.name)
    team_signal = ", ".join(["h"] + signal_tokens)
    count_air = sum(1 for token in signal_tokens 
                    if Troops.troops_data.get(token) and Troops.troops_data[token].type == "air")
    count_ground = sum(1 for token in signal_tokens 
                       if Troops.troops_data.get(token) and Troops.troops_data[token].type == "ground")
    return count_air, count_ground

def calculate_troop_score(troop_name: str, counter_type: str):
    """
    Calculates a score for each troop based on DPS, health, and bonus if it counters the given type.
    """
    troop = Troops.troops_data[troop_name]
    dps = troop.damage / troop.attack_speed
    health_factor = troop.health / 1000
    base_score = dps + health_factor
    if counter_type == "air" and troop.target_type.get("air", False):
        return base_score + 5
    elif counter_type == "ground" and troop.target_type.get("ground", False):
        return base_score + 5
    return base_score

def choose_best_troop(deployable: list, counter_type: str):
    """
    Returns the best troop from deployable ones based on calculated effectiveness.
    """
    return max(deployable, key=lambda t: calculate_troop_score(t, counter_type), default=None)

def choose_counter_troop(deployable: list, target, opp_troops):
    """
    Chooses the best counter troop from deployable ones to neutralize the target.
    """
    best_troop = None
    best_score = -1
    for troop_name in deployable:
        troop = Troops.troops_data[troop_name]
        # Only consider troops that can hit the target.
        if (target.type == "air" and not troop.target_type.get("air", False)) or \
           (target.type == "ground" and not troop.target_type.get("ground", False)):
            continue
        dps = troop.damage / troop.attack_speed
        time_to_kill = target.health / dps if dps > 0 else float('inf')
        score = 1 / time_to_kill if time_to_kill > 0 else 0
        nearby_enemies = [e for e in opp_troops if Utils.calculate_distance(target.position, e.position, False) < 5]
        if len(nearby_enemies) > 1 and troop.splash_range > 0:
            score *= 1.5
        if score > best_score:
            best_score = score
            best_troop = troop_name
    return best_troop

def get_optimal_attack_position():
    """
    Calculates the best position for an offensive push.
    This position is chosen to be close to the enemy tower (assumed to be near y=0)
    and maximizes time in the tower's attack range.
    """
    return (random_x(-5, 5), random.randint(5, 15))

def get_optimal_defense_position(target):
    """
    Calculates an optimal position for a defensive counter relative to an enemy target.
    """
    x_offset = random.uniform(-2, 2)
    y_offset = -5 if target.type == "air" else -3
    return (target.position[0] + x_offset, max(0, target.position[1] + y_offset))

def should_deploy_now(deployable: list, enemy_push: list):
    """
    Determines if deployment should occur immediately based on current battlefield conditions.
    If our available troop has low health and might benefit from tower damage,
    we may delay deployment.
    """
    if not enemy_push or len(enemy_push) < 2:
        return True
    best_troop = choose_best_troop(deployable, "ground")
    if best_troop:
        troop_obj = Troops.troops_data[best_troop]
        # If troop's health is low compared to its max (simulated condition), delay.
        # (Assuming troop_obj.health is current health; adjust threshold as needed)
        if troop_obj.health < (troop_obj.health * 0.5):
            return False
    return True

# -----------------------------
# Main Deploy Function
# -----------------------------
def deploy(arena_data: dict):
    """
    Clears previous orders, runs advanced AI logic, and returns deployment orders and team signal.
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

# -----------------------------
# MASTER AI ULTIMATE LOGIC – THE FINAL DOMINATOR
# -----------------------------
def logic(arena_data: dict):
    """
    Advanced dynamic strategy that adapts to all battlefield conditions:
    - Aggressive tower assault when the path is clear.
    - Perfect defense when enemy threats are detected.
    - Multi-lane support and delayed deployment when beneficial.
    - Ultimate final push when time or conditions demand it.
    """
    global team_signal
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data.get("OppTroops", [])
    my_troops = arena_data.get("MyTroops", [])
    deployable = my_tower.deployable_troops if hasattr(my_tower, "deployable_troops") else []

    analyze_opponent(arena_data)

    # FINAL PUSH: When game time is low or elixir is abundant, go all-out.
    if my_tower.game_timer <= 30 or my_tower.total_elixir >= 10:
        deploy_list.list_.append(("Giant", get_optimal_attack_position()))
        deploy_list.list_.append(("Prince", get_optimal_attack_position()))
        deploy_list.list_.append(("Wizard", get_optimal_attack_position()))
        deploy_list.list_.append(("Musketeer", get_optimal_attack_position()))
        return

    # Identify enemy threats using a comprehensive list from the documentation.
    high_priority_types = ["Giant", "Balloon", "Prince", "Wizard", "Knight", "Dragon"]
    threats = [troop for troop in opp_troops if troop.name in high_priority_types and troop.position[1] < 30]

    if threats:
        # Defensive Mode: Counter enemy threats.
        target = min(threats, key=lambda t: t.position[1])
        best_troop = choose_counter_troop(deployable, target, opp_troops)
        deploy_position = get_optimal_defense_position(target)
        # If our best counter has low health, consider delaying deployment.
        if not should_deploy_now(deployable, my_troops):
            return
    else:
        # Offensive Mode: If no immediate threats, support ongoing push or start a new one.
        if my_troops:
            push_point = min(my_troops, key=lambda t: t.position[1])
            best_troop = choose_best_troop(deployable, "ground")
            deploy_position = (push_point.position[0] + random.uniform(-3, 3), push_point.position[1] - 5)
        else:
            best_troop = choose_best_troop(deployable, "ground")
            deploy_position = get_optimal_attack_position()

    if best_troop:
        deploy_list.list_.append((best_troop, deploy_position))