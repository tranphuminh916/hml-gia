# Kỳ môn mở rộng: phi bàn, âm bàn, niên/nguyệt/nhật gia, Mao Sơn, khắc ứng, vẽ bàn, bản mệnh

> Phần cài đặt và tự kiểm tra đã làm ở Bước 2 của SKILL.md (skill tu-vi-bat-tu-phong-thuy-v3). Mọi file đã có sẵn trong `tvbt/`; bỏ qua mọi chỗ nhắc tới "trích", "vá", "Bước 1/2 của skill v2" hay tên các skill cũ (v2, luan-la-so-chi-tiet, ky-mon-mo-rong, …) – nay tất cả là một bộ.

## Đã kiểm chứng
- Chuyển bàn thời gia (hủy bổ, trí nhuận) và bảng cách cục: giữ nguyên của v2. Tự kiểm tra của v2 vẫn ĐẠT sau khi vá.
- **Phi bàn** (phái Mao Sơn / Đạo Âm): khớp toàn bộ thần, sao, môn, can của 3 bàn mẫu đã công bố:
  - dương 1 cục 23/12/2006 giờ Bính Thân;
  - âm 4 cục ngày Quý Hợi giờ Đinh Tỵ (2/8/2006);
  - âm 8 cục 10/7/2008 giờ Giáp Ngọ (trực phù Thiên Cầm ở trung cung).
- Định cục **Mao Sơn** ra đúng cục của cả 3 bàn trên.
- **Âm bàn** (Vương Phượng Lân):
  - công thức cục khớp 21/21 ví dụ có ngày giờ (*Đế vương chi thuật*, *Đạo gia kỳ môn dự trắc tam thập lệ*);
  - sao, môn, thần, can thiên/địa bàn và ẩn can khớp 5 bàn mẫu, có cả trường hợp can giờ đã ở cung trực sử (thực lệ 13).
- **Niên gia, nguyệt gia, nhật gia**:
  - khớp ví dụ của *Kỳ môn pháp khiếu*: nhật gia dương 1 ngày Canh Tý → Thiên Phụ đến Chấn, Đỗ môn đến Khảm; âm 9 ngày Đinh Mão → Thiên Anh đến Chấn, Cảnh môn đến Càn;
  - khớp ví dụ của Trần Bỉnh Duật: niên gia 2002 hạ nguyên âm 7 → Thiên Tâm, Khai môn; nguyệt gia tháng Ất Tỵ 2002 → Thương môn đến Khôn.
- **Thập can khắc ứng** đủ 81 cặp, đối chiếu 3 bảng đầy đủ và 4 bảng một phần. Chỗ các sách đặt tên khác nhau có ghi dị danh.
- Chạy ngẫu nhiên 1901–2099 với mọi tổ hợp gia × bàn × phép định cục (cả trạng thái, bản mệnh, vẽ ảnh): không lỗi.
- Đối chiếu với bàn của một phần mềm Việt Nam (Phong Thủy Đại Nam) lúc 07:47 31/10/2026, Hà Nội: cả 9 cung trùng (âm 2 cục; thần, sao, môn, can; Kv, Mã), và trạng thái họ ghi cũng trùng: Khai môn phản ngâm, Thiên Tâm "hưu" (khớp cột "cung" của skill), Trực Phù "Mộ" (khớp trường sinh tại Thìn).

## Chạy

Thông tin cần hỏi giống v2: việc cần hỏi, thời điểm (mặc định bây giờ), nơi đang ở.

```bash
python3 tvbt/tvbt.py kymon --noi "Hà Nội"                                        # chuyển bàn, thời gia, hủy bổ (như v2)
python3 tvbt/tvbt.py kymon --kymon-ban phi --kymon-phep maoson --noi "Hà Nội"     # phi bàn, định cục Mao Sơn
python3 tvbt/tvbt.py kymon --kymon-ban am --noi "Hà Nội"                         # âm bàn Vương Phượng Lân (có ẩn can)
python3 tvbt/tvbt.py kymon --kymon-gia nien --ngay 2027-03-01 --gio 08:00        # niên gia; nguyet, nhat tương tự
python3 tvbt/tvbt.py kymon --noi "Hà Nội" --nam-sinh 1990 --ve-ban /tmp/ban.png --cau-hoi "Việc cần hỏi"   # kèm bản mệnh + ảnh
```

