# Sổ Tử Vi – trang cho khách

Nhánh này chứa trang web "Sổ Tử Vi" để gửi link cho khách. Nhánh `main` (trang HML) không liên quan và không bị sửa.

- `web/`: giao diện trang (`index.html`) cùng dữ liệu đi kèm.
  - `py-bundle.json`: bộ tính Tử vi – Bát tự của nhánh `tuvi-skill`, bản `492a69d`, cộng thư viện lunar-python 1.4.8 (giấy phép MIT, xem `LICENSE-lunar-python.txt`).
  - `docs.json`: hướng dẫn luận.
  - Bộ tính chạy ngay trên máy khách bằng Pyodide.
- `apps-script/`: mã dán vào Google Apps Script, gắn với Google Sheet "Sổ Tử Vi – Khách".
  - `Code.gs`: ghi thông tin khách và các lần xem vào Sheet; phần luận gọi API Claude nếu có khóa.
  - `Index.html`: trang khung. Thay `__BASE__` bằng `https://cdn.jsdelivr.net/gh/tranphuminh916/hml-gia@<commit>/web/`.
- `tools/`: script dựng lại `py-bundle.json`.

Kho này công khai, không chứa dữ liệu khách. Dữ liệu khách chỉ nằm trong Google Sheet của chủ trang.
