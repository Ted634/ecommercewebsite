from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# 使用者帳號資料表
class CustomUser(AbstractUser):
    # 讓管理員確認使用者是否為有效帳號 也可以將 default設成 True，預設為有效帳號
    is_approved = models.BooleanField(default=True)
    is_consumer = models.BooleanField(default=False)   # 使用者的身分權限
    is_seller = models.BooleanField(default=False)   # 使用者的身分權限


# 產品資料表
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


# 購物車資料表(結帳統整顯示用)
class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')


# 購物車物品資料表(物品增加減少都在此資料表)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
