import os
import re
from difflib import get_close_matches
import shutil
import time

# Define the folder paths
ps1_cover_art_folder = "ps1 cover art"
ps1_games_folder = "ps1 games"
ps1_plain_text_names_folder = "ps1 plain text names"
renamed_cover_art_folder = "renamed cover art"
unmatched_games_folder = "unmatched games"

# Ensure the renamed cover art and unmatched games folders exist
if not os.path.exists(renamed_cover_art_folder):
    os.makedirs(renamed_cover_art_folder)
if not os.path.exists(unmatched_games_folder):
    os.makedirs(unmatched_games_folder)

# Placeholder for specific rename function
def special_names():
    renamed_files = []
    try:
        specific_renames = {
            "EA Sports Supercross 2000 (USA)": "Supercross 2000",
            "Final Fantasy Anthology - Final Fantasy V (USA)": "Final Fantasy Anthology",
            "Final Fantasy Anthology - Final Fantasy VI (USA)": "Final Fantasy Anthology",
            "Final Fantasy Chronicles - Final Fantasy IV (USA)": "Final Fantasy Chronicles",
            "G. Darius + Devil Dice + Brunswick Circuit Pro Bowling (USA)": "Brunswick Circuit Pro Bowling 2",
            "Jet Moto 2 - Championship Edition (USA)": "Jet Moto 2",
            "Lost World, The - Jurassic Park - Special Edition (USA)": "Lost World, The - Jurassic Park",
            "Nickelodeon Rugrats - Studio Tour (USA)": "Rugrats - Studio Tour",
            "Peter Pan in Disney's Return to Never Land (USA)": "Disney's Peter Pan Return to Never Land",
            "Bubsy 3D - Furbitten Planet (USA)": "Bubsy 3D",
            "Pac-Man World - 20th Anniversary (USA)": "Pac-Man World",
            "Rival Schools - United by Fate (USA) (Disc 1)": "Rival Schools (Disc 1)",
            "Rival Schools - United by Fate (USA) (Disc 2)": "Rival Schools (Disc 2)",
            "Space Shot (USA)": "Shooter Space Shot",
            "Wing Commander III - Heart of the Tiger (USA) (Disc 1)": "Wing Commander III (Disc 1)",
            "Wing Commander III - Heart of the Tiger (USA) (Disc 2)": "Wing Commander III (Disc 2)",
            "Wing Commander III - Heart of the Tiger (USA) (Disc 3)": "Wing Commander III (Disc 3)",
            "Wing Commander III - Heart of the Tiger (USA) (Disc 4)": "Wing Commander III (Disc 4)",
            # New entries
            "Arcade's Greatest Hits - The Atari Collection 2 (USA)": "Arcade's Greatest Hits - The Atari Collection 2",
            "Caesars Palace II (USA)": "Caesars Palace II",
            "Final Fantasy IX (USA) (Disc 1)": "Final Fantasy IX (Disc 1)",
            "Final Fantasy IX (USA) (Disc 2)": "Final Fantasy IX (Disc 2)",
            "Final Fantasy IX (USA) (Disc 3)": "Final Fantasy IX (Disc 3)",
            "Final Fantasy IX (USA) (Disc 4)": "Final Fantasy IX (Disc 4)",
            "Final Fantasy VIII (USA) (Disc 1)": "Final Fantasy VII (Disc 1)",
            "Final Fantasy VIII (USA) (Disc 2)": "Final Fantasy VII (Disc 2)",
            "Final Fantasy VIII (USA) (Disc 3)": "Final Fantasy VII (Disc 3)",
            "Final Fantasy VIII (USA) (Disc 4)": "Final Fantasy VII (Disc 4)",
            "Nightmare Creatures II (USA)": "Nightmare Creatures II"
        }
        for file in os.listdir(ps1_games_folder):
            base_name, ext = os.path.splitext(file)
            disc_info = re.search(r"\(Disc \d+\)", base_name)
            base_name_with_disc = base_name  # Include the disc info in the base name for exact matching
            if base_name_with_disc in specific_renames:
                new_base_name = specific_renames[base_name_with_disc]
                old_folder_path = os.path.join(ps1_games_folder, file)
                new_folder_path = os.path.join(ps1_games_folder, new_base_name)
                if os.path.exists(new_folder_path):
                    print(f"Skipping renaming folder {file} -> {new_base_name}: Folder already exists.")
                else:
                    os.rename(old_folder_path, new_folder_path)
                    print(f"Renamed folder: {file} -> {new_base_name}")
                # Now handle renaming the .bin and .cue files inside the renamed folder
                for inner_file in os.listdir(new_folder_path):
                    inner_base_name, inner_ext = os.path.splitext(inner_file)
                    if inner_ext in ['.bin', '.cue']:  # Only process .bin and .cue files
                        new_inner_base_name = new_base_name
                        new_inner_file_name = new_inner_base_name + inner_ext
                        new_inner_file_path = os.path.join(new_folder_path, new_inner_file_name)
                        if os.path.exists(new_inner_file_path):
                            print(f"Skipping {inner_file} -> {new_inner_file_name}: File already exists.")
                        else:
                            old_inner_file_path = os.path.join(new_folder_path, inner_file)
                            os.rename(old_inner_file_path, new_inner_file_path)
                            print(f"Renamed: {inner_file} -> {new_inner_file_name}")
                renamed_files.append(new_base_name)
    except Exception as e:
        print(f"Error in special_names: {e}")
    return renamed_files

