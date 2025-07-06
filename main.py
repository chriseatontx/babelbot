import time
import pyautogui
import tkinter
import pygetwindow
import keyboard
import os
import math

SKILL_ICON_FOLDER = "./images/skill_icons"

# Set to 1 to enable walking in a circle when in-game.
# Set to 0 to make the character stand still.
WALK_IN_CIRCLE = 1

# Determines the size of the circle. Larger number = larger circle path.
# This value acts as a multiplier for how long each direction key (W,A,S,D) is held.
# A value of 1.0 is a good starting point. Try 0.5 for a smaller circle or 2.0 for a larger one.
CIRCLE_RADIUS_MULTIPLIER = 6.0

# --- DEFINE YOUR SKILL PRIORITIES HERE ---
# Higher number = higher priority.
# Skills not in this list will be treated with a priority of 0.
SKILL_WEIGHTS = {
    'autopickkupradius': 1000,
    'expgain':           967,
    'sanctuary':         933,
    'criticalhitchance': 900,
    'piercingchance':    867,
    'castspeed':         833,
    'chainlightning':    800,
    'attackspeed':       767,
    'attackpower':       733,
    'dagger':            700,
    'basicattack':       667,
    'range':             633,
    'projectilecount':   600,
    'specialattack':     567,
    'frostarrow':        533,
    'magichammer':       500,
    'fireorb':           467,
    'iceorb':            433,
    'dragonsbreath':     400,
    'earthspike':        367,
    'lightningstrike':   333,
    'lightningwave':     300,
    'heavensjudgement':  267,
    'blizzard':          233,
    'meteorstrike':      200,
    'duration':          167,
    'magicitemfindchance': 133,
    'curse':             100,
    'reducedamage':      67,
    'swampofthedead':    34,
    'movementspeed':     1,
}


def wait():
    """Wait for a short duration to prevent overwhelming the game with inputs."""
    time.sleep(0.1)

def focus_game_window():
    """Brings the 'Tower of Babel' game window to the foreground."""
    try:
        # Find the game window by its title
        game_window = pygetwindow.getWindowsWithTitle('Tower of Babel')[0]
        game_window.activate()
        print("Game window focused.")
    except IndexError:
        print("Game window not found. Please ensure the game is running and the title is correct.")

def mouseclick(x,y):
    """Moves the mouse to the specified coordinates (x, y) and performs a left click."""
    print(f"Moving mouse to ({x}, {y}) and clicking left mouse button")
    wait()
    pyautogui.moveTo(x, y, duration=0.5)
    wait()
    pyautogui.click() 

def release_all_keys():
    """Releases all movement and action keys to prevent them from getting stuck."""
    keys = ['w', 'a', 's', 'd', 'e', 'space', 'shift', 'ctrl']
    for key in keys:
        print(f"Releasing key: {key}")
        pyautogui.keyUp(key)

def on_key_press(event):
    """Handles global key press events, specifically for stopping the bot."""
    print(f"Key pressed: {event.name}")
    if event.name == 'ctrl' and keyboard.is_pressed('c'):
        print("Ctrl+C detected. Exiting bot.")
        raise KeyboardInterrupt  # Raise an exception to stop the bot

# Set up a global key press hook to listen for the exit command.
keyboard.on_press(on_key_press)

def find_and_click(image_filename, confidence=0.7):
    """
    Finds an image on screen by its filename, calculates its center,
    and clicks it.

    Args:
        image_filename (str): The path to the image file (e.g., './images/lobbypause.png').
        confidence (float): The accuracy confidence required for the match (0.0 to 1.0).

    Returns:
        bool: True if the image was found and clicked, False otherwise.
    """
    try:
        # Locate the center of the image on the screen.
        location = pyautogui.locateCenterOnScreen(image_filename, confidence=confidence)

        # If the image is found, click on its location.
        if location:
            print(f"Found '{image_filename}' at {location}.")
            mouseclick(location.x, location.y)
            return True
        else:
            print(f"Could not find '{image_filename}' on the screen.")
            return False

    except pyautogui.PyAutoGUIException as e:
        # This error usually means the image file itself could not be found on your disk.
        print(f"Error finding image file: {e}")
        return False
     
