import pychrome
import time

# Connect to Chrome DevTools
browser = pychrome.Browser(url="http://127.0.0.1:9222")

# List all available tabs
tabs = browser.list_tab()

# Print out URLs for all tabs to debug
print("Listing all open tabs:")
for tab in tabs:
    tab_url = tab._kwargs['url']
    print(f"Tab URL: {tab_url}")

# Try to find the Dino game tab
dino_tab = None
for tab in tabs:
    if "chrome://dino" in tab._kwargs['url']:
        dino_tab = tab
        break

if not dino_tab:
    print("Dino game tab not found!")
    exit()

# Attach to the Dino game tab
dino_tab.start()

# Start the game by simulating a spacebar press
dino_tab.Runtime.evaluate(expression="""
    var event = new KeyboardEvent('keydown', {
        bubbles: true, cancelable: true, keyCode: 32
    });
    document.dispatchEvent(event);
""")
time.sleep(1)
dino_tab.Runtime.evaluate(expression="""
    var event = new KeyboardEvent('keyup', {
        bubbles: true, cancelable: true, keyCode: 32
    });
    document.dispatchEvent(event);
""")

# Main loop to detect obstacles and jump or duck
def play_game():
    while True:
        try:
            # Get the current game state
            response = dino_tab.Runtime.evaluate(expression="""
                (function() {
                    var obstacle = Runner.instance_.horizon.obstacles[0];
                    var distance = obstacle ? obstacle.xPos : 9999;
                    var height = obstacle ? obstacle.yPos : 9999;
                    var speed = Runner.instance_.currentSpeed;
                    return {distance: distance, height: height, speed: speed};
                })();
            """)

            # Debugging the raw response
            print(f"Raw response: {response}")

            # Extract the objectId from the response
            if 'result' in response and 'objectId' in response['result']:
                object_id = response['result']['objectId']

                # Use Runtime.getProperties to extract the object’s properties
                properties_response = dino_tab.Runtime.getProperties(objectId=object_id)

                # Extract values from the object’s properties
                distance, height, speed = None, None, None
                for prop in properties_response['result']:
                    if prop['name'] == 'distance':
                        distance = prop['value']['value']
                    if prop['name'] == 'height':
                        height = prop['value']['value']
                    if prop['name'] == 'speed':
                        speed = prop['value']['value']

                print(f"Distance: {distance}, Height: {height}, Speed: {speed}")

                if distance is not None and speed is not None and height is not None:
                    jump_threshold = (180 / speed) + 130
                    
                    # React to obstacles
                    if distance < jump_threshold:
                        if height > 50:  # Low obstacles like cacti
                            print(f"Low obstacle detected at distance {distance}, jumping...")
                            dino_tab.Runtime.evaluate(expression="""
                                var event = new KeyboardEvent('keydown', {
                                    bubbles: true, cancelable: true, keyCode: 32
                                });
                                document.dispatchEvent(event);
                            """)
                            if speed < 9:
                                time.sleep(0.12)
                            elif speed < 14:
                                time.sleep(0.07)
                                
                            dino_tab.Runtime.evaluate(expression="""
                                var event = new KeyboardEvent('keyup', {
                                    bubbles: true, cancelable: true, keyCode: 32
                                });
                                document.dispatchEvent(event);
                            """)
                        elif height <= 50:  # High obstacles like vultures
                            print(f"High obstacle detected at distance {distance}, ducking...")
                            dino_tab.Runtime.evaluate(expression="""
                                var event = new KeyboardEvent('keydown', {
                                    bubbles: true, cancelable: true, keyCode: 40
                                });
                                document.dispatchEvent(event);
                            """)
                            
                            if speed < 9:
                                time.sleep(0.12)
                            elif speed < 14:
                                time.sleep(0.07)
                                
                            dino_tab.Runtime.evaluate(expression="""
                                var event = new KeyboardEvent('keyup', {
                                    bubbles: true, cancelable: true, keyCode: 40
                                });
                                document.dispatchEvent(event);
                            """)
                    else:
                        print(f"No obstacles within range (distance {distance})...")
                else:
                    print("Could not extract distance, height, or speed.")

            else:
                print(f"Unexpected response format: {response}")

        except Exception as e:
            print(f"Error in obstacle detection: {e}")

        time.sleep(0.001)

if __name__ == "__main__":
    play_game()
