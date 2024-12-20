# RUN THIS WITH SUDO
import re
from testing.require import *

packages = [
    "python3-pip",
    "python3-setuptools",
    "porch_pirate",
    "massdns",
    "gitleaks"
    "crlfsuite",
    "dnsx",
    "dnsgen",
    "goaltdns",
    "smbmap",
    "amass",
     "gobuster",
     "dirsearch",
     "httpx-toolkit",
     "sublist3r",
     "exiftool",
     "puredns",
     "feroxbuster",
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

def InstallParamSpider():
    RunCommand("git clone https://github.com/devanshbatham/paramspider")
    RunCommand("cd paramspider")
    RunCommand("pip install .")

# InstallGo("github.com/tomnomnom/qsreplace@latest")
# InstallGo("github.com/projectdiscovery/katana/cmd/katana@latest")
# InstallGo("github.com/tomnomnom/gf@latest")
# InstallGo("github.com/hahwul/dalfox/v2@latest")
# InstallGo("github.com/d3mondev/puredns/v2@latest")
# InstallGo("github.com/projectdiscovery/mapcidr/cmd/mapcidr@latest")
# InstallGhauri()