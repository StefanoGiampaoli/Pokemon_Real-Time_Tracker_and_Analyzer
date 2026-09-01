# IMPORTS
import pandas as pd

# HELPER FUNCTIONS
def fix_abilities_string(abilities):
  return abilities.replace("[", "").replace("]", "").replace("'", "").split(",")

def fix_names(name):
  return name.lower()

def change_pkmn_abilities(name, correct_abilities):
  indices = new_df[new_df['name'] == name].index
  correct_list = correct_abilities

  if not indices.empty:
    idx = indices[0]
    current_value = new_df.at[idx, 'abilities']

    if isinstance(current_value, list) and len(current_value) > len(correct_list):
      new_df.at[idx, 'abilities'] = correct_list

def correct_pkmn_type2(name):
  new_df.loc[new_df['name'] == name, 'type2'] = pd.NA

  
def add_pkmn(name, first_type, second_type, abilities, a_bug, a_dark, a_dragon, a_electric, a_fairy, a_fight, a_fire, a_flying, a_ghost, a_grass, a_ground, a_ice, a_normal, a_poison, a_psychic, a_rock, a_steel, a_water):
    return {
      'name': name,
      'type1': first_type,
      'type2': second_type,
      'abilities': abilities,
      'against_bug': a_bug,
      'against_dark': a_dark,
      'against_dragon': a_dragon,
      'against_electric': a_electric,
      'against_fairy': a_fairy,
      'against_fight': a_fight,
      'against_fire': a_fire,
      'against_flying': a_flying,
      'against_ghost': a_ghost,
      'against_grass': a_grass,
      'against_ground': a_ground,
      'against_ice': a_ice,
      'against_normal': a_normal,
      'against_poison': a_poison,
      'against_psychic': a_psychic,
      'against_rock': a_rock,
      'against_steel': a_steel,
      'against_water': a_water
    }

# READ AND PREPARE THE DATASET
df = pd.read_csv("pokemon.csv")
columns_to_keep = ['name', 'type1', 'type2', 'abilities']
columns_to_keep += df.filter(like="against").columns.to_list()
new_df = df[columns_to_keep].copy()

# CLEANING AND FIX THE DATASET
new_df['abilities'] = new_df['abilities'].apply(fix_abilities_string)

correct_pkmn_type2('Rattata')
correct_pkmn_type2('Raticate')
correct_pkmn_type2('Raichu')
correct_pkmn_type2('Sandshrew')
correct_pkmn_type2('Sandslash')
correct_pkmn_type2('Vulpix')
correct_pkmn_type2('Ninetales')
correct_pkmn_type2('Diglett')
correct_pkmn_type2('Dugtrio')
correct_pkmn_type2('Meowth')
correct_pkmn_type2('Persian')
correct_pkmn_type2('Grimer')
correct_pkmn_type2('Muk')
correct_pkmn_type2('Marowak')

change_pkmn_abilities('Rattata', ['Run Away', 'Guts', 'Hustle'])
change_pkmn_abilities('Raticate', ['Run Away', 'Guts', 'Hustle'])
change_pkmn_abilities('Raichu', ['Static', 'Lightningrod'])
change_pkmn_abilities('Sandshrew', ['Sand Veil', 'Sand Rush'])
change_pkmn_abilities('Sandslash', ['Sand Veil', 'Sand Rush'])
change_pkmn_abilities('Vulpix', ['Flash Fire', 'Drought'])
change_pkmn_abilities('Ninetales', ['Flash Fire', 'Drought'])
change_pkmn_abilities('Diglett', ['Sand Veil', 'Arena Trap', 'Sand Force'])
change_pkmn_abilities('Dugtrio', ['Sand Veil', 'Arena Trap', 'Sand Force'])
change_pkmn_abilities('Meowth', ['Pickup', 'Technician', 'Unnerve'])
change_pkmn_abilities('Persian', ['Limber', 'Technician', 'Unnerve'])
change_pkmn_abilities('Geodude', ['Rock Head', 'Sturdy', 'Sand Veil'])
change_pkmn_abilities('Graveler', ['Rock Head', 'Sturdy', 'Sand Veil'])
change_pkmn_abilities('Golem', ['Rock Head', 'Sturdy', 'Sand Veil'])
change_pkmn_abilities('Grimer', ['Stench', 'Sticky Hold', 'Poison Touch'])
change_pkmn_abilities('Muk', ['Stench', 'Sticky Hold', 'Poison Touch'])
change_pkmn_abilities('Exeggutor', ['Chlorophyll', 'Harvest'])
change_pkmn_abilities('Marowak', ['Rock Head', 'Ligthningrod', 'Battle Armor'])

