# Cách cục Tử vi (lệnh nc.py cachcuc)

> Phần cài đặt và tự kiểm tra đã làm ở Bước 2 của SKILL.md (skill tu-vi-bat-tu-phong-thuy-v3). Mọi file đã có sẵn trong `tvbt/`; bỏ qua mọi chỗ nhắc tới "trích", "vá", "Bước 1/2 của skill v2" hay tên các skill cũ (v2, luan-la-so-chi-tiet, ky-mon-mo-rong, …) – nay tất cả là một bộ.

## Có gì
| Lệnh | Làm gì |
|---|---|
| `cachcuc` | Nhận diện cách cục Tử vi ở cung Mệnh (cùng tam phương tứ chính) và cung Thân, mức thành cách / cách yếu / phá cách, kèm căn cứ và nguồn; `--nam-xem` xét thêm cung đại hạn, tiểu hạn của năm đó |

## Đã kiểm chứng
- **Cách cục Tử vi (`cachcuc`).**
  - Các bảng tháng – giờ (Phụ củng văn tinh, Xương Khúc giáp, Tả Hữu đồng cung) và các bảng theo can năm (Thiên Ất củng mệnh, Khôi Việt giáp, Kình Dương nhập miếu, Mã đầu đới kiếm) khớp nguồn.
  - 14 lá số mẫu chạy qua toàn bộ chuỗi đổi giờ và đổi lịch đều rơi đúng cách nguồn nêu.
  - Chạy 5.000 lá số ngẫu nhiên năm 1930–2020 không lỗi:
    - Tử Phủ đồng cung xuất hiện 1,42%, sát mức lý thuyết 1/72.
    - Không cách nào xuất hiện quá 25%.
  - Khoảng 35 bất biến về vị trí đều đúng, ví dụ Tử Phủ đồng cung chỉ ở Dần/Thân, Tử Sát chỉ ở Tỵ/Hợi.
- **Rà soát độc lập 11/2026.** Hai trợ lý tra sách (Toàn thư, Toàn tập, phú Cốt tủy, Thái vi; Tân Biên, Dịch Lý Huyền Cơ, tuvisonkhiem; Vương Đình Chi, 紫微樓, 斗數宣微...) và viết lại điều kiện thành cách, phá cách của cả 55 cách mà không xem mã. Hai trợ lý khác so bản đó với mã, chạy thử trên lá số dựng tay và 5.000 lá số ngẫu nhiên. Đã sửa:
  - lỗi thật: Cự Hỏa Kình Dương nhận cả bộ Đà + Linh (nay đòi đủ Hỏa + Kình; "Cự phùng tứ sát" đòi đủ Kình Đà Hỏa Linh, bản ba nhóm sát của tuvisonkhiem chỉ là cách yếu); Lộc phùng xung phá hạ nhẹ đúng thế Hóa Lộc bị Hóa Kỵ đối cung (vốn là định nghĩa gốc); Nhật Nguyệt phản bối coi cát hóa trên Nhật Nguyệt là cứu (Toàn thư không tính); Thạch trung ẩn ngọc coi Tuần Triệt là yếu (sách Việt coi là điều kiện hay); Nhật Nguyệt đồng lâm kiểu chiếu coi Tuần Triệt là yếu; Cự Nhật đếm trùng sát tinh; Không Kiếp giáp ghi Thiên Phủ (Đ) là miếu vượng;
  - lệch nguồn: Quân thần khánh hội nay xét cả hai cung giáp (trước đó gần như không thể có ở 6 can năm); Đào hoa phạm chủ thành theo vị trí Tử Tham Mão Dậu, sao đào hoa chỉ làm nặng; Phủ Tướng triều viên, Kình Dương nhập miếu, Lộc hợp uyên ương: Tuần Triệt hạ từ phá xuống yếu; thêm điều kiện phá hoặc yếu còn thiếu cho Anh tinh nhập miếu (tứ sát tại Mệnh, tuổi Bính Mậu), Hỏa/Linh Tham, Lộc Mã giao trì (Hóa Kỵ xung), Thất Sát triều đẩu (Kình, Linh), Cơ Nguyệt Đồng Lương (Kình Đà), Nguyệt sinh thương hải (Hóa Kỵ), Minh châu xuất hải (Kình Đà tại Mệnh), Dương Lương Xương Lộc (sát tinh), Thiên Ất củng mệnh (Hóa Kỵ là phá), Vũ Khúc thủ viên (Tuần Triệt là phá); Lương Mã kiểu Mã ở Thiên Di chỉ nhận khi có sát, không cát (斗數宣微); Hỏa Tham, Mã đầu, Minh Lộc ám Lộc, Lương Mã chỉ xét ở Mệnh.
  - Còn để ngỏ (sách định nghĩa rất khác nhau, script giữ một phương án và ghi rõ): Nhật Nguyệt tịnh minh (ít nhất 4 kiểu), Vũ Khúc thủ viên (Mão / mọi chỗ miếu vượng / Thìn Tuất), Mã đầu đới kiếm (cát hay hung), Thất Sát triều đẩu (bốn cung hay Dần Thân), Hùng tú triều viên, Hình Kỵ giáp ấn, Bách quan triều củng.

