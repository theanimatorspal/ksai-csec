import subprocess

def Run(input_file, output_file):
    """
    Finds root domains for a list of ASN numbers using Amass.

    :param input_file: Path to the input file containing ASN numbers.
    :param output_file: Path to save the output root domains.
    """
    # Open the input and output files
    with open(input_file, 'r') as file:
        asn_numbers = [line.strip() for line in file.readlines()]

    with open(output_file, 'w') as outfile:
        # Iterate through each ASN number and run Amass command
        for asn in asn_numbers:
            try:
                # Run amass command and capture output
                result = subprocess.run(
                    ['amass', 'intel', '-asn', asn],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Write results to output file
                outfile.write(f"ASN {asn}:\n")
                outfile.write(result.stdout + "\n")
                outfile.write("-" * 60 + "\n")
                
                print(f"Results for ASN {asn} added to output file.")
                
            except Exception as e:
                print(f"An error occurred with ASN {asn}: {e}")
