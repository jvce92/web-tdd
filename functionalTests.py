from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class newVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def checkForRowInTable(self,rowText):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(rowText, [row.text for row in rows])

    def testPageTitle(self):

        #Access the to-do list website
        self.browser.get('http://localhost:8000')

        #checks for the website title
        self.assertIn('To-Do',self.browser.title)
        headerText = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',headerText)
        #user is asked to input its first to-do list
        inputBox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputBox.get_attribute('placeholder'),'Enter a to-do item')
        #test a new list input
        inputBox.send_keys('Buy peacock feathers')
        inputBox.send_keys(Keys.ENTER)
        #check if the new entry is at the to-do list
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        # self.assertTrue(any(row.text == '1: Buy peacock feathers' for row in rows),
        #                 'New to-do item does not appear in the table --its text was: \n %s' % (table.text,))
        #better way to check for the new item
        self.assertIn('1: Buy peacock feathers',[row.text for row in rows])

        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
