import pandas as pd
import os
import sys
import ast
from pathlib import Path

# find the correct path
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# split single strings into a list of strings
def fix_abilities_string(abilities):
    if isinstance(abilities, list):
        return abilities
    try:
        return ast.literal_eval(abilities)
    except (ValueError, SyntaxError):
        return [abilities]

# set all names to lowecase
def fix_names(name):
    return name.lower()

# set to NaN second type of single-type pokemons
def correct_pkmn_type2(df, name):
    df.loc[df['name'] == name, 'type2'] = pd.NA

# set the correct abilities to a specific pokemon
def change_pkmn_abilities(df, name, correct_abilities):
    indices = df[df['name'] == name].index
    if not indices.empty:
        idx = indices[0]
        current_value = df.at[idx, 'abilities']
        if isinstance(current_value, list) and len(current_value) > len(correct_abilities):
            df.at[idx, 'abilities'] = correct_abilities

# add a pokemon to the dataset
def add_pkmn(name, first_type, second_type, abilities, a_bug, a_dark, a_dragon, a_electric, a_fairy, a_fight, a_fire, a_flying, a_ghost, a_grass, a_ground, a_ice, a_normal, a_poison, a_psychic, a_rock, a_steel, a_water):
    return {
        'name': name, 'type1': first_type, 'type2': second_type, 'abilities': abilities,
        'against_bug': a_bug, 'against_dark': a_dark, 'against_dragon': a_dragon,
        'against_electric': a_electric, 'against_fairy': a_fairy, 'against_fight': a_fight,
        'against_fire': a_fire, 'against_flying': a_flying, 'against_ghost': a_ghost,
        'against_grass': a_grass, 'against_ground': a_ground, 'against_ice': a_ice,
        'against_normal': a_normal, 'against_poison': a_poison, 'against_psychic': a_psychic,
        'against_rock': a_rock, 'against_steel': a_steel, 'against_water': a_water
    }

# read, load and prepare the dataset
filepath = resource_path('datasets/raw_pokemon.csv')
df = pd.read_csv(filepath)
columns_to_keep = ['pokedex_number', 'name', 'type1', 'type2', 'abilities'] + df.filter(like="against").columns.to_list()
new_df = df[columns_to_keep].copy()
new_df['abilities'] = new_df['abilities'].apply(fix_abilities_string)

# correct the second type of these pokemon
pkmn_to_reset_type2 = [
    'Rattata', 'Raticate', 'Raichu', 'Sandshrew', 'Sandslash', 'Vulpix',
    'Ninetales', 'Diglett', 'Dugtrio', 'Meowth', 'Persian', 'Grimer', 'Muk', 'Marowak'
]

for pkmn in pkmn_to_reset_type2:
    correct_pkmn_type2(new_df, pkmn)

# abilities to be overridden
abilities_overrides = {
    'Rattata': ['Run Away', 'Guts', 'Hustle'],
    'Raticate': ['Run Away', 'Guts', 'Hustle'],
    'Raichu': ['Static', 'Lightningrod'],
    'Sandshrew': ['Sand Veil', 'Sand Rush'],
    'Sandslash': ['Sand Veil', 'Sand Rush'],
    'Vulpix': ['Flash Fire', 'Drought'],
    'Ninetales': ['Flash Fire', 'Drought'],
    'Diglett': ['Sand Veil', 'Arena Trap', 'Sand Force'],
    'Dugtrio': ['Sand Veil', 'Arena Trap', 'Sand Force'],
    'Meowth': ['Pickup', 'Technician', 'Unnerve'],
    'Persian': ['Limber', 'Technician', 'Unnerve'],
    'Geodude': ['Rock Head', 'Sturdy', 'Sand Veil'],
    'Graveler': ['Rock Head', 'Sturdy', 'Sand Veil'],
    'Golem': ['Rock Head', 'Sturdy', 'Sand Veil'],
    'Grimer': ['Stench', 'Sticky Hold', 'Poison Touch'],
    'Muk': ['Stench', 'Sticky Hold', 'Poison Touch'],
    'Exeggutor': ['Chlorophyll', 'Harvest'],
    'Marowak': ['Rock Head', 'Ligthningrod', 'Battle Armor']
}

for pkmn, abilities in abilities_overrides.items():
    change_pkmn_abilities(new_df, pkmn, abilities)

