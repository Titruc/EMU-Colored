# Easy Map Updater
# Copyright (C) 2024  Jesse Spicer, and StickyPiston Hosting



# Import things

import json
from typing import Any
from pathlib import Path
from lib import json_manager
from lib import utils
from lib.log import log
from lib import defaults
import lib.color_manager as MK


# Initialize variables

pack_version = defaults.PACK_VERSION
PROGRAM_PATH = Path(__file__).parent

with (PROGRAM_PATH / "file_legend.json").open("r", encoding="utf-8") as file:
    FILE_LEGEND: dict[str, Any] = json.load(file)



# Define functions

def update(pack: Path, version: int):
    MK.MKprint("Updating models","EMU","CYAN")

    global pack_version
    pack_version = version

    assets_folder = pack / "assets"
    if not assets_folder.exists():
        return
    for namespace_folder in assets_folder.iterdir():
        if namespace_folder.is_file():
            continue
        models_folder = namespace_folder / "models"
        if not models_folder.exists():
            continue
        for model_path in models_folder.glob("**/*.json"):
            if not model_path.is_file():
                continue
            modified = False
            model_json, load_bool = json_manager.safe_load(model_path)
            if not load_bool:
                continue
            if "textures" not in model_json:
                continue
            if not isinstance(model_json["textures"], dict):
                continue
            for key in model_json["textures"]:
                texture = model_json["textures"][key]
                if not isinstance(texture, str):
                    continue
                if texture.startswith("#"):
                    continue
                if ":" not in texture:
                    texture = "minecraft:" + texture
                texture += ".png"
                if texture.split(":")[0] != "minecraft":
                    continue
                path = ["minecraft", "textures"] + texture.split(":")[1].split("/")

                for file_version in FILE_LEGEND:
                    if pack_version > int(file_version):
                        continue
                    legend = FILE_LEGEND[file_version]
                    for folder in path[:-1]:
                        if folder in legend:
                            legend = legend[folder]
                        else:
                            break
                    else:
                        if path[-1] in legend:
                            target = legend[path[-1]]
                        elif "*" in legend:
                            target = legend["*"]
                        else:
                            continue

                        if isinstance(target, list):
                            target = target[0]
                        elif isinstance(target, dict):
                            continue
                        new_texture = "minecraft:" + "/".join(update_texture_name("/".join(path), target).split("/")[2:])
                        
                        if texture != new_texture:
                            model_json["textures"][key] = new_texture[:-4]
                            modified = True

                        break

            if modified:
                utils.safe_file_write(model_path, json.dumps(model_json))

def update_texture_name(subdir: str, target: str) -> str:
    path = Path(subdir)
    target_path = target.replace("*", path.name).split("/")
    path = path.parent
    for target_folder in target_path:
        if target_folder == ".":
            path = path.parent
        else:
            path = path / target_folder
    return path.as_posix()