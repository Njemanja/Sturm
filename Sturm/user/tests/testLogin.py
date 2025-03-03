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

class TestLogin(unittest.TestCase):

    def setUp(self):
        logging.info("SETUP testLogin")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        url = "http://127.0.0.1:8000/sr/login/"
        self.driver.maximize_window()
        self.driver.get(url)
        self.usernameField = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "username")))
        self.passwordField = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "password")))
        self.submit = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
        self.username = "testReg123"
        self.password = "Test1234!"

    def test01LoginNoUsernameNoPassword(self):
        try:
            logging.info("TEST: Starting the test01LoginNoUsernameNoPassword.")
            self.usernameField.send_keys("")
            self.passwordField.send_keys("")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite korisničko ime i lozinku.",
                             "Error message is incorrect or not displayed.")
            logging.info("test01LoginNoUsernameNoPassword: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test02LoginNoUsername(self):
        try:
            logging.info("TEST: Starting the test02LoginNoUsername.")
            self.usernameField.send_keys("")
            self.passwordField.send_keys(self.password)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite korisničko ime.", "Error message is incorrect or not displayed.")
            logging.info("test02LoginNoUsername: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test03LoginNoPassword(self):
        try:
            logging.info("TEST: Starting the test03LoginNoPassword.")
            self.usernameField.send_keys(self.username)
            self.passwordField.send_keys("")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite lozinku.", "Error message is incorrect or not displayed.")
            logging.info("test03LoginNoPassword: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test04LoginNoUser(self):
        try:
            logging.info("TEST: Starting the test04LoginNoUser.")
            self.usernameField.send_keys(self.username)
            self.passwordField.send_keys("N" + self.password)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Korisničko ime ili lozinka nisu ispravni.",
                             "Error message is incorrect or not displayed.")
            logging.info("test04LoginNoUser: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test05LoginSuccessful(self):
        try:
            logging.info("TEST: Starting the test05LoginSuccessful.")
            self.usernameField.send_keys(self.username)
            self.passwordField.send_keys(self.password)
            self.submit.click()

            WebDriverWait(self.driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/sr/index/"))
            current_url = self.driver.current_url
            self.assertEqual(current_url, "http://127.0.0.1:8000/sr/index/",
                             "After successful login, redirection to the index page did not occur.")
            logging.info("test05LoginSuccessful: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def tearDown(self):
        logging.info("TEARDOWN testLogin")
        if self.driver:
            self.driver.quit()


if __name__ == '__main__':
    unittest.main()
