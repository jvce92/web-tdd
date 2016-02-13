from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys

class newVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return #
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

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
        self.browser.get(self.server_url)

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
        userListUrl = self.browser.current_url
        self.assertRegex(userListUrl, '/lists/.+')
        self.checkForRowInTable('1: Buy peacock feathers')

        inputBox = self.browser.find_element_by_id('id_new_item')
        inputBox.send_keys('Use peacock feathers to make a fly')
        inputBox.send_keys(Keys.ENTER)
        self.checkForRowInTable('2: Use peacock feathers to make a fly')
        #a new user shows up
        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.server_url)

        inputBox = self.browser.find_element_by_id('id_new_item')
        inputBox.send_keys('Buy milk')
        inputBox.send_keys(Keys.ENTER)
        #check if this is actually the new user's page
        newUserListUrl = self.browser.current_url
        self.assertRegex(newUserListUrl,'/lists/.+')
        self.assertNotEqual(userListUrl,newUserListUrl)
        #check for new user input (and that old user input is not present)
        pageText = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',pageText)
        self.assertIn('Buy milk', pageText)

    def testLayouAndStyling(self):
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024,768)

        inputBox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputBox.location['x'] + inputBox.size['width']/2, 512, delta=5)
