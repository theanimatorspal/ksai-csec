
import subprocess

def RunCommand(command, success_message, failure_message):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.returncode != 0:
            print(failure_message)
            print(result.stderr)
        else:
            print(success_message)
    except Exception as e:
        print(f"An error occurred: {e}")