import random, math, copy
from teams.helper_function import Troops, Utils

team_name = "N*gg**s in Pune"
troops = [
    Troops.wizard, Troops.minion, Troops.archer, Troops.prince,                  
    Troops.dragon, Troops.knight, Troops.giant, Troops.skeleton
]
deploy_list = Troops([])
team_signal = " , , , , , , , , , , , , , , , ,0, , , , , , , , , , , , , , , , , , , , , , , , ,0"

def name_to_elixir(x):
    if x in ['Archer','Minion','Knight','Skeleton','Barbarian']:
        return 3
    elif x in ['Dragon','Valkyrie','Musketeer']:
        return 4
    elif x in ['Giant','Balloon','Prince','Wizard']:
        return 5


def getcount(troop,list):
    count=0
    for x in list:
        if x.name == troop:
            count+=1
    return count


def dist_from_tower(A):
    return math.sqrt((A.position[0])**2 + (A.position[1])**2)
        

def fullform(info: list):#list(team_signal) to usable data conversion
    mapping = {
        'P': 'Prince', 'D': 'Dragon', 'W': 'Wizard', 'V': 'Valkyrie',
        'G': 'Giant', 'R': 'Barbarian', 'B': 'Balloon', 'S': 'Skeleton',
        'K': 'Knight', 'A': 'Archer', 'M': 'Minion', 'T': 'Musketeer'
    }
    
    return [mapping.get(i, i) for i in info]  # Replace only if found in mapping

def abbreviate(info: list):#usable data to list(team_signal) conversion
    mapping = {
        'Prince': 'P', 'Dragon': 'D', 'Wizard': 'W', 'Valkyrie': 'V',
        'Giant': 'G', 'Barbarian': 'R', 'Balloon': 'B', 'Skeleton': 'S',
        'Knight': 'K', 'Archer': 'A', 'Minion': 'M', 'Musketeer': 'T'
    }

    return [mapping.get(i, i) for i in info]  # Replace only if found in mapping

def extract_letters(info:str): #converting team_signal to list(team_signal)
    infolist=info.split(",")
    return infolist

def join_letters(letters: list) -> str:
    return ",".join(map(str, letters))  # Ensure all elements are strings

def pad_list(letters: list, desired_length: int):
    # Pad the list with blank spaces if it's too short
    while len(letters) < desired_length:
        letters.append(" ")  # Add a blank space
    
    return letters

def fill_blanks(target_list: list, source_list: list):
    target_set = set(target_list) - {" "}  # Track existing elements, ignoring blanks
    source_index = 0  # Track position in source_list
    existing_entries = []  # List for non-blank existing elements
    new_entries = []  # List for newly filled elements
    blank_count = 0  # Count blanks that can't be filled

    # Process target_list and replace blanks
    for item in target_list:
        if item == " ":  # If it's a blank, try to replace it
            while source_index < len(source_list) and (source_list[source_index] in target_set or source_list[source_index] == " "):
                source_index += 1  # Skip existing elements and blanks

            if source_index < len(source_list):  # If a valid element is found
                new_entries.append(source_list[source_index])  # Fill blank
                target_set.add(source_list[source_index])  # Add to uniqueness check
                source_index += 1  # Move to next source element
            else:
                blank_count += 1  # No valid replacement, keep blank
        else:
            existing_entries.append(item)  # Keep existing elements

    # Return list with remaining blanks at the start, then existing elements, then new ones
    return [" "] * blank_count + existing_entries + new_entries

def rearrange_list(list1: list, list2: list):
    blank_count = list1.count(" ")  # Count blanks in list1
    kept_entries = [item for item in list1 if item not in list2 or item == " "]  # Keep non-matching elements & blanks
    moved_entries = [item for item in list1 if item in list2 and item != " "]  # Move only non-blank matching elements

    return [" "] * blank_count + kept_entries[blank_count:] + moved_entries  # Maintain order & size

