from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Category
from .forms import BookForm, CategoryForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from .models import Book
from django.db.models import Q
from .utils import validate_query_param, ValidationError
from django.contrib import messages

# Chỉ cho role = 'Thủ thư' được truy cập
def is_librarian(user):
    return hasattr(user, 'role') and user.role.name == 'Librarian'

def search_book(request):
    query = request.GET.get('q_book')

    try:
        query = validate_query_param(query)
    except ValidationError as e:
        messages.error(request, str(e))
        return redirect('book_list.html')  

    result = Book.objects.filter(
        Q(code__icontains=query) | Q(title__icontains=query) | Q(author__icontains=query) | Q(year__icontains=query) | Q(publisher__icontains=query) | Q(category__name__icontains=query) | Q(description__icontains=query) | Q(quantity__icontains=query) | Q(price__icontains=query)
    )
    context = {
        'books': result,
        'query': query,
    }
    
    return render(request, 'books/book_list.html', context)


def search_category(request):
    query = request.GET.get('q_category')
    result = Category.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
    context = {
        'categories': result,
        'query': query,
    }
    
    return render(request, 'books/category_list.html', context)

#@user_passes_test(is_librarian)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

#@user_passes_test(is_librarian)
def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})

#@user_passes_test(is_librarian)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})

#@user_passes_test(is_librarian)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('book_list')

#@user_passes_test(is_librarian)
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'books/category_form.html', {'form': form})


#@user_passes_test(is_librarian)
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'books/category_form.html', {'form': form})

@user_passes_test(is_librarian)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'books/category_list.html', {'categories': categories})

@user_passes_test(is_librarian)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('category_list')
