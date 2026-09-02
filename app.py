# IMPORTS
import pandas as pd
import ast
import sys
import os

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

# APP STARTING
while True:
  print("Inserisci il nome di un pokemon: (q per uscire)")
  name = input().strip().lower()
  if name == 'q':
    break
  else:
    # check if pokemon's name was written correctly
    match_df = df[df['name'] == name]
    if match_df.empty:
      print(f"Pokemon '{name}' non trovato\n")
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
      print(f"Primo tipo: {first_type}")
      print(f"Secondo tipo: {second_type}")
    else:
      print(f"Tipo: {first_type}")

    if quad_effective:
      print(f"Debole x4 a mosse di tipo: {quad_effective}")

    print(f"Debole x2 a mosse di tipo: {super_effective}")
    print(f"Neutro contro mosse di tipo: {normal}")
    print(f"Resistente x2 a mosse di tipo: {resistence}")

    if quad_resistence:
      print(f"Resistente x4 a mosse di tipo: {quad_resistence}")

    if immunity:
      print(f"Immune a mosse di tipo: {immunity}")

    # print the warning only if blocking ability is not the only one that the pokemon has
    if len(abilities) > 1 and not additional_immunity == "":
      print(f"ATTENZIONE!!! Il pokemon potrebbe possedere l'abilità {blocking_ability.strip()}, quindi con un'immunità aggiuntiva al tipo {additional_immunity}")

    print("\n")