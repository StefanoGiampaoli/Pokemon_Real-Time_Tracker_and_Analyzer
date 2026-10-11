# IMPORTS
import pandas as pd
import ast
import sys
import os

# if the pokemon ONLY has a blocking ability as its ability, move the blocked type location
def change_immunities(additional_immunity):
  data = [quad_effective, super_effective, normal, resistence, quad_resistence]
  for case in data:
    if additional_immunity in case:
      case.remove(additional_immunity)
      immunity.append(additional_immunity)

# find the correct path
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# LOAD DATASET ALREADY CLEANED
df = pd.read_csv(resource_path('final_pokemon.csv'))
df['abilities'] = df['abilities'].apply(ast.literal_eval)
clmns_name = df.columns.tolist()

# INSTRUCTIONS ON HOW TO SEARCH FOR POKEMONS
print("For alolan regional forms digit: alolan <pokemon name>")
print("For mega forms digit: mega <pokemon name>")
print("For primal forms digit: primal <pokemon name>")

# APP STARTING
while True:
  print("What pokemon do you want to look for? (q to quit)")
  name = input().strip().lower()
  if name == 'q':
    break
  else:
    # check if pokemon's name was written correctly
    match_df = df[df['name'] == name]
    if match_df.empty:
      print(f"Pokemon '{name}' not found\n")
      continue

    # gather info about the wanted pokemon
    info = df[df['name'] == name].values.flatten()

    # check for additional immunities thanks to some ability
    blocking_moves_abilities = [
      ['Water Absorb', 'Storm Drain', 'Dry Skin'], 
      ['Volt Absorb', 'Lightningrod', "Motor Drive"], 
      ['Flash Fire'], ['Sap Sipper'], ['Levitate']
    ]

    abilities = info[3]
    blocking_ability = ""
    additional_immunity = ""

    for ability in abilities:
      for idx, group in enumerate(blocking_moves_abilities):
        if ability.strip() in group:
          blocking_ability = ability
          match idx:
            case 0:
              additional_immunity = "water"
            case 1:
              additional_immunity = "electric"
            case 2:
              additional_immunity = "fire"
            case 3:
              additional_immunity = "grass"
            case 4:
              additional_immunity = "ground"

    # lists for each move type effectiveness
    quad_effective, super_effective, normal = [], [], []
    resistence, quad_resistence, immunity = [], [], []

    # set each move type in its group
    for i in range(4, len(info)):
      damage = info[i]
      move_type = (clmns_name[i].split("_"))[1]

      match damage:
        case 4:
          quad_effective.append(move_type)
        case 2:
          super_effective.append(move_type)
        case 1:
          normal.append(move_type)
        case 0.5:
          resistence.append(move_type)
        case 0.25:
          quad_resistence.append(move_type)
        case 0:
          immunity.append(move_type)

    # print results
    first_type = info[1]
    second_type = info[2]

    if not pd.isna(second_type):
      print(f"First type: {first_type}")
      print(f"Second type: {second_type}")
    else:
      print(f"Mono type: {first_type}")

    if len(abilities) > 1 and not additional_immunity == '':
      print(f"WATCH OUT!!! This pokemon could have '{blocking_ability.strip()}', meaning an additional immunity against {additional_immunity}")
    else:
      change_immunities(additional_immunity)
      print(f"WATCH OUT!!! This pokemon has '{blocking_ability.strip()}', meaning an additional immunity against {additional_immunity}")
    
    if quad_effective:
      print(f"x4 weakness against: {quad_effective}")

    if super_effective:
      print(f"x2 weakness against: {super_effective}")

    print(f"Neutral damage against: {normal}")

    if resistence:
      print(f"x2 resistant against: {resistence}")

    if quad_resistence:
      print(f"x4 resistant against: {quad_resistence}")

    if immunity:
      print(f"Immune against: {immunity}")

    if 'Thick Fat' in abilities:
      print(f"{name.capitalize()} could have 'Thick Fat' as ability, increasing its resistance against Fire and Ice moves")

    print("\n")