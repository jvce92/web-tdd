from django.shortcuts import render,redirect
from django.http import HttpResponse
from lists.models import Item,List
from django.core.exceptions import ValidationError

# Create your views here.

def homePage(request):
    return render(request, 'home.html')

def viewList(request,listID):
    myList = List.objects.get(id=listID)
    #items = Item.objects.filter(list = myList)
    error = None
    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list = myList)
            item.full_clean()
            item.save()
            return redirect('/lists/%d/' % (myList.id, ))
        except ValidationError:
            error = "You can't have an empty list item!"
    return  render(request, 'list.html', {'list': myList, 'error': error,} )

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
