import os
import time
import re
import difflib
import shutil
from collections import defaultdict

def normalize_title(title):
    return re.sub(r'\s*\((?!Disk \d+|Disk \d+ Side [A-C]|Side [A-C]).*?\)\s*|\s*\[(?!Disk \d+|Side [A-C]).*?\]\s*', '', title, flags=re.IGNORECASE).strip()

def remove_version_region_info(filename):
    keep_patterns = [
        r'\(Disk \d+\)',
        r'\(Disk \d+ Side [A-C]\)',
        r'\(Side [A-C]\)',
        r'\[Disk \d+\]',
        r'\[Side [A-C]\]'
    ]
    
    def replace_func(match):
        match_str = match.group(0)
        if any(re.search(pattern, match_str, re.IGNORECASE) for pattern in keep_patterns):
            return ' ' + match_str.strip()  # Ensure there's a space before the kept match
        return ''  # Remove other matches
    
    # This part removes the unwanted version/region info but keeps disk/side info
    cleaned_filename = re.sub(r'\s*\((?!Disk \d+|Disk \d+ Side [A-C]|Side [A-C]).*?\)\s*|\s*\[(?!Disk \d+|Side [A-C]).*?\]\s*', replace_func, filename)
    
    # Ensure there's a single space before any kept disk/side info
    cleaned_filename = re.sub(r'(?<=\S)([\(\[])', r' \1', cleaned_filename)
    
    return cleaned_filename.strip()

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

def list_commodore64_games():
    commodore64_folder = os.path.join(os.getcwd(), "commodore64 games")
    if not os.path.exists(commodore64_folder):
        print('The "commodore64 games" folder does not exist.')
        return False
    valid_extensions = ['.tap', '.d64', '.t64', '.prg']
    game_files = [f for f in os.listdir(commodore64_folder) if any(f.lower().endswith(ext) for ext in valid_extensions) and not f.lower().endswith('.crt')]

    if not game_files:
        print('No valid game files present in the "commodore64 games" folder.')
        time.sleep(5)
        return False

    return game_files

def list_txt_files():
    txt_folder = os.path.join(os.getcwd(), "commodore64 plain text names")
    if not os.path.exists(txt_folder):
        print('The "commodore64 plain text names" folder does not exist.')
        return False
    txt_files = [f for f in os.listdir(txt_folder) if f.endswith('.txt')]

    if not txt_files:
        print('No .txt files present in the "commodore64 plain text names" folder.')
        return False

    return txt_files