def is_too_close(p1, p2, min_distance):
    """Helper function to check if two points are too close to each other."""
    distance = math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))
    return distance < min_distance

def walk_in_a_circle(radius_multiplier=1.0):
    """
    Makes the character walk in a square path to simulate a circle.
    The size of the path is determined by the radius_multiplier.

    This function executes one segment of the path (e.g., moves forward)
    and then returns, allowing the main loop to re-check the game state.
    It uses a static variable to remember its position in the path sequence.

    Args:
        radius_multiplier (float): Multiplies the base duration for key presses.
    """
    # Use a static variable to keep track of the current step in the path
    if not hasattr(walk_in_a_circle, "step"):
        walk_in_a_circle.step = 0  # Initialize step counter

    path_keys = ['w', 'a', 's', 'd']
    
    # A base duration for each side of the square path.
    base_duration = 0.5  # seconds
    
    # Calculate the actual time to hold each key down
    side_duration = base_duration * radius_multiplier
    
    # Get the current key for this step
    current_key = path_keys[walk_in_a_circle.step]

    print(f"--- Walking segment {walk_in_a_circle.step + 1}/4: Pressing '{current_key}' for {side_duration:.2f}s ---")
    
    # Press, wait, and release the key for one segment of the circle
    keyboard.press(current_key)
    time.sleep(side_duration)
    keyboard.release(current_key)

    # A brief pause between key presses can make movement feel less jerky
    time.sleep(0.1)

    # Advance the step for the next time the function is called
    walk_in_a_circle.step = (walk_in_a_circle.step + 1) % len(path_keys)


def determine_game_state():
    """
    Checks for a series of images to determine the current state of the game.
    Returns the name of the state as a string, or "Unknown" if no state is recognized.
    """
    # Define states as a tuple: (State Name, Image Path)
    # Order them by likelihood or priority if needed.
    states_to_check = [
        ("Level Up Screen", './images/levelup.png'),
        ("Start Screen", './images/play.png'),
        ("Lobby Pause", './images/lobbypause.png'),
        ("Select Floor", './images/selectfloor.png'),
        ("End of Run", './images/endofrun.png'),
        ("Sell Items", './images/sellitems.png'),
        ("Lobby Screen", './images/thebag.png'),
        ('In Game', './images/ingame.png')
    ]

    for state_name, image_path in states_to_check:
        try:
            # Use locateOnScreen which is fine for simple state checks.
            # It returns a Box object if found, or raises an exception if not.
            if pyautogui.locateOnScreen(image_path, confidence=0.8) is not None:
               # print(f"Detected state: {state_name}") #uncomment for debugging
                return state_name
        except pyautogui.ImageNotFoundException:
            # This is normal, just means this specific image wasn't found.
            continue
        except Exception as e:
            # Catch other potential errors, like file not found on disk.
            print(f"Error checking for state image {image_path}: {e}")
            
    # If the loop completes without finding any state
    return "Unknown"

# =================================================================
# Skill finder functions
# These functions are used to find and click on specific skills.
# =================================================================

