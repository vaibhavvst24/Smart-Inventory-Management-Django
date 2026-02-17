from django.db import models


# Supplier Model
class Supplier(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(max_length=15)

    address = models.TextField()

    def __str__(self):
        return self.name



# Product Model
class Product(models.Model):

    CATEGORY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Clothing', 'Clothing'),
        ('Food', 'Food'),
        ('Stationery', 'Stationery'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=200)

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    quantity = models.IntegerField()

    price = models.FloatField()

    reorder_level = models.IntegerField(default=10)

    created_at = models.DateTimeField(auto_now_add=True)

    def is_low_stock(self):
        return self.quantity <= self.reorder_level

    def __str__(self):
        return self.name



# Stock Transaction Model
class StockTransaction(models.Model):

    TRANSACTION_TYPE = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out')
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)

    quantity = models.IntegerField()

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.transaction_type}"
