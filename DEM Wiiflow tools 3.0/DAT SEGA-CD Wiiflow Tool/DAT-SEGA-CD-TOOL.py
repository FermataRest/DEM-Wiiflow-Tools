import os
import shutil
import re
from difflib import get_close_matches

def find_files(directory, extensions):
    matches = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(extensions):
                matches.append(os.path.join(root, filename))
    return matches

def display_txt_files(directory, text_list_name):
    # Simply list the .txt files without renaming
    txt_files = [f for f in os.listdir(directory) if f.lower().endswith('.txt')]
    print(f"Found the following .txt files in '{text_list_name}':")
    for file in txt_files:
        print(file)
    return txt_files

def get_txt_base_names(directory, text_list_name):
    txt_files = display_txt_files(directory, text_list_name)
    base_names = [os.path.splitext(f)[0] for f in txt_files]
    return base_names

def normalize_name(name):
    name = re.sub(r'\(.*?\)', '', name).strip()
    return re.sub(r'[^a-zA-Z0-9]', '', name).lower()

def extract_disc_cd_info(name):
    name = re.sub(r'\[CD(\d+)\]', r'(Disc \1)', name)
    disc_info = re.search(r'\(Disc (\d+)\)', name)
    if disc_info:
        return f"(Disc {disc_info.group(1)})"
    return ''

def find_closest_match(source_name, target_files):
    normalized_source = normalize_name(source_name)
    normalized_targets = [normalize_name(target) for target in target_files]

    print(f"DEBUG: Matching '{source_name}' (normalized: '{normalized_source}') against:")
    for target, normalized_target in zip(target_files, normalized_targets):
        print(f"DEBUG: - '{target}' (normalized: '{normalized_target}')")

    matches = get_close_matches(normalized_source, normalized_targets, n=1, cutoff=0.6)
    if matches:
        print(f"DEBUG: Closest match found: '{matches[0]}'\n")
        return target_files[normalized_targets.index(matches[0])]
    else:
        print("DEBUG: No close match found.\n")
    return None

def rename_files(source_files, target_files, output_dir, excluded_files):
    if not os.path.exists(output_dir):
        print(f"DEBUG: Creating output directory: {output_dir}")
        os.makedirs(output_dir)

    for src in source_files:
        base_src = os.path.splitext(os.path.basename(src))[0]
        if base_src in excluded_files:
            print(f"Skipping {src} as it was already renamed by special_names.")
            continue

        # Extract disc information if present
        disc_cd_info = extract_disc_cd_info(base_src)

        # Find the closest match in the target files
        closest_match = find_closest_match(base_src, target_files)

        if closest_match:
            # Remove any existing disc information from the matched name
            matched_name = os.path.splitext(closest_match)[0]
            matched_name_clean = re.sub(r'\s*\(Disc \d+\)', '', matched_name)  # Remove any existing disc info

            # Construct the new name
            new_name = f"{matched_name_clean} {disc_cd_info}".strip() + ".bin.png"

            # Remove any redundant spaces before the parentheses
            new_name = re.sub(r'\s+\((Disc \d+)\)', r'(\1)', new_name)

            new_path = os.path.join(output_dir, new_name)
            print(f"DEBUG: Copying {src} to {new_path}")
            shutil.copy(src, new_path)
            print(f"Copied: {src} -> {new_name}")
        else:
            print(f"No match found for: {src}")

def list_image_files(directory):
    if not os.path.exists(directory):
        print(f"DEBUG: Directory not found: {directory}")
        return []
    
    matches = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(('.png', '.jpeg', '.jpg')):
                matches.append(os.path.join(root, filename))
    return matches

def list_txt_files(directory):
    if not os.path.exists(directory):
        print(f"DEBUG: Directory not found: {directory}")
        return []
    
    return [os.path.splitext(f)[0] for f in os.listdir(directory) if f.lower().endswith('.txt')]

def clean_name(name):
    cleaned_name = re.sub(r'[^A-Za-z0-9\s]', '', name).lower()
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name)
    return cleaned_name.strip()

