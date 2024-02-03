import sys
import json
import os
import re

from lib.gvas import GvasFile
from lib.noindent import CustomEncoder
from lib.palsav import compress_gvas_to_sav, decompress_sav_to_gvas
from lib.paltypes import PALWORLD_CUSTOM_PROPERTIES, PALWORLD_TYPE_HINTS


def main(sav_file: str, guid: str):
    if sav_file[-4:] == ".SAV":
        sav_file = sav_file[:-4]
    if guid[-4:] == ".SAV":
        guid = guid[:-4]

    convert_sav_to_json(filename=f"savs/{sav_file}.sav", output_path=f"./savs/{sav_file}.json")
    # do work on user.sav
    edit_user_json(sav_file, guid)

    convert_json_to_sav(filename=f"savs/{sav_file}.json", output_path=f"./savs/{guid}.sav")
    os.remove(f"savs/{sav_file}.json")

    convert_sav_to_json(filename="savs/Level.sav", output_path="./savs/Level.json")
    os.remove("savs/Level.sav")
    # do work on level.sav
    edit_level_json(sav_file, guid)

    convert_json_to_sav(filename="savs/Level.json", output_path="./savs/Level.sav")
    os.remove("savs/Level.json")


def format_id_string(guid: str):
    return f"{guid[0:8]}-{guid[8:12]}-{guid[12:16]}-{guid[16:20]}-{guid[20:]}"


def edit_user_json(old_id: str, new_id: str):
    print(f"Editing user.sav from {old_id} to {new_id}")
    filename = f"savs/{old_id}.json"
    old_id = format_id_string(old_id)
    new_id = format_id_string(new_id)
    with open(filename, "r+") as old_file:
        data = str(json.load(old_file))
    new_data = eval(re.sub(old_id, new_id, data, flags=re.I))  # eval(data.replace(old_id, new_id))
    os.remove(filename)
    with open(filename, 'w') as new_file:
        indent = "\t"
        json.dump(new_data, new_file, indent=indent)


def edit_level_json(old_id: str, new_id: str):
    print(f"Editing Level.sav from {old_id} to {new_id}")
    filler_id = "00000000-0000-0000-0000-000000000009"
    filename = "savs/Level.json"
    old_id = format_id_string(old_id)
    new_id = format_id_string(new_id)
    with open(filename, "r+") as old_file:
        data = str(json.load(old_file))
    temp_data = re.sub(new_id, filler_id, data, flags=re.I)  # data.replace(new_id, filler_id)
    temp_data2 = re.sub(old_id, new_id, temp_data, flags=re.I)  # eval(temp_data.replace(old_id, new_id))
    new_data = eval(re.sub(filler_id, old_id, temp_data2, flags=re.I))  # eval(temp_data2.replace(filler_id, old_id))
    os.remove(filename)
    with open(filename, 'w') as new_file:
        indent = "\t"
        json.dump(new_data, new_file, indent=indent)


def convert_sav_to_json(filename: str, output_path: str):
    minify = False
    print(f"Converting {filename} to JSON, saving to {output_path}")
    if os.path.exists(output_path):
        print(f"{output_path} already exists, this will overwrite the file")
        if not confirm_prompt("Are you sure you want to continue?"):
            exit(1)
    print(f"Decompressing sav file")
    with open(filename, "rb") as f:
        data = f.read()
        raw_gvas, _ = decompress_sav_to_gvas(data)
    print(f"Loading GVAS file")
    gvas_file = GvasFile.read(raw_gvas, PALWORLD_TYPE_HINTS, PALWORLD_CUSTOM_PROPERTIES)
    print(f"Writing JSON to {output_path}")
    with open(output_path, "w", encoding="utf8") as f:
        indent = None if minify else "\t"
        json.dump(gvas_file.dump(), f, indent=indent, cls=CustomEncoder)



def convert_json_to_sav(filename: str, output_path: str):
    print(f"Converting {filename} to SAV, saving to {output_path}")
    if os.path.exists(output_path):
        print(f"{output_path} already exists, this will overwrite the file")
        if not confirm_prompt("Are you sure you want to continue?"):
            exit(1)
    print(f"Loading JSON from {filename}")
    with open(filename, "r", encoding="utf8") as f:
        data = json.load(f)
    gvas_file = GvasFile.load(data)
    print(f"Compressing SAV file")
    if (
        "Pal.PalWorldSaveGame" in gvas_file.header.save_game_class_name
        or "Pal.PalLocalWorldSaveGame" in gvas_file.header.save_game_class_name
    ):
        save_type = 0x32
    else:
        save_type = 0x31
    sav_file = compress_gvas_to_sav(
        gvas_file.write(PALWORLD_CUSTOM_PROPERTIES), save_type
    )
    print(f"Writing SAV file to {output_path}")
    with open(output_path, "wb") as f:
        f.write(sav_file)


def confirm_prompt(question: str) -> bool:
    reply = None
    while reply not in ("y", "n"):
        reply = input(f"{question} (y/n): ").casefold()
    return reply == "y"


if __name__ == "__main__":
    a = sys.argv[1]
    b = sys.argv[2]
    main(sav_file=a.upper(), guid=b.upper())
