import os
import time
import re
import difflib

def list_game_watch_games():
    game_watch_folder = os.path.join(os.getcwd(), "game&watch games")
    if not os.path.exists(game_watch_folder):
        print('The "game&watch games" folder does not exist.')
        return False
    mgw_files = [f for f in os.listdir(game_watch_folder) if f.endswith('.mgw')]

    if not mgw_files:
        print('No .mgw files present in the "game&watch games" folder.')
        time.sleep(5)
        return False

    return mgw_files

def remove_version_region_info(filename):
    new_filename = re.sub(r'[\(\[].*?[\)\]]', '', filename)
    return new_filename.strip()

def list_txt_files():
    txt_folder = os.path.join(os.getcwd(), "game&watch plain text names")
    if not os.path.exists(txt_folder):
        print('The "game&watch plain text names" folder does not exist.')
        return False
    txt_files = [f for f in os.listdir(txt_folder) if f.endswith('.txt')]

    if not txt_files:
        print('No .txt files present in the "game&watch plain text names" folder.')
        return False

    return txt_files

def list_cover_art_files():
    art_folder = os.path.join(os.getcwd(), "game&watch cover art")
    if not os.path.exists(art_folder):
        print('The "game&watch cover art" folder does not exist.')
        return False

    art_files = []
    for root, dirs, files in os.walk(art_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpeg', '.jpg')):
                art_files.append(os.path.join(root, file))

    if not art_files:
        print('No cover art files present in the "game&watch cover art" folder.')
        return False

    return art_files

def find_best_match(game_name, file_names):
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

def main():
    print("Thank you for using DAT Game&Watch Wiiflow Tool!")
    answer = input("Would you like to see your listed Game&Watch games? (yes/no): ").strip().lower()

    if answer == 'yes':
        mgw_files = list_game_watch_games()
        if mgw_files:
            print("Here are your Game&Watch games:")
            for file in mgw_files:
                print(file)
            print("\n\n\nThese are the games I picked up!")
        else:
            print("No .mgw files present in the 'game&watch games' folder.")
            time.sleep(5)
            return
    else:
        print("Too Bad, So Sad...")
        time.sleep(3)
        mgw_files = list_game_watch_games()
        if mgw_files:
            print("Here are your Game&Watch games:")
            for file in mgw_files:
                print(file)
            print("\n\n\nThese are the games I picked up!")
        else:
            print("No .mgw files present in the 'game&watch games' folder.")
            time.sleep(5)
            return

    if mgw_files:
        print("\n\n")
        
        answer = input("Would you like to remove the version and region information from the title names?\nExample: 'Donkey Kong (USA).mgw' would be changed to 'Donkey Kong.mgw'\nYes or no? ").strip().lower()

        if answer == 'yes':
            game_watch_folder = os.path.join(os.getcwd(), "game&watch games")
            for file in mgw_files:
                base_name, ext = os.path.splitext(file)
                new_base_name = remove_version_region_info(base_name)
                new_file = new_base_name + ext
                
                if os.path.exists(os.path.join(game_watch_folder, new_file)):
                    print(f"File '{new_file}' already exists. Skipping rename for '{file}'.")
                else:
                    try:
                        os.rename(os.path.join(game_watch_folder, file), os.path.join(game_watch_folder, new_file))
                        print(f"Renamed '{file}' to '{new_file}'")
                    except Exception as e:
                        print(f"Failed to rename '{file}' to '{new_file}': {e}")
            
            print("\n\n\nAll Done! I did my best to remove what I could.\n\n\n")
        
        answer = input("Would you like to reference the text list made by Below Average Gaming to rename your games too? (yes/no): ").strip().lower()

        if answer == 'yes':
            txt_files = list_txt_files()
            if txt_files:
                print("Here are the text files in the 'game&watch plain text names' folder:")
                for file in txt_files:
                    print(file)
                
                print("\n\n\n")
                answer = input("Would you like to match the names above to your Game&Watch games and then rename them? (yes/no): ").strip().lower()

                if answer == 'yes':
                    game_watch_folder = os.path.join(os.getcwd(), "game&watch games")
                    matches = []
                    already_matched = set()  # Track already matched files
                    while True:
                        changes_made = False
                        mgw_files = list_game_watch_games()  # Update the list of mgw files
                        for game_file in mgw_files:
                            if game_file in already_matched:
                                continue  # Skip already matched files
                            game_name, _ = os.path.splitext(game_file)
                            best_match = find_best_match(game_name, txt_files)
                            if best_match:
                                matches.append((game_file, best_match))
                                new_file_name = os.path.splitext(best_match)[0] + ".mgw"
                                if os.path.exists(os.path.join(game_watch_folder, new_file_name)):
                                    print(f"File '{new_file_name}' already exists. Skipping rename for '{game_file}'.")
                                else:
                                    try:
                                        os.rename(os.path.join(game_watch_folder, game_file), os.path.join(game_watch_folder, new_file_name))
                                        print(f"Matched '{game_file}' to '{best_match}' and renamed to '{new_file_name}'")
                                        changes_made = True
                                        already_matched.add(new_file_name)
                                    except Exception as e:
                                        print(f"Failed to rename '{game_file}' to '{new_file_name}': {e}")
                        if not changes_made:
                            break  # Stop if no changes were made in the current iteration

                    if matches:
                        print("\nMatched and renamed files:")
                        for match in matches:
                            print(f"{match[0]} -> {match[1]}")

                    print("\n\n\nYour Game&Watch games have been renamed!\n\n\n")
                    answer = input("Would you like to start working on your boxart now? (yes/no): ").strip().lower()

                    if answer == 'yes':
                        art_files = list_cover_art_files()
                        if art_files:
                            answer = input("First thing we should do is remove all of the version information from the boxart titles. Sound good? (yes/no): ").strip().lower()

                            if answer == 'yes':
                                art_folder = os.path.join(os.getcwd(), "game&watch cover art")
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

                                # Refresh the art_files list after renaming
                                art_files = list_cover_art_files()

                            print("\n\n\nGreat! Now that that's out of the way, This is the boxart that I found! You should probably rename this as well... Want to rename them? (yes/no): ")
                            answer = input().strip().lower()

                            if answer == 'yes':
                                renamed_folder = os.path.join(os.getcwd(), "renamed cover art")
                                if not os.path.exists(renamed_folder):
                                    os.makedirs(renamed_folder)
                                art_matches = []
                                mgw_file_titles = [os.path.splitext(f)[0] for f in mgw_files]
                                already_matched_art = set()  # Track already matched art files
                                while True:
                                    changes_made = False
                                    for art_file in art_files:
                                        if art_file in already_matched_art:
                                            continue  # Skip already matched files
                                        art_file_title = os.path.splitext(os.path.basename(art_file))[0]
                                        best_match = find_best_match(art_file_title, mgw_file_titles)
                                        if best_match:
                                            art_matches.append((best_match + ".mgw", art_file))
                                            changes_made = True
                                            already_matched_art.add(art_file)
                                            print(f"Matched '{art_file}' to '{best_match}'")  # Debugging print
                                    if not changes_made:
                                        break  # Stop if no changes were made in the current iteration

                                if art_matches:
                                    for game_file, art_file in art_matches:
                                        game_base, _ = os.path.splitext(game_file)
                                        # Remove "()" and their contents from new art name
                                        new_art_name = re.sub(r'\(.*?\)', '', game_base).strip() + ".mgw.png"
                                        new_art_path = os.path.join(renamed_folder, new_art_name)
                                        
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

                                # Handle files that were not matched
                                unmatched_art_files = [file for file in art_files if file not in already_matched_art]
                                if unmatched_art_files:
                                    print("The following art files were not matched and transferred:")
                                    for file in unmatched_art_files:
                                        # Move unmatched files to renamed folder as well
                                        new_art_name = os.path.basename(file)
                                        new_art_path = os.path.join(renamed_folder, new_art_name)
                                        try:
                                            os.rename(file, new_art_path)
                                            print(f"Moved unmatched art file '{file}' to '{new_art_path}'")
                                        except Exception as e:
                                            print(f"Failed to move '{file}' to '{new_art_path}': {e}")
                                else:
                                    print("All cover art files were successfully matched and transferred.")
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

    print("\n\n\nAll Done!")
    print("This tool was created by Below Average Gaming!")
    print("""
d8888b.  .d8b.  d888888b       d888b   .d8b.  .88b  d88. d88888b       
88  `8D d8' `8b `~~88~~'      88' Y8b d8' `8b 88'YbdP`88 88'           
88   88 88ooo88    88         88      88ooo88 88  88  88 88ooooo       
88   88 88~~~88    88         88  ooo 88~~~88 88  88  88 88~~~~~       
88  .8D 88   88    88         88. ~8~ 88   88 88  88  88 88.           
Y8888D' YP   YP    YP          Y888P  YP   YP YP  YP  YP Y88888P       
                                                                       
                                                                       
.d888b.       db   d8b   db  .d8b.  d888888b  .o88b. db   db           
8P   8D       88   I8I   88 d8' `8b `~~88~~' d8P  Y8 88   88           
`Vb d8'       88   I8I   88 88ooo88    88    8P      88ooo88           
 d88C dD      Y8   I8I   88 88~~~88    88    8b      88~~~88           
C8' d8D       `8b d8'8b d8' 88   88    88    Y8b  d8 88   88           
`888P Yb       `8b8' `8d8'  YP   YP    YP     `Y88P' YP   YP           
                                                                       
                                                                       
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
