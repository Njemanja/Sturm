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

class TestLogout(unittest.TestCase):

    def setUp(self):
        logging.info("SETUP testLogout")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.login()
        self.logoutField = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Odjavi se")))

    def test01LogoutSuccessful(self):
        try:
            logging.info("TEST: Starting the test01LogoutSuccessful.")
            self.logoutField.click()
            WebDriverWait(self.driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/sr/login/"))
            current_url = self.driver.current_url
            self.assertEqual(current_url, "http://127.0.0.1:8000/sr/login/",
                             "After successful logout, redirection to the login page did not occur.")
            logging.info("test01LogoutSuccessful: Successful.")

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
        logging.info("TEARDOWN testLogout")
        if self.driver:
            self.driver.quit()


if __name__ == '__main__':
    unittest.main()
