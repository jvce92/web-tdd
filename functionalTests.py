from selenium import webdriver
import unittest

class newVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def testPageTitle(self):

        #Access the to-do list website
        self.browser.get('http://localhost:8000')

        #checks for the website title
        self.assertIn('To-Do',self.browser.title)
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
