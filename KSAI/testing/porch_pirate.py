from testing.require import *

def Run(url, file_name):
    command = f"porch-pirate -s {url} --dump | tee {file_name}"
    RunCommand(command, "Domain extraction succeeded", "Domain extraction failed")
