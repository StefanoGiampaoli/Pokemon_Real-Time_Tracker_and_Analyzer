import csv
import ast
import time, subprocess, sys
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from scripts.pokemon_memory_reader import PokemonMemoryReader
from scripts.pkmm_analyzer import enemy_analysis
from scripts.dynamic_dataset_builder import build_modern_dataset, build_old_dataset

IS_EXE = getattr(sys, 'frozen', False)

# project directory
if IS_EXE:
    # handle .exe 
    BUNDLE_DIR = Path(sys._MEIPASS)
    APP_DIR = Path(sys.executable).resolve().parent
else:
    # handle terminal script
    APP_DIR = Path(__file__).resolve().parent

# Contains resources bundled by PyInstaller
RESOURCE_DIR = BUNDLE_DIR if IS_EXE else APP_DIR
DATASET_CSV = RESOURCE_DIR / "datasets" / "final_pokemon.csv"

# specific configuration (different for every user)
CONFIG_FILE = APP_DIR / "configurations" / "config.json"

# show the GUI for starting the game
def show_GUI():
    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo(
        "Initial configuration",
        "First select the DeSmuME executable and then a USA version .nds Pokemon ROM",
        parent=root,
    )

    desmume_path = filedialog.askopenfilename(
        title="1- Select DeSmuME_0.9.13_x64.exe",
        filetypes=[("DeSmuME executable", "*.exe")]
    )

    if not desmume_path:
        sys.exit(0)

    rom_path = filedialog.askopenfilename(
        title="2- Select a USA version .nds Pokemon ROM",
        filetypes=[("Nintendo DS ROM", "*nds")]
    )

    if not rom_path:
        sys.exit(0)

    config = {
        "desmume_exe": desmume_path,
        "rom_path": rom_path
    }

    return config

# load your personal configuration settings
def load_config():
    if IS_EXE:
       return show_GUI()

    if not CONFIG_FILE.exists:
       raise FileNotFoundError(f"File not found in {CONFIG_FILE}. First create config.json following config_example.json")        
    
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
    dataset = {}
    columns = []
    
    with open(DATASET_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        columns = next(reader)
        id_idx = columns.index("pokedex_number")
        
        for row in reader:
            if not row or not row[id_idx]:
                continue
            poke_id = int(float(row[id_idx]))
            
            # Transform the values
            parsed_row = [
                poke_id,
                row[1],                                     # name
                row[2],                                     # first_type
                row[3] if row[3] != "" else None,           # second_type
                ast.literal_eval(row[4]),                   # abilities
            ]

            # Damage multipliers
            for val in row[5:]:
                num = float(val)
                parsed_row.append(int(num) if num.is_integer() else num)
                
            dataset[poke_id] = parsed_row
            
    return dataset, columns

def checking_loop(emulator_process, df, columns, reader):
    """"Check constantly DeSmuME RAM for new pokemon during battle"""
    print("[*] Waiting for DeSmuME memory hook...")

    # Wait for DeSmuME process to finishing loading modules in RAM
    while not reader.connect():
        # poll return None if the process is still alive
        if emulator_process.poll() is not None:
            print("[!] Emulator closed before connecting.")
            return
        time.sleep(0.5)

    while not reader.get_gen():
        time.sleep(0.5)

    game_profile, gen = reader.get_gen()

    if gen >= 6:
        df, columns = build_modern_dataset(df, columns)
    else:
        df, columns = build_old_dataset(df, columns)

    recent_id = []
    last_id = None
    last_battle_type = None

    while True:
        # Check if the user has closed the windows
        if emulator_process.poll() is not None:
            print("Closing the app...")
            break

        pokemon_data = reader.get_enemy_pokemon(game_profile)

        # Analyze different possible scenarios
        # pokemon_data = None & recent_id = [] --> waiting for the very first battle
        # pokemon_data = None & recent_id > 1  --> battle just ended, therefore you are in the overworld
        # pokemon_data != None & recent_id > 1  --> you are in a middle of a battle
        if pokemon_data is None:
            if recent_id:
                recent_id.clear()
        else:
            enemy_list, max_dex = pokemon_data
            for _, enemy_species in enumerate(enemy_list, start=1):
                battle_type = 3 if len(enemy_list) > 2 else 2 if len(enemy_list) == 2 else 1
                if enemy_species not in recent_id and (enemy_species != last_id or battle_type != last_battle_type):
                    enemy_analysis(df, columns, enemy_species, max_dex, battle_type=battle_type)
                    recent_id.append(enemy_species) # solve an infinite print in double battles
                    last_id = enemy_species         # avoid printing continously the same species back to back
                    last_battle_type = battle_type  # avoid a bug where a double battle is not detected if it has the same pokemon of a previous single battle (and the other way around)

        time.sleep(0.2)  # check every 200ms


if __name__ == "__main__":
    df_pokemon, columns = load_dataset()

    # Launch the emulator
    emulator_process = launch_emulator()

    if emulator_process is None:
        sys.exit(1)

    # Giving both the configured process and the exact PID of it
    reader = PokemonMemoryReader(
        process_name=DESMUME_EXE.name,
        pid=emulator_process.pid
    )

    try:
        checking_loop(emulator_process, df_pokemon, columns, reader)
    except KeyboardInterrupt:
        print("\nClosing the app...")