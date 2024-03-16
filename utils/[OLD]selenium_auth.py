from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.config import auth_creds
from utils.api_variables import url_auth, url_logout
import time
import json

def login_and_extract_token(username, password):
    """Login to the website and extract JWT token."""
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--mute-audio')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--disable-infobars')
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--no-sandbox')
    options.add_argument('--no-zygote')
    options.add_argument('--log-level=3')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--disable-breakpad')
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    
    try:
        print('[Starting...]')
        # Navigate to the login page
        driver.get(url_auth)

        # Fill in the username and password fields
        username_input = driver.find_element(By.NAME, 'username')
        username_input.send_keys(username)

        password_input = driver.find_element(By.NAME, 'password')
        password_input.send_keys(password)

        # Submit the form
        login_button = driver.find_element(By.CLASS_NAME, 'button')
        login_button.click()
        time.sleep(1)
        # Logout
        driver.get(url_logout)
        time.sleep(1)

        # Extract JWT token from local storage
        print('[Getting token...]')
        jwt_data = json.loads(driver.execute_script("return localStorage.getItem('edu-token-collection')"))
        first_key = next(iter(jwt_data.keys()))
        token = jwt_data[first_key]["token"]

        return token
    finally:
        driver.quit()
    
def save_token_to_json(token, filename="token.json"):
    """Save the token to a JSON file."""
    try:
        with open(filename, "w") as file:
            json.dump({"token": token}, file, indent=4)
        return True
    except Exception as e:
        return False

def get_token():
    token = login_and_extract_token(auth_creds['username'], auth_creds['password'])
    if token:
        success = save_token_to_json(token)   
        return success
    return False