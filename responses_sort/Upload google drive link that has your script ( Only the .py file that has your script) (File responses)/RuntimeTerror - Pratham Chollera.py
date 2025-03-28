import random
import time
from teams.helper_function import Troops, Utils

team_name = "RuntimeTerror"
troops = [
	Troops.giant, Troops.minion, Troops.valkyrie, Troops.balloon,
	Troops.dragon, Troops.skeleton, Troops.knight, Troops.wizard
]
deploy_list = Troops([])
team_signal = "0" * 128

def initialize(my_tower, opp_tower, my_troops, opp_troops):
	global team_signal
	length_of_team_signal = len(team_signal)
	elixir_index = length_of_team_signal - 3

	all_troops_list = ["Archer", "Minion", "Knight", "Skeleton", "Barbarian", "Dragon", "Valkyrie", "Musketeer", "Giant", "Prince", "Balloon", "Wizard"]
	#in priority order of most threatening to least threatening (dict keys) and best counter to worst counter (list elements)
	recommended_counters = {
	"Balloon": ["Minion", "Wizard", "Archer", "Dragon", "Musketeer"],
  	"Skeleton": ["Valkyrie", "Dragon", "Wizard", "Skeleton", "Minion"],
  	"Giant": ["Skeleton", "Minion", "Wizard", "Prince", "Barbarian", "Knight", "Archer"],
  	"Prince": ["Skeleton", "Prince", "Minion", "Wizard"],
  	"Wizard": ["Prince", "Knight", "Wizard", "Valkyrie"], 
  	"Barbarian": ["Wizard", "Valkyrie", "Skeleton", "Prince", "Dragon", "Barbarian"],
  	"Knight": ["Skeleton", "Prince",  "Minion", "Wizard", "Barbarian", "Valkyrie", "Knight", "Dragon", "Musketeer"],
  	"Valkyrie": ["Knight", "Prince", "Wizard", "Valkyrie", "Minion", "Musketeer"],
  	"Dragon": ["Wizard", "Dragon"],
  	"Minion": ["Dragon", "Wizard", "Minion", "Archer", "Musketeer"],
  	"Musketeer": ["Minion", "Prince", "Wizard", "Knight", "Skeleton", "Barbarian", "Valkyrie", "Musketeer", "Dragon"], 
  	"Archer": [ "Prince", "Wizard", "Barbarian", "Knight", "Valkyrie", "Dragon", "Minion", "Musketeer", "Archer", "Skeleton"]            
	}

	indexes_of_troops_in_recommended_counters = ["Balloon", "Skeleton", "Giant", "Prince", "Wizard", "Barbarian", "Knight", "Valkyrie", "Dragon", "Minion", "Musketeer", "Archer"]
	max_value_for_each_troop = []
	value_for_each_counter = []
	for i in range(12):
		number_of_troops = get_swarm_count(indexes_of_troops_in_recommended_counters[i])
		min_value_for_troop = (11 - i) * (1 / 11)
		max_value_for_each_troop.append((1 + (11 - i) * (1 / 11)) / number_of_troops)
		value_for_each_counter.append([])
		length_of_counter = len(recommended_counters[indexes_of_troops_in_recommended_counters[i]])
		for j in range(length_of_counter):
			value_for_each_counter[i].append((min_value_for_troop + (length_of_counter - 1 - j) / (length_of_counter - 1)) / number_of_troops)

	air_troops = ["Minion", "Dragon", "Balloon"]
	ground_troops = ["Archer", "Knight", "Skeleton", "Barbarian", "Valkyrie", "Musketeer", "Giant", "Prince", "Wizard"]
	attacking_air_troops = ["Archer", "Minion", "Dragon", "Musketeer", "Wizard"]
	attacking_ground_troops = ["Archer", "Minion", "Knight", "Skeleton", "Barbarian", "Dragon", "Valkyrie", "Musketeer", "Prince", "Wizard"]
	swarm_troops = ["Archer", "Minion", "Skeleton", "Barbarian"]
	splash_damage_troops = ["Dragon", "Valkyrie", "Wizard"]
	distance_damage_troops = ["Archer", "Minion", "Dragon", "Musketeer", "Wizard"]
	tank_troops = ["Giant", "Balloon", "Valkyrie", "Knight", "Prince"]
	fast_speed_troops = ["Minion", "Skeleton", "Dragon", "Prince"]
	medium_speed_troops = ["Archer", "Knight", "Barbarian", "Valkyrie", "Musketeer", "Balloon", "Wizard"]
	slow_speed_troops = ["Giant"]
	fast_attacking_troops = ["Archer", "Minion", "Knight", "Skeleton", "Dragon", "Valkyrie", "Prince", "Wizard"]
	medium_attacking_troops = ["Musketeer", "Barbarian", "Balloon"]
	slow_attacking_troops = ["Giant"]
	low_damage_troops = ["Skeleton"]
	medium_damage_troops = ["Archer", "Minion", "Barbarian", "Dragon", "Valkyrie"]
	high_damage_troops = ["Knight", "Musketeer", "Giant", "Prince", "Balloon", "Wizard"]
	my_troops_list = ["Minion", "Knight", "Skeleton", "Dragon", "Valkyrie", "Giant", "Balloon", "Wizard"]
	no_sole_attack = ["Archer", "Minion", "Skeleton"]
	opponent_troops_list = ["", "", "", "", "", "", "", ""]
	my_deployable_troops = my_tower.deployable_troops
	my_troops_order = ["", "", "", "", "", "", "", ""]
	opponent_troops_order = ["", "", "", "", "", "", "", ""]
	local_time = my_tower.game_timer
	if local_time == 0:
		change_team_signal(elixir_index, "A")
		opponent_elixir = 10
	else:
		opponent_elixir = update_opponent_elixir(elixir_index, local_time=local_time)

	good_enough_databasing_done = int(team_signal[length_of_team_signal - 24])
	making_my_troops_order(my_troops_list, my_troops_order, my_deployable_troops)
	# print("Our troops on the field (using my_troops)")
	# previous_troop = ""
	# i = 0
	# while i < len(my_troops):
	#     troop = my_troops[i].name
	#     troop_index = find_index(my_troops_list, troop)
	#     if troop != previous_troop:
	#         print(f"\t{troop}")
	#     i += 1
	#     previous_troop = troop
	# print("Our troops on the field (using team_signal)")
	# for i in range(8):
	#     troop_count = team_signal[length_of_team_signal - 19 + i]
	#     if troop_count != "0":
	#         print(f"\t{my_troops_list[i]}")
	# print("Our troops deployed on the last to last frame: ")
	# for i in range(3):
	#     troop_index = int(team_signal[length_of_team_signal - 11 + i])
	#     if troop_index != 0:
	#         print(f"\t{my_troops_list[troop_index - 1]}")
	# print("Our troops deployed on the last frame: ")
	# for i in range(3):
	#     troop_index = int(team_signal[length_of_team_signal - 8 + i])
	#     if troop_index != 0:
	#         print(f"\t{my_troops_list[troop_index - 1]}")
	extract_opponent_troops_list_from_team_signal(all_troops_list, opponent_troops_list, team_signal[:12])
	extract_opponent_troops_order_from_team_signal(all_troops_list, opponent_troops_order, team_signal[84:92])
	previous_opponent_troops_list = opponent_troops_list.copy()
	(opponent_deployed_troops, opponent_deployed_troops_position, temp_opponent_elixir) = making_opponents_troops_order(all_troops_list, length_of_team_signal, opp_troops, opponent_troops_list, opponent_troops_order)
	if len(opponent_deployed_troops):
		int_to_hexacontadidecimal(hexacontadidecimal_to_int(team_signal[length_of_team_signal - 21]) * 62 + hexacontadidecimal_to_int(team_signal[length_of_team_signal - 20]) + 1)
		# print("Opponent Deployed:")
		# for troop in opponent_deployed_troops:
		#     print(f'\t{troop}')
		opponent_elixir = temp_opponent_elixir
		# opponent_troops_order_elixir = [elixir(troop) for troop in opponent_troops_order]
		# if opponent_elixir < 2 or (good_enough_databasing_done and opponent_elixir < ):

		mapping(length_of_team_signal, all_troops_list, previous_opponent_troops_list, opponent_troops_list, opponent_deployed_troops)
		# for i in range(8):
		#     print(f"Against {my_troops_list[i]}, he deployed:")
		#     for j in range (8):
		#         if opponent_troops_list[j] != "":
		#             print(f"\t{opponent_troops_list[j]} with a Score of {team_signal[12 + 8*i + j]} points")


	oldest_deployed_troop_in_team_signal = int(team_signal[length_of_team_signal - 33])

	if not good_enough_databasing_done:
		counter = 0
		for i in range(8):
			if opponent_troops_list[i] != "":
				counter += 1
		if counter >= 6:
			change_team_signal(length_of_team_signal - 24, "1")
	to_team_signal_from_my_troops(length_of_team_signal, my_troops_list, my_troops)
	changing_troops_deployed(length_of_team_signal)

	if local_time == 0:
		previous_tower_health = 7032
	else:
		previous_tower_health = 0
	for i in range(3):
		previous_tower_health += (hexacontadidecimal_to_int(team_signal[length_of_team_signal - 28 + i]) * (62 ** (2 - i)))
	my_elixir = my_tower.total_elixir

	return (good_enough_databasing_done, oldest_deployed_troop_in_team_signal, recommended_counters, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, air_troops, ground_troops, attacking_air_troops, attacking_ground_troops, swarm_troops, splash_damage_troops, distance_damage_troops, tank_troops, fast_speed_troops, medium_speed_troops, slow_speed_troops, high_damage_troops, medium_damage_troops, low_damage_troops, no_sole_attack, fast_attacking_troops, medium_attacking_troops, slow_attacking_troops, previous_tower_health, all_troops_list, my_troops_list, my_deployable_troops, my_troops_order, opponent_troops_list, opponent_troops_order, opponent_deployed_troops, opponent_deployed_troops_position, length_of_team_signal, local_time, my_elixir, opponent_elixir)

