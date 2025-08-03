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
    zip_files = [f for f in os.listdir(snes_folder) if f.endswith('.zip')]

    if not zip_files:
        print('No .zip files present in the "snes games" folder.')
        time.sleep(5)
        return False

    return zip_files

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
            "Mega Man VII.zip": "Mega Man 7.zip",
            "3 Ninjas Kick Back.zip": "3 Ninjas Kick Back.zip",
            "A Bug's Life.zip": "Bug's Life, A.zip",
            "A.S.P. Air Strike Patrol.zip": "A.S.P. - Air Strike Patrol.zip",
            "AAAHH!!! Real Monsters.zip": "Aaahh!!! Real Monsters.zip",
            "ABC Monday Night Football.zip": "ABC Monday Night Football.zip",
            "Accelebrid.zip": "Accele Brid.zip",
            "ACME Animation Factory.zip": "ACME Animation Factory.zip",
            "ActRaiser.zip": "ActRaiser.zip",
            "ActRaiser 2.zip": "ActRaiser 2.zip",
            "AD&D - Eye of the Beholder.zip": "Advanced Dungeons & Dragons - Eye of the Beholder.zip",
            "Addams Family Values.zip": "Addams Family Values.zip",
            "Addams Family, The.zip": "Addams Family, The.zip",
            "Addams Family, The - Pugsley's Scavenger Hunt.zip": "Addams Family, The - Pugsley's Scavenger Hunt.zip",
            "Adventures of Batman & Robin, The.zip": "Adventures of Batman & Robin, The.zip",
            "Adventures of Dr. Franken, The.zip": "Adventures of Dr. Franken, The.zip",
            "Adventures of Kid Kleets, The.zip": "Adventures of Kid Kleets, The.zip",
            "Adventures of Rocky and Bullwinkle and Friends, The.zip": "Adventures of Rocky and Bullwinkle and Friends, The.zip",
            "Aero Fighters.zip": "Aero Fighters.zip",
            "Aero the Acro-Bat.zip": "Aero the Acro-Bat.zip",
            "Aero the Acro-Bat 2.zip": "Aero the Acro-Bat 2.zip",
            "Aerobiz.zip": "Aerobiz.zip",
            "Aerobiz Supersonic.zip": "Aerobiz Supersonic.zip",
            "Air Cavalry.zip": "Air Cavalry.zip",
            "Al Unser Jr's Road to the Top.zip": "Al Unser Jr.'s Road to the Top.zip",
            "Aladdin.zip": "Aladdin.zip",
            "Alcahest.zip": "Alcahest.zip",
            "Alien 3.zip": "Alien 3.zip",
            "Alien vs. Predator.zip": "Alien vs. Predator.zip",
            "American Gladiators.zip": "American Gladiators.zip",
            "American Tail, An - Fievel Goes West.zip": "American Tail, An - Fievel Goes West.zip",
            "Ancient Magic - Bazoo! Mahou Sekai.zip": "Ancient Magic - Bazoo! World of Magic.zip",
            "Andre Agassi Tennis.zip": "Andre Agassi Tennis.zip",
            "Animaniacs.zip": "Animaniacs.zip",
            "Arabian Nights - Sabaku no Seirei Ou.zip": "Arabian Nights - Desert Spirit King.zip",
            "Arcade's Greatest Hits.zip": "Williams Arcade's Greatest Hits.zip",
            "Arcade's Greatest Hits - The Atari Collection 1.zip": "Arcade's Greatest Hits - The Atari Collection 1.zip",
            "Arcana.zip": "Arcana.zip",
            "Ardy Lightfoot.zip": "Ardy Lightfoot.zip",
            "Arkanoid - Doh It Again.zip": "Arkanoid - Doh It Again.zip",
            "Art of Fighting.zip": "Art of Fighting.zip",
            "Assault Suits Valken.zip": "Assault Suits Valken.zip",
            "Axelay.zip": "Axelay.zip",
            "B.O.B..zip": "B.O.B..zip",
            "Bahamut Lagoon.zip": "Bahamut Lagoon.zip",
            "Ball Bullet Gun.zip": "Ball Bullet Gun.zip",
            "Barbie Super Model.zip": "Barbie Super Model.zip",
            "Barbie Vacation Adventure.zip": "Barbie Vacation Adventure.zip",
            "Barkley Shut Up and Jam!.zip": "Barkley Shut Up and Jam!.zip",
            "Bass Masters Classic.zip": "BASS Masters Classic.zip",
            "Bass Masters Classic - Pro Edition.zip": "BASS Masters Classic - Pro Edition.zip",
            "Bassin's Black Bass.zip": "Bassin's Black Bass.zip",
            "Batman - Revenge of the Joker.zip": "Batman - Revenge of the Joker.zip",
            "Batman Forever.zip": "Batman Forever.zip",
            "Batman Returns.zip": "Batman Returns.zip",
            "Battle Blaze.zip": "Battle Blaze.zip",
            "Battle Cars.zip": "Battle Cars.zip",
            "Battle Clash.zip": "Battle Clash.zip",
            "Battle Grand Prix.zip": "Battle Grand Prix.zip",
            "Battletoads & Double Dragon - The Ultimate Team.zip": "Battletoads & Double Dragon - The Ultimate Team.zip",
            "Battletoads in Battlemaniacs.zip": "Battletoads in Battlemaniacs.zip",
            "Bazooka Blitzkrieg.zip": "Bazooka Blitzkrieg.zip",
            "Beauty and the Beast.zip": "Beauty and the Beast.zip",
            "Beavis and Butt-head.zip": "Beavis and Butt-Head.zip",
            "Bebe's Kids.zip": "Bebe's Kids.zip",
            "Best of the Best - Championship Karate.zip": "Best of the Best - Championship Karate.zip",
            "Big Sky Trooper.zip": "Big Sky Trooper.zip",
            "Biker Mice From Mars.zip": "Biker Mice from Mars.zip",
            "Bill Laimbeer's Combat Basketball.zip": "Bill Laimbeer's Combat Basketball.zip",
            "Bill Walsh College Football.zip": "Bill Walsh College Football.zip",
            "Bio Metal.zip": "BioMetal.zip",
            "Bishoujo Senshi Sailor Moon - Another Story.zip": "Sailor Moon - Another Story.zip",
            "Blackthorne.zip": "Blackthorne.zip",
            "Blues Brothers, The.zip": "Blues Brothers, The.zip",
            "Bobby's World.zip": "Bobby's World.zip",
            "Bonkers.zip": "Bonkers.zip",
            "Boogerman - A Pick and Flick Adventure.zip": "Boogerman - A Pick and Flick Adventure.zip",
            "Boxing Legends of the Ring.zip": "Boxing Legends of the Ring.zip",
            "Brain Lord.zip": "Brain Lord.zip",
            "Brainies, The.zip": "Brainies, The.zip",
            "Bram Stoker's Dracula.zip": "Bram Stoker's Dracula.zip",
            "Brandish.zip": "Brandish.zip",
            "Brandish 2 - The Planet Buster.zip": "Brandish 2 - The Planet Buster.zip",
            "Brawl Brothers.zip": "Brawl Brothers.zip",
            "BreakThru!.zip": "BreakThru!.zip",
            "Breath of Fire.zip": "Breath of Fire.zip",
            "Breath of Fire II.zip": "Breath of Fire II.zip",
            "Brett Hull Hockey '95.zip": "Brett Hull Hockey '95.zip",
            "Brett Hull Hockey.zip": "Brett Hull Hockey.zip",
            "Brunswick World Tournament of Champions.zip": "Brunswick World Tournament of Champions.zip",
            "Brutal - Paws of Fury.zip": "Brutal - Paws of Fury.zip",
            "Bubsy II.zip": "Bubsy II.zip",
            "Bubsy in Claws Encounters of the Furred Kind.zip": "Bubsy in Claws Encounters of the Furred Kind.zip",
            "Bugs Bunny - Rabbit Rampage.zip": "Bugs Bunny - Rabbit Rampage.zip",
            "Bulls Vs Blazers and the NBA Playoffs.zip": "Bulls vs Blazers and the NBA Playoffs.zip",
            "Bust-A-Move.zip": "Bust-A-Move.zip",
            "Cacoma Knight in Bizyland.zip": "Cacoma Knight in Bizyland.zip",
            "Cal Ripken Jr. Baseball.zip": "Cal Ripken Jr. Baseball.zip",
            "California Games II.zip": "California Games II.zip",
            "Cannondale Cup.zip": "Cannondale Cup.zip",
            "Capcom's MVP Football.zip": "Capcom's MVP Football.zip",
            "Capcom's Soccer Shootout.zip": "Capcom's Soccer Shootout.zip",
            "Captain America and The Avengers.zip": "Captain America and the Avengers.zip",
            "Captain Commando.zip": "Captain Commando.zip",
            "Captain Novolin.zip": "Captain Novolin.zip",
            "Carrier Aces.zip": "Carrier Aces.zip",
            "Casper.zip": "Casper.zip",
            "Castlevania - Dracula X.zip": "Castlevania - Dracula X.zip",
            "Champions World Class Soccer.zip": "Champions - World Class Soccer.zip",
            "Championship Pool.zip": "Championship Pool.zip",
            "Championship Soccer '94.zip": "Championship Soccer '94.zip",
            "Chavez.zip": "Chavez.zip",
            "Chavez II.zip": "Chavez II.zip",
            "Chessmaster, The.zip": "Chessmaster, The.zip",
            "Chester Cheetah - Too Cool to Fool.zip": "Chester Cheetah - Too Cool to Fool.zip",
            "Chester Cheetah - Wild Wild Quest.zip": "Chester Cheetah - Wild Wild Quest.zip",
            "Chrono Trigger.zip": "Chrono Trigger.zip",
            "Chuck Rock.zip": "Chuck Rock.zip",
            "Civilization.zip": "Civilization.zip",
            "Classic Kong Complete.zip": "Classic Kong.zip",
            "Clay Fighter.zip": "Clay Fighter.zip",
            "Clay Fighter - Tournament Edition.zip": "Clay Fighter - Tournament Edition.zip",
            "Clay Fighter 2 - Judgment Clay.zip": "Clay Fighter 2 - Judgment Clay.zip",
            "Claymates.zip": "Claymates.zip",
            "Claymates Demo.zip": "Claymates.zip",
            "Cliffhanger.zip": "Cliffhanger.zip",
            "Clock Tower.zip": "Clock Tower.zip",
            "Clue.zip": "Clue.zip",
            "College Football USA '97 - The Road to New Orleans.zip": "College Football USA '97 - The Road to New Orleans.zip",
            "College Slam Basketball.zip": "College Slam.zip",
            "Combatribes, The.zip": "Combatribes, The.zip",
            "Congo's Caper.zip": "Congo's Caper.zip",
            "Contra III - The Alien Wars.zip": "Contra III - The Alien Wars.zip",
            "Cool Spot.zip": "Cool Spot.zip",
            "Cool World.zip": "Cool World.zip",
            "Crystal Beans - From Dungeon Explorer.zip": "Crystal Beans From Dungeon Explorer.zip",
            "Cu-On-Pa SFC.zip": "Cu-On-Pa SFC.zip",
            "Cutthroat Island.zip": "Cutthroat Island.zip",
            "Cyber Knight.zip": "Cyber Knight.zip",
            "Cyber Spin.zip": "Cyber Spin.zip",
            "Cybernator.zip": "Cybernator.zip",
            "Cyborg 009.zip": "Cyborg 009.zip",
            "D-Force.zip": "D-Force.zip",
            "Daffy Duck - The Marvin Missions.zip": "Daffy Duck - The Marvin Missions.zip",
            "Darius Twin.zip": "Darius Twin.zip",
            "Dark Law - Meaning of Death.zip": "Dark Law - Meaning of Death.zip",
            "David Crane's Amazing Tennis.zip": "David Crane's Amazing Tennis.zip",
            "Death and Return of Superman, The.zip": "Death and Return of Superman, The.zip",
            "Demolition Man.zip": "Demolition Man.zip",
            "Demon's Crest.zip": "Demon's Crest.zip",
            "Dennis the Menace.zip": "Dennis the Menace.zip",
            "Der Langrisser.zip": "Der Langrisser.zip",
            "Desert Strike - Return to the Gulf.zip": "Desert Strike - Return to the Gulf.zip",
            "Dig & Spike Volleyball.zip": "Dig & Spike Volleyball.zip",
            "Digimon Adventure.zip": "Digimon Adventure.zip",
            "Dino City.zip": "DinoCity.zip",
            "Dirt Trax FX.zip": "Dirt Trax FX.zip",
            "Donald Duck and the Magical Hat.zip": "Donald Duck and the Magical Hat.zip",
            "Donkey Kong Country (Competition Cartridge).zip": "Donkey Kong Country - Competition Edition.zip",
            "Donkey Kong Country.zip": "Donkey Kong Country.zip",
            "Donkey Kong Country 2 - Diddy's Kong Quest.zip": "Donkey Kong Country 2 - Diddy's Kong Quest.zip",
            "Donkey Kong Country 3 - Dixie Kong's Double Trouble.zip": "Donkey Kong Country 3 - Dixie Kong's Double Trouble!.zip",
            "Doom.zip": "Doom.zip",
            "Doomsday Warrior.zip": "Doomsday Warrior.zip",
            "DoReMi Fantasy - Milon no DokiDoki Daibouken.zip": "DoReMi Fantasy - Milon's Quest.zip",
            "Dorke & Ymp.zip": "Dorke & Ymp.zip",
            "Dossun! Ganseki Battle.zip": "Dossun! Stone Battle.zip",
            "Double Dragon V - The Shadow Falls.zip": "Double Dragon V - The Shadow Falls.zip",
            "Dragon - The Bruce Lee Story.zip": "Dragon - The Bruce Lee Story.zip",
            "Dragon Ball Z - Hyper Dimension.zip": "Dragon Ball Z - Hyper Dimension.zip",
            "Dragon Ball Z - Super Butouden 3.zip": "Dragon Ball Z - Super Butouden 3.zip",
            "Dragon Ball Z - Super Butouden.zip": "Dragon Ball Z - Super Butouden.zip",
            "Dragon Ball Z - Super Saiya Densetsu.zip": "Dragon Ball Z - Super Butouden.zip",
            "Dragon Quest 1 and 2.zip": "Dragon Quest V.zip",
            "Dragon Quest I & II.zip": "Dragon Quest I & II.zip",
            "Dragon View.zip": "Dragon View.zip",
            "Dragon's Lair.zip": "Dragon's Lair.zip",
            "Dragon-Ball Z - Hyper Dimension.zip": "Dragon Ball Z - Hyper Dimension.zip",
            "Dragon-Ball Z - Super Butouden.zip": "Dragon Ball Z - Super Butouden.zip",
            "Dragon-Ball Z - Super Butouden 3.zip": "Dragon Ball Z - Super Butouden 3.zip",
            "Dragon-Ball Z - Super Gokuden Totsugeki Hen.zip": "Dragon Ball Z - Super Butouden 3.zip",
            "Dragon-Ball Z - Super Saiyan Densetsu.zip": "Dragon Ball Z - Super Butouden.zip",
            "Dragon-Ball-Z - Super Gokuden 2.zip": "Dragon Ball Z - Super Butouden 2.zip",
            "Drakkhen.zip": "Drakkhen.zip",
            "Dream TV.zip": "Dream TV.zip",
            "Dual Orb 2.zip": "Dual Orb II.zip",
            "Dual Orb II.zip": "Dual Orb II.zip",
            "Dungeon Master.zip": "Dungeon Master.zip",
            "E.V.O. Search for Eden.zip": "E.V.O. - Search For Eden.zip",
            "Earthbound.zip": "EarthBound.zip",
            "Earthworm Jim.zip": "Earthworm Jim.zip",
            "Earthworm Jim 2.zip": "Earthworm Jim 2.zip",
            "Eek! The Cat.zip": "Eek! The Cat.zip",
            "Elite Soccer.zip": "Elite Soccer.zip",
            "Emerald Dragon.zip": "Emerald Dragon.zip",
            "Emmitt Smith Football.zip": "Emmitt Smith Football.zip",
            "Energy Breaker.zip": "Energy Breaker.zip",
            "Equinox.zip": "Equinox.zip",
            "ESPN Baseball Tonight.zip": "ESPN Baseball Tonight.zip",
            "ESPN National Hockey Night.zip": "ESPN National Hockey Night.zip",
            "ESPN Speedworld.zip": "ESPN Speedworld.zip",
            "ESPN Sunday Night NFL.zip": "ESPN Sunday Night NFL.zip",
            "Extra Innings.zip": "Extra Innings.zip",
            "F1 Pole Position.zip": "F1 Pole Position.zip",
            "F1 ROC - Race of Champions.zip": "F1 ROC - Race of Champions.zip",
            "F1 ROC II - Race of Champions.zip": "F1 ROC II - Race of Champions.zip",
            "Faceball 2000.zip": "Faceball 2000.zip",
            "Famicom Tantei Club Part II.zip": "Famicom Detective Club Part II.zip",
            "Family Dog.zip": "Family Dog.zip",
            "Family Feud.zip": "Family Feud.zip",
            "Fatal Fury.zip": "Fatal Fury.zip",
            "Fatal Fury 2.zip": "Fatal Fury 2.zip",
            "Fatal Fury Special.zip": "Fatal Fury Special.zip",
            "Feda - the Emblem of Justice.zip": "Feda - The Emblem of Justice.zip",
            "FIFA International Soccer.zip": "FIFA International Soccer.zip",
            "FIFA Soccer 96.zip": "FIFA Soccer 96.zip",
            "Fighter's History.zip": "Fighter's History.zip",
            "Final Fantasy - Mystic Quest.zip": "Final Fantasy - Mystic Quest.zip",
            "Final Fantasy 4 - 10th Anniversary Edition.zip": "Final Fantasy IV - Ultima Edition.zip",
            "Final Fantasy 6.zip": "Final Fantasy VI.zip",
            "Final Fantasy II.zip": "Final Fantasy II.zip",
            "Final Fantasy III.zip": "Final Fantasy III.zip",
            "Final Fantasy V.zip": "Final Fantasy V.zip",
            "Final Fight.zip": "Final Fight.zip",
            "Final Fight 2.zip": "Final Fight 2.zip",
            "Final Fight 3.zip": "Final Fight 3.zip",
            "Final Fight Guy.zip": "Final Fight Guy.zip",
            "Fire Emblem - Thracia 776.zip": "Fire Emblem 5 - Thracia 776.zip",
            "Fire Striker.zip": "FireStriker.zip",
            "Firepower 2000.zip": "Firepower 2000.zip",
            "First Samurai.zip": "First Samurai.zip",
            "Flashback - The Quest for Identity.zip": "Flashback - The Quest for Identity.zip",
            "Flintstones, The.zip": "Flintstones, The.zip",
            "Flintstones, The - The Treasure of Sierra Madrock.zip": "Flintstones, The - The Treasure of Sierra Madrock.zip",
            "Flying Hero - Bugyuru no Daibouken.zip": "Flying Hero - Bugyuru's Adventure.zip",
            "Football Fury.zip": "Football Fury.zip",
            "Foreman For Real.zip": "Foreman for Real.zip",
            "Frank Thomas' Big Hurt Baseball.zip": "Frank Thomas Big Hurt Baseball.zip",
            "Frantic Flea.zip": "Frantic Flea.zip",
            "Frogger.zip": "Frogger.zip",
            "Front Mission - Gun Hazard.zip": "Front Mission - Gun Hazard.zip",
            "Front Mission.zip": "Front Mission.zip",
            "Full Throttle Racing.zip": "Full Throttle - All-American Racing.zip",
            "Fun 'N Games.zip": "Fun 'n Games.zip",
            "Funaki Masakatsu Hybrid Wrestler - Tougi Denshou.zip": "Funaki Masakatsu Hybrid Wrestler - Tougi Denshou.zip",
            "Gekitou Burning Pro Wrestling.zip": "Burning Pro Wrestling.zip",
            "Gemfire.zip": "Gemfire.zip",
            "Genghis Khan II - Clan of the Gray Wolf.zip": "Genghis Khan II - Clan of the Gray Wolf.zip",
            "George Foreman's KO Boxing.zip": "George Foreman's KO Boxing.zip",
            "Ghoul Patrol.zip": "Ghoul Patrol.zip",
            "Go Go Ackman.zip": "Go Go Ackman.zip",
            "Gods.zip": "Gods.zip",
            "Goof Troop.zip": "Goof Troop.zip",
            "GP-1.zip": "GP-1.zip",
            "GP-1 Part II.zip": "GP-1 - Part II.zip",
            "Gradius III.zip": "Gradius III.zip",
            "Great Circus Mystery Starring Mickey & Minnie, The.zip": "Great Circus Mystery Starring Mickey & Minnie, The.zip",
            "Great Waldo Search, The.zip": "Great Waldo Search, The.zip",
            "Gunple - Gunman's Proof.zip": "Ganpuru - Gunman's Proof.zip",
            "HAL's Hole in One Golf.zip": "HAL's Hole in One Golf.zip",
            "Hammerlock Wrestling.zip": "Hammerlock Wrestling.zip",
            "Hardball III.zip": "HardBall III.zip",
            "Harley's Humongous Adventure.zip": "Harley's Humongous Adventure.zip",
            "Harvest Moon.zip": "Harvest Moon.zip",
            "Head-On Soccer.zip": "Head-On Soccer.zip",
            "Hind Strike.zip": "Hind Strike.zip",
            "Hit the Ice.zip": "Hit the Ice.zip",
            "Holy Umbrella - Dondera no Mubo!!.zip": "Holy Umbrella - Dondera's Wild!!.zip",
            "Home Alone.zip": "Home Alone.zip",
            "Home Alone 2 - Lost in New York.zip": "Home Alone 2 - Lost in New York.zip",
            "Hook.zip": "Hook.zip",
            "Hunt for Red October, The.zip": "Hunt for Red October, The.zip",
            "Hurricanes, The.zip": "Hurricanes.zip",
            "Hyper V-Ball.zip": "Hyper V-Ball.zip",
            "HyperZone.zip": "HyperZone.zip",
            "Ignition Factor, The.zip": "Ignition Factor, The.zip",
            "Illusion of Gaia.zip": "Illusion of Gaia.zip",
            "Imperium.zip": "Imperium.zip",
            "Incantation.zip": "Incantation.zip",
            "Incredible Crash Dummies, The.zip": "Incredible Crash Dummies, The.zip",
            "Incredible Hulk, The.zip": "Incredible Hulk, The.zip",
            "Indiana Jones' Greatest Adventures.zip": "Indiana Jones' Greatest Adventures.zip",
            "Inindo - Way of the Ninja.zip": "Inindo - Way of the Ninja.zip",
            "Inspector Gadget.zip": "Inspector Gadget.zip",
            "International Superstar Soccer.zip": "International Superstar Soccer.zip",
            "International Superstar Soccer Deluxe.zip": "International Superstar Soccer Deluxe.zip",
            "International Tennis Tour.zip": "International Tennis Tour.zip",
            "Irem Skins Game, The.zip": "Irem Skins Game, The.zip",
            "Iron Commando.zip": "Iron Commando.zip",
            "Itchy & Scratchy Game, The.zip": "Itchy & Scratchy Game, The.zip",
            "Izzy's Quest for the Olympic Rings.zip": "Izzy's Quest for the Olympic Rings.zip",
            "Jack Nicklaus Golf.zip": "Jack Nicklaus Golf.zip",
            "James Bond Jr.zip": "James Bond Jr.zip",
            "Jammit.zip": "Jammit.zip",
            "Jeopardy!.zip": "Jeopardy!.zip",
            "Jeopardy! Deluxe Edition.zip": "Jeopardy! Deluxe Edition.zip",
            "Jeopardy! Sports Edition.zip": "Jeopardy! Sports Edition.zip",
            "Jerry Boy.zip": "Jerry Boy.zip",
            "Jet Pilot Rising.zip": "Jet Pilot Rising.zip",
            "Jetsons, The - Invasion of the Planet Pirates.zip": "Jetsons, The - Invasion of the Planet Pirates.zip",
            "Jim Lee's WildC.A.T.S.zip": "Jim Lee's WildC.A.T.S - Covert-Action-Teams.zip",
            "Jim Power - The Lost Dimension in 3D.zip": "Jim Power - The Lost Dimension in 3D.zip",
            "Jimmy Connors Pro Tennis Tour.zip": "Jimmy Connors Pro Tennis Tour.zip",
            "Jimmy Houston's Bass Tournament U.S.A..zip": "Jimmy Houston's Bass Tournament U.S.A..zip",
            "Joe & Mac.zip": "Joe & Mac.zip",
            "Joe & Mac 2 - Lost in the Tropics.zip": "Joe & Mac 2 - Lost in the Tropics.zip",
            "John Madden Football '93.zip": "John Madden Football '93.zip",
            "John Madden Football.zip": "John Madden Football.zip",
            "JRR Tolkien's The Lord of the Rings - Volume 1.zip": "J.R.R. Tolkien's The Lord of the Rings - Volume 1.zip",
            "Judge Dredd.zip": "Judge Dredd.zip",
            "Jungle Book, The.zip": "Jungle Book, The.zip",
            "Jungle Strike.zip": "Jungle Strike.zip",
            "Jurassic Park.zip": "Jurassic Park.zip",
            "Jurassic Park Part 2 - The Chaos Continues.zip": "Jurassic Park II - The Chaos Continues.zip",
            "Justice League Task Force.zip": "Justice League Task Force.zip",
            "Kablooey.zip": "Kablooey.zip",
            "Kawasaki Caribbean Challenge.zip": "Kawasaki Caribbean Challenge.zip",
            "Kawasaki Superbike Challenge.zip": "Kawasaki Superbike Challenge.zip",
            "Ken Griffey Jr. Presents Major League Baseball.zip": "Ken Griffey Jr. Presents Major League Baseball.zip",
            "Ken Griffey Jr.'s Winning Run.zip": "Ken Griffey Jr.'s Winning Run.zip",
            "Kendo Rage.zip": "Kendo Rage.zip",
            "Kid Klown in Crazy Chase.zip": "Kid Klown in Crazy Chase.zip",
            "Kidou Senshi Gundam - Cross Dimension 0079.zip": "Mobile Suit Gundam - Cross Dimension 0079.zip",
            "Killer Instinct.zip": "Killer Instinct.zip",
            "King Arthur & The Knights of Justice.zip": "King Arthur & The Knights of Justice.zip",
            "King Arthur's World.zip": "King Arthur's World.zip",
            "King of Dragons, The.zip": "King of Dragons.zip",
            "King of Fighters 2000.zip": "King of Fighters 2000.zip",
            "King of the Monsters.zip": "King of the Monsters.zip",
            "King of the Monsters 2.zip": "King of the Monsters 2.zip",
            "Kirby Super Star.zip": "Kirby Super Star.zip",
            "Kirby's Avalanche.zip": "Kirby's Avalanche.zip",
            "Kirby's Dream Course.zip": "Kirby's Dream Course.zip",
            "Kirby's Dream Land 3.zip": "Kirby's Dream Land 3.zip",
            "Knights of the Round.zip": "Knights of the Round.zip",
            "Krusty's Super Fun House.zip": "Krusty's Super Fun House.zip",
            "Kyle Petty's No Fear Racing.zip": "Kyle Petty's No Fear Racing.zip",
            "Lagoon.zip": "Lagoon.zip",
            "Lamborghini - American Challenge.zip": "Lamborghini American Challenge.zip",
            "Last Action Hero.zip": "Last Action Hero.zip",
            "Lawnmower Man, The.zip": "Lawnmower Man, The.zip",
            "Legend.zip": "Legend.zip",
            "Legend of The Mystical Ninja, The.zip": "Legend of the Mystical Ninja, The.zip",
            "Legend of Zelda, The - A Link to the Past.zip": "Legend of Zelda, The - A Link to the Past.zip",
            "Lemmings.zip": "Lemmings.zip",
            "Lemmings 2 - The Tribes.zip": "Lemmings 2 - The Tribes.zip",
            "Lester the Unlikely.zip": "Lester the Unlikely.zip",
            "Lethal Enforcers.zip": "Lethal Enforcers.zip",
            "Lethal Weapon.zip": "Lethal Weapon.zip",
            "Liberty or Death.zip": "Liberty or Death.zip",
            "Lion King, The.zip": "Lion King, The.zip",
            "Little Magic.zip": "Little Magic.zip",
            "Live A Live.zip": "Live A Live.zip",
            "Lock On.zip": "Lock On.zip",
            "Looney Tunes B-Ball.zip": "Looney Tunes B-Ball.zip",
            "Lost Vikings II, The.zip": "Lost Vikings 2.zip",
            "Lost Vikings, The.zip": "Lost Vikings, The.zip",
            "Lufia & The Fortress of Doom.zip": "Lufia & The Fortress of Doom.zip",
            "Lufia II - Rise of the Sinistrals.zip": "Lufia II - Rise of the Sinistrals.zip",
            "Madden NFL '94.zip": "Madden NFL '94.zip",
            "Madden NFL '95.zip": "Madden NFL '95.zip",
            "Madden NFL '96.zip": "Madden NFL '96.zip",
            "Madden NFL '97.zip": "Madden NFL '97.zip",
            "Madden NFL '98.zip": "Madden NFL '98.zip",
            "Magic Boy.zip": "Magic Boy.zip",
            "Magic Sword.zip": "Magic Sword.zip",
            "Magical Pop'n.zip": "Magical Pop'n.zip",
            "Mario is Missing!.zip": "Mario is Missing!.zip",
            "Mario Paint.zip": "Mario Paint.zip",
            "Mario's Early Years! - Fun with Letters.zip": "Mario's Early Years! - Fun with Letters.zip",
            "Mario's Early Years! - Fun with Numbers.zip": "Mario's Early Years! - Fun with Numbers.zip",
            "Mario's Early Years! - Preschool Fun.zip": "Mario's Early Years! - Preschool Fun.zip",
            "Marvel Super Heroes - War of the Gems.zip": "Marvel Super Heroes - War of the Gems.zip",
            "Mary Shelley's Frankenstein.zip": "Mary Shelley's Frankenstein.zip",
            "Mask, The.zip": "Mask, The.zip",
            "Math Blaster Episode 1.zip": "Math Blaster - Episode 1.zip",
            "Maui Mallard in Cold Shadow.zip": "Maui Mallard in Cold Shadow.zip",
            "Mecarobot Golf.zip": "Mecarobot Golf.zip",
            "MechWarrior.zip": "MechWarrior.zip",
            "MechWarrior 3050.zip": "MechWarrior 3050.zip",
            "Mega Lo Mania.zip": "Mega Lo Mania.zip",
            "Mega Man 7.zip": "Mega Man 7.zip",
            "Mega Man X.zip": "Mega Man X.zip",
            "Mega Man X 2.zip": "Mega Man X2.zip",
            "Mega Man X 3.zip": "Mega Man X3.zip",
            "Mega Man X2.zip": "Mega Man X2.zip",
            "Mega Man X3.zip": "Mega Man X3.zip",
            "Metal Combat - Falcon's Revenge.zip": "Metal Combat - Falcon's Revenge.zip",
            "Metal Marines.zip": "Metal Marines.zip",
            "Metal Max 2.zip": "Metal Max 2.zip",
            "Metal Morph.zip": "Metal Morph.zip",
            "Metal Warriors.zip": "Metal Warriors.zip",
            "Michael Andretti's Indy Car Challenge.zip": "Michael Andretti's Indy Car Challenge.zip",
            "Michael Jordan - Chaos in the Windy City.zip": "Michael Jordan - Chaos in the Windy City.zip",
            "Mickey Mania - The Timeless Adventures of Mickey Mouse.zip": "Mickey Mania - The Timeless Adventures of Mickey Mouse.zip",
            "Mickey no Tokyo Disneyland Daibouken.zip": "Mickey's Tokyo Disneyland Adventure.zip",
            "Mickey's Playtown Adventure - A Day of Discovery!.zip": "Mickey's Playtown Adventure - A Day of Discovery!.zip",
            "Micro Machines.zip": "Micro Machines.zip",
            "Might and Magic III - Isles of Terra.zip": "Might and Magic III - Isles of Terra.zip",
            "Mighty Max.zip": "Mighty Max.zip",
            "Mighty Morphin Power Rangers.zip": "Mighty Morphin Power Rangers.zip",
            "Mighty Morphin Power Rangers - The Fighting Edition.zip": "Mighty Morphin Power Rangers - The Fighting Edition.zip",
            "Mighty Morphin Power Rangers - The Movie.zip": "Mighty Morphin Power Rangers - The Movie.zip",
            "Militia.zip": "Militia.zip",
            "Miracle Piano Teaching System, The.zip": "Miracle Piano Teaching System, The.zip",
            "Mohawk & Headphone Jack.zip": "Mohawk & Headphone Jack.zip",
            "Monopoly.zip": "Monopoly.zip",
            "Monster Maker 3 - Hikari no Majutsushi.zip": "Monster Maker 3 - Wizard of Light.zip",
            "Monstania.zip": "Monstania.zip",
            "Mortal Kombat.zip": "Mortal Kombat.zip",
            "Mortal Kombat 3.zip": "Mortal Kombat 3.zip",
            "Mortal Kombat II.zip": "Mortal Kombat II.zip",
            "Mountain Bike Rally.zip": "Mountain Bike Rally.zip",
            "Mr. Do!.zip": "Mr. Do!.zip",
            "Mr. Nutz.zip": "Mr. Nutz.zip",
            "Ms. Pac-Man.zip": "Ms. Pac-Man.zip",
            "Muscle Bomber.zip": "Saturday Night Slam Masters.zip",
            "Mutant Chronicles - Doom Troopers.zip": "Doom Troopers.zip",
            "Nageshiko Den - Ketteiban - Shoujo Pro Wrestler Densetsu.zip": "Nageshiko Den - Ketteiban - Shoujo Pro Wrestler Densetsu.zip",
            "NBA All-Star Challenge.zip": "NBA All-Star Challenge.zip",
            "NBA Give 'n Go.zip": "NBA Give 'n Go.zip",
            "NBA Hang Time.zip": "NBA Hangtime.zip",
            "NBA Jam.zip": "NBA Jam.zip",
            "NBA Jam - Tournament Edition.zip": "NBA Jam - Tournament Edition.zip",
            "NBA Jam T.E..zip": "NBA Jam T.E..zip",
            "NBA Live '95.zip": "NBA Live '95.zip",
            "NBA Live '96.zip": "NBA Live '96.zip",
            "NBA Live '97.zip": "NBA Live '97.zip",
            "NBA Live '98.zip": "NBA Live '98.zip",
            "NCAA Basketball.zip": "NCAA Basketball.zip",
            "NCAA Football.zip": "NCAA Football.zip",
            "NCAA Final Four Basketball.zip": "NCAA Final Four Basketball.zip",
            "New Horizons.zip": "New Horizons.zip",
            "NFL Football.zip": "NFL.zip",
            "NHL '94.zip": "NHL '94.zip",
            "NHL '95.zip": "NHL '95.zip",
            "NHL '96.zip": "NHL '96.zip",
            "NHL '97.zip": "NHL '97.zip",
            "NHL '98.zip": "NHL '98.zip",
            "NHLPA Hockey '93.zip": "NHLPA Hockey '93.zip",
            "Ninja Gaiden Trilogy.zip": "Ninja Gaiden Trilogy.zip",
            "Ninja Warriors, The.zip": "Ninjawarriors.zip",
            "Nintama Rantarou - Ninjutsu Gakuen Puzzle Taikai no Dan.zip": "Nintama Rantarou - Ninjutsu Gakuen Puzzle Taikai no Dan.zip",
            "No Escape.zip": "No Escape.zip",
            "Nosferatu.zip": "Nosferatu.zip",
            "Nurikabe Crazy Town.zip": "Nurikabe Crazy Town.zip",
            "Obitus.zip": "Obitus.zip",
            "Ogre Battle - The March of the Black Queen.zip": "Ogre Battle - The March of the Black Queen.zip",
            "Ooze, The.zip": "Ooze, The.zip",
            "Operation Europe - Path to Victory 1939-45.zip": "Operation Europe - Path to Victory 1939-45.zip",
            "Operation Logic Bomb.zip": "Operation Logic Bomb.zip",
            "Operation Thunderbolt.zip": "Operation Thunderbolt.zip",
            "Oscar.zip": "Oscar.zip",
            "Out of This World.zip": "Out of This World.zip",
            "Out to Lunch.zip": "Out to Lunch.zip",
            "Pac-Attack.zip": "Pac-Attack.zip",
            "Pac-In-Time.zip": "Pac-In-Time.zip",
            "Pac-Man 2 - The New Adventures.zip": "Pac-Man 2 - The New Adventures.zip",
            "Pagemaster, The.zip": "Pagemaster, The.zip",
            "Paladin's Quest.zip": "Paladin's Quest.zip",
            "Panic in Nakayoshi World.zip": "Panic in Nakayoshi World.zip",
            "Paperboy 2.zip": "Paperboy 2.zip",
            "Parlor! Mini 2.zip": "Parlor! Mini 2.zip",
            "Patlabor.zip": "Patlabor.zip",
            "Peace Keepers, The.zip": "Peace Keepers, The.zip",
            "Pebble Beach Golf Links.zip": "Pebble Beach Golf Links.zip",
            "Pele.zip": "Pele.zip",
            "Pele! II.zip": "Pele! II.zip",
            "Phalanx.zip": "Phalanx.zip",
            "Phantom 2040.zip": "Phantom 2040.zip",
            "Pieces.zip": "Pieces.zip",
            "Pilotwings.zip": "Pilotwings.zip",
            "Pink Goes to Hollywood.zip": "Pink Goes to Hollywood.zip",
            "Pinocchio.zip": "Pinocchio.zip",
            "Pirates of Dark Water, The.zip": "Pirates of Dark Water, The.zip",
            "Pitfall - The Mayan Adventure.zip": "Pitfall - The Mayan Adventure.zip",
            "Pitfall II.zip": "Pitfall II.zip",
            "Plok!.zip": "Plok!.zip",
            "Pocky & Rocky.zip": "Pocky & Rocky.zip",
            "Pocky & Rocky 2.zip": "Pocky & Rocky 2.zip",
            "Porky Pig's Haunted Holiday.zip": "Porky Pig's Haunted Holiday.zip",
            "Power Drive.zip": "Power Drive.zip",
            "Power Instinct.zip": "Power Instinct.zip",
            "Power Moves.zip": "Power Moves.zip",
            "Power Piggs of the Dark Age.zip": "Power Piggs of the Dark Age.zip",
            "Power Rangers III.zip": "Power Rangers 3.zip",
            "Power Rangers IV.zip": "Power Rangers 4.zip",
            "Power Rangers Zeo - Battle Racers.zip": "Power Rangers Zeo - Battle Racers.zip",
            "Power Soukoban.zip": "Power Soukoban.zip",
            "PowerMonger.zip": "PowerMonger.zip",
            "Prehistorik Man.zip": "Prehistorik Man.zip",
            "Primal Rage.zip": "Primal Rage.zip",
            "Prince of Persia.zip": "Prince of Persia.zip",
            "Prince of Persia 2 - The Shadow & The Flame.zip": "Prince of Persia 2 - The Shadow & The Flame.zip",
            "Pro Quarterback.zip": "Pro Quarterback.zip",
            "Pro Yakyuu Nettou Puzzle Stadium.zip": "Baseball Exciting Puzzle Stadium.zip",
            "Psycho Dream.zip": "Psycho Dream.zip",
            "PTO - Pacific Theater of Operations.zip": "P.T.O. - Pacific Theater of Operations.zip",
            "PTO II - Pacific Theater of Operations.zip": "P.T.O. II - Pacific Theater of Operations.zip",
            "Puggsy.zip": "Puggsy.zip",
            "Punch-Out!!.zip": "Punch-Out!!.zip",
            "Push-Over.zip": "Push-Over.zip",
            "Q*bert 3.zip": "Q*bert 3.zip",
            "R-Type III - The Third Lightning.zip": "R-Type III - The Third Lightning.zip",
            "Race Drivin'.zip": "Race Drivin'.zip",
            "Radical Rex.zip": "Radical Rex.zip",
            "Raiden Trad.zip": "Raiden Trad.zip",
            "Rampart.zip": "Rampart.zip",
            "Ranma 1-2 - Akanekodan Teki Hihou.zip": "Ranma 1-2 - Akanekodan Teki Hihou.zip",
            "Ranma 1-2 - Chougi Ranbu Hen.zip": "Ranma 1-2 - Chougi Ranbu Hen.zip",
            "Ranma 1-2 - Hard Battle.zip": "Ranma 1-2 - Hard Battle.zip",
            "Ranma 1-2 - Super Battle.zip": "Ranma 1-2 - Super Battle.zip",
            "Rap Jam - Volume One.zip": "Rap Jam - Volume One.zip",
            "Realm.zip": "Realm.zip",
            "Red Line F-1 Racer.zip": "Red Line F-1 Racer.zip",
            "Relief Pitcher.zip": "Relief Pitcher.zip",
            "Ren & Stimpy Show, The.zip": "Ren & Stimpy Show, The - Buckeroo$.zip",
            "Riddick Bowe Boxing.zip": "Riddick Bowe Boxing.zip",
            "Rise of the Phoenix.zip": "Rise of the Phoenix.zip",
            "Rival Turf!.zip": "Rival Turf!.zip",
            "Road Riot 4WD.zip": "Road Riot 4WD.zip",
            "Road Runner's Death Valley Rally.zip": "Road Runner's Death Valley Rally.zip",
            "RoboCop 3.zip": "RoboCop 3.zip",
            "RoboCop vs The Terminator.zip": "RoboCop vs The Terminator.zip",
            "Robotrek.zip": "Robotrek.zip",
            "Rock N' Roll Racing.zip": "Rock N' Roll Racing.zip",
            "Rocketeer, The.zip": "Rocketeer, The.zip",
            "Rocko's Modern Life - Spunky's Dangerous Day.zip": "Rocko's Modern Life - Spunky's Dangerous Day.zip",
            "Rocky Rodent.zip": "Rocky Rodent.zip",
            "Roger Clemens' MVP Baseball.zip": "Roger Clemens' MVP Baseball.zip",
            "Romancing SaGa.zip": "Romancing SaGa.zip",
            "Romancing SaGa 2.zip": "Romancing SaGa 2.zip",
            "Romancing SaGa 3.zip": "Romancing SaGa 3.zip",
            "Rudra no Hihou.zip": "Rudra no Hihou.zip",
            "Run Saber.zip": "Run Saber.zip",
            "Rushing Beat Ran - Fukusei Toshi.zip": "Rushing Beat Ran - Fukusei Toshi.zip",
            "Rushing Beat Shura.zip": "Rushing Beat Shura.zip",
            "S.O.S..zip": "S.O.S..zip",
            "Sailor Moon S - Kurukkurin.zip": "Sailor Moon S - Kurukkurin.zip",
            "Sailor Moon S - Kurrenai.png": "Sailor Moon S - Kurrenai.zip",
            "Saturday Night Slam Masters.zip": "Saturday Night Slam Masters.zip",
            "Scooby-Doo.zip": "Scooby-Doo Mystery.zip",
            "SD Gundam G Next - Senyou Rom Pack.zip": "SD Gundam G Next - Senyou Rom Pack.zip",
            "SD Gundam GX.zip": "SD Gundam GX.zip",
            "Secret of Evermore.zip": "Secret of Evermore.zip",
            "Secret of Mana.zip": "Secret of Mana.zip",
            "Seiken Densetsu 3.zip": "Seiken Densetsu 3.zip",
            "Seiken Densetsu.zip": "Seiken Densetsu.zip",
            "Senshi Heroes Saga.zip": "Senshi Heroes Saga.zip",
            "Shanghai II - Dragon's Eye.zip": "Shanghai II - Dragon's Eye.zip",
            "Shaq Fu.zip": "Shaq-Fu.zip",
            "Shien's Revenge.zip": "Shien's Revenge.zip",
            "Shin Kidou Senki Gundam Wing - Endless Duel.zip": "Mobile Suit Gundam Wing - Endless Duel.zip",
            "Shin Megami Tensei.zip": "Shin Megami Tensei.zip",
            "Shin Megami Tensei II.zip": "Shin Megami Tensei II.zip",
            "Shin Megami Tensei If....zip": "Shin Megami Tensei If....zip",
            "Shining Soul II.zip": "Shining Soul II.zip",
            "Shockwave.zip": "Shockwave.zip",
            "Side Pocket.zip": "Side Pocket.zip",
            "Sim Ant.zip": "SimAnt - The Electronic Ant Colony.zip",
            "Sim City.zip": "SimCity.zip",
            "SimCity 2000.zip": "SimCity 2000 - The Ultimate City Simulator.zip",
            "SimEarth - The Living Planet.zip": "SimEarth - The Living Planet.zip",
            "Sink or Swim.zip": "Sink or Swim.zip",
            "Skuljagger - Revolt of the Westicans.zip": "Skuljagger - Revolt of the Westicans.zip",
            "Sky Blazer.zip": "Sky Blazer.zip",
            "SmartBall.zip": "SmartBall.zip",
            "Snow White in Happily Ever After.zip": "Snow White in Happily Ever After.zip",
            "Snowboard Kids 2.zip": "Snowboard Kids 2.zip",
            "Soccer Shootout.zip": "Soccer Shootout.zip",
            "Soldiers of Fortune.zip": "Soldiers of Fortune.zip",
            "Sonic Blast Man.zip": "Sonic Blast Man.zip",
            "Sonic Blast Man II.zip": "Sonic Blast Man II.zip",
            "Soul Blazer.zip": "Soul Blazer.zip",
            "Space Ace.zip": "Space Ace.zip",
            "Space Funky B.O.B..zip": "Space Funky B.O.B..zip",
            "Space Invaders.zip": "Space Invaders.zip",
            "Space Megaforce.zip": "Space Megaforce.zip",
            "Sparkster.zip": "Sparkster.zip",
            "Spawn.zip": "Spawn.zip",
            "Speed Racer in My Most Dangerous Adventures.zip": "Speed Racer.zip",
            "Speedy Gonzales in Los Gatos Bandidos.zip": "Speedy Gonzales in Los Gatos Bandidos.zip",
            "Spider-Man - Lethal Foes.zip": "Spider-Man - Lethal Foes.zip",
            "Spider-Man - Maximum Carnage.zip": "Spider-Man - Maximum Carnage.zip",
            "Spider-Man - Separation Anxiety.zip": "Spider-Man - Separation Anxiety.zip",
            "Spider-Man and Venom - Maximum Carnage.zip": "Spider-Man & Venom - Maximum Carnage.zip",
            "Spider-Man and the X-Men in Arcade's Revenge.zip": "Spider-Man - X-Men - Arcade's Revenge.zip",
            "Spider-Man.zip": "Spider-Man.zip",
            "Spindizzy Worlds.zip": "Spindizzy Worlds.zip",
            "Sporting News Baseball.zip": "Sporting News Baseball.zip",
            "Star Fox 2.zip": "Star Fox 2.zip",
            "Star Fox.zip": "Star Fox.zip",
            "Star Ocean.zip": "Star Ocean.zip",
            "Star Trek - Deep Space Nine - Crossroads of Time.zip": "Star Trek - Deep Space Nine - Crossroads of Time.zip",
            "Star Trek - Starfleet Academy.zip": "Star Trek - Starfleet Academy.zip",
            "Star Trek - The Next Generation - Future's Past.zip": "Star Trek - The Next Generation - Future's Past.zip",
            "Stargate.zip": "Stargate.zip",
            "Steel Talons.zip": "Steel Talons.zip",
            "Sterling Sharpe - End 2 End.zip": "Sterling Sharpe - End 2 End.zip",
            "Stone Protectors.zip": "Stone Protectors.zip",
            "Street Fighter Alpha 2.zip": "Street Fighter Alpha 2.zip",
            "Street Fighter II - The World Warrior.zip": "Street Fighter II - The World Warrior.zip",
            "Street Fighter II Turbo - Hyper Fighting.zip": "Street Fighter II Turbo - Hyper Fighting.zip",
            "Street Fighter II.zip": "Street Fighter II.zip",
            "Street Hockey '95.zip": "Street Hockey '95.zip",
            "Stunt Race FX.zip": "Stunt Race FX.zip",
            "Sugoi Hebereke.zip": "Sugoi Hebereke.zip",
            "Super Adventure Island.zip": "Super Adventure Island.zip",
            "Super Adventure Island II.zip": "Super Adventure Island II.zip",
            "Super Alfred Chicken.zip": "Super Alfred Chicken.zip",
            "Super Aquatic Games Starring the Aquabats, The.zip": "Super Aquatic Games Starring the Aquabats, The.zip",
            "Super Back to the Future Part II.zip": "Super Back to the Future Part II.zip",
            "Super Baseball 2020.zip": "Super Baseball 2020.zip",
            "Super Bases Loaded.zip": "Super Bases Loaded.zip",
            "Super Bases Loaded 2.zip": "Super Bases Loaded 2.zip",
            "Super Bases Loaded 3 - License to Steal.zip": "Super Bases Loaded 3 - License to Steal.zip",
            "Super Batter Up.zip": "Super Batter Up.zip",
            "Super Battleship.zip": "Super Battleship.zip",
            "Super Battletank 2.zip": "Super Battletank 2.zip",
            "Super Battletank.zip": "Super Battletank.zip",
            "Super Black Bass.zip": "Super Black Bass.zip",
            "Super Bomberman.zip": "Super Bomberman.zip",
            "Super Bomberman 2.zip": "Super Bomberman 2.zip",
            "Super Bonk.zip": "Super Bonk.zip",
            "Super Bowling.zip": "Super Bowling.zip",
            "Super Buster Bros..zip": "Super Buster Bros..zip",
            "Super Caesars Palace.zip": "Super Caesars Palace.zip",
            "Super Castlevania IV.zip": "Super Castlevania IV.zip",
            "Super Chase H.Q..zip": "Super Chase H.Q..zip",
            "Super Conflict - The Mideast.zip": "Super Conflict - The Mideast.zip",
            "Super Double Dragon.zip": "Super Double Dragon.zip",
            "Super Earth Defense Force.zip": "Super Earth Defense Force.zip",
            "Super Family Circuit.zip": "Super Family Circuit.zip",
            "Super Ghouls 'N Ghosts.zip": "Super Ghouls'n Ghosts.zip",
            "Super Goal! 2.zip": "Super Goal! 2.zip",
            "Super Godzilla.zip": "Super Godzilla.zip",
            "Super High Impact.zip": "Super High Impact.zip",
            "Super Ice Hockey.zip": "Super Ice Hockey.zip",
            "Super James Pond.zip": "Super James Pond.zip",
            "Super Loopz.zip": "Super Loopz.zip",
            "Super Mario All-Stars.zip": "Super Mario All-Stars.zip",
            "Super Mario All-Stars + Super Mario World.zip": "Super Mario All-Stars + Super Mario World.zip",
            "Super Mario Kart.zip": "Super Mario Kart.zip",
            "Super Mario RPG - Legend of the Seven Stars.zip": "Super Mario RPG - Legend of the Seven Stars.zip",
            "Super Mario World.zip": "Super Mario World.zip",
            "Super Mario World 2 - Yoshi's Island.zip": "Super Mario World 2 - Yoshi's Island.zip",
            "Super Metroid.zip": "Super Metroid.zip",
            "Super Morph.zip": "Super Morph.zip",
            "Super Ninja Boy.zip": "Super Ninja Boy.zip",
            "Super Noah's Ark 3D.zip": "Super Noah's Ark 3D.zip",
            "Super Nova.zip": "Super Nova.zip",
            "Super Off Road - The Baja.zip": "Super Off Road - The Baja.zip",
            "Super Pinball - Behind the Mask.zip": "Super Pinball - Behind the Mask.zip",
            "Super Play Action Football.zip": "Super Play Action Football.zip",
            "Super Punch-Out!!.zip": "Super Punch-Out!!.zip",
            "Super Putty.zip": "Super Putty.zip",
            "Super R.B.I. Baseball.zip": "Super R.B.I. Baseball.zip",
            "Super Shadow of the Beast.zip": "Super Shadow of the Beast.zip",
            "Super Slap Shot.zip": "Super Slap Shot.zip",
            "Super Smash T.V..zip": "Super Smash T.V..zip",
            "Super Soccer.zip": "Super Soccer.zip",
            "Super Soccer Champ.zip": "Super Soccer Champ.zip",
            "Super Solitaire.zip": "Super Solitaire.zip",
            "Super Star Wars.zip": "Super Star Wars.zip",
            "Super Star Wars - Return of the Jedi.zip": "Super Star Wars - Return of the Jedi.zip",
            "Super Star Wars - The Empire Strikes Back.zip": "Super Star Wars - The Empire Strikes Back.zip",
            "Super Strike Eagle.zip": "Super Strike Eagle.zip",
            "Super Street Fighter II - The New Challengers.zip": "Super Street Fighter II - The New Challengers.zip",
            "Super SWIV.zip": "Super SWIV.zip",
            "Super Tennis.zip": "Super Tennis.zip",
            "Super Troll Islands.zip": "Super Troll Islands.zip",
            "Super Turrican.zip": "Super Turrican.zip",
            "Super Turrican 2.zip": "Super Turrican 2.zip",
            "Super Valis IV.zip": "Super Valis IV.zip",
            "Super Widget.zip": "Super Widget.zip",
            "Suzuka 8 Hours.zip": "Suzuka 8 Hours.zip",
            "Swat Kats - The Radical Squadron.zip": "Swat Kats - The Radical Squadron.zip",
            "Sword Master.zip": "Sword Master.zip",
            "Syndicate.zip": "Syndicate.zip",
            "T2 - The Arcade Game.zip": "T2 - The Arcade Game.zip",
            "T2 - The Arcade Game.zip": "T2 - The Arcade Game.zip",
            "T2 - The Terminator.zip": "T2 - The Terminator.zip",
            "Tactics Ogre - Let Us Cling Together.zip": "Tactics Ogre - Let Us Cling Together.zip",
            "Takahashi Meijin no Daibouken Jima.zip": "Adventure Island.zip",
            "Takahashi Meijin no Daibouken Jima II.zip": "Adventure Island II.zip",
            "Takahashi Meijin no Daibouken Jima III.zip": "Adventure Island III.zip",
            "Takahashi Meijin no Daibouken Jima IV.zip": "Adventure Island IV.zip",
            "Takahashi Meijin no Daibouken Jima V.zip": "Adventure Island V.zip",
            "Taikyoku Igo - Goliath.zip": "Taikyoku Igo - Goliath.zip",
            "Tales of Phantasia.zip": "Tales of Phantasia.zip",
            "Tarzan - Lord of the Jungle.zip": "Tarzan - Lord of the Jungle.zip",
            "Taz-Mania.zip": "Taz-Mania.zip",
            "Teenage Mutant Ninja Turtles IV - Turtles in Time.zip": "Teenage Mutant Ninja Turtles IV - Turtles in Time.zip",
            "Teenage Mutant Ninja Turtles Tournament Fighters.zip": "Teenage Mutant Ninja Turtles Tournament Fighters.zip",
            "Tekken 2.zip": "Tekken 2.zip",
            "Tekken 3.zip": "Tekken 3.zip",
            "Tekken.zip": "Tekken.zip",
            "Terminator 2 - Judgment Day.zip": "Terminator 2 - Judgment Day.zip",
            "Terminator, The.zip": "Terminator, The.zip",
            "Test Drive II - The Duel.zip": "Test Drive II - The Duel.zip",
            "Tetris 2.zip": "Tetris 2.zip",
            "Tetris & Dr. Mario.zip": "Tetris & Dr. Mario.zip",
            "Tetris Attack.zip": "Tetris Attack.zip",
            "Tetris Battle Gaiden.zip": "Tetris Battle Gaiden.zip",
            "Tetsuwan Atom.zip": "Astro Boy.zip",
            "The Addams Family.zip": "Addams Family, The.zip",
            "The Adventures of Batman & Robin.zip": "Adventures of Batman & Robin, The.zip",
            "The Chessmaster.zip": "Chessmaster, The.zip",
            "The Death and Return of Superman.zip": "Death and Return of Superman, The.zip",
            "The Flintstones.zip": "Flintstones, The.zip",
            "The Flintstones - The Treasure of Sierra Madrock.zip": "Flintstones, The - The Treasure of Sierra Madrock.zip",
            "The Hunt for Red October.zip": "Hunt for Red October, The.zip",
            "The Ignition Factor.zip": "Ignition Factor, The.zip",
            "The Incredible Hulk.zip": "Incredible Hulk, The.zip",
            "The Incredible Hulk.zip": "Incredible Hulk, The.zip",
            "The Itchy & Scratchy Game.zip": "Itchy & Scratchy Game, The.zip",
            "The Jungle Book.zip": "Jungle Book, The.zip",
            "The King of Dragons.zip": "King of Dragons.zip",
            "The Legend of Zelda - A Link to the Past.zip": "Legend of Zelda, The - A Link to the Past.zip",
            "The Lion King.zip": "Lion King, The.zip",
            "The Magical Quest Starring Mickey Mouse.zip": "Magical Quest Starring Mickey Mouse.zip",
            "The Mask.zip": "Mask, The.zip",
            "The Peace Keepers.zip": "Peace Keepers, The.zip",
            "The Ren & Stimpy Show.zip": "Ren & Stimpy Show, The.zip",
            "The Ren & Stimpy Show - Time Warp.zip": "Ren & Stimpy Show, The - Time Warp.zip",
            "The Simpsons - Bart's Nightmare.zip": "Simpsons, The - Bart's Nightmare.zip",
            "The Simpsons - Itchy & Scratchy Game.zip": "Simpsons, The - Itchy & Scratchy Game.zip",
            "The Smurfs.zip": "Smurfs, The.zip",
            "The Smurfs - Travel the World.zip": "Smurfs, The - Travel the World.zip",
            "The Tick.zip": "Tick, The.zip",
            "The Wizard of Oz.zip": "Wizard of Oz, The.zip",
            "Theme Park.zip": "Theme Park.zip",
            "Thoroughbred Breeder.zip": "Thoroughbred Breeder.zip",
            "Thunder Spirits.zip": "Thunder Spirits.zip",
            "Tick, The.zip": "Tick, The.zip",
            "Timon & Pumbaa's Jungle Games.zip": "Timon & Pumbaa's Jungle Games.zip",
            "Tin Star.zip": "Tin Star.zip",
            "Tiny Toon Adventures - Buster Busts Loose!.zip": "Tiny Toon Adventures - Buster Busts Loose!.zip",
            "Tiny Toon Adventures - Wacky Sports Challenge.zip": "Tiny Toon Adventures - Wacky Sports Challenge.zip",
            "Tom & Jerry.zip": "Tom and Jerry.zip",
            "Tom & Jerry - The Ultimate Game of Cat and Mouse!.zip": "Tom & Jerry - The Ultimate Game of Cat and Mouse!.zip",
            "Tom & Jerry.zip": "Tom and Jerry.zip",
            "Top Gear.zip": "Top Gear.zip",
            "Top Gear 2.zip": "Top Gear 2.zip",
            "Top Gear 3000.zip": "Top Gear 3000.zip",
            "Total Carnage.zip": "Total Carnage.zip",
            "Toys.zip": "Toys - Let the Toy Wars Begin!.zip",
            "Troddlers.zip": "Troddlers.zip",
            "Troy Aikman NFL Football.zip": "Troy Aikman NFL Football.zip",
            "True Lies.zip": "True Lies.zip",
            "True Golf Classics - Pebble Beach Golf Links.zip": "True Golf Classics - Pebble Beach Golf Links.zip",
            "True Golf Classics - Waialae Country Club.zip": "True Golf Classics - Waialae Country Club.zip",
            "True Golf Classics - Wicked 18.zip": "True Golf Classics - Wicked 18.zip",
            "Tuff E Nuff.zip": "Tuff E Nuff.zip",
            "Turn and Burn - No-Fly Zone.zip": "Turn and Burn - No-Fly Zone.zip",
            "Turok - Dinosaur Hunter.zip": "Turok - Dinosaur Hunter.zip",
            "Twisted Tales of Spike McFang, The.zip": "Twisted Tales of Spike McFang, The.zip",
            "U.N. Squadron.zip": "U.N. Squadron.zip",
            "Ultima VI - The False Prophet.zip": "Ultima VI - The False Prophet.zip",
            "Ultima VII - The Black Gate.zip": "Ultima VII - The Black Gate.zip",
            "Ultima - Runes of Virtue II.zip": "Ultima - Runes of Virtue II.zip",
            "Ultimate Fighter.zip": "Ultimate Fighter.zip",
            "Ultimate Mortal Kombat 3.zip": "Ultimate Mortal Kombat 3.zip",
            "Ultra Seven.zip": "Ultra Seven.zip",
            "Uncharted Waters.zip": "Uncharted Waters.zip",
            "Uncharted Waters - New Horizons.zip": "Uncharted Waters - New Horizons.zip",
            "Uniracers.zip": "Uniracers.zip",
            "Untouchables, The.zip": "Untouchables, The.zip",
            "Urban Strike - The Sequel to Jungle Strike.zip": "Urban Strike - The Sequel to Jungle Strike.zip",
            "Utopia - The Creation of a Nation.zip": "Utopia - The Creation of a Nation.zip",
            "V.R. Fighter.zip": "V.R. Fighter.zip",
            "V-Rally 97 Championship Edition.zip": "V-Rally 97 Championship Edition.zip",
            "Vortex.zip": "Vortex.zip",
            "Wagyan Paradise.zip": "Wagyan Paradise.zip",
            "War 2410.zip": "War 2410.zip",
            "War 3010 - The Revolution.zip": "War 3010 - The Revolution.zip",
            "Warlock.zip": "Warlock.zip",
            "WarpSpeed.zip": "WarpSpeed.zip",
            "Warriors of Fate.zip": "Warriors of Fate.zip",
            "Wayne Gretzky and the NHLPA All-Stars.zip": "Wayne Gretzky and the NHLPA All-Stars.zip",
            "Wayne's World.zip": "Wayne's World.zip",
            "WCW SuperBrawl Wrestling.zip": "WCW SuperBrawl Wrestling.zip",
            "Weapon Lord.zip": "WeaponLord.zip",
            "We're Back! A Dinosaur's Story.zip": "We're Back! A Dinosaur's Story.zip",
            "Wheel of Fortune.zip": "Wheel of Fortune.zip",
            "Where in the World is Carmen Sandiego.zip": "Where in the World is Carmen Sandiego.zip",
            "Where in Time is Carmen Sandiego.zip": "Where in Time is Carmen Sandiego.zip",
            "Whizz.zip": "Whizz.zip",
            "Wild C.A.T.S.zip": "Wild C.A.T.S.zip",
            "Wild Guns.zip": "Wild Guns.zip",
            "WildSnake.zip": "Wild Snake.zip",
            "Williams Arcade's Greatest Hits.zip": "Williams Arcade's Greatest Hits.zip",
            "Wing Commander.zip": "Wing Commander.zip",
            "Wing Commander - The Secret Missions.zip": "Wing Commander - The Secret Missions.zip",
            "Wings 2 - Aces High.zip": "Wings 2 - Aces High.zip",
            "Winter Extreme - Skiing & Snowboarding.zip": "Winter Extreme - Skiing & Snowboarding.zip",
            "Wolverine - Adamantium Rage.zip": "Wolverine - Adamantium Rage.zip",
            "Wordtris.zip": "Wordtris.zip",
            "World Champ - Super Boxing Great Fight.zip": "World Champ - Super Boxing Great Fight.zip",
            "World Cup USA '94.zip": "World Cup USA '94.zip",
            "World Heroes.zip": "World Heroes.zip",
            "World Heroes 2.zip": "World Heroes 2.zip",
            "World League Soccer.zip": "World League Soccer.zip",
            "World League Soccer '95.zip": "World League Soccer '95.zip",
            "World Masters Golf.zip": "World Masters Golf.zip",
            "World Soccer 94.zip": "World Soccer 94.zip",
            "World Soccer 95.zip": "World Soccer 95.zip",
            "WWF Raw.zip": "WWF Raw.zip",
            "WWF Royal Rumble.zip": "WWF Royal Rumble.zip",
            "WWF Super WrestleMania.zip": "WWF Super WrestleMania.zip",
            "X-Men - Mutant Apocalypse.zip": "X-Men - Mutant Apocalypse.zip",
            "Xardion.zip": "Xardion.zip",
            "Yogi Bear.zip": "Adventures of Yogi Bear.zip",
            "Ys III - Wanderers from Ys.zip": "Ys III - Wanderers from Ys.zip",
            "Yuu Yuu Hakusho.zip": "Yuu Yuu Hakusho.zip",
            "Zero The Kamikaze Squirrel.zip": "Zero The Kamikaze Squirrel.zip",
            "Zombies Ate My Neighbors.zip": "Zombies Ate My Neighbors.zip",
            "Zool.zip": "Zool - Ninja of the 'Nth' Dimension.zip",
            "Zoop.zip": "Zoop.zip",
            "Mega Man VII.zip": "Mega Man 7.zip",
            "Yogi Bear.zip": "Adventures of Yogi Bear.zip",
            "Beethoven's 2nd.zip": "Beethoven The Ultimate Canine Caper.zip",
            "Ballz 3D.zip": "Ballz 3D Fighting at Its Ballziest.zip",
            "Blazeon.zip": "BlaZeon - The Bio-Cyborg Challenge.zip",
            "Bronkie Health Hero.zip": "Bronkie the Bronchiasaurus.zip",
            "Choplifter III.zip": "Choplifter III - Rescue & Survive.zip",
            "College Slam Basketball.zip": "College Slam.zip",
            "Mutant Chronicles - Doom Troopers.zip": "Doom Troopers.zip",
            "Mountain Bike Rally.zip": "Exertainment Mountain Bike Rally.zip",
            "Hagane.zip": "Hagane - The Final Conflict.zip",
            "Mickey Mania.zip": "Mickey Mania - The Timeless Adventures of Mickey Mouse.zip",
            "Pink Panther in Pink Goes to Hollywood.zip": "Pink Goes to Hollywood.zip",
            "Scooby-Doo.zip": "Scooby-Doo Mystery.zip",
            "Super NES Super Scope 6.zip": "Super Scope 6.zip",
            "Magic Johnson's Super Slam Dunk.zip": "Super Slam Dunk.zip",
            "Test Drive II - The Duel.zip": "Duel, The - Test Drive II.zip",
            "Pebble Beach Golf Links.zip": "True Golf Classics - Pebble Beach Golf Links.zip",
            "Waialae Country Club.zip": "True Golf Classics - Waialae Country Club.zip",
            "Wicked 18 Golf.zip": "True Golf Classics - Wicked 18.zip",
            "Zool.zip": "Zool - Ninja of the 'Nth' Dimension.zip",
            "Battletoads-Double Dragon.zip": "Battletoads & Double Dragon - The Ultimate Team.zip"
            
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


