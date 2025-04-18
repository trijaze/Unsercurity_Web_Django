# models.py
from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from django.conf import settings
from django.utils import timezone



class BorrowSlip(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE,
        related_name='borrow_slips'  
    )
    created_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True)
    submitted = models.BooleanField(default=False)
    is_borrowed = models.BooleanField(default=False)

    def __str__(self):
        return f'Phiếu mượn #{self.id} - {self.user.username}'

class BorrowedBook(models.Model):
    slip = models.ForeignKey(BorrowSlip, related_name='borrowed_books', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.book.title} (x{self.quantity})'
