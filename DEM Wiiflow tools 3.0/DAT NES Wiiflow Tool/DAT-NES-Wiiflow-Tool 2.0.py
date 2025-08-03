import os
import time
import re
import difflib
import shutil
from collections import defaultdict

def normalize_title(title):
    return re.sub(r'\s*\(.*?\)\s*', '', title, flags=re.IGNORECASE).strip()

def find_duplicates(directory):
    file_titles = defaultdict(list)
    
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            title, _ = os.path.splitext(file)
            normalized_title = normalize_title(title)
            file_titles[normalized_title].append(file)
    
    duplicates = {title: paths for title, paths in file_titles.items() if len(paths) > 1}
    return duplicates

def prompt_for_versions(files, title):
    print(f"Duplicate versions found for: {title}")
    for idx, file in enumerate(files, 1):
        print(f"{idx}. {file}")
    
    while True:
        choice = input(f"Which version would you like to keep (enter the number 1-{len(files)}). If you want to keep more than 1, separate your choices with a comma (1,2,3): ").strip()
        choices = [int(c) - 1 for c in choice.split(',') if c.isdigit() and 1 <= int(c) <= len(files)]
        if choices:
            return choices
        else:
            print("Invalid choice. Please enter valid numbers separated by commas.")

def move_unwanted_versions(duplicates, source_folder, target_folder):
    removed_files = []
    
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    for title, files in duplicates.items():
        choice_idxs = prompt_for_versions(files, title)
        
        for idx, file in enumerate(files):
            if idx not in choice_idxs:
                shutil.move(os.path.join(source_folder, file), os.path.join(target_folder, file))
                removed_files.append(file)
    
    return removed_files

def list_nes_games():
    try:
        nes_folder = os.path.join(os.getcwd(), "nes games")
        if not os.path.exists(nes_folder):
            print('The "nes games" folder does not exist.')
            return False
        nes_files = [f for f in os.listdir(nes_folder) if f.endswith('.nes')]

        if not nes_files:
            print('No .nes files present in the "nes games" folder.')
            time.sleep(5)
            return False

        return nes_files
    except Exception as e:
        print(f"Error in list_nes_games: {e}")
        return False

def remove_version_region_info(filename):
    try:
        new_filename = re.sub(r'[\(\[].*?[\)\]]', '', filename)
        return new_filename.strip()
    except Exception as e:
        print(f"Error in remove_version_region_info: {e}")
        return filename

def list_txt_files():
    try:
        txt_folder = os.path.join(os.getcwd(), "nes plain text names")
        if not os.path.exists(txt_folder):
            print('The "nes plain text names" folder does not exist.')
            return False
        txt_files = [f for f in os.listdir(txt_folder) if f.endswith('.txt')]

        if not txt_files:
            print('No .txt files present in the "nes plain text names" folder.')
            return False

        return txt_files
    except Exception as e:
        print(f"Error in list_txt_files: {e}")
        return False

def list_cover_art_files():
    try:
        art_folder = os.path.join(os.getcwd(), "nes cover art")
        if not os.path.exists(art_folder):
            print('The "nes cover art" folder does not exist.')
            return False

        art_files = []
        for root, dirs, files in os.walk(art_folder):
            for file in files:
                if file.lower().endswith(('.png', '.jpeg', '.jpg')):
                    art_files.append(os.path.join(root, file))

        if not art_files:
            print('No cover art files present in the "nes cover art" folder.')
            return False

        return art_files
    except Exception as e:
        print(f"Error in list_cover_art_files: {e}")
        return False

def find_best_match(game_name, file_names):
    try:
        def clean_name(name):
            name = re.sub(r'[\(\[].*?[\)\]]', '', name)  # Remove parentheses and their contents
            return re.sub(r'[^A-Za-z0-9 ]+', '', name).lower().strip()

        def token_set_ratio(name1, name2):
            tokens1 = set(clean_name(name1).split())
            tokens2 = set(clean_name(name2).split())
            return difflib.SequenceMatcher(None, " ".join(sorted(tokens1)), " ".join(sorted(tokens2))).ratio()

        cleaned_game_name = clean_name(game_name)
        best_match = None
        highest_ratio = 0.85  # Start with a higher threshold for better accuracy

        for file_name in file_names:
            cleaned_file_name = clean_name(file_name)
            if cleaned_game_name == cleaned_file_name:
                return file_name  # Exact match

            ratio = token_set_ratio(cleaned_game_name, cleaned_file_name)
            if ratio > highest_ratio:
                highest_ratio = ratio
                best_match = file_name

        return best_match if highest_ratio > 0.85 else None  # Only return matches with ratio above threshold
    except Exception as e:
        print(f"Error in find_best_match: {e}")
        return None

