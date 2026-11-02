import pymem
import pymem.process


class PokemonMemoryReader:
    PROCESS_NAME = "DeSmuME_0.9.13_x64.exe"
    RAM_BASE_OFFSET = 0xA915400
    GAME_CODE_OFFSET = 0x3FFE0C
    RAM_SIZE = 0x400000
    GEN4_STRIDE = 0xC0
    GEN5_STRIDE = 0x224

    GAME_PROFILES = {
        # --- Diamond & Pearl ---
        "ADAE": {"name": "Diamond (USA)",    "gen": 4, "base": 0x00107120, "offsets": [0x10, 0x5CAC], "off_hp": 0x4C, "off_max_hp": 0x50, "max_dex": 493},
        "APAE": {"name": "Pearl (USA)",      "gen": 4, "base": 0x00107120, "offsets": [0x10, 0x5CAC], "off_hp": 0x4C, "off_max_hp": 0x50, "max_dex": 493},

        # --- Platinum ---
        "CPUI": {"name": "Platino (ITA)",    "gen": 4, "base": 0x00102004, "offsets": [0x10, 0x5ED4], "off_hp": 0x4C, "off_max_hp": 0x50, "max_dex": 493},
        "CPUE": {"name": "Platinum (USA)",   "gen": 4, "base": 0x00101EA4, "offsets": [0x10, 0x5ED4], "off_hp": 0x4C, "off_max_hp": 0x50, "max_dex": 493},

        # --- HeartGold & SoulSilver ---
        "IPKI": {"name": "HeartGold (ITA)",  "gen": 4, "base": 0x001119A4, "offsets": [0x10, 0x5F24], "off_hp": 0x4C, "off_max_hp": 0x50, "max_dex": 493},
        "IPGI": {"name": "SoulSilver (ITA)", "gen": 4, "base": 0x001119A4, "offsets": [0x10, 0x5F24], "off_hp": 0x4C, "off_max_hp": 0x50, "max_dex": 493},
        "IPKE": {"name": "HeartGold (USA)",  "gen": 4, "base": 0x00111A04, "offsets": [0x10, 0x5F24], "off_hp": 0x4C, "off_max_hp": 0x50, "max_dex": 493},
        "IPGE": {"name": "SoulSilver (USA)", "gen": 4, "base": 0x00111A04, "offsets": [0x10, 0x5F24], "off_hp": 0x4C, "off_max_hp": 0x50, "max_dex": 493},

        # --- White & Black ---
        "IRAI": {"name": "Bianco (ITA)",     "gen": 5, "base": 0x000F30D8, "p2_offsets": [0x6A4],                                         "max_dex": 649},
        "IRBI": {"name": "Nero (ITA)",       "gen": 5, "base": 0x000F30D8, "p2_offsets": [0x6A4],                                         "max_dex": 649},
        "IRAO": {"name": "White (USA)",      "gen": 5, "base": 0x00146284, "p2_offsets": [0x214, 0x14],                                   "max_dex": 649},
        "IRBO": {"name": "Black (USA)",      "gen": 5, "base": 0x00146284, "p2_offsets": [0x214, 0x14],                                   "max_dex": 649},

        # --- White 2 & Black 2 ---
        "IRDO": {"name": "White 2 (USA)",    "gen": 5, "base": 0x000C0BFC, "p2_offsets": [0xA54],                                         "max_dex": 649},
        "IREO": {"name": "Black 2 (USA)",    "gen": 5, "base": 0x000C0BFC, "p2_offsets": [0xA54],                                         "max_dex": 649}
    }

    def __init__(self, process_name: str = None, pid: int = None):
        if process_name:
            self.PROCESS_NAME = process_name
        self.pid = pid
        self.pm = None
        self.ds_ram_base = None
        self.current_game = None

    def connect(self) -> bool:
        """Try to connect to DeSmuME process and compute RAM base offset."""
        try:
            if self.pid:
                self.pm = pymem.Pymem()
                self.pm.open_process_from_id(self.pid)
            else:
                self.pm = pymem.Pymem(self.PROCESS_NAME)

            modulo = pymem.process.module_from_name(self.pm.process_handle, self.PROCESS_NAME)
            if not modulo:
                return False

            self.ds_ram_base = modulo.lpBaseOfDll + self.RAM_BASE_OFFSET
            print("Connected!")
            return True
        except Exception:
            self.pm = None
            self.ds_ram_base = None
            return False
        
    @staticmethod
    def is_valid_pointer(ptr: int) -> bool:
        """Validate if a pointer falls within DS Main RAM and is 32-bit word aligned."""
        return (0x02000000 <= ptr < 0x02400000) and (ptr % 4 == 0)

    def read_gen4_battle(self, profile: dict) -> list[int] | None:
        """Read active enemy Pokemon in 4th Gen battles (both single and double)."""
        ptr = self.pm.read_uint(self.ds_ram_base + profile["base"])
        if not self.is_valid_pointer(ptr):
            return None

        p1_off = ptr - 0x02000000

        # Block every other menu type (trainier card, bag, ecc...) other than the BattleTask
        task_id = self.pm.read_uint(self.ds_ram_base + p1_off + 0x14) & 0xFF
        if task_id != 0x03:
            return None

        battle_sys = self.pm.read_uint(self.ds_ram_base + p1_off + profile["offsets"][0])
        if not self.is_valid_pointer(battle_sys):
            return None

        base_battle_off = battle_sys - 0x02000000
        off_single = profile["offsets"][1]
        active_enemies = []

        enemy_slots = [
            off_single,                           # Right enemy
            off_single + (2 * self.GEN4_STRIDE)   # Left enemy
        ]

        for off in enemy_slots:
            addr = self.ds_ram_base + base_battle_off + off
            species = self.pm.read_ushort(addr)
            hp = self.pm.read_ushort(addr + profile["off_hp"])
            max_hp = self.pm.read_ushort(addr + profile["off_max_hp"])

            if 1 <= species <= profile["max_dex"] and 0 < hp <= max_hp < 1000:
                active_enemies.append(species)

        return active_enemies if active_enemies else None

    def read_gen5_battle(self, profile: dict) -> list[int] | None:
        """Read active enemy Pokemon in 5th Gen battles through PartyID deduplication."""
        ptr = self.pm.read_uint(self.ds_ram_base + profile["base"])
        if not self.is_valid_pointer(ptr):
            return None

        # Reach BattleController (p2)
        for off in profile["p2_offsets"]:
            addr = self.ds_ram_base + (ptr - 0x02000000) + off
            ptr = self.pm.read_uint(addr)
            if not self.is_valid_pointer(ptr):
                return None
        
        p2_ram = ptr - 0x02000000
        p_anchor = None

        for off in range(0x000, 0x800, 4):
            val = self.pm.read_uint(self.ds_ram_base + p2_ram + off)
            if self.is_valid_pointer(val):
                test_addr = self.ds_ram_base + (val - 0x02000000) + 0x0C
                if 0 <= (val - 0x02000000) + 0x0C <= self.RAM_SIZE - 20:
                    sp = self.pm.read_ushort(test_addr)
                    mhp = self.pm.read_ushort(test_addr + 0x02)
                    if 1 <= sp <= profile["max_dex"] and 1 <= mhp < 1000:
                        p_anchor = val
                        break

        if not p_anchor:
            return None

        # Sweep the array and deduplicate enemies by their distinct Party ID
        anchor_species_ds = p_anchor + 0x0C
        active_enemies = {}  # Dictionary mapped by party_id

        for step in range(-12, 13):
            slot_ram = (anchor_species_ds + (step * self.GEN5_STRIDE)) - 0x02000000
            if not (0 <= slot_ram <= self.RAM_SIZE - 20):
                continue
            
            addr = self.ds_ram_base + slot_ram
            species = self.pm.read_ushort(addr)
            max_hp = self.pm.read_ushort(addr + 0x02)
            hp = self.pm.read_ushort(addr + 0x04)
            party_id = self.pm.read_bytes(addr + 0x0D, 1)[0]
            flag = self.pm.read_bytes(addr + 0x0F, 1)[0]

            if 1 <= species <= profile["max_dex"] and 0 < hp <= max_hp < 1000:
                is_enemy = (party_id >= 8) or ((party_id & 0x08) != 0)
                is_active = (flag & 0x80) != 0

                if is_enemy and is_active:
                    # solve the Client/Server bug by let duplicate overwrite the same key
                    active_enemies[party_id] = species

        if not active_enemies:
            return None

        # Sort descending by party_id so visual order on screen maps left-to-right correctly
        sorted_enemies = sorted(active_enemies.items(), key=lambda x: -x[0])
        return [species for _, species in sorted_enemies]

    def get_enemy_pokemon(self) -> tuple[list[int], int] | None:
        """Return a tuple of (list_of_enemy_species, max_dex) if in battle, else None."""
        if not self.pm or not self.ds_ram_base:
            if not self.connect():
                return None

        try:
            game_code = self.pm.read_bytes(self.ds_ram_base + self.GAME_CODE_OFFSET, 4).decode("ascii", errors="ignore")
            game_profile = self.GAME_PROFILES.get(game_code)
            if not game_profile:
                return None

            if self.current_game != game_code:
                self.current_game = game_code
                print(f"[*] Game detected: Pokemon {game_profile['name']} [{game_code}]")

            if game_profile["gen"] == 4:
                enemies = self.read_gen4_battle(game_profile)
            else:
                enemies = self.read_gen5_battle(game_profile)

            if enemies:
                return enemies, game_profile["max_dex"]

            return None

        except (pymem.exception.MemoryReadError, pymem.exception.ProcessError):
            return None
        except Exception:
            return None