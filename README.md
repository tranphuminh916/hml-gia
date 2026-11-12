# Sổ Tử Vi – trang cho khách

Nhánh này chứa trang web "Sổ Tử Vi" để gửi link cho khách. Nhánh `main` (trang HML) không liên quan và không bị sửa.

- `web/`: giao diện trang (`index.html`) cùng dữ liệu đi kèm.
  - `py-bundle.json`: bộ tính Tử vi – Bát tự của nhánh `tuvi-skill`, bản `1d6cbc5` (rà soát 11/2026; dò giờ sinh bản 2, sao hạn năm `hannam`, xem tuổi kiểu Việt Nam `tuoivn`), cộng thư viện lunar-python 1.4.8 (giấy phép MIT, xem `LICENSE-lunar-python.txt`).
  - `docs.json`: hướng dẫn luận.
  - Bộ tính chạy ngay trên máy khách bằng Pyodide.
- `apps-script/`: mã dán vào Google Apps Script, gắn với Google Sheet "Sổ Tử Vi – Khách".
  - `Code.gs`: ghi thông tin khách và các lần xem vào Sheet; phần luận gọi API Claude nếu có khóa.
  - `Index.html`: trang khung. Thay `__BASE__` bằng `https://cdn.jsdelivr.net/gh/tranphuminh916/hml-gia@<commit>/web/`.
- `tools/`: script dựng lại `py-bundle.json`; `giosinh.py` là bản sao công cụ dò giờ sinh (bản gốc ở nhánh `tuvi-skill`).

## Google nhắn mã kích hoạt (Firebase)

Khi đã điền cấu hình Firebase (biến `FIREBASE_CFG` trong `Code.gs`, hoặc thuộc tính tập lệnh `FIREBASE_CONFIG` dán nguyên đoạn `firebaseConfig`), khách đăng ký xong sẽ thấy nút "Gửi mã về số …". Google nhắn mã 6 số về số đó; khách nhập đúng là trang tự kích hoạt.

- Máy chủ hỏi Google số điện thoại vừa xác nhận (`accounts:lookup`) và chỉ kích hoạt khi trùng số khách đã đăng ký. Ô "Kích hoạt lúc" ghi thêm "(tự nhận mã)".
- Chủ vẫn nhận email báo khách mới kèm mã dự phòng; khách không nhận được tin thì bấm "Nhập mã chủ trang gửi".
- Cần gói Blaze của Firebase. Bật đăng nhập bằng số điện thoại, chỉ cho phép gửi tin tới Việt Nam (SMS region policy) và thêm tên miền của trang Apps Script (dạng `n-…-script.googleusercontent.com`) vào Authorized domains.
- Không điền cấu hình thì trang chạy như cũ: chủ gửi mã.

## Sửa thông tin sinh và xem lại

- Khi giờ, ngày, nơi sinh hay giới tính của một người vừa đổi (sửa tay hoặc "Ghi giờ" từ Tìm giờ sinh), kết quả đang hiện ở tab Lá số được đánh dấu "tính theo thông tin cũ" kèm nút xem lại.
- Ghi giờ từ Tìm giờ sinh xong, trang hiện ngay nút "Xem lại … với giờ mới".
- Xem lại không tính lượt: trong 24 giờ sau một lượt của cùng người, cùng mục, nếu thông tin sinh đã sửa; mỗi lượt cũ được 1 lần. Máy chủ kiểm lại (`xemLaiHopLe_`), dòng trong "Lượt xem" ghi "(xem lại sau khi sửa thông tin sinh, không tính lượt)". Giới hạn số lần luận mỗi ngày vẫn áp dụng.

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
