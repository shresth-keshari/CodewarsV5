import os
import importlib.util
import csv
import datetime
from game import Game
import inspect

def validate_module(module, name):
    attributes = dir(module)
    
    # Expected variables and classes
    expected_variables = {"team_name", "troops", "deploy_list", "team_signal"}
    expected_classes = {"Troops", "Utils"}
    
    # Extract variables (excluding functions, classes, and modules)
    variables = {
        attr for attr in attributes
        if not callable(getattr(module, attr))
        and not attr.startswith("__")
        and not inspect.ismodule(getattr(module, attr))
        and not inspect.isclass(getattr(module, attr))
    }
    
    # Extract classes
    classes = {
        attr for attr in attributes
        if inspect.isclass(getattr(module, attr))
    }
    
    # Condition 1: Check for exact variables and classes
    if variables != expected_variables:
        print(f"Fail: Variables do not match. Found: {variables} for {name}")
        return False
    
    if classes != expected_classes:
        print(f"Fail: Classes do not match. Found: {classes} for {name}")
        return False
    
    # Condition 3: Check len(set(troops)) == 8
    if len(set(module.troops)) != 8 or len(module.troops) != 8:
        print(f"Fail: troops does not contain exactly 8 unique elements for {name}")
        return False
    
    print(f"Pass: All conditions met for {name} : {module.team_name}!")

    return True

def load_team_module(filepath):
    spec = importlib.util.spec_from_file_location("team_module", filepath)
    team_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(team_module)
    return team_module

def update_config(team1, team2):
    with open('config.py', 'w') as f:
        f.write(f"from team_files import {team1},{team2}\n\n")
        f.write(f"TEAM1 = {team1}\n")
        f.write(f"TEAM2 = {team2}\n")
        f.write("VALUE_ERROR = False\n")

team_files = [f for f in os.listdir('team_files') if f.endswith('.py') and f not in ['__init__.py', 'helper_function.py', 'troops_data.py']]
team_files.sort()

game_outcomes = []
match_number = 1

game_instance = None

with open('game_results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Match Number', 'Start Time', 'End Time', 'Total Game Time', 'Remaining Health Tower 1', 'Remaining Health Tower 2', 'Win State', 'Winner']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(len(team_files)):
        for j in range(i + 1, len(team_files)):
            team1 = team_files[i].replace('.py', '')
            team2 = team_files[j].replace('.py', '')
            
            update_config(team1, team2)
            
            TEAM1 = load_team_module(f'team_files/{team_files[i]}')
            TEAM2 = load_team_module(f'team_files/{team_files[j]}')
            
            team1_test_pass = validate_module(TEAM1, "TEAM 1")
            team2_test_pass = validate_module(TEAM2, "TEAM 2")
            
            if team1_test_pass and team2_test_pass:
                for _ in range(2):  # Run each match twice
                    print(f"Running match {match_number}: {team1} vs {team2}")
                    if game_instance is None:
                        game_instance = Game(TEAM1.troops, TEAM2.troops, TEAM1.team_name, TEAM2.team_name)
                    else:
                        game_instance.reset(TEAM1.troops, TEAM2.troops, TEAM1.team_name, TEAM2.team_name)
                    outcome = game_instance.run()
                    outcome['Match Number'] = match_number
                    writer.writerow({
                        'Match Number': match_number,
                        'Start Time': outcome['start_time'],
                        'End Time': outcome['end_time'],
                        'Total Game Time': outcome['game_time'],
                        'Remaining Health Tower 1': outcome['remaining_health_tower1'],
                        'Remaining Health Tower 2': outcome['remaining_health_tower2'],
                        'Win State': outcome['win_state'],
                        'Winner': outcome['winner']
                    })
                    game_outcomes.append(outcome)
                    print(f"Match {match_number} completed: {team1} vs {team2}")
                    match_number += 1

print("Game Outcomes:", game_outcomes)