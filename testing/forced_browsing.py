import subprocess
import sys

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
        f"ffuf -w {wordlist} -u {domain}/FUZZ -o {filepath}_ffuf.json -of json",  # ffuf (JSON format)
        f"gobuster dir -u {domain} -w {wordlist} -o {filepath}_gobuster.txt",      # gobuster (TXT format)
        f"dirsearch -u {domain} -w {wordlist} -e all -o {filepath}_dirsearch.txt"  # dirsearch (TXT format)
    ]
    
    # Run each tool command
    for command in tools:
        print(f"Running command: {command}")
        run_command(command, filepath)
    
    print("Forced browsing scan completed. Results saved.")