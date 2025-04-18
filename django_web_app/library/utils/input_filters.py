import re
import html
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError

def validate_username(username):
    if not re.match(r'^[\w.@+-]+$', username):
        raise ValidationError("Tên người dùng không hợp lệ.")

def validate_no_script_tag(text):
    if '<script' in text.lower():
        raise ValidationError("Không được chứa mã script.")
    return strip_tags(text)

def validate_query_param(query):
    if re.search(r'[<>"]', query):
        raise ValidationError("Chuỗi tìm kiếm không hợp lệ.")
    return query

def sanitize_search_input(query):
    return re.sub(r"[^a-zA-Z0-9\s]", "", query)

def sanitize_html_input(raw):
    return html.escape(raw)

def is_safe_filename(filename):
    return not (".." in filename or filename.startswith("/"))

def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

def is_valid_string(s, max_len=100):
    return isinstance(s, str) and 0 < len(s.strip()) <= max_len
