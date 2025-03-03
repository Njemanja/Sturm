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

class TestQuiz(unittest.TestCase):

    def setUp(self):
        logging.info("SETUP testQuiz")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.login()
        self.driver.get("http://127.0.0.1:8000/sr/quiz/")

    def test01QuizGoodAnswer(self):
        try:
            logging.info("TEST: Starting the test01QuizGoodAnswer.")
            correctField = self.driver.find_element(By.CSS_SELECTOR, 'button[data-correct="True"]')
            correctField.click()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'score')))
            scoreField = self.driver.find_element(By.ID, 'score').text
            self.assertEqual(scoreField, "1", "Error score.")
            logging.info("test01QuizGoodAnswer: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test02QuizBadAnswer(self):
        try:
            logging.info("TEST: Starting the test02QuizBadAnswer.")
            badField = self.driver.find_element(By.CSS_SELECTOR, 'button[data-correct="False"]')
            badField.click()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'score')))
            scoreField = self.driver.find_element(By.ID, 'score').text
            #self.assertEqual(scoreField, "0", "Error score.")
            logging.info("test02QuizBadAnswer: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test03GoodTable(self):
        try:
            logging.info("TEST: Starting the test03GoodTable.")
            showTableField = self.driver.find_element(By.ID, 'showTableBtn')
            showTableField.click()
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'scoreTable')))
            while True:
                try:
                    showMoreField = self.driver.find_element(By.ID, 'showMoreBtn')
                    showMoreField.click()
                    WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located((By.ID, 'showMoreBtn')))
                except:
                    break

            userFound = False
            score = None

            rows = self.driver.find_elements(By.CSS_SELECTOR, '.score-row')
            for row in rows:
                usernameField = row.find_element(By.XPATH, './td[1]')
                scoreField = row.find_element(By.XPATH, './td[2]')
                if usernameField.text == "testReg123":
                    userFound = True
                    score = scoreField.text
                    break

            if not userFound:
                self.fail('User not found in table.')
            else:
                self.assertEqual(score, "0", 'Bad score in table.".')

            logging.info("test03GoodTable: Successful.")

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
        logging.info("TEARDOWN testQuiz")
        if self.driver:
            self.driver.quit()


if __name__ == '__main__':
    unittest.main()
