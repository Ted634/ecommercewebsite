from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Product, Cart, CartItem, Order, OrderItem
from .forms import CustomUserCreationForm

# Register your models here.


# 管理 CustomUser資料表
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm  # 表單資料
    model = CustomUser                 # 資料表
    list_display = ('username', 'is_consumer', 'is_seller',
                    'is_approved', 'is_staff')   # 顯示列表
    list_filter = ('is_consumer', 'is_seller', 'is_approved')  # 過濾器列表

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_staff',
         'is_active', 'is_approved', 'is_consumer', 'is_seller')}),
    )  # is_active 才是管理員審核的項目，is_approved 只是顯示是否被認可
    add_fieldsets = (
        (None, {
            'classes': ('wide',), 'fields': ('username', 'password1', 'password2', 'is_consumer', 'is_seller', 'is_approved')}
         ),
    )
    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Product)


class CartItemInline(admin.TabularInline):
    model = CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

# admin.site.register(Product): 註冊 Product 模型，以便在 Django 管理後台中管理商品。

# CartItemInline 類別: 創建一個內聯類別，用於在 Cart 管理頁面中直接編輯 CartItem。

# CartAdmin 類別: 註冊 Cart 模型，並指定 CartItemInline 作為內聯，這樣在 Cart 管理頁面中就可以直接編輯 CartItem。

# OrderItemInline 類別: 創建一個內聯類別，用於在 Order 管理頁面中直接編輯 OrderItem。

# OrderAdmin 類別: 註冊 Order 模型，並指定 OrderItemInline 作為內聯，這樣在 Order 管理頁面中就可以直接編輯 OrderItem。
