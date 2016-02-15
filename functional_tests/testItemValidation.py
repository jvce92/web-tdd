from .base import FunctionalTests
from unittest import skip

class ItemValidationTest(FunctionalTests):

    def testCannotAddEmptyLists(self):
        #tries to input an empty entry to the List
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        #The page refereshes and returns an error to the user
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text,"You can't have an empty list item!")
        #The user tries a new entry that should work
        self.browser.find_element_by_id('id_new_item').send_keys('Buy hats\n')
        self.checkForRowInTable('1: Buy hats')
        #the user again tries to input a blank item
        self.browser.find_element_by_id('id_new_item').send_keys('\n')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text,"You can't have an empty list item!")
        #after the error, the user can keep on filling the list with valid entries
        self.browser.find_element_by_id('id_new_item').send_keys('Buy a purse')
        self.checkForRowInTable('2: Buy a purse')
