from subprocess import run
from time import sleep

# Path and name to the script you are trying to start
file_path = "main2.py"

restart_timer = 2
def start_script():
    try:
        run("python "+file_path, check=True)
    except:
        # restart crashed script
        handle_crash()

def handle_crash():
    sleep(restart_timer)  # Restarts the script after 2 seconds
    start_script()

start_script()
