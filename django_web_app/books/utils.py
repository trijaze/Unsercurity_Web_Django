import re
from django.core.exceptions import ValidationError

def validate_query_param(query):
    if not query:
        return query
    if re.search(r'[<>{}[\]"\'/]', query):
        raise ValidationError("Từ khóa tìm kiếm chứa ký tự không hợp lệ.")
    return query