def find_all_available_skills(skill_icons_path, confidence=0.68, min_separation_distance=50):
    """
    Scans the screen to identify ALL DISTINCT skill choices currently presented.

    This function finds all occurrences of each skill icon and then filters out
    duplicates that are too close to each other, ensuring each unique on-screen
    icon is reported only once.

    Args:
        skill_icons_path (str): The file path to the folder containing all
                                possible skill icon images.
        confidence (float, optional): The confidence level for image matching.
                                      Defaults to 0.68
        min_separation_distance (int, optional): The minimum pixel distance
                                                 between two detections to be
                                                 considered separate items.
                                                 Helps filter out duplicate
                                                 detections of the same icon.
                                                 Defaults to 50.

    Returns:
        dict: A dictionary where keys are skill names and values are a LIST
              of (x, y) center coordinates for each distinct instance found.
              Example: {'fireball': [(950, 420)], 'reroll': [(950, 580), (950, 740)]}
    """
    found_skills = {}
    all_found_points = [] # A flat list of all points found so far to check for duplicates

    try:
        all_skill_images = [f for f in os.listdir(skill_icons_path) if f.endswith('.png')]
    except FileNotFoundError:
        print(f"Error: The directory does not exist: {skill_icons_path}")
        return {}

    print("Starting screen search for all available skills...")

    for image_file in all_skill_images:
        full_path = os.path.join(skill_icons_path, image_file)
        skill_name = os.path.splitext(image_file)[0]

        try:
            # Use locateAllOnScreen to find all instances of the image.
            # We will now correctly handle the ImageNotFoundException.
            locations = pyautogui.locateAllOnScreen(full_path, confidence=confidence)

            for box in locations:
                center_point = pyautogui.center(box)
                # Convert to a simple tuple of ints
                current_point = (int(center_point.x), int(center_point.y))

                # --- DUPLICATE CHECKING LOGIC ---
                # Check if this point is too close to any point we've already logged
                is_duplicate = False
                for existing_point in all_found_points:
                    if is_too_close(current_point, existing_point, min_separation_distance):
                        is_duplicate = True
                        break # Found a duplicate, no need to check further

                if not is_duplicate:
                    # This is a new, unique skill location
                    if skill_name not in found_skills:
                        found_skills[skill_name] = []
                    
                    found_skills[skill_name].append(current_point)
                    all_found_points.append(current_point) # Add to our master list of points
                    print(f"  [+] Found unique '{skill_name}' at coordinates: {current_point}")

        except pyautogui.ImageNotFoundException:
            # This is expected behavior when a skill icon is not on screen.
            # We can uncomment the line below for very verbose debugging.
            # print(f"  [-] '{skill_name}' not found on screen.")
            continue
        except Exception as e:
            print(f"An unexpected error occurred while searching for {image_file}: {e}")

    total_found = sum(len(coords) for coords in found_skills.values())
    if total_found == 0:
        print("\nWarning: No skills were found on the screen.")
    else:
        print(f"\nSearch complete. Found a total of {total_found} unique skills.")

    return found_skills

# =================================================================
# STATE HANDLER FUNCTIONS
# Each function handles one state and returns the outcome.
# =================================================================

def handle_lobby_screen_state():
    """Handle the lobby screen state by clicking the 'select floor' button."""
    print("Handling lobby screen state...")
    # move up to the elevator
    keyboard.press('w')
    time.sleep(3)
    keyboard.release('w')
    wait()
    keyboard.press_and_release('e')
    wait()
    
def floor_selector_state():
    # Move down to floor 1
    for i in range(1, 10):
        print(f"Moving selector down to floor 1 {i}...")
        mouseclick(1379, 492)
        wait()
    
    #click the Battle Button
    print(f"Clicking the Battle Button...")
    wait()
    try:
        find_and_click('./images/BattleButton.png', confidence=0.8)
    except pyautogui.PyAutoGUIException as e:
        print(f"Could not click the Battle Button: {e}")
    return "Floor Selector Handled"



def handle_level_up_screen_state():
    """Handle the level up screen state by choosing the highest-weighted skill."""
    print("Handling level up screen state...")

    available_skills = find_all_available_skills(
        SKILL_ICON_FOLDER, 
        confidence=0.68, 
        min_separation_distance=50
    )

    if not available_skills:
        print("\nCould not identify any skills on the screen. Waiting and retrying.")
        time.sleep(1) # Wait a moment before the state machine runs again
        return

    print("\n--- Available Skill Choices ---")
    best_skill_to_choose = None
    highest_weight = -1
    
    # This loop is just for printing and doesn't need to change
    for skill, coords_list in available_skills.items():
        for coords in coords_list:
            print(f"Skill: {skill.replace('_', ' ').title()}, Location: {coords}")

    print("\n--- Evaluating Choices Based on Priority ---")
    for skill in available_skills:
        weight = SKILL_WEIGHTS.get(skill, 0)
        print(f" - Evaluating '{skill}': Priority = {weight}")
        if weight > highest_weight:
            highest_weight = weight
            best_skill_to_choose = skill

    # --- CLICK THE CHOSEN SKILL (CORRECTED LOGIC) ---
    if best_skill_to_choose:
        # We already have the coordinates, so retrieve them.
        # We take the first set of coordinates found for that skill.
        coords_to_click = available_skills[best_skill_to_choose][0]
        
        print(f"\n---> Best option is '{best_skill_to_choose}' with priority {highest_weight}. Clicking at {coords_to_click}.")
        
        # Call mouseclick directly with the coordinates. No need for find_and_click.
        mouseclick(coords_to_click[0], coords_to_click[1])

    else:
        # Fallback: If all skills had a weight of 0, pick the first one.
        fallback_skill_name = list(available_skills.keys())[0]
        coords_to_click = available_skills[fallback_skill_name][0]
        print(f"\nNo prioritized skills found. Selecting fallback: '{fallback_skill_name}' at {coords_to_click}")
        mouseclick(coords_to_click[0], coords_to_click[1])

