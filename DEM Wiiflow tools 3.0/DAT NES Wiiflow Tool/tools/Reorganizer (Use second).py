import os
import shutil

# Folders to include in the search
folders_to_include = ["Europe", "Japan"]

# Get the directory where the script is located
current_directory = os.path.dirname(os.path.abspath(__file__))

# Get a list of all .zip files in the current directory (excluding folders)
current_dir_zip_files = [file for file in os.listdir(current_directory) if file.endswith(".zip") and os.path.isfile(os.path.join(current_directory, file))]

# Function to normalize the filenames by removing anything in parentheses and trimming whitespace
def normalize_filename(name):
    return name.split('(')[0].strip().lower()

# Create a set of normalized base names of the current directory zip files
current_zip_base_names = set(normalize_filename(zip_file) for zip_file in current_dir_zip_files)

# Loop through each specified folder
for folder in folders_to_include:
    folder_path = os.path.join(current_directory, folder)
    if os.path.exists(folder_path):
        # Get all .zip files in the folder
        folder_zip_files = [file for file in os.listdir(folder_path) if file.endswith(".zip")]

        for zip_file in folder_zip_files:
            # Normalize the name of the file
            normalized_name = normalize_filename(zip_file)

            # Check if this normalized name exists in the current directory zip base names
            if normalized_name not in current_zip_base_names:
                # Move the file to the current directory
                shutil.move(os.path.join(folder_path, zip_file), os.path.join(current_directory, zip_file))
                print(f"Moved {zip_file} from {folder} to current directory.")
            else:
                print(f"{zip_file} in {folder} matches a file in the current directory, not moving.")

print("Script completed!")