def elixir(troop_name):
	if troop_name in ["Archer", "Minion", "Knight", "Skeleton", "Barbarian"]:
		return 3
	elif troop_name in ["Dragon", "Valkyrie", "Musketeer"]:
		return 4
	else:
		return 5

def health(troop_name):
	if troop_name == "Archer":
		return 334
	elif troop_name == "Minion":
		return 252
	elif troop_name == "Knight":
		return 1938
	elif troop_name == "Skeleton":
		return 89
	elif troop_name == "Barbarian":
		return 736
	elif troop_name == "Dragon":
		return 1267
	elif troop_name == "Valkyrie":
		return 2097
	elif troop_name == "Musketeer":
		return 792
	elif troop_name == "Giant":
		return 5423
	elif troop_name == "Prince":
		return 1920
	elif troop_name == "Balloon":
		return 2226
	elif troop_name == "Wizard":
		return 1100

def attack_speed(troop_name):
	if troop_name in ["Archer", "Minion", "Knight", "Skeleton", "Dragon", "Valkyrie", "Prince", "Wizard"]:
		return 6
	elif troop_name in ["Musketeer", "Barbarian", "Balloon"]:
		return 12
	elif troop_name in ["Giant"]:
		return 18

def attack_range(troop_name):
	if troop_name == "Archer":
		return 9.375
	elif troop_name == "Minion":
		return 3.75
	elif troop_name == "Dragon":
		return 6.5625
	elif troop_name == "Musketeer":
		return 11.25
	elif troop_name == "Wizard":
		return 10.3125

def get_swarm_count(troop_name):
	if troop_name == "Archer":
		return 2
	elif troop_name == "Barbarian" or troop_name == "Minion":
		return 3
	elif troop_name == "Skeleton":
		return 10
	return 1

def enumerat(passed_obj, reverse=False):
	temp_list = []
	if not reverse:
		for i in range(len(passed_obj)):
			temp_list.append([i, passed_obj[i]])
	else:
		length_of_passed_object = len(passed_obj)
		for i in range(length_of_passed_object):
			temp_index = length_of_passed_object - i - 1
			temp_list.append([temp_index, passed_obj[temp_index]])
	return temp_list

def making_my_troops_order(my_troops_list, my_troops_order, my_deployable_troops):
	global team_signal
	for temp_list in enumerat(my_deployable_troops):
		my_troops_order[temp_list[0]] = temp_list[1]
	for temp_list in enumerat(team_signal[76:84]):
		# print(f"{temp_list[0]} of team_signal ({my_troops_list[temp_list[0]]} at position): {temp_list[1]}")
		if int(temp_list[1]) > 4:
			my_troops_order[int(temp_list[1]) - 1] = my_troops_list[temp_list[0]]

def making_opponents_troops_order(all_troops_list, length_of_team_signal, opponent_troops_deployed, opponent_troops_list, opponent_troops_order):
	global team_signal
	troops_deployed = []
	troops_deployed_position = []
	elixir_index = length_of_team_signal - 3
	previous_length = length_of_opponent_troops_deployed(length_of_team_signal)
	new_length = len(opponent_troops_deployed)
	new_length_hexacontadi = int_to_hexacontadidecimal(new_length, True)
	change_team_signal(length_of_team_signal - 5, new_length_hexacontadi[0])
	change_team_signal(length_of_team_signal - 4, new_length_hexacontadi[1])
	if new_length > previous_length:
		while(new_length > previous_length):
			troop = opponent_troops_deployed[previous_length]
			troop_name = troop.name
			troop_position = troop.position
			troops_deployed.append(troop_name)
			troops_deployed_position.append(troop_position)
			opponent_elixir = update_opponent_elixir(elixir_index, troop_deployed=troop_name)
			change_troops_order(opponent_troops_order, troop_name)
			previous_length += get_swarm_count(troop_name)
			adding_opponent_troops_to_team_signal(all_troops_list, troop_name)
		converting_opponent_troops_order_to_team_signal(all_troops_list, opponent_troops_order)
		extract_opponent_troops_list_from_team_signal(all_troops_list, opponent_troops_list, team_signal[:12])
		# print("after calling making_opponents_troops_order with new_length > previous_length:", len(opponent_troops_deployed), opponent_troops_list, opponent_troops_order, team_signal[:12], team_signal[84:92], team_signal[-5], team_signal[-4], opponent_elixir)
		return (troops_deployed, troops_deployed_position, opponent_elixir)
	#too specific error checking in below case, optional
	elif new_length - 1 >= 0:
		last_deployed_troop = opponent_troops_deployed[new_length - 1]
		last_deployed_troop_name = last_deployed_troop.name
		last_deployed_troop_position = last_deployed_troop.position
		if not last_deployed_troop_name in opponent_troops_order[4:8]:
			opponent_elixir = update_opponent_elixir(elixir_index, troop_deployed=last_deployed_troop_name)
			adding_opponent_troops_to_team_signal(all_troops_list, last_deployed_troop_name)
			troops_deployed.append(last_deployed_troop_name)
			troops_deployed_position.append(last_deployed_troop_position)
			if new_length - 1 - get_swarm_count(last_deployed_troop_name) >= 0:
				last_to_last_deployed_troop = opponent_troops_deployed[new_length - 1 - get_swarm_count(last_deployed_troop_name)]
				last_to_last_deployed_troop_name = last_to_last_deployed_troop.name
				last_to_last_deployed_troop_position = last_to_last_deployed_troop.position
				if not last_to_last_deployed_troop_name in opponent_troops_order[4:8]:
					opponent_elixir = update_opponent_elixir(elixir_index, troop_deployed=last_to_last_deployed_troop_name)
					adding_opponent_troops_to_team_signal(all_troops_list, last_to_last_deployed_troop_name)
					troops_deployed.append(last_to_last_deployed_troop_name)
					troops_deployed_position.append(last_to_last_deployed_troop_position)
					if new_length - 1 - get_swarm_count(last_deployed_troop_name) - get_swarm_count(last_to_last_deployed_troop_name) >= 0:
						last_to_last_to_last_deployed_troop = opponent_troops_deployed[new_length - 1 - get_swarm_count(last_deployed_troop_name) - get_swarm_count(last_to_last_deployed_troop_name)]
						last_to_last_to_last_deployed_troop_name = last_to_last_to_last_deployed_troop.name
						last_to_last_to_last_deployed_troop_position = last_to_last_to_last_deployed_troop.position
						if not last_to_last_to_last_deployed_troop_name in opponent_troops_order[4:8]:
							opponent_elixir = update_opponent_elixir(elixir_index, troop_deployed=last_to_last_to_last_deployed_troop_name)
							troops_deployed.append(last_to_last_to_last_deployed_troop_name)
							troops_deployed_position.append(last_to_last_to_last_deployed_troop_position)
							adding_opponent_troops_to_team_signal(all_troops_list, last_to_last_to_last_deployed_troop_name)
							change_troops_order(opponent_troops_order, last_to_last_to_last_deployed_troop_name)
							change_troops_order(opponent_troops_order, last_to_last_deployed_troop_name)
							change_troops_order(opponent_troops_order, last_deployed_troop_name)
						else:
							change_troops_order(opponent_troops_order, last_to_last_deployed_troop_name)
							change_troops_order(opponent_troops_order, last_deployed_troop_name)
					else:
						change_troops_order(opponent_troops_order, last_to_last_deployed_troop_name)
						change_troops_order(opponent_troops_order, last_deployed_troop_name)
				else:
					change_troops_order(opponent_troops_order, last_deployed_troop_name)
			else:
				change_troops_order(opponent_troops_order, last_deployed_troop_name)
			extract_opponent_troops_list_from_team_signal(all_troops_list, opponent_troops_list, team_signal[:12])
			converting_opponent_troops_order_to_team_signal(all_troops_list, opponent_troops_order)
			# print("after calling making_opponents_troops_order:", len(opponent_troops_deployed), opponent_troops_list, opponent_troops_order, team_signal[:12], team_signal[84:92], team_signal[-5], team_signal[-4], opponent_elixir)
			return (troops_deployed, troops_deployed_position, opponent_elixir)
	return (troops_deployed, troops_deployed_position, 0)

def extract_opponent_troops_list_from_team_signal(all_troops_list, opponent_troops_list, bits):
	counter = 0
	for temp_list in enumerat(bits):
		if temp_list[1] != "0":
			troop = all_troops_list[temp_list[0]]
			opponent_troops_list[counter] = troop
			counter += 1

def extract_opponent_troops_order_from_team_signal(all_troops_list, opponent_troops_order, bits):
	for temp_list in enumerat(bits):
		if temp_list[1] != "0":
			troop = all_troops_list[non_zero_index_bit(temp_list[0])]
			opponent_troops_order[int(temp_list[1]) - 1] = troop
		else:
			break

def non_zero_index_bit(index):
	global team_signal
	counter = 0
	for i in range(12):
		if team_signal[i] != "0":
			if counter == index:
				return i
			counter += 1
	return -1

def adding_opponent_troops_to_team_signal(all_troops_list, troop):
	global team_signal
	index = find_index(all_troops_list, troop)
	char_to_change_to = (int_to_hexacontadidecimal(hexacontadidecimal_to_int(team_signal[index]) + 1))
	change_team_signal(index, char_to_change_to)

def converting_opponent_troops_order_to_team_signal(all_troops_list, opponent_troops_order):
	global team_signal
	for temp_list in enumerat(opponent_troops_order, reverse=True):
		if temp_list[1] != "":
			index = find_returning_non_zero_index(all_troops_list, temp_list[1])
			change_team_signal(84 + index, f'{(temp_list[0] + 1)}')
		else:
			break

def find_returning_non_zero_index(all_troops_list, troop_name):
	global team_signal
	counter = 0
	for i in range(12):
		if team_signal[i] != "0":
			if all_troops_list[i] == troop_name:
				return counter
			counter += 1
	return -1

def change_troops_order(troops_order, troop_deployed):
	index_of_troop_deployed = find_index(troops_order, troop_deployed)
	for i in range(8):
		if i < index_of_troop_deployed:
			continue
		elif i > index_of_troop_deployed:
			if i == 0:
				continue
			troops_order[i - 1] = troops_order[i]
	troops_order[7] = troop_deployed

