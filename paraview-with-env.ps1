# This command starts paraview in Windows, with python virtual env (venv) in the folder:
# ~/0/repos/paraview-scripts/.venv (Windows path)
# Change the folder to custom path
# It can be called from wsl or from windows

powershell.exe -command '&{paraview.exe --venv (($env:USERPROFILE -replace "\\","/") + "/0/repos/paraview-scripts/.venv")}'