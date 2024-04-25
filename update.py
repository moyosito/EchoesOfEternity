import requests
import os

def read_file_to_string(file_path):
    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
            return file_contents
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except Exception as e:
        print("Error reading file:", e)
        return None

def get_remote_version(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.strip()
        else:
            print("Failed to fetch version information:", response.status_code)
            return None
    except Exception as e:
        print("Error fetching version information:", e)
        return None

# Fetching remote version
remote_version = get_remote_version("https://raw.githubusercontent.com/moyosito/EchoesOfEternity/main/version")

# Checking for update
if remote_version is not None:
    remote_version = float(remote_version)
    current_version = read_file_to_string("version.txt")
    if current_version is not None:
        current_version = float(current_version)
        if current_version <= remote_version:
            print("UPDATE!!!")
            os.remove("main.py")
            os.system("curl -o main2.py https://raw.githubusercontent.com/moyosito/EchoesOfEternity/main/main.py")
            os.rename("main2.py", "main.py")  # Rename the downloaded file to main.py
            print("Updated 'main.py'")
            # Change version.txt to the new version
            with open("version.txt", "w") as version_file:
                version_file.write(str(remote_version))
            print("Version updated to:", remote_version)
        else:
            print("Up to date! :)")
    else:
        print("Failed to fetch current version from file.")
else:
    print("Failed to fetch remote version information.")
