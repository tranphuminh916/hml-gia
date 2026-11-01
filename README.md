# Sổ Tử Vi – trang cho khách

Nhánh này chứa trang web "Sổ Tử Vi" để gửi link cho khách. Nhánh `main` (trang HML) không liên quan và không bị sửa.

- `web/`: giao diện trang (`index.html`) cùng dữ liệu đi kèm.
  - `py-bundle.json`: bộ tính Tử vi – Bát tự của nhánh `tuvi-skill`, bản `492a69d`, thêm `giosinh.py` (dò giờ sinh), cộng thư viện lunar-python 1.4.8 (giấy phép MIT, xem `LICENSE-lunar-python.txt`).
  - `docs.json`: hướng dẫn luận.
  - Bộ tính chạy ngay trên máy khách bằng Pyodide.
- `apps-script/`: mã dán vào Google Apps Script, gắn với Google Sheet "Sổ Tử Vi – Khách".
  - `Code.gs`: ghi thông tin khách và các lần xem vào Sheet; phần luận gọi API Claude nếu có khóa.
  - `Index.html`: trang khung. Thay `__BASE__` bằng `https://cdn.jsdelivr.net/gh/tranphuminh916/hml-gia@<commit>/web/`.
- `tools/`: script dựng lại `py-bundle.json`; `giosinh.py` là công cụ dò giờ sinh (đặt cùng thư mục với `tvbt.py` khi chạy).

## Dò giờ sinh

Bấm "Tìm giờ sinh" trên thẻ thông tin. Có 7 câu hỏi, câu nào không rõ thì bỏ qua:
1. Giờ gia đình còn nhớ.
2. Xoáy tóc.
3. Dáng ngủ.
4. Khuôn mặt.
5. Điều chiếm tâm sức nhiều nhất từ 30 tuổi (cung an Thân).
6. Tính cách giống mô tả nào (sao chính cung Mệnh).
7. Năm đời rẽ hướng (đại hạn).

Bộ tính lập sẵn lá số cho mọi giờ trong ngày sinh. Mỗi câu trả lời nhân thêm một hệ số, nên không giờ nào bị loại hẳn. Kết quả là ước đoán để tham khảo.

Kho này công khai, không chứa dữ liệu khách. Dữ liệu khách chỉ nằm trong Google Sheet của chủ trang.