def special_names():
    try:
        nes_folder = os.path.join(os.getcwd(), "nes games")
        if not os.path.exists(nes_folder):
            print('The "nes games" folder does not exist.')
            return False
        
        specific_renames = {
            "720.nes": "720 Degrees.nes",
            "Hudson's Adventure Island.nes": "Adventure Island.nes",
            "Hudson's Adventure Island II.nes": "Adventure Island II.nes",
            "Hudson's Adventure Island III.nes": "Adventure Island 3.nes",
            "Hudson's Adventure Island V.nes": "Adventure Island 4.nes",
            "Penguin & Seal, The.nes": "Arctic Adventure - Penguin & Seal.nes",
            "Bases Loaded II.nes": "Bases Loaded 2 - Second Season.nes",
            "Battletoads & Double Dragon - The Ultimate Team.nes": "Battletoads-Double Dragon.nes",
            "Bugs Bunny Crazy Castle, The.nes": "Bugs Bunny Crazy Castle, The.nes",
            "Gold Medal Challenge '92.nes": "Capcom's Gold Medal Challenge '92.nes",
            "Chip 'n Dale Rescue Rangers.nes": "Chip 'n Dale - Rescue Rangers.nes",
            "Conan - The Mysteries of Time.nes": "Conan.nes",
            "Base Wars.nes": "Cyber Stadium Series - Base Wars.nes",
            "Demon Sword.nes": "Demon Sword - Release the Power.nes",
            "Dirty Harry - The War Against Drugs.nes": "Dirty Harry.nes",
            "Dizzy The Adventurer.nes": "Wonderland Dizzy.nes",
            "Double Strike.nes": "Double Strike - Aerial Attack Force.nes",
            "Duck.nes": "Duck Hunt.nes",
            "Exodus.nes": "Exodus - Journey to the Promised Land.nes",
            "Fire Emblem.nes": "Fire Emblem - Shadow Dragon & the Blade of Light.nes",
            "Firehouse Rescue.nes": "Fisher-Price - Firehouse Rescue.nes",
            "I Can Remember.nes": "Fisher-Price - I Can Remember.nes",
            "Perfect Fit.nes": "Fisher-Price - Perfect Fit.nes",
            "Peter Pan & The Pirates.nes": "Fox's Peter Pan & the Pirates - The Revenge of Captain Hook.nes",
            "G.I. Joe.nes": "G.I. Joe - A Real American Hero.nes",
            "Gargoyle's Quest II - The Demon Darkness.nes": "Gargoyle's Quest II.nes",
            "Ghosts 'N Goblins.nes": "Ghosts'n Goblins.nes",
            "Thunder Warrior.nes": "gluk the thunder warrior.nes",
            "Iron Tank.nes": "Iron Tank - The Invasion of Normandy.nes",
            "Joe & Mac - Caveman Ninja.nes": "Joe & Mac.nes",
            "Joshua.nes": "Joshua & the Battle of Jericho.nes",
            "Joypad Test Cartridge.nes": "Joystick Test Cartridge.nes",
            "Kid Klown.nes": "Kid Klown in Night Mayor World.nes",
            "King of Kings, The.nes": "King of Kings - The Early Years.nes",
            "Kings of the Beach.nes": "Kings of the Beach - Professional Beach Volleyball.nes",
            "Legend of the Ghost Lion.nes": "Ghost Lion.nes",
            "Legends of the Diamond.nes": "Legends of the Diamond - The Baseball Championship Game.nes",
            "M.U.S.C.L.E..nes": "M.U.S.C.L.E. - Tag Team Match.nes",
            "Magic Mathematic.nes": "Magical Mathematics.nes",
            "Mermaids of Atlantis The Riddle of the Magic Bubble.nes": "Mermaids of Atlantis.nes",
            "Michael Andretti's World Grand Prix.nes": "Michael Andretti's World GP.nes",
            "Might and Magic.nes": "Might & Magic - Secret of the Inner Sanctum.nes",
            "NFL Football.nes": "NFL.nes",
            "Orb 3D.nes": "Orb-3D.nes",
            "Pesterminator - The Western Exterminator.nes": "Pesterminator.nes",
            "Pictionary.nes": "Pictionary - The Game of Video Quick Draw.nes",
            "Power Rangers III.nes": "Power Rangers 3.nes",
            "Power Rangers IV.nes": "Power Rangers 4.nes",
            "Rainbow Islands - The Story of Bubble Bobble 2.nes": "Parasol Stars - Rainbow Islands 2.nes",
            "Snow Bros..nes": "Snow Brothers.nes",
            "Somari.nes": "Somari the Adventurer.nes",
            "Spot.nes": "Spot - The Video Game.nes",
            "Sunday Funday.nes": "Sunday Funday - The Ride.nes",
            "3-D Battles of World Runner, The.nes": "3-D WorldRunner.nes",
            "Bard's Tale, The - Tales of the Unknown.nes": "Bard's Tale, The.nes",
            "Black Bass USA, The.nes": "Black Bass, The.nes",
            "Mafat Conspiracy - Golgo 13.nes": "Mafat Conspiracy, The.nes",
            "Mutant Virus, The.nes": "Mutant Virus, The - Crisis in a Computer World.nes",
            "Ren & Stimpy Show, The.nes": "Ren & Stimpy Show, The - Buckeroo$.nes",
            "Three Stooges.nes": "Three Stooges, The.nes",
            "Tom & Jerry.nes": "Tom & Jerry - The Ultimate Game of Cat and Mouse!.nes",
            "Touch Down Fever.nes": "Touchdown Fever.nes",
            "T&C 2 - Thrilla's Surfari.nes": "Town & Country Surf Designs - Thrilla's Surfari.nes",
            "T&C Surf Design.nes": "Town & Country Surf Designs - Wood & Water Rage.nes",
            "Whomp'Em.nes": "Whomp 'Em.nes",
            "Wizardry - The Knight of Diamonds.nes": "Wizardry - Knight of Diamonds - The Second Scenario.nes",
            "Wizards & Warriors III - Kuros - Visions of Power.nes": "Wizards & Warriors III - Kuros...Visions of Power.nes",
            "World Champ.nes": "World Champ - Super Boxing Great Fight.nes",
            "Xevious.nes": "Xevious - The Avenger.nes",
            "Advanced Dungeons & Dragons  Dragon Strike.nes": "Advanced Dungeons & Dragons - DragonStrike.nes",
            "Chip 'n Dale  Rescue Rangers.nes": "Chip 'n Dale - Rescue Rangers.nes",
            "Dig Dug.nes": "Dig Dug (World) (Namcot Collection, Namco Museum Archives Vol 1).nes",
            "Dig Dug II.nes": "Dig Dug II  Trouble in Paradise.nes",
            "Big Bird's Hide & Speak.nes": "Sesame Street - Big Bird's Hide & Speak.nes",
            "Ren & Stimpy Show, The - Buckeroo$.nes": "Ren & Stimpy Show, The - Buckeroo$!.nes",
            "Twin Eagle - Revenge Joe's Brother.nes": "Twin Eagle.nes"
        }
        
        for file in os.listdir(nes_folder):
            if file in specific_renames:
                new_file_name = specific_renames[file]
                if os.path.exists(os.path.join(nes_folder, new_file_name)):
                    print(f"File '{new_file_name}' already exists. Skipping rename for '{file}'.")
                else:
                    try:
                        os.rename(os.path.join(nes_folder, file), os.path.join(nes_folder, new_file_name))
                        print(f"Renamed '{file}' to '{new_file_name}'")
                    except Exception as e:
                        print(f"Failed to rename '{file}' to '{new_file_name}': {e}")
        
        # Force rename for "Mermaids of Atlantis The Riddle of the Magic Bubble.nes"
        file_to_force_rename = "Mermaids of Atlantis The Riddle of the Magic Bubble.nes"
        forced_new_name = "Mermaids of Atlantis.nes"
        if os.path.exists(os.path.join(nes_folder, file_to_force_rename)):
            try:
                os.rename(os.path.join(nes_folder, file_to_force_rename), os.path.join(nes_folder, forced_new_name))
                print(f"Force renamed '{file_to_force_rename}' to '{forced_new_name}'")
            except Exception as e:
                print(f"Failed to force rename '{file_to_force_rename}' to '{forced_new_name}'")

    except Exception as e:
        print(f"Error in special_names: {e}")