def transfer_matching_cover_art(zip_files, art_files):
    renamed_folder = os.path.join(os.getcwd(), "renamed cover art")
    if not os.path.exists(renamed_folder):
        os.makedirs(renamed_folder)

    for zip_file in zip_files:
        zip_file_base = os.path.splitext(zip_file)[0]
        for art_file in art_files:
            art_file_base = os.path.splitext(os.path.basename(art_file))[0]
            if art_file_base.lower() == zip_file_base.lower():
                new_art_name = f"{zip_file_base}.zip.png"
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
        zip_files = list_snes_games()
        if zip_files:
            print("Here are your SNES games:")
            for file in zip_files:
                print(file)
            print("\n\n\nThese are the games I picked up!")
        else:
            print("No .zip files present in the 'snes games' folder.")
            time.sleep(5)
            return
    else:
        print("Too Bad, So Sad...")
        time.sleep(3)
        zip_files = list_snes_games()
        if zip_files:
            print("Here are your SNES games:")
            for file in zip_files:
                print(file)
            print("\n\n\nThese are the games I picked up!")
        else:
            print("No .zip files present in the 'snes games' folder.")
            time.sleep(5)
            return

    if zip_files:
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

        answer = input("Would you like to remove the version and region information from the title names?\nExample: 'SuperMarioWorld(USA).zip' would be changed to 'SuperMarioWorld.zip'\nYes or no? ").strip().lower()

        if answer == 'yes':
            snes_folder = os.path.join(os.getcwd(), "snes games")
            for file in zip_files:
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
                        zip_files = list_snes_games()
                        for game_file in zip_files:
                            if game_file in already_matched:
                                continue
                            game_name, _ = os.path.splitext(game_file)
                            best_match = find_best_match(game_name, txt_files)
                            if best_match:
                                matches.append((game_file, best_match))
                                new_file_name = os.path.splitext(best_match)[0] + ".zip"
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
                                zip_file_titles = [os.path.splitext(f)[0] for f in zip_files]
                                already_matched_art = set()
                                while True:
                                    changes_made = False
                                    for art_file in art_files:
                                        if art_file in already_matched_art:
                                            continue
                                        art_file_title = os.path.splitext(os.path.basename(art_file))[0]
                                        best_match = find_best_match(art_file_title, zip_file_titles)
                                        if best_match:
                                            art_matches.append((best_match + ".zip", art_file))
                                            changes_made = True
                                            already_matched_art.add(art_file)
                                            print(f"Matched '{art_file}' to '{best_match}'")
                                    if not changes_made:
                                        break

                                if art_matches:
                                    for game_file, art_file in art_matches:
                                        game_base, _ = os.path.splitext(game_file)
                                        new_art_name = game_base + ".zip.png"
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

                                transfer_matching_cover_art(zip_files, art_files)
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

        snes_games = [f for f in os.listdir(snes_games_folder) if f.endswith('.zip')]
        renamed_cover_art = [f for f in os.listdir(renamed_cover_art_folder) if f.endswith('.zip.png')]

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
