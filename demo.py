import pandas as pd
import ast
import time, subprocess, sys
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from scripts.pokemon_memory_reader import PlatinumMemoryReader

# project directory
if getattr(sys, 'frozen', False):
    # handle .exe 
    BUNDLE_DIR = Path(sys._MEIPASS)
    APP_DIR = Path(sys.executable).resolve().parent
else:
    # handle terminal script
    APP_DIR = Path(__file__).resolve().parent

# project's resources
DATASET_CSV = APP_DIR / "datasets" / "final_pokemon.csv"

# specific configuration of your pc
CONFIG_FILE = APP_DIR / "configurations" / "config.json"

# load your personal configuration settings
def load_config():
    if not CONFIG_FILE.exists():
        root = tk.Tk()
        root.withdraw()
 
        messagebox.showinfo("Initial configuration")
 
        desmume_path = filedialog.askopenfilename(
           title="1-Seleziona DeSmuME_0.9.13_x64.exe",
           filetypes=[("DeSmuME executable", "*.exe")]
        )
 
        if not desmume_path:
         sys.exit(0)

        rom_path = filedialog.askopenfilename(
           title="2-Select Pokemon Platinum ROM",
           filetypes=[("Nintendo DS ROM", "*nds")]
        )

        if not rom_path:
           sys.exit(0)

        config = {
           "desmume_exe": desmume_path,
           "rom_path": rom_path
        }

        with CONFIG_FILE.open("w", encoding="utf-8") as f:
           json.dump(config, f, indent=4)

        return config
    
    with CONFIG_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

CONFIG = load_config()

DESMUME_EXE = Path(CONFIG["desmume_exe"]).expanduser()
ROM_PATH = Path(CONFIG["rom_path"]).expanduser()

# check that configured paths are absolute
if not DESMUME_EXE.is_absolute():
    DESMUME_EXE = (APP_DIR / DESMUME_EXE).resolve()

if not ROM_PATH.is_absolute():
    ROM_PATH = (APP_DIR / ROM_PATH).resolve()

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
    return ", ".join([t.capitalize() for t in type_list])

# app functions
def launch_emulator():
    """Launch DeSmuME with the Rom already configured"""
    if not DESMUME_EXE.is_file():
        print(f"[!] DeSmuME's executable not found: {DESMUME_EXE}")
        return None

    if not ROM_PATH.is_file():
        print(f"[!] ROM not found: {ROM_PATH}")
        return None

    print("[*] Launching DeSmuME...")

    try:
        process = subprocess.Popen(
            [str(DESMUME_EXE), str(ROM_PATH)],
            cwd=str(APP_DIR)
        )
        return process

    except OSError as exc:
        print(f"[!] DeSmuME can not be launched: {exc}")
        return None

def load_dataset():
    """Load the dataset"""
    df = pd.read_csv(DATASET_CSV)
    df['abilities'] = df['abilities'].apply(ast.literal_eval)
    id = 'pokedex_number'
    df[id] = df[id].fillna(0).astype(int)
    return df, id

def enemy_analysis(df, col_id, pokemon_id):
    """Extract the current pokemon' info e print them in the terminal"""
    info = df[df[col_id] == pokemon_id]
    clmns_name = df.columns.tolist()

    if info.empty:
        print(f"[!] ID {pokemon_id} not found")
        return
    info = info.values.flatten()
    name = info[1]
    first_type = info[2]
    second_type = info[3]

    blocking_moves_abilities = [
      ['Water Absorb', 'Storm Drain', 'Dry Skin'], 
      ['Volt Absorb', 'Lightningrod', "Motor Drive"], 
      ['Flash Fire'], ['Sap Sipper'], ['Levitate']
    ]

    abilities = info[4]
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

    for i in range(5, len(info)):
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

    # printing informations
    print("\n" + "═" * 50)
    print(f" 🚀 BATTLE STARTED: #{pokemon_id} {name.upper()}")

    # clearing types
    types_str = first_type.capitalize()
    if pd.notna(second_type):
        types_str += f" / {second_type.capitalize()}"
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
        print(f" ⚖️  {'Neutral' :<{width}} : {format_types(normal)}")

    if resistence:
        print(f" 🛡️  {'Res. x2' :<{width}} : {format_types(resistence)}")
    if quad_resistence:
        print(f" 🛡️  {'Res. x4' :<{width}} : {format_types(quad_resistence)}")
    if immunity:
        print(f" 🚫 {'Immune' :<{width}} : {format_types(immunity)}")

    # Other special cases
    if 'Thick Fat' in abilities:
        print(f" ❄️ {name.capitalize()} could have Thick Fat (Stronger resistence vs Fire and Ice)")

    print("═" * 50 + "\n")

def checking_loop(emulator_process, df, col_id, reader):
    """"Check constantly DeSmuME RAM for new pokemon during battle"""
    last_id = None
    print("[*] Waiting for DeSmuME memory hook...")

    # Wait for DeSmuME process to finishing loading modules in RAM
    while not reader.connect():
        if emulator_process.poll() is not None:
            print("[!] Emulator closed before connecting.")
            return
        time.sleep(0.5)

    print(f"[OK] Connected to DeSmuME (PID: {emulator_process.pid})! Checking memory...")

    while True:
        # Check if the user has closed the windows
        if emulator_process.poll() is not None:
            print("Closing the app...")
            break

        pokemon_id = reader.get_enemy_pokemon()

        # Launch the analysis if the pokemon has changed or battle has ended
        if pokemon_id != last_id:
            last_id = pokemon_id

            if pokemon_id is not None:
                enemy_analysis(df, col_id, pokemon_id)
            else:
                print("[*] Battle ended. Waiting for the next one...")

        time.sleep(0.3)  # check ogni 300ms


if __name__ == "__main__":
    df_pokemon, col_id = load_dataset()

    # Avvia l'emulatore con la ROM
    emulator_process = launch_emulator()

    if emulator_process is None:
        sys.exit(1)

    # Giving bot the configured process and the exact PID of it
    reader = PlatinumMemoryReader(
        process_name=DESMUME_EXE.name,
        pid=emulator_process.pid
    )

    try:
        checking_loop(emulator_process, df_pokemon, col_id, reader)
    except KeyboardInterrupt:
        print("\nClosing the app...")