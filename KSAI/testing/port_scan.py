from testing.require import *

def Run(ip, port_range="--top-ports 5", output_file="nmap_results.txt"):
    command = f"nmap -sC -sV -sT {port_range} {ip} -Pn | tee {output_file}"
    """
    -sC runs the default scripts
    -sV is for discovering service versions
    -Pn for disabling host discovery

    -sT le TCP connect scan use गर्छ
    -sU ले UDP scan गर्छ 
    -sS ले TCP SYN Scan गर्छ
    """
    RunCommand(command, "Nmap succeeded", "Nmap Failed"); 

def RunDaiKoWriteUpBata(ip):
    command = f"nmap -sC -sV {ip} -p"