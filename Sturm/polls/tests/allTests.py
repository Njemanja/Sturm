import unittest

# Uvezite testove
from testChangeLanguage import TestChangeLanguage
from testContact import TestContact
from Master.user.tests.testForgotPassword import TestForgotPassword
from testIndex import TestIndex
from Master.user.tests.testLogin import TestLogin
from Master.user.tests.testLogout import TestLogout
from testMenu import TestMenu
from Master.user.tests.testNewPassword import TestNewPassword
from testPDF import TestPDF
from Master.user.tests.testProfile import TestProfile
from testQuiz import TestQuiz
from Master.user.tests.testRegister import TestRegister

def run_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRegister))
    suite.addTest(unittest.makeSuite(TestLogin))
    suite.addTest(unittest.makeSuite(TestLogout))
    suite.addTest(unittest.makeSuite(TestMenu))
    suite.addTest(unittest.makeSuite(TestChangeLanguage))
    suite.addTest(unittest.makeSuite(TestContact))
    suite.addTest(unittest.makeSuite(TestIndex))
    suite.addTest(unittest.makeSuite(TestQuiz))
    suite.addTest(unittest.makeSuite(TestPDF))
    suite.addTest(unittest.makeSuite(TestProfile))
    suite.addTest(unittest.makeSuite(TestForgotPassword))
    suite.addTest(unittest.makeSuite(TestNewPassword))
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    run_tests()
