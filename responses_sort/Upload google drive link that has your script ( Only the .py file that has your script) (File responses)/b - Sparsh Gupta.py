from teams.helper_function import Troops, Utils

team_name = "Spash Royale"
troops = [
    Troops.giant,
    Troops.wizard,
    Troops.minion,
    Troops.dragon,
    Troops.archer,
    Troops.musketeer,
    Troops.skeleton,
    Troops.valkyrie,
]
deploy_list = Troops([])
team_signal = "||10"

def deploy(arena_data: dict):
    """
    DON'T TEMPER DEPLOY FUCNTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal


def logic(arena_data: dict):
    from collections import OrderedDict
    import random
    from math import exp

    global team_signal
    DEBUG = 10

    my_tower = arena_data["MyTower"]
    my_troops = arena_data["MyTroops"]
    opp_troops = arena_data["OppTroops"]
    troop_data = {
        "Archer":    { "cost": 3, "flags": {'air', 'walk'},           "air_dmg": 2596.0, "gnd_dmg": 2596.0, "hp": 1002.0,   "range": 8 },
        "Minion":    { "cost": 3, "flags": {'fly', 'air'},            "air_dmg": 3096.0, "gnd_dmg": 3096.0, "hp": 907.2,    "range": 4 },
        "Knight":    { "cost": 3, "flags": {'gnd', 'tank', 'walk'},   "air_dmg": 0,      "gnd_dmg": 1326.0, "hp": 1938.0,   "range": 7 },
        "Skeleton":  { "cost": 3, "flags": {'gnd', 'walk'},           "air_dmg": 0,      "gnd_dmg": 5340.0, "hp": 890.0,    "range": 4 },
        "Dragon":    { "cost": 4, "flags": {'splash', 'fly', 'air'},  "air_dmg": 2508.0, "gnd_dmg": 2508.0, "hp": 1710.45,  "range": 5 },
        # "Musketeer": { "cost": 4, "flags": {'air', 'walk'},           "air_dmg": 1434.0, "gnd_dmg": 1434.0, "hp": 1267.2,   "range": 8 },  # original
        "Musketeer": { "cost": 4, "flags": {'air', 'walk'},           "air_dmg": 2034.0, "gnd_dmg": 2034.0, "hp": 1267.2,   "range": 8 },
        # "Valkyrie":  { "cost": 4, "flags": {'splash', 'gnd', 'walk'}, "air_dmg": 0,      "gnd_dmg": 1755.0, "hp": 2097.0,   "range": 7 },  # original
        "Valkyrie":  { "cost": 4, "flags": {'splash', 'gnd', 'walk'}, "air_dmg": 0,      "gnd_dmg": 2155.0, "hp": 2097.0,   "range": 7 },
        "Giant":     { "cost": 5, "flags": {'gnd', 'tank', 'walk'},   "air_dmg": 0,      "gnd_dmg": 674.0,  "hp": 5423.0,   "range": 7 },
        "Prince":    { "cost": 5, "flags": {'gnd', 'charge', 'walk'}, "air_dmg": 0,      "gnd_dmg": 2352.0, "hp": 1920.0,   "range": 5 },
        "Barbarian": { "cost": 3, "flags": {'gnd', 'walk'},           "air_dmg": 0,      "gnd_dmg": 1449.0, "hp": 2208.0,   "range": 5 },
        "Balloon":   { "cost": 5, "flags": {'splash', 'fly', 'gnd'},  "air_dmg": 1908.0, "gnd_dmg": 1908.0, "hp": 2226.0,   "range": 5 },
        "Wizard":    { "cost": 5, "flags": {'splash', 'walk', 'air'}, "air_dmg": 7072.5, "gnd_dmg": 7072.5, "hp": 1705.0,   "range": 8 },
    }

    win_cards = {"Giant", "Balloon"}

    # * based on deck
    my_win_card = "Giant"

    ######################## LOGIC FOR TRACKING ENEMY DECK, OWN CYCLE AND ELIXIR ############################
    # sorted from least recently (part of current deck) to most recently deployed
    # opp_deck has comma seperated value, each value being "troop_name troop_uid1 troop_uid2..."

    opp_deck, my_cycle, opp_elixir = team_signal.split("|")

    opp_deck = opp_deck.split(",")
    my_cycle = list(s for s in my_cycle.split(",") if s)
    opp_elixir = float(opp_elixir)

    _opp_deck = [] if opp_deck == [""] else opp_deck

    # convert opp_deck to ordered dict: troop_name: [troop_uids...] (minimum in case of multi troops)
    # * note using str everywhere
    opp_deck = OrderedDict()
    for a, *b in map(lambda x: x.split(" "), _opp_deck):
        if '' in b:
            b.remove('')
        opp_deck[a] = b

    # increment on per frame basis
    opp_elixir += 0.05
    double_elixir = False
    if my_tower.game_timer > 1200:
        double_elixir = True
        opp_elixir += 0.05
    opp_elixir = min(opp_elixir, 10)

    new_opp_troop = None

    # return whether troop with given name (and optional uid) is in deployed opp troops
    def check_deployed(name, uid=None):
        for opp_troop in opp_troops:
            if opp_troop.name == name and (uid is None or str(opp_troop.uid) == uid):
                return True
        return False

    # first, remove any troops previously added to opp_deck but not deployed anymore
    for seen_name in opp_deck:
        for seen_uid in opp_deck[seen_name]:
            # if same name, uid is not deployed anymore, remove uid
            if not check_deployed(seen_name, seen_uid):
                opp_deck[seen_name].remove(seen_uid)

    # next, iterate over deployed troops and add/update
    for opp in opp_troops:
        # if troop not seen, add it (not with uid)
        if opp.name not in opp_deck:
            opp_deck[opp.name] = []

        # atp troop must be in opp deck

        # if same name, different uid is deployed, append uid and move to first
        if str(opp.uid) not in opp_deck[opp.name]:
            opp_deck[opp.name].append(str(opp.uid))
            opp_deck.move_to_end(opp.name)
            new_opp_troop = opp.name

    # remove opp elixir by that of new troop
    opp_elixir -= troop_data[new_opp_troop]["cost"] if new_opp_troop else 0

    # ! if counting duplicates, may lead to erroneus calculation for multi troop entities
    opp_troop_names = set(opp.name for opp in opp_troops)
    my_troop_names = set(my.name for my in my_troops)
    
    opp_cycle = [t for i,t in enumerate(opp_deck) if len(opp_deck) - i > 4]
    my_elixir = my_tower.total_elixir
    hand = my_tower.deployable_troops

    
    def random_position_near(position):
        x = position[0] + random.randint(-5, 5)
        y = position[1] + random.randint(0, 5)    
        return (max(-25, min(49, x)), max(-25, min(49, y)))

    def random_position_forward(position):
        x = position[0] + random.randint(-25, 25)
        y = position[1] + random.randint(0, 10)
        return (max(-25, min(49, x)), max(-25, min(49, y)))


        
    if my_win_card in my_tower.deployable_troops and my_elixir >= troop_data[my_win_card]["cost"]:
        win_troops = [t for t in my_troops if t.name == my_win_card]
        if len(win_troops) < 1:
            deploy_list.list_.append((my_win_card, random_position_forward(my_tower.position)))
            return
        
    CYCLE_THREAT_SCALING = 0.30              # (was 0.25)
    CYCLE_THREAT_ELIXIR_SCALING = 0.25       # (was 0.20)

    DOUBLE_ELIXIR_SCALING = 0.8

    THREAT_WEIGHT_FLYATK = 0.8 / 1000        # (was 1.2/1000)
    THREAT_WEIGHT_WALKATK = 1.4 / 1000       # (was 1.1/1000)
    THREAT_WEIGHT_AIRDEF = 1.1 / 1000        # (was 1.2/1000)
    THREAT_WEIGHT_GNDDEF = 1.5 / 1000        # (was 1.2/1000)

    # Re-enable a modest elixir penalty to factor in resource differences
    ELIXIR_WEIGHT = 0                   # (was 0)

    # Adjust threat thresholds (increasing high-threat thresholds prevents overreacting)
    AIR_THREAT_THRESHOLD_MOD = 10
    GND_THREAT_THRESHOLD_MOD = 12
    AIR_THREAT_THRESHOLD_HIGH = 13         # (was 10)
    GND_THREAT_THRESHOLD_HIGH = 15         # (was 10)

    # Elixir thresholds for decision-making
    MY_ELIXIR_THRESHOLD = 5                 # (was 6)
    OPP_ELIXIR_THRESHOLD = 3                # remains unchanged

    # Lower win counter thresholds to deploy win cards slightly earlier
    WIN_COUNTER_THRESHOLDS = {
        "Giant": 8,                        # (was 10)
        "Balloon": 8                       # (was 10)
    }

    EARLY_GAME_TICKS = 300  # (30 seconds at 10 ticks/second)

    # Role-specific weights – push offense a bit more and balance defense
    ROLE_WEIGHTS = {
        "DEFENSE": {"atk": 0.6, "def": 1.4},
        "OFFENSE": {"atk": 1.2, "def": 0.7},
        "NEUTRAL": {"atk": 1.0, "def": 1.0},
    }

    # Lower the threshold for long-term strategy so the bot is less “picky”
    SCORE_THRESHOLD_FACTOR = 1.1            # (was 1.2 or 1.35 in previous iterations)

    # Increase elixir offset to smooth out cost variations
    ELIXIR_OFFSET = 3                        # (was 2)

    SPLASH_PENALIZED_TROOPS = (Troops.skeleton)
    SPLASH_DMG_PENALTY = 150

    # ! temporary
    win_counter = 0
    
    def compute_raw_threats(troop_list):
        air = 0  # air attack capability
        gnd = 0  # gnd attack capability
        fly = 0  # air hp
        walk = 0  # gnd hp
        for t in troop_list:
            if t not in troop_data:
                continue
            flags, air_dmg, gnd_dmg, hp, cost = troop_data[t]["flags"], troop_data[t]["air_dmg"], troop_data[t]["gnd_dmg"], troop_data[t]["hp"], troop_data[t]["cost"]

            gnd += gnd_dmg
            if "air" in flags:
                air += air_dmg

            if "walk" in flags:
                walk += hp
            elif "fly" in flags:
                fly += hp

        return air, gnd, fly, walk

    def compute_threats(troop_names, cycle):
        """
        Returns FlyAtk, WalkAtk, AirDef, GndDef attacks.
        """
        # Threat from currently deployed enemy troops (full weight)
        fly_deployed, walk_deployed, air_deployed, gnd_deployed = compute_raw_threats(troop_names)

        # Threat from enemy cycle (half weight, as they are not yet in play)
        # should scale (slowly) with opp elixir
        fly_cycle, walk_cycle, air_cycle, gnd_cycle = compute_raw_threats(cycle)

        cycle_factor = CYCLE_THREAT_SCALING * (1 + opp_elixir * CYCLE_THREAT_ELIXIR_SCALING)

        fly_cycle *= cycle_factor
        walk_cycle *= cycle_factor
        air_cycle *= cycle_factor
        gnd_cycle *= cycle_factor

        threat_fly_atk = (fly_deployed + fly_cycle) * THREAT_WEIGHT_FLYATK  # air attack capability (relevant for def)
        threat_walk_atk = (walk_deployed + walk_cycle) * THREAT_WEIGHT_WALKATK  # gnd attack capability (relevant for def)
        threat_air_def = (air_deployed + air_cycle) * THREAT_WEIGHT_AIRDEF  # air hp (relevant for off)
        threat_gnd_def = (gnd_deployed + gnd_cycle) * THREAT_WEIGHT_GNDDEF  # gnd hp (relevant for off)

        # Incorporate elixir advantage: if you have more elixir, enemy threat is comparatively less dangerous.
        elixir_diff = my_elixir - opp_elixir
        if double_elixir:
            elixir_diff *= DOUBLE_ELIXIR_SCALING  # dampen the impact in double elixir mode

        threat_fly_atk = threat_fly_atk - (elixir_diff * ELIXIR_WEIGHT)
        threat_walk_atk = threat_walk_atk - (elixir_diff * ELIXIR_WEIGHT)
        threat_air_def = threat_air_def - (elixir_diff * ELIXIR_WEIGHT)
        threat_gnd_def = threat_gnd_def - (elixir_diff * ELIXIR_WEIGHT)
        
        return (threat_fly_atk, threat_walk_atk, threat_air_def, threat_gnd_def)

    
    def compute_effective_threats(_opp_troop_names, _opp_cycle, _my_troop_names, _my_cycle):
        opp_threats = compute_threats(_opp_troop_names, _opp_cycle)
        
        my_threats = compute_threats(_my_troop_names, _my_cycle)
        threats = (
            opp_threats[0] - my_threats[2],
            opp_threats[1] - my_threats[3],
            opp_threats[2] - my_threats[0],
            opp_threats[3] - my_threats[1]
        )
        return threats


    def assess_threat_level():
        threats = compute_effective_threats(opp_troop_names, opp_cycle, my_troop_names, my_cycle)

        threat_win = False
        for i in win_cards:
            if i in opp_troop_names:
                threat_win = True

                # if already deployed sufficient counter for win troop then stop doing so
                if win_counter > WIN_COUNTER_THRESHOLDS[i]:
                    threat_win = False

        return *threats, threat_win


    def determine_role(threat_fly_atk, threat_walk_atk, threat_air_def, threat_gnd_def, threat_win):

        def stable_sigmoid(x):
            if x >= 0:
                z = exp(-x)
                return 1 / (1 + z)
            else:
                z = exp(x)
                return z / (1 + z)

        k = 0.1

        # 0 → prefer ground troops for defense, 1 → prefer flying troops for defense
        def_pref = stable_sigmoid(k * (threat_walk_atk - threat_fly_atk))
        # def_pref = threat_walk_atk / (threat_fly_atk + threat_walk_atk) if (threat_fly_atk + threat_walk_atk) else 0.5

        # 0 → prioritize gnd dmg, 1 → prioritize air dmg
        atk_pref = stable_sigmoid(k * (threat_air_def - threat_gnd_def))
        # atk_pref = threat_air_def / (threat_air_def + threat_gnd_def) if (threat_air_def + threat_gnd_def) else 0.5

        # Determine role based on threats and elixir
        moderate_threat = threat_fly_atk > AIR_THREAT_THRESHOLD_MOD or threat_walk_atk > GND_THREAT_THRESHOLD_MOD
        high_threat = threat_fly_atk > AIR_THREAT_THRESHOLD_HIGH or threat_walk_atk > GND_THREAT_THRESHOLD_HIGH

        win_card_in_hand = my_win_card in hand
        win_card_deployed = my_win_card in my_troops

        role = "NEUTRAL"

        # ATTACK if low threat and win card and sufficient elixir
        if not moderate_threat and win_card_in_hand and my_elixir > MY_ELIXIR_THRESHOLD:
            role = "ATTACK"
        # DEFENSE if high threat and or not win card
        elif high_threat or not win_card_in_hand:
            role = "DEFENSE"
        # NEUTRAL if early game or too little elixir (implied that threat is not high)
        elif my_elixir < MY_ELIXIR_THRESHOLD and my_tower.game_timer < EARLY_GAME_TICKS:
            role = "NEUTRAL"
        # OFFENSE if threat is not high (implied) and enemy low on elixir or we have win card deployed
        elif opp_elixir < OPP_ELIXIR_THRESHOLD or win_card_deployed:
            role = "OFFENSE"

        return role, def_pref, atk_pref


    def compute_best_troop(role, atk_pref, def_pref):
        # ATTACK MODE: Always deploy win_card if elixir is sufficient
        if role == "ATTACK":
            if my_win_card in hand and troop_data[my_win_card]["cost"] <= my_elixir:
                return my_win_card
            return None  # Wait for elixir

        # Weights for different modes
        role_weights = ROLE_WEIGHTS.get(role, ROLE_WEIGHTS["NEUTRAL"])
        role_atk_weight = role_weights["atk"]
        role_def_weight = role_weights["def"]

        # Consider both current hand and next 2 cycle troops
        all_troops = hand + my_cycle[:-2]
        troop_scores = {}

        for troop in all_troops:
            if troop not in troop_data:
                continue
            data = troop_data[troop]
            cost = data["cost"]
            air_dmg = data["air_dmg"]
            gnd_dmg = data["gnd_dmg"]
            hp = data["hp"]
            flags = data["flags"]

            # Calculate attack and defense components as before
            atk_score = atk_pref * air_dmg + (1 - atk_pref) * gnd_dmg
            def_score = def_pref * hp if "fly" in flags else (1 - def_pref) * hp

            # Instead of dividing by cost, use a multiplier that dampens variation:
            # multiplier = (ELIXIR_OFFSET + my_elixir) / (ELIXIR_OFFSET + cost)
            multiplier = (ELIXIR_OFFSET + my_elixir) / (ELIXIR_OFFSET + cost)
            score = (role_atk_weight * atk_score + role_def_weight * def_score) * multiplier

            troop_scores[troop] = (score, cost)
            
        # splash
        for t in hand:
            if "splash" in troop_data[t]["flags"]:
                for tt in SPLASH_PENALIZED_TROOPS:
                    if tt in troop_scores:
                        troop_scores[tt][0] = -SPLASH_DMG_PENALTY


        # Best troop overall
        best_troop, (best_score, best_cost) = max(
            troop_scores.items(), key=lambda x: x[1][0]
        )

        # Best deployable troop (affordable troops only)
        deployable_troops = {t: v for t, v in troop_scores.items() if v[1] <= my_elixir and t in hand}
        if deployable_troops:
            best_deployable, (best_deployable_score, _) = max(
                deployable_troops.items(), key=lambda x: x[1][0]
            )
        else:
            best_deployable, best_deployable_score = None, -float("inf")

        # Apply long-term strategy if the best troop is significantly better
        if best_score > best_deployable_score * SCORE_THRESHOLD_FACTOR:
            if best_troop in hand and best_cost > my_elixir:
                return None  # Wait for elixir
            elif best_troop in my_cycle:
                # Deploy cheapest troop (with best score) to cycle towards best troop
                low_cost_troops = sorted(deployable_troops.items(), key=lambda x: (x[1][1], -x[1][0]))
                if low_cost_troops:
                    best_cycle_troop = low_cost_troops[0][0]
                    return best_cycle_troop
        
        if not best_deployable and random.random() > 0.6 and role == "DEFENSE":
            troop_scores.pop(best_troop, None)
            _t, (_s, _c) = max(
                troop_scores.items(), key=lambda x: x[1][0]
            )
            if (_c <= my_elixir and best_deployable in hand):
                best_deployable = _t
        
        return best_deployable

    threat_fly_atk, threat_walk_atk, threat_air_def, threat_gnd_def, threat_win = assess_threat_level()
    role, def_pref, atk_pref = determine_role(threat_fly_atk, threat_walk_atk, threat_air_def, threat_gnd_def, threat_win)

    best_troop = compute_best_troop(role, def_pref, atk_pref)

    _ = deploy_list.list_.append((best_troop, ((random.random() - 0.5) * 40, 20))) if best_troop else None

    _ = my_cycle.append(best_troop) if best_troop else None
    my_cycle = my_cycle[-4:]
    team_signal = ",".join(k + " " + " ".join(v) for k, v in opp_deck.items())
    team_signal += "|"
    team_signal += ",".join(i for i in my_cycle if i)
    team_signal += f"|{opp_elixir:.3f}"
