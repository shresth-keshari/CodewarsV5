
from teams.helper_function import Troops, Utils
import random

team_name = "Test_File_c_f"

troops = [
    Troops.prince, Troops.wizard, Troops.valkyrie,
    Troops.musketeer, Troops.dragon, Troops.minion, Troops.barbarian, Troops.archer
]

deploy_list = Troops([])
team_signal = ""  # Only allowed global variable


def is_in_attack_range(troop1, troop2, range):
    """
    Checks if troop2 is within troop1's attack range considering troop sizes.
    """
    distance = Utils.calculate_distance(troop1, troop2)
    return distance < (troop1.size + troop2.size + range)


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
    my_tower = arena_data["MyTower"]
    opp_tower = arena_data["OppTower"]
    opp_troops = arena_data["OppTroops"]
    my_troops = arena_data["MyTroops"]
    deployable = my_tower.deployable_troops

    # Deploy an aggressive troop in the initial phase to exploit weak defense
    if my_tower.game_timer < 500:
        deploy_aggressive_start(deployable, opp_tower)

    # Adjusted Defensive Strategy
    if any(is_in_attack_range(my_tower, troop, 15) for troop in opp_troops):
        deploy_strong_defense(deployable, my_troops, opp_troops, my_tower)
    else:
        deploy_offensively(deployable, opp_tower, my_tower)

    # Last 60 Seconds - More Aggressive Deployment
    if my_tower.game_timer >= 1600 or my_tower.health > opp_tower.health:
        deploy_more_aggressively(deployable, opp_tower)

    # Final 15 Seconds - Prioritize Defense
    if my_tower.game_timer > 1800 - 150 and my_tower.health <= opp_tower.health:
        deploy_strong_defense(deployable, my_troops, opp_troops, my_tower)



    for troop in opp_troops:
        if troop.name == "Wizard" :
            if Troops.wizard in deployable:
                deploy_list.deploy_wizard(troop.position)
            else:
                deploy_list.list_.append((deployable[0],troop.position))


def deploy_aggressive_start(deployable, opp_tower):
    """
    Deploys an aggressive troop at the beginning to bypass weak defense.
    """
    if deployable:
        initial_attackers = [Troops.prince, Troops.dragon,Troops.wizard]
        available_attackers = [t for t in deployable if t in initial_attackers]
        if available_attackers:
            selected_troop = random.choice(available_attackers)
        else:
            selected_troop = random.choice(deployable)
        deploy_position = (random.randint(-5, 5), 50)
        deploy_list.list_.append((selected_troop, deploy_position))


def deploy_strong_defense(deployable, my_troops, opp_troops, my_tower):
    """
    Deploys stronger defense against both ground and air units, prioritizing Wizard.
    """
    if deployable:
        tanks = [Troops.valkyrie, Troops.barbarian,Troops.wizard]
        support = [Troops.wizard, Troops.musketeer, Troops.archer]
        air_defense = [Troops.musketeer, Troops.wizard, Troops.minion,Troops.dragon]

        # Ensure Wizard is prioritized in defense
        if Troops.wizard in deployable:
            deploy_list.list_.append((Troops.wizard, (random.randint(-6, 6), random.randint(28, 44))))

        if any(t.target_type == "air" for t in opp_troops):  # If enemy has air units
            defenders = [t for t in deployable if t in air_defense]
        else:
            defenders = [t for t in deployable if t in support]

        if defenders:
            defender = random.choice(defenders)
            deploy_list.list_.append((defender, (random.randint(-6, 6), random.randint(8, 14))))

        tank_choices = [t for t in deployable if t in tanks]
        if tank_choices:
            tank = random.choice(tank_choices)
            deploy_list.list_.append((tank, (random.randint(-8, 8), random.randint(5, 12))))


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