## Chạy
Tham số ngày giờ giống `tvbt.py`: `--ngay YYYY-MM-DD --gio HH:MM --gioi nam|nu --noi "<tỉnh>"`, cộng `--am`, `--nhuan`, `--kinhdo`, `--utc`, `--mien`, `--gio-dong-ho`, `--ty` khi cần. Mọi lệnh có `--help`.

```bash
python3 tvbt/nc.py cachcuc --ngay 1990-05-17 --gio 08:30 --gioi nam --noi "Hà Nội" [--nam-xem 2026]
```

## Luận
Trình bày theo v2: (1) bảng số liệu, (2) luận theo mục, (3) lưu ý và độ chắc chắn. Không phán chắc chắn, không gieo sợ hãi, không quyết định y tế, tài chính, pháp lý thay người dùng. Chạy lệnh này cùng phần Tử vi của v2, đưa các cách có mức "thành cách" hoặc "phá cách" ở Mệnh, Thân vào bản luận.

### 4.1 Cách cục Tử vi (lệnh `cachcuc`)
**Lệnh:** `python3 tvbt/nc.py cachcuc --ngay … --gio … --gioi … --noi …`. Muốn xem hạn một năm thì thêm `--nam-xem 2026`.
- Kết quả là bảng 5 cột: Cách | Nhóm | Mức | Cung | Căn cứ.
- Cột Căn cứ ghi sao nào, độ sáng, ở cung nào. Số trong ngoặc vuông trỏ tới nguồn ở cuối bảng.
- Script xét cung Mệnh (cùng tam phương tứ chính) và cung Thân. Có khoảng 66 tên cách theo sách Việt Nam.

**Cách cục là gì:** một thế sao được sách xưa đặt tên, thường đi kèm một kiểu đời sống. Cách chỉ là tín hiệu tổng quát, không thay cho việc xét từng cung, từng sao.

**Cột Mức:**
- **Thành cách:** đủ thế sao và đủ điều kiện.
- **Cách yếu:** có thế sao nhưng thiếu điều kiện, ví dụ chính tinh kém sáng, gặp Tuần Triệt, thiếu cát tinh, hoặc chỉ mượn sao cung đối. Với cách hung, "cách yếu" nghĩa là cái xấu đã giảm bớt.
- **Phá cách:** bị phá rõ (gặp Không Kiếp, Hóa Kỵ đúng chỗ, đủ bộ sát tinh). Không có nghĩa là xấu hẳn, chỉ là cái tốt khó phát huy trọn.

**Thứ tự cân nhắc:**
- Độ sáng chính tinh → Tứ hóa → cát tinh và sát tinh ở tam phương → cung đối → thế giáp → sao nhỏ.
- Một thành cách ở Mệnh nặng hơn ở Thân; ở Thân nặng hơn ở cung hạn.

**Cách nói:**
- Dùng lời "lá số có nét của cách…", "sách xưa cho rằng…".
- Cách tốt là thuận lợi tiềm năng, cần nỗ lực và thời điểm.
- Cách hung là điểm cần lưu tâm. Nói kèm cách làm cho nhẹ đi:
  - Lộc phùng xung phá: giữ tiền chặt, tránh vay mượn mạo hiểm.
  - Lương Mã phiêu đãng: chọn nghề hợp với di chuyển.
  - Cự Hỏa Kình Dương: giữ lời, tránh tranh cãi.
