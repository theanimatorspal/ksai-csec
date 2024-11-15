import re
from testing.require import *

packages = [
    "amass",
     "gobuster",
     "dirsearch",
     "httpx-toolkit",
     "sublist3r",
     "exiftool",

]

def InstallGo(inlink):
    match = re.search(r'/([^/@]+)@', inlink)
    if match:
        binary_name = match.group(1)
        install_cmd = rf"go install {inlink}"
        RunCommand(install_cmd, f"{binary_name} installed successfully.", f"Failed to install {binary_name}.")
        copy_cmd = rf"cp ~/go/bin/{binary_name} /usr/local/bin"
        RunCommand(copy_cmd, f"{binary_name} copied to /usr/local/bin.", f"Failed to copy {binary_name}.")
    else:
        print("Invalid link format. Could not extract binary name.")

def InstallGhauri():
    RunCommand("git clone https://github.com/r0oth3x49/ghauri.git")
    RunCommand("cd ghauri")
    RunCommand("python3 -m pip install --upgrade -r requirements.txt")
    RunCommand("python3 setup.py install")

InstallGo("github.com/tomnomnom/qsreplace@latest")
InstallGo("github.com/projectdiscovery/katana/cmd/katana@latest")
InstallGo("github.com/tomnomnom/gf@latest")
InstallGo("github.com/hahwul/dalfox/v2@latest")
InstallGhauri()