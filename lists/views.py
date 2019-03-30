from django.http import HttpResponse
from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):
    # 处理完POST请求后一定要重定向
    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
        return redirect('/')
    else:
        new_item_text = ''
    # item = Item()
    # item.text = request.POST.get('item_text', '')
    # item.save()
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})
