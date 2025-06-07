from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import logging
import time

# URL components
MAIN_URL = "https://www.popmart.com/ca/pop-now/set/195-1001"
VAR_URL = 2374  # This will be incremented by 10
END_URL = 40585

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def play_sound(success=True):
    """Play a sound to indicate success or failure"""
    if success:
        os.system('afplay /System/Library/Sounds/Glass.aiff')  # Success sound
    else:
        os.system('afplay /System/Library/Sounds/Basso.aiff')  # Failure sound

def setup_driver():
    # Set up Chrome options with incognito mode
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.set_capability("acceptInsecureCerts", True)
    
    try:
        # Try using Chrome directly
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"First attempt failed: {e}")
        try:
            # Second attempt using ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            return driver
        except Exception as e:
            print(f"Second attempt failed: {e}")
            raise

def wait_for_element(driver, by, selector, timeout=10):
    """Helper function to wait for an element to be present and visible"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
        return element
    except Exception as e:
        logging.error(f"Failed to find element {selector}: {e}")
        play_sound(False)  # Play failure sound when element not found
        raise

def find_and_click_elements(driver):
    """Find and click all box items, tracking progress and handling pagination"""
    clicked_positions = set()
    error_count = 0
    max_errors = 3
    
    try:
        while True:
            # Find all box items on current page with specific image source
            try:
                box_items = driver.find_elements(
                    By.CLASS_NAME, "index_showBoxItem__5YQkR", 
                    By.CSS_SELECTOR, 
                    'img.index_showBoxItem__5YQkR[src="https://global-static.popmart.com/globalAdmin/1745405615070____box_pic____.png"]'
                )
                logging.info(f"Found {len(box_items)} matching box items on current page")
                
                if not box_items:
                    error_count += 1
                    logging.warning(f"No box items found on page (attempt {error_count}/{max_errors})")
                    if error_count >= max_errors:
                        logging.error("Maximum error attempts reached")
                        play_sound(False)
                        break
                    time.sleep(2)
                    continue
                
                # Try clicking each box item that hasn't been clicked yet
                current_page_clicked = False
                for idx, item in enumerate(box_items):
                    if idx not in clicked_positions:
                        try:
                            logging.info(f"Attempting to click box item {idx + 1}")
                            initial_url = driver.current_url
                            item.click()
                            time.sleep(2)  # Wait to see if page changes
                            
                            if driver.current_url != initial_url:
                                logging.info(f"Successfully clicked box item {idx + 1} - Page changed")
                                play_sound(True)
                                driver.back()  # Go back to continue with other items
                                time.sleep(2)  # Wait for page to load after going back
                            else:
                                logging.info(f"Clicked box item {idx + 1} but page did not change")
                            
                            clicked_positions.add(idx)
                            current_page_clicked = True
                            error_count = 0  # Reset error count on success
                        except Exception as e:
                            logging.warning(f"Failed to click box item {idx + 1}: {e}")
                            error_count += 1
                            if error_count >= max_errors:
                                logging.error("Maximum error attempts reached")
                                play_sound(False)
                                return
                
                if not current_page_clicked:
                    # Try to find and click the next arrow
                    try:
                        next_arrow = driver.find_element(
                            By.CSS_SELECTOR, 
                            'img[class="index_nextImg__PTfZF"][src*="thBoxNextArrow.png"]'
                        )
                        if next_arrow.is_displayed():
                            logging.info("Clicking next page arrow")
                            next_arrow.click()
                            time.sleep(2)
                            clicked_positions.clear()  # Reset clicked positions for new page
                            continue
                    except Exception as e:
                        logging.info("No more pages to navigate")
                        play_sound(False)
                        break
                    
                    logging.info("All items on all pages have been processed")
                    play_sound(False)
                    break
                    
            except Exception as e:
                logging.error(f"Error processing page: {e}")
                error_count += 1
                if error_count >= max_errors:
                    logging.error("Maximum error attempts reached")
                    play_sound(False)
                    break
                time.sleep(2)
                
    except Exception as e:
        logging.error(f"Critical error in find_and_click_elements: {e}")
        play_sound(False)
        raise

def main():
    error_count = 0
    max_errors = 3
    url_attempts = 0
    max_url_attempts = 5
    current_var_url = VAR_URL
    driver = None

    try:
        # Get first URL from user before opening Chrome
        current_url = f"{MAIN_URL}{current_var_url}{END_URL}"
        url = input(f"Enter URL to navigate to [{current_url}]: ") or current_url
        
        # Set up Chrome driver only after getting initial URL
        driver = setup_driver()
        
        while url_attempts < max_url_attempts:
            # Navigate to URL
            if url_attempts == 0:
                driver.get(url)
                logging.info("Navigating to initial URL...")
                
                # Accept cookies only on first navigation
                try:
                    accept_button = wait_for_element(driver, By.CLASS_NAME, "policy_acceptBtn__ZNU71")
                    accept_button.click()
                    logging.info("Accepted cookies")
                except Exception as e:
                    logging.warning("Cookie accept button not found, continuing...")
            else:
                # For subsequent attempts, construct and navigate to new URL
                current_url = f"{MAIN_URL}{current_var_url}{END_URL}"
                logging.info(f"Trying next URL with VAR_URL={current_var_url} (attempt {url_attempts + 1}/{max_url_attempts})")
                driver.get(current_url)
                logging.info("Navigating to new URL...")
                
            time.sleep(2)  # Wait for page to load

            # Try to find and click items on this URL
            try:
                # Find and click specific box items up to 3 times per page
                box_items = driver.find_elements(
                    By.CSS_SELECTOR, 
                    'img.index_showBoxItem__5YQkR[src="https://global-static.popmart.com/globalAdmin/1745405615070____box_pic____.png"]'
                )
                
                if box_items:
                    attempts_on_page = 0
                    max_attempts_per_page = 3
                    clicked_positions = set()  # Track which positions we've clicked
                    
                    while attempts_on_page < max_attempts_per_page and len(clicked_positions) < len(box_items):
                        # Try to find an unclicked item
                        for idx, item in enumerate(box_items):
                            if idx not in clicked_positions:
                                try:
                                    item.click()
                                    play_sound(True)
                                    logging.info(f"Successfully clicked box item at position {idx}")
                                    clicked_positions.add(idx)
                                    attempts_on_page += 1
                                    time.sleep(1)
                                    break  # Move to next attempt after successful click
                                except Exception as click_error:
                                    logging.error(f"Failed to click item at position {idx}: {click_error}")
                                    error_count += 1
                        
                        if attempts_on_page >= max_attempts_per_page:
                            logging.info("Reached maximum attempts for this page")
                            break
                            
                    # If we've tried 3 times or clicked all available items, move to next URL
                    current_var_url += 10
                    url_attempts += 1
                    if url_attempts < max_url_attempts:
                        logging.info(f"Moving to next URL variation...")
                        continue  # Continue to next URL in the loop
                    else:
                        logging.info("Maximum URL attempts reached. Ending application.")
                        return
                else:
                    logging.warning("No matching box items found on current page")
                    play_sound(False)
                    # Move to next URL variation
                    current_var_url += 10
                    url_attempts += 1
                    if url_attempts < max_url_attempts:
                        logging.info(f"Moving to next URL variation...")
                        continue  # Continue to next URL in the loop
                    else:
                        logging.info("Maximum URL attempts reached. Ending application.")
                        return

                if error_count >= max_errors:
                    logging.error("Maximum error attempts reached for current page")
                    # Move to next URL variation
                    current_var_url += 10
                    url_attempts += 1
                    if url_attempts < max_url_attempts:
                        logging.info(f"Moving to next URL variation...")
                        break  # Break inner loop to try next URL
                    else:
                        logging.info("Maximum URL attempts reached. Ending application.")
                        return

            except Exception as e:
                logging.error(f"An error occurred: {e}")
                play_sound(False)  # Failure sound for general errors
                error_count += 1
                time.sleep(2)  # Delay before retry

    except Exception as e:
        logging.error(f"Critical error occurred: {e}")
        play_sound(False)  # Failure sound for critical errors
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
