from django.shortcuts import render
from .models import Product, Supplier, StockTransaction
from django.db.models import Sum, F
from .forms import SupplierForm, ProductForm, StockTransactionForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import SupplierSerializer, ProductSerializer, StockTransactionSerializer
import csv
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages



@login_required(login_url='login')
def dashboard(request):

    total_products = Product.objects.count()

    total_suppliers = Supplier.objects.count()

    low_stock_products = Product.objects.filter(
        quantity__lte=F('reorder_level')
    ).count()

    total_inventory_value = Product.objects.aggregate(
        total_value=Sum(F('price') * F('quantity'))
    )['total_value'] or 0

    recent_transactions = StockTransaction.objects.all().order_by('-date')[:5]

    context = {
        'total_products': total_products,
        'total_suppliers': total_suppliers,
        'low_stock_products': low_stock_products,
        'total_inventory_value': total_inventory_value,
        'recent_transactions': recent_transactions,
    }

    return render(request, 'inventory/dashboard.html', context)

# Add Supplier
@login_required(login_url='login')
def add_supplier(request):

    if request.method == 'POST':
        form = SupplierForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:
        form = SupplierForm()

    return render(request, 'inventory/add_supplier.html', {'form': form})



# Add Product
@login_required(login_url='login')
def add_product(request):

    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:
        form = ProductForm()

    return render(request, 'inventory/add_product.html', {'form': form})



# Add Stock Transaction
@login_required(login_url='login')
def add_transaction(request):

    if request.method == 'POST':
        form = StockTransactionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:
        form = StockTransactionForm()

    return render(request, 'inventory/add_transaction.html', {'form': form})

def user_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        else:
            return render(request, 'inventory/login.html', {'error': 'Invalid credentials'})

    return render(request, 'inventory/login.html')

def user_logout(request):

    logout(request)

    return redirect('login')

# Supplier API
class SupplierViewSet(viewsets.ModelViewSet):

    queryset = Supplier.objects.all()

    serializer_class = SupplierSerializer



# Product API
class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer



# Stock Transaction API
class StockTransactionViewSet(viewsets.ModelViewSet):

    queryset = StockTransaction.objects.all()

    serializer_class = StockTransactionSerializer

@login_required(login_url='login')
def export_products_csv(request):

    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)

    writer.writerow([
        'ID',
        'Name',
        'Category',
        'Supplier',
        'Quantity',
        'Price',
        'Reorder Level',
        'Created At'
    ])

    products = Product.objects.all()

    for product in products:

        writer.writerow([
            product.id,
            product.name,
            product.category,
            product.supplier.name,
            product.quantity,
            product.price,
            product.reorder_level,
            product.created_at
        ])

    return response

@login_required(login_url='login')
def export_transactions_csv(request):

    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

    writer = csv.writer(response)

    writer.writerow([
        'ID',
        'Product',
        'Transaction Type',
        'Quantity',
        'Date'
    ])

    transactions = StockTransaction.objects.all()

    for transaction in transactions:

        writer.writerow([
            transaction.id,
            transaction.product.name,
            transaction.transaction_type,
            transaction.quantity,
            transaction.date
        ])

    return response

def signup_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # check passwords match
        if password != confirm_password:
            return render(request, "signup.html", {"error": "Passwords do not match"})

        # check username exists
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already exists"})

        # create user
        User.objects.create_user(username=username, password=password)

        return redirect("login")

    return render(request, 'inventory/signup.html')