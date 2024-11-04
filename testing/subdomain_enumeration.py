import subprocess

def Run(domain, output_file):
    try:
        # Run the amass command to enumerate subdomains
        result = subprocess.run(
            ["amass", "enum", "-d", domain],
            capture_output=True,
            text=True
        )

        # Check if there was an error
        if result.returncode != 0:
            print(f"Error running amass: {result.stderr}")
            return

        # Write output to the specified file
        with open(output_file, "w") as file:
            file.write(result.stdout)

        print(f"Subdomain enumeration for {domain} is complete. Results saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")


def Run(target_domain, wordlist_file, output_file, threads=10):
    """Run gobuster to brute-force subdomains and save results."""
    try:
        # Run the gobuster command
        with open(output_file, "w") as file:
            result = subprocess.run(
                ["gobuster", "dns", "-d", target_domain, "-t", str(threads), "-w", wordlist_file],
                stdout=file,
                stderr=subprocess.PIPE,
                text=True
            )

        # Check for errors
        if result.returncode != 0:
            print(f"Error running gobuster: {result.stderr}")
            return False

        print(f"Brute-forcing with gobuster completed. Results saved to {output_file}")
        return True

    except Exception as e:
        print(f"An error occurred with gobuster brute-force: {e}")
        return False

def RunAmass(domain, wordlist_file, output_file):
    """Run Amass to enumerate subdomains using brute-forcing with a wordlist."""
    try:
        # Run the Amass command with brute force and wordlist
        result = subprocess.run(
            ["amass", "enum", "-d", domain, "-brute", "-w", wordlist_file],
            capture_output=True,
            text=True
        )

        # Check for errors
        if result.returncode != 0:
            print(f"Error running amass: {result.stderr}")
            return False

        # Write Amass output to the specified file
        with open(output_file, "w") as file:
            file.write(result.stdout)

        print(f"Amass subdomain enumeration with brute-forcing for {domain} is complete. Results saved to {output_file}")
        return True

    except Exception as e:
        print(f"An error occurred with Amass: {e}")
        return False
