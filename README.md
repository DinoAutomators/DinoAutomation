# Chrome Dino AI Game Bot

This Python script automates gameplay for the Chrome Dino game by interacting with the game's tab using Chrome's DevTools protocol through the `pychrome` library. The bot reads the game's internal state to detect obstacles and performs the appropriate actions (jump or duck) to avoid them.

## Features
- **Automates Chrome Dino Gameplay**: The script identifies obstacles (cacti and vultures) and triggers jumps or ducks based on the obstacle's size and distance.
- **Chrome DevTools Integration**: Uses Chrome's DevTools protocol to manipulate the Dino game in real-time.
- **Customizable Game Speed Reaction**: Adjusts actions based on the current game speed for optimal gameplay.

## Requirements

- **Google Chrome**: The game must be played in Google Chrome.
- **Chrome DevTools Protocol**: Chrome needs to be started with remote debugging enabled.
- **Python 3.x**
- **pychrome**: A Python library for interacting with Chrome using its DevTools protocol.

## Installation

1. Install `pychrome`:
   ```bash
   pip install pychrome
2. Launch Google Chrome with remote debugging enabled:
   ```bash
   chrome --remote-debugging-port=9222
3. Open the Chrome Dino game:
   - Go to `chrome://dino` in a new tab to start the game.

## Usage

1. **Run the script**:
   ```bash
   python dino_bot.py
2. **How it works**:
   - The script connects to Chrome through the DevTools protocol and checks for the Dino game tab.
   - Once the tab is found, it starts the game by simulating a spacebar press.
   - The script monitors the game state for obstacles and decides whether to jump (for low obstacles) or duck (for flying obstacles).

## Code Breakdown

- **Chrome DevTools Connection**:  
  The script connects to the Chrome DevTools protocol via `pychrome.Browser`. It finds the Dino game tab by looking for `chrome://dino` in the list of open tabs.
  
- **Game Controls**:  
  The game is started by dispatching keyboard events to simulate spacebar presses. This is handled by calling `Runtime.evaluate` with JavaScript to dispatch `KeyboardEvent`s in the Dino tab.

- **Obstacle Detection**:  
  The script evaluates the current game state by inspecting the Dino runner's obstacle properties (`distance`, `height`, and `speed`). It decides whether to jump or duck based on the obstacle's position and the player's speed.

- **Main Gameplay Loop**:  
  The `play_game` function continuously evaluates the game state and reacts in real-time by sending keyboard events (jump or duck) when obstacles are detected within a certain threshold.

## Debugging

- **Tab Detection**:  
  The script prints the URLs of all currently open tabs to ensure it can correctly find the `chrome://dino` tab.

- **Obstacle Detection**:  
  The script prints raw obstacle data (`distance`, `height`, `speed`) to help debug detection issues.

## Potential Issues

- **Tab Not Found**:  
  If the Dino game tab is not found, ensure you have opened the `chrome://dino` game and Chrome is running with remote debugging enabled.

- **DevTools Connection**:  
  Ensure that Chrome's remote debugging is running on the correct port (`9222`) and no firewall or security software is blocking the connection.

## Contributing

Feel free to contribute by creating issues or pull requests. Improvements like optimizing obstacle detection or enhancing gameplay strategies are welcome!

---

This project is intended for educational purposes. Please play fair and have fun with the Chrome Dino game!
