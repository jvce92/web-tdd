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

        self.assertEqual(Item.objects.count(),1)
        newItem = Item.objects.first()
        self.assertEqual(newItem.text,'A new list item')

    def testRedirectsAfterPost(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = homePage(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def testHomePageOnlySavesItemWhenNecessary(self):
        request = HttpRequest()
        homePage(request)
        self.assertEqual(Item.objects.count(),0)

    def testDisplayAllListElements(self):
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')

        request = HttpRequest()
        response = homePage(request)

        self.assertIn('item 1', response.content.decode())
        self.assertIn('item 2', response.content.decode())

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
