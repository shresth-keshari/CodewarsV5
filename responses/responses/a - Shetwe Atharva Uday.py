import random
from teams.helper_function import Troops, Utils

team_name = "Brute Force"
troops = [
    Troops.wizard, Troops.minion, Troops.archer, Troops.musketeer,
    Troops.dragon, Troops.skeleton, Troops.valkyrie, Troops.barbarian
]

deploy_list = Troops([])
team_signal = "h, Prince, Knight, Barbarian, Princess"

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def deploy(arena_data: dict):
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

# Initialize Q-learning attributes if not already set
if not hasattr(deploy, "q"):
    deploy.q = {}
    deploy.epsilon = 0.2
    deploy.alpha = 0.1
    deploy.gamma = 0.9
    deploy.prev_state = None
    deploy.prev_action = None
    deploy.prev_tower_health = None

def logic(arena_data: dict):
    global team_signal
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    
    frame = arena_data["MyTower"].game_timer
    
    # Update team signal based on opponent troops
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")]
        if troop.name not in current_names:
            team_signal += f", {troop.name}" if team_signal else troop.name
    
    # Count air and ground opponent troops
    opponent_air = {"Minion", "Dragon", "Musketeer"}
    opponent_ground = {"Prince", "Knight", "Barbarian", "Princess"}
    
    tokens = [token.strip() for token in team_signal.split(",") if token.strip() != "h"]
    count_air = sum(1 for token in tokens if token in opponent_air)
    count_ground = sum(1 for token in tokens if token in opponent_ground)
    
    recommended_counter = None
    if count_ground > count_air:
        recommended_counter = "air"
    elif count_air > count_ground:
        recommended_counter = "ground"
    
    # Game phases
    if frame < 30:
        return  # No deployment in first 30 frames
    
    deployable = my_tower.deployable_troops
    explicit_choice = None
    
    # Early battle: defense-focused strategy
    if 30 <= frame < 300:
        for unit in [Troops.wizard, Troops.archer]:
            if unit in deployable:
                explicit_choice = (unit, (random_x(-5, 5), 0))
                break

    # Late battle: aggressive push
    elif frame >= 1200:
        for unit in [Troops.barbarian, Troops.musketeer]:
            if unit in deployable:
                explicit_choice = (unit, (random_x(10, 25), 0))
                break

    # Mid battle: Deploy based on opponent troop proximity
    if explicit_choice is None:
        tower_pos = getattr(my_tower, "position", (0, 0))
        arena_size = arena_data.get("ArenaSize", 100)
        for opp in opp_troops:
            if hasattr(opp, "position"):
                opp_pos = opp.position
                if abs(opp_pos[0] - tower_pos[0]) < 0.4 * arena_size:
                    for support in [Troops.archer, Troops.skeleton, Troops.minion, Troops.dragon]:
                        if support in deployable:
                            explicit_choice = (support, (opp_pos[0] + random_x(-5, 5), opp_pos[1]))
                            break
            if explicit_choice:
                break

    # Q-learning fallback if no decision is made
    tower_health = getattr(my_tower, "health", 100)
    state = (recommended_counter, len(deployable), tower_health, frame)

    if explicit_choice is None:
        if state not in deploy.q:
            deploy.q[state] = {troop: 0.0 for troop in troops}
        valid_q = {troop: deploy.q[state][troop] for troop in deployable if troop in deploy.q[state]}
        if not valid_q or random.random() < deploy.epsilon:
            chosen = random.choice(deployable)
        else:
            chosen = max(valid_q, key=deploy.q[state].get)

        troop_category = {
            Troops.wizard: "defense",
            Troops.minion: "defense",
            Troops.archer: "support",
            Troops.musketeer: "support",
            Troops.dragon: "support",
            Troops.skeleton: "support",
            Troops.valkyrie: "support",
            Troops.barbarian: "attack"
        }
        category = troop_category.get(chosen, "support")

        if category == "defense":
            deploy_position = (random_x(-5, 5), 0)
        elif category == "attack":
            deploy_position = (random_x(10, 25), 0)
        else:
            deploy_position = (random_x(-10, 10), 0)

        explicit_choice = (chosen, deploy_position)

    # Ensure troop is deployed
    if explicit_choice:
        best_troop, deploy_position = explicit_choice
        deploy_list.list_.append((best_troop, deploy_position))

    # Q-learning update
    if deploy.prev_state is not None and deploy.prev_action is not None:
        reward = -(deploy.prev_tower_health - tower_health)
        prev_state = deploy.prev_state
        prev_action = deploy.prev_action

        if prev_state not in deploy.q:
            deploy.q[prev_state] = {troop: 0.0 for troop in troops}
        if state not in deploy.q:
            deploy.q[state] = {troop: 0.0 for troop in troops}

        current_q = deploy.q[prev_state][prev_action]
        max_future_q = max(deploy.q[state].values())
        deploy.q[prev_state][prev_action] = current_q + deploy.alpha * (reward + deploy.gamma * max_future_q - current_q)

    deploy.prev_state = state
    deploy.prev_action = best_troop
    deploy.prev_tower_health = tower_health