- Nhiều cách cùng lúc thì tìm điểm chung. Ví dụ Tử Phủ đồng cung đi cùng Vô đạo chi quân: nền tốt nhưng nên chọn cộng sự kỹ.
- Hai cách ngược nhau: nói cả hai, kèm điều kiện của từng cách.

**Ghi chú theo nhóm:**
- **Tử Vi** cần "bề tôi" là Tả Hữu, Xương Khúc, Khôi Việt.
  - Có đủ bề tôi: Quân thần khánh hội, Bách quan triều củng.
  - Thiếu hết bề tôi: Tại dã cô quân, phải tự lực.
  - Sát tinh nhiều hơn bề tôi: Vô đạo chi quân, nên giữ nguyên tắc.
  - Tử Phủ, Tử Tướng rất kỵ Tuần, Triệt, Địa Không.
- **Nhật Nguyệt:** xét sáng hay mờ trước. Người sinh ban ngày hợp Thái Dương, sinh ban đêm hợp Thái Âm. Nhật Nguyệt hãm mà gặp Tuần Triệt có khi lại sáng.
- **Lộc Mã:**
  - Lộc Mã giao trì hợp buôn bán, làm ăn xa.
  - Song Lộc, Lộc hợp uyên ương sợ nhất Không Kiếp.
  - Lộc Tồn ở Mệnh luôn bị Kình Đà kẹp. Đó là cái giá đi kèm, không phải tai họa.
- **Giáp (kẹp):** cát tinh kẹp là có người đỡ hai bên; sát tinh kẹp là có áp lực hai bên. Chính tinh ở giữa vững thì chịu được.
- **Mệnh vô chính diệu:**
  - Luận theo chính tinh cung đối, lực khoảng 7 phần, cộng với sao tại Mệnh.
  - Đắc Tam Không (đủ Tuần, Triệt, Thiên Không, Địa Không): sách đánh giá tốt.
  - Đắc Không Kiếp: sách không thống nhất, nói thận trọng.
- **Tuần, Triệt:** Tuần ảnh hưởng lâu dài. Triệt mạnh ở khoảng ba đại hạn đầu, nhẹ dần từ khoảng 35 tuổi.

**Xét hạn (`--nam-xem`):**
- Script xét cung đại hạn và tiểu hạn như một Mệnh nhỏ, bằng sao gốc, và liệt kê sao lưu chạm tam phương của cung hạn.
- Cách tốt mà gặp lưu Hóa Kỵ: khuyên thận trọng việc lớn.
- Cách hung mà gặp lưu Lộc, lưu Khoa: nói là có cơ hội gỡ.

**Đối chiếu:** cách cục nên kiểm với sự kiện thật của người xem trước khi luận sâu. Giờ sinh sát ranh giới thì Mệnh và cách có thể đổi: lập lá số với giờ bên cạnh để so.

## Trường phái và giới hạn (nói rõ khi liên quan)
- **Cách cục Tử vi:**
  - An sao theo v2 (Thái Thứ Lang); Khôi Việt theo "Canh Tân phùng Mã Hổ".
  - Nhiều cách có 2–3 định nghĩa. Skill chọn như sau:
    - Tử Phủ triều viên: Tử Vi và Thiên Phủ chầu về Mệnh.
    - Phủ Tướng triều viên: Thiên Phủ ở Quan Lộc, Thiên Tướng ở Tài Bạch chầu về.
    - Sát Phá Tham: chỉ tính khi sao ở Mệnh đắc địa.
    - Hình Kỵ giáp ấn: lấy Kình Dương làm "Hình"; bản lấy Thiên Hình thì chỉ ghi là cách yếu.
    - Hùng tú triều viên: Liêm Trinh ở Dần, Thân.
  - Ở cung hạn chưa dựng lại cách theo lưu tinh; sao lưu chỉ được liệt kê kèm theo.
  - Nguồn đối chiếu là các trang tiếng Việt có dẫn sách (Toàn thư, Tân Biên, Chỉ nam…). Lá số mẫu dùng để kiểm là thế sao do nguồn nêu, không phải lá số người thật.