def rename_megaman_games():
    try:
        nes_folder = os.path.join(os.getcwd(), "nes games")
        if not os.path.exists(nes_folder):
            print('The "nes games" folder does not exist.')
            return False
        
        megaman_mapping = {
            "Megaman": "Mega Man",
            "Megaman II": "Mega Man 2",
            "Megaman III": "Mega Man 3",
            "Megaman IV": "Mega Man 4",
            "Megaman V": "Mega Man 5",
            "Megaman VI": "Mega Man 6"
        }
        
        nes_files = [f for f in os.listdir(nes_folder) if f.endswith('.nes')]
        for file in nes_files:
            base_name, ext = os.path.splitext(file)
            if base_name in megaman_mapping:
                new_base_name = megaman_mapping[base_name]
                new_file = new_base_name + ext
                if os.path.exists(os.path.join(nes_folder, new_file)):
                    print(f"File '{new_file}' already exists. Skipping rename for '{file}'.")
                else:
                    try:
                        os.rename(os.path.join(nes_folder, file), os.path.join(nes_folder, new_file))
                        print(f"Renamed '{file}' to '{new_file}'")
                    except Exception as e:
                        print(f"Failed to rename '{file}' to '{new_file}': {e}")
    except Exception as e:
        print(f"Error in rename_megaman_games: {e}")