def find_changes(old_list: list, new_list: list):
    if len(new_list) < len(old_list):  
        return []  # Ignore update if new list is shorter
    
    # Remove blank spaces (' ') before comparing
    old_set = {item for item in old_list if item != " "}
    new_set = {item for item in new_list if item != " "}
    
    added = list(new_set - old_set)  # Elements in new_list but not in old_list

    return added  # Only return added elements

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

#being dealt with : add/remove uid's from the given list
def add_uid(uid_list,uid):
    if len(uid_list)>=4:
        return
    for i in range(4):
        if uid_list[i] ==' ': #first blank space
          uid_list[i]=uid 
          break 

def remove_dead(alive_list, uid_list):
    for i in range(len(uid_list)):
        if uid_list[i] not in alive_list:
            uid_list[i] = ' '

def deploy(arena_data: dict):
    """
    DON'T TEMPER DEPLOY FUNCTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    global team_signal
    underattack =False
                    
                
    

    troop_names=copy.deepcopy(arena_data["MyTower"].deployable_troops)
    dep_list = [Troops.troops_data[name] for name in troop_names]
    dep_list.sort(key=lambda troop: troop.elixir) # sorts the deep copy based on elixir of current troops

    def find_cheapest():
        if not dep_list:
            return None
        return dep_list.pop(0).name
    
    #find number of attackers in a circle with specified centre and radius
    def count_attackers(centre,radius):
        cnt=0
        for x in arena_data['OppTroops']:
            if math.sqrt((x.position[0]-centre[0])**2 + (x.position[1]-centre[1])**2) <= radius:
                cnt+=1
        return cnt
        
    

        



    
    my_tower = arena_data["MyTower"]
    opp_deployed_troops = [] #list to opponents alive troop
    if len(opp_deployed_troops)<8:
        for opptroop in arena_data["OppTroops"]:
            if opptroop.name not in opp_deployed_troops:
                opp_deployed_troops.append(opptroop.name)
    opp_deployed_troops = pad_list(opp_deployed_troops,8)

    my_deployed_troops = [] #list to hold my alive troops
    if len(my_deployed_troops)<8:
        for mytroop in arena_data["MyTroops"]:
            if mytroop.name not in my_deployed_troops:
                my_deployed_troops.append(mytroop.name)    
    my_deployed_troops = pad_list(my_deployed_troops,8)       

    splash_damage = ['Dragon','Balloon','Wizard','Valkyrie'] #type of damage they deal
    single_damage = ['Archer','Knight','Minion','Skeleton','Musketeer','Giant','Prince','Barbarian']
    tank = ['Giant','Balloon','Valkyrie','Knight','Prince'] #segragation on health, anyone with HP over 1900,giant 5423
    weak = ['Archer','Minion','Skeleton'] # HP below 500,sorted fron highest to lowest
    avg_health = ['Dragon','Wizard','Musketeer','Barbarian']
    group_troop = ['Barbarian','Skeleton','Minion','Archer'] #not making list non-groups but rest all are
    attacks_air = ['Wizard','Dragon','Archer','Minion','Musketeer'] #they attack AIR/GROUND/BUILDING
    attacks_ground = ['Knight','Skeleton','Valkyrie','Prince','Barbarian'] #they attack GROUND/BUILDING
    attack_building = ['Giant','Balloon'] #attacks only BUILDING
    #tower_killable = ['Archer'] #tower kills them if they are alone ##removed minion for now
    air_troops=['Balloon',"Dragon","Minion"]
    
    opp_deployed_troops_short = abbreviate(opp_deployed_troops) #this is a list
    my_deployed_troops_short = abbreviate(my_deployed_troops) #this is a list

    from_teamsignal_list=extract_letters(team_signal) #getting a list from team_signal

    oppdeck_last_short = from_teamsignal_list[:8]  # Copy the first 8 elements
    oppdeck_new_short = fill_blanks(oppdeck_last_short,opp_deployed_troops_short)
    OppDeck = fullform(oppdeck_new_short)

    mydeck_last_short = from_teamsignal_list[8:16]  # Copy the second 8 elements
    mydeck_new_short = fill_blanks(mydeck_last_short,my_deployed_troops_short)
    MyDeck = fullform(mydeck_new_short)

    my_elixir = int(arena_data['MyTower'].total_elixir) #my elixir in a variable
    elixir_difference_last = from_teamsignal_list[16]

    opp_deployed_troops_last = from_teamsignal_list[17:25] #troops that were present on the arena in the last instance
    my_deployed_troops_last = from_teamsignal_list[25:33] #these will be short since they were implemented straight from team_signal
    opp_new_deployment_short = find_changes(opp_deployed_troops_last,opp_deployed_troops_short) #new troops in the arena
    my_new_deployment_short = find_changes(my_deployed_troops_last,my_deployed_troops_short)
    opp_new_deployment = fullform(opp_new_deployment_short)
    my_new_deployment = fullform(my_new_deployment_short)

    being_dealt_with=from_teamsignal_list[33:37]  #atmost 4

    last_troop_deployment=int(from_teamsignal_list[-1])

    #rearranging deck to get deployable cards if they use a new troop
    oppdeck_new_short = rearrange_list(oppdeck_new_short,opp_new_deployment_short)
    mydeck_new_short = rearrange_list(mydeck_new_short,my_new_deployment_short)
    
    elixir_change = 0 #any change in elixir_difference due deployment of new troops
    if opp_new_deployment:
        for x in opp_new_deployment:
           elixir_change-=name_to_elixir(x)
    if my_new_deployment:
        for x in my_new_deployment:
            elixir_change+=name_to_elixir(x)

    elixir_difference_new = int(elixir_difference_last) + elixir_change #updating elixir difference to obtain current opp_elixir
    opp_elixir = my_elixir + elixir_difference_new
    
    opp_deployable_troops = OppDeck[:4] #highly useful when you know entire deck
    opp_next_incycle = OppDeck[4] #this information is only useful after they have deployed 4 cards
    my_deployable_troops = arena_data['MyTower'].deployable_troops
    my_next_incycle = MyDeck[4] #this information is only useful after we have deployed 4 cards

    #actual logic- defense SOS
    attack_factor=0 #centre attack
    for attacker in arena_data['OppTroops']:
        f=1
        if attacker.name == Troops.minion:
            f=0.5
        elif attacker.name == Troops.skeleton:
            f=0.2
        if attacker.position[0] >10:
            attack_factor+=f   #right attack
        elif attacker.position[0]< -10:
            attack_factor-=f  #left attack

    for attacker in list(set(arena_data['OppTroops'])):
        if dist_from_tower(attacker) < 22:
            if attacker.name==Troops.archer or (attacker.name==Troops.skeleton and getcount("Skeleton",arena_data['OppTroops'])<5) or (attacker.name==Troops.barbarian and getcount("Barbarian",arena_data['OppTroops'])<3) or (attacker.name==Troops.minion and getcount("Minion",arena_data['OppTroops'])<3) or (attacker.name in ["Giant","Balloon"] and attacker.health<1200 and count_attackers(attacker.position,15)>3):
                continue

            elif (attacker.health > 474 or (attacker.name==Troops.skeleton and getcount("Skeleton",arena_data['OppTroops'])>=5) or (attacker.name==Troops.barbarian and getcount("Barbarian",arena_data['OppTroops'])==3) or (attacker.name==Troops.minion and getcount("Minion",arena_data['OppTroops'])==3)) and attacker.uid not in being_dealt_with:
                if Troops.troops_data["Giant"] in dep_list and attacker.name not in ["Balloon","Giant"]:
                    deploy_list.list_.append(("Giant",(0,10)))
                    add_uid(being_dealt_with,attacker.uid)
                    continue
                if attacker.name in attacks_air:
                    if Troops.troops_data["Dragon"] in dep_list:
                        deploy_list.list_.append(("Dragon",(0,10)))
                        add_uid(being_dealt_with,attacker.uid)
                        continue
                elif Troops.troops_data["Skeleton"] in dep_list:
                    deploy_list.list_.append(("Skeleton",attacker.position))
                    add_uid(being_dealt_with,attacker.uid)
                    continue       
                elif Troops.troops_data["Knight"] in dep_list:
                    deploy_list.list_.append(("Knight",attacker.position))
                    add_uid(being_dealt_with,attacker.uid)
                    continue
                
            
                elif Troops.troops_data["Wizard"] in dep_list:
                    if attack_factor>0:
                        deploy_list.list_.append(("Wizard",(8,0)))
                        add_uid(being_dealt_with,attacker.uid)
                        continue
                    else:
                        deploy_list.list_.append(("Wizard",(-8,0)))
                        add_uid(being_dealt_with,attacker.uid)
                        continue
                else:
                    deploy_list.list_.append((find_cheapest(),attacker.position))
                    add_uid(being_dealt_with,attacker.uid)
                    continue
       
    #actual logic - attack
    number_left = 0
    number_midleft = 0
    number_mid = 0
    number_midright = 0
    number_right = 0

    deploy_troop_x_position = 0
    deploy_troop_y_position = 0

    seen_troop_types = set()

    # Create a set to store unique troop names
    unique_troops = set()

    # Iterate through opponent troops to collect unique troop names
    for troop in arena_data["OppTroops"]:
        unique_troops.add(troop.name)

    # Get the number of unique troops
    number_of_unique_troops = len(unique_troops)

    
    for x in arena_data["OppTroops"]:
        troop_identifier = (x.name, x.position[0] // 1, x.position[1] // 1)
        if troop_identifier[0] not in seen_troop_types:
            if x.position[0] < -15:
                number_left +=1
            if x.position[0] < -5 and x.position[0]>-15:
                number_midleft +=1
            if x.position[0] > -5 and x.position[0] < 5:
                number_mid += 1
            if x.position[0] > 5 and x.position[0] < 15:
                number_midright += 1
            if x.position[0] > 15:
                number_right += 1
            seen_troop_types.add(x.name)

    pressures = [number_left, number_midleft, number_mid, number_midright, number_right]
    pressured_side = number_mid
    for x in pressures:
        if x > pressured_side:
            pressured_side = x
    #print (pressured_side)
    

    
    if pressured_side == number_left:
        #print ("left enemy")
        deploy_troop_x_position = random_x(-25, -15)
    elif pressured_side == number_midleft:
        #print ("left mid enemy")
        deploy_troop_x_position = random_x(-15,-5)
    elif pressured_side == number_mid:
        #print ("mid enemy")
        deploy_troop_x_position = random_x(-5, 5)
    elif pressured_side == number_midright:
        #print ("right mid enemy")
        deploy_troop_x_position = random_x(5,15)
    elif pressured_side == number_right:
        #print ("right enemy")
        deploy_troop_x_position = random_x(15,25)
        
    if(my_elixir > 8):
        for t in arena_data["OppTroops"]:
            if (55 >= t.position[1] > 33) or (number_of_unique_troops>2):
                for x in my_deployable_troops:
                    if x in opp_deployed_troops:
                        if x in group_troop:
                            break
                    if x in tank:
                        for y in my_deployed_troops:
                            if y in tank:
                                break
                            else:
                                if 'Wizard' in my_deployable_troops or 'Dragon' in my_deployable_troops or 'Wizard' in my_next_incycle or 'Dragon' in my_next_incycle:
                                    if 'Giant' in my_deployable_troops:
                                        deploy_list.list_.append((Troops.giant,(0,15)))
                                    elif 'Prince' in my_deployable_troops:
                                        deploy_list.list_.append((Troops.prince,(deploy_troop_x_position,25)))
                    
    if 'Giant' in my_deployed_troops or 'Prince' in my_deployed_troops:#Giant push
        giant_position = None

        for troop in arena_data["MyTroops"]:    #tracks giant position
            if troop.name == "Giant" or troop.name == 'Prince' or (troop.name == 'Knight' and (troop.position[0]<-20 or troop.position[0]>20)):
                giant_position = troop.position
                break
        
        if giant_position[1] > 40:
            if 'Wizard' in my_deployable_troops:
                deploy_list.list_.append((Troops.wizard,(giant_position[0],max(giant_position[0], giant_position[1]-20))))
            elif 'Dragon' in my_deployable_troops:
                deploy_list.list_.append((Troops.dragon,(giant_position[0],max(giant_position[0] ,giant_position[1]-30))))
        elif giant_position[1] < 30:
            if 'Wizard' in my_deployable_troops:
                deploy_list.list_.append((Troops.wizard,(giant_position[0],max(giant_position[0], 0))))
            elif 'Dragon' in my_deployable_troops:
                deploy_list.list_.append((Troops.dragon,(giant_position[0],max(giant_position[0],0))))

    for t in arena_data["OppTroops"]:
        if(my_elixir == 10 and t.position[1] > 55):
                if len(opp_deployed_troops) == 0:
                    if 'Knight' in my_deployable_troops and 'Wizard' in my_deployable_troops:
                        deploy_list.list_.append((Troops.knight,(-25,32)))
                        deploy_list.list_.append((Troops.wizard,(-25,30)))
                
                for x in arena_data["OppTroops"]:
                    if x.name in group_troop:
                        for y in my_deployable_troops:
                            if y in splash_damage:
                                deploy_list.list_.append((y,(x.position[0],20)))
                            else:
                                deploy_list.list_.append((Troops.knight, (-25, 50))) #risky skibidi
                        break
                    
                    for y in opp_deployable_troops:
                        if y in group_troop:
                                for z in my_deployable_troops:
                                    if z in splash_damage:
                                        deploy_list.list_.append #currently not doing shit since we are using y as opp deployable troops
                    if x.position[1] > 65:
                        if 'Knight' in my_deployable_troops and ('Wizard' in my_deployable_troops or 'Dragon' in my_deployable_troops):
                            deploy_list.list_.append((Troops.knight,(-25,32)))
                            deploy_list.list_.append((Troops.wizard,(-25,30)))
                            deploy_list.list_.append((Troops.dragon, (-25, 22)))
                        elif 'Prince' in my_deployable_troops and ('Wizard' in my_deployable_troops or 'Dragon' in my_deployable_troops):
                            deploy_list.list_.append((Troops.prince,(25,30)))
                            deploy_list.list_.append((Troops.wizard,(15,27)))
                            deploy_list.list_.append((Troops.dragon,(15,30)))
                        elif 'Giant' in my_deployable_troops and ('Wizard' in my_deployable_troops or 'Dragon' in my_deployable_troops):
                            deploy_list.list_.append((Troops.giant,(0,30)))
                            deploy_list.list_.append((Troops.wizard,(10,10)))
                            deploy_list.list_.append((Troops.dragon,(10,10)))
                        else:
                            if 'Giant' in my_deployable_troops:
                                deploy_list.list_.append((Troops.giant, (0,0)))
                            elif 'Prince' in my_deployable_troops:
                                deploy_list.list_.append((Troops.prince, (0,0)))
                            
                    
                    else:
                        for my_troop in arena_data["MyTroops"]:
                            if my_troop.position[1] > 55: #next incycle doesnt add to deploy list but this is kinda good still
                                
                                if 'Wizard' in my_deployable_troops:
                                    deploy_list.list_.append((Troops.wizard,(my_troop.position[0], 50)))
                                if 'Knight' in my_deployable_troops:
                                    deploy_list.list_.append((Troops.knight,(my_troop.position[0], 50)))
                                
                        
                        if 'Wizard' in my_deployable_troops:
                            deploy_list.list_.append((Troops.wizard,(25, 50)))
                        if 'Knight' in my_deployable_troops:
                            deploy_list.list_.append((Troops.knight,(25, 50)))

    #Jumping Strategy
    for attacker in arena_data['OppTroops']:
         if 22<attacker.position[1] <=35 and (attacker.health>474 or(attacker.name==Troops.archer and getcount("Archer",arena_data['OppTroops'])==2 and attacker.health>310)) or (attacker.name==Troops.skeleton and getcount("Skeleton",arena_data['OppTroops'])>=5 or (attacker.name==Troops.minion and getcount("Minion",arena_data['OppTroops'])>=2 and attacker.health>200))  :
            
            if attacker.name not in attacks_air and attacker.name not in being_dealt_with:


                if deploy_list.minion in arena_data['MyTower'].deployable_troops  :
                        deploy_list.deploy_minion(attacker.position)
                        add_uid(being_dealt_with,attacker.uid)
                        continue
                elif list(set(arena_data['MyTower'].deployable_troops )& set(air_troops)):
                        deploy_list.list_.append((list(set(arena_data['MyTower'].deployable_troops )& set(air_troops))[0],attacker.position))
                        add_uid(being_dealt_with,attacker.uid)
                        continue
                
            if attacker.name in air_troops:
                    
                    if deploy_list.minion in arena_data['MyTower'].deployable_troops  :
                        deploy_list.deploy_minion(attacker.position)
                    elif list(set(arena_data['MyTower'].deployable_troops )& set(attacks_air)):
                        deploy_list.list_.append((list(set(arena_data['MyTower'].deployable_troops )& set(attacks_air))[0],attacker.position))

            elif attacker.name not in being_dealt_with: 
                    if deploy_list.knight in arena_data['MyTower'].deployable_troops:
                        deploy_list.deploy_knight((attacker.position[0],attacker.position[1]+7))
                        #add_uid(being_dealt_with,attacker.uid)
                    elif deploy_list.minion in arena_data['MyTower'].deployable_troops  :
                        deploy_list.deploy_minion(attacker.position)
                        #add_uid(being_dealt_with,attacker.uid)
                    else:
                                    
                        if not dep_list:
                            continue
                        elif dep_list[0].name == Troops.wizard or dep_list[0].name ==Troops.archer:
                            deploy_list.list_.append((find_cheapest(),(attacker.position[0],attacker.position[1]-12)))
                        else:
                            deploy_list.list_.append((find_cheapest(),(attacker.position[0],attacker.position[1]-3)))


#(attacker.name in ["Giant","Balloon"] and attacker.health<1200 and count_attackers(attacker.position,15)>3):


    #remove dead troops 
    remove_dead([troop.uid for troop in arena_data['OppTroops']],being_dealt_with)

    if my_new_deployment:
        last_troop_deployment=arena_data['MyTower'].game_timer

    if not arena_data['MyTroops'] and not arena_data['OppTroops']:
        if my_elixir==10: 
            if arena_data['MyTower'].game_timer-last_troop_deployment>=500:
                if 'Giant' in my_deployable_troops:
                    deploy_list.list_.append((Troops.giant,(0,0)))
                elif 'Wizard' in my_deployable_troops:
                    deploy_list.list_.append((Troops.wizard,(0,0)))
                elif 'Dragon' in my_deployable_troops:
                    deploy_list.list_.append((Troops.dragon,(0,0)))
                elif 'Knight' in my_deployable_troops:
                    deploy_list.list_.append((Troops.knight,(0,0)))
                elif 'Prince' in my_deployable_troops:
                    deploy_list.list_.append((Troops.prince,(0,0)))
    
    to_teamsignal_list = oppdeck_new_short + mydeck_new_short + [str(elixir_difference_new)] + opp_deployed_troops_short + my_deployed_troops_short+being_dealt_with + [str(last_troop_deployment)]
    team_signal=join_letters(to_teamsignal_list) #converting list to team_signal

    #print(type([str(last_troop_deployment)]))
    #print(team_signal)
    #print(arena_data['MyTower'].game_timer)
    