def find_index(list_to_find_in, element_to_find):
	for i in range(len(list_to_find_in)):
		if list_to_find_in[i] == element_to_find:
			return i
	return -1

def to_team_signal_from_my_troops(length_of_team_signal, my_troops_list, my_troops):
	global team_signal
	for i in range(8):
		change_team_signal(length_of_team_signal - 19 + i, "0")
	i = 0
	while i < len(my_troops):
		troop_name = my_troops[i].name
		troop_index = find_index(my_troops_list, troop_name)
		if team_signal[length_of_team_signal - 19 + troop_index] != "1":
			change_team_signal(length_of_team_signal - 19 + find_index(my_troops_list, troop_name), "1")
		i += 1

def to_team_signal_from_my_troops_order(my_troops_list, my_troops_order):
	for i in range(8):
		if my_troops_order[i] != "":
			index = find_index(my_troops_list, my_troops_order[i])
			if index != -1:
				change_team_signal(76 + index, f'{(i + 1)}')
			# else:
				# print("What:", my_troops_list, my_troops_order[i])

def changing_troops_deployed(length_of_team_signal):
	global team_signal
	for temp_list in enumerat(team_signal[length_of_team_signal - 8: length_of_team_signal - 5]):
		change_team_signal(length_of_team_signal - 11 + temp_list[0], temp_list[1])

def change_team_signal(index, char):
	global team_signal
	team_signal = team_signal[:index] + char + team_signal[index+1:]

def update_opponent_elixir(elixir_index, troop_deployed=None, local_time=None):
	global team_signal
	first_bit = hexacontadidecimal_to_int(team_signal[elixir_index])
	second_bit = int(team_signal[elixir_index + 1])
	third_bit = int(team_signal[elixir_index + 2])
	temp_elixir = first_bit * 100 + second_bit * 10 + third_bit
	# print(team_signal[elixir_index], team_signal[elixir_index + 1], team_signal[elixir_index + 2], first_bit, second_bit, third_bit, temp_elixir)
	if troop_deployed:
		temp_elixir -= (elixir(troop_deployed) * 100)
	if local_time:
		if local_time < 1200:
			elixir_update = 5
		else:
			elixir_update = 10
		if temp_elixir != 1000:
			temp_elixir += elixir_update
	first_bit = temp_elixir // 100
	second_bit = (temp_elixir - first_bit * 100) // 10
	third_bit = temp_elixir % 10
	change_team_signal(elixir_index, int_to_hexacontadidecimal(first_bit))
	change_team_signal(elixir_index + 1, f'{second_bit}')
	change_team_signal(elixir_index + 2, f'{third_bit}')
	# print(team_signal[elixir_index], team_signal[elixir_index + 1], team_signal[elixir_index + 2], first_bit, second_bit, third_bit, temp_elixir)
	opponent_elixir = first_bit + second_bit / 10 + third_bit / 100
	if opponent_elixir < 0:
		opponent_elixir = 4
	opponent_elixir = round(opponent_elixir, 2)
	# print(opponent_elixir)
	return opponent_elixir

def mapping(length_of_team_signal, all_troops_list, previous_opponent_troops_list, opponent_troops_list, opponent_deployed_troops):
	global team_signal
	reference_list = [[], [], [], [], [], [], [], []]
	for i in range(8):
		reference_list[i] = ["", "", "", "", "", "", "", ""]
		for temp_list in enumerat(team_signal[12 + 8*i:12 + 8*(i+1)]):
			reference_list[i][temp_list[0]] = temp_list[1]
			change_team_signal(12 + 8*i + temp_list[0], "0")
		for temp_list in enumerat(reference_list[i]):
			previous_opponent_troop = previous_opponent_troops_list[temp_list[0]]
			if previous_opponent_troop != "":
				index = find_index(opponent_troops_list, previous_opponent_troop)
				change_team_signal(12 + 8*i + index, temp_list[1])
			else:
				break
	excluded_bits = []
	for bit in team_signal[length_of_team_signal - 11:length_of_team_signal - 8]:
		if bit != "0":
			excluded_bits.append(int(bit) - 1)
			primary_index = 12 + 8*(int(bit) - 1)
			for opp_troop in opponent_deployed_troops:
				secondary_index = find_index(opponent_troops_list, opp_troop)
				index_to_change = primary_index + secondary_index
				char_to_change_to = int_to_hexacontadidecimal(hexacontadidecimal_to_int(team_signal[index_to_change]) + 2)
				change_team_signal(primary_index + secondary_index, char_to_change_to)
		else:
			break
	for temp_list in enumerat(team_signal[length_of_team_signal - 19:length_of_team_signal - 11]):
		if temp_list[1] != "0" and temp_list[0] not in excluded_bits:
			primary_index = 12 + 8*(int(temp_list[0]))
			for opp_troop in opponent_deployed_troops:
				secondary_index = find_index(opponent_troops_list, opp_troop)
				index_to_change = primary_index + secondary_index
				char_to_change_to = int_to_hexacontadidecimal(hexacontadidecimal_to_int(team_signal[index_to_change]) + 1)
				change_team_signal(primary_index + secondary_index, char_to_change_to)

def hexacontadidecimal_to_int(hexa):
	if 90 >= ord(hexa) >= 65:
		return ord(hexa) - 55
	elif 122 >= ord(hexa) >= 97:
		return ord(hexa) - 61
	else:
		return int(hexa)

def int_to_hexacontadidecimal(inte, two=False, three=False):
	if three:
		third_bit = inte // 3844
		second_bit = (inte - third_bit * 3844) // 62
		first_bit = inte % 62
		if 36 > first_bit > 9:
			first_bit = chr(first_bit + 55)
		elif first_bit >= 36:
			first_bit = chr(first_bit + 61)
		if 36 > second_bit > 9:
			second_bit = chr(second_bit + 55)
		elif second_bit >= 36:
			second_bit = chr(second_bit + 61)
		if 36 > third_bit > 9:
			third_bit = chr(third_bit + 55)
		elif third_bit >= 36:
			third_bit = chr(third_bit + 61)
		return (f'{third_bit}{second_bit}{first_bit}')
	elif two:
		second_bit = inte // 62
		first_bit = inte % 62
		if 36 > first_bit > 9:
			first_bit = chr(first_bit + 55)
		elif first_bit >= 36:
			first_bit = chr(first_bit + 61)
		if 36 > second_bit > 9:
			second_bit = chr(second_bit + 55)
		elif second_bit >= 36:
			second_bit = chr(second_bit + 61)
		return (f'{second_bit}{first_bit}')
	else:
		if 36 > inte > 9:
			inte = chr(inte + 55)
		elif inte >= 36:
			inte = chr(inte + 61)
		return f'{inte}'

def change_oldest_deployed_troop_in_team_signal():
	global team_signal
	length_of_team_signal = len(team_signal)
	oldest_deployed_troop_in_team_signal = int(team_signal[length_of_team_signal - 33])
	if oldest_deployed_troop_in_team_signal == 2:
		oldest_deployed_troop_in_team_signal = 0
		change_team_signal(length_of_team_signal - 33, "0")
	else:
		oldest_deployed_troop_in_team_signal += 1
		change_team_signal(length_of_team_signal - 33, str(oldest_deployed_troop_in_team_signal))

	return oldest_deployed_troop_in_team_signal

def length_of_opponent_troops_deployed(length_of_team_signal):
	global team_signal
	return (hexacontadidecimal_to_int(team_signal[length_of_team_signal - 5]) * 62 + hexacontadidecimal_to_int(team_signal[length_of_team_signal - 4]))

def find_max_index(list_to_find_in):
	max_element = 0
	index = 0
	for i in range(len(list_to_find_in)):
		if list_to_find_in[i] > max_element:
			index = i
	return index

def find_index_of_least_elixir_card(given_list):
	temp_elixir = 5
	index = 0
	counter = 0
	for troop in given_list:
		elixir_of_troop = elixir(troop)
		if elixir_of_troop < temp_elixir:
			temp_elixir = elixir_of_troop
			index = counter
		counter += 1
	return index

def contains_only_zeroes(given_list):
	for element in given_list:
		if element != 0:
			return False
	return True

def order_in_threatening_order(indexes_of_troops_in_recommended_counters, given_list):
	temp_list = []
	given_list_names = []
	for troop in given_list:
		given_list_names.append(troop.name)
	for troop in indexes_of_troops_in_recommended_counters:
		if troop in given_list_names:
			index = find_index(given_list_names, troop)
			temp_list.append(given_list[index])
	return temp_list

def find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, my_troop_to_deploy, arriving_troops, distance_damage_troops, emergency=False, attacking=False):
	# print(arriving_troops)
	threatening_ordered_arriving_troops = order_in_threatening_order(indexes_of_troops_in_recommended_counters, arriving_troops)
	# print(threatening_ordered_arriving_troops)
	if not len(threatening_ordered_arriving_troops):
		return (0, 0)
	temp_troop = threatening_ordered_arriving_troops[0]
	if not emergency and not attacking:
		if my_troop_to_deploy in distance_damage_troops:
			position = (temp_troop.position[0], max(temp_troop.position[1] - attack_range(my_troop_to_deploy), 0))
			return position
		for troop in threatening_ordered_arriving_troops:
			if troop.name in distance_damage_troops or troop.name in ["Giant", "Balloon"]:
				position = (troop.position[0], troop.position[1])
				return position
		position = ((temp_troop.position[0]) / 2, (4 * 9.375 + temp_troop.position[1]) / 5)
		return position
	if attacking:
		for troop in threatening_ordered_arriving_troops:
			if my_troop_to_deploy in distance_damage_troops:
				position = (troop.position[0], min(troop.position[1] - attack_range(my_troop_to_deploy), 50))
				return position
			if troop.name in distance_damage_troops or troop.name in ["Giant", "Balloon"]:
				position = (troop.position[0], min(troop.position[1], 50))
				return position
		position = (troop.position[0], 50)
		return position
	for troop in threatening_ordered_arriving_troops:
		if my_troop_to_deploy in distance_damage_troops:
			position = (troop.position[0], max(troop.position[1] - attack_range(my_troop_to_deploy), 0))
			return position
		if troop.name in distance_damage_troops or troop.name in ["Giant", "Balloon"]:
			position = (troop.position[0], troop.position[1])
			return position
	position = ((temp_troop.position[0]) / 2, (4 * 9.375 + temp_troop.position[1]) / 5)
	return position

