import os
import subprocess
import requests

def check_for_update(repo_url, local_path):
    try:
        response = requests.get(f"{repo_url}/releases/latest")
        response.raise_for_status()
        latest_version = response.url.split("/")[-1]
        local_version_path = os.path.join(local_path, "version.txt")

        if not os.path.exists(local_version_path):
            with open(local_version_path, "w") as f:
                f.write("0.0.0")

        local_version = open(local_version_path).read().strip()

        if latest_version != local_version:
            print("Updating...")
            download_url = f"{repo_url}/releases/latest/download/my_script.py"
            update_script = requests.get(download_url)
            
            with open(os.path.join(local_path, "my_script.py"), "wb") as f:
                f.write(update_script.content)

            with open(local_version_path, "w") as f:
                f.write(latest_version)

            print("Update complete.")
            return True
        else:
            print("Already up to date.")
            return False
    except Exception as e:
        print(f"Error checking for update: {e}")
        return False

def update_and_restart(repo_url, local_path):
    if check_for_update(repo_url, local_path):
        print("Restarting...")
        subprocess.Popen(["python", os.path.join(local_path, "my_script.py")])
        exit()

def main():
    print("Hello, this is my_script!")

if __name__ == "__main__":
    main()
