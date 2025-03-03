import traceback
import unittest
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

class TestRegister(unittest.TestCase):
    successfulRegistration = False

    def setUp(self):
        logging.info("SETUP testRegister")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        url = "http://127.0.0.1:8000/sr/register/"
        self.driver.maximize_window()
        self.driver.get(url)
        self.usernameField = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "username")))
        self.nameField = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "name")))
        self.surnameField = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "surname")))
        self.emailField = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "email")))
        self.passwordField = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "password")))
        self.password1Field = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "password1")))
        self.submit = WebDriverWait(self.driver, 10).until( EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
        self.username = "testReg123"
        self.name = "Test"
        self.surname = "Testic"
        self.email = "test@etf.rs"
        self.password = "Test1234!"
        self.password1 = "Test1234!"

    def test01RegisterNoUsername(self):
        try:
            logging.info("TEST: Starting the test01RegisterNoUsername.")
            self.usernameField.send_keys("")
            self.nameField.send_keys(self.name)
            self.surnameField.send_keys(self.surname)
            self.emailField.send_keys(self.email)
            self.passwordField.send_keys(self.password)
            self.password1Field.send_keys(self.password1)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite korisničko ime.", "Error message is incorrect or not displayed.")
            logging.info("test01RegisterNoUsername: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test02RegisterNoName(self):
        try:
            logging.info("TEST: Starting the test02RegisterNoName.")
            self.usernameField.send_keys(self.username)
            self.nameField.send_keys("")
            self.surnameField.send_keys(self.surname)
            self.emailField.send_keys(self.email)
            self.passwordField.send_keys(self.password)
            self.password1Field.send_keys(self.password1)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite ime.", "Error message is incorrect or not displayed.")
            logging.info("test02RegisterNoName: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test03RegisterNoSurname(self):
        try:
            logging.info("TEST: Starting the test03RegisterNoSurname.")
            self.usernameField.send_keys(self.username)
            self.nameField.send_keys(self.name)
            self.surnameField.send_keys("")
            self.emailField.send_keys(self.email)
            self.passwordField.send_keys(self.password)
            self.password1Field.send_keys(self.password1)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite prezime.", "Error message is incorrect or not displayed.")
            logging.info("test03RegisterNoSurname: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test04RegisterNoEmail(self):
        try:
            logging.info("TEST: Starting the test04RegisterNoEmail.")
            self.usernameField.send_keys(self.username)
            self.nameField.send_keys(self.name)
            self.surnameField.send_keys(self.surname)
            self.emailField.send_keys("")
            self.passwordField.send_keys(self.password)
            self.password1Field.send_keys(self.password1)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite email.", "Error message is incorrect or not displayed.")
            logging.info("test04RegisterNoEmail: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test05RegisterNoPassword(self):
        try:
            logging.info("TEST: Starting the test05RegisterNoPassword.")
            self.usernameField.send_keys(self.username)
            self.nameField.send_keys(self.name)
            self.surnameField.send_keys(self.surname)
            self.emailField.send_keys(self.email)
            self.passwordField.send_keys("")
            self.password1Field.send_keys(self.password1)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite lozinku.", "Error message is incorrect or not displayed.")
            logging.info("test05RegisterNoPassword: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test06RegisterNoPassword1(self):
        try:
            logging.info("TEST: Starting the test06RegisterNoPassword1.")
            self.usernameField.send_keys(self.username)
            self.nameField.send_keys(self.name)
            self.surnameField.send_keys(self.surname)
            self.emailField.send_keys(self.email)
            self.passwordField.send_keys(self.password)
            self.password1Field.send_keys("")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite lozinku i u drugo polje.", "Error message is incorrect or not displayed.")
            logging.info("test06RegisterNoPassword1: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test07RegisterBadUsernameLen(self):
        try:
            logging.info("TEST: Starting the test07RegisterBadUsernameLen.")
            self.usernameField.send_keys("t")
            self.nameField.send_keys(self.name)
            self.surnameField.send_keys(self.surname)
            self.emailField.send_keys(self.email)
            self.passwordField.send_keys(self.password)
            self.password1Field.send_keys(self.password1)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Korisničko ime mora imati između 6 i 25 karaktera  i može sadržati samo slova i cifre.", "Error message is incorrect or not displayed.")
            logging.info("test07RegisterBadUsernameLen: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test08RegisterBadUsernameLen(self):
        try:
            logging.info("TEST: Starting the test08RegisterBadUsernameLen.")
            self.usernameField.send_keys("tttttttttttttttttttttttttt")
            self.nameField.send_keys(self.name)
            self.surnameField.send_keys(self.surname)
            self.emailField.send_keys(self.email)
            self.passwordField.send_keys(self.password)
            self.password1Field.send_keys(self.password1)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Korisničko ime mora imati između 6 i 25 karaktera  i može sadržati samo slova i cifre.", "Error message is incorrect or not displayed.")
            logging.info("test07RegisterBadUsernameLen: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test09RegisterDiffPasswords(self):
        try:
            logging.info("TEST: Starting the test09RegisterDiffPasswords.")
            self.usernameField.send_keys(self.username)
            self.nameField.send_keys(self.name)
            self.surnameField.send_keys(self.surname)
            self.emailField.send_keys(self.email)
            self.passwordField.send_keys(self.password)
            self.password1Field.send_keys("N"+self.password1)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unete lozinke nisu iste.", "Error message is incorrect or not displayed.")
            logging.info("test08RegisterDiffPasswords: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test10RegisterBadLenPassword(self):
        try:
            logging.info("TEST: Starting the test10RegisterBadLenPassword.")
            self.usernameField.send_keys(self.username)
            self.nameField.send_keys(self.name)
            self.surnameField.send_keys(self.surname)
            self.emailField.send_keys(self.email)
            self.passwordField.send_keys("exam")
            self.password1Field.send_keys("exam")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text,"Lozinka mora imati minimalno 6 karaktera, barem jednu cifru i barem jedan specijalni znak.", "Error message is incorrect or not displayed.")
            logging.info("test09RegisterBadLenPassword: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    @unittest.skip("Test test11RegisterWithoutUpperLetterPassword skipped")
    def test11RegisterWithoutUpperLetterPassword(self):
        try:
            logging.info("TEST: Starting the test11RegisterWithoutUpperLetterPassword.")
            self.usernameField.send_keys(self.username)
            self.nameField.send_keys(self.name)
            self.surnameField.send_keys(self.surname)
            self.emailField.send_keys(self.email)
            self.passwordField.send_keys("example123!")
            self.password1Field.send_keys("example123!")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text,"Lozinka mora imati minimalno 6 karaktera, barem jednu cifru i barem jedan specijalni znak.", "Error message is incorrect or not displayed.")
            logging.info("test10RegisterWithoutUpperLetterPassword: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test12RegisterWithoutSpecialCharPassword(self):
        try:
            logging.info("TEST: Starting the test12RegisterWithoutSpecialCharPassword.")
            self.usernameField.send_keys(self.username)
            self.nameField.send_keys(self.name)
            self.surnameField.send_keys(self.surname)
            self.emailField.send_keys(self.email)
            self.passwordField.send_keys("Example123")
            self.password1Field.send_keys("Example123")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text,"Lozinka mora imati minimalno 6 karaktera, barem jednu cifru i barem jedan specijalni znak.", "Error message is incorrect or not displayed.")
            logging.info("test11RegisterWithoutSpecialCharPassword: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test13RegisterWithoutNumberPassword(self):
        try:
            logging.info("TEST: Starting the test13RegisterWithoutNumberPassword.")
            self.usernameField.send_keys(self.username)
            self.nameField.send_keys(self.name)
            self.surnameField.send_keys(self.surname)
            self.emailField.send_keys(self.email)
            self.passwordField.send_keys("Example!")
            self.password1Field.send_keys("Example!")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text,"Lozinka mora imati minimalno 6 karaktera, barem jednu cifru i barem jedan specijalni znak.", "Error message is incorrect or not displayed.")
            logging.info("test12RegisterWithoutNumberPassword: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test14RegisterUsernameExists(self):
        try:
            logging.info("TEST: Starting the test14RegisterUsernameExists.")
            self.usernameField.send_keys("admin1")
            self.nameField.send_keys(self.name)
            self.surnameField.send_keys(self.surname)
            self.emailField.send_keys(self.email)
            self.passwordField.send_keys(self.password)
            self.password1Field.send_keys(self.password1)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Korisničko ime već postoji.", "Error message is incorrect or not displayed.")
            logging.info("test13RegisterUsernameExists: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test15RegisterEmailExists(self):
        try:
            logging.info("TEST: Starting the test15RegisterEmailExists.")
            self.usernameField.send_keys(self.username)
            self.nameField.send_keys(self.name)
            self.surnameField.send_keys(self.surname)
            self.emailField.send_keys("kn233091m@student.etf.bg.ac.rs")
            self.passwordField.send_keys(self.password)
            self.password1Field.send_keys(self.password1)
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Email već postoji.", "Error message is incorrect or not displayed.")
            logging.info("test14RegisterEmailExists: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test16RegisterSuccessful(self):
        try:
            logging.info("TEST: Starting the test16RegisterSuccessful.")
            self.usernameField.send_keys(self.username)
            self.nameField.send_keys(self.name)
            self.surnameField.send_keys(self.surname)
            self.emailField.send_keys(self.email)
            self.passwordField.send_keys(self.password)
            self.password1Field.send_keys(self.password1)
            self.submit.click()

            WebDriverWait(self.driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/sr/login/"))
            current_url = self.driver.current_url
            self.assertEqual(current_url, "http://127.0.0.1:8000/sr/login/", "After successful registration, redirection to the login page did not occur.")
            TestRegister.successfulRegistration = True
            logging.info("test15RegisterSuccessful: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def tearDown(self):
        logging.info("TEARDOWN testRegister")
        if self.driver:
            self.driver.quit()

if __name__ == '__main__':
    unittest.main()