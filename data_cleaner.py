import pandas as pd
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def fix_abilities_string(abilities):
    return abilities.replace("[", "").replace("]", "").replace("'", "").split(",")

def fix_names(name):
    return name.lower()

def correct_pkmn_type2(df, name):
    df.loc[df['name'] == name, 'type2'] = pd.NA

def change_pkmn_abilities(df, name, correct_abilities):
    indices = df[df['name'] == name].index
    if not indices.empty:
        idx = indices[0]
        current_value = df.at[idx, 'abilities']
        if isinstance(current_value, list) and len(current_value) > len(correct_abilities):
            df.at[idx, 'abilities'] = correct_abilities

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

def get_cleaned_dataset(filename="pokemon.csv"):
    filepath = resource_path(filename)
    df = pd.read_csv(filepath)
    columns_to_keep = ['name', 'type1', 'type2', 'abilities'] + df.filter(like="against").columns.to_list()
    new_df = df[columns_to_keep].copy()

    new_df['abilities'] = new_df['abilities'].apply(fix_abilities_string)

    pkmn_to_reset_type2 = [
        'Rattata', 'Raticate', 'Raichu', 'Sandshrew', 'Sandslash', 'Vulpix',
        'Ninetales', 'Diglett', 'Dugtrio', 'Meowth', 'Persian', 'Grimer', 'Muk', 'Marowak'
    ]
    for pkmn in pkmn_to_reset_type2:
        correct_pkmn_type2(new_df, pkmn)

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
        add_pkmn('Alolan Marowak', 'fire', 'ghost', ['Cursed Body', 'Lightningrod', 'Rock Head'], 0.25, 2, 1, 1, 0.5, 0, 0.5, 1, 2, 0.5, 2, 0.5, 0, 0.5, 1, 2, 0.5, 2)
    ]

    alolan_df = pd.DataFrame(new_pkmn)
    new_df = pd.concat([new_df, alolan_df], ignore_index=True)
    new_df['name'] = new_df['name'].apply(fix_names)
    
    return new_df