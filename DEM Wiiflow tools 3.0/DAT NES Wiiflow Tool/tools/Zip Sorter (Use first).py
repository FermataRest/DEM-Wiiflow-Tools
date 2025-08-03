import os
import shutil

# Define folder names for the categories
japan_folder = "Japan"
unl_folder = "unl"
prototype_folder = "Prototype"
sachen_folder = "Sachen"
vc_folder = "Virtual Console"
vs_folder = "VS"
underscore_folder = "Underscore"
hack_folder = "Hack"
europe_folder = "Europe"

# Create directories if they don't exist
os.makedirs(japan_folder, exist_ok=True)
os.makedirs(unl_folder, exist_ok=True)
os.makedirs(prototype_folder, exist_ok=True)
os.makedirs(sachen_folder, exist_ok=True)
os.makedirs(vc_folder, exist_ok=True)
os.makedirs(vs_folder, exist_ok=True)
os.makedirs(underscore_folder, exist_ok=True)
os.makedirs(hack_folder, exist_ok=True)
os.makedirs(europe_folder, exist_ok=True)

# Get a list of all .zip files in the current directory
zip_files = [file for file in os.listdir() if file.endswith(".zip")]

# Loop through each file and move it to the appropriate folder
for zip_file in zip_files:
    lower_name = zip_file.lower()  # Convert to lowercase for consistent checking
    if "(j)" in lower_name or "(jap)" in lower_name or "(japan)" in lower_name:
        shutil.move(zip_file, os.path.join(japan_folder, zip_file))
    elif "(e)" in lower_name or "(eu)" in lower_name or "(europe)" in lower_name:
        shutil.move(zip_file, os.path.join(europe_folder, zip_file))
    elif "(unl)" in lower_name:
        shutil.move(zip_file, os.path.join(unl_folder, zip_file))
    elif "(prototype)" in lower_name or "(proto)" in lower_name:
        shutil.move(zip_file, os.path.join(prototype_folder, zip_file))
    elif "(sachen)" in lower_name:
        shutil.move(zip_file, os.path.join(sachen_folder, zip_file))
    elif "(virtual console)" in lower_name:
        shutil.move(zip_file, os.path.join(vc_folder, zip_file))
    elif "(vs)" in lower_name:
        shutil.move(zip_file, os.path.join(vs_folder, zip_file))
    elif "(hack)" in lower_name:
        shutil.move(zip_file, os.path.join(hack_folder, zip_file))
    elif "_" in zip_file:
        shutil.move(zip_file, os.path.join(underscore_folder, zip_file))

print("Files sorted into respective folders!")
