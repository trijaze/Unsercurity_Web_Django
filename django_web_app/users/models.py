from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from PIL import Image

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)  # Đảm bảo user được active mặc định
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True or extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_staff=True and is_superuser=True")
        return self.create_user(username, email, password, **extra_fields)

class Role(models.Model):
    name = models.CharField(max_length=50)  # Admin, Librarian, Student
    permissions = models.IntegerField(default=0)  # bitmask nếu dùng
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.username
    
    def assign_role(self, role_name):
        role, created = Group.objects.get_or_create(name=role_name)
        self.groups.add(role)
        self.save()

    def is_admin(self):
        return self.role and self.role.name == 'Admin'

    def is_librarian(self):
        return self.role and self.role.name == 'Librarian'

    def is_student(self):
        return self.role and self.role.name == 'Student'
    
    def default_role():
        return Role.objects.get_or_create(name='Normal')[0]
    
    """ Mô hình người dùng tùy chỉnh """
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)  # Cho phép trống
    objects = CustomUserManager()  # Sử dụng CustomUserManager
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, default=default_role)

class Profile(models.Model):
    """ Hồ sơ người dùng """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """ Giới hạn kích thước ảnh profile """
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


