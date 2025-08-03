import os
import shutil

def package_bin_and_cue():
    # Get the current directory
    current_dir = os.getcwd()
    
    # Create a list of all .bin and .cue files in the directory
    bin_files = [f for f in os.listdir(current_dir) if f.endswith('.bin')]
    cue_files = [f for f in os.listdir(current_dir) if f.endswith('.cue')]
    
    # Find matching .bin and .cue files
    for bin_file in bin_files:
        base_name = os.path.splitext(bin_file)[0]
        matching_cue = f"{base_name}.cue"
        
        if matching_cue in cue_files:
            # Create a new folder with the matching name
            new_folder = os.path.join(current_dir, base_name)
            os.makedirs(new_folder, exist_ok=True)
            
            # Move the .bin and .cue files into the new folder
            shutil.move(os.path.join(current_dir, bin_file), os.path.join(new_folder, bin_file))
            shutil.move(os.path.join(current_dir, matching_cue), os.path.join(new_folder, matching_cue))
            
            print(f"Packaged '{bin_file}' and '{matching_cue}' into '{new_folder}'")
        else:
            print(f"No matching .cue file found for '{bin_file}'")
            
    print("All Done! I did my best to package the files.")

if __name__ == "__main__":
    package_bin_and_cue()
