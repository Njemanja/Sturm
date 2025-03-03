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

class TestMenu(unittest.TestCase):

    def setUp(self):
        logging.info("SETUP testMenu")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.login()
        self.indexField = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Početna strana")))
        self.historyField = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Istorija")))
        self.quizField = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Kviz")))
        self.helpField = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Pomoć")))
        self.profileField = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Profil")))
        self.contactField = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Kontakt")))

    def test01IndexSuccessful(self):
        try:
            logging.info("TEST: Starting the test01IndexSuccessful.")
            self.indexField.click()
            WebDriverWait(self.driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/sr/index/"))
            current_url = self.driver.current_url
            self.assertEqual(current_url, "http://127.0.0.1:8000/sr/index/","Redirection to the index page did not occur.")
            logging.info("test01IndexSuccessful: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test02HistorySuccessful(self):
        try:
            logging.info("TEST: Starting the test02HistorySuccessful.")
            self.historyField.click()
            WebDriverWait(self.driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/sr/history/"))
            current_url = self.driver.current_url
            self.assertEqual(current_url, "http://127.0.0.1:8000/sr/history/","Redirection to the history page did not occur.")
            logging.info("test02HistorySuccessful: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test03QuizSuccessful(self):
        try:
            logging.info("TEST: Starting the test03QuizSuccessful.")
            self.quizField.click()
            WebDriverWait(self.driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/sr/quiz/"))
            current_url = self.driver.current_url
            self.assertEqual(current_url, "http://127.0.0.1:8000/sr/quiz/","Redirection to the quiz page did not occur.")
            logging.info("test03QuizSuccessful: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test04HelpSuccessful(self):
        try:
            logging.info("TEST: Starting the test04HelpSuccessful.")
            self.helpField.click()
            WebDriverWait(self.driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/sr/help/"))
            current_url = self.driver.current_url
            self.assertEqual(current_url, "http://127.0.0.1:8000/sr/help/","Redirection to the help page did not occur.")
            logging.info("test04HelpSuccessful: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test05ProfileSuccessful(self):
        try:
            logging.info("TEST: Starting the test05ProfileSuccessful.")
            self.profileField.click()
            WebDriverWait(self.driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/sr/profile/"))
            current_url = self.driver.current_url
            self.assertEqual(current_url, "http://127.0.0.1:8000/sr/profile/","Redirection to the profile page did not occur.")
            logging.info("test05ProfileSuccessful: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test06ContactSuccessful(self):
        try:
            logging.info("TEST: Starting the test06ContactSuccessful.")
            self.contactField.click()
            WebDriverWait(self.driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/sr/contact/"))
            current_url = self.driver.current_url
            self.assertEqual(current_url, "http://127.0.0.1:8000/sr/contact/","Redirection to the contact page did not occur.")
            logging.info("test06ContactSuccessful: Successful.")

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
        logging.info("TEARDOWN testMenu")
        if self.driver:
            self.driver.quit()


if __name__ == '__main__':
    unittest.main()
