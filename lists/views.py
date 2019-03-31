from django.http import HttpResponse
from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):
    # 处理完POST请求后一定要重定向
    # if request.method == 'POST':
    #     # new_item_text = request.POST['item_text']
    #     Item.objects.create(text=request.POST['item_text'])
    #     return redirect('/lists/the-only-list-in-the-world/')
    # else:
    #     new_item_text = ''
    # item = Item()
    # item.text = request.POST.get('item_text', '')
    # item.save()
    return render(request, 'home.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})


def new_list(request):
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/the-only-list-in-the-world/')
