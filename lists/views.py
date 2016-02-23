from django.shortcuts import render,redirect
from django.http import HttpResponse
from lists.models import Item,List
from django.core.exceptions import ValidationError

# Create your views here.

def homePage(request):
    return render(request, 'home.html')

def viewList(request,listID):
    myList = List.objects.get(id=listID)
    items = Item.objects.filter(list = myList)
    return  render(request, 'list.html', {'list': myList, } )

def newList(request):
    myList = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list = myList)
    try:
        item.full_clean()
    except ValidationError:
        myList.delete()
        error = "You can't have an empty list item!"
        return render(request, 'home.html', {'error': error,})

    return redirect('/lists/%d/' % (myList.id, ))

def addItem(request,listID):
    myList = List.objects.get(id=listID)
    Item.objects.create(text=request.POST['item_text'], list = myList)
    return redirect('/lists/%d/' % (myList.id, ))
