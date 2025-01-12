# Easy Map Updater
# Copyright (C) 2024  Jesse Spicer, and StickyPiston Hosting



# Import things

from pathlib import Path
from typing import cast
from nbt import nbt as NBT
from nbt import region
from lib import defaults
from lib.log import log
import lib.color_manager as MK


# Initialize variables

PROGRAM_PATH = Path(__file__).parent.parent.parent



# Define functions

def extract(world: Path, get_confirmation: bool):
    MK.MKprint("Extracting entity data","EMU","CYAN")

    # Check for errors
    if not world.exists():
        MK.printError("ERROR: World does not exist!")
        return

    # Get confirmation
    if get_confirmation:
        log(f'This action will modify several region files in: {world.as_posix()}')
        confirm = input("Is this okay? (Y/N): ")
        if confirm not in ["Y", "y"]:
            MK.printColored("Action canceled","LIGHT_RED")
            return
    
    # Iterate through region files
    for path in [world, world / "DIM1", world / "DIM-1"]:
        extract_from_region_folder(world, path / "region", path / "entities")
    dimensions = (world / "dimensions")
    if dimensions.exists():
        for dimension_namespace in dimensions.iterdir():
            for dimension in dimension_namespace.iterdir():
                extract_from_region_folder(world, dimension / "region", dimension / "entities")

    log("Entity data extracted")

def extract_from_region_folder(world: Path, region_folder_path: Path, entities_folder_path: Path):
    if not region_folder_path.exists():
        return

    for region_file_path in region_folder_path.iterdir():
        extract_from_region(world, region_file_path, entities_folder_path)

def extract_from_region(world: Path, region_file_path: Path, entities_folder_path: Path):
    MK.printColoredWithoutNewLine(f" Extracting ", "BRIGHT_MAGENTA")
    MK.printColored(f"{region_file_path.name}","DEFAULT")
    
    opened_entity_file = False
    region_file = region.RegionFile(region_file_path)
    entity_file = None
    for chunk_metadata in cast(list[region.ChunkMetadata], region_file.get_metadata()):
        if defaults.DEBUG_MODE:
            MK.printColoredWithoutNewLine(f" Extracting ", "BRIGHT_MAGENTA")
            MK.printColored(f"{chunk_metadata.x}, {chunk_metadata.z}","DEFAULT")
        try:
            region_chunk = region_file.get_nbt(chunk_metadata.x, chunk_metadata.z)
        except:
            continue
        if not region_chunk:
            continue
        if "entities" not in region_chunk:
            continue
        entities: NBT.TAG_List = region_chunk["entities"]
        if entities == None or len(entities) == 0:
            del region_chunk["entities"]
            region_file.write_chunk(chunk_metadata.x, chunk_metadata.z, region_chunk)
            continue
        entity_list = region_chunk["entities"]
        del region_chunk["entities"]

        # Create entity region file if it doesn't exist
        entities_folder_path.mkdir(exist_ok=True, parents=True)
        entity_file_path = entities_folder_path / region_file_path.name
        if not entity_file_path.exists():
            with entity_file_path.open("wb") as file:
                file.write(b"")

        # Open region file if it hasn't been opened yet
        if not opened_entity_file:
            opened_entity_file = True
            entity_file = region.RegionFile(entity_file_path)

        # Open entity chunk, create it if it doesn't exist
        try:
            if entity_file:
                entity_chunk = entity_file.get_nbt(chunk_metadata.x, chunk_metadata.z)
                if not entity_chunk:
                    raise
            else:
                raise
        except:
            entity_chunk = NBT.NBTFile()
            entity_chunk["DataVersion"] = region_chunk["DataVersion"]
            entity_chunk["Position"] = NBT.TAG_Int_Array(name="Position")
            entity_chunk["Position"].value = [region_chunk["xPos"].value, region_chunk["zPos"].value]

        # Move entities
        if "Entities" not in entity_chunk:
            entity_chunk["Entities"] = entity_list
        else:
            entity_chunk["Entities"].extend(entity_list)

        # Save chunks
        region_file.write_chunk(chunk_metadata.x, chunk_metadata.z, region_chunk)
        if entity_file:
            entity_file.write_chunk(chunk_metadata.x, chunk_metadata.z, entity_chunk)