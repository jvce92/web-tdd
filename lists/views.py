from django.shortcuts import render,redirect
from django.http import HttpResponse
from lists.models import Item,List

# Create your views here.

def homePage(request):
    return render(request, 'home.html')

def viewList(request,listID):
    myList = List.objects.get(id=listID)
    items = Item.objects.filter(list = myList)
    return  render(request, 'list.html', {'list': myList, } )

def newList(request):
    myList = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list = myList)
    return redirect('/lists/%d/' % (myList.id, ))

def addItem(request,listID):
    myList = List.objects.get(id=listID)
    Item.objects.create(text=request.POST['item_text'], list = myList)
    return redirect('/lists/%d/' % (myList.id, ))
