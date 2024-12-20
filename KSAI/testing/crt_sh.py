from testing.require import *

def Run(search_param, file_name):
    search_param_encoded = search_param.replace(' ', '+')
    command = f"wget 'https://crt.sh/?q={search_param_encoded}&output=json' -O {file_name};" 
    """
    - `wget` fetches the data from crt.sh using the search parameter.
    - `-O crtsh.txt` saves the output to a temporary file.
    - `jq` processes the JSON output.
    - `grep common_name` filters lines containing the common name field.
    - `cut -d':' -f2 | cut -d'"' -f2` extracts the domain names.
    - `sort -u` removes duplicates.
    - `tee -a {output_file}` appends unique domains to the output file.
    """
    RunCommand(command, "Domain extraction succeeded", "Domain extraction failed")
