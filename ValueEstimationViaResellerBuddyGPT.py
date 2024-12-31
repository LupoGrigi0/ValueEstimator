from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import csv
import json
import time



'''
First Block of Code
open the CSV file, iterate through it, building the prompt that will be passed to Reseller Buddy GPT
'''
# Load the CSV file
input_file = "ItemsLupoWantsv2.csv"  # Replace with your actual file path
items_df = pd.read_csv(input_file)
ListOfPrompts = []

# Prepare columns for output
items_df['Estimated per item value'] = None
items_df['Method 1'] = None
items_df['Method 2'] = None
items_df['Method 3'] = None

# Iterate through the dataset and process each row
for index, row in items_df.iterrows():
    item_description = row['item description']
    condition = row['condition'] if not pd.isnull(row['condition']) else "unknown"

    # Construct the prompt for Reseller GPT
    prompt = (
        f"I need an estimate of the value of {item_description} in {condition} condition. "
        "Then give me a description of how you came up with the value, and a link to a specific item you used for creating this value."
    )
    ListOfPrompts.append(prompt)


'''
Second Block of Code
Use selinium to have reseller buddy create estimated values and spit them out
'''
# Specify the path to the ChromeDriver executable
driver_path = "/usr/local/bin/chromedriver"  # Update this path if necessary, path to the chromedriver download from chromedriver site from google search
profile_path = "/Users/lupo/Library/Application Support/Google/Chrome for Testing/Profile 1" #path to an existing profile if google OAUTH is used to log in
# Path to Chrome for Testing
chrome_testing_path = "/Applications/GoogleChromefor Testing.app/Contents/MacOS/Google Chrome for Testing"  # macOS example

# Initialize Chrome options Set all the flags that chrome checks to see if it is being automated
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={profile_path}")
options.binary_location = chrome_testing_path  # Use Chrome for Testing
options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation features
options.add_argument("--disable-extensions")  # Disable extensions for simplicity
options.add_argument("--disable-infobars")  # Remove the "Chrome is being controlled" banner
options.add_argument("--disable-dev-shm-usage")  # Fix issues with headless mode on Linux
options.add_argument("--no-sandbox")  # Security sandbox disabled (not recommended for production)
options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging
options.add_argument("--profile-directory=Profile 1")



# Set up the ChromeDriver service
service = Service(executable_path=driver_path)

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Spoof automation flags
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    """
})

# Track processed message IDs
processed_ids = set()

def Fetch_new_response():
    while True:
        # Fetch all response blocks
        response_blocks = driver.find_elements(
            By.XPATH,
            '//div[@data-message-model-slug="gpt-4o"]'
        )
        
        for block in response_blocks:
            message_id = block.get_attribute("data-message-id")
            if message_id not in processed_ids:
                processed_ids.add(message_id)
                return block  # Return the new response block


try: #some dodgy window switching shit

    #track the original window
    # because logging into a specific profile will open a new window
    original_window = driver.current_window_handle

    # Open a base URL to set cookies
    driver.get("https://chatgpt.com") 
    # Wait for the page to load
 
    print("you should be logged into the second window")
    input()  # Pauses execution until the user presses Enter

    # Check for additional windows
    for handle in driver.window_handles:
        if handle != original_window:
            print(f"Switching to new window: {handle}")
            driver.switch_to.window(handle)

finally:
    # Close all windows and quit the driver
    print(f"try block for window switch finished successfully")



print("hit enter to load reseller buddy.")
input()  # Pauses execution until the user presses Enter

try:
    # Navigate to ChatGPT
    driver.get("https://chatgpt.com/g/g-0gC7BDUd5-reseller-buddy")

    # Refresh the page to apply cookies
    # driver.refresh()

    # Wait for the page to load
    # time.sleep(200)
    print("you should be logged in and the reseller buddy GPT")
    input()  # Pauses execution until the user presses Enter

    # Locate the input field and send a message
    input_box = driver.find_element(By.ID, "prompt-textarea")

    ResponseList = [] # hold the list of responses
    #Send Crafted prompt for line item in spreadsheet
    for i, BuiltPrompt in enumerate(ListOfPrompts, start=1):

        #input_box.send_keys("I need an estimate of the value of magazine Heavy Metal pre 2005 in Fair condition. Then give me a description of how you came up with the value, and a link to a specific item you used for creating this value.")
        print(f"Sending prompt number {i} {BuiltPrompt}")
        input_box.send_keys(f"{BuiltPrompt}")
        input_box.send_keys(Keys.RETURN)

        print("Input Sent.. hit return when response is ready")
        input()  # Pauses execution until the user presses Enter

        response_block = Fetch_new_response()
        print(f"ChatGPT Response: {i} : {response_block.text}")
        ResponseList.append(response_block.text)

        print("you should see results hit enter to send next prompt")
        input()  # Pauses execution until the user presses Enter

finally:
    print(f"it worked?")

for i, ReturnedResponse in enumerate(ResponseList, start=1):
    print(f"RESPONSE number {i} : {ReturnedResponse} \n")

# Save responses as a JSON file
with open("responses.json", "w") as json_file:
    json.dump(ResponseList, json_file, indent=4)
print("Responses saved to responses.json")

