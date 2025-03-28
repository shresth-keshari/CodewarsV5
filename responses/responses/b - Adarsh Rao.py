import random
from teams.helper_function import Troops, Utils

team_name = "Opera_House"
troops = [Troops.wizard, Troops.minion, Troops.giant, Troops.valkyrie,
          Troops.dragon, Troops.skeleton, Troops.barbarian, Troops.prince]
deploy_list = Troops([])
team_signal = ""


def deploy(arena_data: dict):
    """
    DON'T TEMPER DEPLOY FUCNTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal


def logic(arena_data: dict):
    global team_signal
    my_tower = arena_data["MyTower"]
    opp_tower = arena_data["OppTower"]
    opp_troops = arena_data["OppTroops"]
    my_troops = arena_data["MyTroops"]
    for troop in opp_troops:
        current_names = [name.strip()
                         for name in team_signal.split(",")] if team_signal else []
        if troop.name not in current_names:
            team_signal = team_signal + ", " + troop.name if team_signal else troop.name

    defense = [Troops.wizard, Troops.skeleton,Troops.dragon,
               Troops.giant, Troops.minion, Troops.barbarian]
    attack = [Troops.prince, Troops.skeleton]
    opposition_air_attack = [Troops.minion, Troops.dragon, Troops.balloon]
    air_defense = [Troops.dragon, Troops.wizard, Troops.minion]
    deployable = my_tower.deployable_troops
    count1 = 0
    count2 = 0
    strategy = "defense"
    is_opponent_air_attacking = False

    if my_tower.game_timer > 1740 and opp_tower.health == my_tower.health:
        for troop in deployable:
            deploy_list.list_.append(
                (troop, (random.choice([-25, 25, 0]), 50)))
    for troop in opp_troops:
        troop_position = troop.position
        if (troop_position[0] < 0):
            count1 += 1
        if (troop_position[0] > 0):
            count2 += 1
        if (troop in opposition_air_attack):
            is_opponent_air_attacking = True
        if ((count1 + count2 >= 2) or troop.name == "wizard" or troop.name == "prince"):
            strategy = "defense"
            break
            
    if ((Troops.prince in deployable) or (Troops.skeleton in deployable)):
        if (len(opp_troops) <= 2 or opp_tower.health == my_tower.health):
            strategy = "attack"
    if (opp_tower.health < my_tower.health):
        defense[0] = Troops.wizard
        defense[1] = Troops.dragon
        defense[2] = Troops.giant
        defense[3] = Troops.skeleton
    else:
        defense[0] = Troops.wizard
        defense[1] = Troops.skeleton
        defense[2] = Troops.dragon
        defense[3] = Troops.giant

    if (strategy == "defense"):
        if (is_opponent_air_attacking):
            for my_troops in air_defense:
                if (my_troops in deployable) and (my_troops.name != "giant" or my_tower.total_elixir > 6):
                    if (count1 > count2):
                        deploy_list.list_.append(
                            (my_troops, (random.randint(0, -15), 15)))
                    else:
                        deploy_list.list_.append(
                            (my_troops, (random.randint(0, 15), 15)))
        else:
            for my_troops in defense:
                if my_troops in deployable:
                    if (count1 > count2):
                        deploy_list.list_.append(
                            (my_troops, (random.choice([0, -15]), 15)))
                    else:
                        deploy_list.list_.append(
                            (my_troops, (random.choice([0, 15]), 15)))

    elif (strategy == "attack"):
        my_troops_position = random.choice([-25, 25])
        for my_troops in attack:
            if (my_troops in deployable):
                for troop in opp_troops:
                    if (troop not in {Troops.wizard, Troops.valkyrie}):
                        my_troops_position = random.choice([-25, 25])

                    else:
                        position_troop = troop.position
                        if (position_troop[0] >= 0):
                            my_troops_position = -25

                        else:
                            my_troops_position = 25

                deploy_list.list_.append((my_troops, (my_troops_position, 50)))