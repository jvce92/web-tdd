from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import homePage
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List


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

class ListAndItemModelsTest(TestCase):

    def testSavingAndRetrievingItems(self):
        myList = List()
        myList.save()

        firstItem = Item()
        firstItem.text = 'The first list item'
        firstItem.list = myList
        firstItem.save()

        secondItem = Item()
        secondItem.text = 'The second list item'
        secondItem.list = myList
        secondItem.save()

        savedItems = Item.objects.all()
        self.assertEqual(savedItems.count(),2)

        savedLists = List.objects.first()
        self.assertEqual(savedLists, myList)

        firstSavedItem = savedItems[0]
        secondSavedItem = savedItems[1]
        self.assertEqual(firstSavedItem.text,'The first list item')
        self.assertEqual(secondSavedItem.text,'The second list item')
        self.assertEqual(firstSavedItem.list, myList)
        self.assertEqual(secondSavedItem.list, myList)

class ListViewTest(TestCase):

    def testDisplayAllItems(self):
        myList = List.objects.create()
        Item.objects.create(text='item1', list = myList)
        Item.objects.create(text='item2', list = myList)

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')

    def testUseDifferentTemplates(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response,'list.html')

class NewListTest(TestCase):

    def testHandlePostRequest(self):
        self.client.post(
        '/lists/new', data = {'item_text':'New item', }
        )

        self.assertEqual(Item.objects.count(),1)
        newItem = Item.objects.first()
        self.assertEqual(newItem.text,'New item')

    def testRedirectsAfterPost(self):
        response = self.client.post(
        '/lists/new', data = {'item_text': 'New item', }
        )
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
