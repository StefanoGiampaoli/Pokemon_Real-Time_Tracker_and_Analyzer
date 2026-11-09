import subprocess


def launch_emulator(desmume_path, rom_path, app_dir):
    """Launch DeSmuME with the Rom already configured"""
    if not desmume_path.is_file():
        print(f"[!] DeSmuME's executable not found: {desmume_path}")
        return None

    if not rom_path.is_file():
        print(f"[!] ROM not found: {rom_path}")
        return None

    print("[*] Launching DeSmuME...")

    try:
        process = subprocess.Popen(
            [str(desmume_path), str(rom_path)],
            cwd=str(app_dir)
        )
        return process

    except OSError as exc:
        print(f"[!] DeSmuME can not be launched: {exc}")
        return None