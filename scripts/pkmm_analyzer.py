# helper functions
def change_immunities(coverage, immunity, additional_immunity):
  """"Move an additional immunity from a different coverage to immunity coverage"""
  for case in coverage:
    if additional_immunity in case:
      case.remove(additional_immunity)
      immunity.append(additional_immunity)

def format_types(type_list):
    """"Format types' lists into single-easier readable words"""
    if not type_list:
        return "None"
    return ", ".join([t for t in type_list])

# main function
def enemy_analysis(df, pokemon_id, max_dex, battle_type):
    """Extract the current pokemon' info e print them in the terminal"""
    info = df.get(pokemon_id)

    if not (pokemon_id > 0 and pokemon_id <= max_dex):
        print(f"[!] ID {pokemon_id} not found")
        return
    
    name = info.name
    first_type = info.type1
    second_type = info.type2
    abilities = info.abilities

    blocking_moves_abilities = [
      ['Water Absorb', 'Storm Drain', 'Dry Skin'],    # block water moves
      ['Volt Absorb', 'Lightningrod', "Motor Drive"], # block electric moves
      ['Flash Fire'],                                 # block fire moves
      ['Sap Sipper'],                                 # block grass moves
      ['Levitate']                                    # block ground moves
    ]
    
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

    quad_effective, super_effective, normal = [], [], []
    resistence, quad_resistence, immunity = [], [], []

    for move_type, damage in info.matchups.items():
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

    # printing informations
    print("\n" + "═" * 50)
    if battle_type == 1:
      print(f" 🚀 [SINGLE BATTLE DETECTED]: #{pokemon_id} {name.upper()}")
    elif battle_type == 2:
      print(f" 🚀 [DOUBLE BATTLE DETECTED]: #{pokemon_id} {name.upper()}")
    else:
      print(f" 🚀 [TRIPLE/ROTATION BATTLE DETECTED]: #{pokemon_id} {name.upper()}")

    # clearing types
    types_str = first_type
    if second_type:
        types_str += f" / {second_type}"
    print(f" 📌 Type: {types_str}")
    print("─" * 50)

    # handle special abilities' warnings
    if additional_immunity:
        if len(abilities) > 1:
            print(f" ⚠️  WATCH OUT: Could have '{blocking_ability.strip()}'")
            print(f"     ➔ Extra immunity vs: {additional_immunity}")
        else:
            data = [quad_effective, super_effective, normal, resistence, quad_resistence]
            change_immunities(data, immunity, additional_immunity)
            print(f" ⚠️  WATCH OUT: It has '{blocking_ability.strip()}'")
            print(f"     ➔ Extra immunity vs: {additional_immunity}")
        print("─" * 50)

    # move effectiveness
    width = 7
    if quad_effective:
        print(f" 💥 {'Weak x4' :<{width}} : {format_types(quad_effective)}")
    if super_effective:
        print(f" ⚡ {'Weak x2' :<{width}} : {format_types(super_effective)}")

    if normal:
        print(f" ⚖️ {'Neutral' :<{width}} : {format_types(normal)}")

    if resistence:
        print(f" 🛡️ {'Res. x2' :<{width}} : {format_types(resistence)}")
    if quad_resistence:
        print(f" 🛡️ {'Res. x4' :<{width}} : {format_types(quad_resistence)}")
    if immunity:
        print(f" 🚫 {'Immune' :<{width}} : {format_types(immunity)}")

    # Other special cases
    if 'Thick Fat' in abilities:
        print(f" ❄️ {name} could have Thick Fat (Stronger resistence vs Fire and Ice)")

    print("═" * 50 + "\n")