# Run special renames first and collect the renamed base names
renamed_files = special_names()

# Initial prompt
user_input = input("Thanks for using this PS1 Wiiflow tool! Do you want to see what games I can find for you? (yes/no): ").strip().lower()
if user_input == "yes":
    bin_files = {}
    cue_files = {}
    png_files = []
    try:
        # Walk through the ps1 games folder and its subfolders
        for root, dirs, files in os.walk(ps1_games_folder):
            for file in files:
                base_name, ext = os.path.splitext(file)
                if file.endswith('.bin') and base_name not in renamed_files:
                    bin_files[base_name] = os.path.join(root, file)
                elif file.endswith('.cue') and base_name not in renamed_files:
                    cue_files[base_name] = os.path.join(root, file)

        # Display matching pairs with spacing
        matches_found = False
        for base_name in bin_files:
            if base_name in cue_files:
                matches_found = True
                print(f"Match found: {base_name}.cue and {base_name}.bin")
                print(f" - {cue_files[base_name]}")
                print(f" - {bin_files[base_name]}\n\n")

        if matches_found:
            remove_region = input("These are the games that I've found! Do you want to remove the '(Region)' info from the title of your games? (yes/no): ").strip().lower()
            if remove_region == "yes":
                updated_bin_files = {}
                updated_cue_files = {}
                for base_name in list(bin_files.keys()):
                    disc_info = re.search(r"\(Disc \d+\)", base_name)
                    new_base_name = re.sub(r"\((?!Disc \d+)[^\)]+\)", "", base_name).strip()
                    new_base_name = re.sub(r"\[\[.*?\]\]", "", new_base_name).strip()
                    if disc_info:
                        new_base_name = new_base_name + " " + disc_info.group()
                    new_base_name = re.sub(r"\s+", " ", new_base_name).strip()
                    new_bin_path = os.path.join(os.path.dirname(bin_files[base_name]), new_base_name + ".bin")
                    new_cue_path = os.path.join(os.path.dirname(cue_files[base_name]), new_base_name + ".cue")
                    if new_base_name != base_name:
                        os.rename(bin_files[base_name], new_bin_path)
                        os.rename(cue_files[base_name], new_cue_path)
                        updated_bin_files[new_base_name] = new_bin_path
                        updated_cue_files[new_base_name] = new_cue_path
                        print(f"Renamed: {base_name}.bin and {base_name}.cue to {new_base_name}.bin and {new_base_name}.cue")
                    else:
                        print(f"File name already matches: {base_name}.bin and {base_name}.cue")
                        updated_bin_files[base_name] = bin_files[base_name]
                        updated_cue_files[base_name] = cue_files[base_name]
                bin_files = updated_bin_files
                cue_files = updated_cue_files

            continue_renaming = input("\nGreat! Now that this is done, let's rename all of your game titles so they are good for Wiiflow. Do you want to continue? (yes/no): ").strip().lower()
            if continue_renaming == "yes":
                # Start matching process
                for txt_file in os.listdir(ps1_plain_text_names_folder):
                    if txt_file.endswith('.txt'):
                        txt_base_name = os.path.splitext(txt_file)[0]
                        for base_name in list(bin_files.keys()):
                            clean_base_name = re.sub(r"\(Disc \d+\)", "", base_name).strip()
                            clean_base_name = re.sub(r"\((?!Disc \d+)[^\)]+\)", "", clean_base_name).strip()
                            clean_base_name = re.sub(r"\[\[.*?\]\]", "", clean_base_name).strip()
                            clean_base_name = re.sub(r"\s+", " ", clean_base_name).strip()
                            match = get_close_matches(clean_base_name, [txt_base_name], n=1, cutoff=0.9)
                            base_name_numbers = re.findall(r'\d+', clean_base_name)
                            txt_name_numbers = re.findall(r'\d+', txt_base_name)
                            if match:
                                matched_name = match[0]
                                matched_name_numbers = re.findall(r'\d+', matched_name)
                                if (base_name_numbers and matched_name_numbers and base_name_numbers == matched_name_numbers) or (not base_name_numbers and not matched_name_numbers):
                                    new_base_name = matched_name
                                    disc_info = re.search(r"\(Disc \d+\)", base_name)
                                    if disc_info:
                                        new_base_name = new_base_name + " " + disc_info.group()
                                    new_bin_path = os.path.join(os.path.dirname(bin_files[base_name]), new_base_name + ".bin")
                                    new_cue_path = os.path.join(os.path.dirname(cue_files[base_name]), new_base_name + ".cue")
                                    if new_base_name != base_name:
                                        print(f"Renaming {base_name}.bin and {base_name}.cue to {new_base_name}.bin and {new_base_name}.cue")
                                        os.rename(bin_files[base_name], new_bin_path)
                                        os.rename(cue_files[base_name], new_cue_path)
                                        bin_files[new_base_name] = new_bin_path
                                        cue_files[new_base_name] = new_cue_path
                                        del bin_files[base_name]
                                        del cue_files[base_name]
                                    else:
                                        print(f"File name already matches: {base_name}.bin and {base_name}.cue")
                                else:
                                    print(f"Skipping {base_name}.bin and {base_name}.cue due to number mismatch with {matched_name}")
                print("All game titles have been renamed according to the closest match from the .txt files.")
                print("\n\n\n")

                # New prompt for cover art
                work_on_cover_art = input("Your games should be all set now. Do you want to start working on your cover art? (yes/no): ").strip().lower()
                if work_on_cover_art == "yes":
                    print("Here are the .png files found in the 'ps1 cover art' folder:")
                    for root, dirs, files in os.walk(ps1_cover_art_folder):
                        for file in files:
                            if file.endswith('.png'):
                                png_files.append(os.path.join(root, file))
                                print(f"- {file}")
                    print("\n\n\n")

                    remove_region_from_png = input("Would you like to remove the '(Region)' information from these titles too? (yes/no): ").strip().lower()
                    if remove_region_from_png == "yes":
                        updated_png_files = []
                        for file_path in png_files:
                            file_name = os.path.basename(file_path)
                            new_file_name = re.sub(r"\((?!Disc \d+)[^\)]+\)", "", file_name).strip()
                            new_file_name = re.sub(r"\[\[.*?\]\]", "", new_file_name).strip()
                            new_file_name = re.sub(r"\s+", " ", new_file_name).replace(" .", ".").strip()
                            new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
                            if new_file_name != file_name:
                                os.rename(file_path, new_file_path)
                                updated_png_files.append(new_file_path)
                                print(f"Renamed: {file_name} to {new_file_name}")
                            else:
                                print(f"File name already matches: {file_name}")
                                updated_png_files.append(file_path)
                        png_files = updated_png_files
                        print("\nAll done! All region info has been removed from your covers.")
                        print("\n\n\n")

                    rename_covers = input("Do you want to rename the covers so they match your game titles? (yes/no): ").strip().lower()
                    if rename_covers == "yes":
                        print("Renaming covers to match game titles...")
                        unmatched_games = []
                        for base_name in bin_files.keys():
                            match_found = False
                            clean_base_name = re.sub(r"\(Disc \d+\)", "", base_name).strip().lower()
                            clean_base_name = re.sub(r"\[\[.*?\]\]", "", clean_base_name).strip().lower()
                            for png_file_path in png_files:
                                png_base_name = os.path.splitext(os.path.basename(png_file_path))[0].lower()
                                match = get_close_matches(png_base_name, [clean_base_name], n=1, cutoff=0.95)
                                base_name_numbers = re.findall(r'\d+', clean_base_name)
                                png_name_numbers = re.findall(r'\d+', png_base_name)
                                if match and ((not base_name_numbers and not png_name_numbers) or base_name_numbers == png_name_numbers):
                                    new_png_name = base_name + ".cue.png"
                                    new_png_path = os.path.join(os.path.dirname(png_file_path), new_png_name)
                                    print(f"Renaming {os.path.basename(png_file_path)} to {new_png_name}")
                                    shutil.copyfile(png_file_path, new_png_path)
                                    shutil.move(new_png_path, os.path.join(renamed_cover_art_folder, new_png_name))
                                    print(f"Moved {new_png_name} to {renamed_cover_art_folder}")
                                    match_found = True
                                    break
                            if not match_found:
                                unmatched_games.append(os.path.dirname(bin_files[base_name]))
                                print(f"No match found for game: {base_name}")
                        for game_folder in set(unmatched_games):
                            new_folder_path = shutil.move(game_folder, unmatched_games_folder)
                            print(f"Moved {os.path.basename(game_folder)} to {new_folder_path}")
                        print("Cover renaming complete.")
                    else:
                        print("Cover renaming skipped.")
                else:
                    print("Region removal skipped for cover art.")
            elif continue_renaming == "no":
                print("Renaming process aborted.")
            else:
                print("Invalid input. Renaming process aborted.")
        else:
            print("No matching .bin and .cue files found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        # Move all unmatched directories to the unmatched games folder
        for dir_path in unmatched_games:
            new_path = shutil.move(dir_path, unmatched_games_folder)
            print(f"Moved {os.path.basename(dir_path)} to {new_path}")
else:
    print("Okay, maybe next time!")

# Final pause to ensure the user can see everything before the script closes
print("\nAll unmatched games have been moved to the 'unmatched games' folder.")
print("\nThank you for using this script!")
time.sleep(3)
print("""
d8888b.  .d8b.  d888888b      d8888b. .d8888.  db                      
88  `8D d8' `8b `~~88~~'      88  `8D 88'  YP o88                      
88   88 88ooo88    88         88oodD' `8bo.    88                      
88   88 88~~~88    88         88~~~     `Y8b.  88                      
88  .8D 88   88    88         88      db   8D  88                      
Y8888D' YP   YP    YP         88      `8888Y'  VP                      
                                                                       
                                                                       
db   d8b   db d888888b d888888b d88888b db       .d88b.  db   d8b   db 
88   I8I   88   `88'     `88'   88'     88      .8P  Y8. 88   I8I   88 
88   I8I   88    88       88    88ooo   88      88    88 88   I8I   88 
Y8   I8I   88    88       88    88~~~   88      88    88 Y8   I8I   88 
`8b d8'8b d8'   .88.     .88.   88      88booo. `8b  d8' `8b d8'8b d8' 
 `8b8' `8d8'  Y888888P Y888888P YP      Y88888P  `Y88P'   `8b8' `8d8'  
                                                                       
                                                                       
d888888b  .d88b.   .d88b.  db                                          
`~~88~~' .8P  Y8. .8P  Y8. 88                                          
   88    88    88 88    88 88                                          
   88    88    88 88    88 88                                          
   88    `8b  d8' `8b  d8' 88booo.                                     
   YP     `Y88P'   `Y88P'  Y88888P 
                                                          
                                                          
""")
input("\nProcess complete. Press Enter to exit...")  # Pause to keep the script open