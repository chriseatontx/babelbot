import pyautogui
import time

# Enable the failsafe: Move mouse to a corner of the screen to stop.
pyautogui.FAILSAFE = True

print("Reading mouse coordinates and pixel RGB values...")
print("To stop, slam the mouse into any screen corner.")
print("-" * 55) # Prints a separator line for clarity

try:
    while True:
        # 1. Get the current mouse coordinates
        x, y = pyautogui.position()
        
        # 2. Get the RGB color value of the pixel at that exact location
        r, g, b = pyautogui.pixel(x, y)
        
        # 3. Format the string to be easy to read.
        # .ljust() and .rjust() help align the text in neat columns.
        positionStr = f'X: {str(x).ljust(4)} Y: {str(y).ljust(4)} | RGB: ({str(r).rjust(3)}, {str(g).rjust(3)}, {str(b).rjust(3)})'
        
        # 4. Print the final output string
        print(positionStr)
        
        # Wait a moment before the next reading to avoid flooding the screen
        time.sleep(0.5)

except pyautogui.FailSafeException:
    print("\nFailsafe activated. Program stopped.")
    
except KeyboardInterrupt:
    print("\nProgram stopped by user (Ctrl+C).")

