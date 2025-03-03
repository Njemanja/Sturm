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

class TestIndex(unittest.TestCase):

    def setUp(self):
        logging.info("SETUP testIndex")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.login()
        self.polyField = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "polinomInput")))
        self.lowerField = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "lower")))
        self.upperField = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "upper")))
        self.decimalsField = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "decimals")))
        self.submit = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
        self.poly = "x**2"
        self.lower = 0
        self.upper = 2
        self.decimals = 2

    def test01IndexNoPoly(self):
        try:
            logging.info("TEST: Starting the test01IndexNoPoly.")
            self.polyField.send_keys("")
            self.lowerField.send_keys(self.lower)
            self.upperField.send_keys(self.upper)
            self.decimalsField.send_keys(self.decimals)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite polinom.","Error message is incorrect or not displayed.")
            logging.info("test01IndexNoPoly: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test02IndexNoLower(self):
        try:
            logging.info("TEST: Starting the test02IndexNoLower.")
            self.polyField.send_keys(self.poly)
            self.lowerField.send_keys("")
            self.upperField.send_keys(self.upper)
            self.decimalsField.send_keys(self.decimals)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite donju granicu.","Error message is incorrect or not displayed.")
            logging.info("test02IndexNoLower: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test03IndexNoUpper(self):
        try:
            logging.info("TEST: Starting the test03IndexNoUpper.")
            self.polyField.send_keys(self.poly)
            self.lowerField.send_keys(self.lower)
            self.upperField.send_keys("")
            self.decimalsField.send_keys(self.decimals)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite gornju granicu.", "Error message is incorrect or not displayed.")
            logging.info("test03IndexNoUpper: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test04IndexNoDecimals(self):
        try:
            logging.info("TEST: Starting the test04IndexNoDecimals.")
            self.polyField.send_keys(self.poly)
            self.lowerField.send_keys(self.lower)
            self.upperField.send_keys(self.upper)
            self.decimalsField.send_keys("")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite broj decimala.", "Error message is incorrect or not displayed.")
            logging.info("test04IndexNoDecimals: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test05IndexLowerNotNumber(self):
        try:
            logging.info("TEST: Starting the test05IndexLowerNotNumber.")
            self.polyField.send_keys(self.poly)
            self.lowerField.send_keys("N")
            self.upperField.send_keys(self.upper)
            self.decimalsField.send_keys(self.decimals)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Donja, gornja granica i koficijent moraju biti brojevi.", "Error message is incorrect or not displayed.")
            logging.info("test05IndexLowerNotNumber: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test06IndexUpperNotNumber(self):
        try:
            logging.info("TEST: Starting the test06IndexUpperNotNumber.")
            self.polyField.send_keys(self.poly)
            self.lowerField.send_keys(self.lower)
            self.upperField.send_keys("M")
            self.decimalsField.send_keys(self.decimals)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Donja, gornja granica i koficijent moraju biti brojevi.", "Error message is incorrect or not displayed.")
            logging.info("test06IndexUpperNotNumber: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test07IndexDecimalsNotNumber(self):
        try:
            logging.info("TEST: Starting the test07IndexDecimalsNotNumber.")
            self.polyField.send_keys(self.poly)
            self.lowerField.send_keys(self.lower)
            self.upperField.send_keys(self.upper)
            self.decimalsField.send_keys("M")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Donja, gornja granica i koficijent moraju biti brojevi.", "Error message is incorrect or not displayed.")
            logging.info("test07IndexDecimalsNotNumber: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test08IndexBadPoly1(self):
        try:
            logging.info("TEST: Starting the test08IndexBadPoly1.")
            self.polyField.send_keys("x***2")
            self.lowerField.send_keys(self.lower)
            self.upperField.send_keys(self.upper)
            self.decimalsField.send_keys(self.decimals)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Polinom nije ispravan.", "Error message is incorrect or not displayed.")
            logging.info("test08IndexBadPoly1: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test09IndexBadPoly2(self):
        try:
            logging.info("TEST: Starting the test09IndexBadPoly2.")
            self.polyField.send_keys("kdalsdl")
            self.lowerField.send_keys(self.lower)
            self.upperField.send_keys(self.upper)
            self.decimalsField.send_keys(self.decimals)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Polinom nije ispravan.", "Error message is incorrect or not displayed.")
            logging.info("test09IndexBadPoly2: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test10IndexBadPoly3(self):
        try:
            logging.info("TEST: Starting the test10IndexBadPoly3.")
            self.polyField.send_keys("x**3*(2*1")
            self.lowerField.send_keys(self.lower)
            self.upperField.send_keys(self.upper)
            self.decimalsField.send_keys(self.decimals)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Polinom nije ispravan.", "Error message is incorrect or not displayed.")
            logging.info("test10IndexBadPoly3: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test11IndexLowerGreaterThanUpper(self):
        try:
            logging.info("TEST: Starting the test11IndexLowerGreaterThanUpper.")
            self.polyField.send_keys(self.poly)
            self.lowerField.send_keys(self.upper)
            self.upperField.send_keys(self.lower)
            self.decimalsField.send_keys(self.decimals)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Donja granica mora biti strogo manja od gornje.", "Error message is incorrect or not displayed.")
            logging.info("test11IndexLowerGreaterThanUpper: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test12IndexLowerEqualsUpper(self):
        try:
            logging.info("TEST: Starting the test12IndexLowerEqualsUpper.")
            self.polyField.send_keys(self.poly)
            self.lowerField.send_keys(self.upper)
            self.upperField.send_keys(self.upper)
            self.decimalsField.send_keys(self.decimals)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Donja granica mora biti strogo manja od gornje.", "Error message is incorrect or not displayed.")
            logging.info("test12IndexLowerEqualsUpper: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test13IndexNegativeDecimals(self):
        try:
            logging.info("TEST: Starting the test13IndexNegativeDecimals.")
            self.polyField.send_keys(self.poly)
            self.lowerField.send_keys(self.lower)
            self.upperField.send_keys(self.upper)
            self.decimalsField.send_keys(-1)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Broj decimala mora biti jednak ili veći od 0.", "Error message is incorrect or not displayed.")
            logging.info("test13IndexNegativeDecimals: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test14IndexSuccessful(self):
        try:
            logging.info("TEST: Starting the test14IndexSuccessful.")
            self.polyField.send_keys(self.poly)
            self.lowerField.send_keys(self.lower)
            self.upperField.send_keys(self.upper)
            self.decimalsField.send_keys(self.decimals)
            self.submit.click()
            resultField = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'glowing-text') and h1[text()='Rezultat']]")))
            self.assertTrue(resultField.is_displayed(), "Result div is not displayed.")
            logging.info("test14IndexSuccessful: Successful.")

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
        logging.info("TEARDOWN testIndex")
        if self.driver:
            self.driver.quit()


if __name__ == '__main__':
    unittest.main()