def list_cover_art_files():
    art_folder = os.path.join(os.getcwd(), "commodore64 cover art")
    if not os.path.exists(art_folder):
        print('The "commodore64 cover art" folder does not exist.')
        return False

    art_files = []
    for root, dirs, files in os.walk(art_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpeg', '.jpg')):
                art_files.append(os.path.join(root, file))

    if not art_files:
        print('No cover art files present in the "commodore64 cover art" folder.')
        return False

    return art_files

def find_best_match(game_name, file_names):
    def clean_name(name):
        # Preserve hyphens in the name
        name = re.sub(r'[^A-Za-z0-9 \-\(\)]+', '', name).lower().strip()
        return name

    def token_set_ratio(name1, name2):
        tokens1 = set(clean_name(name1).split())
        tokens2 = set(clean_name(name2).split())
        return difflib.SequenceMatcher(None, " ".join(sorted(tokens1)), " ".join(sorted(tokens2))).ratio()

    cleaned_game_name = clean_name(game_name)
    best_match = None
    highest_ratio = 0.85

    for file_name in file_names:
        cleaned_file_name = clean_name(file_name)
        if cleaned_game_name == cleaned_file_name:
            return file_name

        ratio = token_set_ratio(cleaned_game_name, cleaned_file_name)
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = file_name

    return best_match if highest_ratio > 0.85 else None

def special_names(game_files):
    commodore64_folder = os.path.join(os.getcwd(), "commodore64 games")
    
    specific_renames = {
        "720°": "720 Degrees",
        "atv - all terrain vehicle simulator": "ATV Simulator",
        "ace ii": "Ace 2",
        "back to the future 3": "Back to the Future Part III",
        "batman and the caped crusader": "Batman - The Caped Crusader",
        "buck rogers": "Buck Rogers - Countdown to Doomsday",
        "heatseeker": "Heat Seeker",
        "micro rhythm+": "Micro Rhythm +",
        "milk_race_": "Milk Race",
        "stunt bike": "Stunt Bike Simulator",
        "creatures ii - torture trouble": "Creatures 2",
        "cybernoid": "Cybernoid - The Fighting Machine",
        "dam buster": "Dam Busters, The",
        "death wish 3": "Deathwish III",
        "detective": "Detective, The",
        "test drive 2": "Duel, The - Test Drive II",
        "fist 2": "Fist II - The Legend Continues",
        "hellfire": "Hellfire Attack",
        "hole in one golf": "Hole in One",
        "hypa-ball": "Hyper Ball",
        "inheritance, the": "Inheritance, The",
        "international karate plus": "International Karate +",
        "ninja rabbits": "International Ninja Rabbits",
        "jail break": "Jailbreak",
        "last ninja , the": "Last Ninja",
        "last ninja ii": "Last Ninja 2",
        "last ninja iii": "Last Ninja 3",  # Directly specify the rename
        "lord of the rings": "Lord of the Rings, The",
        "match day 2": "Match Day II",
        "metro cross": "Metro-Cross",
        "mighty bomb jack": "Mighty Bombjack",
        "big mac - the mad maintenance man": "More Adventures of Big-Mac",
        "north and south": "North & South",
        "olli and lissa": "Olli & Lissa - The Ghost of Shilmoore Castle",
        "pitstop 2": "Pitstop II",
        "popeye ii": "Popeye 2",
        "predator ii": "Predator 2",
        "raging beast": "Raging Beast - Ole!",
        "rambo 3": "Rambo III - The Rescue",
        "rebounder": "Re-Bounder",
        "space warriors": "Return of the Space Warriors",
        "robocop ii": "RoboCop 2",
        "space harrier 2": "Space Harrier II",
        "spikey in transylvania": "Spike in Transylvania",
        "task 3": "Task III",
        "terminator ii - judgment day": "Terminator 2 - Judgment Day",
        "train escape to normandy, the": "Train, The - Escape to Normandy",
        "trap door, the": "Trapdoor, The",
        "221b baker street": "221B Baker St.",
        "faery tale adventure, the": "Faery Tale Adventure",
        "teenage mutant ninja turtles": "Teenage Mutant Ninja Turtles, The"
    }
    
    renamed_files = []
    
    for file in game_files:
        file_lower = file.lower()  # Convert the filename to lowercase for comparison
        
        # Check specifically for "last ninja iii" and rename it directly, retaining side/disk info
        if "last ninja iii" in file_lower:
            disk_info_match = re.search(r'\(Disk \d+\)|\(Disk \d+ Side [A-C]\)|\(Side [A-C]\)', file, re.IGNORECASE)
            disk_info = disk_info_match.group(0) if disk_info_match else ''
            new_file_name = f"Last Ninja 3 {disk_info}".strip() + os.path.splitext(file)[1]
            target_path = os.path.join(commodore64_folder, new_file_name)
            try:
                os.rename(os.path.join(commodore64_folder, file), target_path)
                print(f"Renamed '{file}' to '{new_file_name}'")
                renamed_files.append(new_file_name)
            except Exception as e:
                print(f"Failed to rename '{file}' to '{new_file_name}': {e}")
            continue  # Skip to the next file
        
        # Proceed with the general renaming process
        cleaned_file_name = remove_version_region_info(file_lower)  # Clean the file name
        
        # Convert the cleaned filename and the specific renames keys to lowercase for comparison
        for original, new_name in specific_renames.items():
            if original in cleaned_file_name:
                # Extract the disk/side info if present
                disk_info_match = re.search(r'\(Disk \d+\)|\(Disk \d+ Side [A-C]\)|\(Side [A-C]\)', file)
                disk_info = disk_info_match.group(0) if disk_info_match else ''
                
                # Append the disk/side info if available
                new_file_name = f"{new_name} {disk_info}{os.path.splitext(file)[1]}"
                target_path = os.path.join(commodore64_folder, new_file_name)
                
                try:
                    os.rename(os.path.join(commodore64_folder, file), target_path)
                    print(f"Renamed '{file}' to '{new_file_name}'")
                    renamed_files.append(new_file_name)
                except Exception as e:
                    print(f"Failed to rename '{file}' to '{new_file_name}': {e}")
                break  # Exit the loop once a match is found and renamed
                
    return renamed_files

def transfer_matching_cover_art(game_files, art_files):
    renamed_folder = os.path.join(os.getcwd(), "renamed cover art")
    if not os.path.exists(renamed_folder):
        os.makedirs(renamed_folder)

    matched_files = set()
    
    for game_file in game_files:
        game_file_base, game_ext = os.path.splitext(game_file)
        game_file_base_lower = game_file_base.lower()
        for art_file in art_files:
            art_file_base = os.path.splitext(os.path.basename(art_file))[0].lower()
            if art_file_base == game_file_base_lower:
                # Check for any disk info in the game file
                disk_info_match = re.search(r'\(Disk \d+\)|\(Disk \d+ Side [A-C]\)|\(Side [A-C]\)|\[Disk \d+\]|\[Side [A-C]\]', game_file, re.IGNORECASE)
                disk_info = disk_info_match.group(0) if disk_info_match else ''
                
                new_art_name = f"{game_file_base}{disk_info}{game_ext}.png".strip()  # Retain original extension, disk info, and append .png
                new_art_path = os.path.join(renamed_folder, new_art_name)
                
                if os.path.exists(new_art_path):
                    print(f"File '{new_art_path}' already exists. Skipping rename for '{art_file}'.")
                else:
                    try:
                        shutil.copy(art_file, new_art_path)
                        print(f"Transferred '{art_file}' to '{new_art_path}'")
                        matched_files.add(game_file)  # Track the matched game file
                    except Exception as e:
                        print(f"Failed to transfer '{art_file}' to '{new_art_name}': {e}")

    return matched_files

def match_and_rename_cover_art_with_disk_info(game_files, art_files):
    commodore64_folder = os.path.join(os.getcwd(), "commodore64 games")
    renamed_folder = os.path.join(os.getcwd(), "renamed cover art")

    if not os.path.exists(renamed_folder):
        os.makedirs(renamed_folder)

    for game_file in game_files:
        base_name, ext = os.path.splitext(game_file)
        base_name_cleaned = re.sub(r'\(Disk \d+\)|\(Disk \d+ Side [A-C]\)|\(Side [A-C]\)|\[Disk \d+\]|\[Side [A-C]\]', '', base_name).strip()  # Remove disk info from base name for matching
        
        matched = False
        for art_file in art_files:
            art_file_base, art_ext = os.path.splitext(os.path.basename(art_file))
            if base_name_cleaned.lower() == art_file_base.lower():  # Match base name
                matched = True
                disk_info_match = re.search(r'\(Disk \d+\)|\(Disk \d+ Side [A-C]\)|\(Side [A-C]\)|\[Disk \d+\]|\[Side [A-C]\]', game_file, re.IGNORECASE)
                disk_info = disk_info_match.group(0) if disk_info_match else ''
                new_art_name = f"{art_file_base} {disk_info}{ext}.png".strip() if disk_info else f"{art_file_base}{ext}.png".strip()
                new_art_path = os.path.join(renamed_folder, new_art_name)
                
                if os.path.exists(new_art_path):
                    print(f"File '{new_art_path}' already exists. Skipping rename for '{art_file}'.")
                else:
                    try:
                        shutil.copy(art_file, new_art_path)
                        print(f"Matched and renamed '{art_file}' to '{new_art_name}'")
                        
                        # Create additional copies for other disks or sides
                        if disk_info:
                            disk_number_match = re.search(r'Disk (\d+)', disk_info)
                            if disk_number_match:
                                disk_number = int(disk_number_match.group(1))
                                for i in range(2, disk_number + 1):
                                    additional_disk_info = f"(Disk {i})"
                                    additional_art_name = f"{art_file_base} {additional_disk_info}{ext}.png"
                                    additional_art_path = os.path.join(renamed_folder, additional_art_name)
                                    shutil.copy(art_file, additional_art_path)
                                    print(f"Created additional copy for '{additional_art_name}'")
                    except Exception as e:
                        print(f"Failed to rename '{art_file}' to '{new_art_name}': {e}")
                break
        
        if not matched:
            print(f"No match found for: {game_file}. Moving to 'unmatched games' folder.")
            unmatched_folder = os.path.join(os.getcwd(), 'unmatched games')
            if not os.path.exists(unmatched_folder):
                os.makedirs(unmatched_folder)
            try:
                if os.path.exists(os.path.join(commodore64_folder, game_file)):
                    shutil.move(os.path.join(commodore64_folder, game_file), os.path.join(unmatched_folder, game_file))
                else:
                    print(f"File '{game_file}' does not exist, skipping move.")
            except Exception as e:
                print(f"Failed to move '{game_file}' to 'unmatched games' folder: {e}")

def main():
    print("Thank you for using DAT Commodore 64 Wiiflow Tool!")
    
    # Perform special renaming at the start
    game_files = list_commodore64_games()
    if game_files:
        print("I already started renaming a few of these for you!")
        special_names(game_files)

    answer = input("Would you like to see your listed Commodore 64 games? (yes/no): ").strip().lower()

    if answer == 'yes':
        game_files = list_commodore64_games()
        if game_files:
            print("Here are your Commodore 64 games:")
            for file in game_files:
                print(file)
            print("\n\n\nThese are the games I picked up!")
        else:
            print("No valid game files present in the 'commodore64 games' folder.")
            time.sleep(5)
            return
    else:
        print("Too Bad, So Sad...")
        time.sleep(3)
        game_files = list_commodore64_games()
        if game_files:
            print("Here are your Commodore 64 games:")
            for file in game_files:
                print(file)
            print("\n\n\nThese are the games I picked up!")
        else:
            print("No valid game files present in the 'commodore64 games' folder.")
            time.sleep(5)
            return

    if game_files:
        print("\n\n")
        
        answer = input("Would you like to check for duplicate titles? (yes/no): ").strip().lower()

        if answer == 'yes':
            source_folder = 'commodore64 games'
            target_folder = 'Removed games'

            duplicates = find_duplicates(source_folder)
            
            if duplicates:
                print("Duplicate titles found:")
                for title, files in duplicates.items():
                    print(f"{title}:")
                    for file in files:
                        print(f"  - {file}")
                
                while True:
                    user_input = input("Do you want to remove duplicates by selecting which version to keep? (yes/no): ").strip().lower()
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

        answer = input("Would you like to remove the version and region information from the title names?\nExample: 'Avenger (USA).tap' would be changed to 'Avenger.tap'\nYes or no? ").strip().lower()

        if answer == 'yes':
            commodore64_folder = os.path.join(os.getcwd(), "commodore64 games")
            
            for file in game_files:
                title, ext = os.path.splitext(file)
                new_base_name = remove_version_region_info(title)
                new_file = new_base_name + ext
                
                if os.path.exists(os.path.join(commodore64_folder, new_file)):
                    print(f"File '{new_file}' already exists. Skipping rename for '{file}'.")
                else:
                    try:
                        os.rename(os.path.join(commodore64_folder, file), os.path.join(commodore64_folder, new_file))
                        print(f"Renamed '{file}' to '{new_file}'")
                    except Exception as e:
                        print(f"Failed to rename '{file}' to '{new_file}': {e}")

            print("\n\n\nAll Done! I did my best to remove what I could.\n\n\n")

        print("\n\nWould you like to reference the text list made by Below Average Gaming to rename your games too? (yes/no): ")
        
        answer = input().strip().lower()

        if answer == 'yes':
            txt_files = list_txt_files()
            if txt_files:
                print("Here are the text files in the 'commodore64 plain text names' folder:")
                for file in txt_files:
                    print(file)

                print("\n\n\n")
                answer = input("Would you like to match the names above to your Commodore 64 games and then rename them? (yes/no): ").strip().lower()

                if answer == 'yes':
                    commodore64_folder = os.path.join(os.getcwd(), "commodore64 games")
                    matches = []
                    already_matched = set()
                    while True:
                        changes_made = False
                        game_files = list_commodore64_games()
                        for game_file in game_files:
                            if game_file in already_matched:
                                continue
                            game_name, _ = os.path.splitext(game_file)
                            best_match = find_best_match(game_name, txt_files)
                            if best_match:
                                matches.append((game_file, best_match))
                                new_file_name = os.path.splitext(best_match)[0] + os.path.splitext(game_file)[1]
                                if os.path.exists(os.path.join(commodore64_folder, new_file_name)):
                                    print(f"File '{new_file_name}' already exists. Skipping rename for '{game_file}'.")
                                else:
                                    try:
                                        os.rename(os.path.join(commodore64_folder, game_file), os.path.join(commodore64_folder, new_file_name))
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

                    print("\n\n\nYour Commodore 64 games have been renamed!\n\n\n")
                    answer = input("Would you like to start working on your boxart now? (yes/no): ").strip().lower()

                    if answer == 'yes':
                        art_files = list_cover_art_files()
                        if art_files:
                            answer = input("First thing we should do is remove all of the version information from the boxart titles. Sound good? (yes/no): ").strip().lower()

                            if answer == 'yes':
                                art_folder = os.path.join(os.getcwd(), "commodore64 cover art")
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

                                art_files = list_cover_art_files()  # Refresh list after renaming

                            matched_files = transfer_matching_cover_art(game_files, art_files)
                
                            # Handle unmatched files
                            unmatched_games = set(game_files) - matched_files
                            excluded_patterns = [
                                r'\(Disk \d+\)',
                                r'\(Disk \d+ Side [A-C]\)',
                                r'\(Side [A-C]\)',
                                r'\[Disk \d+\]',
                                r'\[Side [A-C]\]'
                            ]

                            def should_exclude(game_file):
                                for pattern in excluded_patterns:
                                    if re.search(pattern, game_file, re.IGNORECASE):
                                        return True
                                return False

                            if unmatched_games:
                                unmatched_folder = os.path.join(os.getcwd(), 'unmatched games')
                                if not os.path.exists(unmatched_folder):
                                    os.makedirs(unmatched_folder)

                                for game_file in unmatched_games:
                                    if should_exclude(game_file):
                                        print(f"\nExcluding from unmatched: {game_file}")
                                        continue
                                    print(f"\nNo match found for: {game_file}. Moving to 'unmatched games' folder.")
                                    shutil.move(os.path.join(os.getcwd(), 'commodore64 games', game_file), os.path.join(unmatched_folder, game_file))

                                # Perform the disk/side info check and renaming
                                match_and_rename_cover_art_with_disk_info(game_files, art_files)

    print("\n\n\nAll Done!")
    print("This tool was created by Below Average Gaming!")
    
    ascii_art = """
d8888b.  .d8b.  d888888b                                                                         
88  `8D d8' `8b `~~88~~'                                                                         
88   88 88ooo88    88                                                                            
88   88 88~~~88    88                                                                            
88  .8D 88   88    88                                                                            
Y8888D' YP   YP    YP                                                                            
                                                                                                 
                                                                                                 
 .o88b.  .d88b.  .88b  d88. .88b  d88.  .d88b.  d8888b.  .d88b.  d8888b. d88888b    dD     j88D  
d8P  Y8 .8P  Y8. 88'YbdP`88 88'YbdP`88 .8P  Y8. 88  `8D .8P  Y8. 88  `8D 88'       d8'    j8~88  
8P      88    88 88  88  88 88  88  88 88    88 88   88 88    88 88oobY' 88ooooo  d8'    j8' 88  
8b      88    88 88  88  88 88  88  88 88    88 88   88 88    88 88`8b   88~~~~~ d8888b. V88888D 
Y8b  d8 `8b  d8' 88  88  88 88  88  88 `8b  d8' 88  .8D `8b  d8' 88 `88. 88.     88' `8D     88  
 `Y88P'  `Y88P'  YP  YP  YP YP  YP  YP  `Y88P'  Y8888D'  `Y88P'  88   YD Y88888P `8888P      VP  
                                                                                                 
                                                                                                 
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
"""

    print(ascii_art)

    print("Press Enter to exit...")
    input()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")
