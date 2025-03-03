import os
import sys
import traceback
import unittest
import logging

import django
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestNewPassword(unittest.TestCase):
    forgotPassowrdCall = False

    def setUp(self):
        logging.info("SETUP testNewPassword")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        url = "http://127.0.0.1:8000/sr/forgotPassword/"
        self.driver.maximize_window()
        self.driver.get(url)
        self.emailField = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "email")))
        self.submit = WebDriverWait(self.driver, 10).until( EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
        with open('../../token.txt', 'r') as tokenFile:
            token = tokenFile.read().strip()
        url = f"http://127.0.0.1:8000/sr/newPassword/{token}/"
        self.driver.get(url)
        self.passwordField = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "password")))
        self.password1Field = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "password1")))
        self.submit = WebDriverWait(self.driver, 10).until( EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
        self.password = "Test123#"

    def test01NewPasswordNoPassword(self):
        try:
            logging.info("TEST: Starting the test01NewPasswordNoPassword.")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite lozinku.", "Error message is incorrect or not displayed.")
            logging.info("test01NewPasswordNoPassword: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test02NewPasswordNoPassword1(self):
        try:
            logging.info("TEST: Starting the test02NewPasswordNoPassword1.")
            self.passwordField.send_keys(self.password)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite lozinku i u drugo polje.", "Error message is incorrect or not displayed.")
            logging.info("test02NewPasswordNoPassword1: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test03NewPasswordDiffPasswords(self):
        try:
            logging.info("TEST: Starting the test03NewPasswordDiffPasswords.")
            self.passwordField.send_keys(self.password)
            self.password1Field.send_keys("N" + self.password)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unete lozinke nisu iste.", "Error message is incorrect or not displayed.")
            logging.info("test03NewPasswordDiffPasswords: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test04NewPasswordBadLenPassword(self):
        try:
            logging.info("TEST: Starting the test04NewPasswordBadLenPassword.")
            self.passwordField.send_keys(self.password[:3])
            self.password1Field.send_keys(self.password[:3])
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text,"Lozinka mora imati minimalno 6 karaktera, barem jednu cifru i barem jedan specijalni znak.", "Error message is incorrect or not displayed.")
            logging.info("test04NewPasswordBadLenPassword: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test05NewPasswordWithoutSpecialCharPassword(self):
        try:
            logging.info("TEST: Starting the test05NewPasswordWithoutSpecialCharPassword.")
            self.passwordField.send_keys("Example123")
            self.password1Field.send_keys("Example123")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text,"Lozinka mora imati minimalno 6 karaktera, barem jednu cifru i barem jedan specijalni znak.", "Error message is incorrect or not displayed.")
            logging.info("test05NewPasswordWithoutSpecialCharPassword: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test06NewPasswordWithoutNumberPassword(self):
        try:
            logging.info("TEST: Starting the test06NewPasswordWithoutNumberPassword.")
            self.passwordField.send_keys("Example!")
            self.password1Field.send_keys("Example!")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text,"Lozinka mora imati minimalno 6 karaktera, barem jednu cifru i barem jedan specijalni znak.", "Error message is incorrect or not displayed.")
            logging.info("test06NewPasswordWithoutNumberPassword: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test07NewPasswordSuccessful(self):
        try:
            logging.info("TEST: Starting the test07NewPasswordSuccessful.")
            self.passwordField.send_keys(self.password)
            self.password1Field.send_keys(self.password)
            self.submit.click()
            WebDriverWait(self.driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/sr/login/"))
            current_url = self.driver.current_url
            self.assertEqual(current_url, "http://127.0.0.1:8000/sr/login/", "After successful change password, redirection to the login page did not occur.")
            logging.info("test07NewPasswordSuccessful: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def forgotPassword(self):
        try:
            logging.info("TEST: Starting the test03ForgotPasswordSuccessful.")
            self.emailField.send_keys("kn233091m@student.etf.bg.ac.rs")
            self.submit.click()

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")


    def tearDown(self):
        logging.info("TEARDOWN testNewPassword")
        if self.driver:
            self.driver.quit()


if __name__ == '__main__':
    unittest.main()
