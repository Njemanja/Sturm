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

class TestProfile(unittest.TestCase):

    def setUp(self):
        logging.info("SETUP testProfile")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.login()
        self.profileField = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Profil")))
        self.profileField.click()
        self.usernameField = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "username")))
        self.nameField = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "name")))
        self.surnameField = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "surname")))
        self.emailField = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "email")))
        self.passwordField = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "password")))
        self.password1Field = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "password1")))
        self.submit = WebDriverWait(self.driver, 10).until( EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))

    def test01ProfileNoUsername(self):
        try:
            logging.info("TEST: Starting the test01ProfileNoUsername.")
            self.usernameField.clear()
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite korisničko ime.", "Error message is incorrect or not displayed.")
            logging.info("test01ProfileNoUsername: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test02ProfileNoName(self):
        try:
            logging.info("TEST: Starting the test02ProfileNoName.")
            self.nameField.clear()
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite ime.", "Error message is incorrect or not displayed.")
            logging.info("test02ProfileNoName: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test03ProfileNoSurname(self):
        try:
            logging.info("TEST: Starting the test03ProfileNoSurname.")
            self.surnameField.clear()
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite prezime.", "Error message is incorrect or not displayed.")
            logging.info("test03ProfileNoSurname: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test04ProfileNoEmail(self):
        try:
            logging.info("TEST: Starting the test04ProfileNoEmail.")
            self.emailField.clear()
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite email.", "Error message is incorrect or not displayed.")
            logging.info("test04ProfileNoEmail: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test05ProfileBadUsernameLen(self):
        try:
            logging.info("TEST: Starting the test05ProfileBadUsernameLen.")
            self.usernameField.clear()
            self.usernameField.send_keys("t")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Korisničko ime mora imati između 6 i 25 karaktera  i može sadržati samo slova i cifre.", "Error message is incorrect or not displayed.")
            logging.info("test05ProfileBadUsernameLen: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test06RegisterBadUsernameLen(self):
        try:
            logging.info("TEST: Starting the test06RegisterBadUsernameLen.")
            self.usernameField.clear()
            self.usernameField.send_keys("tttttttttttttttttttttttttt")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text,
                             "Korisničko ime mora imati između 6 i 25 karaktera  i može sadržati samo slova i cifre.",
                             "Error message is incorrect or not displayed.")
            logging.info("test05ProfileBadUsernameLen: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test07ProfileEmailExists(self):
        try:
            logging.info("TEST: Starting the test07ProfileEmailExists.")
            self.emailField.clear()
            self.emailField.send_keys("kn233091m@student.etf.bg.ac.rs")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Korisnik sa datim emailom već postoji.", "Error message is incorrect or not displayed.")
            logging.info("test06ProfileEmailExists: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test08ProfileUsernameExists(self):
        try:
            logging.info("TEST: Starting the test08ProfileUsernameExists.")
            self.usernameField.clear()
            self.usernameField.send_keys("admin1")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Korisnik sa datim korisničkim imenom postoji.", "Error message is incorrect or not displayed.")
            logging.info("test07ProfileUsernameExists: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test09ProfileNoPassword1(self):
        try:
            logging.info("TEST: Starting the test09ProfileNoPassword1.")
            self.passwordField.send_keys("Test1234!")
            self.password1Field.send_keys("")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unesite lozinku i u drugo polje.", "Error message is incorrect or not displayed.")
            logging.info("test08ProfileNoPassword1: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test10ProfileDiffPasswords(self):
        try:
            logging.info("TEST: Starting the test10ProfileDiffPasswords.")
            self.passwordField.send_keys("Test1234!")
            self.password1Field.send_keys("Test1234!!")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text, "Unete lozinke nisu iste.", "Error message is incorrect or not displayed.")
            logging.info("test09ProfileDiffPasswords: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test11ProfileBadLenPassword(self):
        try:
            logging.info("TEST: Starting the test11ProfileBadLenPassword.")
            self.passwordField.send_keys("exam")
            self.password1Field.send_keys("exam")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text,"Lozinka mora imati minimalno 6 karaktera, barem jednu cifru i barem jedan specijalni znak.", "Error message is incorrect or not displayed.")
            logging.info("test10ProfileBadLenPassword: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    @unittest.skip("Test test12ProfileWithoutUpperLetterPassword skipped")
    def test12ProfileWithoutUpperLetterPassword(self):
        try:
            logging.info("TEST: Starting the test12ProfileWithoutUpperLetterPassword.")
            self.passwordField.send_keys("example123!")
            self.password1Field.send_keys("example123!")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text,"Lozinka mora imati minimalno 6 karaktera, barem jednu cifru i barem jedan specijalni znak.", "Error message is incorrect or not displayed.")
            logging.info("test11ProfileWithoutUpperLetterPassword: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test13ProfileWithoutSpecialCharPassword(self):
        try:
            logging.info("TEST: Starting the test13ProfileWithoutSpecialCharPassword.")
            self.passwordField.send_keys("Example123")
            self.password1Field.send_keys("Example123")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text,"Lozinka mora imati minimalno 6 karaktera, barem jednu cifru i barem jedan specijalni znak.", "Error message is incorrect or not displayed.")
            logging.info("test12ProfileWithoutSpecialCharPassword: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test14ProfileWithoutNumberPassword(self):
        try:
            logging.info("TEST: Starting the test14ProfileWithoutNumberPassword.")
            self.passwordField.send_keys("Example!")
            self.password1Field.send_keys("Example!")
            self.submit.click()
            errorField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errDiv .message")))
            self.assertEqual(errorField.text,"Lozinka mora imati minimalno 6 karaktera, barem jednu cifru i barem jedan specijalni znak.", "Error message is incorrect or not displayed.")
            logging.info("test13ProfileWithoutNumberPassword: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test15ProfileSuccessful(self):
        try:
            logging.info("TEST: Starting the test15ProfileSuccessful.")
            self.usernameField.clear()
            self.nameField.clear()
            self.surnameField.clear()
            self.emailField.clear()

            self.usernameField.send_keys("testReg1231")
            self.nameField.send_keys("Test!")
            self.surnameField.send_keys("Testic!")
            self.emailField.send_keys("test1@etf.rs")
            self.passwordField.send_keys("Test1234!!")
            self.password1Field.send_keys("Test1234!!")

            self.submit.click()

            successfulField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".succDiv .message")))
            self.assertEqual(successfulField.text,"Uspešno ste promenili podatke.","Error message is incorrect or not displayed.")

            logging.info("test14ProfileSuccessful: Successful.")

        except Exception:
            logging.error("TEST: Test failed due to an exception. Stack trace: %s", traceback.format_exc())
            self.fail("Test failed due to an exception.")

    def test16ProfileSuccessfulAgain(self):
        try:
            logging.info("TEST: Starting the test16ProfileSuccessfulAgain.")
            self.usernameField.clear()

            self.usernameField.send_keys("testReg123")
            self.passwordField.send_keys("Test1234!")
            self.password1Field.send_keys("Test1234!")

            self.submit.click()

            successfulField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".succDiv .message")))
            self.assertEqual(successfulField.text,"Uspešno ste promenili podatke.","Error message is incorrect or not displayed.")

            logging.info("test15ProfileSuccessfulAgain: Successful.")

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
        logging.info("TEARDOWN testProfile")
        if self.driver:
            self.driver.quit()


if __name__ == '__main__':
    unittest.main()