def find_counter_for_hypothetical_troops(troops_to_counter, indexes_of_troops_in_recommended_counters, value_for_each_counter, my_troops_order_left, recommended_counters):
	global team_signal
	arriving_troops = []
	troop_sum = [0, 0, 0]
	for troop_to_counter in troops_to_counter:
		arriving_troops.append(troop_to_counter)
		index_of_troop_to_counter = find_index(indexes_of_troops_in_recommended_counters, troop_to_counter)
		troop_to_counter_value_list = value_for_each_counter[index_of_troop_to_counter]
		temp_deployable_troops = my_troops_order_left.copy()
		for temp_list in enumerat(temp_deployable_troops):
			if temp_list[1] in recommended_counters[troop_to_counter]:
				index_of_sum_value = find_index(troop_to_counter_value_list, temp_list[1])
				troop_sum[temp_list[0]] += troop_to_counter_value_list[index_of_sum_value]

	if contains_only_zeroes(troop_sum):
		return None

	return find_max_index(troop_sum)

def find_counters_for_troops(length_of_team_signal, right_defended, left_defended, distance_damage_troops, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, right_troops_to_counter, left_troops_to_counter, recommended_counters, my_troops_order, my_troops_list, my_elixir, emergency=False, attacking=False):
	global team_signal
	left_arriving_troops = []
	right_arriving_troops = []
	left_troop_sum = [0, 0, 0, 0, 0]
	right_troop_sum = [0, 0, 0, 0, 0]
	left_troops_total_health = 0
	right_troops_total_health = 0
	left_troops_health = 0
	right_troops_health = 0
	left_threat_sum = 0
	right_threat_sum = 0
	for troop_to_counter in left_troops_to_counter:
		if not troop_to_counter:
			continue
		left_arriving_troops.append(troop_to_counter)
		left_troops_total_health += health(troop_to_counter.name)
		left_troops_health += troop_to_counter.health
		index_of_troop_to_counter = find_index(indexes_of_troops_in_recommended_counters, troop_to_counter.name)
		left_threat_sum += max_value_for_each_troop[index_of_troop_to_counter]
		troop_to_counter_value_list = value_for_each_counter[index_of_troop_to_counter]
		temp_deployable_troops = my_troops_order[:5].copy()
		for temp_list in enumerat(temp_deployable_troops):
			if temp_list[1] in recommended_counters[troop_to_counter.name]:
				index_of_sum_value = find_index(troop_to_counter_value_list, temp_list[1])
				left_troop_sum[temp_list[0]] += troop_to_counter_value_list[index_of_sum_value]
	for troop_to_counter in right_troops_to_counter:
		if not troop_to_counter:
			continue
		right_arriving_troops.append(troop_to_counter)
		right_troops_total_health += health(troop_to_counter.name)
		right_troops_health += troop_to_counter.health
		index_of_troop_to_counter = find_index(indexes_of_troops_in_recommended_counters, troop_to_counter.name)
		right_threat_sum += max_value_for_each_troop[index_of_troop_to_counter]
		troop_to_counter_value_list = value_for_each_counter[index_of_troop_to_counter]
		temp_deployable_troops = my_troops_order[:5].copy()
		for temp_list in enumerat(temp_deployable_troops):
			if temp_list[1] in recommended_counters[troop_to_counter.name]:
				index_of_sum_value = find_index(troop_to_counter_value_list, temp_list[1])
				right_troop_sum[temp_list[0]] += troop_to_counter_value_list[index_of_sum_value]

	left_to_defend = int(team_signal[length_of_team_signal - 31])
	right_to_defend = int(team_signal[length_of_team_signal - 32])


	# print(left_troop_sum, right_troop_sum, left_threat_sum, right_threat_sum)
	if (left_defended and left_to_defend and not right_defended) or (right_defended and right_to_defend and not left_defended) or (not right_defended and not left_defended):
		if left_threat_sum > right_threat_sum:
			if emergency:
				if contains_only_zeroes(left_troop_sum[:4]):
					index = find_index_of_least_elixir_card(my_troops_order[:4])
					troop_to_deploy = my_troops_order[index]
					return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, left_arriving_troops, distance_damage_troops, emergency=emergency))
				for i in range(4):
					index = find_max_index(left_troop_sum[:5])
					left_troop_sum[index] = -1
					troop_to_deploy = my_troops_order[index]
					# print(f"{troop_to_deploy}")
					if my_elixir >= elixir(troop_to_deploy):
						# print(f"Left side: {troop_to_deploy}")
						return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, left_arriving_troops, distance_damage_troops, emergency=emergency))
					elif round(elixir(troop_to_deploy), 2) - round(my_elixir, 2)  == round(0.05, 2):
						# print(f"Left side waiting for 1 frame: {troop_to_deploy}")
						return (None, None)
			else:
				if contains_only_zeroes(left_troop_sum[:4]):
					index = find_index_of_least_elixir_card(my_troops_order[:4])
					troop_to_deploy = my_troops_order[index]
					return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, left_arriving_troops, distance_damage_troops, emergency=emergency, attacking=attacking))
				if left_to_defend:
					troop_to_deploy = my_troops_list[left_to_defend - 1]
					change_team_signal(length_of_team_signal - 31, "0")
					return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, left_arriving_troops, distance_damage_troops, emergency=emergency, attacking=attacking))
				temp_troop_sum = left_troop_sum.copy()
				index = find_max_index(temp_troop_sum)
				if index == 4:
					best_troop_counter = my_troops_order[index]
					change_team_signal(length_of_team_signal - 31, f'{find_index(my_troops_list, best_troop_counter) + 1}')
					left_troop_sum[index] = -1
					temp_troop_sum[index] = -1
					for i in range(2):
						index = find_max_index(temp_troop_sum)
						troop_to_deploy = my_troops_order[index]
						if my_elixir >= elixir(troop_to_deploy) + elixir(best_troop_counter) or round(elixir(troop_to_deploy) + elixir(best_troop_counter), 2) - round(my_elixir, 2) == round(0.05, 2):
							return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, left_arriving_troops, distance_damage_troops, emergency=emergency, attacking=attacking))
				change_team_signal(length_of_team_signal - 31, "0")
				for i in range(4):
					index = find_max_index(left_troop_sum)
					left_troop_sum[index] = -1
					troop_to_deploy = my_troops_order[index]
					if my_elixir >= elixir(troop_to_deploy):
						return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, left_arriving_troops, distance_damage_troops, emergency=emergency))
					elif round(elixir(troop_to_deploy), 2) - round(my_elixir, 2) == round(0.05, 2):
						return (None, None)
		else:
			if emergency:
				if contains_only_zeroes(right_troop_sum[:4]):
					index = find_index_of_least_elixir_card(my_troops_order[:4])
					troop_to_deploy = my_troops_order[index]
					return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, right_arriving_troops, distance_damage_troops, emergency=emergency, attacking=attacking))
				for i in range(4):
					index = find_max_index(right_troop_sum[:5])
					right_troop_sum[index] = -1
					troop_to_deploy = my_troops_order[index]
					# print(f"{troop_to_deploy}")
					if my_elixir >= elixir(troop_to_deploy):
						# print(f"Right side: {troop_to_deploy}")
						return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, right_arriving_troops, distance_damage_troops, emergency=emergency, attacking=attacking))
					elif round(elixir(troop_to_deploy), 2) - round(my_elixir, 2) == round(0.05, 2):
						# print(f"Right side waiting for 1 frame: {troop_to_deploy}")
						return (None, None)
			else:
				if contains_only_zeroes(right_troop_sum[:4]):
					index = find_index_of_least_elixir_card(my_troops_order[:4])
					troop_to_deploy = my_troops_order[index]
					return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, right_arriving_troops, distance_damage_troops, emergency=emergency, attacking=attacking))
				if right_to_defend:
					troop_to_deploy = my_troops_list[right_to_defend - 1]
					change_team_signal(length_of_team_signal - 32, "0")
					return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, right_arriving_troops, distance_damage_troops, emergency=emergency, attacking=attacking))
				temp_troop_sum = right_troop_sum.copy()
				index = find_max_index(temp_troop_sum)
				if index == 4:
					best_troop_counter = my_troops_order[index]
					change_team_signal(length_of_team_signal - 32, f'{find_index(my_troops_list, best_troop_counter) + 1}')
					right_troop_sum[index] = -1
					temp_troop_sum[index] = -1
					for i in range(2):
						index = find_max_index(temp_troop_sum)
						troop_to_deploy = my_troops_order[index]
						if my_elixir >= elixir(troop_to_deploy) + elixir(best_troop_counter) or round(elixir(troop_to_deploy) + elixir(best_troop_counter), 2) - round(my_elixir, 2) == round(0.05, 2):
							return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, right_arriving_troops, distance_damage_troops))
				change_team_signal(length_of_team_signal - 32, "0")
				for i in range(4):
					index = find_max_index(right_troop_sum)
					right_troop_sum[index] = -1
					troop_to_deploy = my_troops_order[index]
					if my_elixir >= elixir(troop_to_deploy):
						return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, right_arriving_troops, distance_damage_troops, emergency=emergency, attacking=attacking))
					elif round(elixir(troop_to_deploy), 2) - round(my_elixir, 2) == round(0.05, 2):
						return (None, None)

	elif left_defended and right_defended:
		if emergency:
			if left_threat_sum > right_threat_sum:
				if int(team_signal[length_of_team_signal - 30]) == "0":
					change_team_signal(length_of_team_signal - 30, "2")
			else:
				if int(team_signal[length_of_team_signal - 30]) == "0":
					change_team_signal(length_of_team_signal - 30, "1")
			if int(team_signal[length_of_team_signal - 30]) == "2":
				if contains_only_zeroes(left_troop_sum[:4]):
					index = find_index_of_least_elixir_card(my_troops_order[:4])
					troop_to_deploy = my_troops_order[index]
					return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, left_arriving_troops, distance_damage_troops, emergency=emergency, attacking=attacking))
				if left_to_defend:
					troop_to_deploy = my_troops_list[left_to_defend - 1]
					change_team_signal(length_of_team_signal - 31, "0")
					change_team_signal(length_of_team_signal - 30, "1")
					return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, left_arriving_troops, distance_damage_troops, emergency=emergency, attacking=attacking))
				temp_troop_sum = left_troop_sum.copy()
				index = find_max_index(temp_troop_sum)
				if index == 4:
					best_troop_counter = my_troops_order[index]
					change_team_signal(length_of_team_signal - 31, f'{find_index(my_troops_list, best_troop_counter) + 1}')
					left_troop_sum[index] = -1
					temp_troop_sum[index] = -1
					for i in range(2):
						index = find_max_index(temp_troop_sum)
						troop_to_deploy = my_troops_order[index]
						if my_elixir >= elixir(troop_to_deploy) + elixir(best_troop_counter) or round(elixir(troop_to_deploy) + elixir(best_troop_counter), 2) - round(my_elixir, 2) == round(0.05, 2):
							return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, left_arriving_troops, distance_damage_troops, emergency=emergency, attacking=attacking))
				change_team_signal(length_of_team_signal - 31, "0")
				change_team_signal(length_of_team_signal - 30, "1")
				for i in range(4):
					index = find_max_index(left_troop_sum)
					left_troop_sum[index] = -1
					troop_to_deploy = my_troops_order[index]
					if my_elixir >= elixir(troop_to_deploy):
						return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, left_arriving_troops, distance_damage_troops, emergency=emergency, attacking=attacking))
					elif round(elixir(troop_to_deploy), 2) - round(my_elixir, 2) == round(0.05, 2):
						return (None, None)
			elif int(team_signal[length_of_team_signal - 30]) == "1":
				if contains_only_zeroes(right_troop_sum[:4]):
					index = find_index_of_least_elixir_card(my_troops_order[:4])
					troop_to_deploy = my_troops_order[index]
					return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, right_arriving_troops, distance_damage_troops, emergency=emergency, attacking=attacking))
				if right_to_defend:
					troop_to_deploy = my_troops_list[right_to_defend - 1]
					change_team_signal(length_of_team_signal - 32, "0")
					change_team_signal(length_of_team_signal - 30, "2")
					return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, right_arriving_troops, distance_damage_troops, emergency=emergency, attacking=attacking))
				temp_troop_sum = right_troop_sum.copy()
				index = find_max_index(temp_troop_sum)
				if index == 4:
					best_troop_counter = my_troops_order[index]
					change_team_signal(length_of_team_signal - 32, f'{find_index(my_troops_list, best_troop_counter) + 1}')
					right_troop_sum[index] = -1
					temp_troop_sum[index] = -1
					for i in range(2):
						index = find_max_index(temp_troop_sum)
						troop_to_deploy = my_troops_order[index]
						if my_elixir >= elixir(troop_to_deploy) + elixir(best_troop_counter) or round(elixir(troop_to_deploy) + elixir(best_troop_counter), 2) - round(my_elixir, 2) == round(0.05, 2):
							return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, right_arriving_troops, distance_damage_troops, emergency=emergency, attacking=attacking))
				change_team_signal(length_of_team_signal - 32, "0")
				change_team_signal(length_of_team_signal - 30, "2")
				for i in range(4):
					index = find_max_index(right_troop_sum)
					right_troop_sum[index] = -1
					troop_to_deploy = my_troops_order[index]
					if my_elixir >= elixir(troop_to_deploy):
						return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, right_arriving_troops, distance_damage_troops, emergency=emergency, attacking=attacking))
					elif round(elixir(troop_to_deploy), 2) - round(my_elixir, 2) == round(0.05, 2):
						return (None, None)

	if right_threat_sum != 0 or attacking:
		if left_defended and not left_to_defend and not right_defended:
			if contains_only_zeroes(right_troop_sum[:4]):
				index = find_index_of_least_elixir_card(my_troops_order[:4])
				troop_to_deploy = my_troops_order[index]
				if attacking:
					return (troop_to_deploy, (25, 50))
				return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, right_arriving_troops, distance_damage_troops, emergency=emergency, attacking=attacking))
			for i in range(4):
				index = find_max_index(right_troop_sum)
				right_troop_sum[index] = -1
				troop_to_deploy = my_troops_order[index]
				if my_elixir >= elixir(troop_to_deploy):
					return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, right_arriving_troops, distance_damage_troops, emergency=emergency, attacking=attacking))
				elif round(elixir(troop_to_deploy), 2) - round(my_elixir, 2) == round(0.05, 2):
					return (None, None)
	if left_threat_sum != 0 or attacking:
		if right_defended and not right_to_defend and not left_defended:
			if contains_only_zeroes(left_troop_sum[:4]):
				index = find_index_of_least_elixir_card(my_troops_order[:4])
				troop_to_deploy = my_troops_order[index]
				if attacking:
					return (troop_to_deploy, (-25, 50))
				return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, left_arriving_troops, distance_damage_troops, emergency=emergency, attacking=attacking))
			for i in range(4):
				index = find_max_index(left_troop_sum)
				left_troop_sum[index] = -1
				troop_to_deploy = my_troops_order[index]
				if my_elixir >= elixir(troop_to_deploy):
					return (troop_to_deploy, find_optimal_position_to_deploy_troop(indexes_of_troops_in_recommended_counters, troop_to_deploy, left_arriving_troops, distance_damage_troops, emergency=emergency, attacking=attacking))
				elif round(elixir(troop_to_deploy), 2) - round(my_elixir, 2) == round(0.05, 2):
					return (None, None)
		
	return (None, None)

