# Workspace DUMUX

Repository to work with DUMUX on VS Code

## Usage

Clone this repo on the same folder as the
[DUMUX installation folder](https://dumux.org/docs/doxygen/master/installation.html#configure-and-build)
(alonside with `dumux` and `dune` modules)

```
git clone https://github.com/diogo-rossi/workspace-dumux.git
```

Open the workspace in VSCode with the file
[`dumux.code-workspace`](./dumux.code-workspace).

You can configure the default folder (first folder in the workspace) in the
`"folders"` property of file [`dumux.code-workspace`](./dumux.code-workspace).

## Tasks included in the workspace

1. **Configure workspaces:** Collect test lists with python and creates .vscode
   folder

2. **`dunecontrol` to configure:** Calls `dunecontrol` in the dumux installation
   folder (run in folder above module) to configure and build the module stack

3. **`dunecontrol` to clean cache:** Calls `dunecontrol` in the dumux
   installation folder (run in folder above module) to clean the CMake cache

4. **`duneproject` to create module:** Calls `duneproject` in the dumux
   installation folder (run in folder above module) to create a new module

5. **`configure cmake`:** Reconfigure the module with `cmake build-cmake` (run
   in module folder)

6. **`make build_tests`:** Make all tests with `make build_tests` (run in
   `build-cmake` folder)

7. **Make specific test:** Make specific test with `make <test-name>` (Run in
   `build-cmake/{relative-file}` folder)

8. **Run test:** Run specific test with `<test-name> <param.input>`(Run in
   `build-cmake/{relative-file}` folder)

9. **Make and Run test:** Compile and Run specific test (Run in
   `build-cmake/{relative-file}` folder)

10. **Open Results:** Open results in Paraview (Run in
    `build-cmake/{relative-file}` folder)
