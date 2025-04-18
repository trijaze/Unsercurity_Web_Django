from django import forms
from .models import BorrowSlip, BorrowedBook
from django.forms import inlineformset_factory

BorrowedBookFormSet = inlineformset_factory(
    BorrowSlip,
    BorrowedBook,
    fields=['book', 'quantity'],
    extra=1,
    can_delete=True
)

class BorrowedBookForm(forms.ModelForm):
    class Meta:
        model = BorrowedBook
        fields = ['book', 'quantity']

class BorrowSlipForm(forms.ModelForm):
    class Meta:
        model = BorrowSlip
        fields = ['due_date', 'is_borrowed']
        widgets = {
            'borrow_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'is_borrowed': forms.CheckboxInput(),
            # thêm widget khác nếu cần
        }

class BorrowSlipFullForm(forms.ModelForm):
    class Meta:
        model = BorrowSlip
        fields = '__all__'  # hoặc chọn các field cụ thể nếu cần
        widgets = {
            'borrow_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),

        }