def defend(my_troops, opp_troops, my_tower, length_of_team_signal, distance_damage_troops, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, recommended_counters, my_troops_order, my_troops_list, my_elixir):
	temp_opp_troops = opp_troops.copy()
	right_troops_to_consider = []
	left_troops_to_consider = []
	right_defended = 0
	left_defended = 0
	# change_team_signal(length_of_team_signal - 31, "0")
	# change_team_signal(length_of_team_signal - 32, "0")
	for troop in my_troops:
		if Utils.calculate_distance(troop, my_tower) - troop.size - my_tower.size < 30 and troop not in ["Giant", "Balloon"]:
			if troop.position[0] < 0:
				left_defended = 1
			else:
				right_defended = 1
	for main_troop in temp_opp_troops:
		if Utils.calculate_distance(my_tower, main_troop) - my_tower.size - main_troop.size < 30:
			if main_troop.position[0] < 0:
				for troop in temp_opp_troops:
					if Utils.calculate_distance(troop, main_troop) - troop.size - main_troop.size < 3:
						if troop in temp_opp_troops:
							temp_opp_troops.remove(troop)
						left_troops_to_consider.append(troop)
			if main_troop.position[0] > 0:
				for troop in temp_opp_troops:
					if Utils.calculate_distance(troop, main_troop) - troop.size - main_troop.size < 3:
						if troop in temp_opp_troops:
							temp_opp_troops.remove(troop)
						right_troops_to_consider.append(troop)
	if len(right_troops_to_consider) or len(left_troops_to_consider):
		# print("1st case")
		change_team_signal(length_of_team_signal - 29, "1")
		(troop_to_deploy, troop_position) = find_counters_for_troops(length_of_team_signal, right_defended, left_defended, distance_damage_troops, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, right_troops_to_consider, left_troops_to_consider, recommended_counters, my_troops_order, my_troops_list, my_elixir)
		return (troop_to_deploy, troop_position)
	# temp_opp_troops = opp_troops.copy()
	# potential_damage_by_troops_per_frame = 0
	# for main_troop in temp_opp_troops:
	# 	if Utils.calculate_distance(my_tower, main_troop) - my_tower.size - main_troop.size < 40:
	# 		if main_troop.position[0] < 0:
	# 			for troop in temp_opp_troops:
	# 				if Utils.calculate_distance(troop, main_troop) - troop.size - main_troop.size < 2.5:
	# 					temp_opp_troops.remove(troop)
	# 					potential_damage_by_troops_per_frame += (troop.damage / attack_speed(troop.name))
	# 					left_troops_to_consider.append(troop)
	# 		if main_troop.position[0] > 0:
	# 			for troop in temp_opp_troops:
	# 				if Utils.calculate_distance(troop, main_troop) - troop.size - main_troop.size < 2.5:
	# 					temp_opp_troops.remove(troop)
	# 					potential_damage_by_troops_per_frame += (troop.damage / attack_speed(troop.name))
	# 					right_troops_to_consider.append(troop)
	# if len(right_troops_to_consider) or len(left_troops_to_consider):
	# 	# print("2nd case")
	# 	if potential_damage_by_troops_per_frame > 0.02 * my_tower.health:
	# 		change_team_signal(length_of_team_signal - 29, "1")
	# 		(troop_to_deploy, troop_position) = find_counters_for_troops(length_of_team_signal, right_defended, left_defended, distance_damage_troops, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, right_troops_to_consider, left_troops_to_consider, recommended_counters, my_troops_order, my_troops_list, my_elixir)
	# 		return (troop_to_deploy, troop_position)
	temp_opp_troops = opp_troops.copy()
	for main_troop in temp_opp_troops:
		if Utils.calculate_distance(my_tower, main_troop) - my_tower.size - main_troop.size < 50:
			if main_troop.position[0] < 0:
				for troop in temp_opp_troops:
					if Utils.calculate_distance(troop, main_troop) - troop.size - main_troop.size < 4:
						temp_opp_troops.remove(troop)
						left_troops_to_consider.append(troop)
			if main_troop.position[0] > 0:
				for troop in temp_opp_troops:
					if Utils.calculate_distance(troop, main_troop) - troop.size - main_troop.size < 4:
						temp_opp_troops.remove(troop)
						right_troops_to_consider.append(troop)
	if len(right_troops_to_consider) or len(left_troops_to_consider):
		# print("3rd case")
		# print(right_defended, left_defended)
		left_to_defend = int(team_signal[length_of_team_signal - 31])
		right_to_defend = int(team_signal[length_of_team_signal - 32])
		# print(left_to_defend, right_to_defend)
		change_team_signal(length_of_team_signal - 29, "0")
		(troop_to_deploy, troop_position) = find_counters_for_troops(length_of_team_signal, right_defended, left_defended, distance_damage_troops, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, right_troops_to_consider, left_troops_to_consider, recommended_counters, my_troops_order, my_troops_list, my_elixir)
		# print(troop_to_deploy, troop_position)
		return (troop_to_deploy, troop_position)

	change_team_signal(length_of_team_signal - 29, "0")
	return (None, None)

