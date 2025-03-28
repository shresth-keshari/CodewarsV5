import random
from teams.helper_function import Troops, Utils
team_name="INSANE"

team_signal = "ADAPTIVE_MODE"
troops = [
    Troops.wizard, Troops.minion, Troops.knight, Troops.valkyrie,
    Troops.dragon, Troops.giant, Troops.prince, Troops.skeleton
]
deploy_list = Troops([])

def deploy(arena_data: dict):
    """DO NOT MODIFY THIS FUNCTION"""
    deploy_list.list_ = []
    logic(arena_data, deploy_list)
    return deploy_list.list_, team_signal

def logic(arena_data: dict, deploy_list: Troops):
    # Strategic positioning constants
    LEFT_FLANK = -25
    RIGHT_FLANK = 25
    CENTER_LINE = 0

    def random_x(min_val=-25, max_val=25):
        return random.randint(min_val, max_val)

    def should_attack(my_tower, opp_tower, opp_troops):
        """Determine if we should switch to attack mode"""
        health_advantage = my_tower.health > opp_tower.health * 1.2
        troop_advantage = len(opp_troops) < 2
        return health_advantage and troop_advantage

    def execute_attack_strategy(deployable, arena_data):
        """Execute coordinated attack with flanking strategy"""
        # Determine optimal flank based on enemy wizard positions
        enemy_wizards = [t for t in arena_data["OppTroops"] if t.type == Troops.wizard]
        preferred_flank = RIGHT_FLANK if any(w.position[0] < CENTER_LINE for w in enemy_wizards) else LEFT_FLANK
        
        # Balloon-Wizard combo
        if Troops.balloon in deployable:
            our_wizards = [t for t in arena_data["MyTroops"] if t.type == Troops.wizard]
            if our_wizards:
                wizard_flank = our_wizards[0].position[0]
                balloon_flank = -wizard_flank
                deploy_list.list_.append((Troops.balloon, (balloon_flank, 50)))
                deployable.remove(Troops.balloon)
        
        # Prince charge with skeleton support
        if Troops.prince in deployable:
            deploy_list.list_.append((Troops.prince, (preferred_flank, 50)))
            if Troops.skeleton in deployable:
                deploy_list.list_.append((Troops.skeleton, (preferred_flank, 50)))
        
        # Wizard support
        if Troops.wizard in deployable:
            deploy_list.list_.append((Troops.wizard, (random_x(-15, 15), 25)))

    def execute_defense_strategy(deployable, opp_troops):
        """Execute layered defense prioritizing tank units"""
        target_x = CENTER_LINE
        if opp_troops:
            frontmost = min(opp_troops, key=lambda t: t.position[1])
            target_x = frontmost.position[0]
        
        # Priority deployment sequence
        defense_priority = [Troops.giant, Troops.wizard, Troops.knight, Troops.valkyrie, Troops.dragon, Troops.minion]
        for troop_type in defense_priority:
            if troop_type in deployable:
                deploy_list.list_.append((troop_type, (target_x, 0)))
                return

    my_tower = arena_data["MyTower"]
    opp_tower = arena_data["OppTower"]
    opp_troops = arena_data.get("OppTroops", [])
    deployable = my_tower.deployable_troops.copy()
    
    if not deployable:
        return

    # Emergency defense against close threats (y < 25)
    emergency_troop = next((t for t in opp_troops if t.position[1] < 25), None)
    if emergency_troop:
        # Deploy any available troop except Balloon at threat position
        emergency_unit = next((unit for unit in deployable if unit != Troops.balloon), None)
        if emergency_unit:
            deploy_list.list_.append((emergency_unit, emergency_troop.position))
            return

    # Mode determination
    attack_mode = should_attack(my_tower, opp_tower, opp_troops)
    
    if attack_mode:
        execute_attack_strategy(deployable, arena_data)
    else:
        execute_defense_strategy(deployable, opp_troops)

    # Fallback deployment if no strategy was triggered
    if not deploy_list.list_ and deployable:
        deploy_list.list_.append((deployable[0], (random_x(), 10)))