from django.shortcuts import render
from .models import Product

# Create your views here.

def all_products(request):
    """A View to show all products and sorting and searching  """

    products = Product.objects.all()
    print(f"Number of products: {products.count()}")

    context = {
        'products': products,
    }
    
    return render(request, 'products/products.html', context)