import random
from teams.helper_function import Troops, Utils

team_name = "Cheme Bots"
troops = [
    Troops.wizard, Troops.minion, Troops.archer, Troops.giant,
    Troops.dragon, Troops.knight, Troops.valkyrie, Troops.prince
]
deploy_list = Troops([])
team_signal = "h, Prince, Knight, Barbarian, Princess"

def in_myrange(my_troops,l,d):
   n=[]
   for troop in my_troops:
      if troop.position[1]<d and troop.name in l:
         n.append(troop)
   return n     
         
def can_deploy(My_troops,opptroop,searchlist):
   a=True
   for mytroop in My_troops:
      if mytroop.name in searchlist:
          if Utils.is_in_range(mytroop,opptroop,mytroop.attack_range+3) :
           a=False
   return a

def deploy(arena_data:dict):
    """
    DON'T TEMPER DEPLOY FUCNTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    global team_signal    
    global x 
    global a
    Tower_range=20 
    global n   
    
    if arena_data["MyTower"].game_timer<=1200:
      if arena_data["MyTower"].game_timer == 0:
        x = 10
        n=0  
        a=" "
      elif (arena_data["MyTower"].game_timer)%20==0 :
        x=x+1
    else:
      if (arena_data["MyTower"].game_timer)%10==0 :
          x=x+1     
    opp_troops = arena_data["OppTroops"]
    my_tower=arena_data["MyTower"]
    my_troops=arena_data["MyTroops"]
    global prev_opp_troops
    if arena_data["MyTower"].game_timer==0:
        prev_opp_troops=[]

    D={
      "Archer" : 3,
      "Giant":5,
      "Dragon":4,
      "Balloon":5,
      "Prince":5,
      "Barbarian":3,
      "Knight":3,
      "Minion":3,
      "Skeleton":3,
      "Wizard":5,
      "Valkyrie":4,
      "Musketeer":4}

    if arena_data["MyTower"].game_timer == 1:
        for troop in list(set(opp_troops)):
            x = x - troop.elixir
    elif arena_data["MyTower"].game_timer > 0:
        set1 = set(troop.name for troop in prev_opp_troops)
        set2 = set(troop.name for troop in opp_troops)
        new_elements = set2 - set1        
        for i in list(new_elements):
            x = x - D[i]
    prev_opp_troops = opp_troops            
    deployable = my_tower.deployable_troops
            
    if arena_data["MyTower"].game_timer>1400 and (arena_data["MyTower"].health>=arena_data["OppTower"].health):    
       None

    elif arena_data["MyTower"].game_timer>1400 and (arena_data["MyTower"].health<arena_data["OppTower"].health):
      t=[]
      p=[]
      for i in opp_troops:
        t.append(i.position[0])
        p.append(i.position[1])
      if all(a >=0 for a in t) and all(a>=55 for a in p):
                        if Troops.prince in deployable:
                           deploy_list.list_.append((Troops.prince,(-25,50)))
                        elif Troops.wizard in deployable:
                           deploy_list.list_.append((Troops.wizard,(-25,50))) 
                        elif Troops.dragon in deployable:
                           deploy_list.list_.append((Troops.dragon,(-25,50))) 
                        elif Troops.knight in deployable:
                           deploy_list.list_.append((Troops.knight,(-25,50)))   
                        elif Troops.valkyrie in deployable:
                           deploy_list.list_.append((Troops.valkyrie,(-25,50)))  

      elif all(a <=0 for a in t) and all(a>=55 for a in p):     
                        if Troops.prince in deployable:
                           deploy_list.list_.append((Troops.prince,(25,50)))
                        elif Troops.wizard in deployable:
                           deploy_list.list_.append((Troops.wizard,(25,50))) 
                        elif Troops.dragon in deployable:
                           deploy_list.list_.append((Troops.dragon,(25,50))) 
                        elif Troops.knight in deployable:
                           deploy_list.list_.append((Troops.knight,(25,50)))   
                        elif Troops.valkyrie in deployable:
                           deploy_list.list_.append((Troops.valkyrie,(25,50)))    

      elif all(a >=0 for a in t) and all(a<=50 for a in p):         
                        if Troops.prince in deployable:
                           deploy_list.list_.append((Troops.prince,(random.randit(-20,0),50)))
                        elif Troops.wizard in deployable:
                           deploy_list.list_.append((Troops.wizard,(random.randit(-20,0),50))) 
                        elif Troops.dragon in deployable:
                           deploy_list.list_.append((Troops.dragon,(random.randit(-20,0),50))) 
                        elif Troops.knight in deployable:
                           deploy_list.list_.append((Troops.knight,(random.randit(-20,0),50)))   
                        elif Troops.valkyrie in deployable:
                           deploy_list.list_.append((Troops.valkyrie,(random.randit(-20,0),50)))                   
                           
      elif all(a <=0 for a in t) and all(a<=50 for a in p):         
                        if Troops.prince in deployable:
                           deploy_list.list_.append((Troops.prince,(random.randit(20,0),50)))
                        elif Troops.wizard in deployable:
                           deploy_list.list_.append((Troops.wizard,(random.randit(20,0),50))) 
                        elif Troops.dragon in deployable:
                           deploy_list.list_.append((Troops.dragon,(random.randit(20,0),50))) 
                        elif Troops.knight in deployable:
                           deploy_list.list_.append((Troops.knight,(random.randit(20,0),50)))   
                        elif Troops.valkyrie in deployable:
                           deploy_list.list_.append((Troops.valkyrie,(random.randit(20,0),50))) 



      if arena_data["MyTower"].game_timer>1600 and (arena_data["MyTower"].health>=arena_data["OppTower"].health):       
          None
      elif arena_data["MyTower"].game_timer>1600 and (arena_data["MyTower"].health<arena_data["OppTower"].health): 
          t=[]
          p=[]
          for i in opp_troops:
           t.append(i.position[0])
           p.append(i.position[1])
          if all(a >=0 for a in t) and all(a<=55 for a in p):
                        if Troops.prince in deployable:
                           deploy_list.list_.append((Troops.prince,(-25,50)))
                        elif Troops.wizard in deployable:
                           deploy_list.list_.append((Troops.wizard,(-20,50))) 
                        elif Troops.dragon in deployable:
                           deploy_list.list_.append((Troops.dragon,(-20,50))) 
                        elif Troops.knight in deployable:
                           deploy_list.list_.append((Troops.knight,(-20,50)))   
                        elif Troops.valkyrie in deployable:
                           deploy_list.list_.append((Troops.valkyrie,(-20,50)))  

          elif all(a <=0 for a in t) and all(a<=55 for a in p):     
                         if Troops.prince in deployable:
                           deploy_list.list_.append((Troops.prince,(25,50)))
                         elif Troops.wizard in deployable:
                           deploy_list.list_.append((Troops.wizard,(20,50))) 
                         elif Troops.dragon in deployable:
                           deploy_list.list_.append((Troops.dragon,(20,50))) 
                         elif Troops.knight in deployable:
                           deploy_list.list_.append((Troops.knight,(20,50)))   
                         elif Troops.valkyrie in deployable:
                           deploy_list.list_.append((Troops.valkyrie,(20,50)))    

          elif all(a >=0 for a in t) and all(a<=50 for a in p):         
                        if Troops.prince in deployable:
                           deploy_list.list_.append((Troops.prince,(random.randit(-25,0),50)))
                        elif Troops.wizard in deployable:
                           deploy_list.list_.append((Troops.wizard,(random.randit(-20,0),50))) 
                        elif Troops.dragon in deployable:
                           deploy_list.list_.append((Troops.dragon,(random.randit(-20,0),50))) 
                        elif Troops.knight in deployable:
                           deploy_list.list_.append((Troops.knight,(random.randit(-20,0),50)))   
                        elif Troops.valkyrie in deployable:
                           deploy_list.list_.append((Troops.valkyrie,(random.randit(-20,0),50)))                   
                           
          elif all(a <=0 for a in t) and all(a<=50 for a in p):         
                        if Troops.prince in deployable:
                           deploy_list.list_.append((Troops.prince,(random.randit(20,0),50)))   
                        elif Troops.wizard in deployable:
                           deploy_list.list_.append((Troops.wizard,(random.randit(20,0),50))) 
                        elif Troops.dragon in deployable:
                           deploy_list.list_.append((Troops.dragon,(random.randit(20,0),50))) 
                        elif Troops.knight in deployable:
                           deploy_list.list_.append((Troops.knight,(random.randit(20,0),50)))   
                        elif Troops.valkyrie in deployable:
                           deploy_list.list_.append((Troops.valkyrie,(random.randit(20,0),50))) 

          else :
                       if Troops.prince in deployable:
                           deploy_list.list_.append((Troops.prince,(0,50)))
                       elif Troops.wizard in deployable:
                           deploy_list.list_.append((Troops.wizard,(0,50))) 
                       elif Troops.dragon in deployable:
                           deploy_list.list_.append((Troops.dragon,(0,50))) 
                       elif Troops.knight in deployable:
                           deploy_list.list_.append((Troops.knight,(0,50)))   
                       elif Troops.valkyrie in deployable:
                           deploy_list.list_.append((Troops.valkyrie,(0,50)))  
                       elif Troops.minion in deployable:
                           deploy_list.list_.append((Troops.minion,(0,50)))  
                       elif Troops.archer in deployable:
                           deploy_list.list_.append((Troops.archer,(0,50)))
  
    for opptroop in arena_data["OppTroops"]:
      if opptroop.name=="Wizard" and opptroop.position[1]<50:
        if can_deploy(arena_data["MyTroops"],opptroop,["Knight","Valkyrie"]):    
         if Troops.knight in deployable:         
            deploy_list.deploy_knight(opptroop.position)
            if Troops.archer in deployable:         
             deploy_list.list_.append((Troops.archer,(opptroop.position[0],opptroop.position[1]-9))) 
         elif Troops.valkyrie in deployable:
            deploy_list.deploy_valkyrie(opptroop.position)
            if Troops.archer in deployable:         
                 deploy_list.list_.append((Troops.archer,(opptroop.position[0],opptroop.position[1]-9)))  

#red_zone
    in_tower_range=0
    for i in opp_troops:
       
       if i.position[1]<=Tower_range and (i.name!=a or in_tower_range==0):
          in_tower_range+=1
          a=i.name
    if in_tower_range>=2:
        if Troops.giant in deployable:
          deploy_list.list_.append((Troops.giant,(0,10)))# position to be declare
        if Troops.valkyrie in deployable:
          deploy_list.list_.append((Troops.valkyrie,(0,10)))# position to be declare
        elif Troops.dragon in deployable:
          deploy_list.list_.append((Troops.dragon,(0,10)))# position to be declare 
        elif Troops.wizard in deployable:
          deploy_list.list_.append((Troops.wizard,(0,10)))# position to be declare 
        elif Troops.prince in deployable:
          deploy_list.list_.append((Troops.prince,(0,10)))# position to be declare
        elif Troops.knight in deployable:
          deploy_list.list_.append((Troops.knight,(0,10)))# position to be declare  

    for i in opp_troops:
     if i.name=="Prince" and i.position[1]<50:
        if can_deploy(arena_data["MyTroops"],i,["Minion","Valkyrie","Dragon","Wizard"]):
         if Troops.minion in deployable:
          deploy_list.list_.append((Troops.minion,(i.position[0],i.position[1]-6.5)))
         elif Troops.dragon in deployable:
          deploy_list.list_.append((Troops.dragon,(i.position[0],i.position[1]-3.8)))
         elif Troops.valkyrie in deployable:
           deploy_list.list_.append((Troops.valkyrie,(i.position)))
         elif Troops.wizard in deployable:
           deploy_list.list_.append((Troops.wizard,(i.position[0],i.position[1]-10.3)))
         elif i.health>=1000:    
           if Troops.knight in deployable and  i.position[1]<30:
              deploy_list.list_.append((Troops.knight,i.position)) 

     if i.name=="Balloon":
         if i.position[1]<=38:
          if can_deploy(arena_data["MyTroops"],i,["Minion","Archer","Dragon","Wizard"]):
           if Troops.minion in deployable:
             deploy_list.list_.append((Troops.minion,(i.position)))
           elif Troops.wizard in deployable:
             deploy_list.list_.append((Troops.wizard,(i.position[0],24)))
           elif Troops.dragon in deployable:
             deploy_list.list_.append((Troops.dragon,(i.position[0],30)))
           elif Troops.archer in deployable:
             deploy_list.list_.append((Troops.archer,(i.position[0],28)))             
    #single defense
    #(red)
    for i in opp_troops:
      if in_tower_range==1:
       if i.name=="Dragon" and i.position[1]<23 and i.health>=131:
        if can_deploy(arena_data["MyTroops"],i,["Minion","Valkyrie","Archer","Wizard","Dragon"]):
            if Troops.minion in deployable:
               deploy_list.list_.append((Troops.minion,(i.position[0],i.position[1]-3.8)))
            elif Troops.wizard in deployable:
             deploy_list.list_.append((Troops.wizard,(i.position[0],i.position[1]-10)))   
            elif Troops.dragon in deployable:
             deploy_list.list_.append((Troops.dragon,(i.position[0],i.position[1]-6.5))) 
            elif Troops.archer in deployable:
             deploy_list.list_.append((Troops.archer,(i.position[0],i.position[1]-9.3)))     
            elif Troops.valkyrie in deployable:
             deploy_list.list_.append((Troops.valkyrie,(i.position[0],14.3)))   

       if i.name in ["Musketeer","Wizard","Archer"] and  i.position[1]<25:
        if can_deploy(arena_data["MyTroops"],i,["Minion","Knight","Valkyrie","Wizard","Archer"]):
         if Troops.valkyrie in deployable:
           deploy_list.list_.append((Troops.valkyrie,(i.position[0])))
         elif Troops.wizard in deployable:
          deploy_list.list_.append((Troops.wizard,(i.position[0],i.position[1]-10.3)))
         elif Troops.minion in deployable:
             deploy_list.list_.append((Troops.minion,(i.position[0],i.position[1]-3.8))) 
         elif Troops.archer in deployable:
          deploy_list.list_.append((Troops.archer,(i.position[0],i.position[1]-9.3)))
         elif Troops.knight in deployable:
           deploy_list.list_.append((Troops.knight,(i.position)))      
   

       if  i.name in ["Knight","Minion","Barbarian","Valkyrie","Skeleton","Giant","Prince","Balloon"]  and i.position[1]<23:
        if can_deploy(arena_data["MyTroops"],i,["Minion","Knight","Archer","Wizard","Dragon"]):
           if Troops.minion in deployable:
               deploy_list.list_.append((Troops.minion,(i.position[0],i.position[1]-3.8)))
           elif Troops.wizard in deployable:
             deploy_list.list_.append((Troops.wizard,(i.position[0],i.position[1]-10.3)))
           elif Troops.dragon in deployable:
             deploy_list.list_.append((Troops.dragon,(i.position[0],i.position[1]-6.5)))  
           elif Troops.archer in deployable:
             deploy_list.list_.append((Troops.archer,(i.position[0],i.position[1]-9.3)))      
           elif Troops.knight in deployable:
             deploy_list.list_.append((Troops.knight,(i.position)))    

              
    if x<2 and len(opp_troops)<2 and my_tower.total_elixir>=8 and my_tower.game_timer>50:
        if Troops.prince in deployable  and len(opp_troops)==0:
           deploy_list.list_.append((Troops.prince, (0, 50)))
           if Troops.wizard in deployable:
              deploy_list.list_.append((Troops.wizard,(0,50)))
           elif Troops.minion in deployable:
              deploy_list.list_.append((Troops.minion,(0,50)))
           elif Troops.archer in deployable:
              deploy_list.list_.append((Troops.archer,(0,50)))     
        elif Troops.prince in deployable  and len(opp_troops)==1: 
              if opp_troops[0].position[0]>0 and opp_troops[0].position[1]<85   :
               deploy_list.list_.append((Troops.prince, (-25, 50)))
               if Troops.wizard in deployable:
                deploy_list.list_.append((Troops.wizard,(-20,50)))
               elif Troops.minion in deployable:
                 deploy_list.list_.append((Troops.minion,(-20,50)))
               elif Troops.archer in deployable:
                 deploy_list.list_.append((Troops.archer,(-20,50)))   

              if opp_troops[0].position[0]<0   :  
               deploy_list.list_.append((Troops.prince, (25, 50)))
               if Troops.wizard in deployable:
                deploy_list.list_.append((Troops.wizard,(20,50)))
               elif Troops.minion in deployable:
                 deploy_list.list_.append((Troops.minion,(20,50)))
               elif Troops.archer in deployable:
                 deploy_list.list_.append((Troops.archer,(20,50))) 

    #(yellow)
    for i in opp_troops:      
      if i.name in ["Dragon","Minion"] and i.position[1]<49:
       if can_deploy(arena_data["MyTroops"],i,["Minion","Archer","Dragon","Wizard"]):
         if Troops.minion in deployable:
          deploy_list.list_.append((Troops.minion,(i.position[0],i.position[1]-3.8))) 
         if Troops.wizard in deployable:
           deploy_list.list_.append((Troops.wizard,(i.position[0],i.position[1]-16.5)))
         elif Troops.dragon in deployable:
          deploy_list.list_.append((Troops.dragon,(i.position[0],i.position[1]-7)))
         elif Troops.archer in deployable:
           deploy_list.list_.append((Troops.archer,(i.position[0],i.position[1]-13)))
      if i.name in ["Musketeer","Archer"] and i.position[1]<45:
         if can_deploy(arena_data["MyTroops"],i,["Minion","Knight","Valkyrie","Wizard"]):
             if Troops.valkyrie in deployable:
               deploy_list.list_.append((Troops.valkyrie,(i.position)))
             elif Troops.knight in deployable:
                deploy_list.list_.append((Troops.knight,(i.position)))
             elif Troops.minion in deployable:
                deploy_list.list_.append((Troops.minion,(i.position)))   
             elif Troops.wizard in deployable:
               deploy_list.list_.append((Troops.wizard,(i.position[0],i.position[1]-10.3)))
            
      if i.name in["Barbarian","Skeleton","Giant"] and i.position[1]<45:   
         if can_deploy(arena_data["MyTroops"],i,["Minion","Dragon","Wizard","Archer"]):
             if Troops.dragon in deployable:
              deploy_list.list_.append((Troops.dragon,(i.position[0],i.position[1]-6.5)))
             elif Troops.minion in deployable:
              deploy_list.list_.append((Troops.minion,(i.position[0],i.position[1]-3.8)))
             elif Troops.wizard in deployable:
              deploy_list.list_.append((Troops.wizard,(i.position[0],i.position[1]-10.3)))
             elif Troops.archer in deployable:
              deploy_list.list_.append((Troops.archer,(i.position[0],i.position[1]-9.3))) 
      if i.name in["Knight","Valkyrie"] and i.position[1]<45:   
         if can_deploy(arena_data["MyTroops"],i,["Minion","Dragon","Wizard","Archer"]):
             if Troops.valkyrie in deployable:
               deploy_list.list_.append((Troops.valkyrie,(i.position)))
             elif Troops.minion in deployable:
              deploy_list.list_.append((Troops.minion,(i.position[0],i.position[1]-6.3)))
             elif Troops.dragon in deployable:
              deploy_list.list_.append((Troops.dragon,(i.position[0],i.position[1]-7.9)))
             elif Troops.wizard in deployable:
              deploy_list.list_.append((Troops.wizard,(i.position[0],i.position[1]-13)))
             elif Troops.archer in deployable:
              deploy_list.list_.append((Troops.archer,(i.position[0],i.position[1]-11)))         
             
          
          #attack strategies
    if x<=1 and len(opp_troops)==0 and my_tower.total_elixir>=5:
        if Troops.prince in deployable  and len(opp_troops)==0:
           deploy_list.list_.append((Troops.prince, (0, 50)))
        elif Troops.wizard in deployable  and len(opp_troops)==0:
           deploy_list.list_.append((Troops.wizard, (0, 50)))  
        elif Troops.dragon in deployable  and len(opp_troops)==0:
           deploy_list.list_.append((Troops.dragon, (0, 50)))     

    if arena_data["MyTower"].total_elixir>=5 and x<=1 and len(opp_troops)<=2:
      t=[]
      p=[]
      for i in opp_troops:
        t.append(i.position[0])
        p.append(i.position[1])
      if all(a >=8 for a in t) and all(a>=60 and a<=70 for a in p) and arena_data["MyTower"].total_elixir>=6:
                        if Troops.prince in deployable:
                           deploy_list.list_.append((Troops.prince,(-25,50)))
      elif all(a <=-8 for a in t) and all(a>=60 and a<=75 for a in p) and arena_data["MyTower"].total_elixir>=6:     
                        if Troops.prince in deployable:
                           deploy_list.list_.append((Troops.prince,(25,50)))      
      elif all(a <=-12.5 for a in t) and all(a>=75 for a in p):     
                        if Troops.prince in deployable:
                           deploy_list.list_.append((Troops.prince,(25,50)))  
                        elif Troops.dragon in deployable  and len(opp_troops)==0:
                            deploy_list.list_.append((Troops.dragon, (0, 50)))            
      elif all(a>=12.5 for a in t) and all(a>=75 for a in p):     
                        if Troops.prince in deployable:
                           deploy_list.list_.append((Troops.prince,(-25,50)))     
                        elif Troops.dragon in deployable  and len(opp_troops)==0:
                            deploy_list.list_.append((Troops.dragon, (0, 50)))                                 
                             

    for i in my_troops:
       if i.name=="Giant" and i.health>=2700 and i.position[1]>=30 and i.position[1]<=45 and my_tower.total_elixir>=6:
             if Troops.wizard in deployable:
              deploy_list.list_.append((Troops.wizard,(0,15)))  
             elif Troops.dragon in deployable:
              deploy_list.list_.append((Troops.dragon,(0,15)))  
       elif i.name=="Giant" and i.health>=3300 and i.position[1]>=45 and i.position[1]<=60 and my_tower.total_elixir>=6:
             if Troops.wizard in deployable:
              deploy_list.list_.append((Troops.wizard,(0,35)))   
             elif Troops.dragon in deployable:
              deploy_list.list_.append((Troops.dragon,(0,35)))       
    K=[Troops.giant,Troops.wizard,Troops.valkyrie,Troops.dragon,Troops.archer,Troops.prince,Troops.knight,Troops.minion]
    C=[Troops.archer,Troops.dragon,Troops.wizard,Troops.minion,Troops.prince]
    if arena_data["MyTower"].total_elixir>=9.8:
        found=True
        p=[]
        for i in opp_troops:
         p.append(i.position[1])

        for i in K:  
         if i in deployable and all(a>70 for a in p):
            deploy_list.list_.append((i,(random.randint(-4,4),10)))
            found=False
            break

        for t in C:  
          if t in deployable and all(a<70 and a>50 for a in p) and found:
            deploy_list.list_.append((i,(random.randint(-4,4),10)))
            found=False
            break