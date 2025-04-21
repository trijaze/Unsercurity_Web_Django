from django.shortcuts import render, redirect, get_object_or_404
from .models import BorrowSlip, BorrowedBook
from .forms import BorrowSlipForm, BorrowedBookForm, BorrowSlipFullForm, BorrowedBookFormSet
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import inlineformset_factory
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.db import connection
from django.http import HttpResponse
from borrow.models import BorrowSlip





# Hàm kiểm tra vai trò được phép
def is_student_or_staff(user):
    return hasattr(user, 'role') and user.role.name in ['Student', 'Staff', 'Teacher', 'Librarian']

def is_librarian(user):
    return hasattr(user, 'role') and user.role.name == 'Librarian'

def search_slip(request):
    q = request.GET.get('q_slip', '')

    with connection.cursor() as cursor:
        try:
            cursor.execute(f"SELECT * FROM borrow_borrowslip WHERE id = {q}")
            rows = cursor.fetchall()
        except Exception as e:
            rows = []
            print("SQL Error:", e)

    return render(request, 'borrow/slip_list.html', {'slips': rows})

@user_passes_test(is_librarian)
def borrow_slip_delete(request, slip_id):
    slip = get_object_or_404(BorrowSlip, id=slip_id)
    slip.delete()
    return redirect('borrow_slip_list')

# Danh sách phiếu mượn của người dùng
@user_passes_test(is_student_or_staff)
def borrow_slip_list(request):
    slips = BorrowSlip.objects.filter(user=request.user)
    if request.user.role.name == 'Librarian':
        slips = BorrowSlip.objects.all()
    else:
        slips = BorrowSlip.objects.filter(user=request.user)

    return render(request, 'borrow/slip_list.html', {'slips': slips})

# Tạo mới phiếu mượn
@user_passes_test(is_student_or_staff)
def borrow_slip_create(request):
    now = timezone.now()
    slip = BorrowSlip.objects.create(
        user=request.user,
        created_at=now,
        due_date=now + timedelta(days=30)
    )
    return redirect('borrow_slip_edit', slip_id=slip.id)

# Chỉnh sửa phiếu mượn
@user_passes_test(is_student_or_staff)
def borrow_slip_edit(request, slip_id):
    slip = get_object_or_404(BorrowSlip, id=slip_id, user=request.user)

    if slip.submitted:
        return redirect('borrow_slip_list')

    books = slip.borrowed_books.all()
    if request.method == 'POST':
        if 'submit' in request.POST:
            slip.submitted = True
            slip.save()
            return redirect('borrow_slip_list')
    return render(request, 'borrow/slip_edit.html', {'slip': slip, 'books': books})

# Thêm sách vào phiếu
@user_passes_test(is_student_or_staff)
def borrowed_book_add(request, slip_id):
    slip = get_object_or_404(BorrowSlip, id=slip_id, user=request.user)

    if slip.submitted:
        return redirect('borrow_slip_edit', slip_id=slip.id)

    if request.method == 'POST':
        form = BorrowedBookForm(request.POST)
        if form.is_valid():
            borrowed_book = form.save(commit=False)
            borrowed_book.slip = slip
            borrowed_book.save()
            return redirect('borrow_slip_edit', slip_id=slip.id)
    else:
        form = BorrowedBookForm()
        return render(request, 'borrow/book_form.html', {'form': form, 'slip_id': slip.id})
    

@user_passes_test(is_student_or_staff)
def borrow_slip_update_full(request, slip_id):
    slip = get_object_or_404(BorrowSlip, id=slip_id)

    is_editable = hasattr(request.user, 'role') and request.user.role.name in ['Staff', 'Teacher', 'Librarian']

    BorrowedBookFormSet = inlineformset_factory(
        BorrowSlip, BorrowedBook, form=BorrowedBookForm, extra=0, can_delete=is_editable
    )
    if request.method == 'POST' and is_editable:
        form = BorrowSlipForm(request.POST, instance=slip)
        formset = BorrowedBookFormSet(request.POST, instance=slip)
        if form.is_valid() and formset.is_valid():
            #form.save()
            #formset.save()        
            slip = form.save(commit=True)

            if 'submit' in request.POST:
                slip.submitted = True

            slip.save()
            formset.save()
            return redirect('borrow_slip_list')
        else:
            print(form.errors)
            print(formset.errors)
    else:
        form = BorrowSlipForm(instance=slip)
        formset = BorrowedBookFormSet(instance=slip)

    return render(request, 'borrow/slip_update_full.html', {
        'slip': slip,
        'form': form,
        'formset': formset,
        'is_editable': is_editable
    })

