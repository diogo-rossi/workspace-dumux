# %%          IMPORTS
############# IMPORTS ##################################################################

import os
import sys
from pathlib import Path
from glob import glob
import json

# %%          CONSTANTS
############# CONSTANTS ################################################################

LAUNCH_CONTENT = r"""{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "(gdb) Launch",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}/build-cmake/${relativeFileDirname}/${input:testCase}",
            "args": [
                "${input:paramsFile}"
            ],
            "stopAtEntry": false,
            "cwd": "${workspaceFolder}/build-cmake/${relativeFileDirname}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "miDebuggerPath": "/usr/bin/gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                },
                {
                    "description": "Set Disassembly Flavor to Intel",
                    "text": "-gdb-set disassembly-flavor intel",
                    "ignoreFailures": true
                }
            ]
        }
    ],
    "inputs": [
        {
            "type": "pickString",
            "id": "testCase",
            "description": "List of test cases",
            "options": []
        },
        {
            "type": "pickString",
            "id": "paramsFile",
            "description": "custom params.input file to use",
            "default": "",
            "options": []
        }
    ]
}"""

TASKS_CONTENT = r"""{
    "version": "2.0.0",
    "inputs": [
        {
            "type": "promptString",
            "id": "problemName",
            "description": "Name of the output file problem (empty to use default)",
            "default": ""
        },
        {
            "type": "pickString",
            "id": "controlModule",
            "description": "Choose between: all (empty), --module, --only",
            "default": "",
            "options": [
                "",
                "--module=${workspaceFolderBasename}",
                "--only=${workspaceFolderBasename}"
            ]
        },
        {
            "type": "pickString",
            "id": "cmakeOpts",
            "description": "cmake opts flags file",
            "default": "dumux/cmake.opts",
            "options": [
                "dumux/cmake.opts",
                "settings-dumux/cmake-atena.opts"
            ]
        },
        {
            "type": "pickString",
            "id": "cmakeBuildType",
            "description": "cmake build type",
            "default": "Release",
            "options": [
                "Release",
                "Debug"
            ]
        },
        {
            "type": "pickString",
            "id": "testCase",
            "description": "List of test cases",
            "options": []
        },
        {
            "type": "pickString",
            "id": "paramsFile",
            "description": "custom params.input file to use",
            "default": "",
            "options": []
        }
    ]
}"""

CPP_PROPS_CONTENT = r"""{
    "env": {
        "myIncludePath": [
            "${workspaceFolder}/../dumux/**",
            "${workspaceFolder}/../dune-common",
            "${workspaceFolder}/../dune-geometry",
            "${workspaceFolder}/../dune-grid",
            "${workspaceFolder}/../dune-istl",
            "${workspaceFolder}/../dune-localfunctions",
            "${workspaceFolder}/../dune-alugrid",
            "${workspaceFolder}/../dune-foamgrid",
            "${workspaceFolder}/../dune-subgrid",
        ]
    },
    "configurations": [
        {
            "name": "Linux",
            "includePath": [
                "${myIncludePath}"
            ],
            "defines": [],
            "compilerPath": "/usr/bin/gcc",
            "cStandard": "c11",
            "cppStandard": "c++20",
            "intelliSenseMode": "linux-gcc-x64"
        }
    ],
    "version": 4
}"""

SETTINGS_CONTENT = r"""{
    "C_Cpp.intelliSenseCachePath": "${workspaceFolder}/.vscode/.cache/",
}"""

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
