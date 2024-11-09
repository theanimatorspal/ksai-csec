import subprocess
import re

def Run(ip, port_range="--top-ports 100", output_file="nmap_results.txt"):
    command = f"nmap -v -sT {port_range} {ip}"
    
    try:
        print(command)
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.returncode != 0:
            print("Nmap scan failed.")
            print(result.stderr)
            return
        
        with open(output_file, "w") as file:
            file.write(result.stdout)

        print(f"Scan results saved to {output_file}")

    except FileNotFoundError:
        print("Error: Nmap is not installed.")
    except Exception as e:
        print(f"An error occurred: {e}")
