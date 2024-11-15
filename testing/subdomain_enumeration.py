from testing.require import *

def RunSubfinder(domain, output_file):
    command = f"subfinder -d {domain} -o {output_file}"
    RunCommand(command, "Subfinder Successful", "Subfinder Failed");

def RunFindAlive(domain_file, output_file, ports=None):
    if not ports:
        ports = "21,22,23,25,53,80,110,135,139,143,443,445,587,993,995,1433,1521,3306,3389,5432,5900,6379,8080,8443"
    command = f"cat {domain_file} | httpx-toolkit -l {domain_file} -ports {ports} -mc 200,403,400,500 -threads 200 > {output_file}"
    RunCommand(command, "Alive Domains Succeeded", "Alive Domains Failed")