def find_closest_matches(bin_cue_files, txt_base_names, excluded_files):
    matches = []
    threshold = 0.8  # Adjust the similarity threshold as needed
    for file in bin_cue_files:
        if file in excluded_files:
            continue  # Skip files that were renamed by special_names()

        file_dir, file_name = os.path.split(file)
        base_name, ext = os.path.splitext(file_name)

        # Extract and preserve disc information if present
        disc_info = extract_disc_cd_info(base_name)
        base_name = re.sub(r'\(Disc \d+\)', '', base_name).strip()  # Remove disc info for matching

        # Normalize the name by removing any other unwanted characters
        base_name_normalized = normalize_name(base_name)

        # Attempt an exact match first
        exact_matches = [name for name in txt_base_names if normalize_name(name) == base_name_normalized]
        if exact_matches:
            new_name = (exact_matches[0] + disc_info + ext).replace('  ', ' ').strip()  # Reattach disc info
            new_name = re.sub(r'\s+', ' ', new_name)  # Replace double spaces with single space
            matches.append((file, new_name))
            continue

        # If no exact match is found, find the closest match
        closest_match = get_close_matches(base_name_normalized, [normalize_name(name) for name in txt_base_names], n=1, cutoff=threshold)
        if closest_match:
            match_base_name = txt_base_names[[normalize_name(name) for name in txt_base_names].index(closest_match[0])]
            new_name = (match_base_name + disc_info + ext).replace('  ', ' ').strip()  # Reattach disc info
            new_name = re.sub(r'\s+', ' ', new_name)  # Replace double spaces with single space
            matches.append((file, new_name))
    return matches

def fix_multiple_disc_titles(renamed_dir, games_dir):
    renamed_files = os.listdir(renamed_dir)
    disc_games = [f for f in os.listdir(games_dir) if any(f.endswith(ext) for ext in ['(Disc 1)', '(Disc 2)', '(Disc 3)', '(Disc 4)'])]

    processed_files = set()

    for game in disc_games:
        base_name, disc_info = os.path.splitext(game)[0].rsplit(' ', 1)
        closest_match = find_closest_match(base_name, renamed_files)
        if closest_match:
            src_path = os.path.join(renamed_dir, closest_match)
            ext = os.path.splitext(closest_match)[1]

            base_name_cleaned = re.sub(r'\((?!Disc \d\))[^)]*\)', '', base_name).strip()

            new_name = f"{base_name_cleaned} {disc_info}.bin.png"
            new_name = re.sub(r'\s+\((Disc \d+)\)', r'(\1)', new_name)
            new_path = os.path.join(renamed_dir, new_name)
            
            if new_path not in processed_files and not os.path.exists(new_path):
                print(f"DEBUG: Copying {src_path} to {new_path}")
                shutil.copy(src_path, new_path)
                print(f"Copied: {src_path} -> {new_name}")
                processed_files.add(new_path)

    cleanup_base_files(renamed_dir, disc_games)

def cleanup_base_files(renamed_dir, disc_games):
    for game in disc_games:
        base_name = re.sub(r' \(Disc \d\)$', '', game)
        base_file_path = os.path.join(renamed_dir, f"{base_name}.bin.png")
        
        if os.path.exists(base_file_path):
            print(f"DEBUG: Deleting base title file {base_file_path}")
            os.remove(base_file_path)
            print(f"Deleted: {base_file_path}")
        else:
            print(f"DEBUG: Base title file not found for deletion: {base_file_path}")

def remove_spaces_before_parentheses(directory):
    for filename in os.listdir(directory):
        if "(Disc" in filename:
            new_filename = re.sub(r'\s+\((Disc \d+)\)', r'(\1)', filename)
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            if old_path != new_path and not os.path.exists(new_path):
                print(f"DEBUG: Renaming {old_path} to {new_path}")
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")

