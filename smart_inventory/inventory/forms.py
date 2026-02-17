from django import forms
from .models import Supplier, Product, StockTransaction


class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = ['name', 'email', 'phone', 'address']


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'category', 'supplier', 'quantity', 'price', 'reorder_level']


class StockTransactionForm(forms.ModelForm):

    class Meta:
        model = StockTransaction
        fields = ['product', 'transaction_type', 'quantity']