def handle_end_of_run_state():
    """Handle the end of run state by clicking the 'continue' button."""
    print("Handling end of run state...")
    find_and_click('./images/endofrunokbutton.png', confidence=0.8)
    wait()
    find_and_click('./images/endofrunokbutton2.png', confidence=0.8)

def handle_sell_items_state():
    """Handle the sell items state by clicking the 'sell' button."""
    print("Handling sell items state...")
    # Click the 'sell' button
    find_and_click('./images/sellitems.png', confidence=0.8)
    wait()


# =================================================================
# Main bot loop
# =================================================================   

def run_state_machine_bot():
    # Main function to run the bot
    print("Starting bot...")
    wait()

    # Check if the game window is already focused
    print("Focusing game window...")
    focus_game_window()
    wait()


    while True:
        # Determine the game state
        print("Determining game state...")
        game_state = determine_game_state()
        print(f"Game state: {game_state}") 
        wait()

        # Perform actions based on the game state
        match game_state:
            case "Start Screen":
                print("Game is at the Start Screen. Clicking Play...")
                find_and_click('./images/play.png', confidence=0.8)
            case "Lobby Screen":
                print("Game is at the Lobby Screen. Moving to Select floor...")
                handle_lobby_screen_state()
            case "Lobby Pause":
                print("Game is at the Lobby Pause Screen. Clicking Resume...")
                find_and_click('./images/lobbypause.png', confidence=0.8)
            case "Select Floor":
                print("Game is at the Select Floor screen. Performing actions...")
                wait()
                print("Running floor selector state")
                wait()
                floor_selector_state()
            case "Level Up Screen":
                print("Game is at the Level Up Screen Determining choices...")
                handle_level_up_screen_state()
            case "End of Run":
                print("Game is at the End of Run screen. Performing actions...")
                handle_end_of_run_state()
            case "Sell Items":
                print("Game is at the Sell Items screen. Performing actions...")
                handle_sell_items_state()
            case "In Game":
                print("Game is in progress.")
                time.sleep(1)
                if WALK_IN_CIRCLE == 1:
                    # Call the function to perform one step of the walk cycle
                    walk_in_a_circle(CIRCLE_RADIUS_MULTIPLIER)
                else:
                    # If walking is disabled, just wait before checking again.
                    print("Walking in circle is disabled. Standing still...")
                    time.sleep(1)
                wait()




    # Simulate key press 'a'
    #print("Pressing 'a' key")
    #wait()
    #pyautogui.keyDown('a')
    #wait()
    #pyautogui.keyUp('a')

    # Simulate key press 'enter'
    #print("Pressing 'enter' key")
    #wait()
    #pyautogui.press('enter')

    #1727 Y: 427
    # Move mouse to (100, 100) and click
    #print("Moving mouse to (1727, 427) and clicking left mouse button")
    #wait()
    #pyautogui.moveTo(1727, 427, duration=0.5)
    #wait()
    #pyautogui.click()

# --- Start the bot ---
if __name__ == "__main__":
    try:
        run_state_machine_bot()
    except (KeyboardInterrupt, pyautogui.FailSafeException):
        print("\nBot stopped by user.")
        print("End of Line.")