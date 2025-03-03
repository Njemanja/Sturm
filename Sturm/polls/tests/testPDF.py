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

class TestPDF(unittest.TestCase):

    def setUp(self):
        logging.info("SETUP testPDF")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.login()
        url = "http://127.0.0.1:8000/sr/history/"
        self.driver.get(url)
        self.pdfField = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//td/a[contains(text(), 'Preuzmi PDF')]")))

    def test01PDFSuccessful(self):
        try:
            logging.info("TEST: Starting the test01PDFSuccessful.")
            self.pdfField.click()
            logging.info("test01PDFSuccessful: Successful.")

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
        logging.info("TEARDOWN testPDF")
        if self.driver:
            self.driver.quit()


if __name__ == '__main__':
    unittest.main()
