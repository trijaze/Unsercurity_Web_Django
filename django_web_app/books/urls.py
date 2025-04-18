from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.book_add, name='add_book'),
    path('books/edit/<int:pk>/', views.book_edit, name='edit_book'),  # 👈 fix lỗi tại đây
    path('books/delete/<int:pk>/', views.book_delete, name='delete_book'),
    path('books/search/',views.search_book,name='search_book' ),

    # CATEGORIES
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),
    path('categories/search/',views.search_category,name='search_category' ),
]