**Mặc định mỗi lần lập bàn cho người dùng:** thêm `--ve-ban <đường dẫn .png>` và `--cau-hoi "<câu hỏi>"`. Nếu biết năm sinh người hỏi (từ hội thoại hoặc bộ nhớ) thì thêm `--nam-sinh`. Sau khi chạy, gửi file PNG cho người dùng bằng công cụ gửi file, kèm một dòng chú thích. Nếu không vẽ được PNG, gửi file HTML cùng tên.

Tham số mới:
- `--kymon-ban chuyen|phi|am`:
  - `chuyen`: chuyển bàn (mặc định).
  - `phi`: phi bàn.
  - `am`: âm bàn Vương Phượng Lân, chỉ dùng với thời gia.
- `--kymon-gia thoi|nhat|nguyet|nien`:
  - `thoi`: thời gia, chiêm việc theo giờ (mặc định).
  - `nhat`, `nguyet`, `nien`: khí vận cả ngày, cả tháng, cả năm.
  - Dùng được với chuyển bàn và phi bàn.
- `--kymon-phep huybo|trinhuan|maoson`: phép định cục thời gia. Script luôn tính cả ba và in `!` khi chúng ra cục khác nhau.
- `--an-can-khong-bay`: chỉ cho âm bàn. Khi can giờ vốn đã ở cung trực sử thì giữ ẩn can trùng địa bàn. Mặc định là nhập trung cung rồi bay.
- `--lich-tz 8`: dùng lịch âm Trung Quốc (sách âm bàn dùng lịch này). Script tự cảnh báo khi lịch Việt Nam và lịch Trung Quốc cho ra hai cục khác nhau.
- `--nam-sinh YYYY`: đánh dấu **cung bản mệnh**, tức cung có can năm sinh trên thiên bàn (Giáp đọc theo nghi ẩn). Năm tính từ Lập Xuân: người sinh tháng 1 hoặc đầu tháng 2 dương lịch có thể thuộc năm trước, cần hỏi lại.
- `--ve-ban PATH.png`: vẽ bàn 9 cung thành ảnh, kèm file `.html` cùng tên. Ảnh có màu cát/hung, Kv, Mã, Trực phù, Trực sử, bản mệnh, trạng thái và ý nghĩa ngắn ở mỗi ô. Cần Chromium và Playwright; thiếu thì chỉ có HTML.
- `--cau-hoi "..."`: in câu hỏi lên đầu ảnh.

## Luận giải Kỳ môn

Trình bày theo v2: (1) bảng số liệu, (2) luận theo mục, (3) lưu ý và độ chắc chắn. Không phán chắc chắn, không gieo sợ hãi, chỉ trả lời câu đã hỏi.

1. **Dụng thần theo việc hỏi**: chọn 1–2 yếu tố, tìm cung chứa nó.

   | Việc | Xem chủ yếu |
   |---|---|
   | Bản thân người hỏi | Can ngày (trên thiên bàn), Trực phù |
   | Việc đang hỏi / thời cơ | Can giờ, Trực sử |
   | Tiền bạc, kinh doanh | Sinh môn, Mậu (vốn), Thiên Tâm |
   | Công việc, thăng tiến | Khai môn, Trực phù, Thiên Phụ |
   | Hợp tác, hôn nhân | Lục Hợp; Ất (nữ), Canh (nam); Đinh – Nhâm |
   | Thi cử, giấy tờ | Cảnh môn, Đinh, Thiên Phụ |
   | Sức khỏe | Thiên Nhuế (bệnh), Thiên Tâm (thầy thuốc), Ất (thuốc) |
   | Kiện tụng | Kinh môn, Khai môn (quan tòa), Canh |
   | Đi xa | Dịch mã, Hưu môn, Khai môn; cung của hướng định đi |

