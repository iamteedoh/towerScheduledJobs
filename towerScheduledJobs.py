import requests
from getpass import getpass
import json
import os
import time
import shutil
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # Suppress SSL warnings

# Fetch user input
tower_host = input("Enter your Ansible Tower host: ")
tower_username = input("Enter your username (admin access required): ")
tower_password = getpass("Enter your password: ")

# Prepare requests session
s = requests.Session()
s.auth = (tower_username, tower_password)

def get_jobs(enabled=None, disabled=None):
    url = f"https://{tower_host}/api/v2/schedules/"
    if enabled:
        params = {"enabled": "true"}
    elif disabled:
        params = {"enabled": "false"}
    else:
        params = {}
    
    jobs = []

    while url:
        response = s.get(url, params=params, verify=False)
        data = response.json()
        jobs.extend([{"id": result["id"], "name": result["name"]} for result in data["results"]])
        url = data["next"]
        if data["next"]:
            url = f"https://{tower_host}" + data["next"]
        else:
            url = None

    return jobs

def enable_jobs():
    files = [f for f in os.listdir() if f.startswith("enabled_jobs.json")]
    
    if not files:
        print("No files starting with 'enabled_jobs.json' found in the current directory.")
        return
    
    job_ids = []
    print("\n1. Choose a single file\n2. Use all files")
    choice = input("Choose an option: ")
    
    if choice == "1":
        for index, file in enumerate(files, 1):
            print(f"{index}. {file}")
        file_choice = input("Select a file from the list: ")
        with open(files[int(file_choice)-1], "r") as f:
            job_ids = json.load(f)
    elif choice == "2":
        for file in files:
            with open(file, "r") as f:
                job_ids.extend(json.load(f))
                
    for job_id in job_ids:
        url = f"https://{tower_host}/api/v2/schedules/{job_id}/"
        data = {"enabled": True}
        s.patch(url, json=data, verify=False)
        
    print(f"\nEnabled {len(job_ids)} job(s).")

def disable_jobs(job_ids):
    if not job_ids:
        print("No enabled jobs found to disable.")
        return
    for job_id in job_ids:
        url = f"https://{tower_host}/api/v2/schedules/{job_id}/"
        data = {"enabled": False}
        s.patch(url, json=data, verify=False)
    backup_file("enabled_jobs.json")
    with open("enabled_jobs.json", "w") as f:
        json.dump(job_ids, f)
    print(f"\nDisabled {len(job_ids)} job(s).")

def display_jobs(jobs, output_option):
    print() # Newline for clarity
    if output_option in ["1", "3"]:
        for job in jobs:
            print(f"ID: {job['id']}, Name: {job['name']}")
    print(f"\nTotal jobs found: {len(jobs)}")
    if output_option in ["2", "3"]:
        filename = "jobs.json"
        with open(filename, "w") as f:
            json.dump(jobs, f, indent=4)
        print(f"\nJobs written to file: {os.path.abspath(filename)}")

def backup_file(filename):
    if os.path.exists(filename):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        backup_filename = f"{filename}.{timestamp}.bak"
        shutil.copyfile(filename, backup_filename)
        print(f"\nBackup of {filename} created: {backup_filename}")

while True:
    print("\n1. Enable jobs\n2. Disable jobs\n3. List all jobs\n4. List only enabled jobs\n5. List only disabled jobs\n6. Exit (X or x)")
    action = input("Choose an action: ")

    if action.lower() in ["x", "6"]:
        break
    elif action in ["3", "4", "5"]:
        if action == "5":
            jobs = get_jobs(disabled=True)
        else:
            jobs = get_jobs(enabled=(action=="4"))
        print("\n1. Display jobs on screen\n2. Write jobs to a file\n3. Do both")
        output_option = input("Choose an output option: ")
        display_jobs(jobs, output_option)
    elif action == "1":
        enable_jobs()
    elif action == "2":
        job_ids = [job["id"] for job in get_jobs(enabled=True)]
        disable_jobs(job_ids)

