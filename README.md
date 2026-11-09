# Pokémon Real-Time Tracker & Analyzer

A real-time memory tracking utility for Pokémon Generation 4 and Generation 5 games running on the **DeSmuME** emulator (**Windows**). This tool seamlessly hooks into the emulator's RAM to detect active enemy Pokémon during battles (Singles, Doubles, Triples, and Rotations) and instantly provides tactical analysis (weaknesses and  resistances).

## Features
* **Zero-Click Tracking:** Automatically detects when you enter and exit battles.
* **Universal Gen 4 & 5 Support:** Works flawlessly across Diamond, Pearl, Platinum, HeartGold, SoulSilver, Black, White, Black 2, and White 2 (**ONLY .NDS'S USA VERSION ARE CURRENTLY ACCEPTED**).
* **Complex Battle Handling:** Dynamically maps memory to support multiple enemies at once.
* **Tactical Readout:** Instantly calculates and displays the enemy's type matchups via a local CSV dataset.
* **Standalone Executable:** Can be compiled into a single `.exe` using PyInstaller for easy distribution.

---

## Project Structure

```text
.
├── .github/
│   └── workflows/
│       └── build.yaml              # Automated PyInstaller build via GitHub Actions
├── configurations/
│   └── config.json                 # User-specific local paths (ignored by git)
├── datasets/
│   └── final_pokemon.csv           # Database of Pokémon types and matchups
├── scripts/
│   ├── data_cleaner.py             # Utility for dataset maintenance
|   ├── dynamic_dataset_builder.py  # Modifies the dataset according to the current gen
│   ├── pkmm_analyzer.py            # Calculates pokemon matchups with every type
│   └── pokemon_memory_reader.py    # Core RAM hooking and pointer traversal logic
├── main.py                         # Application entry point & process manager
├── pyproject.toml                  # Python dependencies configuration
├── uv.lock                         # Fast package manager lockfile
└── README.md
```

---

## Requirements

* **Operating System:** Windows (Required for `pymem` memory hooking).
* **Emulator:** `DeSmuME_0.9.13_x64.exe` (Specifically targeted by the memory reader).
* **Python Environment:** Python 3.12+ (Managed via [uv](https://docs.astral.sh/uv/)).

---

## Configuration

The application requires the exact file paths to your DeSmuME executable and the **USA** Nintendo DS ROM you wish to play. 

**Option A: Automatic GUI Setup:**
If you run the compiled `.exe`, a visual prompt will open automatically. Simply select your DeSmuME executable and your **USA** `.nds` ROM file through the dialog windows.

**Option B: Manual Setup:**
Create a file named `config.json` inside the `configurations/` folder:
```json
{
    "desmume_exe": "C:\\Path\\To\\DeSmuME_0.9.13_x64.exe",
    "rom_path": "C:\\Path\\To\\Your_Pokemon_ROM.nds"
}
```

---

## How to Run

### 1. Running from Source
This project uses `uv` for lightning-fast dependency management.
```bash
# Install dependencies
uv sync

# Run the tracker
uv run main.py
```
*Note: The script will automatically launch DeSmuME with your configured ROM and begin polling memory.*

### 2. Running the Standalone Executable
If you downloaded `tracker.exe` from the GitHub Actions artifacts (or built it yourself), simply double-click `tracker.exe`. No Python installation is required.

**To build it yourself:**
```bash
uv run pyinstaller --noconfirm --onefile --icon="ultraball.ico" --add-data "datasets/final_pokemon.csv;datasets" --name "tracker.exe" main.py
```

### 3. Dataset Management
If you need to update or modify the Pokémon dataset (`final_pokemon.csv`), it is highly recommended to apply your changes to the raw datasets and execute `data_cleaner.py`, which is responsible for cleaning, merging, and generating the final dataset. 

Run the following command before launching the main tracker:

```bash
# Generate an updated version of final_pokemon.csv
uv run scripts/data_cleaner.py
```

## Runtime Architecture & Memory Polling Lifecycle

*This section provides a deep technical walkthrough of how the real-time memory tracker initializes, attaches to the DeSmuME emulator process, monitors Nintendo DS RAM, and seamlessly transitions between overworld exploration and active battle encounters.*

### 1. Architecture Overview

The system operates across three primary layers:

```text
┌────────────────────────────────────────────────────────┐
│                   DeSmuME (x64)                        │
│   Simulated ARM9 Main RAM (0x02000000 - 0x023FFFFF)    │
└───────────────────────────▲────────────────────────────┘
                            │ PyMem Read Operations
┌───────────────────────────┴────────────────────────────┐
│              PokemonMemoryReader Engine                │
│   - ROM Header Identification (0x3FFE0C)               │
│   - Multi-Level Pointer De-referencing                 │
│   - Gen 4: Task ID Filtering & 4-Client Grid           │
│   - Gen 5: Universal Dynamic Anchor Scanning           │
└───────────────────────────▲────────────────────────────┘
                            │ Polls every 200ms
┌───────────────────────────┴────────────────────────────┐
│                    main.py Runner                      │
│   - Process Lifecycle & Crash Detection                │
│   - State Transitions (Overworld <-> Battle)           │
│   - Analysis Dispatcher (Type Multipliers & Stats)     │
└────────────────────────────────────────────────────────┘
```

### 2. Execution Phases: From Startup to First Encounter

**Phase 1: Bootstrap & Process Spawning (`main.py`)**
1. **Dataset Ingestion**: `load_dataset()` loads `final_pokemon.csv` into an in-memory dictionary indexed by national Pokédex IDs.
2. **Subprocess Instantiation**: `launch_emulator()` executes DeSmuME using `subprocess.Popen`. The OS assigns a unique Process ID (`PID`).
3. **Memory Reader Initialization**: `PokemonMemoryReader` uses this PID to secure a direct handle to the emulator's memory space via `OpenProcess`. The simulated DS ARM9 Main Memory base is computed via a fixed module offset (`ModuleBaseOfDll + 0xA915400`).

**Phase 2: The Silent Polling Loop (Overworld / Title / Menus)**
While the player explores the overworld, navigates menus, or watches cutscenes, the console remains quiet. The execution loop samples memory **every 200 ms**.
Outside of a battle, the DS game engine has not allocated the `BattleSystem` (Gen 4) or `BattleController` (Gen 5) structures. The base pointer reads either `0x00000000` or an unmapped address, causing pointer evaluation to fail immediately and returning `None`.

### 3. Generation 4 Architecture (Diamond, Pearl, Platinum, HG/SS)

**The False-Positive Challenge (Trainer Card / Bag)**
In Gen 4, the primary base pointer points to the `FieldSystem` (`p1`). The offset `p1 + 0x10` stores the pointer for *any* currently active sub-application. Opening the Trainer Card or the Bag allocates memory to the exact same pointer, filling the offsets with coordinate/graphics data that coincidentally mimic Pokémon HP and Species limits.

**Task ID Filtering**
To achieve flawless detection, the reader inspects the **Task Manager ID** located at `p1 + 0x14`:
* Overworld: Usually `0x00000000`
* Trainer Card / Bag: `0x04` or higher
* **Battle Engine**: `0x03` (The reader enforces a strict bitwise check `task_id & 0xFF == 0x03` before reading).

**The 4-Client Grid**
Once the battle task is confirmed, the system maps the field. Gen 4 uses a fixed 4-slot grid with a memory stride of `0xC0` (192 bytes):
* **Client 1 (Right Enemy)**: Base offset.
* **Client 3 (Left Enemy)**: Base offset + `2 * 0x180`.

### 4. Generation 5 Architecture (Black, White, Black 2, White 2)

Generation 5 battle memory is significantly more complex, abandoning the fixed 4-slot grid for a dynamic `BattleController` object (`p2`) and a contiguous combatant array supporting Triple and Rotation battles (stride of `0x224`).

**The Shifting Anchor Problem**
The pointer to the array inside `p2` shifts drastically depending on the opponent:
* Wild Singles: `0x15C`
* Wild Doubles: `0x5A4` (B2W2) or `0x80` (B1W1)
* Single Trainers: `0x19C`
* Full Party Trainers: `0x5E4` (can shift to `0x5EC`, `0x1B0`, etc., due to specific AI scripts).

**Deep Dynamic Scanning & Array Extraction**
To guarantee 100% detection, the reader performs a **Deep Dynamic Scan** of the entire `BattleController` object (from `0x000` to `0x800`). It checks if any word points to a valid `BattleMon` structure (Valid Species, HP > 0, Enemy Faction Flag, Active On-Field Flag).
Once *any* valid enemy is dynamically found, its address serves as the **Anchor**. The reader then sweeps the surrounding contiguous memory slots using the `0x224` stride.

**Solving the "Twin-Buffer" Bug (Client vs Server)**
Gen 5 utilizes double buffering in memory for animations and damage calculations, meaning a single enemy might appear multiple times in the array. 
To solve this flawlessly, the tracker aggregates enemies using their **`Party ID`** mapped to a Python Dictionary (`active_enemies[party_id] = species`). Duplicated memory buffers safely overwrite themselves, guaranteeing perfect support for Singles, Doubles, Triples, and Rotations without false duplicate reads.