2. **Đánh giá cung dụng thần**:
   - Môn: cát (Khai, Hưu, Sinh) hay hung (Tử, Kinh, Thương).
   - Thần: Cửu Thiên, Cửu Địa, Trực Phù, Thái Âm, Lục Hợp là cát; Bạch Hổ, Huyền Vũ, Đằng Xà thì cẩn thận.
   - Không vong: việc chưa thành, còn hư. Mã: việc động, nhanh.
   - Sinh khắc giữa cung việc và cung bản thân (Khảm Thủy; Khôn, Cấn Thổ; Chấn, Tốn Mộc; Càn, Đoài Kim; Ly Hỏa): cung việc sinh hoặc trợ cung mình là thuận, khắc cung mình là nghịch.
   - Vượng suy bát môn theo tháng: môn cát vượng/tướng thì có lực; hưu/tù/tử thì yếu.
3. **Hướng**: gợi ý hướng có môn cát và thần cát; tránh hướng có Tử môn, Kinh môn, Bạch Hổ.
4. **Dụng thần theo can**: dòng này cho biết cung chứa can năm (bề trên, việc lớn), can tháng (anh em, đồng nghiệp), can ngày (người hỏi) và can giờ (việc hỏi). Cung can ngày và cung can giờ sinh, trợ nhau là thuận; khắc nhau là trở ngại.
5. **Thập can khắc ứng** (bảng "THẬP CAN KHẮC ỨNG TỪNG CUNG", có cho mọi loại bàn):
   - Mỗi cung là một cặp: can thiên bàn trên can địa bàn. Giáp ẩn nên đọc theo Mậu.
   - Chỉ dẫn các cặp ở cung dụng thần, cung can ngày, cung can giờ và hướng định đi.
   - Khắc ứng luôn đi cùng môn. Cách cát gặp hung môn, môn bức, nhập mộ hay kích hình thì giảm hoặc hóa hung. Cách hung gặp cát môn, cát thần thì nhẹ đi.
   - Dị danh in trong ngoặc, không cần nêu hết.
6. **Cách cục** (bảng "CÁCH CỤC NHẬN DIỆN ĐƯỢC", có cho chuyển bàn và âm bàn): đọc như mục 4.4.8 của v2. Không tự gán cách ngoài bảng.
7. **Các phép định cục**:
   - Nếu script báo các phép (hủy bổ / trí nhuận / Mao Sơn) ra cục khác nhau, chạy thêm phép kia, nói rõ chỗ khác, hoặc hỏi người dùng theo phái nào.
   - Mao Sơn lệch nhiều nhất: 5 ngày đầu sau giao tiết luôn là thượng nguyên.
   - Phi bàn trong sách thường đi với Mao Sơn.
8. **Phi bàn** (`--kymon-ban phi`): đọc như chuyển bàn, khác ở mấy điểm:
   - Trung cung có sao, can, thần riêng nhưng **không có môn**. Việc rơi vào trung cung thì xét sao, thần, khắc ứng ở đó, kèm môn của cung ký (dương độn ký Cấn, âm độn ký Khôn).
   - Cửu thần có **Thái Thường**: cát, chủ yến tiệc, lễ nghi, ăn uống, áo mũ.
   - Dương độn dùng **Câu Trận** (trì trệ, tranh chấp, đất đai) và **Chu Tước** (văn thư, khẩu thiệt); âm độn dùng Bạch Hổ, Huyền Vũ.
   - Chưa có bảng cách cục tổng hợp cho phi bàn: luận từ môn, sao, thần và khắc ứng.
9. **Âm bàn Vương Phượng Lân** (`--kymon-ban am`):
   - Cục không theo tiết khí mà theo (chi năm + tháng âm + ngày âm + chi giờ) chia 9. Script in sẵn phép cộng.
   - **Ẩn can** (cột riêng) là việc ngầm, động cơ thật, điều chưa lộ của cung đó:
     - Xét can ngày và can giờ trên thiên bàn **và** trong ẩn can.
     - Ẩn can của cung dụng thần sinh hay khắc cung bản thân cho biết bên trong thuận hay nghịch.
     - Ẩn can trùng thiên bàn hoặc địa bàn: việc đã lộ rõ.
   - Phái này coi trọng tượng của cung, sao, môn, thần hơn cách cục cổ. Khắc ứng và cách cục chỉ là phần bổ trợ.