new_pkmn = []
new_pkmn.append(add_pkmn('Alolan Rattata', 'dark', 'normal', ['Gluttorny', 'Hustle', 'Thick Fat'], 2, 0.5, 1, 1, 2, 4, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1))
new_pkmn.append(add_pkmn('Alolan Raticate', 'dark', 'normal', ['Gluttorny', 'Hustle', 'Thick Fat'], 2, 0.5, 1, 1, 2, 4, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1))
new_pkmn.append(add_pkmn('Alolan Raichu', 'electric', 'psychic', ['Surge Surfer', 'Lightningrod'], 2, 2, 1, 0.5, 1, 0.5, 1, 0.5, 2, 1, 2, 1, 1, 1, 0.5, 1, 0.5, 1))
new_pkmn.append(add_pkmn('Alolan Sandshrew', 'ice', 'steel', ['Snow Cloak', 'Slush Rush'], 0.5, 1, 0.5, 1, 0.5, 4, 4, 0.5, 1, 0.5, 2, 0.25, 0.5, 0, 0.5, 1, 1, 1))
new_pkmn.append(add_pkmn('Alolan Sandslash', 'ice', 'steel', ['Snow Cloak', 'Slush Rush'], 0.5, 1, 0.5, 1, 0.5, 4, 4, 0.5, 1, 0.5, 2, 0.25, 0.5, 0, 0.5, 1, 1, 1))
new_pkmn.append(add_pkmn('Alolan Vulpix', 'ice', 'fairy', ['Snow Cloak', 'Snow Warning'], 0.5, 0.5, 0, 1, 1, 1, 2, 1, 1, 1, 1, 0.5, 1, 2, 1, 2, 4, 1))
new_pkmn.append(add_pkmn('Alolan Ninetales', 'ice', 'fairy', ['Snow Cloak', 'Snow Warning'], 0.5, 0.5, 0, 1, 1, 1, 2, 1, 1, 1, 1, 0.5, 1, 2, 1, 2, 4, 1))
new_pkmn.append(add_pkmn('Alolan Diglett', 'ground', 'steel', ['Sand Veil', 'Tangling Hair', 'Sand Force'], 0.5, 1, 0.5, 0, 0.5, 2, 2, 0.5, 1, 1, 2, 1, 0.5, 0, 0.5, 0.25, 0.5, 2))
new_pkmn.append(add_pkmn('Alolan Dugtrio', 'ground', 'steel', ['Sand Veil', 'Tangling Hair', 'Sand Force'], 0.5, 1, 0.5, 0, 0.5, 2, 2, 0.5, 1, 1, 2, 1, 0.5, 0, 0.5, 0.25, 0.5, 2))
new_pkmn.append(add_pkmn('Alolan Meowth', 'dark', pd.NA, ['Pickup', 'Technician', 'Rattled'], 2, 0.5, 1, 1, 2, 2, 1, 1, 0.5, 1, 1, 1, 1, 1, 0, 1, 1, 1))
new_pkmn.append(add_pkmn('Alolan Persian', 'dark', pd.NA, ['Fur Coat', 'Technician', 'Rattled'], 2, 0.5, 1, 1, 2, 2, 1, 1, 0.5, 1, 1, 1, 1, 1, 0, 1, 1, 1))
new_pkmn.append(add_pkmn('Alolan Geodude', 'rock', 'electric', ['Magnet Pull', 'Sturdy', 'Galvanize'], 1, 1, 1, 0.5, 1, 2, 0.5, 0.25, 1, 2, 4, 1, 0.5, 0.5, 1, 1, 1, 2))
new_pkmn.append(add_pkmn('Alolan Graveler', 'rock', 'electric', ['Magnet Pull', 'Sturdy', 'Galvanize'], 1, 1, 1, 0.5, 1, 2, 0.5, 0.25, 1, 2, 4, 1, 0.5, 0.5, 1, 1, 1, 2))
new_pkmn.append(add_pkmn('Alolan Golem', 'rock', 'electric', ['Magnet Pull', 'Sturdy', 'Galvanize'], 1, 1, 1, 0.5, 1, 2, 0.5, 0.25, 1, 2, 4, 1, 0.5, 0.5, 1, 1, 1, 2))
new_pkmn.append(add_pkmn('Alolan Grimer', 'poison', 'dark', ['Poison Touch', 'Gluttony', 'Power of Alchemy'], 1, 0.5, 1, 1, 1, 1, 1, 1, 0.5, 0.5, 2, 1, 1, 0.5, 0, 1, 1, 1))
new_pkmn.append(add_pkmn('Alolan Muk', 'poison', 'dark', ['Poison Touch', 'Gluttony', 'Power of Alchemy'], 1, 0.5, 1, 1, 1, 1, 1, 1, 0.5, 0.5, 2, 1, 1, 0.5, 0, 1, 1, 1))
new_pkmn.append(add_pkmn('Alolan Exeggutor', 'grass', 'dragon', ['Frisk', 'Harvest'], 2, 1, 2, 0.25, 2, 1, 1, 2, 1, 0.25, 0.5, 4, 1, 2, 1, 1, 1, 0.25))
new_pkmn.append(add_pkmn('Alolan Marowak', 'fire', 'ghost', ['Cursed Body', 'Lightningrod', 'Rock Head'], 0.25, 2, 1, 1, 0.5, 0, 0.5, 1, 2, 0.5, 2, 0.5, 0, 0.5, 1, 2, 0.5, 2))

