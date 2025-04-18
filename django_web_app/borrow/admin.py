from django.contrib import admin
from .models import BorrowSlip, BorrowedBook
from django import forms

admin.site.register(BorrowSlip)
admin.site.register(BorrowedBook)