def special_names():
    renamed_files = []
    try:
        sega_cd_folder = os.path.join(os.getcwd(), "sega-cd games")
        if not os.path.exists(sega_cd_folder):
            print('The "sega-cd games" folder does not exist.')
            return renamed_files
        
        specific_renames = {
            "3 Ninjas Kick Back": "3 Ninjas Kick Back",
            "A-X-101": "AX-101",
            "AH3 - Thunderstrike": "AH-3 Thunderstrike",
            "Adventures of Batman and Robin, The": "Adventures of Batman & Robin, The",
            "Adventures of Willy Beamish, The": "Adventures of Willy Beamish, The",
            "After Burner III": "After Burner III",
            "Amazing Spider-Man vs. The Kingpin, The": "Amazing Spider-Man vs. The Kingpin, The",
            "Android Assault - The Revenge of Bari-Arm": "Android Assault - The Revenge of Bari-Arm",
            "BC Racers": "BC Racers",
            "Batman Returns": "Batman Returns",
            "Battlecorps": "Battlecorps",
            "Bill Walsh College Football": "Bill Walsh College Football",
            "Blackhole Assault": "Blackhole Assault",
            "Bouncers": "Bouncers",
            "Bram Stoker's Dracula": "Bram Stoker's Dracula",
            "Brutal - Paws of Fury": "Brutal - Paws of Fury",
            "Championship Soccer '94": "Championship Soccer '94",
            "Chuck Rock": "Chuck Rock",
            "Chuck Rock II - Son of Chuck": "Chuck Rock II - Son of Chuck",
            "Cliffhanger": "Cliffhanger",
            "Cobra Command": "Cobra Command",
            "Colors of Modern Rock, The": "Virtual VCR Colors of Modern Rock, The",
            "Compton's Interactive Encyclopedia": "Compton's Interactive Encyclopedia",
            "Corpse Killer": "Corpse Killer",
            "Crime Patrol": "Crime Patrol",
            "Dark Wizard": "Dark Wizard",
            "Demolition Man": "Demolition Man",
            "Double Switch": "Double Switch",
            "Dracula Unleashed (Disc 1)": "Dracula Unleashed",
            "Dracula Unleashed (Disc 2)": "Dracula Unleashed",
            "Dragon's Lair": "Dragon's Lair",
            "Dune": "Dune",
            "Dungeon Explorer": "Dungeon Explorer",
            "Dungeon Master II - Skullkeep": "Dungeon Master II - Skullkeep",
            "ESPN Baseball Tonight": "ESPN Baseball Tonight",
            "ESPN NBA Hangtime '95": "ESPN NBA Hangtime '95",
            "ESPN National Hockey Night": "ESPN National Hockey Night",
            "ESPN Sunday Night NFL": "ESPN Sunday Night NFL",
            "Earthworm Jim - Special Edition": "Earthworm Jim - Special Edition",
            "Ecco - The Tides of Time": "Ecco The Tides of Time",
            "Ecco the Dolphin": "Ecco the Dolphin",
            "Eternal Champions - Challenge from the Dark Side": "Eternal Champions - Challenge from the Dark Side",
            "Eye of the Beholder": "Eye of the Beholder",
            "FIFA International Soccer": "FIFA International Soccer",
            "Fahrenheit (Disc 1)": "Fahrenheit",
            "Fahrenheit (Disc 2)": "Fahrenheit",
            "Fatal Fury Special": "Fatal Fury Special",
            "Final Fight CD": "Final Fight CD",
            "Flashback - The Quest for Identity": "Flashback - The Quest for Identity",
            "Flink": "Flink",
            "Formula One World Championship - Beyond the Limit": "Formula One World Championship - Beyond the Limit",
            "Ground Zero Texas (Disc 1)": "Ground Zero Texas",
            "Ground Zero Texas (Disc 2)": "Ground Zero Texas",
            "Heart of the Alien - Out of This World Parts I and II": "Heart of the Alien - Out of This World Parts I and II",
            "Heimdall": "Heimdall",
            "Hook": "Hook",
            "Iron Helix": "Iron Helix",
            "Jaguar XJ220": "Jaguar XJ220",
            "Jeopardy!": "Jeopardy!",
            "Joe Montana's NFL Football": "Joe Montana's NFL Football",
            "Jurassic Park": "Jurassic Park",
            "Keio Flying Squadron": "Keio Flying Squadron",
            "Kids on Site": "Kids on Site",
            "Lawnmower Man, The": "Lawnmower Man, The",
            "Lethal Enforcers": "Lethal Enforcers",
            "Lethal Enforcers II - Gun Fighters": "Lethal Enforcers II - Gun Fighters",
            "Links - The Challenge of Golf": "Links - The Challenge of Golf",
            "Lords of Thunder": "Lords of Thunder",
            "Lunar - Eternal Blue": "Lunar - Eternal Blue",
            "Lunar - The Silver Star": "Lunar - The Silver Star",
            "Mad Dog II - The Lost Gold": "Mad Dog II - The Lost Gold",
            "Mad Dog McCree": "Mad Dog McCree",
            "Make My Video - INXS": "Make My Video - INXS",
            "Make My Video - Kris Kross": "Make My Video - Kris Kross",
            "Make My Video - Marky Mark and the Funky Bunch": "Make My Video - Marky Mark and The Funky Bunch",
            "Mansion of Hidden Souls": "Mansion of Hidden Souls",
            "Mary Shelley's Frankenstein": "Mary Shelley's Frankenstein",
            "Masked Rider, The - Kamen Rider ZO": "Masked Rider, The - Kamen Rider ZO",
            "MegaRace": "MegaRace",
            "Mickey Mania - The Timeless Adventures of Mickey Mouse": "Mickey Mania - The Timeless Adventures of Mickey Mouse",
            "Microcosm": "Microcosm",
            "Midnight Raiders": "Midnight Raiders",
            "Mighty Morphin Power Rangers": "Mighty Morphin Power Rangers",
            "Mortal Kombat": "Mortal Kombat",
            "NBA Jam": "NBA Jam",
            "NFL Football Trivia Challenge": "NFL Football Trivia Challenge",
            "NFL's Greatest - San Francisco vs. Dallas 1978-1993": "NFL's Greatest - San Francisco vs. Dallas 1978-1993",
            "NHL '94": "NHL '94",
            "Night Trap (Disc 1)": "Night Trap",
            "Night Trap (Disc 2)": "Night Trap",
            "Novastorm": "Novastorm",
            "Panic!": "Panic!",
            "Pitfall - The Mayan Adventure": "Pitfall - The Mayan Adventure",
            "Popful Mail": "Popful Mail",
            "Power Monger": "Power Monger",
            "Prince of Persia": "Prince of Persia",
            "Prize Fighter (Disc 1)": "Prize Fighter",
            "Prize Fighter (Disc 2)": "Prize Fighter",
            "Puggsy": "Puggsy",
            "RDF - Global Conflict": "RDF - Global Conflict",
            "Racing Aces": "Racing Aces",
            "Radical Rex": "Radical Rex",
            "Revenge of the Ninja": "Revenge of the Ninja",
            "Revengers of Vengeance": "Revengers of Vengeance",
            "Rise of the Dragon": "Rise of the Dragon",
            "Road Avenger": "Road Avenger",
            "Road Rash": "Road Rash",
            "Robo Aleste": "Robo Aleste",
            "Samurai Shodown": "Samurai Shodown",
            "Secret of Monkey Island, The": "Secret of Monkey Island, The",
            "Sega Classics Arcade Collection": "Sega Classics Arcade Collection",
            "Sewer Shark": "Sewer Shark",
            "Shadow of the Beast II": "Shadow of the Beast II",
            "Sherlock Holmes - Consulting Detective": "Sherlock Holmes - Consulting Detective",
            "Sherlock Holmes - Consulting Detective Vol. II (Disc 1)": "Sherlock Holmes - Consulting Detective Vol. II",
            "Sherlock Holmes - Consulting Detective Vol. II (Disc 2)": "Sherlock Holmes - Consulting Detective Vol. II",
            "Shining Force CD": "Shining Force CD",
            "Silpheed": "Silpheed",
            "Slam City with Scottie Pippen (Disc 1)": "Slam City with Scottie Pippen",
            "Slam City with Scottie Pippen (Disc 2)": "Slam City with Scottie Pippen",
            "Slam City with Scottie Pippen (Disc 3)": "Slam City with Scottie Pippen",
            "Slam City with Scottie Pippen (Disc 4)": "Slam City with Scottie Pippen",
            "Snatcher": "Snatcher",
            "Software Toolworks' Star Wars Chess, The": "Software Toolworks' Star Wars Chess, The",
            "Sol-Feace": "Sol-Feace",
            "Sonic CD": "Sonic CD",
            "Sonic MegaMix": "Sonic MegaMix",
            "SoulStar": "SoulStar",
            "Space Ace": "Space Ace",
            "Space Adventure, The - Cobra - The Legendary Bandit": "Space Adventure, The - Cobra - The Legendary Bandit",
            "Star Wars - Rebel Assault": "Star Wars Rebel Assault",
            "Starblade": "Starblade",
            "Stellar-Fire": "Stellar-Fire",
            "Supreme Warrior (Disc 1)": "Supreme Warrior",
            "Supreme Warrior (Disc 2)": "Supreme Warrior",
            "Surgical Strike": "Surgical Strike",
            "Terminator, The": "Terminator, The",
            "Third World War": "Third World War"
        }

        for file in os.listdir(sega_cd_folder):
            base_name, ext = os.path.splitext(file)
            disc_info = extract_disc_cd_info(base_name)  # Extract (Disc X) information if present
            base_name_without_disc = re.sub(r'\(Disc \d+\)', '', base_name).strip()  # Remove (Disc X) to match with specific_renames

            if base_name_without_disc in specific_renames:
                new_base_name = specific_renames[base_name_without_disc]

                # Construct the new name with the disc info
                new_file_name = f"{new_base_name} {disc_info}".strip() + ext
                new_file_name = re.sub(r'\s+\((Disc \d+)\)', r'(\1)', new_file_name)  # Ensure no extra space before (Disc X)
                os.rename(os.path.join(sega_cd_folder, file), os.path.join(sega_cd_folder, new_file_name))
                renamed_files.append(os.path.join(sega_cd_folder, new_file_name))  # Track the renamed files with their full path

    except Exception as e:
        print(f"Error in special_names: {e}")

    return renamed_files