def attack(length_of_team_signal, good_enough_databasing_done, my_troops, opp_troops, no_sole_attack, distance_damage_troops, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, recommended_counters, my_troops_order, my_troops_list, my_elixir):
	global team_signal
	change_team_signal(length_of_team_signal - 31, "0")
	change_team_signal(length_of_team_signal - 32, "0")
	if int(team_signal[length_of_team_signal - 25]):
		for troop in my_troops:
			if troop in ["Giant", "Balloon"]:
				if troop.position[0] < 0:
					surrounding_troops = []
					for opp_troop in opp_troops:
						if calculate_distance(troop, opp_troop) - troop.size - opp_troop.size < 3:
							surrounding_troops.append(opp_troop)
					if 45 < troop.position[1] < 50 or (len(surrounding_troops) > 0 and troop.position[1] < 50):
						(troop_to_deploy, position_of_troop_to_deploy) = find_counters_for_troops(length_of_team_signal, 1, 0, distance_damage_troops, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, [], surrounding_troops, recommended_counters, my_troops_order, my_troops_list, my_elixir, emergency=False, attacking=True)
						if not troop_to_deploy:
							return (None, None) 
						if my_elixir >= elixir(troop_to_deploy):
							return ([troop_to_deploy], [position_of_troop_to_deploy])
							change_team_signal(length_of_team_signal - 25, "0")
						else:
							return (None, None)
				else:
					surrounding_troops = []
					for opp_troop in opp_troops:
						if calculate_distance(troop, opp_troop) - troop.size - opp_troop.size < 3:
							surrounding_troops.append(opp_troop)
					if 45 < troop.position[1] < 50 or (len(surrounding_troops) > 0 and troop.position[1] < 50):
						(troop_to_deploy, position_of_troop_to_deploy) = find_counters_for_troops(length_of_team_signal, 0, 1, distance_damage_troops, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, surrounding_troops, [], recommended_counters, my_troops_order, my_troops_list, my_elixir, emergency=False, attacking=True)
						if not troop_to_deploy:
							return (None, None) 
						if my_elixir >= elixir(troop_to_deploy):
							return ([troop_to_deploy], [position_of_troop_to_deploy])
							change_team_signal(length_of_team_signal - 25, "0")
						else:
							return (None, None)
	left_troops_to_consider = []
	right_troops_to_consider = []
	max_score = 0
	max_score_index = 0
	left_attacked = 0
	right_attacked = 0
	counter = 0
	for troop in my_troops:
		if troop.position[1] > 30:
			if troop.position[0] < 0:
				left_attacked = counter + 1
			else:
				right_attacked = counter + 1
		counter += 1

	if left_attacked:
		troop_attacking = my_troops[left_attacked - 1]
		for temp_troop in opp_troops:
			if Utils.calculate_distance(troop_attacking, temp_troop) - temp_troop.size - troop_attacking.size < 2:
				left_troops_to_consider.append(temp_troop)
			(troop_to_deploy, position_of_troop_to_deploy) = find_counters_for_troops(length_of_team_signal, 1, 0, distance_damage_troops, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, [], left_troops_to_consider, recommended_counters, my_troops_order, my_troops_list, my_elixir, emergency=False, attacking=True)
			if not troop_to_deploy:
				return (None, None) 
			if my_elixir >= elixir(troop_to_deploy):
				return ([troop_to_deploy], [position_of_troop_to_deploy])
			else:
				return (None, None)
	if right_attacked:
		troop_attacking = my_troops[left_attacked - 1]
		for temp_troop in opp_troops:
			if Utils.calculate_distance(troop_attacking, temp_troop) - temp_troop.size - troop_attacking.size < 2:
				right_troops_to_consider.append(temp_troop)
			(troop_to_deploy, position_of_troop_to_deploy) = find_counters_for_troops(length_of_team_signal, 0, 1, distance_damage_troops, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, right_troops_to_consider, [], recommended_counters, my_troops_order, my_troops_list, my_elixir, emergency=False, attacking=True)
			if not troop_to_deploy:
				return (None, None) 
			if my_elixir >= elixir(troop_to_deploy):
				return ([troop_to_deploy], [position_of_troop_to_deploy])
			else:
				return (None, None)

	left_troops_to_consider = []
	right_troops_to_consider = []
	temp_opp_troops = opp_troops.copy()
	for main_troop in temp_opp_troops:
		if main_troop.position[0] < 0:
			for troop in opp_troops:
				if Utils.calculate_distance(troop, main_troop) - troop.size - main_troop.size < 2:
					if troop in temp_opp_troops:
						temp_opp_troops.remove(troop)
					left_troops_to_consider.append(troop)
		if main_troop.position[0] > 0:
			for troop in opp_troops:
				if Utils.calculate_distance(troop, main_troop) - troop.size - main_troop.size < 2:
					if troop in temp_opp_troops:
						temp_opp_troops.remove(troop)
					right_troops_to_consider.append(troop)

	if good_enough_databasing_done:
		if not len(left_troops_to_consider):
			counter = 0
			for troop in my_troops_order[:4]:
				if troop in ["Giant", "Balloon"]:
					continue
				if my_elixir < elixir(troop):
					continue
				index = find_index(my_troops_list, troop)
				indexes_of_troops_in_recommended_counters = find_index(indexes_of_troops_in_recommended_counters, troop)
				max_value = max_value_for_each_troop[indexes_of_troops_in_recommended_counters]
				score = 0
				mapping_of_troop = [0, 0, 0, 0, 0, 0, 0, 0]
				for temp_list in enumerat(team_signal[12 + 8*index:12 + 8*(index + 1)]):
					mapping_of_troop[temp_list[0]] = hexacontadidecimal_to_int(temp_list[1])
				if troop in no_sole_attack:
					continue
				else:
					index = find_max_index(mapping_of_troop)
					opp_troop_map = opponent_troops_list[index]
					if opp_troop_map in opponent_troops_order[4:]:
						troops_to_counter = opponent_troops_order[:4]
						my_troops_order_left = my_troops_order.copy()
						my_troops_order_left.remove(troop)
						index_of_best_counter = find_counter_for_hypothetical_troops(troops_to_counter, indexes_of_troops_in_recommended_counters, value_for_each_counter, my_troops_order_left, recommended_counters)
						if not index_of_best_counter:
							index_of_best_counter = find_index_of_least_elixir_card(my_troops_order_left)
						troop_to_counter = my_troops_order_left[index_of_best_counter]
						if my_eixir >= elixir(troop) + elixir(troop_to_counter):
							return ([troop, troop_to_counter], [(-5, 50), (-5, 50)])
						else:
							return ([troop], [(-5, 25)])
					else:
						troops_to_counter = opponent_troops_order[:4]
						troops_to_counter.append(opp_troop_map)
						my_troops_order_left = my_troops_order.copy()
						my_troops_order_left.remove(troop)
						index_of_best_counter = find_counter_for_hypothetical_troops(troops_to_counter, indexes_of_troops_in_recommended_counters, value_for_each_counter, my_troops_order_left, recommended_counters)
						if not index_of_best_counter:
							index_of_best_counter = find_index_of_least_elixir_card(my_troops_order_left)
						troop_to_counter = my_troops_order_left[index_of_best_counter]
						if my_elixir >= elixir(troop) + elixir(troop_to_counter):
							return ([troop, troop_to_counter], [(-5, 50), (-5, 50)])
						else:
							for troop in my_troops_order[:4]:
								if troop in ["Giant", "Balloon", "Valkyrie", "Knight", "Prince"] and my_elixir >= elixir(troop):
									change_team_signal(length_of_team_signal - 25, "1")
									return ([troop], [(-5, 5)])
							return (None, None)

		elif not len(right_troops_to_consider):
			counter = 0
			for troop in my_troops_order[:4]:
				if troop in ["Giant", "Balloon"]:
					continue
				if my_elixir < elixir(troop):
					continue
				index = find_index(my_troops_list, troop)
				indexes_of_troops_in_recommended_counters = find_index(indexes_of_troops_in_recommended_counters, troop)
				max_value = max_value_for_each_troop[indexes_of_troops_in_recommended_counters]
				score = 0
				mapping_of_troop = [0, 0, 0, 0, 0, 0, 0, 0]
				for temp_list in enumerat(team_signal[12 + 8*index:12 + 8*(index + 1)]):
					mapping_of_troop[temp_list[0]] = hexacontadidecimal_to_int(temp_list[1])
				if troop in no_sole_attack:
					continue
				else:
					index = find_max_index(mapping_of_troop)
					opp_troop_map = opponent_troops_list[index]
					if opp_troop_map in opponent_troops_order[4:]:
						troops_to_counter = opponent_troops_order[:4]
						my_troops_order_left = my_troops_order.copy()
						my_troops_order_left.remove(troop)
						index_of_best_counter = find_counter_for_hypothetical_troops(troops_to_counter, indexes_of_troops_in_recommended_counters, value_for_each_counter, my_troops_order_left, recommended_counters)
						if not index_of_best_counter:
							index_of_best_counter = find_index_of_least_elixir_card(my_troops_order_left)
						troop_to_counter = my_troops_order_left[index_of_best_counter]
						if my_elixir >= elixir(troop) + elixir(troop_to_counter):
							return ([troop, troop_to_counter], [(5, 50), (5, 50)])
						else:
							return ([troop], [(5, 25)])
					else:
						troops_to_counter = opponent_troops_order[:4]
						troops_to_counter.append(opp_troop_map)
						my_troops_order_left = my_troops_order.copy()
						my_troops_order_left.remove(troop)
						index_of_best_counter = find_counter_for_hypothetical_troops(troops_to_counter, indexes_of_troops_in_recommended_counters, value_for_each_counter, my_troops_order_left, recommended_counters)
						if not index_of_best_counter:
							index_of_best_counter = find_index_of_least_elixir_card(my_troops_order_left)
						troop_to_counter = my_troops_order_left[index_of_best_counter]
						if my_elixir >= elixir(troop) + elixir(troop_to_counter):
							return ([troop, troop_to_counter], [(5, 50), (5, 50)])
						else:
							for troop in my_troops_order[:4]:
								if troop in ["Giant", "Balloon", "Valkyrie", "Knight", "Prince"] and my_elixir >= elixir(troop):
									change_team_signal(length_of_team_signal - 25, "1")
									return ([troop], [(5, 5)])
							return (None, None)

		else:
			left_threat_sum = 0
			right_threat_sum = 0
			for troop_to_counter in left_troops_to_consider:
				index_of_troop_to_counter = find_index(indexes_of_troops_in_recommended_counters, troop_to_counter.name)
				left_threat_sum += max_value_for_each_troop[index_of_troop_to_counter]
			for troop_to_counter in right_troops_to_consider:
				index_of_troop_to_counter = find_index(indexes_of_troops_in_recommended_counters, troop_to_counter.name)
				right_threat_sum += max_value_for_each_troop[index_of_troop_to_counter]
			if left_threat_sum > right_threat_sum:
				(troop_to_deploy, position_of_troop_to_deploy) = find_counters_for_troops(length_of_team_signal, 0, 1, distance_damage_troops, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, right_troops_to_consider, [], recommended_counters, my_troops_order, my_troops_list, my_elixir, emergency=False, attacking=True)
				if not troop_to_deploy:
					return (None, None) 
				if my_elixir >= elixir(troop_to_deploy):
					return ([troop_to_deploy], [position_of_troop_to_deploy])
				else:
					for troop in my_troops_order[:4]:
						if troop in ["Giant", "Balloon"] and my_elixir >= elixir(troop):
							change_team_signal(length_of_team_signal - 25, "1")
							return ([troop], [(5, 5)])
					return (None, None)
			else:
				(troop_to_deploy, position_of_troop_to_deploy) = find_counters_for_troops(length_of_team_signal, 1, 0, distance_damage_troops, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, [], left_troops_to_consider, recommended_counters, my_troops_order, my_troops_list, my_elixir, emergency=False, attacking=True)
				if not troop_to_deploy:
					return (None, None) 
				if my_elixir >= elixir(troop_to_deploy):
					return ([troop_to_deploy], [position_of_troop_to_deploy])
				else:
					for troop in my_troops_order[:4]:
						if troop in ["Giant", "Balloon"] and my_elixir >= elixir(troop):
							change_team_signal(length_of_team_signal - 25, "1")
							return ([troop], [(-5, 5)])
					return (None, None)
	else:
		left_threat_sum = 0
		right_threat_sum = 0
		for troop_to_counter in left_troops_to_consider:
			index_of_troop_to_counter = find_index(indexes_of_troops_in_recommended_counters, troop_to_counter.name)
			left_threat_sum += max_value_for_each_troop[index_of_troop_to_counter]
		for troop_to_counter in right_troops_to_consider:
			index_of_troop_to_counter = find_index(indexes_of_troops_in_recommended_counters, troop_to_counter.name)
			right_threat_sum += max_value_for_each_troop[index_of_troop_to_counter]
		if left_threat_sum > right_threat_sum:
			(troop_to_deploy, position_of_troop_to_deploy) = find_counters_for_troops(length_of_team_signal, 0, 1, distance_damage_troops, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, right_troops_to_consider, [], recommended_counters, my_troops_order, my_troops_list, my_elixir, emergency=False, attacking=True)
			if not troop_to_deploy:
				# print(f"left_threat_sum: {left_threat_sum}, right_threat_sum: {right_threat_sum}, no_troop_to_deploy")
				return (None, None) 
			if my_elixir >= elixir(troop_to_deploy):
				return ([troop_to_deploy], [position_of_troop_to_deploy])
			else:
				for troop in my_troops_order[:4]:
					if troop in ["Giant", "Balloon"] and my_elixir >= elixir(troop):
						change_team_signal(length_of_team_signal - 25, "1")
						return ([troop], [(5, 5)])
			# print(f"left_threat_sum: {left_threat_sum}, right_threat_sum: {right_threat_sum}")
			return (None, None)
		else:
			(troop_to_deploy, position_of_troop_to_deploy) = find_counters_for_troops(length_of_team_signal, 1, 0, distance_damage_troops, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, [], left_troops_to_consider, recommended_counters, my_troops_order, my_troops_list, my_elixir, emergency=False, attacking=True)
			if not troop_to_deploy:
				# print(f"right_threat_sum: {right_threat_sum}, left_threat_sum: {left_threat_sum}, no_troop_to_deploy")
				return (None, None) 
			if my_elixir >= elixir(troop_to_deploy):
				return ([troop_to_deploy], [position_of_troop_to_deploy])
			else:
				for troop in my_troops_order[:4]:
					if troop in ["Giant", "Balloon"] and my_elixir >= elixir(troop):
						change_team_signal(length_of_team_signal - 25, "1")
						return ([troop], [(-5, 5)])
			# print(f"right_threat_sum: {right_threat_sum}, left_threat_sum: {left_threat_sum}")
			return (None, None)



