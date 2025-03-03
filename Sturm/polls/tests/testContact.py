import traceback
import unittest
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestContact(unittest.TestCase):

    def setUp(self):
        logging.info("SETUP testContact")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.login()
        self.contactField = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Kontakt")))
        self.contactField.click()
        self.messageField = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "message")))
        self.submit = WebDriverWait(self.driver, 10).until( EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))

    def test01ContactNoMessage(self):
        try:
            logging.info("TEST: Starting the test01ContactNoMessage.")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite poruku.", "Error message is incorrect or not displayed.")
            logging.info("test01ContactNoMessage: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test02ContactSuccessful(self):
        try:
            logging.info("TEST: Starting the test01ContactSuccessful.")
            self.messageField.send_keys("test01ContactSuccessful poruka.")
            self.submit.click()
            successfulField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".succDiv .message")))
            self.assertEqual(successfulField.text, "Uspešno ste poslali poruku. Očekujte odgovor na email adresu.", "Error message is incorrect or not displayed.")
            logging.info("test01ContactSuccessful: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")


    def login(self):
        url = "http://127.0.0.1:8000/sr/login/"
        self.driver.maximize_window()
        self.driver.get(url)
        usernameField = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "username")))
        passwordField = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "password")))
        submit = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
        usernameField.send_keys("testReg123")
        passwordField.send_keys("Test1234!")
        submit.click()

    def tearDown(self):
        logging.info("TEARDOWN testContact")
        if self.driver:
            self.driver.quit()


if __name__ == '__main__':
    unittest.main()
