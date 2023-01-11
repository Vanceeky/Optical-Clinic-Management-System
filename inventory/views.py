from django.shortcuts import render, redirect
from django.contrib import messages

from .models import *
from .forms import *

def error_404_view(request, exception):
    return render(request, 'layouts/404.html')

    

def index(request):
    categories = Category.objects.all().order_by('name')
    products = Product.objects.all()
    

    category_count = categories.count()
    products_count = products.count()

    context = {
        'categories': categories,
        'category_count': category_count,
        
        'products': products,
        'products_count': products_count,
    }
    return render(request, 'inventory/inventory_dashboard.html', context)

def collectionView(request, slug):
    if(Category.objects.filter(id = slug)):
        products = Product.objects.filter(category = slug)
        category = Category.objects.filter(id = slug).first()
        context = {
            'products': products,
            'category': category
            
        }
    else:
        messages.warning(request, 'No such category found!')
        return redirect('inventory')

    return render(request, 'inventory/collection_products.html', context)

def view_product(request, pk):
    product = Product.objects.get(id = pk)


    context = {
        'product': product,

    }

    return render(request, 'inventory/product.html', context)

    
def add_category(request):
    

    
    name = request.POST.get('name')
    description = request.POST.get('description')
    image = request.FILES['image']

    category = Category.objects.create(
        name = name,
        description = description,
        image = image,
    )

    category.save()

    messages.success(request, ' New category added! ')

    return redirect('inventory')

def add_product(request):

    if request.method == 'POST':    
        category = request.POST.get('category')
        code = request.POST.get('code')
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES['p_image']

        category = Category.objects.get(id = category)

        product = Product.objects.create(
            category = category,
            code = code,
            name = name,
            description = description,
            price = price,
            stock = stock,
            image = image,

        )

        product.save()

        messages.success(request, 'New Product added ! ')

        return redirect('inventory')

def update_product(request, pk):

    product = Product.objects.get(id = pk)
    
    if request.method == "POST":
        code = request.POST.get('code')
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        product.code = code
        product.name = name
        product.description = description
        product.price = price
        product.stock = stock

        product.save()

        messages.success(request, 'Product is updated! ')

        return redirect('inventory')

def delete_product(request, pk):
    product = Product.objects.get(id = pk)
    if request.method == 'POST':
        product.delete()

    messages.success(request, 'Product deleted!')
    return redirect('inventory')

