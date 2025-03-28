from teams.helper_function import Troops, Utils
import random

team_name = "Test_File_c_f_op"

troops = [
    Troops.prince, Troops.wizard, Troops.valkyrie,
    Troops.musketeer, Troops.dragon, Troops.minion, Troops.barbarian, Troops.archer
]

deploy_list = Troops([])
team_signal = ""  # Only allowed global variable


def is_in_attack_range(troop1, troop2, attack_range):
    """
    Checks if troop2 is within troop1's attack range considering troop sizes.
    """
    distance = Utils.calculate_distance(troop1, troop2)
    return distance < (troop1.size + troop2.size + attack_range)


def deploy(arena_data: dict):
    """
    Main deployment function called by the game engine.
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal


def logic(arena_data: dict):
    """
    Core logic for troop deployment.
    """
    global team_signal

    my_tower = arena_data["MyTower"]
    opp_tower = arena_data["OppTower"]
    opp_troops = arena_data["OppTroops"]
    my_troops = arena_data["MyTroops"]
    deployable = my_tower.deployable_troops
    my_elixir = my_tower.total_elixir

    # Early Game Strategy: Aggressive Start
    if my_tower.game_timer < 50:
        team_signal = "Attacking"
        deploy_aggressive_start(deployable)

    # Defensive Strategy
    if any(is_in_attack_range(my_tower, troop, 15) for troop in opp_troops):
        team_signal = "Defending"
        deploy_strong_defense(deployable, opp_troops)

    # Offensive Strategy
    else:
        team_signal = "Attacking"
        deploy_offensively(deployable,opp_tower,my_tower)

    # Late Game Strategy: Aggressive Push
    if my_tower.game_timer >= 1770 or my_tower.health > opp_tower.health:
        team_signal = "Attacking"
        deploy_more_aggressively(deployable,opp_tower)

    # Final Phase: Prioritize Defense
    if my_tower.game_timer > 1830 - 15 and my_tower.health <= opp_tower.health:
        team_signal = "Defending"
        deploy_strong_defense(deployable, opp_troops)


def deploy_aggressive_start(deployable):
    """
    Deploys an aggressive troop at the beginning to exploit weak defense.
    """
    if not deployable:
        return

    initial_attackers = [Troops.prince, Troops.dragon]
    available_attackers = [t for t in deployable if t in initial_attackers]

    selected_troop = random.choice(available_attackers) if available_attackers else random.choice(deployable)

    deploy_position = (random.randint(-5, 5), random.randint(30, 50))
    deploy_list.list_.append((selected_troop, deploy_position))


def deploy_strong_defense(deployable, opp_troops):
    """
    Deploys stronger defense against both ground and air units.
    """
    if not deployable:
        return

    tanks = [Troops.valkyrie, Troops.barbarian]
    support_units = [Troops.wizard, Troops.musketeer, Troops.archer]

    air_defense_units = [Troops.musketeer, Troops.wizard, Troops.minion]

    # Prioritize Wizard for defense
    if Troops.wizard in deployable:
        deploy_position = (random.randint(-6, 6), random.randint(8, 14))
        deploy_list.list_.append((Troops.wizard, deploy_position))

    # Check for enemy air units
    has_air_units = any(t.target_type == "air" for t in opp_troops)

    defenders = air_defense_units if has_air_units else support_units
    available_defenders = [t for t in deployable if t in defenders]

    if available_defenders:
        defender = random.choice(available_defenders)
        deploy_position = (random.randint(-6, 6), random.randint(8, 14))
        deploy_list.list_.append((defender, deploy_position))

    # Deploy tank units for defense
    tank_choices = [t for t in deployable if t in tanks]

    if tank_choices:
        tank_unit = random.choice(tank_choices)
        tank_position = (random.randint(-8, 8), random.randint(5, 12))
        deploy_list.list_.append((tank_unit, tank_position))


def deploy_offensively(deployable, opp_tower, my_tower):
    """
    Deploys offensive troops prioritizing counter-attack opportunities, ensuring Wizard deployment.
    """
    if deployable:
        attackers = [Troops.prince, Troops.dragon, Troops.wizard]
        available_attackers = [t for t in deployable if t in attackers]

        if Troops.wizard in deployable:
            selected_troop = Troops.wizard
        elif my_tower.game_timer <= 60:
            selected_troop = random.choice(deployable)
        else:
            selected_troop = random.choice(available_attackers) if available_attackers else random.choice(deployable)

        deploy_position = (random.randint(-5, 5), random.randint(40, 50))
        deploy_list.list_.append((selected_troop, deploy_position))


def deploy_more_aggressively(deployable, opp_tower):
    """
    Increases offensive troop deployment in the last 60 seconds when elixir rate is higher.
    """
    if deployable:
        high_elixir_troops = [Troops.dragon, Troops.prince, Troops.musketeer, Troops.wizard]
        available_troops = [t for t in deployable if t in high_elixir_troops]

        if available_troops:
            troop = random.choice(available_troops)
            deploy_list.list_.append((troop, (random.randint(-5, 5), 50)))


