from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Menu
from .forms import MenuForm

def menu_list(request):
    menus = Menu.objects.all()
    return render(request, 'menu/menu_list.html', {'menus': menus})

@login_required(login_url='/admin/login/')
def menu_create(request):
    if not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '메뉴가 성공적으로 추가되었습니다.')
            return redirect('menu_list')
    else:
        form = MenuForm()
    return render(request, 'menu/menu_form.html', {'form': form})

@login_required(login_url='/admin/login/')
def menu_update(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES, instance=menu)
        if form.is_valid():
            form.save()
            messages.success(request, '메뉴가 성공적으로 수정되었습니다.')
            return redirect('menu_list')
    else:
        form = MenuForm(instance=menu)
    return render(request, 'menu/menu_form.html', {'form': form})

@login_required(login_url='/admin/login/')
def menu_delete(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == 'POST':
        menu.delete()
        messages.success(request, '메뉴가 성공적으로 삭제되었습니다.')
        return redirect('menu_list')
    return render(request, 'menu/menu_confirm_delete.html', {'menu': menu})

@login_required(login_url='/admin/login/')
def update_sold_servings(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == 'POST':
        try:
            sold_servings = int(request.POST.get('sold_servings', 0))
            if sold_servings <= menu.total_servings:
                menu.sold_servings = sold_servings
                menu.save()
                messages.success(request, '판매 수량이 업데이트되었습니다.')
            else:
                messages.error(request, '판매 수량이 총 수량을 초과할 수 없습니다.')
        except ValueError:
            messages.error(request, '올바른 숫자를 입력해주세요.')
    return redirect('menu_list')

@login_required(login_url='/admin/login/')
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
