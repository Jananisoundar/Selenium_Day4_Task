from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def handle_multiple_windows():
    # Initialize the WebDriver with options
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(options=options)

    # Navigate to the website
    driver.get('https://www.cowin.gov.in/')

    # Store the ID of the original window
    original_window = driver.current_window_handle

    # Open the FAQ link in a new window using JavaScript
    faq_link = driver.find_element(By.XPATH, "//a[text()=' FAQ ']")
    driver.execute_script("window.open(arguments[0].href, '_blank', 'width=800,height=600');", faq_link)
    time.sleep(2)  # Wait for the new window to open

    # Open the Partners link in a new window using JavaScript
    partners_link = driver.find_element(By.XPATH, "//a[text()=' Partners ']")
    driver.execute_script("window.open(arguments[0].href, '_blank', 'width=800,height=600');", partners_link)
    time.sleep(2)  # Wait for the new window to open

    # Get the handles of all opened windows
    all_windows = driver.window_handles

    # Display the window handles
    print("Window Handles:")
    for window in all_windows:
        print(window)

    # Close all new windows except the original one
    for window in all_windows:
        if window != original_window:
            driver.switch_to.window(window)
            driver.close()
            time.sleep(20)

    # Switch back to the original window
    driver.switch_to.window(original_window)

    # Confirm we are back on the home page
    print("Back to the home page:", driver.current_url)

    # Close the browser
    driver.quit()

# Run the function
handle_multiple_windows()
