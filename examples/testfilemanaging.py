import os
from time import strftime, strptime

# Specify the subfolder name
subfolder = "reports"

# Create the subfolder if it doesn't exist
if not os.path.exists(subfolder):
    os.makedirs(subfolder)

# Get the latest file in the subfolder
all_files = os.listdir(subfolder)
all_files.sort(reverse=True)
latest_file = None

for file in all_files:
    try:
        latest_file = strptime(file.split('.')[0], '%Y_%m_%d_%I_%M%p')
        break
    except ValueError:
        continue

if latest_file:
    latest_file_path = os.path.join(subfolder, f"{strftime('%Y_%m_%d_%I_%M%p', latest_file)}.txt")
    print(f"Reading contents of the latest file: {latest_file_path}")

    # Read and print the contents of the latest file
    with open(latest_file_path, 'r') as f:
        file_contents = f.read()
        print(file_contents)
    
    # If no relevant file is found, create the first file
    filedate = strftime('%Y_%m_%d_%I_%M%p')
    first_file_path = os.path.join(subfolder, filedate + '.txt')



    with open(first_file_path, 'a') as f:
        # Write some sample content to the first file
        f.write("Hello, this is the first file.")
else:
    # If no relevant file is found, create the first file
    filedate = strftime('%Y_%m_%d_%I_%M%p')
    first_file_path = os.path.join(subfolder, filedate + '.txt')
    print(f"No relevant file to read. Creating the first file: {first_file_path}")

    with open(first_file_path, 'a') as f:
        # Write some sample content to the first file
        f.write("Hello, this is the first file.")
