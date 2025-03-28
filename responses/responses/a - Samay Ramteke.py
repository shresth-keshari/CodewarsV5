from teams.helper_function import Troops, Utils
import random

team_name = "Logic lords"
troops = [
    Troops.wizard,
    Troops.knight,
    Troops.skeleton,
    Troops.giant,
    Troops.archer,
    Troops.minion,
    Troops.prince,
    Troops.dragon
]
deploy_list = Troops([])
team_signal = ""

def deploy(arena_data: dict):
    """
    DON'T TEMPER DEPLOY FUNCTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    global team_signal
    opp_troops = arena_data["OppTroops"]
    opp_tower = arena_data["OppTower"]
    my_tower = arena_data["MyTower"]

    deployable = my_tower.deployable_troops
    opponent_has_more_health = opp_tower.health >= my_tower.health
    opponent_took_damage = opp_tower.health < my_tower.health

    # If we have damaged the opponent and the enemy is approaching our tower, deploy anything in deck near the tower
    if opponent_took_damage:
        for enemy in opp_troops:
            if enemy.position[1] <= 20:  # Enemy is close to our tower
                for troop in deployable:
                    deploy_list.list_.append((troop, (random.randint(-10, 10), random.randint(10, 20))))
                return

    # Priority Counter: Always Deploy Wizard First If Available
    if Troops.wizard in deployable:
        deploy_list.list_.append((Troops.wizard, (random.randint(-10, 10), random.randint(10, 20))))
        return

    # Counter Opponent's Prince, Wizard, and Valkyrie
    for enemy in opp_troops:
        if enemy == Troops.prince:
            if Troops.prince in deployable:
                deploy_list.list_.append((Troops.prince, (10, 0)))
                return
            elif Troops.knight in deployable:
                knight_y = 20 if enemy.position[1] <= 20 else 50
                deploy_list.list_.append((Troops.knight, (random.randint(-10, 10), knight_y)))
                return
            elif Troops.archer in deployable:
                deploy_list.list_.append((Troops.archer, (10, 0)))
                return

        elif enemy == Troops.wizard:
            if Troops.knight in deployable:
                deploy_list.list_.append((Troops.knight, (random.randint(-10, 10), random.randint(10, 20))))
                return

        elif enemy == Troops.valkyrie:
            if Troops.archer in deployable:
                deploy_list.list_.append((Troops.archer, (random.randint(-10, 10), random.randint(10, 20))))
                return
            elif Troops.skeleton in deployable:
                deploy_list.list_.append((Troops.skeleton, (random.randint(-10, 10), random.randint(10, 20))))
                return

    # If opponent has more or equal health, prioritize Prince
    if opponent_has_more_health:
        if Troops.prince in deployable:
            x_choice = random.choice([-25, 25])
            deploy_list.list_.append((Troops.prince, (x_choice, 50)))

            # If Prince is deployed and no damage has been dealt yet, deploy Wizard behind Prince if available
            if not opponent_took_damage:
                if Troops.wizard in deployable:
                    deploy_list.list_.append((Troops.wizard, (x_choice, 45)))
                elif Troops.skeleton in deployable:
                    deploy_list.list_.append((Troops.skeleton, (x_choice, 45)))
                elif Troops.archer in deployable:
                    deploy_list.list_.append((Troops.archer, (x_choice, 45)))
            return

    # If our tower has more health, prioritize Giant
    if not opponent_has_more_health:
        if Troops.giant in deployable:
            deploy_list.list_.append((Troops.giant, (random.randint(-10, 10), random.randint(10, 20))))
            return

        if Troops.knight in deployable:
            knight_y = 20 if any(enemy.position[1] <= 20 for enemy in opp_troops) else 50
            deploy_list.list_.append((Troops.knight, (random.randint(-10, 10), knight_y)))  
            if Troops.wizard in deployable:
                deploy_list.list_.append((Troops.wizard, (0, 45)))  # Wizard behind Knight
            return

    # Ensure Barbarian Deploys When No Other Priority Troops Are Available
    if Troops.archer in deployable:
        deploy_list.list_.append((Troops.archer, (random.randint(-10, 10), random.randint(10, 20))))
        return

    # Deploy any available troop following priority order
    for troop in [Troops.dragon, Troops.minion, Troops.skeleton]:
        if troop in deployable:
            deploy_list.list_.append((troop, (random.randint(-10, 10), random.randint(10, 20))))
            return