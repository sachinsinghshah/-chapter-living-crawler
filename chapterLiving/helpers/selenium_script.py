import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from faker import Faker


class SeleniumHelper:
    def __init__(self):
         # Initialize Selenium WebDriver and other necessary components
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)  # WebDriverWait for waiting until elements appear
        self.fake = Faker() # Faker for generating fake data
    
    def fill_fake_information(self):
         # Fill form fields with fake data
        first_name_input = self.driver.find_element(By.CSS_SELECTOR, '[name="applicant[name_first]"]')
        first_name_input.send_keys(self.fake.first_name())

        last_name_input = self.driver.find_element(By.CSS_SELECTOR, '[name="applicant[name_last]"]')
        last_name_input.send_keys(self.fake.last_name())

        phone_input = self.driver.find_element(By.CSS_SELECTOR, ".phone-number")
        phone_input.send_keys(self.fake.numerify(text='##########'))

        username_input = self.driver.find_element(By.CSS_SELECTOR, "#applicant_username")
        username_input.send_keys(self.fake.email())
        
        password = self.fake.password()

        password_input = self.driver.find_element(By.CSS_SELECTOR, "#applicant_password")
        password_input.send_keys(password)

        password_confirm_input = self.driver.find_element(By.CSS_SELECTOR, "#applicant_password_confirm")
        password_confirm_input.send_keys(password)
        
        check_agree = self.driver.find_element(By.CSS_SELECTOR, '#agrees_to_terms')
        self.scroll_element_into_view(check_agree)
        check_agree.click()
    
    def scroll_element_into_view(self, element):
        # Scroll element into view using JavaScript
        viewport_height = self.driver.execute_script("return window.innerHeight")
        element_y = element.location['y']
        midpoint = element_y - (viewport_height / 2) + (element.size['height'] / 2)

        # Scroll the element into view using JavaScript
        self.driver.execute_script(f"window.scrollTo(0, {midpoint});")
    
    def dismiss_cookies_consent(self):
        # Dismiss cookies consent if present
        try:
            cookies_consent = self.driver.find_element(By.CSS_SELECTOR, '.banner-close-button, #pc_banner_reject_all')
            if cookies_consent:
                cookies_consent.click()
        except NoSuchElementException:
            pass

    def navigate_and_extract_data(self, url):
        try:
            # Navigate to the URL
            self.driver.get(url)
            sleep(5)
            
            # Dismiss cookies consent if present
            self.driver.maximize_window()
            
            self.dismiss_cookies_consent()
                

            # Select property and period
            select_where_button = self.driver.find_element(By.CSS_SELECTOR, '[data-val-required="Please select a property"]')
            
            self.scroll_element_into_view(select_where_button)
            
            sleep(1)

            select_where_option = Select(self.driver.find_element(By.CSS_SELECTOR, '[data-val-required="Please select a property"]'))
            select_where_option.select_by_visible_text("CHAPTER KINGS CROSS")

            sleep(1)
    
            select_when_option = Select(self.driver.find_element(By.ID , "BookingAvailabilityForm_BookingPeriod"))
            
            select_when_option.select_by_visible_text("SEP 24 - AUG 25 (51 WEEKS)")

            sleep(3)
 
            check_type = self.driver.find_element(By.CSS_SELECTOR, '#filter-room-type-ensuite')
            self.scroll_element_into_view(check_type)
            check_type.click()
            
            sleep(3)
   
            detail_button = self.driver.find_element(By.CSS_SELECTOR, '.room-list-selection')
            self.scroll_element_into_view(detail_button)
            detail_button.click()
            sleep(5)
            self.dismiss_cookies_consent()

            self.fill_fake_information()
            
            submit_button = self.driver.find_element(By.CSS_SELECTOR, '#create-app-btn')
            self.scroll_element_into_view(submit_button)
            submit_button.click()
            
            sleep(2)
            
            confirm_button = self.driver.find_element(By.CSS_SELECTOR, '.js-confirm')
            self.scroll_element_into_view(confirm_button)

            confirm_button.click()
            
            sleep(20)
                
            data = []
            # Extract data from the page
            details_container = self.driver.find_elements(By.CSS_SELECTOR, '.sus-unit-space-details')
            
            for detail in details_container:
                self.scroll_element_into_view(detail)
                values = detail.find_elements(By.CSS_SELECTOR, '.value')
                
                unit_spaces = detail.find_elements(By.CSS_SELECTOR, '.value')
                
                
                data_dict = {
                    "Building": values[0].text,
                    "Rent": values[1].text,
                    "Deposit": values[2].text,
                    "Amenities": values[3].text,
                    "Space": unit_spaces[1].text,
                    "Status": unit_spaces[2].text,
                    "date": datetime.datetime.now(tz=datetime.timezone.utc)
                }
                data.append(data_dict)
            
            print(data)
            
            return data

        except TimeoutException:
            print("Timeout waiting for page to load")
            
    def close_driver(self):
        # Close the Selenium WebDriver instance
        self.driver.quit()  
            
    