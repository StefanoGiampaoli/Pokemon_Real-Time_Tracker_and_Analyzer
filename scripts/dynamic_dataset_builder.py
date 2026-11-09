import csv, ast
from dataclasses import dataclass, field

@dataclass
class Pokemon:
    pokedex_id: int
    name: str
    type1: str
    type2: str | None
    abilities: list
    matchups: dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        # Format names and types as soon as the obj is created
        self.name = self.name.capitalize()
        self.type1 = self.type1.capitalize()
        if self.type2:
            self.type2 = self.type2.capitalize()


TYPE_CHART_GEN_2_TO_5 = {
    # move selected -> {enemy type's multiplier}
    "Normal":   {"Rock": 0.5, "Ghost": 0.0, "Steel": 0.5},
    "Fire":     {"Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 2.0, "Bug": 2.0, "Rock": 0.5, "Dragon": 0.5, "Steel": 2.0},
    "Water":    {"Fire": 2.0, "Water": 0.5, "Grass": 0.5, "Ground": 2.0, "Rock": 2.0, "Dragon": 0.5},
    "Electric": {"Water": 2.0, "Electric": 0.5, "Grass": 0.5, "Ground": 0.0, "Flying": 2.0, "Dragon": 0.5},
    "Grass":    {"Fire": 0.5, "Water": 2.0, "Grass": 0.5, "Poison": 0.5, "Ground": 2.0, "Flying": 0.5, "Bug": 0.5, "Rock": 2.0, "Dragon": 0.5, "Steel": 0.5},
    "Ice":      {"Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 0.5, "Ground": 2.0, "Flying": 2.0, "Dragon": 2.0, "Steel": 0.5},
    "Fighting": {"Normal": 2.0, "Ice": 2.0, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Rock": 2.0, "Ghost": 0.0, "Dark": 2.0, "Steel": 2.0},
    "Poison":   {"Grass": 2.0, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0.0},
    "Ground":   {"Fire": 2.0, "Water": 0.5, "Grass": 0.5, "Electric": 2.0, "Poison": 2.0, "Flying": 0.0, "Bug": 0.5, "Rock": 2.0, "Steel": 2.0},
    "Flying":   {"Grass": 2.0, "Electric": 0.5, "Fighting": 2.0, "Bug": 2.0, "Rock": 0.5, "Steel": 0.5},
    "Psychic":  {"Fighting": 2.0, "Poison": 2.0, "Psychic": 0.5, "Dark": 0.0, "Steel": 0.5},
    "Bug":      {"Fire": 0.5, "Grass": 2.0, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Psychic": 2.0, "Ghost": 0.5, "Dark": 2.0, "Steel": 0.5},
    "Rock":     {"Fire": 2.0, "Water": 0.5, "Grass": 0.5, "Ice": 2.0, "Fighting": 0.5, "Ground": 0.5, "Flying": 2.0, "Bug": 2.0, "Steel": 0.5},
    "Ghost":    {"Normal": 0.0, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5, "Steel": 0.5}, 
    "Dragon":   {"Dragon": 2.0, "Steel": 0.5},
    "Dark":     {"Fighting": 0.5, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5, "Steel": 0.5}, 
    "Steel":    {"Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Ice": 2.0, "Rock": 2.0, "Steel": 0.5}
}

TYPE_CHART_GEN_6_AND_AFTER = {
    # move selected -> {enemy type's multiplier}
    "Normal":   {"Rock": 0.5, "Ghost": 0.0, "Steel": 0.5},
    "Fire":     {"Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 2.0, "Bug": 2.0, "Rock": 0.5, "Dragon": 0.5, "Steel": 2.0},
    "Water":    {"Fire": 2.0, "Water": 0.5, "Grass": 0.5, "Ground": 2.0, "Rock": 2.0, "Dragon": 0.5},
    "Electric": {"Water": 2.0, "Electric": 0.5, "Grass": 0.5, "Ground": 0.0, "Flying": 2.0, "Dragon": 0.5},
    "Grass":    {"Fire": 0.5, "Water": 2.0, "Grass": 0.5, "Poison": 0.5, "Ground": 2.0, "Flying": 0.5, "Bug": 0.5, "Rock": 2.0, "Dragon": 0.5, "Steel": 0.5},
    "Ice":      {"Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 0.5, "Ground": 2.0, "Flying": 2.0, "Dragon": 2.0, "Steel": 0.5},
    "Fighting": {"Normal": 2.0, "Ice": 2.0, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Rock": 2.0, "Ghost": 0.0, "Dark": 2.0, "Steel": 2.0, "Fairy": 0.5},
    "Poison":   {"Grass": 2.0, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0.0, "Fairy": 2.0},
    "Ground":   {"Fire": 2.0, "Water": 0.5, "Grass": 0.5, "Electric": 2.0, "Poison": 2.0, "Flying": 0.0, "Bug": 0.5, "Rock": 2.0, "Steel": 2.0},
    "Flying":   {"Grass": 2.0, "Electric": 0.5, "Fighting": 2.0, "Bug": 2.0, "Rock": 0.5, "Steel": 0.5},
    "Psychic":  {"Fighting": 2.0, "Poison": 2.0, "Psychic": 0.5, "Dark": 0.0, "Steel": 0.5},
    "Bug":      {"Fire": 0.5, "Grass": 2.0, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Psychic": 2.0, "Ghost": 0.5, "Dark": 2.0, "Steel": 0.5, "Fairy": 0.5},
    "Rock":     {"Fire": 2.0, "Water": 0.5, "Grass": 0.5, "Ice": 2.0, "Fighting": 0.5, "Ground": 0.5, "Flying": 2.0, "Bug": 2.0, "Steel": 0.5},
    "Ghost":    {"Normal": 0.0, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5},
    "Dragon":   {"Dragon": 2.0, "Steel": 0.5, "Fairy": 0.0},
    "Dark":     {"Fighting": 0.5, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5},
    "Steel":    {"Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Ice": 2.0, "Rock": 2.0, "Steel": 0.5, "Fairy": 2.0},
    "Fairy":    {"Fire": 0.5, "Fighting": 2.0, "Poison": 0.5, "Dragon": 2.0, "Dark": 2.0, "Steel": 0.5}
}

PRE_GEN_6_TYPE_CHANGES = {
    35: ["Normal", None],
    36: ["Normal", None],
    173: ["Normal", None],
    39: ["Normal", None],
    40: ["Normal", None],
    174: ["Normal", None],
    175: ["Normal", None],
    176: ["Normal", "Flying"],
    468: ["Normal", "Flying"],
    209: ["Normal", None],
    210: ["Normal", None],
    183: ["Water", None],
    184: ["Water", None],
    298: ["Normal", None],
    280: ["Psychic", None],
    281: ["Psychic", None],
    282: ["Psychic", None],
    439: ["Psychic", None],
    122: ["Psychic", None],
    303: ["Steel", None],
    546: ["Grass", None],
    547: ["Grass", None],
}

def load_dataset(dataset_path):
    """Load the dataset"""
    dataset = {}
    columns = []
    
    with open(dataset_path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        columns = next(reader)
        id_idx = columns.index("pokedex_number")
        
        for row in reader:
            if not row or not row[id_idx]:
                continue
            poke_id = int(float(row[id_idx]))

            # create a pokemon
            pokemon = Pokemon(
                pokedex_id=poke_id,
                name=row[1],                                # name
                type1=row[2],                               # first_type
                type2=row[3] if row[3] != "" else None,     # second_type
                abilities=ast.literal_eval(row[4])          # abilities
            )
                
            dataset[poke_id] = pokemon
                
    return dataset

def build_old_dataset(df):
    for id, types in PRE_GEN_6_TYPE_CHANGES.items():
        pkmn_info = df.get(id, None) 
        if pkmn_info:
            pkmn_info.type1 = types[0] if types[0] else None
            pkmn_info.type2 = types[1] if types[1] else None

    for pkmn_info in df.values():
        type1 = pkmn_info.type1
        type2 = pkmn_info.type2 if pkmn_info.type2 else None

        for type in TYPE_CHART_GEN_2_TO_5:
            damage_on_type1 = TYPE_CHART_GEN_2_TO_5.get(type, {}).get(type1, 1)
            if type2:
                damage_on_type2 = TYPE_CHART_GEN_2_TO_5.get(type, {}).get(type2, 1)
            final_damage = damage_on_type1 * damage_on_type2 if type2 else damage_on_type1
            pkmn_info.matchups[type] = final_damage

    return df

def build_modern_dataset(df):    
    for pkmn_info in df.values():
        type1 = pkmn_info.type1
        type2 = pkmn_info.type2 if pkmn_info.type2 else None
    
        for type in TYPE_CHART_GEN_6_AND_AFTER:
            damage_on_type1 = TYPE_CHART_GEN_6_AND_AFTER.get(type, {}).get(type1, 1)
            if type2:
                damage_on_type2 = TYPE_CHART_GEN_6_AND_AFTER.get(type, {}).get(type2, 1)
            final_damage = damage_on_type1 * damage_on_type2 if type2 else damage_on_type1
            pkmn_info.matchups[type] = final_damage
    
    return df