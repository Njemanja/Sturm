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

class TestForgotPassword(unittest.TestCase):

    def setUp(self):
        logging.info("SETUP testForgotPassword")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        url = "http://127.0.0.1:8000/sr/forgotPassword/"
        self.driver.maximize_window()
        self.driver.get(url)
        self.emailField = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "email")))
        self.submit = WebDriverWait(self.driver, 10).until( EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))

    def test01ForgotPasswordNoEmail(self):
        try:
            logging.info("TEST: Starting the test01ForgotPasswordNoEmail.")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite email.", "Error message is incorrect or not displayed.")
            logging.info("test01ForgotPasswordNoEmail: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test02ForgotPasswordEmailNotExists(self):
        try:
            logging.info("TEST: Starting the test02ForgotPasswordEmailNotExists.")
            self.emailField.send_keys("kn233091mm@student.etf.bg.ac.rs")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Korisnik sa datom email adresom ne postoji.", "Error message is incorrect or not displayed.")
            logging.info("test02ForgotPasswordEmailNotExists: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test03ForgotPasswordSuccessful(self):
        try:
            logging.info("TEST: Starting the test03ForgotPasswordSuccessful.")
            self.emailField.send_keys("kn233091m@student.etf.bg.ac.rs")
            self.submit.click()
            successfulField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".succDiv .message")))
            self.assertEqual(successfulField.text, "Uspešno ste poslali zahtev za promenu lozinke.", "Error message is incorrect or not displayed.")
            logging.info("test03ForgotPasswordSuccessful: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")


    def tearDown(self):
        logging.info("TEARDOWN testForgotPassword")
        if self.driver:
            self.driver.quit()


if __name__ == '__main__':
    unittest.main()
