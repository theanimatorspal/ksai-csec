from testing.require import *

def Run(ip, port_range="--top-ports 100", output_file="nmap_results.txt"):
    command = f"nmap -v -sT {port_range} {ip} | tee {output_file}"
    RunCommand(command, "Nmap succeeded", "Nmap Failed"); 