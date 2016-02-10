from django.test import TestCase

# Create your tests here.

class smokeTest(TestCase):

    def testBadMath(self):
        self.assertEqual(1+1,3)
