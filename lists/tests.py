from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import homePage
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item


# Create your tests here.
#
# class smokeTest(TestCase):
#
#     def testBadMath(self):
#         self.assertEqual(1+1,3)

class homePageTest(TestCase):

    def testRootUrlResolvesToHomePage(self):
        found = resolve('/')
        self.assertEqual(found.func,homePage)

    def testHomePageReturnsHtml(self):
        request = HttpRequest()
        response = homePage(request)
        expectedHtml = render_to_string('home.html')
        self.assertEqual(expectedHtml,response.content.decode())
        # self.assertTrue(response.content.startswith(b'<html>'))
        # self.assertIn(b'<title>To-Do lists</title>',response.content)
        # self.assertTrue(response.content.strip().endswith(b'</html>'))

    def testHandlePostRequest(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        response = homePage(request)
        self.assertIn('A new list item', response.content.decode())
        expectedHtml = render_to_string('home.html', {'new_item_text':'A new list item'})
        self.assertEqual(response.content.decode(),expectedHtml)

class ItemModelTest(TestCase):

    def testSavingAndRetrievingItems(self):
        firstItem = Item()
        firstItem.text = 'The first list item'
        firstItem.save()

        secondItem = Item()
        secondItem.text = 'The second list item'
        secondItem.save()

        savedItems = Item.objects.all()
        self.assertEqual(savedItems.count(),2)

        firstSavedItem = savedItems[0]
        secondSavedItem = savedItems[1]
        self.assertEqual(firstSavedItem.text,'The first list item')
        self.assertEqual(secondSavedItem.text,'The second list item')
