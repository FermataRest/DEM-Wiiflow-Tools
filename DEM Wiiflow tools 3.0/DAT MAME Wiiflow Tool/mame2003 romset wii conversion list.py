import os
import shutil

def read_zip_files(folder_path):
    zip_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.zip'):
                zip_files.append(os.path.join(root, file))
    return zip_files

def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        contents = file.read().splitlines()
    return contents

def prompt_for_folder():
    print("Please drag and drop your Mame2003 romset folder here to pick out the games that actually work on the Wii and press Enter:")
    
    folder_path = input().strip('"')
    
    if os.path.isdir(folder_path):
        print("Reading .zip files in the selected folder and subfolders...")
        zip_files = read_zip_files(folder_path)
        if zip_files:
            print("Found the following .zip files:")
            for file in zip_files:
                print(file)
        else:
            print("No .zip files found in the selected folder.")
    else:
        print("No valid folder path entered or folder does not exist.")
        return

    # Ask if the user wants to reference a .txt file
    reference_txt = input("Would you like to reference a .txt file that has all the Wii/Mame information? (yes/no): ").strip().lower()
    if reference_txt == 'yes':
        print('Please drag and drop the "mame2003 working wii list.txt" into this script and press Enter:')
        txt_file_path = input().strip('"')
        
        if os.path.isfile(txt_file_path) and txt_file_path.endswith('.txt'):
            print("Reading the contents of the .txt file...")
            txt_contents = read_txt_file(txt_file_path)
            print("Contents of the .txt file:")
            for line in txt_contents:
                print(line)

            # Perform exact match
            matched_files = []
            for zip_file in zip_files:
                zip_file_name = os.path.basename(zip_file)
                if zip_file_name in txt_contents:
                    matched_files.append(zip_file)

            if matched_files:
                print("Matched the following .zip files:")
                for file in matched_files:
                    print(file)

                # Define the destination directory
                destination_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mame games")
                
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)
                    print(f"Created the directory {destination_dir}")

                # Copy matched files to the mame games directory
                for file in matched_files:
                    shutil.copy(file, destination_dir)
                print(f"Copied matched .zip files to {destination_dir}")
            else:
                print("No matching .zip files found.")
        else:
            print("No valid .txt file entered or file does not exist.")
    
    # Final prompt with new message three lines lower
    print("\n\n\nThanks for using this Below Average conversion list! Your games have been matched and placed into the 'mame games' folder. Happy Modding!")
    
    # Keep the window open until a key is pressed
    input("Press Enter to exit...")

if __name__ == "__main__":
    prompt_for_folder()
