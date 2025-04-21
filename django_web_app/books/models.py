from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name    

class Book(models.Model):
    code = models.CharField(max_length=20, unique=True)  # Mã số sách
    title = models.CharField(max_length=200)             # Tên sách
    author = models.CharField(max_length=100)            # Tác giả
    year = models.PositiveIntegerField()                 # Năm xuất bản
    publisher = models.CharField(max_length=100)         # Nhà xuất bản
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)           # Mô tả
    quantity = models.PositiveIntegerField()             # Số lượng
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Đơn giá

    def __str__(self):
        return f"{self.title} - {self.author}"
