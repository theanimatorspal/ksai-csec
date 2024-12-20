import subprocess
import os

# Function to run a command and return the output
def run_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)

# Function to perform network scanning using nmap
def network_scan(target):
    print(f"[*] Running network scan on {target}")
    scan_command = f"nmap -sP {target}"
    scan_results = run_command(scan_command)
    print(scan_results)
    return scan_results

# Function to test firewall using nmap (basic port scanning)
def firewall_test(target_ip):
    print(f"[*] Running firewall test on {target_ip}")
    firewall_command = f"nmap -p 1-1000 {target_ip}"
    firewall_results = run_command(firewall_command)
    print(firewall_results)
    return firewall_results

# Function to perform ping test to check if a host is reachable
def ping_test(target_ip):
    print(f"[*] Pinging {target_ip}")
    ping_command = f"ping -c 4 {target_ip}"
    ping_results = run_command(ping_command)
    print(ping_results)
    return ping_results

# Function to perform traceroute to check network path
def traceroute_test(target_ip):
    print(f"[*] Running traceroute to {target_ip}")
    traceroute_command = f"traceroute {target_ip}"
    traceroute_results = run_command(traceroute_command)
    print(traceroute_results)
    return traceroute_results

# Function to run vulnerability scan using nmap
def vulnerability_scan(target_ip):
    print(f"[*] Running vulnerability scan on {target_ip}")
    vuln_command = f"nmap --script vuln {target_ip}"
    vuln_results = run_command(vuln_command)
    print(vuln_results)
    return vuln_results

# Main function to run all tests
def run_all_tests(target_ip):
    print(f"[*] Running all tests for {target_ip}")
    
    # Run network scan
    network_scan(target_ip)
    
    # Run ping test
    ping_test(target_ip)
    
    # Run firewall test
    firewall_test(target_ip)
    
    # Run traceroute test
    traceroute_test(target_ip)
    
    # Run vulnerability scan
    vulnerability_scan(target_ip)

if __name__ == "__main__":
    target_ip = input("Enter the target IP or network range (e.g., 192.168.1.1 or 192.168.1.0/24): ")
    run_all_tests(target_ip)
