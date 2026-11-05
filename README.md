# Sổ Tử Vi – trang cho khách

Nhánh này chứa trang web "Sổ Tử Vi" để gửi link cho khách. Nhánh `main` (trang HML) không liên quan và không bị sửa.

- `web/`: giao diện trang (`index.html`) cùng dữ liệu đi kèm.
  - `py-bundle.json`: bộ tính Tử vi – Bát tự của nhánh `tuvi-skill`, bản `6fab541` (đã có `giosinh.py` dò giờ sinh; Mệnh chủ theo năm sinh, cân lượng, độ sáng phụ tinh, thêm sao lưu, nguyệt hạn 2 phép), cộng thư viện lunar-python 1.4.8 (giấy phép MIT, xem `LICENSE-lunar-python.txt`).
  - `docs.json`: hướng dẫn luận.
  - Bộ tính chạy ngay trên máy khách bằng Pyodide.
- `apps-script/`: mã dán vào Google Apps Script, gắn với Google Sheet "Sổ Tử Vi – Khách".
  - `Code.gs`: ghi thông tin khách và các lần xem vào Sheet; phần luận gọi API Claude nếu có khóa.
  - `Index.html`: trang khung. Thay `__BASE__` bằng `https://cdn.jsdelivr.net/gh/tranphuminh916/hml-gia@<commit>/web/`.
- `tools/`: script dựng lại `py-bundle.json`; `giosinh.py` là bản sao công cụ dò giờ sinh (bản gốc ở nhánh `tuvi-skill`).

## Xem chỉ tay

Tab "Chỉ tay" ở thanh dưới cùng. Khách chọn người cần xem, tay thuận, rồi chọn ảnh lòng bàn tay trái, tay phải và (không bắt buộc) cạnh bàn tay phía ngón út.

- Ảnh được nén ngay trên máy khách (cạnh dài tối đa 1500 điểm ảnh) rồi gửi kèm yêu cầu luận. Máy chủ chuyển ảnh cho Claude xem; **ảnh không ghi vào Sheet**, Sheet chỉ ghi thông tin đã gửi và bài luận.
- Mỗi lần xem tính 1 lượt xem và 1 lần luận như các mục khác. Cần có khóa API Claude (không có phần luận thì không xem chỉ tay được).
- Cách luận theo skill "xem-chi-tay": kiểm ảnh, ba trường phái Tây – Ấn – Đông, tổng kết chỗ các trường phái cùng nói; không đoán tuổi thọ, không chẩn đoán bệnh.
- Sau khi cập nhật trang này phải dán lại `apps-script/Code.gs` (có thêm phần nhận ảnh) và đổi commit trong tệp `Index` của Apps Script.

## Dò giờ sinh

Bấm "Tìm giờ sinh" trên thẻ thông tin. Có tối đa 8 câu hỏi; câu nào không giúp phân biệt các giờ còn lại thì tự bỏ qua, câu nào không rõ thì bấm "Không rõ" (bản 2, 11/2026):
1. Giờ gia đình còn nhớ: giờ đồng hồ, tên giờ âm lịch (giờ Tý hỏi thêm trước hay sau 12 giờ đêm), hoặc mốc như "gà gáy", "lên đèn".
2. Cách sinh (mổ có hẹn trước thường rơi vào giờ hành chính).
3. Xoáy tóc (dân gian, tính nhẹ).
4. Dáng ngủ (dân gian, tính nhẹ).
5. Mảng đời chiếm tâm sức nhất từ 30 tuổi (cung an Thân), có trừ tỉ lệ người chọn công việc, tiền bạc.
6. Tính cách giống mô tả nào (sao chính cung Mệnh).
7. Tính vợ/chồng giống mô tả nào (sao chính cung Phu Thê).
8. 1–3 năm đời rẽ hướng (đại hạn).

Bộ tính lập sẵn lá số cho mọi giờ trong ngày sinh rồi chấm bằng phép Bayes: mỗi câu nhân một hệ số theo độ tin của câu đó, nên không giờ nào bị loại hẳn. Chi tiết trong `tvbt/docs/gio-sinh.md` (nhánh `tuvi-skill`). Kết quả là ước đoán để tham khảo.

Kho này công khai, không chứa dữ liệu khách. Dữ liệu khách chỉ nằm trong Google Sheet của chủ trang.
