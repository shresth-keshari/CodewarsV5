import random
from teams.helper_function import Troops, Utils

team_name = "Naam me kya rakha hai"
# Our team uses these 8 troops. (Note: Balloon is our key attack unit.)
troops = [
    Troops.wizard, Troops.minion, Troops.knight, Troops.valkyrie,
    Troops.dragon, Troops.giant, Troops.prince, Troops.skeleton
]
deploy_list = Troops([])
team_signal = "h, Prince, Knight, Barbarian, Princess"  # Signal can be updated as needed.

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def deploy(arena_data: dict):
    """
    DON'T TEMPER DEPLOY FUNCTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    my_tower = arena_data["MyTower"]
    opp_tower = arena_data["OppTower"]
    opp_troops = arena_data.get("OppTroops", [])
    my_deployed_troops = arena_data.get("MyTroops", [])
    
    # Make a copy of deployable units for safe manipulation.
    deployable_units = my_tower.deployable_troops.copy()
    
    # ---------------- Emergency Mode ----------------
    # If any opponent troop is very close (y < 25), deploy an emergency unit immediately,
    # but do NOT use Balloon.
    emergency_troop = next((t for t in opp_troops if t.position[1] < 25), None)
    if emergency_troop:
        emergency_unit = next((unit for unit in deployable_units if unit != Troops.balloon), None)
        if emergency_unit:
            deploy_list.list_.append((emergency_unit, emergency_troop.position))
            return

    # ---------------- Mode Determination ----------------
    # Count opponent troops in lower half (y < 50)
    opp_troops_in_lower = sum(1 for t in opp_troops if t.position[1] < 50)
    
    # Use attack mode if our tower’s health is less than or equal to the opponent’s,
    # and if there are fewer than 2 enemy troops in the lower half and fewer than 1 enemy troop in closer range.
    attack_mode = (my_tower.health <= opp_tower.health) and (opp_troops_in_lower < 2)

    # ---------------- Attack Mode (Balloon-Based) ----------------
    if attack_mode:
        # Highest Priority: If Balloon is in our deck AND one of our Wizards is already deployed,
        # then deploy Balloon on the opposite flank.
        if Troops.balloon in deployable_units:
            # Check for our own Wizard among our deployed troops.
            wizard_instance = next((t for t in opp_troops if t.name == Troops.wizard), None)
            if wizard_instance:
                wizard_x = int(wizard_instance.position[0])
                # If Wizard is on the left side (between -25 and -5), deploy Balloon at (25, 50).
                # If Wizard is on the right side (between 5 and 25), deploy Balloon at (-25, 50).
                # If Wizard is between -5 and 5, do NOT deploy Balloon.
                if -25 <= wizard_x <= -5:
                    balloon_x = 25
                elif 5 <= wizard_x <= 25:
                    balloon_x = -25
                else:
                    wizard_instance = None  # Skip Balloon deployment.
                if wizard_instance is not None:
                    balloon_pos = (balloon_x, 50)
                    deploy_list.list_.append((Troops.balloon, balloon_pos))
                    deployable_units.remove(Troops.balloon)
        # Attack Mode Rotation: Deploy remaining attack troops.
        formation_order = [
            Troops.wizard, Troops.prince, Troops.skeleton, Troops.dragon, Troops.giant
        ] * 2  # Repeated cycle.
        max_deployments = 6  # Total units to deploy per wave.
        i = 0
        while len(deploy_list.list_) < max_deployments and i < len(formation_order) * 2:
            candidate = formation_order[i % len(formation_order)]
            i += 1
            if candidate not in deployable_units:
                continue
            pos = (random_x(-15, 15), 5)  # Generic attack position.
            deploy_list.list_.append((candidate, pos))
    # ---------------- Defense Mode ----------------
    else:
        # In defense mode, we target the enemy's troops.
        target_x = 0
        if opp_troops:
            min_y_troop = min(opp_troops, key=lambda t: t.position[1])
            target_x = min_y_troop.position[0]
        # Priority: Deploy Giant as the primary defensive unit if available.
        if Troops.giant in deployable_units:
            deploy_list.list_.append((Troops.giant, (target_x, 0)))
            return
        elif Troops.wizard in deployable_units:
            deploy_list.list_.append((Troops.wizard, (target_x, 0)))
            return
        # Fallback: deploy one of the preferred defensive units.
        for preferred in [Troops.knight,Troops.valkyrie, Troops.dragon, Troops.minion]:
            if preferred in deployable_units:
                deploy_list.list_.append((preferred, (target_x, 0)))
                return

# End of code.