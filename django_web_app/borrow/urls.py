from django.urls import path
from . import views

urlpatterns = [
    path('borrow/create/', views.borrow_slip_create, name='borrow_slip_create'),
    path('borrow/<int:slip_id>/edit/', views.borrow_slip_edit, name='borrow_slip_edit'),
    path('borrow/<int:slip_id>/add-book/', views.borrowed_book_add, name='borrowed_book_add'),
    path('borrow-slips/', views.borrow_slip_list, name='borrow_slip_list'),
    path('borrow/<int:slip_id>/update/', views.borrow_slip_update_full, name='borrow_slip_update_full'),
    path('borrow-slips/<int:slip_id>/delete/', views.borrow_slip_delete, name='borrow_slip_delete'),
    path('borrow-slips/search/', views.search_slip, name='search_slip'),
]
