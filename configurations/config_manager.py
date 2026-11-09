import json, sys
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

def load_resources(is_exe, config):
    # project directory
    if is_exe:
        # handle .exe 
        BUNDLE_DIR = Path(sys._MEIPASS)
        APP_DIR = Path(sys.executable).resolve().parent.parent
    else:
        # handle terminal script
        APP_DIR = Path(__file__).resolve().parent.parent

    # Contains resources bundled by PyInstaller
    RESOURCE_DIR = BUNDLE_DIR if is_exe else APP_DIR
    DATASET_PATH = RESOURCE_DIR / "datasets" / "final_pokemon.csv"

    config["dataset_path"] = DATASET_PATH
    config["app_dir"] = APP_DIR

    return config


def check_path(emulator_path, rom_path, config):
    # check that configured paths are absolute
    if not emulator_path.is_absolute():
        emulator_path = (config["app_dir"] / emulator_path).resolve()

    if not rom_path.is_absolute():
        rom_path = (config["app_dir"] / rom_path).resolve()

    return emulator_path, rom_path


# show the GUI for starting the game
def show_GUI(config):
    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo(
        "Initial configuration",
        "First select the DeSmuME executable and then a USA version .nds Pokemon ROM",
        parent=root,
    )

    DESMUME_PATH = filedialog.askopenfilename(
        title="1- Select DeSmuME_0.9.13_x64.exe",
        filetypes=[("DeSmuME executable", "*.exe")]
    )

    if not DESMUME_PATH:
        sys.exit(0)

    ROM_PATH = filedialog.askopenfilename(
        title="2- Select a USA version .nds Pokemon ROM",
        filetypes=[("Nintendo DS ROM", "*nds")]
    )

    if not ROM_PATH:
        sys.exit(0)

    emulator_path, rom_path = check_path(DESMUME_PATH, ROM_PATH, config)
    config["desmume_path"] = emulator_path
    config["rom_path"] = rom_path

    return config

# Use the config from json file
def use_config_file(config):
    # specific configuration (different for every user)
    CONFIG_FILE = config["app_dir"] / "configurations" / "config.json"

    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"File not found in {CONFIG_FILE}. First create config.json following config_example.json")        

    with CONFIG_FILE.open("r", encoding="utf-8") as f:
        CONFIG = json.load(f)

    DESMUME_PATH = Path(CONFIG["desmume_path"]).expanduser()
    ROM_PATH = Path(CONFIG["rom_path"]).expanduser()

    emulator_path, rom_path = check_path(DESMUME_PATH, ROM_PATH, config)
    config["desmume_path"] = emulator_path
    config["rom_path"] = rom_path

    return config

# load your personal configuration settings
def load_config() -> dict:
    IS_EXE = getattr(sys, 'frozen', False)
    config = {}
    config = load_resources(IS_EXE, config)

    if IS_EXE:
       config = show_GUI(config)
       return config
    else:
        config = use_config_file(config)
        return config