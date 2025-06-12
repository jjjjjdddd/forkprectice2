from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Menu
from .forms import MenuForm

def menu_list(request):
    menus = Menu.objects.all()
    return render(request, 'menu/menu_list.html', {'menus': menus})

@login_required
def menu_create(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuForm()
    return render(request, 'menu/menu_form.html', {'form': form})

@login_required
def menu_update(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES, instance=menu)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuForm(instance=menu)
    return render(request, 'menu/menu_form.html', {'form': form})

@login_required
def menu_delete(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == 'POST':
        menu.delete()
        return redirect('menu_list')
    return render(request, 'menu/menu_confirm_delete.html', {'menu': menu})

@login_required
def update_sold_servings(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == 'POST':
        sold_servings = int(request.POST.get('sold_servings', 0))
        if sold_servings <= menu.total_servings:
            menu.sold_servings = sold_servings
            menu.save()
    return redirect('menu_list')

@login_required
def purchase_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == 'POST':
        if menu.remaining_servings > 0:
            menu.sold_servings += 1
            menu.save()
            messages.success(request, f'{menu.name} 구매가 완료되었습니다.')
        else:
            messages.error(request, '죄송합니다. 재고가 부족합니다.')
    return redirect('menu_list')
