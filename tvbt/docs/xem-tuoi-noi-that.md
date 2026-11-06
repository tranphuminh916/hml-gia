# Xem tuổi kiểu Việt Nam, năm sinh con, bố trí trong nhà

## 1. Xem tuổi vợ chồng, làm ăn (`nc.py tuoivn`)

### Khi nào dùng
Người hỏi chỉ có năm sinh, hoặc hỏi theo kiểu quen thuộc: "tuổi Dần lấy tuổi Ngọ có hợp không", "năm nào sinh con hợp bố mẹ".

Có đủ ngày giờ sinh của cả hai người thì chạy thêm `nc.py hoptac` (so Bát tự), vì cách này sâu hơn. Khi hai cách nói khác nhau, ưu tiên Bát tự và nói rõ.

### Lệnh
```
python3 tvbt/nc.py tuoivn --nguoi 1986:nam 1990:nu
python3 tvbt/nc.py tuoivn --nguoi 1986:nam 1990:nu --con-tu 2026 --con-den 2032
```
Năm ghi là **năm âm lịch**. Người sinh trước Tết thì lấy năm trước.

### 5 tiêu chí
Mỗi tiêu chí script ghi Tốt / Bình / Xấu kèm lý do:

| # | Tiêu chí | Tốt | Xấu |
|---|---|---|---|
| 1 | Mệnh (ngũ hành nạp âm) | sinh nhau | khắc nhau |
| 2 | Thiên can năm | ngũ hợp | xung: Giáp–Canh, Ất–Tân, Bính–Nhâm, Đinh–Quý |
| 3 | Địa chi năm | tam hợp, lục hợp | xung, hình, hại, phá, tự hình |
| 4 | Cung phi Bát trạch (nam, nữ khác công thức) | Sinh Khí, Thiên Y, Diên Niên, Phục Vị (hai người cùng Đông hoặc cùng Tây tứ mệnh) | Họa Hại, Lục Sát, Ngũ Quỷ, Tuyệt Mệnh |
| 5 | Ngũ hành cung phi | sinh nhau | khắc nhau |

Ở tiêu chí 1 và 5, cùng hành là Bình.

### Cách nói kết quả
- Nói từng tiêu chí bằng lời thường, rồi nói chung. Ví dụ: "Ba điểm thuận, hai điểm bình; chỗ đáng lưu ý là …".
- **Không** quy ra điểm số. **Không** phán "không lấy được nhau", "khắc chồng/khắc vợ".
- Tiêu chí xấu thì nói cách bù theo tục:
  - Cung phi không hợp: kê giường, mở cửa theo hướng tốt của cả hai. Không có hướng chung thì ưu tiên người trụ cột.
  - Chi xung: tục nói nhường nhịn, chọn ngày cưới hợp tuổi.
- Năm sinh con:
  - Bảng so mệnh, can, chi năm của con với bố và mẹ.
  - Chỉ nói năm nào thuận hơn; không khuyên trì hoãn hay vội vàng chỉ vì tuổi.
  - Quyết định sinh con là chuyện sức khỏe, kinh tế của gia đình. Không bao giờ đoán con trai hay con gái.

## 2. Bố trí trong nhà theo Bát trạch (dựa vào bảng `tvbt.py phongthuy`)
Script đã in đủ bảng 8 hướng (du niên) theo cung phi của người, và Cửu tinh năm. Chỉ **tra** từ các bảng đó; không nhẩm cung phi.

| Hạng mục | Cách đặt theo Bát trạch | Ghi chú |
|---|---|---|
| Cửa chính | Mở ra một trong 4 hướng tốt của chủ nhà | Không đổi được hướng nhà thì chỉnh cửa phòng, giường, bàn |
| Bếp | **Tọa hung, hướng cát**: bếp đặt ở khu hướng xấu (Tuyệt Mệnh, Ngũ Quỷ, Lục Sát, Họa Hại) để "đè" cái xấu; mặt trước của bếp (phía người đứng nấu) quay về hướng tốt, tức người nấu đứng quay lưng về hướng tốt | Ý "tọa hung hướng cát" các sách thống nhất. Có nơi lại lấy hướng mặt người nấu nhìn vào làm hướng bếp, nên khi trả lời phải nói rõ đang theo cách nào |
| Ban thờ | Đặt ở khu tốt, mặt ban thờ hướng về một hướng tốt của chủ nhà (tọa cát hướng cát) | Có nơi theo hướng nhà; nói rõ khi hai cách khác nhau |
| Giường | Đầu giường quay về hướng tốt: Thiên Y khi cần giữ sức, Diên Niên cho vợ chồng hòa thuận, Sinh Khí khi cần làm ăn | Vợ chồng khác nhóm thì ưu tiên người cần hơn, hoặc chọn Phục Vị của một người |
| Bàn làm việc | Ngồi quay mặt về Sinh Khí hoặc Phục Vị | Lưng có tường tựa |
| Nhà vệ sinh, kho | Đặt ở khu hướng xấu | – |

**Năm nay** (bảng Cửu tinh):
- Cung có Ngũ Hoàng (5) và Nhị Hắc (2): tránh động thổ, đục phá, sửa lớn trong năm.
- Hướng Thái Tuế và Tuế Phá: không đặt bếp mới, không khởi công quay về hai hướng này trong năm. Script có in hai hướng này.

## 3. Kiểm tra hình thế (loan đầu)
Hỏi người dùng từng mục theo bảng dưới, rồi nói gọn mục nào chưa ổn và cách chỉnh nhẹ. Nguồn: Bát trạch minh kính, Dương trạch tam yếu và kinh nghiệm phổ biến.

| Nhóm | Mục kiểm tra |
|---|---|
| Bếp | Không nhìn thẳng ra cửa chính; không đối diện hoặc sát cửa nhà vệ sinh; bếp lửa không sát chậu rửa, tủ lạnh (thủy hỏa xung), cách ra một đoạn hoặc có vật ngăn; không đặt dưới xà ngang; sau lưng bếp nên là tường đặc |
| Ban thờ | Không dựa lưng vào tường nhà vệ sinh hoặc bếp; không đặt dưới gầm cầu thang; không đối diện thẳng cửa chính hoặc cửa nhà vệ sinh; trên ban thờ không là nhà vệ sinh của tầng trên; nơi yên tĩnh, sạch, sáng vừa |
| Giường | Không nằm dưới xà ngang; không có gương chiếu thẳng vào giường; chân giường không chĩa thẳng ra cửa phòng; đầu giường dựa tường đặc, không sát cửa sổ |
| Cửa, cầu thang | Cầu thang không đổ thẳng ra cửa chính; cửa chính không đối thẳng cửa sau (xuyên tâm); cửa chính không bị cột điện, góc nhọn nhà khác chĩa vào |
| Chung | Nhà thông thoáng, đủ sáng; không bày đồ hỏng, cây chết |

## 4. Nói gì, không nói gì
- **An toàn trước phong thủy.** Bếp ga, điện, lối thoát hiểm, thông gió quan trọng hơn mọi hướng tốt xấu. Đừng bao giờ khuyên dời bếp hay đổi cửa trái với an toàn hoặc quy định xây dựng.
- Ưu tiên cách chỉnh rẻ, dễ làm: xoay bàn, đổi đầu giường, kê lại đồ. **Không** khuyên mua vật phẩm phong thủy, đá, tượng, bùa. **Không** giới thiệu dịch vụ trả tiền.
- Đo hướng nhà: đứng ở cửa chính nhìn thẳng ra ngoài; xem mục đo hướng trong `co-ban.md`.
