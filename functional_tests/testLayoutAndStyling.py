from .base import FunctionalTests

class LayoutAndStyling(FunctionalTests):
    def testLayouAndStyling(self):
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024,768)

        inputBox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputBox.location['x'] + inputBox.size['width']/2, 512, delta=5)