def initial_strategy(number_of_troops_deployed, my_deployable_troops, tank_troops, my_elixir, length_of_team_signal, no_sole_attack):
	to_deploy = []
	if number_of_troops_deployed:
		i = int(number_of_troops_deployed)
		for troop in my_deployable_troops:
			if troop not in tank_troops:
				if elixir(troop) >= my_elixir:
					to_deploy.append([temp_list[1], (-5 + 5*temp[0], 50)])
					my_elixir -= elixir(temp_list[1])
					to_deploy.append([temp_list[1], (-5 + 5*i, 50)])
					i +=  1
				else:
					return (True, to_deploy)
	else:
		for troop in tank_troops:
			if troop in my_deployable_troops:
				to_deploy.append([troop, (5, 5)])
				change_team_signal(length_of_team_signal - 25, "1")
				return (True, to_deploy)
		else:
			for temp_list in enumerat(my_deployable_troops):
				if temp_list[1] not in no_sole_attack:
					if elixir(temp_list[1]) >= my_elixir:
						to_deploy.append([temp_list[1], (-5 + 5*temp[0], 50)])
						my_elixir -= elixir(temp_list[1])
					else:
						return (True, to_deploy)
			number_of_troops_deployed = len(to_deploy)
			if number_of_troops_deployed < 3:
				change_team_signal(length_of_team_signal - 29, str(number_of_troops_deployed))
			return (True, to_deploy)

def emergency_strategy(length_of_team_signal, right_defended, left_defended, fast_attacking_troops, medium_attacking_troops, slow_attacking_troops, fast_speed_troops, medium_speed_troops, slow_speed_troops, distance_damage_troops, my_tower, previous_tower_health, opp_troops, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, recommended_counters, my_troops_order, my_troops_list, my_elixir):
	potential_damage_by_troops_per_frame = 0
	left_troops_to_consider = []
	right_troops_to_consider = []
	rate_of_decrease_of_tower_health = my_tower.health - previous_tower_health
	for main_troop in opp_troops:
		if Utils.calculate_distance(my_tower, main_troop) - my_tower.size - main_troop.size < 20:
			if main_troop.position[0] < 0:
				for troop in opp_troops:
					if Utils.calculate_distance(troop, main_troop) - troop.size - main_troop.size < 2:
						if troop in opp_troops:
							opp_troops.remove(troop)
						potential_damage_by_troops_per_frame += (troop.damage / attack_speed(troop.name))
						left_troops_to_consider.append(troop)
			if main_troop.position[0] > 0:
				for troop in opp_troops:
					if Utils.calculate_distance(troop, main_troop) - troop.size - main_troop.size < 2:
						if troop in opp_troops:
							opp_troops.remove(troop)
						potential_damage_by_troops_per_frame += (troop.damage / attack_speed(troop.name))
						right_troops_to_consider.append(troop)
	if rate_of_decrease_of_tower_health > 0.004 * my_tower.health or potential_damage_by_troops_per_frame > 0.004 * my_tower.health:
		(troop_to_deploy, position_of_troop_to_deploy) = find_counters_for_troops(length_of_team_signal, right_defended, left_defended, distance_damage_troops, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, right_troops_to_consider, left_troops_to_consider, recommended_counters, my_troops_order, my_troops_list, my_elixir, emergency=True)
		return (True, troop_to_deploy, position_of_troop_to_deploy)

	return (False, None, None)

# def spam():


def deploy(arena_data: dict):
	"""
	DON'T TEMPER DEPLOY FUNCTION
	"""
	deploy_list.list_ = []
	logic(arena_data)
	return deploy_list.list_, team_signal

