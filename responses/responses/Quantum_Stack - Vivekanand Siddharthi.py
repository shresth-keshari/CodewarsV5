from teams.helper_function import Troops, Utils 

team_name = "Quantum"
troops = [
    Troops.wizard, Troops.minion, Troops.valkyrie, Troops.archer,
    Troops.dragon, Troops.skeleton, Troops.knight, Troops.barbarian
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
    """Handles troop deployment strategy based on game state."""
    
    global team_signal
    my_tower = arena_data["MyTower"]
    opp_tower = arena_data["OppTower"]
    my_troops = arena_data["MyTroops"]
    opp_troops = arena_data["OppTroops"]
    elixir = my_tower.total_elixir
    game_time = my_tower.game_timer

    if len(opp_troops) > 0:
            for enemy in opp_troops:
                distance = ((my_tower.position[0] - enemy.position[0]) ** 2 +
                            (my_tower.position[1] - enemy.position[1]) ** 2) ** 0.5
                

                if distance < 6:
                    if Troops.knight in my_tower.deployable_troops and elixir >= 3:
                        deploy_list.deploy_knight(my_tower.position)
                    elif Troops.barbarian in my_tower.deployable_troops and elixir >= 4:
                        deploy_list.deploy_valkyrie(my_tower.position)
                    elif Troops.archer in my_tower.deployable_troops and elixir >= 3:
                        deploy_list.deploy_barbarian((my_tower.position[0] + 1, my_tower.position[1]))

    tanks = [Troops.valkyrie, Troops.knight]  
    available_tank = next((tank for tank in tanks if tank in my_tower.deployable_troops), None)
    wizard_available = Troops.wizard in my_tower.deployable_troops
    if game_time > 120:
        x = 8
    else:
        x = 9
    if available_tank and wizard_available and elixir >= x:
        if available_tank == Troops.valkyrie:
            deploy_list.list_.extend([
                (Troops.valkyrie, (0, 5)),
                (Troops.wizard, (0, 0))  
            ])
        elif available_tank == Troops.dragon:
             deploy_list.list_.extend([
                (Troops.dragon, (0, 2)),
                (Troops.wizard, (0, 0))  
            ])
        elif available_tank == Troops.knight:
            deploy_list.list_.extend([
                (Troops.knight, (0, 2)),
                (Troops.wizard, (0, 0))  
            ])


    elif available_tank and not wizard_available:
        for troop in my_tower.deployable_troops:
            if troop != available_tank:
                deploy_list.list_.append((troop, (0, 1)))
    elif not available_tank and wizard_available:
        for troop in my_tower.deployable_troops:
            if troop != wizard_available:
                deploy_list.list_.append((troop, (0, 4)))
                deploy_list.deploy_wizard((0,0)) 
    elif not available_tank and not wizard_available:
        if my_tower.deployable_troops:
            deploy_list.list_.append((my_tower.deployable_troops[0], (0, 1)))
