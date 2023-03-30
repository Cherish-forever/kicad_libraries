#!/usr/bin/env python3

import sys
import os
import re
from pathlib import Path
from west.commands import WestCommand
from west import log

def parse_kicad_mod(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    return {"filename": file_path, "content": content}

def save_kicad_mod(file_path, kicad_mod_data):
    with open(file_path, "w") as f:
        f.write(kicad_mod_data["content"])

def add_3d_model(kicad_mod_data, model_folder, model_file_name):
    model_path = (Path(model_folder) / model_file_name).resolve()
    model_path = model_path.as_posix()

    new_model_line = f'(model {model_path}\n    (offset (xyz 0 0 0))\n    (scale (xyz 1 1 1))\n    (rotate (xyz 0 0 0))\n  )'
    pattern = re.compile(r'\(model(?:\s|\n)*((?:\((?:[^()]+|\((?:[^()]+|\([^()]*\))*\))*\)|[^\(\)]*)*)(?:\s|\n)*\)')
    mod_end_pattern = re.compile(r'\)[^\(\)]*$')
    if re.search(pattern, kicad_mod_data["content"]):
        kicad_mod_data["content"] = re.sub(pattern, new_model_line, kicad_mod_data["content"])
    else:
        kicad_mod_data["content"] = re.sub(mod_end_pattern, '  ' + new_model_line + '\n)', kicad_mod_data["content"])

    return kicad_mod_data

def process_files_in_folder(footprint_folder, model_folder, model_file_extension):
    footprint_folder = Path(footprint_folder)
    model_folder = Path(model_folder)

    kicad_mod_files = list(footprint_folder.rglob("*.kicad_mod"))

    for kicad_mod_file in kicad_mod_files:
        kicad_mod_data = parse_kicad_mod(kicad_mod_file)
        kicad_mod_name = os.path.splitext(kicad_mod_file.name)[0]

        model_file = next(model_folder.rglob(f"{kicad_mod_name}{model_file_extension}"), None)

        if model_file:
            kicad_mod_data = add_3d_model(kicad_mod_data, model_file.parent, model_file.name)
            save_kicad_mod(kicad_mod_file, kicad_mod_data)
        else:
            print(f"Warning: No matching 3D model found for {kicad_mod_file.name}.")

def main():
    folder_path = sys.argv[1]
    model_folder = sys.argv[2]
    model_file_extension = sys.argv[3]

    process_files_in_folder(folder_path, model_folder, model_file_extension)

if __name__ == "__main__":
    main()
