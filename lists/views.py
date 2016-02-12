from django.shortcuts import render,redirect
from django.http import HttpResponse
from lists.models import Item,List

# Create your views here.

def homePage(request):
    return render(request, 'home.html')

def viewList(request):
    items = Item.objects.all()
    return  render(request, 'list.html', {'items':items, } )

def newList(request):
    myList = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list = myList)
    return redirect('/lists/the-only-list-in-the-world/')
