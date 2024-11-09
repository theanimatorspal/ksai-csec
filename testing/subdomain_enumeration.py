import subprocess
import os

def RunSubfinder(domain, output_file):
    command = ["subfinder", "-d", domain, "-o", output_file]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print("Sublist3r scan failed.")
            print(result.stderr)
            return
        
        print(f"Subdomains saved to {output_file}")
    
    except FileNotFoundError:
        print("Error: Sublist3r is not installed.")
    except Exception as e:
        print(f"An error occurred: {e}")

def RunFindAlive(domain_file, output_file, ports=None):
    if not ports:
        ports = "21,22,23,25,53,80,110,135,139,143,443,445,587,993,995,1433,1521,3306,3389,5432,5900,6379,8080,8443"
    command = f"cat {domain_file} | httpx-toolkit -l {domain_file} -ports {ports} -mc 200,403,400,500 -threads 200 > {output_file}"
    try:
        result = subprocess.run(command, text=True, shell=True)
        if result.returncode != 0:
            print("Sublist3r scan failed.")
            print(result.stderr)
            return
        
        print(f"Subdomains saved to {output_file}")
    
    except Exception as e:
        print(f"An error occurred: {e}")