def fix_specific_title(output_dir):
    old_name = "Amazing Spider-Man vs.bin.png"
    new_name = "Amazing Spider-Man vs. The Kingpin, The.bin.png"
    
    old_path = os.path.join(output_dir, old_name)
    new_path = os.path.join(output_dir, new_name)
    
    if os.path.exists(old_path):
        print(f"DEBUG: Renaming {old_path} to {new_path}")
        os.rename(old_path, new_path)
        print(f"Renamed: {old_name} -> {new_name}")
    else:
        print(f"DEBUG: {old_name} not found in {output_dir}")

def main():
    try:
        print("Thank you for using this Sega-CD tool! Let me find your games for you.")
        input("Press Enter to continue...")

        # Call special_names function at the start
        excluded_files = special_names()

        script_dir = os.path.dirname(os.path.abspath(__file__))
        extensions = ('.bin', '.cue')
        found_files = find_files(script_dir, extensions)

        if found_files:
            print("Found the following files:")
            for file in found_files:
                print(file)
        else:
            print("No .bin or .cue files found.")

        while True:
            print("\n" * 3)
            response = input("Do you want to continue and reference the text list? (yes/no): ").strip().lower()
            if response == 'yes':
                print("\n" * 3 + "Continuing the script and referencing the text list...")
                txt_dir = os.path.join(script_dir, 'sega-cd cue file names')
                text_list_name = 'sega-cd cue file names'
                if os.path.exists(txt_dir) and os.path.isdir(txt_dir):
                    txt_base_names = get_txt_base_names(txt_dir, text_list_name)
                    print("\n" * 3)
                    fix_response = input("Would you like to fix the .bin and .cue files? (yes/no): ").strip().lower()
                    if fix_response == 'yes':
                        matches = find_closest_matches(found_files, txt_base_names, excluded_files)
                        if matches:
                            print("The following files will be matched:")
                            for original, new in matches:
                                print(f"{original} -> {new}")
                            print("\n" * 3)
                            confirm_fix = input("Do you really want to fix these names? (yes/no): ").strip().lower()
                            if confirm_fix == 'yes':
                                for original, new in matches:
                                    original_dir, original_file = os.path.split(original)
                                    new_path = os.path.join(original_dir, new)
                                    os.rename(original, new_path)
                                print("\n" * 5 + "The names have been fixed.")
                            else:
                                print("No changes were made to the .bin and .cue files.")
                        else:
                            print("No close matches found for the .bin and .cue files.")
                    else:
                        print("No changes were made to the .bin and .cue files.")
                else:
                    print("'sega-cd cue file names' directory does not exist.")
                break
            elif response == 'no':
                print("Exiting the script.")
                break

        print("This tool was created by Below Average Gaming.")
        print(r"""
d8888b.  .d8b.  d888888b                                               
88  `8D d8' `8b `~~88~~'                                               
88   88 88ooo88    88                                                  
88   88 88~~~88    88                                                  
88  .8D 88   88    88                                                  
Y8888D' YP   YP    YP                                                  
                                                                       
                                                                       
.d8888. d88888b  d888b   .d8b.        .o88b. d8888b.                   
88'  YP 88'     88' Y8b d8' `8b      d8P  Y8 88  `8D                   
`8bo.   88ooooo 88      88ooo88      8P      88   88                   
  `Y8b. 88~~~~~ 88  ooo 88~~~88      8b      88   88                   
db   8D 88.     88. ~8~ 88   88      Y8b  d8 88  .8D                   
`8888Y' Y88888P  Y888P  YP   YP       `Y88P' Y8888D'                   
                                                                       
                                                                       
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

        print("\n" * 3)
        work_on_box_art = input("Would you like to start working on your box art now? (yes/no): ").strip().lower()

        if work_on_box_art == 'yes':
            convert_images = input("Do you want to convert the images? (yes/no): ").strip().lower()
            if convert_images != 'yes':
                print("No images were converted.")
                return

            source_dir = os.path.join(script_dir, 'sega-cd cover art')
            target_dir = os.path.join(script_dir, 'sega-cd cue file names')
            output_dir = os.path.join(script_dir, 'renamed cover art')
            games_dir = os.path.join(script_dir, 'sega-cd games')

            if not os.path.isdir(source_dir) or not os.path.isdir(target_dir):
                print("One or both of the required directories do not exist in the script's location.")
                return

            txt_files = list_txt_files(target_dir)
            if not txt_files:
                print("No .txt files found in the 'sega-cd cue file names' directory.")
                return

            print("Found the following .txt files in 'sega-cd cue file names':")
            for file in txt_files:
                print(file)

            print("\n\n\nDo you want to proceed with the conversion based on these .txt files? (yes/no):", end="")
            proceed = input(" ").strip().lower()
            if proceed != 'yes':
                print("Conversion aborted.")
                return

            source_files = list_image_files(source_dir)
            if not source_files:
                print("No image files found in the 'sega-cd cover art' directory.")
                return

            rename_files(source_files, txt_files, output_dir, excluded_files)
            print(f"Files have been copied and renamed to the new directory: {output_dir}")
            
            # Fix the specific title after renaming
            fix_specific_title(output_dir)

            print("\n\n\nWould you like to fix box art titles for games that have multiple discs? (yes/no):", end="")
            fix_discs = input(" ").strip().lower()
            if fix_discs == 'yes':
                if not os.path.isdir(games_dir):
                    print("The 'sega-cd games' directory does not exist in the script's location.")
                    return
                fix_multiple_disc_titles(output_dir, games_dir)
                print("Multiple disc titles have been processed.")

            remove_spaces_before_parentheses(output_dir)
            print("Spaces before parentheses in disc titles have been removed.")

            print("\n\nThis tool was created by Below Average Gaming.")
            print(r"""
d8888b.  .d8b.  d888888b                                               
88  `8D d8' `8b `~~88~~'                                               
88   88 88ooo88    88                                                  
88   88 88~~~88    88                                                  
88  .8D 88   88    88                                                  
Y8888D' YP   YP    YP                                                  
                                                                       
                                                                       
.d8888. d88888b  d888b   .d8b.        .o88b. d8888b.                   
88'  YP 88'     88' Y8b d8' `8b      d8P  Y8 88  `8D                   
`8bo.   88ooooo 88      88ooo88      8P      88   88                   
  `Y8b. 88~~~~~ 88  ooo 88~~~88      8b      88   88                   
db   8D 88.     88. ~8~ 88   88      Y8b  d8 88  .8D                   
`8888Y' Y88888P  Y888P  YP   YP       `Y88P' Y8888D'                   
                                                                       
                                                                       
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

            input("Press any button to exit...")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press any button to exit...")

if __name__ == "__main__":
    main()
