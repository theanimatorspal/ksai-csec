import subprocess
import sys
import re

def default_port_range():
    # Define a default list of popular ports as a string
    return "21,22,23,25,53,80,110,135,139,143,443,445,587,993,995,1433,1521,3306,3389,5432,5900,6379,8080,8443"

def Run(ip, port_range, output_file):
    # Construct the Nmap command
    command = f"nmap -p {port_range} {ip}"
    
    try:
        print(f"Running command: {command}")
        
        # Run the Nmap command and capture the output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Check if the command was successful
        if result.returncode != 0:
            print("Nmap scan failed.")
            print(result.stderr)
            return
        
        # Write the results to the specified output file
        with open(output_file, "w") as file:
            file.write(result.stdout)
        
        print(f"\nScan results saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")