10. **Niên gia / nguyệt gia / nhật gia** (`--kymon-gia nien|nguyet|nhat`):
    - Không dùng để chiêm việc theo giờ, mà để xem khí vận chung của năm, tháng, ngày.
    - Phương có cát môn, cát thần thì nên hướng tới, xuất hành, mở việc lớn. Phương hung thì tránh động thổ, đi xa.
    - Can chi năm/tháng/ngày đóng vai trò "giờ".
    - Các phép này ít dùng và sách nói khác nhau, nhất là nguyệt gia và mốc năm. Luôn nói là tham khảo; việc cụ thể vẫn lập thời gia.
11. **Trạng thái từng cung** (bảng "TRẠNG THÁI TỪNG CUNG", cũng in trên ảnh):
    - **Phục ngâm** (môn hay sao nằm ở cung nhà): việc đình trệ, nên giữ. **Phản ngâm** (nằm ở cung đối diện): việc lật ngược, đi rồi về, dễ thay đổi.
    - Quan hệ môn – cung:
      - **Môn bức** (môn khắc cung): cát môn bị bức thì việc tốt khó thành; hung môn bị bức thì hung thêm.
      - **Môn chế** (cung khắc môn): môn bị kiềm, lực yếu.
      - **Môn nghĩa** (cung sinh môn) và **môn hòa** (môn sinh cung): thuận. Sách mới gọi trường hợp môn sinh cung là "môn tướng".
      - **Môn nhập mộ**: môn bị giam, khó phát huy.
    - **Vượng suy cửu tinh** theo *Yên Ba điếu tẩu ca*: ta sinh = vượng, đồng hành = tướng, ta khắc = hưu, khắc ta = tù, sinh ta = phế.
      - Cột "tháng" so với hành của tháng; cột "cung" so với hành của cung.
      - Phần mềm Việt Nam đã đối chiếu có vẻ dùng cột "cung". Nói rõ hai cách khi chúng khác nhau.
      - Sao vượng/tướng thì có lực; hưu/tù/phế thì yếu.
    - **12 trường sinh** của thần và của can thiên bàn tại các chi của cung. Cung góc có hai chi nên ghi cả hai.
      - Trường sinh, Quan đới, Lâm quan, Đế vượng là có sức.
      - Bệnh, Tử, Mộ, Tuyệt là yếu hoặc bị giam.
      - Can **nhập mộ** là việc bị chôn, khó ra; nếu can đó vượng theo mùa thì có sách gọi là "nhập khố" (được cất giữ).
    - Chỉ dẫn trạng thái của cung dụng thần, cung bản thân, cung bản mệnh và hướng định đi; không đọc hết cả bàn.
12. **Loại tượng** (bảng "LOẠI TƯỢNG…", và dòng "Ý:" trên ảnh): nghĩa tham khảo của môn, sao, thần, can. Phải đặt vào câu hỏi cụ thể; ví dụ với câu hỏi về logistics, Nhâm (lưu động, vận tải) và Sinh môn (lợi nhuận) đáng chú ý hơn.
13. **Cung bản mệnh** (khi có `--nam-sinh`): đại diện cho chính người hỏi theo tuổi, bổ sung cho can ngày. Xét cung bản mệnh và cung việc (can giờ, môn dụng thần) sinh hay khắc nhau, và trạng thái của cung bản mệnh (Kv, nhập mộ, môn bức…).

## Trường phái đã chọn (nói rõ khi liên quan)
- **Mao Sơn**: giao tiết là dùng ngay thượng nguyên; sau 120 giờ dùng trung nguyên; sau 240 giờ dùng hạ nguyên đến hết tiết. Không siêu thần, không nhuận.
- **Phi bàn** (Mao Sơn / Đạo Âm, *Kỳ môn pháp khiếu*):
  - Sao: trực phù tinh bay đến cung can giờ; các sao theo số Lạc Thư bay qua cả 9 cung, dương thuận, âm nghịch. Mỗi sao mang can địa bàn của cung nhà. Thiên Cầm không ký cung.
  - Môn: trực sử đếm từ cung tuần thủ, tính cả trung cung. Rơi vào trung cung thì dương ký Cấn, âm ký Khôn. 8 môn bay qua 8 cung ngoài. Tuần thủ ở trung cung thì trực sử là Sinh môn (dương) hoặc Tử môn (âm).
  - Cửu thần dương độn: Trực Phù, Đằng Xà, Thái Âm, Lục Hợp, Câu Trận, Thái Thường, Chu Tước, Cửu Địa, Cửu Thiên. Âm độn thay Câu Trận, Chu Tước bằng Bạch Hổ, Huyền Vũ.
  - Chưa tính phái phi bàn "mọi thứ bay thuận, ký Khôn cả hai độn".
