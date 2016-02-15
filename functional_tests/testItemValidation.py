from .base import FunctionalTests
from unittest import skip

class ItemValidationTest(FunctionalTests):

    def testCannotAddEmptyLists(self):
        self.fail('write me')
