from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category

import logging
logger = logging.getLogger(__name__)

def all_products(request):
    print("--- Starting all_products view ---")
    all_categories = Category.objects.all()
    print(f"All categories in database: {[cat.name for cat in all_categories]}")

    """A View to show all products and sorting and searching"""

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None
    
    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            # Strip whitespace from each category
            categories = [c.strip() for c in categories]
            print(f"Categories from URL: {categories}")  # New print statement
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
            print(f"Filtered categories: {[cat.name for cat in categories]}")

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }
    
    print(f"Number of products being sent to template: {products.count()}")
    print(f"Categories being sent to template: {[cat.name for cat in categories] if categories else 'All'}")
    print("--- Ending all_products view ---")

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    """A View to show product detail"""

    product = get_object_or_404(Product, pk=product_id)
    
    context = {
        'product': product,
    }
    
    return render(request, 'products/product_detail.html', context)