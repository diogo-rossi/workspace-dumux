# %%          IMPORTS
############# IMPORTS ##################################################################

import os
import sys
from pathlib import Path
from glob import glob
import json

# %%          CONSTANTS
############# CONSTANTS ################################################################

THIS_DIR: Path = Path(__file__).parent

with open(THIS_DIR / "cppprop_file.json", "r", encoding="utf-8") as file:
    CPP_PROPS_CONTENT = file.read()

with open(THIS_DIR / "launch_file.json", "r", encoding="utf-8") as file:
    LAUNCH_CONTENT = file.read()

with open(THIS_DIR / "settings_file.json", "r", encoding="utf-8") as file:
    SETTINGS_CONTENT = file.read()

with open(THIS_DIR / "tasks_file.json", "r", encoding="utf-8") as file:
    TASKS_CONTENT = file.read()


ROOT_DIR = Path(os.getcwd())

# %%          COLLECT
############# COLLECT ##################################################################

os.chdir(ROOT_DIR)

cmake_lists = glob(f"{ROOT_DIR}/**/CMakeLists.txt", recursive=True)

tests = []
folders = []

for file in cmake_lists:
    with open(file, "r", encoding="utf-8") as fd:
        folder = str(Path(file).parent.relative_to(ROOT_DIR))
        lines = fd.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("dumux_add_test(NAME "):
                tests.append(f"{line.split()[1]}")
                folders.append(folder)
            if line.startswith("TARGET "):
                tests.pop()
                tests.append(f"{line.split()[1]}")
                folders.pop()
                folders.append(folder)

tests = sorted(list(set(tests)))
folders = sorted(list(set(folders)))
inputs = sorted(
    list(
        set(
            map(
                lambda s: str(Path(s).name),
                glob(f"{ROOT_DIR}/**/*.input", recursive=True),
            )
        )
    )
)

print("Collected tests:")
for test in tests:
    print(f"    {test}")

print("Collected folders:")
for folder in folders:
    print(f"    {folder}")

print("Collected inputs:")
for inp in inputs:
    print(f"    {inp}")

# %%          VSCODE
############# VSCODE ###################################################################

path = f"{ROOT_DIR}/.vscode"
if not os.path.exists(path):
    print(f"Creating folder '{path}'")
    os.mkdir(path)

path = f"{ROOT_DIR}/.vscode/.cache"
if not os.path.exists(path):
    print(f"Creating folder '{path}'")
    os.mkdir(path)

path = f"{ROOT_DIR}/.vscode/logs"
if not os.path.exists(path):
    print(f"Creating folder '{path}'")
    os.mkdir(path)

path = f"{ROOT_DIR}/.vscode/.gitignore"
if not os.path.exists(path):
    print(f"Creating file '{path}'")
    with open(path, "w", encoding="utf-8") as fd:
        fd.write("*")

path = f"{ROOT_DIR}/.vscode/launch.json"
if not os.path.exists(path):
    print(f"Creating file '{path}'")
    with open(path, "w", encoding="utf-8") as json_file:
        json_file.write(LAUNCH_CONTENT)

path = f"{ROOT_DIR}/.vscode/tasks.json"
if not os.path.exists(path):
    print(f"Creating file '{path}'")
    with open(path, "w", encoding="utf-8") as json_file:
        json_file.write(TASKS_CONTENT)

path = f"{ROOT_DIR}/.vscode/c_cpp_properties.json"
if not os.path.exists(path):
    print(f"Creating file '{path}'")
    with open(path, "w", encoding="utf-8") as fd:
        fd.write(CPP_PROPS_CONTENT)

path = f"{ROOT_DIR}/.vscode/settings.json"
if not os.path.exists(path):
    print(f"Creating file '{path}'")
    with open(path, "w", encoding="utf-8") as fd:
        fd.write(SETTINGS_CONTENT)

# %%          SAVE
############# SAVE #####################################################################

with open(f"{ROOT_DIR}/.vscode/tasks.json", "r", encoding="utf-8") as json_file:
    tasks = json.load(json_file)

with open(f"{ROOT_DIR}/.vscode/launch.json", "r", encoding="utf-8") as json_file:
    launch = json.load(json_file)

inputs = [""] + inputs

tasks["inputs"][-2]["options"] = tests
tasks["inputs"][-1]["options"] = inputs
launch["inputs"][-2]["options"] = tests
launch["inputs"][-1]["options"] = inputs

print(f"Editing file '{ROOT_DIR}/.vscode/tasks.json'")
with open(f"{ROOT_DIR}/.vscode/tasks.json", "w", encoding="utf-8") as json_file:
    json.dump(tasks, json_file, indent=4, ensure_ascii=False)

print(f"Editing file '{ROOT_DIR}/.vscode/launch.json'")
with open(f"{ROOT_DIR}/.vscode/launch.json", "w", encoding="utf-8") as json_file:
    json.dump(launch, json_file, indent=4, ensure_ascii=False)

# %%          EDIT
############# EDIT #####################################################################

if input(f"> Add subdirectories to main CMakeLists.txt? (y/[n]])? ") == "y":

    with open(f"{ROOT_DIR}/CMakeLists.txt", "r", encoding="utf-8") as fd:
        lines = fd.readlines()

    changed = False
    new_lines = []
    for folder in folders:
        if all([folder not in line for line in lines]):
            new_lines.append(f"add_subdirectory({folder})\n")
            changed = True

    if changed:
        lines = lines + ["\n", "\n", "# Tests folders\n"] + new_lines

    with open(f"{ROOT_DIR}/CMakeLists.txt", "w", encoding="utf-8") as fd:
        fd.write("".join(lines))
