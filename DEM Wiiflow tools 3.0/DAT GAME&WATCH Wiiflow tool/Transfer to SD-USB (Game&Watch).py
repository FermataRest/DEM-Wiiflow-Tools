import os
import shutil

def get_drives():
    """Returns a list of available drives on the system."""
    drives = []
    if os.name == 'nt':  # Windows-based system
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            drive = f'{letter}:\\'
            if os.path.exists(drive):
                drives.append(drive)
    else:
        # For non-Windows systems (Linux, Mac), you can adapt this part
        drives.append('/')  # Assuming root as the main drive
    return drives

def display_drives(drives):
    """Displays available drives for the user to select."""
    print("Available Drives:")
    for i, drive in enumerate(drives):
        print(f'{i + 1}. {drive}')

def select_drive(drives):
    """Allows user to select a drive."""
    while True:
        try:
            choice = int(input("Select a drive number: "))
            if 1 <= choice <= len(drives):
                return drives[choice - 1]
            else:
                print("Invalid selection. Please select a valid drive number.")
        except ValueError:
            print("Please enter a valid number.")

def transfer_folder_contents(source_folder, destination_folder):
    """Transfers the contents of a folder to the destination."""
    if not os.path.exists(source_folder):
        print(f"The source folder {source_folder} does not exist.")
        return
    
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    try:
        for item in os.listdir(source_folder):
            s = os.path.join(source_folder, item)
            d = os.path.join(destination_folder, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
        print(f'Contents of {source_folder} have been successfully transferred to {destination_folder}')
    except Exception as e:
        print(f'An error occurred while transferring {source_folder}: {e}')

def main():
    # Get the folder where this script is running
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Paths to the source folders
    source_gnw_games = os.path.join(script_directory, "game&watch games")
    source_renamed_cover_art = os.path.join(script_directory, "renamed cover art")

    # Get available drives
    drives = get_drives()
    if not drives:
        print("No available drives found.")
        return

    # Display and select destination drive
    print("\nSelect the destination drive:")
    display_drives(drives)
    destination_drive = select_drive(drives)

    # Set the new destination path for Game & Watch games
    destination_gnw_path = os.path.join(destination_drive, "ROMS", "Nintendo", "GW")

    # Prompt after the drive is selected to transfer Game & Watch games
    user_input_games = input("Do you want to transfer your Game & Watch games to the SD/USB drive? (yes/no): ").strip().lower()

    if user_input_games == 'yes':
        # Transfer contents to the "ROMS/Nintendo/GW" folder
        transfer_folder_contents(source_gnw_games, destination_gnw_path)
    else:
        print("Game & Watch games transfer cancelled.")

    # Second prompt to transfer cover art
    user_input_art = input("Would you like to transfer your cover art as well? (yes/no): ").strip().lower()

    if user_input_art == 'yes':
        # Set the new destination path for cover art
        destination_cover_art_path = os.path.join(destination_drive, "wiiflow", "boxcovers", "Nintendo", "GW")

        # Transfer contents to the "wiiflow/boxcovers/Nintendo/GW" folder
        transfer_folder_contents(source_renamed_cover_art, destination_cover_art_path)
    else:
        print("Cover art transfer cancelled.")
    
    # Keep the script open and wait for user input to exit
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