- **Âm bàn** (Vương Phượng Lân):
  - Cục: dư 0 tính là 9.
  - Ba điểm sách không nói rõ, đang theo phần mềm phổ biến: chi năm tính từ Lập Xuân; tháng nhuận lấy số tháng thường; 23h đã sang ngày mới.
  - Dương độn từ Đông Chí đến trước Hạ Chí.
  - Sao và môn an như chuyển bàn, luôn xoay theo chiều kim đồng hồ. Thần: dương thuận, âm nghịch.
  - Ẩn can: xoay nguyên vòng địa bàn để can giờ đến cung trực sử. Nếu can giờ vốn ở cung trực sử thì nhập trung cung rồi bay 9 cung (theo thực lệ 13). Một số bàn trong sách in ẩn can trùng địa bàn: dùng `--an-can-khong-bay`.
  - Chưa tính ẩn can theo phái Mạnh Lệnh Vĩ, Vương Minh.
- **Niên gia**: luôn âm độn. Mỗi nguyên 60 năm: 1864 thượng (âm 1), 1924 trung (âm 4), 1984–2043 hạ (âm 7). Năm tính từ Lập Xuân (sách không nói rõ).
- **Nguyệt gia**: luôn âm độn, 5 năm một nguyên, theo chi của năm Giáp/Kỷ mở đầu khối:
  - Dần Thân Tỵ Hợi: thượng (âm 1); Tý Ngọ Mão Dậu: trung (âm 7); Thìn Tuất Sửu Mùi: hạ (âm 4).
  - Đây là phái Vương Thụy Dân, Trần Bỉnh Duật; có bản chép đảo trung và hạ. Tháng tính theo tiết khí.
- **Nhật gia** (*Kỳ môn pháp khiếu*): ngày Giáp Tý gần tiết nào nhất thì 60 ngày đó dùng cục của tiết ấy:
  - Đông Chí dương 1; Vũ Thủy dương 7; Cốc Vũ dương 4.
  - Hạ Chí âm 9; Xử Thử âm 3; Sương Giáng âm 6.
  - Gần như trùng với *Ngự định kỳ môn bảo giám*. Không dùng lối "Hưu môn 3 ngày đổi cung" của *Độn giáp diễn nghĩa*.
- **Khắc ứng**: bảng 81 cặp theo *Thống tông* / *Bí cấp đại toàn*. Khoảng 40 cặp có tên khác nhau giữa các sách. Ví dụ: Mậu + Ất là Thanh Long hợp linh hay hợp hội; Bính + Kỷ là Hỏa bội nhập hình hay Nguyệt kỳ nhập mộ.

- **Trạng thái**:
  - Ngũ hành thần: Trực Phù, Câu Trận, Cửu Địa là Thổ; Đằng Xà, Chu Tước là Hỏa; Thái Âm, Bạch Hổ, Cửu Thiên là Kim; Lục Hợp là Mộc; Huyền Vũ là Thủy; Thái Thường tạm lấy Thổ. Có phái lấy Trực Phù là Mộc (Giáp).
  - Trường sinh của thần: Thổ theo Thủy (thủy thổ cộng mộ ở Thìn).
  - Trường sinh của can: dương thuận âm nghịch; Mậu theo Bính, Kỷ theo Đinh.
  - Can nhập mộ: Giáp, Quý ở Khôn; Ất, Bính, Mậu ở Càn; Đinh, Kỷ, Canh ở Cấn; Tân, Nhâm ở Tốn.
  - Bát môn vượng suy theo tháng dùng ngũ hành thông thường (đương lệnh vượng); khác với quy tắc của cửu tinh.

## Còn chưa tính
- Kỳ môn khắc gia (theo phút): các phái khác nhau quá nhiều.
- Trạng thái của ẩn can (âm bàn) chưa in riêng.
- Bảng cách cục tổng hợp cho phi bàn.
- Phi bàn phái "mọi thứ bay thuận".
- Ẩn can phái Mạnh Lệnh Vĩ, Vương Minh.
