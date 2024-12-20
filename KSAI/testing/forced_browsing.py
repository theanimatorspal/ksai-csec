from testing.require import *
import subprocess
import re
import os

def run_command(command, file):
    """Run a shell command and append output to a file."""
    with open(file, "a") as output_file:
        process = subprocess.Popen(command, shell=True, stdout=output_file, stderr=subprocess.STDOUT)
        process.communicate()

def Run(domain, filepath, wordlist):
    # Clear the output file first
    with open(filepath, "w") as f:
        f.write("")

    print(f"Running forced browsing tools on domain: {domain}\nUsing wordlist: {wordlist}\nSaving output to: {filepath}")

    # List of commands for each tool with the wordlist
    tools = [
        #f"ffuf -w {wordlist} -u {domain}/FUZZ -o {filepath}_ffuf.json -of json -r -rate 5",  # ffuf (JSON format)
        #f"gobuster dir -u {domain} -w {wordlist} -o {filepath}_gobuster.txt",      # gobuster (TXT format)
        rf"dirsearch -u {domain} -w {wordlist} -e all -o {filepath}"  # dirsearch (TXT format)
    ]
    
    # Run each tool command
    for command in tools:
        print(f"Running command: {command}")
        run_command(command, filepath)
    
    print("Forced browsing scan completed. Results saved.")


def RunGobuster(domain, output_file, wordlist="/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt", exclude="403,301,302"):
    command = ["gobuster", "dir", "-u", f"{domain}", "-w", wordlist, "-o", output_file, "-k", "-b", exclude]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print("Gobuster scan failed.")
            print(result.stderr)
            return
        
        print(f"File paths saved to {output_file}")
    
    except FileNotFoundError:
        print("Error: Gobuster is not installed.")
    except Exception as e:
        print(f"An error occurred: {e}")


def RunFeroxbuster(domain, output_file, wordlist="/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt", exclude="403,404", auto_tune=True, thorough=False):
    command = f"feroxbuster -u {domain} -w {wordlist} -o {output_file} --filter-status {exclude}"
    if auto_tune:
        command += " --auto-tune"
    if thorough:
        command += " --thorough"

    RunCommand(command, f"Scan completed successfully. Results saved to {output_file}", "Feroxbuster scan failed.")

def RunFeroxbusterFromFile(file_path, output_dir, wordlist="/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt", exclude="403,404", auto_tune=True, thorough=False, rate_limit=50):
    try:
        with open(file_path, "r") as file:
            domains = [line.strip() for line in file if line.strip()]
        
        for domain in domains:
            sanitized_domain = re.sub(r"[^\w.-]", "_", domain)  # Replace non-alphanumeric/symbols with _
            output_file = f"{output_dir}/{sanitized_domain}.txt"
            RunFeroxbuster(domain, output_file, wordlist, exclude, auto_tune, thorough, rate_limit)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
