import time, sys

from configurations.config_manager import load_config
from scripts.dynamic_dataset_builder import load_dataset
from scripts.emulator_manager import launch_emulator
from scripts.pokemon_memory_reader import PokemonMemoryReader
from scripts.dynamic_dataset_builder import build_modern_dataset, build_old_dataset
from scripts.pkmm_analyzer import enemy_analysis


def checking_loop(emulator_process, df, reader):
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
        df = build_modern_dataset(df)
    else:
        df = build_old_dataset(df)

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
                    enemy_analysis(df, enemy_species, max_dex, battle_type=battle_type)
                    recent_id.append(enemy_species) # solve an infinite print in double battles
                    last_id = enemy_species         # avoid printing continously the same species back to back
                    last_battle_type = battle_type  # avoid a bug where a double battle is not detected if it has the same pokemon of a previous single battle (and the other way around)

        time.sleep(0.2)  # check every 200ms


if __name__ == "__main__":
    config = load_config()

    dataset = load_dataset(config["dataset_path"])

    # Launch the emulator
    emulator_process = launch_emulator(config["desmume_path"], config["rom_path"], config["app_dir"])

    if emulator_process is None:
        sys.exit(1)

    # Giving both the configured process and the exact PID of it
    reader = PokemonMemoryReader(
        process_name=config["desmume_path"].name,
        pid=emulator_process.pid
    )

    try:
        checking_loop(emulator_process, dataset, reader)
    except KeyboardInterrupt:
        print("\nClosing the app...")