from django.contrib.auth.decorators import user_passes_test

def is_librarian(user):
    return hasattr(user, 'role') and user.role.name == 'Librarian'

librarian_required = user_passes_test(is_librarian)
