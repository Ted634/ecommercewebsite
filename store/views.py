from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from .forms import CustomUserCreationForm
from .models import Product, Cart, CartItem, Order, OrderItem    # 載入資料表
# Create your views here.


# 註冊頁面
def register(request):
    if request.method == 'POST':
        # 從 forms.py的 CustomUserCreationForm中取得資料
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():  # 如果 form有執行
            user = form.save(commit=False)
            user.is_active = True  # 使用者註冊後需要管理員審核
            user.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'store/register.html', {'form': form})


# 登入頁面
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_approved:       # 如果帳號被認可
                login(request, user)   # 登入
                if user.is_consumer:    # 如果身分為消費者
                    return redirect('consumer_home')
                elif user.is_seller:  # 如果身分為賣家
                    return redirect('seller_home')
                elif user.is_staff:    # 如果身分為管理員
                    return redirect('/admin/')
            else:
                return render(request, 'store/login.html', {'form': form, 'error': 'Account not approved yet.'})
                # 如果帳號審核尚未通過則會顯示 'Account not approved yet.' 的錯誤訊息(error message)
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})


# 登出
def logout(request):
    auth.logout(request)
    return redirect('product_list')


# 消費者主頁面
@login_required
def consumer_home(request):
    products = Product.objects.all()
    return render(request, 'store/consumer_home.html', {'products': products})


# 賣家主頁面
@login_required
def seller_home(request):
    products = Product.objects.all()
    return render(request, 'store/seller_home.html', {'products': products})


# 產品首頁
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


# 關於我們頁面
def about(request):
    return render(request, 'store/about.html')


# 將產品加入購物車的 function
@login_required(login_url='login')  # 會檢測使用者是否已經登入，若已登入才會執行 add_to_cart() 的程式
def add_to_cart(request, product_id):    # product_id 為 product_list.html 中所回傳的 product.id
    # 從 Product資料表中抓出 id 為 product_id的產品
    product = Product.objects.get(id=product_id)

    # 從 Cart資料表中抓出 user，get_or_create() 會回傳2個參數
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product)  # 從 CartItem資料表中抓出 cart和 product，get_or_create() 會回傳2個參數

    cart_item.quantity += 1   # 每執行一次 add_to_cart() ，購物車裡的此項產品數量就增加 1 個

    cart_item.save()  # 將購物車裡的產品數量儲存

    return redirect('consumer_home')
    # 渲染在同一個頁面中(consumer_home.html)，只是網址會有所變化(通常只能在 terminal中看到)


# 顯示購物車頁面
@login_required(login_url='login')
def view_cart(request):
    cart = Cart.objects.get(user=request.user)
    total_price = sum(item.product.price *
                      item.quantity for item in cart.cartitem_set.all())
    # for item in cart.cartitem_set.all() 透過 for迴圈去 cartitem資料表中抓取資料
    return render(request, 'store/view_cart.html', {'cart': cart, 'total_price': total_price})


# 購物車確認付款頁面
@login_required(login_url='login')
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    total_price = sum(item.product.price *
                      item.quantity for item in cart.cartitem_set.all())
    if request.method == 'POST':  # 如果使用者在 checkout頁面點擊 Confirm Order並送出請求
        # 模擬貨到付款的邏輯，假設訂單已成功支付
        order = Order.objects.create(
            user=request.user, total_price=total_price)  # 從 Cart資料表中抓取資料，並在 Order資料表中新增資料
        # 透過 for迴圈去 cartitem資料表中抓取資料
        for item in cart.cartitem_set.all():
            OrderItem.objects.create(
                order=order, product=item.product, quantity=item.quantity)

        cart.cartitem_set.all().delete()
        # 將 Cart購物車資料表中的資料寫進 Order訂單資料表中後，刪除Cart購物車資料表中的資料

        return redirect('order_success')  # 將使用者重新定向到訂單成功頁面
    # 如果使用者還沒在 checkout頁面點擊 Confirm Order並送出請求時，顯示 Cart資料表中的資料
    return render(request, 'store/checkout.html', {'cart': cart, 'total_price': total_price})


# 訂單成功完成頁面
def order_success(request):
    return render(request, 'store/order_success.html')
