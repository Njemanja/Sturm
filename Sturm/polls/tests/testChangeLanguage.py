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

class TestChangeLanguage(unittest.TestCase):

    def setUp(self):
        logging.info("SETUP testChangeLanguage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.login()
        self.languageSelect = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "languageSelect")))

    def test01ChangeLanguageToEnglish(self):
        try:
            logging.info("TEST: Starting the test01ChangeLanguageToEnglish.")
            self.languageSelect.click()
            englishOption = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//select[@id='languageSelect']/option[@value='/en']")))
            englishOption.click()
            link = WebDriverWait(self.driver, 10).until( EC.visibility_of_element_located((By.XPATH, "//a[contains(@href, '/history/') and text()='History']")))
            self.assertIsNotNone(link, "Change language failed.")
            logging.info("test01ChangeLanguageToEnglish: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    @unittest.skip("Test test02ChangeLanguageToDeutsch skipped")
    def test02ChangeLanguageToDeutsch(self):
        try:
            logging.info("TEST: Starting the test02ChangeLanguageToDeutsch.")
            self.languageSelect.click()
            deutschOption = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//select[@id='languageSelect']/option[@value='/de']")))
            deutschOption.click()
            link = WebDriverWait(self.driver, 10).until( EC.visibility_of_element_located((By.XPATH, "//a[contains(@href, '/history/') and text()='Geschichte']")))
            self.assertIsNotNone(link, "Change language failed.")
            logging.info("test02ChangeLanguageToDeutsch: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    @unittest.skip("Test test03ChangeLanguageToCyrillic skipped")
    def test03ChangeLanguageToCyrillic(self):
        try:
            logging.info("TEST: Starting the test03ChangeLanguageToCyrillic.")
            self.languageSelect.click()
            cyrillicOption = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//select[@id='languageSelect']/option[@value='/sr-cyrl']")))
            cyrillicOption.click()
            link = WebDriverWait(self.driver, 10).until( EC.visibility_of_element_located((By.XPATH, "//a[contains(@href, '/history/') and text()='Историја']")))
            self.assertIsNotNone(link, "Change language failed.")
            logging.info("test03ChangeLanguageToCyrillic: Successful.")

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
        logging.info("TEARDOWN testChangeLanguage")
        if self.driver:
            self.driver.quit()


if __name__ == '__main__':
    unittest.main()