def transfer_matching_cover_art(nes_files, art_files):
    renamed_folder = os.path.join(os.getcwd(), "renamed cover art")
    if not os.path.exists(renamed_folder):
        os.makedirs(renamed_folder)

    for nes_file in nes_files:
        nes_file_base = os.path.splitext(nes_file)[0]
        for art_file in art_files:
            art_file_base = os.path.splitext(os.path.basename(art_file))[0]
            if art_file_base.lower() == nes_file_base.lower():
                new_art_name = f"{nes_file_base}.nes.png"
                new_art_path = os.path.join(renamed_folder, new_art_name)
                
                if os.path.exists(new_art_path):
                    print(f"File '{new_art_path}' already exists. Skipping rename for '{art_file}'.")
                else:
                    try:
                        os.rename(art_file, new_art_path)
                        print(f"Transferred '{art_file}' to '{new_art_path}'")
                    except Exception as e:
                        print(f"Failed to transfer '{art_file}' to '{new_art_name}': {e}")

def main():
    print("Thank you for using DAT NES Wiiflow Tool!")
    answer = input("Would you like to see your listed NES games? (yes/no): ").strip().lower()

    if answer == 'yes':
        nes_files = list_nes_games()
        if nes_files:
            print("Here are your NES games:")
            for file in nes_files:
                print(file)
            print("\n\n\nThese are the games I picked up!")
        else:
            print("No .nes files present in the 'nes games' folder.")
            time.sleep(5)
            return
    else:
        print("Too Bad, So Sad...")
        time.sleep(3)
        nes_files = list_nes_games()
        if nes_files:
            print("Here are your NES games:")
            for file in nes_files:
                print(file)
            print("\n\n\nThese are the games I picked up!")
        else:
            print("No .nes files present in the 'nes games' folder.")
            time.sleep(5)
            return

    if nes_files:
        print("\n\n")
        
        answer = input("Would you like to check for duplicate titles? (yes/no): ").strip().lower()

        if answer == 'yes':
            source_folder = 'nes games'
            target_folder = 'Removed games'

            duplicates = find_duplicates(source_folder)
            
            if duplicates:
                print("Duplicate titles found:")
                for title, files in duplicates.items():
                    print(f"{title}:")
                    for file in files:
                        print(f"  - {file}")
                
                while True:
                    user_input = input("\n\n\nDo you want to remove duplicates by selecting which version to keep? (yes/no): ").strip().lower()
                    if user_input == 'yes':
                        removed_files = move_unwanted_versions(duplicates, source_folder, target_folder)
                        
                        print("\n\nThe following files were moved to 'Removed games':")
                        
                        for file in removed_files:
                            print(f"  - {file}")
                        break
                    elif user_input == 'no':
                        print("No files were moved.")
                        break
                    else:
                        print("Please answer 'yes' or 'no'.")
            else:
                print("No duplicate titles found.")
            input("Press Enter to continue...")

        answer = input("Would you like to remove the version and region information from the title names?\nExample: 'Dr.Mario (USA).nes' would be changed to 'Dr.Mario.nes'\nYes or no? ").strip().lower()

        if answer == 'yes':
            nes_folder = os.path.join(os.getcwd(), "nes games")
            for file in nes_files:
                base_name, ext = os.path.splitext(file)
                new_base_name = remove_version_region_info(base_name)
                new_file = new_base_name + ext
                
                if os.path.exists(os.path.join(nes_folder, new_file)):
                    print(f"File '{new_file}' already exists. Skipping rename for '{file}'.")
                else:
                    try:
                        os.rename(os.path.join(nes_folder, file), os.path.join(nes_folder, new_file))
                        print(f"Renamed '{file}' to '{new_file}'")
                    except Exception as e:
                        print(f"Failed to rename '{file}' to '{new_file}': {e}")
            
            print("\n\n\nAll Done! I did my best to remove what I could.\n\n\n")

        rename_megaman_games()
        special_names()
        
        print("\n\nWould you like to reference the text list made by Below Average Gaming to rename your games too? (yes/no): ")
        
        answer = input().strip().lower()

        if answer == 'yes':
            txt_files = list_txt_files()
            if txt_files:
                print("Here are the text files in the 'nes plain text names' folder:")
                for file in txt_files:
                    print(file)
                
                print("\n\n\n")
                answer = input("Would you like to match the names above to your NES games and then rename them? (yes/no): ").strip().lower()

                if answer == 'yes':
                    nes_folder = os.path.join(os.getcwd(), "nes games")
                    matches = []
                    already_matched = set()
                    while True:
                        changes_made = False
                        nes_files = list_nes_games()
                        for game_file in nes_files:
                            if game_file in already_matched:
                                continue
                            game_name, _ = os.path.splitext(game_file)
                            best_match = find_best_match(game_name, txt_files)
                            if best_match:
                                matches.append((game_file, best_match))
                                new_file_name = os.path.splitext(best_match)[0] + ".nes"
                                if os.path.exists(os.path.join(nes_folder, new_file_name)):
                                    print(f"File '{new_file_name}' already exists. Skipping rename for '{game_file}'.")
                                else:
                                    try:
                                        os.rename(os.path.join(nes_folder, game_file), os.path.join(nes_folder, new_file_name))
                                        print(f"Matched '{game_file}' to '{best_match}' and renamed to '{new_file_name}'")
                                        changes_made = True
                                        already_matched.add(new_file_name)
                                    except Exception as e:
                                        print(f"Failed to rename '{game_file}' to '{new_file_name}': {e}")
                        if not changes_made:
                            break

                    if matches:
                        print("\nMatched and renamed files:")
                        for match in matches:
                            print(f"{match[0]} -> {match[1]}")

                    print("\n\n\nYour NES games have been renamed!\n\n\n")
                    answer = input("Would you like to start working on your boxart now? (yes/no): ").strip().lower()

                    if answer == 'yes':
                        art_files = list_cover_art_files()
                        if art_files:
                            answer = input("First thing we should do is remove all of the version information from the boxart titles. Sound good? (yes/no): ").strip().lower()

                            if answer == 'yes':
                                art_folder = os.path.join(os.getcwd(), "nes cover art")
                                for art_file in art_files:
                                    base_name, ext = os.path.splitext(os.path.basename(art_file))
                                    new_base_name = remove_version_region_info(base_name)
                                    new_art_file = new_base_name + ext
                                    
                                    new_art_path = os.path.join(art_folder, new_art_file)
                                    if os.path.exists(new_art_path):
                                        print(f"File '{new_art_path}' already exists. Skipping rename for '{art_file}'.")
                                    else:
                                        try:
                                            os.rename(os.path.join(art_folder, art_file), new_art_path)
                                            print(f"Renamed '{art_file}' to '{new_art_file}'")
                                        except Exception as e:
                                            print(f"Failed to rename '{art_file}' to '{new_art_file}': {e}")

                                art_files = list_cover_art_files()

                            print("\n\n\nGreat! Now that that's out of the way, This is the boxart that I found! You should probably rename this as well... Want to rename them? (yes/no): ")
                            answer = input().strip().lower()

                            if answer == 'yes':
                                art_matches = []
                                nes_file_titles = [os.path.splitext(f)[0] for f in nes_files]
                                already_matched_art = set()
                                while True:
                                    changes_made = False
                                    for art_file in art_files:
                                        if art_file in already_matched_art:
                                            continue
                                        art_file_title = os.path.splitext(os.path.basename(art_file))[0]
                                        best_match = find_best_match(art_file_title, nes_file_titles)
                                        if best_match:
                                            art_matches.append((best_match + ".nes", art_file))
                                            changes_made = True
                                            already_matched_art.add(art_file)
                                            print(f"Matched '{art_file}' to '{best_match}'")
                                    if not changes_made:
                                        break

                                if art_matches:
                                    for game_file, art_file in art_matches:
                                        game_base, _ = os.path.splitext(game_file)
                                        new_art_name = game_base + ".nes.png"
                                        new_art_path = os.path.join(os.getcwd(), "renamed cover art", new_art_name)
                                        
                                        if os.path.exists(new_art_path):
                                            print(f"File '{new_art_path}' already exists. Skipping rename for '{art_file}'.")
                                        else:
                                            try:
                                                os.rename(art_file, new_art_path)
                                                print(f"Renamed '{art_file}' to '{new_art_name}'")
                                            except Exception as e:
                                                print(f"Failed to rename '{art_file}' to '{new_art_name}': {e}")
                                else:
                                    print("No matching cover art files found.")

                                transfer_matching_cover_art(nes_files, art_files)
                            else:
                                print("\n\n\nWhy would you get this far and say no! :'(")
                                time.sleep(3)
                                return
                    else:
                        print("\n\n\nWhy would you get this far and say no! :'(")
                        time.sleep(3)
                        return
                else:
                    print("Shutting down...")
                    time.sleep(3)
        else:
            print("\n\n\nThen what did you open me for??")
            time.sleep(3)

    # New prompt to remove unmatched games
    print("\n\n\nWould you like to remove any games that DID NOT match with a box art title? (This will help prevent blank cases in Wiiflow) (yes/no): ")
    
    answer = input().strip().lower()

    if answer == 'yes':
        nes_games_folder = 'nes games'
        renamed_cover_art_folder = 'renamed cover art'
        unmatched_games_folder = 'unmatched games'

        if not os.path.exists(unmatched_games_folder):
            os.makedirs(unmatched_games_folder)

        nes_games = [f for f in os.listdir(nes_games_folder) if f.endswith('.nes')]
        renamed_cover_art = [f for f in os.listdir(renamed_cover_art_folder) if f.endswith('.nes.png')]

        for game in nes_games:
            expected_cover_art_name = game + ".png"
            if expected_cover_art_name not in renamed_cover_art:
                print(f"\nNo match found for: {game}. Moving to 'unmatched games' folder.")
                shutil.move(os.path.join(nes_games_folder, game), os.path.join(unmatched_games_folder, game))
            else:
                print(f"Match found for: {game}")

    print("\n\n\nAll Done!")
    print("This tool was created by Below Average Gaming!")
    print("""
d8888b.  .d8b.  d888888b      d8b   db d88888b .d8888.                 
88  `8D d8' `8b `~~88~~'      888o  88 88'     88'  YP                 
88   88 88ooo88    88         88V8o 88 88ooooo `8bo.                   
88   88 88~~~88    88         88 V8o88 88~~~~~   `Y8b.                 
88  .8D 88   88    88         88  V888 88.     db   8D                 
Y8888D' YP   YP    YP         VP   V8P Y88888P `8888Y'                 
                                                                       
                                                                       
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

    print("Press any key to exit...")
    input()

if __name__ == "__main__":
    main()

# Keep the script open for review
input("Press Enter to exit...")