# pokemon to be added
new_pkmn = [
    add_pkmn('Alolan Rattata', 'dark', 'normal', ['Gluttony', 'Hustle', 'Thick Fat'], 2, 0.5, 1, 1, 2, 4, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1),
    add_pkmn('Alolan Raticate', 'dark', 'normal', ['Gluttony', 'Hustle', 'Thick Fat'], 2, 0.5, 1, 1, 2, 4, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1),
    add_pkmn('Alolan Raichu', 'electric', 'psychic', ['Surge Surfer', 'Lightningrod'], 2, 2, 1, 0.5, 1, 0.5, 1, 0.5, 2, 1, 2, 1, 1, 1, 0.5, 1, 0.5, 1),
    add_pkmn('Alolan Sandshrew', 'ice', 'steel', ['Snow Cloak', 'Slush Rush'], 0.5, 1, 0.5, 1, 0.5, 4, 4, 0.5, 1, 0.5, 2, 0.25, 0.5, 0, 0.5, 1, 1, 1),
    add_pkmn('Alolan Sandslash', 'ice', 'steel', ['Snow Cloak', 'Slush Rush'], 0.5, 1, 0.5, 1, 0.5, 4, 4, 0.5, 1, 0.5, 2, 0.25, 0.5, 0, 0.5, 1, 1, 1),
    add_pkmn('Alolan Vulpix', 'ice', 'fairy', ['Snow Cloak', 'Snow Warning'], 0.5, 0.5, 0, 1, 1, 1, 2, 1, 1, 1, 1, 0.5, 1, 2, 1, 2, 4, 1),
    add_pkmn('Alolan Ninetales', 'ice', 'fairy', ['Snow Cloak', 'Snow Warning'], 0.5, 0.5, 0, 1, 1, 1, 2, 1, 1, 1, 1, 0.5, 1, 2, 1, 2, 4, 1),
    add_pkmn('Alolan Diglett', 'ground', 'steel', ['Sand Veil', 'Tangling Hair', 'Sand Force'], 0.5, 1, 0.5, 0, 0.5, 2, 2, 0.5, 1, 1, 2, 1, 0.5, 0, 0.5, 0.25, 0.5, 2),
    add_pkmn('Alolan Dugtrio', 'ground', 'steel', ['Sand Veil', 'Tangling Hair', 'Sand Force'], 0.5, 1, 0.5, 0, 0.5, 2, 2, 0.5, 1, 1, 2, 1, 0.5, 0, 0.5, 0.25, 0.5, 2),
    add_pkmn('Alolan Meowth', 'dark', pd.NA, ['Pickup', 'Technician', 'Rattled'], 2, 0.5, 1, 1, 2, 2, 1, 1, 0.5, 1, 1, 1, 1, 1, 0, 1, 1, 1),
    add_pkmn('Alolan Persian', 'dark', pd.NA, ['Fur Coat', 'Technician', 'Rattled'], 2, 0.5, 1, 1, 2, 2, 1, 1, 0.5, 1, 1, 1, 1, 1, 0, 1, 1, 1),
    add_pkmn('Alolan Geodude', 'rock', 'electric', ['Magnet Pull', 'Sturdy', 'Galvanize'], 1, 1, 1, 0.5, 1, 2, 0.5, 0.25, 1, 2, 4, 1, 0.5, 0.5, 1, 1, 1, 2),
    add_pkmn('Alolan Graveler', 'rock', 'electric', ['Magnet Pull', 'Sturdy', 'Galvanize'], 1, 1, 1, 0.5, 1, 2, 0.5, 0.25, 1, 2, 4, 1, 0.5, 0.5, 1, 1, 1, 2),
    add_pkmn('Alolan Golem', 'rock', 'electric', ['Magnet Pull', 'Sturdy', 'Galvanize'], 1, 1, 1, 0.5, 1, 2, 0.5, 0.25, 1, 2, 4, 1, 0.5, 0.5, 1, 1, 1, 2),
    add_pkmn('Alolan Grimer', 'poison', 'dark', ['Poison Touch', 'Gluttony', 'Power of Alchemy'], 1, 0.5, 1, 1, 1, 1, 1, 1, 0.5, 0.5, 2, 1, 1, 0.5, 0, 1, 1, 1),
    add_pkmn('Alolan Muk', 'poison', 'dark', ['Poison Touch', 'Gluttony', 'Power of Alchemy'], 1, 0.5, 1, 1, 1, 1, 1, 1, 0.5, 0.5, 2, 1, 1, 0.5, 0, 1, 1, 1),
    add_pkmn('Alolan Exeggutor', 'grass', 'dragon', ['Frisk', 'Harvest'], 2, 1, 2, 0.25, 2, 1, 1, 2, 1, 0.25, 0.5, 4, 1, 2, 1, 1, 1, 0.25),
    add_pkmn('Alolan Marowak', 'fire', 'ghost', ['Cursed Body', 'Lightningrod', 'Rock Head'], 0.25, 2, 1, 1, 0.5, 0, 0.5, 1, 2, 0.5, 2, 0.5, 0, 0.5, 1, 2, 0.5, 2),
    add_pkmn('Mega Venusaur', 'grass', 'poison', ['Thick Fat'], 1, 1, 1, 0.5, 0.5, 0.5, 2, 2, 1, 0.25, 1, 2, 1, 1, 2, 1, 1, 0.5),
    add_pkmn('Mega Charizard Y', 'fire', 'flying', ['Drought'], 0.25, 1, 1, 2, 0.5, 0.5, 0.5, 1, 1, 0.25, 0, 1, 1, 1, 1, 4, 0.5, 2),
    add_pkmn('Mega Charizard X', 'fire', 'dragon', ['Tough Claws'], 0.5, 1, 2, 0.5, 1, 1, 0.25, 1, 1, 0.25, 2, 1, 1, 1, 1, 2, 0.5, 1),
    add_pkmn('Mega Blastoise', 'water', pd.NA, ['Mega Launcher'], 1, 1, 1, 2, 1, 1, 0.5, 1, 1, 2, 1, 0.5, 1, 1, 1, 1, 0.5, 0.5),
    add_pkmn('Mega Alakazam', 'psychic', pd.NA, ['Trace'], 2, 2, 1, 1, 1, 0.5, 1, 1, 2, 1, 1, 1, 1, 1, 0.5, 1, 1, 1),
    add_pkmn('Mega Gengar', 'ghost', 'poison', ['Shadow Tag'], 0.25, 2, 1, 1, 0.5, 0, 1, 1, 2, 0.5, 2, 1, 0, 0.25, 2, 1, 1, 1),
    add_pkmn('Mega Kangaskhan', 'normal', pd.NA, ['Parental Bond'], 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    add_pkmn('Mega Pinsir', 'bug', 'flying', ['Aerilate'], 0.5, 1, 1, 2, 1, 0.25, 2, 2, 1, 0.25, 0, 2, 1, 1, 1, 4, 1, 1),
    add_pkmn('Mega Gyarados', 'water', 'dark', ['Mold Breaker'], 2, 0.5, 1, 2, 2, 2, 0.5, 1, 0.5, 2, 1, 0.5, 1, 1, 0, 1, 0.5, 0.5),
    add_pkmn('Mega Aerodactyl', 'rock', 'flying', ['Tough Claws'], 0.5, 1, 1, 2, 1, 1, 0.5, 0.5, 1, 1, 0, 2, 0.5, 0.5, 1, 2, 2, 2),
    add_pkmn('Mega Mewtwo Y', 'psychic', pd.NA, ['Insomnia'], 2, 2, 1, 1, 1, 0.5, 1, 1, 2, 1, 1, 1, 1, 1, 0.5, 1, 1, 1),
    add_pkmn('Mega Mewtwo X', 'psychic', 'fighting', ['Steadfast'], 1, 1, 1, 1, 2, 0.5, 1, 2, 2, 1, 1, 1, 1, 1, 1, 0.5, 1, 1),
    add_pkmn('Mega Ampharos', 'electric', 'dragon', ['Mold Breaker'], 1, 1, 2, 0.25, 2, 1, 0.5, 0.5, 1, 0.5, 2, 2, 1, 1, 1, 1, 0.5, 0.5),
    add_pkmn('Mega Scizor', 'bug', 'steel', ['Technician'], 0.5, 1, 0.5, 1, 0.5, 1, 4, 1, 1, 0.25, 1, 0.5, 0.5, 0, 0.5, 1, 0.5, 1),
    add_pkmn('Mega Heracross', 'bug', 'fighting', ['Skill Link'], 0.5, 0.5, 1, 1, 2, 0.5, 2, 4, 1, 0.5, 0.5, 1, 1, 1, 2, 1, 1, 1),
    add_pkmn('Mega Houndoom', 'dark', 'fire', ['Solar Power'], 1, 0.5, 1, 1, 1, 2, 0.5, 1, 0.5, 0.5, 2, 0.5, 1, 1, 0, 2, 0.5, 2),
    add_pkmn('Mega Tyranitar', 'rock', 'dark', ['Sand Stream'], 2, 0.5, 1, 1, 2, 4, 0.5, 0.5, 0.5, 2, 2, 1, 0.5, 0.5, 0, 1, 2, 2,),
    add_pkmn('Mega Blaziken', 'fire', 'fighting', ['Speed Boost'], 0.25, 0.5, 1, 1, 1, 1, 0.5, 2, 1, 0.5, 2, 0.5, 1, 1, 2, 1, 0.5, 2),
    add_pkmn('Mega Gardevoir', 'psychic', 'fairy', ['Pixilate'], 1, 1, 0, 1, 1, 0.25, 1, 1, 2, 1, 1, 1, 1, 2, 0.5, 1, 2, 1),
    add_pkmn('Mega Mawile', 'steel', 'fairy', ['Huge Power'], 0.25, 0.5, 0, 1, 0.25, 1, 2, 0.5, 1, 0.5, 2, 0.5, 0.5, 0, 0.5, 0.5, 1, 1),
    add_pkmn('Mega Aggron', 'steel', pd.NA, ['Filter'], 0.5, 1, 0.5, 1, 0.5, 2, 2, 0.5, 1, 0.5, 2, 0.5, 0.5, 0, 0.5, 0.5, 0.5, 1),
    add_pkmn('Mega Medicham', 'fighting', 'psychic', ['Pure Power'], 1, 1, 1, 1, 2, 0.5, 1, 2, 2, 1, 1, 1, 1, 1, 1, 0.5, 1, 1),
    add_pkmn('Mega Manectric', 'electric', pd.NA, ['Intimidate'], 1, 1, 1, 0.5, 1, 1, 1, 0.5, 1, 1, 2, 1, 1, 1, 1, 1, 0.5, 1),
    add_pkmn('Mega Banette', 'ghost', pd.NA, ['Prankster'], 0.25, 2, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 0, 0.5, 1, 1, 1, 1),
    add_pkmn('Mega Absol', 'dark', pd.NA, ['Magic Bounce'], 2, 0.5, 1, 1, 2, 2, 1, 1, 0.5, 1, 1, 1, 1, 1, 0, 1, 1, 1),
    add_pkmn('Mega Latias', 'dragon', 'psychic', ['Levitate'], 2, 2, 2, 0.5, 2, 0.5, 0.5, 1, 2, 0.5, 0, 2, 1, 1, 0.5, 1, 1, 0.5),
    add_pkmn('Mega Latios', 'dragon', 'psychic', ['Levitate'], 2, 2, 2, 0.5, 2, 0.5, 0.5, 1, 2, 0.5, 0, 2, 1, 1, 0.5, 1, 1, 0.5),
    add_pkmn('Mega Garchomp', 'dragon', 'ground', ['Sand Force'], 1, 1, 2, 0, 2, 1, 0.5, 1, 1, 1, 1, 4, 1, 0.5, 1, 0.5, 1, 1),
    add_pkmn('Mega Lucario', 'fighting', 'steel', ['Adaptability'], 0.25, 0.5, 0.5, 1, 1, 2, 2, 0.5, 1, 0.5, 2, 0.5, 0.5, 0, 1, 0.25, 0.5, 1),
    add_pkmn('Mega Abomasnow', 'grass', 'ice', ['Snow Warning'], 2, 1, 1, 0.5, 1, 2, 4, 2, 1, 0.5, 0.5, 1, 1, 2, 1, 2, 2, 0.5),
    add_pkmn('Mega Beedrill', 'bug', 'poison', ['Adaptability'], 0.5, 1, 1, 1, 0.5, 0.25, 2, 2, 1, 0.25, 1, 1, 1, 0.5, 2, 2, 1, 1),
    add_pkmn('Mega Pidgeot', 'normal', 'flying', ['No Guard'], 0.5, 1, 1, 2, 1, 1, 1, 1, 0, 0.5, 0, 2, 1, 1, 1, 2, 1, 1),
    add_pkmn('Mega Slowbro', 'water', 'psychic', ['Shell Armor'], 2, 2, 1, 2, 1, 0.5, 0.5, 1, 2, 2, 1, 0.5, 1, 1, 0.5, 1, 0.5, 0.5),
    add_pkmn('Mega Steelix', 'steel', 'ground', ['Sand Force'], 0.5, 1, 0.5, 0, 0.5, 2, 2, 0.5, 1, 1, 2, 1, 0.5, 0, 0.5, 0.25, 0.5, 2),
    add_pkmn('Mega Sceptile', 'grass', 'dragon', ['Lightningrod'], 2, 1, 2, 0, 2, 1, 1, 2, 1, 0.25, 0.5, 4, 1, 2, 1, 1, 1, 0.25),
    add_pkmn('Mega Swampert', 'water', 'ground', ['Swift Swim'], 1, 1, 1, 0, 1, 1, 0.5, 1, 1, 4, 1, 1, 1, 0.5, 1, 0.5, 0.5, 1),
    add_pkmn('Mega Sableye', 'dark', 'ghost', ['Magic Bounce'], 1, 1, 1, 1, 2, 0, 1, 1, 1, 1, 1, 1, 0, 0.5, 0, 1, 1, 1),
    add_pkmn('Mega Sharpedo', 'water', 'dark', ['Strong Jaw'], 2, 0.5, 1, 2, 2, 2, 0.5, 1, 0.5, 2, 1, 0.5, 1, 1, 0, 1, 0.5, 0.5),
    add_pkmn('Mega Camerupt', 'fire', 'ground', ['Sheer Force'], 0.5, 1, 1, 0, 0.5, 1, 0.5, 1, 1, 1, 2, 1, 1, 0.5, 1, 1, 0.5, 4),
    add_pkmn('Mega Altaria', 'dragon', 'fairy', ['Pixilate'], 0.5, 0.5, 0, 0.5, 2, 0.5, 0.5, 1, 1, 0.5, 1, 2, 1, 2, 1, 1, 2, 0.5),
    add_pkmn('Mega Glalie', 'ice', pd.NA, ['Refrigerate'], 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 0.5, 1, 1, 1, 2, 2, 1),
    add_pkmn('Mega Salamance', 'dragon', 'flying', ['Aerilate'], 0.5, 1, 2, 1, 2, 0.5, 0.5, 1, 1, 0.25, 0, 4, 1, 1, 1, 2, 1, 0.5),
    add_pkmn('Mega Metagross', 'steel', 'psychic', ['Tough Claws'], 1, 2, 0.5, 1, 0.5, 1, 2, 0.5, 2, 0.5, 2, 0.5, 0.5, 0, 0.5, 0.5, 0.5, 1),
    add_pkmn('Mega Lopunny', 'normal', 'fighting', ['Scrappy'], 0.5, 0.5, 1, 1, 2, 2, 1, 2, 0, 1, 1, 1, 1, 1, 2, 0.5, 1, 1),
    add_pkmn('Mega Gallade', 'psychic', 'fighting', ['Inner Focus'], 1, 1, 1, 1, 2, 0.5, 1, 2, 2, 1, 1, 1, 1, 1, 1, 0.5, 1, 1),
    add_pkmn('Mega Audino', 'normal', 'fairy', ['Healer'], 0.5, 0.5, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 2, 1, 1, 2, 1),
    add_pkmn('Mega Diancie', 'rock', 'fairy', ['Magic Bounce'], 0.5, 0.5, 0, 1, 1, 1, 0.5, 0.5, 1, 2, 2, 1, 0.5, 1, 1, 1, 4, 2),
    add_pkmn('Mega Rayquaza', 'dragon', 'flying', ['Delta Stream'], 0.5, 1, 1, 0.5, 2, 0.5, 0.5, 1, 1, 0.25, 0, 2, 1, 1, 1, 1, 1, 0.5),
    add_pkmn('Primal Groudon', 'ground', 'fire', ['Desolate Land'], 0.5, 1, 1, 0, 0.5, 1, 0.5, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0.5, 0),
    add_pkmn('Primal Kyogre', 'water', pd.NA, ['Primordial Sea'], 1, 1, 1, 2, 1, 1, 0, 1, 1, 2, 1, 0.5, 1, 1, 1, 1, 0.5, 0.5)
]

updated_df = pd.DataFrame(new_pkmn)
final_df = pd.concat([new_df, updated_df], ignore_index=True)
final_df['name'] = final_df['name'].apply(fix_names)
output_path = Path(__file__).resolve().parent.parent / "datasets" / "final_pokemon.csv"
final_df.to_csv(output_path, index=False)