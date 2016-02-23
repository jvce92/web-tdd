from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError

# Create your tests here.
#
# class smokeTest(TestCase):
#
#     def testBadMath(self):
#         self.assertEqual(1+1,3)

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

    def testCannotSaveEmptyListItem(self):
        myList = List.objects.create()
        item = Item(list=myList, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

        
