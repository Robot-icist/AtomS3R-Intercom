import os
import shutil

try:
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    ROOT = os.getcwd()

MAPPING = {
    "atoms3r_intercom": "firmware_atoms3r_intercom",
}

FILES = {
    "bootloader.bin": "bootloader_0x1000.bin",
    "partitions.bin": "partitions_0x8000.bin",
    "firmware.bin": "firmware_0x10000.bin",
    "littlefs.bin": "littlefs_0x670000.bin",
}

import shutil as _shutil
import subprocess

for env_name, folder in MAPPING.items():
    build_dir = os.path.join(ROOT, ".pio", "build", env_name)
    if not os.path.isdir(build_dir):
        continue
    littlefs = os.path.join(build_dir, "littlefs.bin")
    if not os.path.exists(littlefs):
        pio = _shutil.which("pio")
        if pio:
            subprocess.run([pio, "run", "-e", env_name, "-t", "buildfs"], cwd=ROOT, check=True)
    dest_dir = os.path.join(ROOT, folder)
    os.makedirs(dest_dir, exist_ok=True)
    for src_name, dst_name in FILES.items():
        src = os.path.join(build_dir, src_name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(dest_dir, dst_name))
            print(f"[m5burner] {env_name}: copied {src_name} -> {folder}/{dst_name}")