def logic(arena_data: dict):
	start_time = time.time()
	global team_signal
	my_tower = arena_data["MyTower"]
	opp_tower = arena_data["OppTower"]
	my_troops = arena_data["MyTroops"]
	opp_troops = arena_data["OppTroops"]
	(good_enough_databasing_done, oldest_deployed_troop_in_team_signal, recommended_counters, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, air_troops, ground_troops, attacking_air_troops, attacking_ground_troops, swarm_troops, splash_damage_troops, distance_damage_troops, tank_troops, fast_speed_troops, medium_speed_troops, slow_speed_troops, high_damage_troops, medium_damage_troops, low_damage_troops, no_sole_attack, fast_attacking_troops, medium_attacking_troops, slow_attacking_troops, previous_tower_health, all_troops_list, my_troops_list, my_deployable_troops, my_troops_order, opponent_troops_list, opponent_troops_order, opponent_deployed_troops, opponent_deployed_troops_position, length_of_team_signal, local_time, my_elixir, opponent_elixir) = initialize(my_tower, opp_tower, my_troops, opp_troops)
	if local_time == 1:
		if not len(opp_troops) > 0:
			(initial_deployment, temp_list) = initial_strategy(0, my_deployable_troops, tank_troops, my_elixir, length_of_team_signal, no_sole_attack)
			if initial_deployment:
				for (troop_to_deploy, position_of_troop_to_deploy) in temp_list:
					deploy_list.list_.append((troop_to_deploy, position_of_troop_to_deploy))  
					change_troops_order(my_troops_order, troop_to_deploy) 
					change_team_signal(length_of_team_signal - 8 + oldest_deployed_troop_in_team_signal, str(find_index(my_troops_list, troop_to_deploy) + 1))
					oldest_deployed_troop_in_team_signal = change_oldest_deployed_troop_in_team_signal()
		else:
			troops_to_deploy = []
			(troop_to_deploy, position_of_troop_to_deploy) = defend(my_troops, opp_troops, my_tower, length_of_team_signal, distance_damage_troops, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, recommended_counters, my_troops_order, my_troops_list, my_elixir)
			if troop_to_deploy:
				elixir_of_troop = elixir(troop_to_deploy)
				if my_elixir >= elixir_of_troop:
					troops_to_deploy.append(troop_to_deploy)
					deploy_list.list_.append((troop_to_deploy, position_of_troop_to_deploy))
					my_elixir -= elixir(troop_to_deploy)
					change_team_signal(length_of_team_signal - 8 + oldest_deployed_troop_in_team_signal, str(find_index(my_troops_list, troop_to_deploy) + 1))
					oldest_deployed_troop_in_team_signal = change_oldest_deployed_troop_in_team_signal()
				else:
					change_team_signal(length_of_team_signal - 29, "1")
			if not int(team_signal[length_of_team_signal - 29]):
				(attack_troops_to_deploy, position_of_attack_troops_to_deploy) = attack(length_of_team_signal, good_enough_databasing_done, my_troops, opp_troops, no_sole_attack, distance_damage_troops, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, recommended_counters, my_troops_order, my_troops_list, my_elixir)
				if attack_troops_to_deploy:
					counter = 0
					for troop_to_deploy in attack_troops_to_deploy:
						my_elixir -= elixir(troop_to_deploy)
						if my_elixir >= 2:
							troops_to_deploy.append(troop_to_deploy)
							position_of_troop_to_deploy = position_of_attack_troops_to_deploy[counter]
							deploy_list.list_.append((troop_to_deploy, position_of_troop_to_deploy))
							change_team_signal(length_of_team_signal - 8 + oldest_deployed_troop_in_team_signal, str(find_index(my_troops_list, troop_to_deploy) + 1))
							oldest_deployed_troop_in_team_signal = change_oldest_deployed_troop_in_team_signal()
							counter += 1

	elif local_time == 2 and team_signal[length_of_team_signal - 29] != "0":
		(initial_deployment, temp_list) = initial_strategy(int(team_signal[length_of_team_signal - 29]), my_deployable_troops, tank_troops, my_elixir, length_of_team_signal, no_sole_attack)
		for (troop_to_deploy, position_of_troop_to_deploy) in temp_list:
			deploy_list.list_.append((troop_to_deploy, position_of_troop_to_deploy))   
			change_troops_order(my_troops_order, troop_to_deploy)
			change_team_signal(length_of_team_signal - 8 + oldest_deployed_troop_in_team_signal, str(find_index(my_troops_list, troop_to_deploy) + 1))
			oldest_deployed_troop_in_team_signal = change_oldest_deployed_troop_in_team_signal()
		change_team_signal(length_of_team_signal - 29, "0")
	else:
		right_defended = 0
		left_defended = 0
		for troop in my_troops:
			if Utils.calculate_distance(troop, my_tower) - troop.size - my_tower.size < 10 and troop not in tank_troops[:2]:
				if troop.position[0] < 0:
					left_defended = 1
				else:
					right_defended = 1
		(to_deploy, troop_to_deploy, position_of_troop_to_deploy) = emergency_strategy(length_of_team_signal, right_defended, left_defended, fast_attacking_troops, medium_attacking_troops, slow_attacking_troops, fast_speed_troops, medium_speed_troops, slow_speed_troops, distance_damage_troops, my_tower, previous_tower_health, opp_troops, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, recommended_counters, my_troops_order, my_troops_list, my_elixir)
		if to_deploy:
			if troop_to_deploy:
				deploy_list.list_.append((troop_to_deploy, position_of_troop_to_deploy))
				change_team_signal(length_of_team_signal - 8 + oldest_deployed_troop_in_team_signal, str(find_index(my_troops_list, troop_to_deploy) + 1))
				oldest_deployed_troop_in_team_signal = change_oldest_deployed_troop_in_team_signal()
				change_troops_order(my_troops_order, troop_to_deploy)
		else:
			troops_to_deploy = []
			(troop_to_deploy, position_of_troop_to_deploy) = defend(my_troops, opp_troops, my_tower, length_of_team_signal, distance_damage_troops, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, recommended_counters, my_troops_order, my_troops_list, my_elixir)
			if troop_to_deploy:
				elixir_of_troop = elixir(troop_to_deploy)
				if my_elixir >= elixir_of_troop:
					troops_to_deploy.append(troop_to_deploy)
					deploy_list.list_.append((troop_to_deploy, position_of_troop_to_deploy))
					my_elixir -= elixir(troop_to_deploy)
					change_team_signal(length_of_team_signal - 8 + oldest_deployed_troop_in_team_signal, str(find_index(my_troops_list, troop_to_deploy) + 1))
					oldest_deployed_troop_in_team_signal = change_oldest_deployed_troop_in_team_signal()
				else:
					change_team_signal(length_of_team_signal - 29, "1")
			if not int(team_signal[length_of_team_signal - 29]):
				(attack_troops_to_deploy, position_of_attack_troops_to_deploy) = attack(length_of_team_signal, good_enough_databasing_done, my_troops, opp_troops, no_sole_attack, distance_damage_troops, indexes_of_troops_in_recommended_counters, max_value_for_each_troop, value_for_each_counter, recommended_counters, my_troops_order, my_troops_list, my_elixir)
				# print(attack_troops_to_deploy, position_of_attack_troops_to_deploy)
				if attack_troops_to_deploy:
					counter = 0
					for troop_to_deploy in attack_troops_to_deploy:
						my_elixir -= elixir(troop_to_deploy)
						if my_elixir >= 2:
							troops_to_deploy.append(troop_to_deploy)
							position_of_troop_to_deploy = position_of_attack_troops_to_deploy[counter]
							deploy_list.list_.append((troop_to_deploy, position_of_troop_to_deploy))
							change_team_signal(length_of_team_signal - 8 + oldest_deployed_troop_in_team_signal, str(find_index(my_troops_list, troop_to_deploy) + 1))
							oldest_deployed_troop_in_team_signal = change_oldest_deployed_troop_in_team_signal()
							counter += 1

			for troop in troops_to_deploy:
				change_troops_order(my_troops_order, troop)

		# 	spam_strategy()
		# 	if spam:
		#
		# counter = 0
		# troops_to_deploy = initial_strategy()
		# counter = 0
		# if len(troop_deployed) > 0:
		#     for troop_deployed in troops_to_deploy:
		#         deploy_list.list_.append((troop_deployed,(-7,0)))
		#         change_team_signal(length_of_team_signal - 8 + counter, str(find_index(my_troops_list, troop_deployed) + 1))
		#         which_indexes_changed.append(length_of_team_signal - 8 + counter)
		#         change_troops_order(my_troops_order, troop_deployed)
		#         counter += 1

	tower_health_in_str = int_to_hexacontadidecimal(my_tower.health, three=True)
	for i in range(3):
		change_team_signal(length_of_team_signal - 28 + i, tower_health_in_str[i])

	change_team_signal(length_of_team_signal - 33, str(oldest_deployed_troop_in_team_signal))
	# spam_strategy()
	# defensive_strategy()
	# attacking_strategy()
	# medium_strategy()
	# rand = random.randint(0, 3)
	# elixir_of_troop_to_be_deployed = elixir(all_troops_list, my_deployable_troops[rand])
	# if elixir_of_troop_to_be_deployed <= my_elixir:
	#     my_elixir -= elixir_of_troop_to_be_deployed
	#     troop_deployed = my_deployable_troops[rand]
	#     deploy_list.list_.append((troop_deployed,(-25,0)))
	#     change_team_signal(length_of_team_signal - 8, str(find_index(my_troops_list, troop_deployed) + 1))
	#     change_troops_order(my_troops_order, troop_deployed)
	#     another_rand = random.randint(0, 3)
	#     while (another_rand == rand):
	#         another_rand = random.randint(0, 3)
	#     elixir_of_troop_to_be_deployed = elixir(all_troops_list, my_deployable_troops[another_rand])
	#     if my_elixir >= elixir_of_troop_to_be_deployed:
	#         my_elixir -= elixir_of_troop_to_be_deployed
	#         troop_deployed = my_deployable_troops[another_rand]
	#         deploy_list.list_.append((troop_deployed,(-25,0)))
	#         change_team_signal(length_of_team_signal - 7, str(find_index(my_troops_list, troop_deployed) + 1))
	#         change_troops_order(my_troops_order, troop_deployed)
	#         another_another_rand = random.randint(0, 3)
	#         while (another_rand == rand or another_another_rand == another_rand):
	#             another_another_rand = random.randint(0, 3)
	#         elixir_of_troop_to_be_deployed = elixir(all_troops_list, my_deployable_troops[another_another_rand])
	#         if my_elixir >= elixir_of_troop_to_be_deployed:
	#             troop_deployed = my_deployable_troops[another_rand]
	#             deploy_list.list_.append((troop_deployed,(-25,0)))
	#             change_team_signal(length_of_team_signal - 6, str(find_index(my_troops_list, troop_deployed) + 1))
	#             change_troops_order(my_troops_order, troop_deployed)
	#         else:
	#             change_team_signal(length_of_team_signal - 6, "0")
	#     else:
	#         change_team_signal(length_of_team_signal - 7, "0")
	#         change_team_signal(length_of_team_signal - 6, "0")
	#     to_team_signal_from_my_troops_order(my_troops_list, my_troops_order)
	end_time = time.time()
	# print(f"Time for per frame calculation: {round((end_time - start_time) * 1000000, 0)} microseconds")