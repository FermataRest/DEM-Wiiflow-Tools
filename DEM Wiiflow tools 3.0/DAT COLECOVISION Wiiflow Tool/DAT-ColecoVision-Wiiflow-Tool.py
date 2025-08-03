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

def list_colecovision_games():
    colecovision_folder = os.path.join(os.getcwd(), "colecovision games")
    if not os.path.exists(colecovision_folder):
        print('The "colecovision games" folder does not exist.')
        return False
    col_files = [f for f in os.listdir(colecovision_folder) if f.endswith('.col')]

    if not col_files:
        print('No .col files present in the "colecovision games" folder.')
        time.sleep(5)
        return False

    return col_files

def remove_version_region_info(filename):
    new_filename = re.sub(r'[\(\[].*?[\)\]]', '', filename)
    return new_filename.strip()

def list_txt_files():
    txt_folder = os.path.join(os.getcwd(), "colecovision plain text names")
    if not os.path.exists(txt_folder):
        print('The "colecovision plain text names" folder does not exist.')
        return False
    txt_files = [f for f in os.listdir(txt_folder) if f.endswith('.txt')]

    if not txt_files:
        print('No .txt files present in the "colecovision plain text names" folder.')
        return False

    return txt_files

def list_cover_art_files():
    art_folder = os.path.join(os.getcwd(), "colecovision cover art")
    if not os.path.exists(art_folder):
        print('The "colecovision cover art" folder does not exist.')
        return False

    art_files = []
    for root, dirs, files in os.walk(art_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpeg', '.jpg')):
                art_files.append(os.path.join(root, file))

    if not art_files:
        print('No cover art files present in the "colecovision cover art" folder.')
        return False

    return art_files

def find_best_match(game_name, file_names):
    def clean_name(name):
        name = re.sub(r'[\(\[].*?[\)\]]', '', name)
        return re.sub(r'[^A-Za-z0-9 ]+', '', name).lower().strip()

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

def special_names():
    try:
        colecovision_folder = os.path.join(os.getcwd(), "colecovision games")
        
        specific_renames = {
            # Add any specific .col file renames here
            # "example_original_name.col": "example_new_name.col",
        }
        
        for file in os.listdir(colecovision_folder):
            if file in specific_renames:
                new_file_name = specific_renames[file]
                target_path = os.path.join(colecovision_folder, new_file_name)
                
                try:
                    os.rename(os.path.join(colecovision_folder, file), target_path)
                    print(f"Renamed '{file}' to '{new_file_name}'")
                except Exception as e:
                    print(f"Failed to rename '{file}' to '{new_file_name}': {e}")

    except Exception as e:
        print(f"Error in special_names: {e}")

def transfer_matching_cover_art(col_files, art_files):
    renamed_folder = os.path.join(os.getcwd(), "renamed cover art")
    if not os.path.exists(renamed_folder):
        os.makedirs(renamed_folder)

    for col_file in col_files:
        col_file_base = os.path.splitext(col_file)[0]
        for art_file in art_files:
            art_file_base = os.path.splitext(os.path.basename(art_file))[0]
            if art_file_base.lower() == col_file_base.lower():
                new_art_name = f"{col_file_base}.col.png"
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
    print("Thank you for using DAT ColecoVision Wiiflow Tool!")
    answer = input("Would you like to see your listed ColecoVision games? (yes/no): ").strip().lower()

    if answer == 'yes':
        col_files = list_colecovision_games()
        if col_files:
            print("Here are your ColecoVision games:")
            for file in col_files:
                print(file)
            print("\n\n\nThese are the games I picked up!")
        else:
            print("No .col files present in the 'colecovision games' folder.")
            time.sleep(5)
            return
    else:
        print("Too Bad, So Sad...")
        time.sleep(3)
        col_files = list_colecovision_games()
        if col_files:
            print("Here are your ColecoVision games:")
            for file in col_files:
                print(file)
            print("\n\n\nThese are the games I picked up!")
        else:
            print("No .col files present in the 'colecovision games' folder.")
            time.sleep(5)
            return

    if col_files:
        print("\n\n")
        
        answer = input("Would you like to check for duplicate titles? (yes/no): ").strip().lower()

        if answer == 'yes':
            source_folder = 'colecovision games'
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

        answer = input("Would you like to remove the version and region information from the title names?\nExample: 'Aquattack (USA).col' would be changed to 'Aquattack.col'\nYes or no? ").strip().lower()

        if answer == 'yes':
            colecovision_folder = os.path.join(os.getcwd(), "colecovision games")
            for file in col_files:
                base_name, ext = os.path.splitext(file)
                new_base_name = remove_version_region_info(base_name)
                new_file = new_base_name + ext
                
                if os.path.exists(os.path.join(colecovision_folder, new_file)):
                    print(f"File '{new_file}' already exists. Skipping rename for '{file}'.")
                else:
                    try:
                        os.rename(os.path.join(colecovision_folder, file), os.path.join(colecovision_folder, new_file))
                        print(f"Renamed '{file}' to '{new_file}'")
                    except Exception as e:
                        print(f"Failed to rename '{file}' to '{new_file}': {e}")
            
            print("\n\n\nAll Done! I did my best to remove what I could.\n\n\n")

        special_names()
        
        print("\n\nWould you like to reference the text list made by Below Average Gaming to rename your games too? (yes/no): ")
        
        answer = input().strip().lower()

        if answer == 'yes':
            txt_files = list_txt_files()
            if txt_files:
                print("Here are the text files in the 'colecovision plain text names' folder:")
                for file in txt_files:
                    print(file)
                
                print("\n\n\n")
                answer = input("Would you like to match the names above to your ColecoVision games and then rename them? (yes/no): ").strip().lower()

                if answer == 'yes':
                    colecovision_folder = os.path.join(os.getcwd(), "colecovision games")
                    matches = []
                    already_matched = set()
                    while True:
                        changes_made = False
                        col_files = list_colecovision_games()
                        for game_file in col_files:
                            if game_file in already_matched:
                                continue
                            game_name, _ = os.path.splitext(game_file)
                            best_match = find_best_match(game_name, txt_files)
                            if best_match:
                                matches.append((game_file, best_match))
                                new_file_name = os.path.splitext(best_match)[0] + ".col"
                                if os.path.exists(os.path.join(colecovision_folder, new_file_name)):
                                    print(f"File '{new_file_name}' already exists. Skipping rename for '{game_file}'.")
                                else:
                                    try:
                                        os.rename(os.path.join(colecovision_folder, game_file), os.path.join(colecovision_folder, new_file_name))
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

                    print("\n\n\nYour ColecoVision games have been renamed!\n\n\n")
                    answer = input("Would you like to start working on your boxart now? (yes/no): ").strip().lower()

                    if answer == 'yes':
                        art_files = list_cover_art_files()
                        if art_files:
                            answer = input("First thing we should do is remove all of the version information from the boxart titles. Sound good? (yes/no): ").strip().lower()

                            if answer == 'yes':
                                art_folder = os.path.join(os.getcwd(), "colecovision cover art")
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
                                col_file_titles = [os.path.splitext(f)[0] for f in col_files]
                                already_matched_art = set()
                                while True:
                                    changes_made = False
                                    for art_file in art_files:
                                        if art_file in already_matched_art:
                                            continue
                                        art_file_title = os.path.splitext(os.path.basename(art_file))[0]
                                        best_match = find_best_match(art_file_title, col_file_titles)
                                        if best_match:
                                            art_matches.append((best_match + ".col", art_file))
                                            changes_made = True
                                            already_matched_art.add(art_file)
                                            print(f"Matched '{art_file}' to '{best_match}'")
                                    if not changes_made:
                                        break

                                if art_matches:
                                    for game_file, art_file in art_matches:
                                        game_base, _ = os.path.splitext(game_file)
                                        new_art_name = game_base + ".col.png"
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

                                transfer_matching_cover_art(col_files, art_files)
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
        colecovision_games_folder = 'colecovision games'
        renamed_cover_art_folder = 'renamed cover art'
        unmatched_games_folder = 'unmatched games'

        if not os.path.exists(unmatched_games_folder):
            os.makedirs(unmatched_games_folder)

        colecovision_games = [f for f in os.listdir(colecovision_games_folder) if f.endswith('.col')]
        renamed_cover_art = [f for f in os.listdir(renamed_cover_art_folder) if f.endswith('.col.png')]

        for game in colecovision_games:
            expected_cover_art_name = game + ".png"
            if expected_cover_art_name not in renamed_cover_art:
                print(f"\nNo match found for: {game}. Moving to 'unmatched games' folder.")
                shutil.move(os.path.join(colecovision_games_folder, game), os.path.join(unmatched_games_folder, game))
            else:
                print(f"Match found for: {game}")

    print("\n\n\nAll Done!")
    print("This tool was created by Below Average Gaming!")
    print("""
d8888b.  .d8b.  d888888b                                                                               
88  `8D d8' `8b `~~88~~'                                                                               
88   88 88ooo88    88                                                                                  
88   88 88~~~88    88                                                                                  
88  .8D 88   88    88                                                                                  
Y8888D' YP   YP    YP                                                                                  
                                                                                                       
                                                                                                       
 .o88b.  .d88b.  db      d88888b  .o88b.  .d88b.  db    db d888888b .d8888. d888888b  .d88b.  d8b   db 
d8P  Y8 .8P  Y8. 88      88'     d8P  Y8 .8P  Y8. 88    88   `88'   88'  YP   `88'   .8P  Y8. 888o  88 
8P      88    88 88      88ooooo 8P      88    88 Y8    8P    88    `8bo.      88    88    88 88V8o 88 
8b      88    88 88      88~~~~~ 8b      88    88 `8b  d8'    88      `Y8b.    88    88    88 88 V8o88 
Y8b  d8 `8b  d8' 88booo. 88.     Y8b  d8 `8b  d8'  `8bd8'    .88.   db   8D   .88.   `8b  d8' 88  V888 
 `Y88P'  `Y88P'  Y88888P Y88888P  `Y88P'  `Y88P'     YP    Y888888P `8888Y' Y888888P  `Y88P'  VP   V8P 
                                                                                                       
                                                                                                       
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
