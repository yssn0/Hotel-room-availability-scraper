# Hotel room availability scraper



## Libraries and Modules

1. **Selenium**: A library used for automating web browser interaction.
   - **`webdriver`**: Provides methods to control web browsers.
   - **`By`**: Used to locate elements on a web page via different strategies (e.g., ID, name, XPath, etc.).
   - **`WebDriverWait`**: Facilitates waiting for certain conditions to be met before proceeding with the next command.
   - **`expected_conditions` (EC)**: Contains predefined conditions to use with WebDriverWait.
   - **`keys`**: Provides keyboard interactions such as pressing keys.

2. **Built-in Modules**:
   - **`time`**: Used for time-related functions.
   - **`datetime`**: Used for manipulating dates and times.

## Code Breakdown

### Initialization and Setup

#### 1. WebDriver Initialization:
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import datetime
```
- **Import Statements**: Various selenium modules and built-in Python modules are imported.

```python
# Set up the web driver
driver = webdriver.Chrome()
driver.get("")  # Ensure this URL is correct for your target site
```
- **WebDriver**: Initializes a Chrome browser instance.
- **Navigate to URL**: Opens the specified URL (empty string here, so replace with the actual target site URL).

### Date Setup

#### 2. Initial Start and End Dates:
```python
start_date = "2024-07-15"
end_date = "2024-08-31"
```
- **Date Variables**: Defines the `start_date` and `end_date` for the search.

#### 3. Explicit Wait Setup:
```python
wait = WebDriverWait(driver, 20)
wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".ant-spin-spinning")))
```
- **`WebDriverWait`**: Creates an explicit wait instance to wait up to 20 seconds.
- **`EC.invisibility_of_element_located`**: Waits until the spinner element (loading indicator) becomes invisible.

### Iterating Through Date Ranges

#### 4. Date Initialization and Looping:
```python
current_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")
```
- **Convert Strings to Dates**: Parses the date strings into `datetime` objects for easier manipulation.

```python
while current_date + datetime.timedelta(days=2) <= end_date_obj:
    current_end_date = current_date + datetime.timedelta(days=2)
    current_end_date_str = current_end_date.strftime("%Y-%m-%d")
```
- **Date Loop**: Iterates every 2 days from `current_date` to `end_date`.
- **Calculate New End Dates**: Adds 2 days to `current_date` each iteration and converts it back to string format.

### Interacting with Date Inputs

#### 5. Element Selection:
```python
start_date_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-picker-input input[placeholder='Start date']")))
end_date_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-picker-input input[placeholder='End date']")))
```
- **Locate Date Inputs**: Finds the date input fields for start and end dates using CSS selectors.

#### 6. Setting Dates:
```python
driver.execute_script("arguments[0].removeAttribute('readonly')", start_date_input)  # Remove readonly if present
start_date_input.click()
start_date_input.send_keys(Keys.CONTROL + "a")
start_date_input.send_keys(Keys.DELETE)
start_date_input.send_keys(current_date.strftime("%Y-%m-%d"))
start_date_input.send_keys(Keys.ENTER)
```
- **Remove `readonly` Attribute**: Executes JavaScript to remove the `readonly` attribute to make the input field editable.
- **Input Date**: Clears the input field and enters the `current_date`.

Repeat the same steps for the end date:
```python
driver.execute_script("arguments[0].removeAttribute('readonly')", end_date_input)
end_date_input.click()
end_date_input.send_keys(Keys.CONTROL + "a")
end_date_input.send_keys(Keys.DELETE)
end_date_input.send_keys(current_end_date_str)
end_date_input.send_keys(Keys.ENTER)
```

### Performing the Search

#### 7. Click Search Button:
```python
search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'vérifier la disponibilitée')]")))
search_button.click()
```
- **Locate and Click**: Finds and clicks the "vérifier la disponibilitée" button using XPath.

#### 8. Wait for Results:
```python
time.sleep(5)
```
- **Wait**: Pauses execution for 5 seconds to allow search results to load.

### Extracting Information

#### 9. Locate "Réserver" Buttons:
```python
reserver_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Réserver')]")
```
- **Find Elements**: Retrieves all buttons with the text "Réserver" using XPath.

#### 10. Collect Available Room Links:
```python
available_rooms = []
for button in reserver_buttons:
    room_link = button.get_attribute("href")
    available_rooms.append(room_link)
```
- **Extract Links**: Loops through buttons and extracts their `href` attribute to get the links.

### Display Results

#### 11. Print Results:
```python
print(f"List of links for available rooms from {current_date.strftime('%Y-%m-%d')} to {current_end_date_str}:")
for room_link in available_rooms:
    print(room_link)
```
- **Print**: Outputs the list of available room links for the current date range.

#### 12. Update Current Date:
```python
current_date = current_end_date
```
- **Progress**: Advances the current date by 2 days for the next iteration.

### Closing the Browser

#### 13. Clean Up:
```python
driver.quit()
```
- **Close**: Shuts down the browser instance to free up resources.

### Summary

1. **Initialization**: Set up WebDriver and navigate to the target site.
2. **Date Processing**: Convert date strings for iteration.
3. **Loop Through Dates**: Increment date ranges by 2 days.
4. **Interact with Inputs**: Input the dates into the search fields.
5. **Perform Search**: Click the search button and wait for results.
6. **Extract Information**: Retrieve links for available rooms.
7. **Display Results**: Print the extracted links to the console.
8. **Clean Up**: Close the browser after processing all date ranges.

This script essentially automates the process of iterating through date ranges, performing searches on a web page, and extracting specific information based on the presence of certain elements.