"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import datetime

# Set up the web driver
driver = webdriver.Chrome()
driver.get("")  # Ensure this URL is correct for your target site

# Set the initial start and end dates
start_date = "2024-07-15"
end_date = "2024-08-31"

# Explicit wait for the elements to be located and interactable
wait = WebDriverWait(driver, 20)

# Wait for any potential loading spinner to disappear
wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".ant-spin-spinning")))

# Initialize the current date
current_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")

while current_date + datetime.timedelta(days=2) <= end_date_obj:
    current_end_date = current_date + datetime.timedelta(days=2)
    current_end_date_str = current_end_date.strftime("%Y-%m-%d")

    # Select the date inputs
    start_date_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-picker-input input[placeholder='Start date']")))
    end_date_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-picker-input input[placeholder='End date']")))

    # Set the start date
    driver.execute_script("arguments[0].removeAttribute('readonly')", start_date_input)  # Remove readonly if present
    start_date_input.click()
    start_date_input.send_keys(Keys.CONTROL + "a")
    start_date_input.send_keys(Keys.DELETE)
    start_date_input.send_keys(current_date.strftime("%Y-%m-%d"))
    start_date_input.send_keys(Keys.ENTER)

    # Set the end date
    driver.execute_script("arguments[0].removeAttribute('readonly')", end_date_input)
    end_date_input.click()
    end_date_input.send_keys(Keys.CONTROL + "a")
    end_date_input.send_keys(Keys.DELETE)
    end_date_input.send_keys(current_end_date_str)
    end_date_input.send_keys(Keys.ENTER)

    # Click the "vérifier la disponibilitée" button
    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'vérifier la disponibilitée')]")))
    search_button.click()

    # Wait for the results to load
    time.sleep(5)

    # Extract the results with the "Réserver" button
    reserver_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Réserver')]")

    # Extract links for available rooms
    available_rooms = []
    for button in reserver_buttons:
        room_link = button.get_attribute("href")
        available_rooms.append(room_link)

    # Print the list of links for available rooms
    print(f"List of links for available rooms from {current_date.strftime('%Y-%m-%d')} to {current_end_date_str}:")
    for room_link in available_rooms:
        print(room_link)

    current_date = current_end_date

# Close the browser
driver.quit()



"""