alolan_pkmn = pd.DataFrame(new_pkmn)
new_df = pd.concat([new_df, alolan_pkmn], ignore_index=True)

new_df['name'] = new_df['name'].apply(fix_names)

# APP STARTING
clmns_name = new_df.columns.tolist()
name = input("Inserisci il nome di un pokemon: ").lower()
info = new_df[new_df['name'] == name].values.flatten()

blocking_moves_abilities = [['Water Absord', 'Storm Drain', 'Dry Skin'], ['Volt Absord', 'Lightningrod', "Motor Drive"], ['Flash Fire'], ['Sap Sipper'], ['Levitate']]

quad_effective = []
super_effective = []
normal = []
resistence = []
quad_resistence = []
immunity = []

abilities = info[3]
blocking_ability = ""
additional_immunity = ""
for i in range(4, len(info)):
  damage = info[i]
  move_type = (clmns_name[i].split("_"))[1]
  for ability in abilities:
    for i in range(len(blocking_moves_abilities)):
      if ability.strip() in blocking_moves_abilities[i]:
        blocking_ability = ability
        match i:
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

first_type = info[1]
second_type = info[2]

#if not pd.isna(second_type):
#  print(f"Primo tipo: {first_type}")
#  print(f"Secondo tipo: {second_type}")
#else:
#  print(f"Tipo: {first_type}")
#
#if len(quad_effective) > 0:
#  print(f"Debole x4 a mosse di tipo: {quad_effective}")
#
#print(f"Debole x2 a mosse di tipo: {super_effective}")
#print(f"Neutro contro mosse di tipo: {normal}")
#print(f"Resistente x2 a mosse di tipo: {resistence}")
#
#if len(quad_resistence) > 0:
#  print(f"Resistente x4 a mosse di tipo: {quad_resistence}")
#
#if len(immunity) > 0:
#  print(f"Immune a mosse di tipo: {immunity}")
#if not additional_immunity == "":
#  print(f"ATTENZIONE!!! Il pokemon potrebbe possedere l'abilità {blocking_ability.strip()}, quindi con un'immunità aggiuntiva al tipo {additional_immunity}")

print(new_df[new_df['name'] == 'eelektross'])