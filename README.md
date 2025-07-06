# Babelbot
```
 ____        _          _ _           _   
| __ )  __ _| |__   ___| | |__   ___ | |_ 
|  _ \ / _` | '_ \ / _ \ | '_ \ / _ \| __|
| |_) | (_| | |_) |  __/ | |_) | (_) | |_ 
|____/ \__,_|_.__/ \___|_|_.__/ \___/ \__|

```

This is a Python bot that automatically plays the game [Tower of Babel: Survivors of Chaos](https.store.steampowered.com/app/2665680/Tower_of_Babel_Survivors_of_Chaos/).

## Features

- **Floor Selection:** Choose which floor the bot should run on.
- **Automated Gameplay Loop:** The bot can automatically start a run, select a floor, and enter combat.
- **State-Based Actions:** It uses image recognition to understand the current game state (e.g., main menu, in-game, level up screen, end of run).
- **Automatic Skill Selection:** When leveling up, the bot chooses the best skill based on a customizable priority list.
- **Configurable In-Game Movement:** The character can be set to either stand still or move in a circle to dodge enemies.
- **Post-Run Handling:** The bot automatically clicks through the end-of-run screens and sells items.
- **Safety Stop:** The bot can be stopped at any time by pressing Ctrl+C.

## How It Works

The bot uses the `pyautogui` library to take screenshots of the game window and identify the current state by matching images. Based on the state, it sends mouse clicks and keyboard presses to control the game.

Skill selection is based on a weighted priority system defined in the `SKILL_WEIGHTS` dictionary in `main.py`. You can customize this list to fit your preferred build.

## Requirements

- Python 3
- The following Python libraries: `pyautogui`, `tkinter`, `pygetwindow`, `keyboard`, `opencv-python`

## Usage

1.  Install the required Python libraries:
    ```
    pip install pyautogui tkinter pygetwindow keyboard opencv-python
    ```
2.  Run the bot:
    ```
    python main.py
    ```
3.  To stop the bot, press `Ctrl+C` in the terminal where the script is running.

## Configuration

- **`WALK_IN_CIRCLE`**: Set to `1` to enable walking in a circle in-game, or `0` to stand still.
- **`CIRCLE_RADIUS_MULTIPLIER`**: Adjusts the size of the circle path when `WALK_IN_CIRCLE` is enabled.
- **`SKILL_WEIGHTS`**: A dictionary where you can set the priority for each skill. Higher numbers mean higher priority.
