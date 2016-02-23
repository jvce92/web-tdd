from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import homePage
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List
from django.utils.html import escape

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

    # def testHomePageReturnsHtml(self):
    #     request = HttpRequest()
    #     response = homePage(request)
    #     expectedHtml = render_to_string('home.html')
    #     self.assertEqual(expectedHtml,response.content.decode())

class ListViewTest(TestCase):

    def testUsesListTemplate(self):
        myList = List.objects.create()
        response = self.client.get('/lists/%d/' % (myList.id,))
        self.assertTemplateUsed(response, 'list.html')

    def testDisplaysOnlyItemsForThatList(self):
        correctList = List.objects.create()
        Item.objects.create(text='item1', list = correctList)
        Item.objects.create(text='item2', list = correctList)

        wrongList = List.objects.create()
        Item.objects.create(text='otherItem1', list = wrongList)
        Item.objects.create(text='otherItem2', list = wrongList)

        response = self.client.get('/lists/%d/' % (correctList.id, ))

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')
        self.assertNotContains(response, 'otherItem1')
        self.assertNotContains(response, 'otherItem2')


    def testDisplayAllItems(self):
        myList = List.objects.create()
        Item.objects.create(text='item1', list = myList)
        Item.objects.create(text='item2', list = myList)

        response = self.client.get('/lists/%d/' % (myList.id, ))

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')

    def testUseDifferentTemplates(self):
        myList = List.objects.create()
        response = self.client.get('/lists/%d/' % (myList.id, ))
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
        newList = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (newList.id, ))

    def testCanSavePostToAnExistingList(self):
        wrongList = List.objects.create()
        correctList = List.objects.create()

        self.client.post(
        '/lists/%d/' % (correctList.id,), data = {'item_text':'New item for existing list'}
        )

        self.assertEqual(Item.objects.count(),1)
        newItem = Item.objects.first()
        self.assertEqual(newItem.text,'New item for existing list')
        self.assertEqual(newItem.list,correctList)

    def testRedirectsToListView(self):
        wrongList = List.objects.create()
        correctList = List.objects.create()

        response = self.client.post(
        '/lists/%d/' % (correctList.id,), data = {'item_text':'New item for existing list'}
        )

        self.assertRedirects(response,'/lists/%d/' % (correctList.id, ))

    def testPassesCorrectListToTemplate(self):
        wrongList = List.objects.create()
        correctList = List.objects.create()

        response = self.client.get(
        '/lists/%d/' % (correctList.id, ),
        )

        self.assertEqual(response.context['list'],correctList)

    def testValidationErrorsAreSentToHomePageTemplate(self):
        response = self.client.post('/lists/new', data={'item_text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expectedError = escape("You can't have an empty list item")
        self.assertContains(response, expectedError)

    def testEmptyItemsAreNotSaved(self):
        response = self.client.post('/lists/new', data={'item_text':''})
        self.assertEqual(List.objects.count(),0)
        self.assertEqual(Item.objects.count(),0)
