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

def list_gameboy_games():
    gameboy_folder = os.path.join(os.getcwd(), "gba games")
    if not os.path.exists(gameboy_folder):
        print('The "gba games" folder does not exist.')
        return False
    gba_files = [f for f in os.listdir(gameboy_folder) if f.endswith('.gba')]

    if not gba_files:
        print('No .gba files present in the "gba games" folder.')
        time.sleep(5)
        return False

    return gba_files

def remove_version_region_info(filename):
    # This regex will remove anything in parentheses or brackets, including (U), (USA), (M4), [!], etc.
    new_filename = re.sub(r'[\(\[].*?[\)\]]', '', filename)
    # Strip any extra spaces that may result from the removal
    return new_filename.strip()

def list_txt_files():
    txt_folder = os.path.join(os.getcwd(), "gba plain text names")
    if not os.path.exists(txt_folder):
        print('The "gba plain text names" folder does not exist.')
        return False
    txt_files = [f for f in os.listdir(txt_folder) if f.endswith('.txt')]

    if not txt_files:
        print('No .txt files present in the "gba plain text names" folder.')
        return False

    return txt_files

def list_cover_art_files():
    art_folder = os.path.join(os.getcwd(), "gba cover art")
    if not os.path.exists(art_folder):
        print('The "gba cover art" folder does not exist.')
        return False

    art_files = []
    for root, dirs, files in os.walk(art_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpeg', '.jpg')):
                art_files.append(os.path.join(root, file))

    if not art_files:
        print('No cover art files present in the "gba cover art" folder.')
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

def special_names():
    try:
        gameboy_folder = os.path.join(os.getcwd(), "gba games")
        
        specific_renames = {
            "2-in-1 - Cartoon Network - Block Party & Cartoon Network - Speedway.gba": "2 Games in 1 - Cartoon Network Block Party + Cartoon Network Speedway.gba",
            "2-in-1 - Castlevania Double Pack - Harmony of Dissonance & Aria of Sorrow.gba": "Castlevania Double Pack.gba",
            "2-in-1 - Golden Nugget Casino & Texas Hold'em Poker.gba": "2 Games in 1 - Golden Nugget Casino + Texas Hold 'em Poker.gba",
            "2-in-1 - Hot Wheels - Velocity X & Hot Wheels - World Race.gba": "2 Games in 1 - Hot Wheels - Velocity X + Hot Wheels - World Race.gba",
            "2-in-1 - Matchbox Missions.gba": "2 Game Pack! - Matchbox Missions - Emergency Response + Air, Land and Sea Rescue.gba",
            "2-in-1 - Paperboy & Rampage.gba": "2 Games in One! - Paperboy + Rampage.gba",
            "2-in-1 - Quad Desert Fury & Monster Trucks.gba": "2 Games in 1 - Quad Desert Fury + Monster Trucks.gba",
            "2-in-1 - Shark Tale & Shrek 2.gba": "2 in 1 Game Pack - Shrek 2 + Shark Tale.gba",
            "2-in-1 - Sonic Gamepack - Sonic Pinball Party & Sonic Advance.gba": "Combo Pack - Sonic Advance + Sonic Pinball Party.gba",
            "2-in-1 - Spider-Man & Spider-Man 2.gba": "2 in 1 Game Pack - Spider-Man + Spider-Man 2.gba",
            "2-in-1 - Spy Hunter & Super Sprint.gba": "2 Games in One! - Spy Hunter + Super Sprint.gba",
            "2-in-1 - Tony Hawk's Underground & Kelly Slater's Pro Surfer.gba": "2 in 1 Game Pack - Tony Hawk's Underground + Kelly Slater's Pro Surfer.gba",
            "2-in-1 - Uno & Skin Bo.gba": "2 Game Pack! - Uno + Skip-Bo.gba",
            "2-in-1 - Yu-Gi-Oh! Gamepack - The Sacred Cards & Reshef of Destruction.gba": "Yu-Gi-Oh! Double Pack.gba",
            "3-in-1 - Candy Land, Chutes and Ladders, Memory.gba": "3 Game Pack! - Candy Land + Chutes and Ladders + Original Memory Game.gba",
            "3-in-1 - Life, Yahtzee, Payday.gba": "3 Game Pack! - The Game of Life + Payday + Yahtzee.gba",
            "3-in-1 - Majesco Sports Pack - Paintball Splat! & Dodgeball & Big Alley Bowling.gba": "Majesco's Sports Pack.gba",
            "3-in-1 - Mousetrap, Simon, Operation.gba": "3 Game Pack! - Mouse Trap + Simon + Operation.gba",
            "3-in-1 - Sorry & Aggravation & Scrabble Junior.gba": "Three-in-One Pack - Sorry! + Aggravation + Scrabble Junior.gba",
            "3-in-1 - Super Breakout & Lunar Lander & Millipede.gba": "3 Games in One! - Super Breakout + Millipede + Lunar Lander.gba",
            "3-in-1 Pong, Asteroids, Yar's Revenge.gba": "3 Games in One! - Yars' Revenge + Asteroids + Pong.gba",
            "All-Star Baseball 2004.gba": "All-Star Baseball 2004 Featuring Derek Jeter.gba",
            "Archer Maclean's Super Dropzone.gba": "Super Dropzone - Intergalactic Rescue Mission.gba",
            "Barbie Horse Adventures.gba": "Barbie Horse Adventures - Blue Ribbon Race.gba",
            "Barbie Secret Agent.gba": "Secret Agent Barbie - Royal Jewels Mission.gba",
            "Bomberman Max 2 - Blue.gba": "Bomberman Max 2 - Blue Advance.gba",
            "Bomberman Max 2 - Red.gba": "Bomberman Max 2 - Red Advance.gba",
            "Breakout, Centipede, Warlords.gba": "3 Games in One! - Breakout + Centipede + Warlords.gba",
            "Buffy - The Vampire Slayer.gba": "Buffy the Vampire Slayer - Wrath of the Darkhul King.gba",
            "Caesar's Palace Advance.gba": "Caesars Palace Advance - Millennium Gold Edition.gba",
            "Chronicles of Narnia, The.gba": "Chronicles of Narnia, The - The Lion, the Witch and the Wardrobe.gba",
            "Connect Four, Perfection, Trouble.gba": "Three-in-One Pack - Connect Four + Perfection + Trouble.gba",
            "Corvette 50th Anniversary.gba": "Corvette.gba",
            "Crazy Taxi.gba": "Crazy Taxi - Catch a Ride.gba",
            "Disney Sports - American Football.gba": "Disney Sports - Football.gba",
            "Disney's Aladdin.gba": "Aladdin.gba",
            "Disney's Brother Bear.gba": "Brother Bear.gba",
            "Disney's Finding Nemo.gba": "Finding Nemo.gba",
            "Disney's Herbie - Fully Loaded.gba": "Herbie - Fully Loaded.gba",
            "Disney's Home on the Range.gba": "Home on the Range.gba",
            "Disney's Kim Possible 3 - Team Possible.gba": "Kim Possible 3 - Team Possible.gba",
            "Disney's Lilo & Stitch.gba": "Lilo & Stitch.gba",
            "Disney's Little Einstein.gba": "Little Einsteins.gba",
            "Disney's Magical Quest 2.gba": "Magical Quest 2 Starring Mickey & Minnie.gba",
            "Disney's Magical Quest.gba": "Magical Quest Starring Mickey & Minnie.gba",
            "Disney's That's SO Raven.gba": "That's So Raven.gba",
            "Disney's The Jungle Book.gba": "Jungle Book, The.gba",
            "Disney's Treasure Planet.gba": "Treasure Planet.gba",
            "Dora's World Adventure.gba": "Dora the Explorer - Dora's World Adventure!.gba",
            "Dr. Mario & Puzzle League.gba": "2 Games in One! - Dr. Mario + Puzzle League.gba",
            "FIFA 06.gba": "FIFA Soccer 06.gba",
            "FIFA 2007.gba": "FIFA Soccer 07.gba",
            "FIFA Football 2004.gba": "FIFA Soccer 2004.gba",
            "FIFA Football 2005.gba": "FIFA Soccer 2005.gba",
            "FIFA World Cup 2006.gba": "2006 FIFA World Cup - Germany 2006.gba",
            "Fire Pro Wrestling A.gba": "Fire Pro Wrestling.gba",
            "Gauntlet & Rampart.gba": "2 Games in One! - Gauntlet + Rampart.gba",
            "Grand Theft Auto Advance.gba": "Grand Theft Auto.gba",
            "GT Championship Racing.gba": "GT Advance - Championship Racing.gba",
            "Hobbit, The.gba": "Hobbit, The - The Prelude to the Lord of the Rings.gba",
            "Hugo - The Evil Mirror Advance.gba": "Hugo - The Evil Mirror.gba",
            "James Bond 007 - Nightfire.gba": "007 - NightFire.gba",
            "KerPlunk!, Toss Across, and TipIt.gba": "3 Game Pack! - Ker Plunk! + Toss Across + Tip It.gba",
            "Kirby - Nightmare in Dreamland.gba": "Kirby - Nightmare in Dream Land.gba",
            "Krazy Racers.gba": "Konami Krazy Racers.gba",
            "LEGO Bionicle - The Game.gba": "Bionicle.gba",
            "LEGO Drome Racers.gba": "Drome Racers.gba",
            "LEGO Football Mania.gba": "LEGO Soccer Mania.gba",
            "LEGO Island 2.gba": "LEGO Island 2 - The Brickster's Revenge.gba",
            "Marble Madness & Klax.gba": "2 Games in One! - Marble Madness + Klax.gba",
            "Megaman & Bass.gba": "Mega Man & Bass.gba",
            "Megaman Battle Network.gba": "Mega Man Battle Network.gba",
            "Megaman Zero 2.gba": "Mega Man Zero 2.gba",
            "Megaman Zero 3.gba": "Mega Man Zero 3.gba",
            "Megaman Zero 4.gba": "Mega Man Zero 4.gba",
            "Megaman Zero.gba": "Mega Man Zero.gba",
            "Moto GP.gba": "MotoGP.gba",
            "MX 2K2 Ricky Carmichael.gba": "MX 2002 Featuring Ricky Carmichael.gba",
            "Phalanx - The Enforce Fighter A-144.gba": "Phalanx.gba",
            "Pirates of the Caribbean.gba": "Pirates of the Caribbean - The Curse of the Black Pearl.gba",
            "Pokemon - Fire Red Version.gba": "Pokémon - FireRed Version.gba",
            "Pokemon - Leaf Green Version.gba": "Pokemon - LeafGreen Version.gba",
            "Princess Natasha.gba": "Princess Natasha - Student, Secret Agent, Princess.gba",
            "R-Type III.gba": "R-Type III - The Third Lightning.gba",
            "Rainbow Six - Rogue Spear.gba": "Tom Clancy's Rainbow Six - Rogue Spear.gba",
            "Rayman 10th Anniversary - Rayman Advance & Rayman 3.gba": "Rayman - 10th Anniversary.gba",
            "Rayman 3 - Hoodlum Havoc.gba": "Rayman 3.gba",
            "Ripping Friends, The.gba": "Ripping Friends, The - The World's Most Manly Men!.gba",
            "Risk, Battleship, Clue.gba": "Three-in-One Pack - Risk + Battleship + Clue.gba",
            "Rock 'em Sock 'em Robots.gba": "Rock'em Sock'em Robots.gba",
            "Shonen Jump's - One Piece.gba": "One Piece.gba",
            "Shonen Jump's - Shaman King - Master of Spirits 2.gba": "Shaman King - Master of Spirits 2.gba",
            "Shonen Jump's - Shaman King - Master of Spirits.gba": "Shaman King - Master of Spirits.gba",
            "Sim City 2000.gba": "SimCity 2000.gba",
            "Snood 2 - Snoods on Vacation.gba": "Snood 2 - On Vacation.gba",
            "Spider-Man - The Movie.gba": "Spider-Man.gba",
            "Spirit - Stallion of The Cimarron.gba": "Spirit - Stallion of the Cimarron - Search for Homeland.gba",
            "Sudoku Fever.gba": "Global Star - Sudoku Fever.gba",
            "Summon Night.gba": "Summon Night - Swordcraft Story.gba",
            "Super Dodgeball Advance.gba": "Super Dodge Ball Advance.gba",
            "Teen Titans 2 - The Brotherhood's Revenge.gba": "Teen Titans 2.gba",
            "Ultimate Muscle - The Path of the Superhero.gba": "Ultimate Muscle - The Kinnikuman Legacy - The Path of the Superhero.gba",
            "WarioWare Inc..gba": "WarioWare, Inc. - Mega Microgame$!.gba",
            "Yu Yu Hakusho - Spirit Detective.gba": "Yu Yu Hakusho - Ghostfiles - Spirit Detective.gba",
            "Yu Yu Hakusho Tournament Tactics.gba": "Yu Yu Hakusho - Ghostfiles - Tournament Tactics.gba",
            "Yu-Gi-Oh! - Ultimate Masters 2006.gba": "Yu-Gi-Oh! - Ultimate Masters - World Championship Tournament 2006.gba",
            "Yu-Gi-Oh! - Worldwide Edition.gba": "Yu-Gi-Oh! - Worldwide Edition - Stairway to the Destined Duel.gba",
            "Zapper.gba": "Zapper - One Wicked Cricket!.gba"
        }
        
        for file in os.listdir(gameboy_folder):
            if file in specific_renames:
                new_file_name = specific_renames[file]
                target_path = os.path.join(gameboy_folder, new_file_name)
                
                try:
                    os.rename(os.path.join(gameboy_folder, file), target_path)
                    print(f"Renamed '{file}' to '{new_file_name}'")
                except Exception as e:
                    print(f"Failed to rename '{file}' to '{new_file_name}': {e}")

    except Exception as e:
        print(f"Error in special_names: {e}")

def transfer_matching_cover_art(gba_files, art_files):
    renamed_folder = os.path.join(os.getcwd(), "renamed cover art")
    if not os.path.exists(renamed_folder):
        os.makedirs(renamed_folder)

    for gba_file in gba_files:
        gba_file_base = os.path.splitext(gba_file)[0]
        for art_file in art_files:
            art_file_base = os.path.splitext(os.path.basename(art_file))[0]
            if art_file_base.lower() == gba_file_base.lower():
                new_art_name = f"{gba_file_base}.gba.png"
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
    print("Thank you for using DAT GBA Wiiflow Tool!")
    answer = input("Would you like to see your listed GBA games? (yes/no): ").strip().lower()

    if answer == 'yes':
        gba_files = list_gameboy_games()
        if gba_files:
            print("Here are your GBA games:")
            for file in gba_files:
                print(file)
            print("\n\n\nThese are the games I picked up!")
        else:
            print("No .gba files present in the 'gba games' folder.")
            time.sleep(5)
            return
    else:
        print("Too Bad, So Sad...")
        time.sleep(3)
        gba_files = list_gameboy_games()
        if gba_files:
            print("Here are your GBA games:")
            for file in gba_files:
                print(file)
            print("\n\n\nThese are the games I picked up!")
        else:
            print("No .gba files present in the 'gba games' folder.")
            time.sleep(5)
            return

    if gba_files:
        print("\n\n")
        
        answer = input("Would you like to check for duplicate titles? (yes/no): ").strip().lower()

        if answer == 'yes':
            source_folder = 'gba games'
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

        answer = input("Would you like to remove the version and region information from the title names?\nExample: 'Pokemon Emerald (USA).gba' would be changed to 'Pokemon Emerald.gba'\nYes or no? ").strip().lower()

        if answer == 'yes':
            gameboy_folder = os.path.join(os.getcwd(), "gba games")
            for file in gba_files:
                base_name, ext = os.path.splitext(file)
                new_base_name = remove_version_region_info(base_name)
                new_file = new_base_name + ext
                
                if os.path.exists(os.path.join(gameboy_folder, new_file)):
                    print(f"File '{new_file}' already exists. Skipping rename for '{file}'.")
                else:
                    try:
                        os.rename(os.path.join(gameboy_folder, file), os.path.join(gameboy_folder, new_file))
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
                print("Here are the text files in the 'gba plain text names' folder:")
                for file in txt_files:
                    print(file)
                
                print("\n\n\n")
                answer = input("Would you like to match the names above to your GBA games and then rename them? (yes/no): ").strip().lower()

                if answer == 'yes':
                    gameboy_folder = os.path.join(os.getcwd(), "gba games")
                    matches = []
                    already_matched = set()
                    while True:
                        changes_made = False
                        gba_files = list_gameboy_games()
                        for game_file in gba_files:
                            if game_file in already_matched:
                                continue
                            game_name, _ = os.path.splitext(game_file)
                            best_match = find_best_match(game_name, txt_files)
                            if best_match:
                                matches.append((game_file, best_match))
                                new_file_name = os.path.splitext(best_match)[0] + ".gba"
                                if os.path.exists(os.path.join(gameboy_folder, new_file_name)):
                                    print(f"File '{new_file_name}' already exists. Skipping rename for '{game_file}'.")
                                else:
                                    try:
                                        os.rename(os.path.join(gameboy_folder, game_file), os.path.join(gameboy_folder, new_file_name))
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

                    print("\n\n\nYour GBA games have been renamed!\n\n\n")
                    answer = input("Would you like to start working on your boxart now? (yes/no): ").strip().lower()

                    if answer == 'yes':
                        art_files = list_cover_art_files()
                        if art_files:
                            answer = input("First thing we should do is remove all of the version information from the boxart titles. Sound good? (yes/no): ").strip().lower()

                            if answer == 'yes':
                                art_folder = os.path.join(os.getcwd(), "gba cover art")
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
                                gba_file_titles = [os.path.splitext(f)[0] for f in gba_files]
                                already_matched_art = set()
                                while True:
                                    changes_made = False
                                    for art_file in art_files:
                                        if art_file in already_matched_art:
                                            continue
                                        art_file_title = os.path.splitext(os.path.basename(art_file))[0]
                                        best_match = find_best_match(art_file_title, gba_file_titles)
                                        if best_match:
                                            art_matches.append((best_match + ".gba", art_file))
                                            changes_made = True
                                            already_matched_art.add(art_file)
                                            print(f"Matched '{art_file}' to '{best_match}'")
                                    if not changes_made:
                                        break

                                if art_matches:
                                    for game_file, art_file in art_matches:
                                        game_base, _ = os.path.splitext(game_file)
                                        new_art_name = game_base + ".gba.png"
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

                                transfer_matching_cover_art(gba_files, art_files)
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
        gameboy_games_folder = 'gba games'
        renamed_cover_art_folder = 'renamed cover art'
        unmatched_games_folder = 'unmatched games'

        if not os.path.exists(unmatched_games_folder):
            os.makedirs(unmatched_games_folder)

        gameboy_games = [f for f in os.listdir(gameboy_games_folder) if f.endswith('.gba')]
        renamed_cover_art = [f for f in os.listdir(renamed_cover_art_folder) if f.endswith('.gba.png')]

        for game in gameboy_games:
            expected_cover_art_name = game + ".png"
            if expected_cover_art_name not in renamed_cover_art:
                print(f"\nNo match found for: {game}. Moving to 'unmatched games' folder.")
                shutil.move(os.path.join(gameboy_games_folder, game), os.path.join(unmatched_games_folder, game))
            else:
                print(f"Match found for: {game}")

    print("\n\n\nAll Done!")
    print("This tool was created by Below Average Gaming!")
    print("""
d8888b.  .d8b.  d888888b       d888b  d8888b.  .d8b.                   
88  `8D d8' `8b `~~88~~'      88' Y8b 88  `8D d8' `8b                  
88   88 88ooo88    88         88      88oooY' 88ooo88                  
88   88 88~~~88    88         88  ooo 88~~~b. 88~~~88                  
88  .8D 88   88    88         88. ~8~ 88   8D 88   88                  
Y8888D' YP   YP    YP          Y888P  Y8888P' YP   YP                  
                                                                       
                                                                       
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
