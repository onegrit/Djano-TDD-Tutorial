from django.http import HttpResponse
from django.shortcuts import render, redirect

from lists.models import Item, List


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


def view_list(request, list_id):
    a_list = List.objects.get(id=list_id)
    items = Item.objects.filter(list=a_list)
    return render(request, 'list.html', {'list': a_list})


def new_list(request):
    a_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=a_list)
    return redirect(f'/lists/{a_list.id}/')


def add_item(request, list_id):
    a_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=a_list)

    return redirect(f'/lists/{list_id}/')
