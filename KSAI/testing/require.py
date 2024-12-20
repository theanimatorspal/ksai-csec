import subprocess

def RunCommand(command, success_message, failure_message):
    try:
        process = subprocess.Popen(command, shell=True)
        process.communicate()  # Waits for the process to finish

        # Check the exit code
        if process.returncode != 0:
            print(failure_message)
        else:
            print(success_message)

    except Exception as e:
        print(f"An error occurred: {e}")

RunCommand("ping -c 4 google.com", "Command succeeded!", "Command failed!")
