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

def list_snes_games():
    snes_folder = os.path.join(os.getcwd(), "snes games")
    if not os.path.exists(snes_folder):
        print('The "snes games" folder does not exist.')
        return False
    sfc_files = [f for f in os.listdir(snes_folder) if f.endswith('.sfc')]

    if not sfc_files:
        print('No .sfc files present in the "snes games" folder.')
        time.sleep(5)
        return False

    return sfc_files

def remove_version_region_info(filename):
    new_filename = re.sub(r'[\(\[].*?[\)\]]', '', filename)
    return new_filename.strip()

def list_txt_files():
    txt_folder = os.path.join(os.getcwd(), "snes plain text names")
    if not os.path.exists(txt_folder):
        print('The "snes plain text names" folder does not exist.')
        return False
    txt_files = [f for f in os.listdir(txt_folder) if f.endswith('.txt')]

    if not txt_files:
        print('No .txt files present in the "snes plain text names" folder.')
        return False

    return txt_files

def list_cover_art_files():
    art_folder = os.path.join(os.getcwd(), "snes cover art")
    if not os.path.exists(art_folder):
        print('The "snes cover art" folder does not exist.')
        return False

    art_files = []
    for root, dirs, files in os.walk(art_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpeg', '.jpg')):
                art_files.append(os.path.join(root, file))

    if not art_files:
        print('No cover art files present in the "snes cover art" folder.')
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
        snes_folder = os.path.join(os.getcwd(), "snes games")
        
        specific_renames = {
            "Mega Man VII.sfc": "Mega Man 7.sfc",
            "3 Ninjas Kick Back.sfc": "3 Ninjas Kick Back.sfc",
            "A Bug's Life.sfc": "Bug's Life, A.sfc",
            "A.S.P. Air Strike Patrol.sfc": "A.S.P. - Air Strike Patrol.sfc",
            "AAAHH!!! Real Monsters.sfc": "Aaahh!!! Real Monsters.sfc",
            "ABC Monday Night Football.sfc": "ABC Monday Night Football.sfc",
            "Accelebrid.sfc": "Accele Brid.sfc",
            "ACME Animation Factory.sfc": "ACME Animation Factory.sfc",
            "ActRaiser.sfc": "ActRaiser.sfc",
            "ActRaiser 2.sfc": "ActRaiser 2.sfc",
            "AD&D - Eye of the Beholder.sfc": "Advanced Dungeons & Dragons - Eye of the Beholder.sfc",
            "Addams Family Values.sfc": "Addams Family Values.sfc",
            "Addams Family, The.sfc": "Addams Family, The.sfc",
            "Addams Family, The - Pugsley's Scavenger Hunt.sfc": "Addams Family, The - Pugsley's Scavenger Hunt.sfc",
            "Adventures of Batman & Robin, The.sfc": "Adventures of Batman & Robin, The.sfc",
            "Adventures of Dr. Franken, The.sfc": "Adventures of Dr. Franken, The.sfc",
            "Adventures of Kid Kleets, The.sfc": "Adventures of Kid Kleets, The.sfc",
            "Adventures of Rocky and Bullwinkle and Friends, The.sfc": "Adventures of Rocky and Bullwinkle and Friends, The.sfc",
            "Aero Fighters.sfc": "Aero Fighters.sfc",
            "Aero the Acro-Bat.sfc": "Aero the Acro-Bat.sfc",
            "Aero the Acro-Bat 2.sfc": "Aero the Acro-Bat 2.sfc",
            "Aerobiz.sfc": "Aerobiz.sfc",
            "Aerobiz Supersonic.sfc": "Aerobiz Supersonic.sfc",
            "Air Cavalry.sfc": "Air Cavalry.sfc",
            "Al Unser Jr's Road to the Top.sfc": "Al Unser Jr.'s Road to the Top.sfc",
            "Aladdin.sfc": "Aladdin.sfc",
            "Alcahest.sfc": "Alcahest.sfc",
            "Alien 3.sfc": "Alien 3.sfc",
            "Alien vs. Predator.sfc": "Alien vs. Predator.sfc",
            "American Gladiators.sfc": "American Gladiators.sfc",
            "American Tail, An - Fievel Goes West.sfc": "American Tail, An - Fievel Goes West.sfc",
            "Ancient Magic - Bazoo! Mahou Sekai.sfc": "Ancient Magic - Bazoo! World of Magic.sfc",
            "Andre Agassi Tennis.sfc": "Andre Agassi Tennis.sfc",
            "Animaniacs.sfc": "Animaniacs.sfc",
            "Arabian Nights - Sabaku no Seirei Ou.sfc": "Arabian Nights - Desert Spirit King.sfc",
            "Arcade's Greatest Hits.sfc": "Williams Arcade's Greatest Hits.sfc",
            "Arcade's Greatest Hits - The Atari Collection 1.sfc": "Arcade's Greatest Hits - The Atari Collection 1.sfc",
            "Arcana.sfc": "Arcana.sfc",
            "Ardy Lightfoot.sfc": "Ardy Lightfoot.sfc",
            "Arkanoid - Doh It Again.sfc": "Arkanoid - Doh It Again.sfc",
            "Art of Fighting.sfc": "Art of Fighting.sfc",
            "Assault Suits Valken.sfc": "Assault Suits Valken.sfc",
            "Axelay.sfc": "Axelay.sfc",
            "B.O.B..sfc": "B.O.B..sfc",
            "Bahamut Lagoon.sfc": "Bahamut Lagoon.sfc",
            "Ball Bullet Gun.sfc": "Ball Bullet Gun.sfc",
            "Barbie Super Model.sfc": "Barbie Super Model.sfc",
            "Barbie Vacation Adventure.sfc": "Barbie Vacation Adventure.sfc",
            "Barkley Shut Up and Jam!.sfc": "Barkley Shut Up and Jam!.sfc",
            "Bass Masters Classic.sfc": "BASS Masters Classic.sfc",
            "Bass Masters Classic - Pro Edition.sfc": "BASS Masters Classic - Pro Edition.sfc",
            "Bassin's Black Bass.sfc": "Bassin's Black Bass.sfc",
            "Batman - Revenge of the Joker.sfc": "Batman - Revenge of the Joker.sfc",
            "Batman Forever.sfc": "Batman Forever.sfc",
            "Batman Returns.sfc": "Batman Returns.sfc",
            "Battle Blaze.sfc": "Battle Blaze.sfc",
            "Battle Cars.sfc": "Battle Cars.sfc",
            "Battle Clash.sfc": "Battle Clash.sfc",
            "Battle Grand Prix.sfc": "Battle Grand Prix.sfc",
            "Battletoads & Double Dragon - The Ultimate Team.sfc": "Battletoads & Double Dragon - The Ultimate Team.sfc",
            "Battletoads in Battlemaniacs.sfc": "Battletoads in Battlemaniacs.sfc",
            "Bazooka Blitzkrieg.sfc": "Bazooka Blitzkrieg.sfc",
            "Beauty and the Beast.sfc": "Beauty and the Beast.sfc",
            "Beavis and Butt-head.sfc": "Beavis and Butt-Head.sfc",
            "Bebe's Kids.sfc": "Bebe's Kids.sfc",
            "Best of the Best - Championship Karate.sfc": "Best of the Best - Championship Karate.sfc",
            "Big Sky Trooper.sfc": "Big Sky Trooper.sfc",
            "Biker Mice From Mars.sfc": "Biker Mice from Mars.sfc",
            "Bill Laimbeer's Combat Basketball.sfc": "Bill Laimbeer's Combat Basketball.sfc",
            "Bill Walsh College Football.sfc": "Bill Walsh College Football.sfc",
            "Bio Metal.sfc": "BioMetal.sfc",
            "Bishoujo Senshi Sailor Moon - Another Story.sfc": "Sailor Moon - Another Story.sfc",
            "Blackthorne.sfc": "Blackthorne.sfc",
            "Blues Brothers, The.sfc": "Blues Brothers, The.sfc",
            "Bobby's World.sfc": "Bobby's World.sfc",
            "Bonkers.sfc": "Bonkers.sfc",
            "Boogerman - A Pick and Flick Adventure.sfc": "Boogerman - A Pick and Flick Adventure.sfc",
            "Boxing Legends of the Ring.sfc": "Boxing Legends of the Ring.sfc",
            "Brain Lord.sfc": "Brain Lord.sfc",
            "Brainies, The.sfc": "Brainies, The.sfc",
            "Bram Stoker's Dracula.sfc": "Bram Stoker's Dracula.sfc",
            "Brandish.sfc": "Brandish.sfc",
            "Brandish 2 - The Planet Buster.sfc": "Brandish 2 - The Planet Buster.sfc",
            "Brawl Brothers.sfc": "Brawl Brothers.sfc",
            "BreakThru!.sfc": "BreakThru!.sfc",
            "Breath of Fire.sfc": "Breath of Fire.sfc",
            "Breath of Fire II.sfc": "Breath of Fire II.sfc",
            "Brett Hull Hockey '95.sfc": "Brett Hull Hockey '95.sfc",
            "Brett Hull Hockey.sfc": "Brett Hull Hockey.sfc",
            "Brunswick World Tournament of Champions.sfc": "Brunswick World Tournament of Champions.sfc",
            "Brutal - Paws of Fury.sfc": "Brutal - Paws of Fury.sfc",
            "Bubsy II.sfc": "Bubsy II.sfc",
            "Bubsy in Claws Encounters of the Furred Kind.sfc": "Bubsy in Claws Encounters of the Furred Kind.sfc",
            "Bugs Bunny - Rabbit Rampage.sfc": "Bugs Bunny - Rabbit Rampage.sfc",
            "Bulls Vs Blazers and the NBA Playoffs.sfc": "Bulls vs Blazers and the NBA Playoffs.sfc",
            "Bust-A-Move.sfc": "Bust-A-Move.sfc",
            "Cacoma Knight in Bizyland.sfc": "Cacoma Knight in Bizyland.sfc",
            "Cal Ripken Jr. Baseball.sfc": "Cal Ripken Jr. Baseball.sfc",
            "California Games II.sfc": "California Games II.sfc",
            "Cannondale Cup.sfc": "Cannondale Cup.sfc",
            "Capcom's MVP Football.sfc": "Capcom's MVP Football.sfc",
            "Capcom's Soccer Shootout.sfc": "Capcom's Soccer Shootout.sfc",
            "Captain America and The Avengers.sfc": "Captain America and the Avengers.sfc",
            "Captain Commando.sfc": "Captain Commando.sfc",
            "Captain Novolin.sfc": "Captain Novolin.sfc",
            "Carrier Aces.sfc": "Carrier Aces.sfc",
            "Casper.sfc": "Casper.sfc",
            "Castlevania - Dracula X.sfc": "Castlevania - Dracula X.sfc",
            "Champions World Class Soccer.sfc": "Champions - World Class Soccer.sfc",
            "Championship Pool.sfc": "Championship Pool.sfc",
            "Championship Soccer '94.sfc": "Championship Soccer '94.sfc",
            "Chavez.sfc": "Chavez.sfc",
            "Chavez II.sfc": "Chavez II.sfc",
            "Chessmaster, The.sfc": "Chessmaster, The.sfc",
            "Chester Cheetah - Too Cool to Fool.sfc": "Chester Cheetah - Too Cool to Fool.sfc",
            "Chester Cheetah - Wild Wild Quest.sfc": "Chester Cheetah - Wild Wild Quest.sfc",
            "Chrono Trigger.sfc": "Chrono Trigger.sfc",
            "Chuck Rock.sfc": "Chuck Rock.sfc",
            "Civilization.sfc": "Civilization.sfc",
            "Classic Kong Complete.sfc": "Classic Kong.sfc",
            "Clay Fighter.sfc": "Clay Fighter.sfc",
            "Clay Fighter - Tournament Edition.sfc": "Clay Fighter - Tournament Edition.sfc",
            "Clay Fighter 2 - Judgment Clay.sfc": "Clay Fighter 2 - Judgment Clay.sfc",
            "Claymates.sfc": "Claymates.sfc",
            "Claymates Demo.sfc": "Claymates.sfc",
            "Cliffhanger.sfc": "Cliffhanger.sfc",
            "Clock Tower.sfc": "Clock Tower.sfc",
            "Clue.sfc": "Clue.sfc",
            "College Football USA '97 - The Road to New Orleans.sfc": "College Football USA '97 - The Road to New Orleans.sfc",
            "College Slam Basketball.sfc": "College Slam.sfc",
            "Combatribes, The.sfc": "Combatribes, The.sfc",
            "Congo's Caper.sfc": "Congo's Caper.sfc",
            "Contra III - The Alien Wars.sfc": "Contra III - The Alien Wars.sfc",
            "Cool Spot.sfc": "Cool Spot.sfc",
            "Cool World.sfc": "Cool World.sfc",
            "Crystal Beans - From Dungeon Explorer.sfc": "Crystal Beans From Dungeon Explorer.sfc",
            "Cu-On-Pa SFC.sfc": "Cu-On-Pa SFC.sfc",
            "Cutthroat Island.sfc": "Cutthroat Island.sfc",
            "Cyber Knight.sfc": "Cyber Knight.sfc",
            "Cyber Spin.sfc": "Cyber Spin.sfc",
            "Cybernator.sfc": "Cybernator.sfc",
            "Cyborg 009.sfc": "Cyborg 009.sfc",
            "D-Force.sfc": "D-Force.sfc",
            "Daffy Duck - The Marvin Missions.sfc": "Daffy Duck - The Marvin Missions.sfc",
            "Darius Twin.sfc": "Darius Twin.sfc",
            "Dark Law - Meaning of Death.sfc": "Dark Law - Meaning of Death.sfc",
            "David Crane's Amazing Tennis.sfc": "David Crane's Amazing Tennis.sfc",
            "Death and Return of Superman, The.sfc": "Death and Return of Superman, The.sfc",
            "Demolition Man.sfc": "Demolition Man.sfc",
            "Demon's Crest.sfc": "Demon's Crest.sfc",
            "Dennis the Menace.sfc": "Dennis the Menace.sfc",
            "Der Langrisser.sfc": "Der Langrisser.sfc",
            "Desert Strike - Return to the Gulf.sfc": "Desert Strike - Return to the Gulf.sfc",
            "Dig & Spike Volleyball.sfc": "Dig & Spike Volleyball.sfc",
            "Digimon Adventure.sfc": "Digimon Adventure.sfc",
            "Dino City.sfc": "DinoCity.sfc",
            "Dirt Trax FX.sfc": "Dirt Trax FX.sfc",
            "Donald Duck and the Magical Hat.sfc": "Donald Duck and the Magical Hat.sfc",
            "Donkey Kong Country (Competition Cartridge).sfc": "Donkey Kong Country - Competition Edition.sfc",
            "Donkey Kong Country.sfc": "Donkey Kong Country.sfc",
            "Donkey Kong Country 2 - Diddy's Kong Quest.sfc": "Donkey Kong Country 2 - Diddy's Kong Quest.sfc",
            "Donkey Kong Country 3 - Dixie Kong's Double Trouble.sfc": "Donkey Kong Country 3 - Dixie Kong's Double Trouble!.sfc",
            "Doom.sfc": "Doom.sfc",
            "Doomsday Warrior.sfc": "Doomsday Warrior.sfc",
            "DoReMi Fantasy - Milon no DokiDoki Daibouken.sfc": "DoReMi Fantasy - Milon's Quest.sfc",
            "Dorke & Ymp.sfc": "Dorke & Ymp.sfc",
            "Dossun! Ganseki Battle.sfc": "Dossun! Stone Battle.sfc",
            "Double Dragon V - The Shadow Falls.sfc": "Double Dragon V - The Shadow Falls.sfc",
            "Dragon - The Bruce Lee Story.sfc": "Dragon - The Bruce Lee Story.sfc",
            "Dragon Ball Z - Hyper Dimension.sfc": "Dragon Ball Z - Hyper Dimension.sfc",
            "Dragon Ball Z - Super Butouden 3.sfc": "Dragon Ball Z - Super Butouden 3.sfc",
            "Dragon Ball Z - Super Butouden.sfc": "Dragon Ball Z - Super Butouden.sfc",
            "Dragon Ball Z - Super Saiya Densetsu.sfc": "Dragon Ball Z - Super Butouden.sfc",
            "Dragon Quest 1 and 2.sfc": "Dragon Quest V.sfc",
            "Dragon Quest I & II.sfc": "Dragon Quest I & II.sfc",
            "Dragon View.sfc": "Dragon View.sfc",
            "Dragon's Lair.sfc": "Dragon's Lair.sfc",
            "Dragon-Ball Z - Hyper Dimension.sfc": "Dragon Ball Z - Hyper Dimension.sfc",
            "Dragon-Ball Z - Super Butouden.sfc": "Dragon Ball Z - Super Butouden.sfc",
            "Dragon-Ball Z - Super Butouden 3.sfc": "Dragon Ball Z - Super Butouden 3.sfc",
            "Dragon-Ball Z - Super Gokuden Totsugeki Hen.sfc": "Dragon Ball Z - Super Butouden 3.sfc",
            "Dragon-Ball Z - Super Saiyan Densetsu.sfc": "Dragon Ball Z - Super Butouden.sfc",
            "Dragon-Ball-Z - Super Gokuden 2.sfc": "Dragon Ball Z - Super Butouden 2.sfc",
            "Drakkhen.sfc": "Drakkhen.sfc",
            "Dream TV.sfc": "Dream TV.sfc",
            "Dual Orb 2.sfc": "Dual Orb II.sfc",
            "Dual Orb II.sfc": "Dual Orb II.sfc",
            "Dungeon Master.sfc": "Dungeon Master.sfc",
            "E.V.O. Search for Eden.sfc": "E.V.O. - Search For Eden.sfc",
            "Earthbound.sfc": "EarthBound.sfc",
            "Earthworm Jim.sfc": "Earthworm Jim.sfc",
            "Earthworm Jim 2.sfc": "Earthworm Jim 2.sfc",
            "Eek! The Cat.sfc": "Eek! The Cat.sfc",
            "Elite Soccer.sfc": "Elite Soccer.sfc",
            "Emerald Dragon.sfc": "Emerald Dragon.sfc",
            "Emmitt Smith Football.sfc": "Emmitt Smith Football.sfc",
            "Energy Breaker.sfc": "Energy Breaker.sfc",
            "Equinox.sfc": "Equinox.sfc",
            "ESPN Baseball Tonight.sfc": "ESPN Baseball Tonight.sfc",
            "ESPN National Hockey Night.sfc": "ESPN National Hockey Night.sfc",
            "ESPN Speedworld.sfc": "ESPN Speedworld.sfc",
            "ESPN Sunday Night NFL.sfc": "ESPN Sunday Night NFL.sfc",
            "Extra Innings.sfc": "Extra Innings.sfc",
            "F1 Pole Position.sfc": "F1 Pole Position.sfc",
            "F1 ROC - Race of Champions.sfc": "F1 ROC - Race of Champions.sfc",
            "F1 ROC II - Race of Champions.sfc": "F1 ROC II - Race of Champions.sfc",
            "Faceball 2000.sfc": "Faceball 2000.sfc",
            "Famicom Tantei Club Part II.sfc": "Famicom Detective Club Part II.sfc",
            "Family Dog.sfc": "Family Dog.sfc",
            "Family Feud.sfc": "Family Feud.sfc",
            "Fatal Fury.sfc": "Fatal Fury.sfc",
            "Fatal Fury 2.sfc": "Fatal Fury 2.sfc",
            "Fatal Fury Special.sfc": "Fatal Fury Special.sfc",
            "Feda - the Emblem of Justice.sfc": "Feda - The Emblem of Justice.sfc",
            "FIFA International Soccer.sfc": "FIFA International Soccer.sfc",
            "FIFA Soccer 96.sfc": "FIFA Soccer 96.sfc",
            "Fighter's History.sfc": "Fighter's History.sfc",
            "Final Fantasy - Mystic Quest.sfc": "Final Fantasy - Mystic Quest.sfc",
            "Final Fantasy 4 - 10th Anniversary Edition.sfc": "Final Fantasy IV - Ultima Edition.sfc",
            "Final Fantasy 6.sfc": "Final Fantasy VI.sfc",
            "Final Fantasy II.sfc": "Final Fantasy II.sfc",
            "Final Fantasy III.sfc": "Final Fantasy III.sfc",
            "Final Fantasy V.sfc": "Final Fantasy V.sfc",
            "Final Fight.sfc": "Final Fight.sfc",
            "Final Fight 2.sfc": "Final Fight 2.sfc",
            "Final Fight 3.sfc": "Final Fight 3.sfc",
            "Final Fight Guy.sfc": "Final Fight Guy.sfc",
            "Fire Emblem - Thracia 776.sfc": "Fire Emblem 5 - Thracia 776.sfc",
            "Fire Striker.sfc": "FireStriker.sfc",
            "Firepower 2000.sfc": "Firepower 2000.sfc",
            "First Samurai.sfc": "First Samurai.sfc",
            "Flashback - The Quest for Identity.sfc": "Flashback - The Quest for Identity.sfc",
            "Flintstones, The.sfc": "Flintstones, The.sfc",
            "Flintstones, The - The Treasure of Sierra Madrock.sfc": "Flintstones, The - The Treasure of Sierra Madrock.sfc",
            "Flying Hero - Bugyuru no Daibouken.sfc": "Flying Hero - Bugyuru's Adventure.sfc",
            "Football Fury.sfc": "Football Fury.sfc",
            "Foreman For Real.sfc": "Foreman for Real.sfc",
            "Frank Thomas' Big Hurt Baseball.sfc": "Frank Thomas Big Hurt Baseball.sfc",
            "Frantic Flea.sfc": "Frantic Flea.sfc",
            "Frogger.sfc": "Frogger.sfc",
            "Front Mission - Gun Hazard.sfc": "Front Mission - Gun Hazard.sfc",
            "Front Mission.sfc": "Front Mission.sfc",
            "Full Throttle Racing.sfc": "Full Throttle - All-American Racing.sfc",
            "Fun 'N Games.sfc": "Fun 'n Games.sfc",
            "Funaki Masakatsu Hybrid Wrestler - Tougi Denshou.sfc": "Funaki Masakatsu Hybrid Wrestler - Tougi Denshou.sfc",
            "Gekitou Burning Pro Wrestling.sfc": "Burning Pro Wrestling.sfc",
            "Gemfire.sfc": "Gemfire.sfc",
            "Genghis Khan II - Clan of the Gray Wolf.sfc": "Genghis Khan II - Clan of the Gray Wolf.sfc",
            "George Foreman's KO Boxing.sfc": "George Foreman's KO Boxing.sfc",
            "Ghoul Patrol.sfc": "Ghoul Patrol.sfc",
            "Go Go Ackman.sfc": "Go Go Ackman.sfc",
            "Gods.sfc": "Gods.sfc",
            "Goof Troop.sfc": "Goof Troop.sfc",
            "GP-1.sfc": "GP-1.sfc",
            "GP-1 Part II.sfc": "GP-1 - Part II.sfc",
            "Gradius III.sfc": "Gradius III.sfc",
            "Great Circus Mystery Starring Mickey & Minnie, The.sfc": "Great Circus Mystery Starring Mickey & Minnie, The.sfc",
            "Great Waldo Search, The.sfc": "Great Waldo Search, The.sfc",
            "Gunple - Gunman's Proof.sfc": "Ganpuru - Gunman's Proof.sfc",
            "HAL's Hole in One Golf.sfc": "HAL's Hole in One Golf.sfc",
            "Hammerlock Wrestling.sfc": "Hammerlock Wrestling.sfc",
            "Hardball III.sfc": "HardBall III.sfc",
            "Harley's Humongous Adventure.sfc": "Harley's Humongous Adventure.sfc",
            "Harvest Moon.sfc": "Harvest Moon.sfc",
            "Head-On Soccer.sfc": "Head-On Soccer.sfc",
            "Hind Strike.sfc": "Hind Strike.sfc",
            "Hit the Ice.sfc": "Hit the Ice.sfc",
            "Holy Umbrella - Dondera no Mubo!!.sfc": "Holy Umbrella - Dondera's Wild!!.sfc",
            "Home Alone.sfc": "Home Alone.sfc",
            "Home Alone 2 - Lost in New York.sfc": "Home Alone 2 - Lost in New York.sfc",
            "Hook.sfc": "Hook.sfc",
            "Hunt for Red October, The.sfc": "Hunt for Red October, The.sfc",
            "Hurricanes, The.sfc": "Hurricanes.sfc",
            "Hyper V-Ball.sfc": "Hyper V-Ball.sfc",
            "HyperZone.sfc": "HyperZone.sfc",
            "Ignition Factor, The.sfc": "Ignition Factor, The.sfc",
            "Illusion of Gaia.sfc": "Illusion of Gaia.sfc",
            "Imperium.sfc": "Imperium.sfc",
            "Incantation.sfc": "Incantation.sfc",
            "Incredible Crash Dummies, The.sfc": "Incredible Crash Dummies, The.sfc",
            "Incredible Hulk, The.sfc": "Incredible Hulk, The.sfc",
            "Indiana Jones' Greatest Adventures.sfc": "Indiana Jones' Greatest Adventures.sfc",
            "Inindo - Way of the Ninja.sfc": "Inindo - Way of the Ninja.sfc",
            "Inspector Gadget.sfc": "Inspector Gadget.sfc",
            "International Superstar Soccer.sfc": "International Superstar Soccer.sfc",
            "International Superstar Soccer Deluxe.sfc": "International Superstar Soccer Deluxe.sfc",
            "International Tennis Tour.sfc": "International Tennis Tour.sfc",
            "Irem Skins Game, The.sfc": "Irem Skins Game, The.sfc",
            "Iron Commando.sfc": "Iron Commando.sfc",
            "Itchy & Scratchy Game, The.sfc": "Itchy & Scratchy Game, The.sfc",
            "Izzy's Quest for the Olympic Rings.sfc": "Izzy's Quest for the Olympic Rings.sfc",
            "Jack Nicklaus Golf.sfc": "Jack Nicklaus Golf.sfc",
            "James Bond Jr.sfc": "James Bond Jr.sfc",
            "Jammit.sfc": "Jammit.sfc",
            "Jeopardy!.sfc": "Jeopardy!.sfc",
            "Jeopardy! Deluxe Edition.sfc": "Jeopardy! Deluxe Edition.sfc",
            "Jeopardy! Sports Edition.sfc": "Jeopardy! Sports Edition.sfc",
            "Jerry Boy.sfc": "Jerry Boy.sfc",
            "Jet Pilot Rising.sfc": "Jet Pilot Rising.sfc",
            "Jetsons, The - Invasion of the Planet Pirates.sfc": "Jetsons, The - Invasion of the Planet Pirates.sfc",
            "Jim Lee's WildC.A.T.S.sfc": "Jim Lee's WildC.A.T.S - Covert-Action-Teams.sfc",
            "Jim Power - The Lost Dimension in 3D.sfc": "Jim Power - The Lost Dimension in 3D.sfc",
            "Jimmy Connors Pro Tennis Tour.sfc": "Jimmy Connors Pro Tennis Tour.sfc",
            "Jimmy Houston's Bass Tournament U.S.A..sfc": "Jimmy Houston's Bass Tournament U.S.A..sfc",
            "Joe & Mac.sfc": "Joe & Mac.sfc",
            "Joe & Mac 2 - Lost in the Tropics.sfc": "Joe & Mac 2 - Lost in the Tropics.sfc",
            "John Madden Football '93.sfc": "John Madden Football '93.sfc",
            "John Madden Football.sfc": "John Madden Football.sfc",
            "JRR Tolkien's The Lord of the Rings - Volume 1.sfc": "J.R.R. Tolkien's The Lord of the Rings - Volume 1.sfc",
            "Judge Dredd.sfc": "Judge Dredd.sfc",
            "Jungle Book, The.sfc": "Jungle Book, The.sfc",
            "Jungle Strike.sfc": "Jungle Strike.sfc",
            "Jurassic Park.sfc": "Jurassic Park.sfc",
            "Jurassic Park Part 2 - The Chaos Continues.sfc": "Jurassic Park II - The Chaos Continues.sfc",
            "Justice League Task Force.sfc": "Justice League Task Force.sfc",
            "Kablooey.sfc": "Kablooey.sfc",
            "Kawasaki Caribbean Challenge.sfc": "Kawasaki Caribbean Challenge.sfc",
            "Kawasaki Superbike Challenge.sfc": "Kawasaki Superbike Challenge.sfc",
            "Ken Griffey Jr. Presents Major League Baseball.sfc": "Ken Griffey Jr. Presents Major League Baseball.sfc",
            "Ken Griffey Jr.'s Winning Run.sfc": "Ken Griffey Jr.'s Winning Run.sfc",
            "Kendo Rage.sfc": "Kendo Rage.sfc",
            "Kid Klown in Crazy Chase.sfc": "Kid Klown in Crazy Chase.sfc",
            "Kidou Senshi Gundam - Cross Dimension 0079.sfc": "Mobile Suit Gundam - Cross Dimension 0079.sfc",
            "Killer Instinct.sfc": "Killer Instinct.sfc",
            "King Arthur & The Knights of Justice.sfc": "King Arthur & The Knights of Justice.sfc",
            "King Arthur's World.sfc": "King Arthur's World.sfc",
            "King of Dragons, The.sfc": "King of Dragons.sfc",
            "King of Fighters 2000.sfc": "King of Fighters 2000.sfc",
            "King of the Monsters.sfc": "King of the Monsters.sfc",
            "King of the Monsters 2.sfc": "King of the Monsters 2.sfc",
            "Kirby Super Star.sfc": "Kirby Super Star.sfc",
            "Kirby's Avalanche.sfc": "Kirby's Avalanche.sfc",
            "Kirby's Dream Course.sfc": "Kirby's Dream Course.sfc",
            "Kirby's Dream Land 3.sfc": "Kirby's Dream Land 3.sfc",
            "Knights of the Round.sfc": "Knights of the Round.sfc",
            "Krusty's Super Fun House.sfc": "Krusty's Super Fun House.sfc",
            "Kyle Petty's No Fear Racing.sfc": "Kyle Petty's No Fear Racing.sfc",
            "Lagoon.sfc": "Lagoon.sfc",
            "Lamborghini - American Challenge.sfc": "Lamborghini American Challenge.sfc",
            "Last Action Hero.sfc": "Last Action Hero.sfc",
            "Lawnmower Man, The.sfc": "Lawnmower Man, The.sfc",
            "Legend.sfc": "Legend.sfc",
            "Legend of The Mystical Ninja, The.sfc": "Legend of the Mystical Ninja, The.sfc",
            "Legend of Zelda, The - A Link to the Past.sfc": "Legend of Zelda, The - A Link to the Past.sfc",
            "Lemmings.sfc": "Lemmings.sfc",
            "Lemmings 2 - The Tribes.sfc": "Lemmings 2 - The Tribes.sfc",
            "Lester the Unlikely.sfc": "Lester the Unlikely.sfc",
            "Lethal Enforcers.sfc": "Lethal Enforcers.sfc",
            "Lethal Weapon.sfc": "Lethal Weapon.sfc",
            "Liberty or Death.sfc": "Liberty or Death.sfc",
            "Lion King, The.sfc": "Lion King, The.sfc",
            "Little Magic.sfc": "Little Magic.sfc",
            "Live A Live.sfc": "Live A Live.sfc",
            "Lock On.sfc": "Lock On.sfc",
            "Looney Tunes B-Ball.sfc": "Looney Tunes B-Ball.sfc",
            "Lost Vikings II, The.sfc": "Lost Vikings 2.sfc",
            "Lost Vikings, The.sfc": "Lost Vikings, The.sfc",
            "Lufia & The Fortress of Doom.sfc": "Lufia & The Fortress of Doom.sfc",
            "Lufia II - Rise of the Sinistrals.sfc": "Lufia II - Rise of the Sinistrals.sfc",
            "Madden NFL '94.sfc": "Madden NFL '94.sfc",
            "Madden NFL '95.sfc": "Madden NFL '95.sfc",
            "Madden NFL '96.sfc": "Madden NFL '96.sfc",
            "Madden NFL '97.sfc": "Madden NFL '97.sfc",
            "Madden NFL '98.sfc": "Madden NFL '98.sfc",
            "Magic Boy.sfc": "Magic Boy.sfc",
            "Magic Sword.sfc": "Magic Sword.sfc",
            "Magical Pop'n.sfc": "Magical Pop'n.sfc",
            "Mario is Missing!.sfc": "Mario is Missing!.sfc",
            "Mario Paint.sfc": "Mario Paint.sfc",
            "Mario's Early Years! - Fun with Letters.sfc": "Mario's Early Years! - Fun with Letters.sfc",
            "Mario's Early Years! - Fun with Numbers.sfc": "Mario's Early Years! - Fun with Numbers.sfc",
            "Mario's Early Years! - Preschool Fun.sfc": "Mario's Early Years! - Preschool Fun.sfc",
            "Marvel Super Heroes - War of the Gems.sfc": "Marvel Super Heroes - War of the Gems.sfc",
            "Mary Shelley's Frankenstein.sfc": "Mary Shelley's Frankenstein.sfc",
            "Mask, The.sfc": "Mask, The.sfc",
            "Math Blaster Episode 1.sfc": "Math Blaster - Episode 1.sfc",
            "Maui Mallard in Cold Shadow.sfc": "Maui Mallard in Cold Shadow.sfc",
            "Mecarobot Golf.sfc": "Mecarobot Golf.sfc",
            "MechWarrior.sfc": "MechWarrior.sfc",
            "MechWarrior 3050.sfc": "MechWarrior 3050.sfc",
            "Mega Lo Mania.sfc": "Mega Lo Mania.sfc",
            "Mega Man 7.sfc": "Mega Man 7.sfc",
            "Mega Man X.sfc": "Mega Man X.sfc",
            "Mega Man X 2.sfc": "Mega Man X2.sfc",
            "Mega Man X 3.sfc": "Mega Man X3.sfc",
            "Mega Man X2.sfc": "Mega Man X2.sfc",
            "Mega Man X3.sfc": "Mega Man X3.sfc",
            "Metal Combat - Falcon's Revenge.sfc": "Metal Combat - Falcon's Revenge.sfc",
            "Metal Marines.sfc": "Metal Marines.sfc",
            "Metal Max 2.sfc": "Metal Max 2.sfc",
            "Metal Morph.sfc": "Metal Morph.sfc",
            "Metal Warriors.sfc": "Metal Warriors.sfc",
            "Michael Andretti's Indy Car Challenge.sfc": "Michael Andretti's Indy Car Challenge.sfc",
            "Michael Jordan - Chaos in the Windy City.sfc": "Michael Jordan - Chaos in the Windy City.sfc",
            "Mickey Mania - The Timeless Adventures of Mickey Mouse.sfc": "Mickey Mania - The Timeless Adventures of Mickey Mouse.sfc",
            "Mickey no Tokyo Disneyland Daibouken.sfc": "Mickey's Tokyo Disneyland Adventure.sfc",
            "Mickey's Playtown Adventure - A Day of Discovery!.sfc": "Mickey's Playtown Adventure - A Day of Discovery!.sfc",
            "Micro Machines.sfc": "Micro Machines.sfc",
            "Might and Magic III - Isles of Terra.sfc": "Might and Magic III - Isles of Terra.sfc",
            "Mighty Max.sfc": "Mighty Max.sfc",
            "Mighty Morphin Power Rangers.sfc": "Mighty Morphin Power Rangers.sfc",
            "Mighty Morphin Power Rangers - The Fighting Edition.sfc": "Mighty Morphin Power Rangers - The Fighting Edition.sfc",
            "Mighty Morphin Power Rangers - The Movie.sfc": "Mighty Morphin Power Rangers - The Movie.sfc",
            "Militia.sfc": "Militia.sfc",
            "Miracle Piano Teaching System, The.sfc": "Miracle Piano Teaching System, The.sfc",
            "Mohawk & Headphone Jack.sfc": "Mohawk & Headphone Jack.sfc",
            "Monopoly.sfc": "Monopoly.sfc",
            "Monster Maker 3 - Hikari no Majutsushi.sfc": "Monster Maker 3 - Wizard of Light.sfc",
            "Monstania.sfc": "Monstania.sfc",
            "Mortal Kombat.sfc": "Mortal Kombat.sfc",
            "Mortal Kombat 3.sfc": "Mortal Kombat 3.sfc",
            "Mortal Kombat II.sfc": "Mortal Kombat II.sfc",
            "Mountain Bike Rally.sfc": "Mountain Bike Rally.sfc",
            "Mr. Do!.sfc": "Mr. Do!.sfc",
            "Mr. Nutz.sfc": "Mr. Nutz.sfc",
            "Ms. Pac-Man.sfc": "Ms. Pac-Man.sfc",
            "Muscle Bomber.sfc": "Saturday Night Slam Masters.sfc",
            "Mutant Chronicles - Doom Troopers.sfc": "Doom Troopers.sfc",
            "Nageshiko Den - Ketteiban - Shoujo Pro Wrestler Densetsu.sfc": "Nageshiko Den - Ketteiban - Shoujo Pro Wrestler Densetsu.sfc",
            "NBA All-Star Challenge.sfc": "NBA All-Star Challenge.sfc",
            "NBA Give 'n Go.sfc": "NBA Give 'n Go.sfc",
            "NBA Hang Time.sfc": "NBA Hangtime.sfc",
            "NBA Jam.sfc": "NBA Jam.sfc",
            "NBA Jam - Tournament Edition.sfc": "NBA Jam - Tournament Edition.sfc",
            "NBA Jam T.E..sfc": "NBA Jam T.E..sfc",
            "NBA Live '95.sfc": "NBA Live '95.sfc",
            "NBA Live '96.sfc": "NBA Live '96.sfc",
            "NBA Live '97.sfc": "NBA Live '97.sfc",
            "NBA Live '98.sfc": "NBA Live '98.sfc",
            "NCAA Basketball.sfc": "NCAA Basketball.sfc",
            "NCAA Football.sfc": "NCAA Football.sfc",
            "NCAA Final Four Basketball.sfc": "NCAA Final Four Basketball.sfc",
            "New Horizons.sfc": "New Horizons.sfc",
            "NFL Football.sfc": "NFL.sfc",
            "NHL '94.sfc": "NHL '94.sfc",
            "NHL '95.sfc": "NHL '95.sfc",
            "NHL '96.sfc": "NHL '96.sfc",
            "NHL '97.sfc": "NHL '97.sfc",
            "NHL '98.sfc": "NHL '98.sfc",
            "NHLPA Hockey '93.sfc": "NHLPA Hockey '93.sfc",
            "Ninja Gaiden Trilogy.sfc": "Ninja Gaiden Trilogy.sfc",
            "Ninja Warriors, The.sfc": "Ninjawarriors.sfc",
            "Nintama Rantarou - Ninjutsu Gakuen Puzzle Taikai no Dan.sfc": "Nintama Rantarou - Ninjutsu Gakuen Puzzle Taikai no Dan.sfc",
            "No Escape.sfc": "No Escape.sfc",
            "Nosferatu.sfc": "Nosferatu.sfc",
            "Nurikabe Crazy Town.sfc": "Nurikabe Crazy Town.sfc",
            "Obitus.sfc": "Obitus.sfc",
            "Ogre Battle - The March of the Black Queen.sfc": "Ogre Battle - The March of the Black Queen.sfc",
            "Ooze, The.sfc": "Ooze, The.sfc",
            "Operation Europe - Path to Victory 1939-45.sfc": "Operation Europe - Path to Victory 1939-45.sfc",
            "Operation Logic Bomb.sfc": "Operation Logic Bomb.sfc",
            "Operation Thunderbolt.sfc": "Operation Thunderbolt.sfc",
            "Oscar.sfc": "Oscar.sfc",
            "Out of This World.sfc": "Out of This World.sfc",
            "Out to Lunch.sfc": "Out to Lunch.sfc",
            "Pac-Attack.sfc": "Pac-Attack.sfc",
            "Pac-In-Time.sfc": "Pac-In-Time.sfc",
            "Pac-Man 2 - The New Adventures.sfc": "Pac-Man 2 - The New Adventures.sfc",
            "Pagemaster, The.sfc": "Pagemaster, The.sfc",
            "Paladin's Quest.sfc": "Paladin's Quest.sfc",
            "Panic in Nakayoshi World.sfc": "Panic in Nakayoshi World.sfc",
            "Paperboy 2.sfc": "Paperboy 2.sfc",
            "Parlor! Mini 2.sfc": "Parlor! Mini 2.sfc",
            "Patlabor.sfc": "Patlabor.sfc",
            "Peace Keepers, The.sfc": "Peace Keepers, The.sfc",
            "Pebble Beach Golf Links.sfc": "Pebble Beach Golf Links.sfc",
            "Pele.sfc": "Pele.sfc",
            "Pele! II.sfc": "Pele! II.sfc",
            "Phalanx.sfc": "Phalanx.sfc",
            "Phantom 2040.sfc": "Phantom 2040.sfc",
            "Pieces.sfc": "Pieces.sfc",
            "Pilotwings.sfc": "Pilotwings.sfc",
            "Pink Goes to Hollywood.sfc": "Pink Goes to Hollywood.sfc",
            "Pinocchio.sfc": "Pinocchio.sfc",
            "Pirates of Dark Water, The.sfc": "Pirates of Dark Water, The.sfc",
            "Pitfall - The Mayan Adventure.sfc": "Pitfall - The Mayan Adventure.sfc",
            "Pitfall II.sfc": "Pitfall II.sfc",
            "Plok!.sfc": "Plok!.sfc",
            "Pocky & Rocky.sfc": "Pocky & Rocky.sfc",
            "Pocky & Rocky 2.sfc": "Pocky & Rocky 2.sfc",
            "Porky Pig's Haunted Holiday.sfc": "Porky Pig's Haunted Holiday.sfc",
            "Power Drive.sfc": "Power Drive.sfc",
            "Power Instinct.sfc": "Power Instinct.sfc",
            "Power Moves.sfc": "Power Moves.sfc",
            "Power Piggs of the Dark Age.sfc": "Power Piggs of the Dark Age.sfc",
            "Power Rangers III.sfc": "Power Rangers 3.sfc",
            "Power Rangers IV.sfc": "Power Rangers 4.sfc",
            "Power Rangers Zeo - Battle Racers.sfc": "Power Rangers Zeo - Battle Racers.sfc",
            "Power Soukoban.sfc": "Power Soukoban.sfc",
            "PowerMonger.sfc": "PowerMonger.sfc",
            "Prehistorik Man.sfc": "Prehistorik Man.sfc",
            "Primal Rage.sfc": "Primal Rage.sfc",
            "Prince of Persia.sfc": "Prince of Persia.sfc",
            "Prince of Persia 2 - The Shadow & The Flame.sfc": "Prince of Persia 2 - The Shadow & The Flame.sfc",
            "Pro Quarterback.sfc": "Pro Quarterback.sfc",
            "Pro Yakyuu Nettou Puzzle Stadium.sfc": "Baseball Exciting Puzzle Stadium.sfc",
            "Psycho Dream.sfc": "Psycho Dream.sfc",
            "PTO - Pacific Theater of Operations.sfc": "P.T.O. - Pacific Theater of Operations.sfc",
            "PTO II - Pacific Theater of Operations.sfc": "P.T.O. II - Pacific Theater of Operations.sfc",
            "Puggsy.sfc": "Puggsy.sfc",
            "Punch-Out!!.sfc": "Punch-Out!!.sfc",
            "Push-Over.sfc": "Push-Over.sfc",
            "Q*bert 3.sfc": "Q*bert 3.sfc",
            "R-Type III - The Third Lightning.sfc": "R-Type III - The Third Lightning.sfc",
            "Race Drivin'.sfc": "Race Drivin'.sfc",
            "Radical Rex.sfc": "Radical Rex.sfc",
            "Raiden Trad.sfc": "Raiden Trad.sfc",
            "Rampart.sfc": "Rampart.sfc",
            "Ranma 1-2 - Akanekodan Teki Hihou.sfc": "Ranma 1-2 - Akanekodan Teki Hihou.sfc",
            "Ranma 1-2 - Chougi Ranbu Hen.sfc": "Ranma 1-2 - Chougi Ranbu Hen.sfc",
            "Ranma 1-2 - Hard Battle.sfc": "Ranma 1-2 - Hard Battle.sfc",
            "Ranma 1-2 - Super Battle.sfc": "Ranma 1-2 - Super Battle.sfc",
            "Rap Jam - Volume One.sfc": "Rap Jam - Volume One.sfc",
            "Realm.sfc": "Realm.sfc",
            "Red Line F-1 Racer.sfc": "Red Line F-1 Racer.sfc",
            "Relief Pitcher.sfc": "Relief Pitcher.sfc",
            "Ren & Stimpy Show, The.sfc": "Ren & Stimpy Show, The - Buckeroo$.sfc",
            "Riddick Bowe Boxing.sfc": "Riddick Bowe Boxing.sfc",
            "Rise of the Phoenix.sfc": "Rise of the Phoenix.sfc",
            "Rival Turf!.sfc": "Rival Turf!.sfc",
            "Road Riot 4WD.sfc": "Road Riot 4WD.sfc",
            "Road Runner's Death Valley Rally.sfc": "Road Runner's Death Valley Rally.sfc",
            "RoboCop 3.sfc": "RoboCop 3.sfc",
            "RoboCop vs The Terminator.sfc": "RoboCop vs The Terminator.sfc",
            "Robotrek.sfc": "Robotrek.sfc",
            "Rock N' Roll Racing.sfc": "Rock N' Roll Racing.sfc",
            "Rocketeer, The.sfc": "Rocketeer, The.sfc",
            "Rocko's Modern Life - Spunky's Dangerous Day.sfc": "Rocko's Modern Life - Spunky's Dangerous Day.sfc",
            "Rocky Rodent.sfc": "Rocky Rodent.sfc",
            "Roger Clemens' MVP Baseball.sfc": "Roger Clemens' MVP Baseball.sfc",
            "Romancing SaGa.sfc": "Romancing SaGa.sfc",
            "Romancing SaGa 2.sfc": "Romancing SaGa 2.sfc",
            "Romancing SaGa 3.sfc": "Romancing SaGa 3.sfc",
            "Rudra no Hihou.sfc": "Rudra no Hihou.sfc",
            "Run Saber.sfc": "Run Saber.sfc",
            "Rushing Beat Ran - Fukusei Toshi.sfc": "Rushing Beat Ran - Fukusei Toshi.sfc",
            "Rushing Beat Shura.sfc": "Rushing Beat Shura.sfc",
            "S.O.S..sfc": "S.O.S..sfc",
            "Sailor Moon S - Kurukkurin.sfc": "Sailor Moon S - Kurukkurin.sfc",
            "Sailor Moon S - Kurrenai.png": "Sailor Moon S - Kurrenai.sfc",
            "Saturday Night Slam Masters.sfc": "Saturday Night Slam Masters.sfc",
            "Scooby-Doo.sfc": "Scooby-Doo Mystery.sfc",
            "SD Gundam G Next - Senyou Rom Pack.sfc": "SD Gundam G Next - Senyou Rom Pack.sfc",
            "SD Gundam GX.sfc": "SD Gundam GX.sfc",
            "Secret of Evermore.sfc": "Secret of Evermore.sfc",
            "Secret of Mana.sfc": "Secret of Mana.sfc",
            "Seiken Densetsu 3.sfc": "Seiken Densetsu 3.sfc",
            "Seiken Densetsu.sfc": "Seiken Densetsu.sfc",
            "Senshi Heroes Saga.sfc": "Senshi Heroes Saga.sfc",
            "Shanghai II - Dragon's Eye.sfc": "Shanghai II - Dragon's Eye.sfc",
            "Shaq Fu.sfc": "Shaq-Fu.sfc",
            "Shien's Revenge.sfc": "Shien's Revenge.sfc",
            "Shin Kidou Senki Gundam Wing - Endless Duel.sfc": "Mobile Suit Gundam Wing - Endless Duel.sfc",
            "Shin Megami Tensei.sfc": "Shin Megami Tensei.sfc",
            "Shin Megami Tensei II.sfc": "Shin Megami Tensei II.sfc",
            "Shin Megami Tensei If....sfc": "Shin Megami Tensei If....sfc",
            "Shining Soul II.sfc": "Shining Soul II.sfc",
            "Shockwave.sfc": "Shockwave.sfc",
            "Side Pocket.sfc": "Side Pocket.sfc",
            "Sim Ant.sfc": "SimAnt - The Electronic Ant Colony.sfc",
            "Sim City.sfc": "SimCity.sfc",
            "SimCity 2000.sfc": "SimCity 2000 - The Ultimate City Simulator.sfc",
            "SimEarth - The Living Planet.sfc": "SimEarth - The Living Planet.sfc",
            "Sink or Swim.sfc": "Sink or Swim.sfc",
            "Skuljagger - Revolt of the Westicans.sfc": "Skuljagger - Revolt of the Westicans.sfc",
            "Sky Blazer.sfc": "Sky Blazer.sfc",
            "SmartBall.sfc": "SmartBall.sfc",
            "Snow White in Happily Ever After.sfc": "Snow White in Happily Ever After.sfc",
            "Snowboard Kids 2.sfc": "Snowboard Kids 2.sfc",
            "Soccer Shootout.sfc": "Soccer Shootout.sfc",
            "Soldiers of Fortune.sfc": "Soldiers of Fortune.sfc",
            "Sonic Blast Man.sfc": "Sonic Blast Man.sfc",
            "Sonic Blast Man II.sfc": "Sonic Blast Man II.sfc",
            "Soul Blazer.sfc": "Soul Blazer.sfc",
            "Space Ace.sfc": "Space Ace.sfc",
            "Space Funky B.O.B..sfc": "Space Funky B.O.B..sfc",
            "Space Invaders.sfc": "Space Invaders.sfc",
            "Space Megaforce.sfc": "Space Megaforce.sfc",
            "Sparkster.sfc": "Sparkster.sfc",
            "Spawn.sfc": "Spawn.sfc",
            "Speed Racer in My Most Dangerous Adventures.sfc": "Speed Racer.sfc",
            "Speedy Gonzales in Los Gatos Bandidos.sfc": "Speedy Gonzales in Los Gatos Bandidos.sfc",
            "Spider-Man - Lethal Foes.sfc": "Spider-Man - Lethal Foes.sfc",
            "Spider-Man - Maximum Carnage.sfc": "Spider-Man - Maximum Carnage.sfc",
            "Spider-Man - Separation Anxiety.sfc": "Spider-Man - Separation Anxiety.sfc",
            "Spider-Man and Venom - Maximum Carnage.sfc": "Spider-Man & Venom - Maximum Carnage.sfc",
            "Spider-Man and the X-Men in Arcade's Revenge.sfc": "Spider-Man - X-Men - Arcade's Revenge.sfc",
            "Spider-Man.sfc": "Spider-Man.sfc",
            "Spindizzy Worlds.sfc": "Spindizzy Worlds.sfc",
            "Sporting News Baseball.sfc": "Sporting News Baseball.sfc",
            "Star Fox 2.sfc": "Star Fox 2.sfc",
            "Star Fox.sfc": "Star Fox.sfc",
            "Star Ocean.sfc": "Star Ocean.sfc",
            "Star Trek - Deep Space Nine - Crossroads of Time.sfc": "Star Trek - Deep Space Nine - Crossroads of Time.sfc",
            "Star Trek - Starfleet Academy.sfc": "Star Trek - Starfleet Academy.sfc",
            "Star Trek - The Next Generation - Future's Past.sfc": "Star Trek - The Next Generation - Future's Past.sfc",
            "Stargate.sfc": "Stargate.sfc",
            "Steel Talons.sfc": "Steel Talons.sfc",
            "Sterling Sharpe - End 2 End.sfc": "Sterling Sharpe - End 2 End.sfc",
            "Stone Protectors.sfc": "Stone Protectors.sfc",
            "Street Fighter Alpha 2.sfc": "Street Fighter Alpha 2.sfc",
            "Street Fighter II - The World Warrior.sfc": "Street Fighter II - The World Warrior.sfc",
            "Street Fighter II Turbo - Hyper Fighting.sfc": "Street Fighter II Turbo - Hyper Fighting.sfc",
            "Street Fighter II.sfc": "Street Fighter II.sfc",
            "Street Hockey '95.sfc": "Street Hockey '95.sfc",
            "Stunt Race FX.sfc": "Stunt Race FX.sfc",
            "Sugoi Hebereke.sfc": "Sugoi Hebereke.sfc",
            "Super Adventure Island.sfc": "Super Adventure Island.sfc",
            "Super Adventure Island II.sfc": "Super Adventure Island II.sfc",
            "Super Alfred Chicken.sfc": "Super Alfred Chicken.sfc",
            "Super Aquatic Games Starring the Aquabats, The.sfc": "Super Aquatic Games Starring the Aquabats, The.sfc",
            "Super Back to the Future Part II.sfc": "Super Back to the Future Part II.sfc",
            "Super Baseball 2020.sfc": "Super Baseball 2020.sfc",
            "Super Bases Loaded.sfc": "Super Bases Loaded.sfc",
            "Super Bases Loaded 2.sfc": "Super Bases Loaded 2.sfc",
            "Super Bases Loaded 3 - License to Steal.sfc": "Super Bases Loaded 3 - License to Steal.sfc",
            "Super Batter Up.sfc": "Super Batter Up.sfc",
            "Super Battleship.sfc": "Super Battleship.sfc",
            "Super Battletank 2.sfc": "Super Battletank 2.sfc",
            "Super Battletank.sfc": "Super Battletank.sfc",
            "Super Black Bass.sfc": "Super Black Bass.sfc",
            "Super Bomberman.sfc": "Super Bomberman.sfc",
            "Super Bomberman 2.sfc": "Super Bomberman 2.sfc",
            "Super Bonk.sfc": "Super Bonk.sfc",
            "Super Bowling.sfc": "Super Bowling.sfc",
            "Super Buster Bros..sfc": "Super Buster Bros..sfc",
            "Super Caesars Palace.sfc": "Super Caesars Palace.sfc",
            "Super Castlevania IV.sfc": "Super Castlevania IV.sfc",
            "Super Chase H.Q..sfc": "Super Chase H.Q..sfc",
            "Super Conflict - The Mideast.sfc": "Super Conflict - The Mideast.sfc",
            "Super Double Dragon.sfc": "Super Double Dragon.sfc",
            "Super Earth Defense Force.sfc": "Super Earth Defense Force.sfc",
            "Super Family Circuit.sfc": "Super Family Circuit.sfc",
            "Super Ghouls 'N Ghosts.sfc": "Super Ghouls'n Ghosts.sfc",
            "Super Goal! 2.sfc": "Super Goal! 2.sfc",
            "Super Godzilla.sfc": "Super Godzilla.sfc",
            "Super High Impact.sfc": "Super High Impact.sfc",
            "Super Ice Hockey.sfc": "Super Ice Hockey.sfc",
            "Super James Pond.sfc": "Super James Pond.sfc",
            "Super Loopz.sfc": "Super Loopz.sfc",
            "Super Mario All-Stars.sfc": "Super Mario All-Stars.sfc",
            "Super Mario All-Stars + Super Mario World.sfc": "Super Mario All-Stars + Super Mario World.sfc",
            "Super Mario Kart.sfc": "Super Mario Kart.sfc",
            "Super Mario RPG - Legend of the Seven Stars.sfc": "Super Mario RPG - Legend of the Seven Stars.sfc",
            "Super Mario World.sfc": "Super Mario World.sfc",
            "Super Mario World 2 - Yoshi's Island.sfc": "Super Mario World 2 - Yoshi's Island.sfc",
            "Super Metroid.sfc": "Super Metroid.sfc",
            "Super Morph.sfc": "Super Morph.sfc",
            "Super Ninja Boy.sfc": "Super Ninja Boy.sfc",
            "Super Noah's Ark 3D.sfc": "Super Noah's Ark 3D.sfc",
            "Super Nova.sfc": "Super Nova.sfc",
            "Super Off Road - The Baja.sfc": "Super Off Road - The Baja.sfc",
            "Super Pinball - Behind the Mask.sfc": "Super Pinball - Behind the Mask.sfc",
            "Super Play Action Football.sfc": "Super Play Action Football.sfc",
            "Super Punch-Out!!.sfc": "Super Punch-Out!!.sfc",
            "Super Putty.sfc": "Super Putty.sfc",
            "Super R.B.I. Baseball.sfc": "Super R.B.I. Baseball.sfc",
            "Super Shadow of the Beast.sfc": "Super Shadow of the Beast.sfc",
            "Super Slap Shot.sfc": "Super Slap Shot.sfc",
            "Super Smash T.V..sfc": "Super Smash T.V..sfc",
            "Super Soccer.sfc": "Super Soccer.sfc",
            "Super Soccer Champ.sfc": "Super Soccer Champ.sfc",
            "Super Solitaire.sfc": "Super Solitaire.sfc",
            "Super Star Wars.sfc": "Super Star Wars.sfc",
            "Super Star Wars - Return of the Jedi.sfc": "Super Star Wars - Return of the Jedi.sfc",
            "Super Star Wars - The Empire Strikes Back.sfc": "Super Star Wars - The Empire Strikes Back.sfc",
            "Super Strike Eagle.sfc": "Super Strike Eagle.sfc",
            "Super Street Fighter II - The New Challengers.sfc": "Super Street Fighter II - The New Challengers.sfc",
            "Super SWIV.sfc": "Super SWIV.sfc",
            "Super Tennis.sfc": "Super Tennis.sfc",
            "Super Troll Islands.sfc": "Super Troll Islands.sfc",
            "Super Turrican.sfc": "Super Turrican.sfc",
            "Super Turrican 2.sfc": "Super Turrican 2.sfc",
            "Super Valis IV.sfc": "Super Valis IV.sfc",
            "Super Widget.sfc": "Super Widget.sfc",
            "Suzuka 8 Hours.sfc": "Suzuka 8 Hours.sfc",
            "Swat Kats - The Radical Squadron.sfc": "Swat Kats - The Radical Squadron.sfc",
            "Sword Master.sfc": "Sword Master.sfc",
            "Syndicate.sfc": "Syndicate.sfc",
            "T2 - The Arcade Game.sfc": "T2 - The Arcade Game.sfc",
            "T2 - The Arcade Game.sfc": "T2 - The Arcade Game.sfc",
            "T2 - The Terminator.sfc": "T2 - The Terminator.sfc",
            "Tactics Ogre - Let Us Cling Together.sfc": "Tactics Ogre - Let Us Cling Together.sfc",
            "Takahashi Meijin no Daibouken Jima.sfc": "Adventure Island.sfc",
            "Takahashi Meijin no Daibouken Jima II.sfc": "Adventure Island II.sfc",
            "Takahashi Meijin no Daibouken Jima III.sfc": "Adventure Island III.sfc",
            "Takahashi Meijin no Daibouken Jima IV.sfc": "Adventure Island IV.sfc",
            "Takahashi Meijin no Daibouken Jima V.sfc": "Adventure Island V.sfc",
            "Taikyoku Igo - Goliath.sfc": "Taikyoku Igo - Goliath.sfc",
            "Tales of Phantasia.sfc": "Tales of Phantasia.sfc",
            "Tarzan - Lord of the Jungle.sfc": "Tarzan - Lord of the Jungle.sfc",
            "Taz-Mania.sfc": "Taz-Mania.sfc",
            "Teenage Mutant Ninja Turtles IV - Turtles in Time.sfc": "Teenage Mutant Ninja Turtles IV - Turtles in Time.sfc",
            "Teenage Mutant Ninja Turtles Tournament Fighters.sfc": "Teenage Mutant Ninja Turtles Tournament Fighters.sfc",
            "Tekken 2.sfc": "Tekken 2.sfc",
            "Tekken 3.sfc": "Tekken 3.sfc",
            "Tekken.sfc": "Tekken.sfc",
            "Terminator 2 - Judgment Day.sfc": "Terminator 2 - Judgment Day.sfc",
            "Terminator, The.sfc": "Terminator, The.sfc",
            "Test Drive II - The Duel.sfc": "Test Drive II - The Duel.sfc",
            "Tetris 2.sfc": "Tetris 2.sfc",
            "Tetris & Dr. Mario.sfc": "Tetris & Dr. Mario.sfc",
            "Tetris Attack.sfc": "Tetris Attack.sfc",
            "Tetris Battle Gaiden.sfc": "Tetris Battle Gaiden.sfc",
            "Tetsuwan Atom.sfc": "Astro Boy.sfc",
            "The Addams Family.sfc": "Addams Family, The.sfc",
            "The Adventures of Batman & Robin.sfc": "Adventures of Batman & Robin, The.sfc",
            "The Chessmaster.sfc": "Chessmaster, The.sfc",
            "The Death and Return of Superman.sfc": "Death and Return of Superman, The.sfc",
            "The Flintstones.sfc": "Flintstones, The.sfc",
            "The Flintstones - The Treasure of Sierra Madrock.sfc": "Flintstones, The - The Treasure of Sierra Madrock.sfc",
            "The Hunt for Red October.sfc": "Hunt for Red October, The.sfc",
            "The Ignition Factor.sfc": "Ignition Factor, The.sfc",
            "The Incredible Hulk.sfc": "Incredible Hulk, The.sfc",
            "The Incredible Hulk.sfc": "Incredible Hulk, The.sfc",
            "The Itchy & Scratchy Game.sfc": "Itchy & Scratchy Game, The.sfc",
            "The Jungle Book.sfc": "Jungle Book, The.sfc",
            "The King of Dragons.sfc": "King of Dragons.sfc",
            "The Legend of Zelda - A Link to the Past.sfc": "Legend of Zelda, The - A Link to the Past.sfc",
            "The Lion King.sfc": "Lion King, The.sfc",
            "The Magical Quest Starring Mickey Mouse.sfc": "Magical Quest Starring Mickey Mouse.sfc",
            "The Mask.sfc": "Mask, The.sfc",
            "The Peace Keepers.sfc": "Peace Keepers, The.sfc",
            "The Ren & Stimpy Show.sfc": "Ren & Stimpy Show, The.sfc",
            "The Ren & Stimpy Show - Time Warp.sfc": "Ren & Stimpy Show, The - Time Warp.sfc",
            "The Simpsons - Bart's Nightmare.sfc": "Simpsons, The - Bart's Nightmare.sfc",
            "The Simpsons - Itchy & Scratchy Game.sfc": "Simpsons, The - Itchy & Scratchy Game.sfc",
            "The Smurfs.sfc": "Smurfs, The.sfc",
            "The Smurfs - Travel the World.sfc": "Smurfs, The - Travel the World.sfc",
            "The Tick.sfc": "Tick, The.sfc",
            "The Wizard of Oz.sfc": "Wizard of Oz, The.sfc",
            "Theme Park.sfc": "Theme Park.sfc",
            "Thoroughbred Breeder.sfc": "Thoroughbred Breeder.sfc",
            "Thunder Spirits.sfc": "Thunder Spirits.sfc",
            "Tick, The.sfc": "Tick, The.sfc",
            "Timon & Pumbaa's Jungle Games.sfc": "Timon & Pumbaa's Jungle Games.sfc",
            "Tin Star.sfc": "Tin Star.sfc",
            "Tiny Toon Adventures - Buster Busts Loose!.sfc": "Tiny Toon Adventures - Buster Busts Loose!.sfc",
            "Tiny Toon Adventures - Wacky Sports Challenge.sfc": "Tiny Toon Adventures - Wacky Sports Challenge.sfc",
            "Tom & Jerry.sfc": "Tom and Jerry.sfc",
            "Tom & Jerry - The Ultimate Game of Cat and Mouse!.sfc": "Tom & Jerry - The Ultimate Game of Cat and Mouse!.sfc",
            "Tom & Jerry.sfc": "Tom and Jerry.sfc",
            "Top Gear.sfc": "Top Gear.sfc",
            "Top Gear 2.sfc": "Top Gear 2.sfc",
            "Top Gear 3000.sfc": "Top Gear 3000.sfc",
            "Total Carnage.sfc": "Total Carnage.sfc",
            "Toys.sfc": "Toys - Let the Toy Wars Begin!.sfc",
            "Troddlers.sfc": "Troddlers.sfc",
            "Troy Aikman NFL Football.sfc": "Troy Aikman NFL Football.sfc",
            "True Lies.sfc": "True Lies.sfc",
            "True Golf Classics - Pebble Beach Golf Links.sfc": "True Golf Classics - Pebble Beach Golf Links.sfc",
            "True Golf Classics - Waialae Country Club.sfc": "True Golf Classics - Waialae Country Club.sfc",
            "True Golf Classics - Wicked 18.sfc": "True Golf Classics - Wicked 18.sfc",
            "Tuff E Nuff.sfc": "Tuff E Nuff.sfc",
            "Turn and Burn - No-Fly Zone.sfc": "Turn and Burn - No-Fly Zone.sfc",
            "Turok - Dinosaur Hunter.sfc": "Turok - Dinosaur Hunter.sfc",
            "Twisted Tales of Spike McFang, The.sfc": "Twisted Tales of Spike McFang, The.sfc",
            "U.N. Squadron.sfc": "U.N. Squadron.sfc",
            "Ultima VI - The False Prophet.sfc": "Ultima VI - The False Prophet.sfc",
            "Ultima VII - The Black Gate.sfc": "Ultima VII - The Black Gate.sfc",
            "Ultima - Runes of Virtue II.sfc": "Ultima - Runes of Virtue II.sfc",
            "Ultimate Fighter.sfc": "Ultimate Fighter.sfc",
            "Ultimate Mortal Kombat 3.sfc": "Ultimate Mortal Kombat 3.sfc",
            "Ultra Seven.sfc": "Ultra Seven.sfc",
            "Uncharted Waters.sfc": "Uncharted Waters.sfc",
            "Uncharted Waters - New Horizons.sfc": "Uncharted Waters - New Horizons.sfc",
            "Uniracers.sfc": "Uniracers.sfc",
            "Untouchables, The.sfc": "Untouchables, The.sfc",
            "Urban Strike - The Sequel to Jungle Strike.sfc": "Urban Strike - The Sequel to Jungle Strike.sfc",
            "Utopia - The Creation of a Nation.sfc": "Utopia - The Creation of a Nation.sfc",
            "V.R. Fighter.sfc": "V.R. Fighter.sfc",
            "V-Rally 97 Championship Edition.sfc": "V-Rally 97 Championship Edition.sfc",
            "Vortex.sfc": "Vortex.sfc",
            "Wagyan Paradise.sfc": "Wagyan Paradise.sfc",
            "War 2410.sfc": "War 2410.sfc",
            "War 3010 - The Revolution.sfc": "War 3010 - The Revolution.sfc",
            "Warlock.sfc": "Warlock.sfc",
            "WarpSpeed.sfc": "WarpSpeed.sfc",
            "Warriors of Fate.sfc": "Warriors of Fate.sfc",
            "Wayne Gretzky and the NHLPA All-Stars.sfc": "Wayne Gretzky and the NHLPA All-Stars.sfc",
            "Wayne's World.sfc": "Wayne's World.sfc",
            "WCW SuperBrawl Wrestling.sfc": "WCW SuperBrawl Wrestling.sfc",
            "Weapon Lord.sfc": "WeaponLord.sfc",
            "We're Back! A Dinosaur's Story.sfc": "We're Back! A Dinosaur's Story.sfc",
            "Wheel of Fortune.sfc": "Wheel of Fortune.sfc",
            "Where in the World is Carmen Sandiego.sfc": "Where in the World is Carmen Sandiego.sfc",
            "Where in Time is Carmen Sandiego.sfc": "Where in Time is Carmen Sandiego.sfc",
            "Whizz.sfc": "Whizz.sfc",
            "Wild C.A.T.S.sfc": "Wild C.A.T.S.sfc",
            "Wild Guns.sfc": "Wild Guns.sfc",
            "WildSnake.sfc": "Wild Snake.sfc",
            "Williams Arcade's Greatest Hits.sfc": "Williams Arcade's Greatest Hits.sfc",
            "Wing Commander.sfc": "Wing Commander.sfc",
            "Wing Commander - The Secret Missions.sfc": "Wing Commander - The Secret Missions.sfc",
            "Wings 2 - Aces High.sfc": "Wings 2 - Aces High.sfc",
            "Winter Extreme - Skiing & Snowboarding.sfc": "Winter Extreme - Skiing & Snowboarding.sfc",
            "Wolverine - Adamantium Rage.sfc": "Wolverine - Adamantium Rage.sfc",
            "Wordtris.sfc": "Wordtris.sfc",
            "World Champ - Super Boxing Great Fight.sfc": "World Champ - Super Boxing Great Fight.sfc",
            "World Cup USA '94.sfc": "World Cup USA '94.sfc",
            "World Heroes.sfc": "World Heroes.sfc",
            "World Heroes 2.sfc": "World Heroes 2.sfc",
            "World League Soccer.sfc": "World League Soccer.sfc",
            "World League Soccer '95.sfc": "World League Soccer '95.sfc",
            "World Masters Golf.sfc": "World Masters Golf.sfc",
            "World Soccer 94.sfc": "World Soccer 94.sfc",
            "World Soccer 95.sfc": "World Soccer 95.sfc",
            "WWF Raw.sfc": "WWF Raw.sfc",
            "WWF Royal Rumble.sfc": "WWF Royal Rumble.sfc",
            "WWF Super WrestleMania.sfc": "WWF Super WrestleMania.sfc",
            "X-Men - Mutant Apocalypse.sfc": "X-Men - Mutant Apocalypse.sfc",
            "Xardion.sfc": "Xardion.sfc",
            "Yogi Bear.sfc": "Adventures of Yogi Bear.sfc",
            "Ys III - Wanderers from Ys.sfc": "Ys III - Wanderers from Ys.sfc",
            "Yuu Yuu Hakusho.sfc": "Yuu Yuu Hakusho.sfc",
            "Zero The Kamikaze Squirrel.sfc": "Zero The Kamikaze Squirrel.sfc",
            "Zombies Ate My Neighbors.sfc": "Zombies Ate My Neighbors.sfc",
            "Zool.sfc": "Zool - Ninja of the 'Nth' Dimension.sfc",
            "Zoop.sfc": "Zoop.sfc",
            "Mega Man VII.sfc": "Mega Man 7.sfc",
            "Yogi Bear.sfc": "Adventures of Yogi Bear.sfc",
            "Beethoven's 2nd.sfc": "Beethoven The Ultimate Canine Caper.sfc",
            "Ballz 3D.sfc": "Ballz 3D Fighting at Its Ballziest.sfc",
            "Blazeon.sfc": "BlaZeon - The Bio-Cyborg Challenge.sfc",
            "Bronkie Health Hero.sfc": "Bronkie the Bronchiasaurus.sfc",
            "Choplifter III.sfc": "Choplifter III - Rescue & Survive.sfc",
            "College Slam Basketball.sfc": "College Slam.sfc",
            "Mutant Chronicles - Doom Troopers.sfc": "Doom Troopers.sfc",
            "Mountain Bike Rally.sfc": "Exertainment Mountain Bike Rally.sfc",
            "Hagane.sfc": "Hagane - The Final Conflict.sfc",
            "Mickey Mania.sfc": "Mickey Mania - The Timeless Adventures of Mickey Mouse.sfc",
            "Pink Panther in Pink Goes to Hollywood.sfc": "Pink Goes to Hollywood.sfc",
            "Scooby-Doo.sfc": "Scooby-Doo Mystery.sfc",
            "Super NES Super Scope 6.sfc": "Super Scope 6.sfc",
            "Magic Johnson's Super Slam Dunk.sfc": "Super Slam Dunk.sfc",
            "Test Drive II - The Duel.sfc": "Duel, The - Test Drive II.sfc",
            "Pebble Beach Golf Links.sfc": "True Golf Classics - Pebble Beach Golf Links.sfc",
            "Waialae Country Club.sfc": "True Golf Classics - Waialae Country Club.sfc",
            "Wicked 18 Golf.sfc": "True Golf Classics - Wicked 18.sfc",
            "Zool.sfc": "Zool - Ninja of the 'Nth' Dimension.sfc",
            "Battletoads-Double Dragon.sfc": "Battletoads & Double Dragon - The Ultimate Team.sfc"
            
        }

        for original_name, new_name in specific_renames.items():
            original_path = os.path.join(snes_folder, original_name)
            new_path = os.path.join(snes_folder, new_name)
            
            if os.path.exists(original_path):
                if os.path.exists(new_path):
                    print(f"File '{new_name}' already exists. Skipping rename for '{original_name}'.")
                else:
                    os.rename(original_path, new_path)
                    print(f"Renamed: {original_name} to {new_name}")
            else:
                print(f"File not found: {original_name}")

    except Exception as e:
        print(f'An error occurred: {e}')


def transfer_matching_cover_art(sfc_files, art_files):
    renamed_folder = os.path.join(os.getcwd(), "renamed cover art")
    if not os.path.exists(renamed_folder):
        os.makedirs(renamed_folder)

    for sfc_file in sfc_files:
        sfc_file_base = os.path.splitext(sfc_file)[0]
        for art_file in art_files:
            art_file_base = os.path.splitext(os.path.basename(art_file))[0]
            if art_file_base.lower() == sfc_file_base.lower():
                new_art_name = f"{sfc_file_base}.sfc.png"
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
    print("Thank you for using DAT SNES Wiiflow Tool!")
    answer = input("Would you like to see your listed SNES games? (yes/no): ").strip().lower()

    if answer == 'yes':
        sfc_files = list_snes_games()
        if sfc_files:
            print("Here are your SNES games:")
            for file in sfc_files:
                print(file)
            print("\n\n\nThese are the games I picked up!")
        else:
            print("No .sfc files present in the 'snes games' folder.")
            time.sleep(5)
            return
    else:
        print("Too Bad, So Sad...")
        time.sleep(3)
        sfc_files = list_snes_games()
        if sfc_files:
            print("Here are your SNES games:")
            for file in sfc_files:
                print(file)
            print("\n\n\nThese are the games I picked up!")
        else:
            print("No .sfc files present in the 'snes games' folder.")
            time.sleep(5)
            return

    if sfc_files:
        print("\n\n")
        
        answer = input("Would you like to check for duplicate titles? (yes/no): ").strip().lower()

        if answer == 'yes':
            source_folder = 'snes games'
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

        answer = input("Would you like to remove the version and region information from the title names?\nExample: 'SuperMarioWorld(USA).sfc' would be changed to 'SuperMarioWorld.sfc'\nYes or no? ").strip().lower()

        if answer == 'yes':
            snes_folder = os.path.join(os.getcwd(), "snes games")
            for file in sfc_files:
                base_name, ext = os.path.splitext(file)
                new_base_name = remove_version_region_info(base_name)
                new_file = new_base_name + ext
                
                if os.path.exists(os.path.join(snes_folder, new_file)):
                    print(f"File '{new_file}' already exists. Skipping rename for '{file}'.")
                else:
                    try:
                        os.rename(os.path.join(snes_folder, file), os.path.join(snes_folder, new_file))
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
                print("Here are the text files in the 'snes plain text names' folder:")
                for file in txt_files:
                    print(file)
                
                print("\n\n\n")
                answer = input("Would you like to match the names above to your SNES games and then rename them? (yes/no): ").strip().lower()

                if answer == 'yes':
                    snes_folder = os.path.join(os.getcwd(), "snes games")
                    matches = []
                    already_matched = set()
                    while True:
                        changes_made = False
                        sfc_files = list_snes_games()
                        for game_file in sfc_files:
                            if game_file in already_matched:
                                continue
                            game_name, _ = os.path.splitext(game_file)
                            best_match = find_best_match(game_name, txt_files)
                            if best_match:
                                matches.append((game_file, best_match))
                                new_file_name = os.path.splitext(best_match)[0] + ".sfc"
                                if os.path.exists(os.path.join(snes_folder, new_file_name)):
                                    print(f"File '{new_file_name}' already exists. Skipping rename for '{game_file}'.")
                                else:
                                    try:
                                        os.rename(os.path.join(snes_folder, game_file), os.path.join(snes_folder, new_file_name))
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

                    print("\n\n\nYour SNES games have been renamed!\n\n\n")
                    answer = input("Would you like to start working on your boxart now? (yes/no): ").strip().lower()

                    if answer == 'yes':
                        art_files = list_cover_art_files()
                        if art_files:
                            answer = input("First thing we should do is remove all of the version information from the boxart titles. Sound good? (yes/no): ").strip().lower()

                            if answer == 'yes':
                                art_folder = os.path.join(os.getcwd(), "snes cover art")
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
                                sfc_file_titles = [os.path.splitext(f)[0] for f in sfc_files]
                                already_matched_art = set()
                                while True:
                                    changes_made = False
                                    for art_file in art_files:
                                        if art_file in already_matched_art:
                                            continue
                                        art_file_title = os.path.splitext(os.path.basename(art_file))[0]
                                        best_match = find_best_match(art_file_title, sfc_file_titles)
                                        if best_match:
                                            art_matches.append((best_match + ".sfc", art_file))
                                            changes_made = True
                                            already_matched_art.add(art_file)
                                            print(f"Matched '{art_file}' to '{best_match}'")
                                    if not changes_made:
                                        break

                                if art_matches:
                                    for game_file, art_file in art_matches:
                                        game_base, _ = os.path.splitext(game_file)
                                        new_art_name = game_base + ".sfc.png"
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

                                transfer_matching_cover_art(sfc_files, art_files)
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
        snes_games_folder = 'snes games'
        renamed_cover_art_folder = 'renamed cover art'
        unmatched_games_folder = 'unmatched games'

        if not os.path.exists(unmatched_games_folder):
            os.makedirs(unmatched_games_folder)

        snes_games = [f for f in os.listdir(snes_games_folder) if f.endswith('.sfc')]
        renamed_cover_art = [f for f in os.listdir(renamed_cover_art_folder) if f.endswith('.sfc.png')]

        for game in snes_games:
            expected_cover_art_name = game + ".png"
            if expected_cover_art_name not in renamed_cover_art:
                print(f"\nNo match found for: {game}. Moving to 'unmatched games' folder.")
                shutil.move(os.path.join(snes_games_folder, game), os.path.join(unmatched_games_folder, game))
            else:
                print(f"Match found for: {game}")

    print("\n\n\nAll Done!")
    print("This tool was created by Below Average Gaming!")
    print("""
d8888b.  .d8b.  d888888b      .d8888. d8b   db d88888b .d8888.         
88  `8D d8' `8b `~~88~~'      88'  YP 888o  88 88'     88'  YP         
88   88 88ooo88    88         `8bo.   88V8o 88 88ooooo `8bo.           
88   88 88~~~88    88           `Y8b. 88 V8o88 88~~~~~   `Y8b.         
88  .8D 88   88    88         db   8D 88  V888 88.     db   8D         
Y8888D' YP   YP    YP         `8888Y' VP   V8P Y88888P `8888Y'         
                                                                       
                                                                       
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
