import time
import pyautogui
import tkinter
import pygetwindow


def wait():
    """Wait for x seconds."""
    time.sleep(0.1)

def focus_game_window():
    """Focus the game window."""
    try:
        # Find the game window by its title
        game_window = pygetwindow.getWindowsWithTitle('Tower of Babel')[0]
        game_window.activate()
        print("Game window focused.")
    except IndexError:
        print("Game window not found. Please ensure the game is running and the title is correct.")

def mouseclick(x,y):
    """Move mouse to (x, y) and click."""
    print(f"Moving mouse to ({x}, {y}) and clicking left mouse button")
    wait()
    pyautogui.moveTo(x, y, duration=0.5)
    wait()
    pyautogui.click() 

def find_and_click(image_filename, confidence=0.8):
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
        # 1. Locate the center of the image on the screen.
        # This is better than locateOnScreen() because it directly gives us the center point.
        location = pyautogui.locateCenterOnScreen(image_filename, confidence=confidence)

        # 2. Check if the image was found.
        if location:
            print(f"Found '{image_filename}' at {location}.")
            
            # 3. If found, call the click function with the coordinates.
            # The 'location' variable is already a Point(x, y) object.
            mouseclick(location.x, location.y)
            return True # Signal that we succeeded
        else:
            print(f"Could not find '{image_filename}' on the screen.")
            return False # Signal that we failed

    except pyautogui.PyAutoGUIException as e:
        # This error usually means the image file itself could not be found on your disk.
        print(f"Error finding image file: {e}")
        return False
     
def determine_game_state():
    """Determine the game state."""
    # This function can be expanded to check for specific game states
    # For now, it just returns a placeholder value
    try:
        location = pyautogui.locateOnScreen('./images/play.png', confidence=0.8)
        print(f"Found 'start.png' at {location}.")
        return "Start Screen"
  
    except pyautogui.PyAutoGUIException as e:
            print(f"Could not find 'start.png' on the screen.")
    
    try:
        location = pyautogui.locateOnScreen('./images/lobbypause.png', confidence=0.8)
        print(f"Found 'lobbypause.png' at {location}.")
        return "Lobby Pause"

    except pyautogui.PyAutoGUIException as e:
            print(f"Could not find 'lobbypause.png' on the screen.")

    try:
        location = pyautogui.locateOnScreen('./images/thebag.png', confidence=0.8)
        print(f"Found 'thebag.png' at {location}.")
        return "Lobby Screen"

    except pyautogui.PyAutoGUIException as e:
            print(f"Could not find 'thebag.png' on the screen.")

    try:
        location = pyautogui.locateOnScreen('./images/selectfloor.png', confidence=0.8)
        print(f"Found 'selectfloor.png' at {location}.")
        return "Select Floor"

    except pyautogui.PyAutoGUIException as e:
            print(f"Could not find 'selectfloor.png' on the screen.")
    

# =================================================================
# STATE HANDLER FUNCTIONS
# Each function handles one state and returns the outcome.
# =================================================================

def handle_main_menu_state():
    """Handle the main menu state."""
    print("Handling main menu state...")
    # Add logic to handle the main menu state
    return "Main Menu Handled"

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


    
     


def run_state_machine_bot():
    # Main function to run the bot
    print("Starting bot in 3 seconds...")
    wait()

    # Check if the game window is already focused
    print("Focusing game window...")
    focus_game_window()
    wait()

    # Determine the game state
    print("Determining game state...")
    game_state = determine_game_state()
    print(f"Game state: {game_state}") 
    wait()

    # Perform actions based on the game state
    match game_state:
        case "Start Screen":
              print("Game is at the Start Screen. Performing actions...")
        case "Lobby Screen":
              print("Game is at the Lobby Screen. Performing actions...")
        case "Lobby Pause":
              print("Game is at the Lobby Pause Screen. Performing actions...")
        case "Select Floor":
              print("Game is at the Select Floor screen. Performing actions...")
              wait()
              print("Running floor selector state")
              wait()
              floor_selector_state()




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