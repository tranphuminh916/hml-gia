# Bát tự/Tử vi nâng cao: vượng suy, ảnh lá số, vận thế, hợp tác, lưu nhật, tự kiểm bản luận

> Phần cài đặt và tự kiểm tra đã làm ở Bước 2 của SKILL.md (skill tu-vi-bat-tu-phong-thuy-v3). Mọi file đã có sẵn trong `tvbt/`; bỏ qua mọi chỗ nhắc tới "trích", "vá", "Bước 1/2 của skill v2" hay tên các skill cũ (v2, luan-la-so-chi-tiet, ky-mon-mo-rong, …) – nay tất cả là một bộ.

## Có gì
| Lệnh | Làm gì | Dùng khi |
|---|---|---|
| `vuongsuy` | Vượng suy Nhật chủ bằng 2 thang độc lập, độ tin; cách cục Bát tự theo nguyệt lệnh; ám hợp, củng hợp, cái đầu/tiệt cước, lục phá | Mọi lần luận Bát tự |
| `anhtuvi`, `anhbattu` | Vẽ lá số Tử vi (12 cung) và bảng Bát tự thành ảnh PNG | Mặc định khi lập lá số cho người dùng |
| `vanthe` | Bảng và biểu đồ vận thế theo năm (điểm do script tính) | Bản luận vận hạn nhiều năm |
| `hoptac` | Chấm điểm hợp tác / hôn nhân nhiều người (thang 100, ma trận) | So tuổi cộng sự, vợ chồng |
| `luunhat` | Lưu nhật (từng ngày) và lưu thời (từng giờ), Bát tự + Tử vi | "Tháng này ngày nào thuận cho tôi", "giờ nào ký tốt" |
| `kiembai` | Tự kiểm bản luận: lời tuyệt đối, gieo sợ hãi, thiếu rào đón, dụng thần không nhất quán… | Bắt buộc trước khi gửi bản luận dài |

## Đã kiểm chứng
- **Vượng suy (`vuongsuy`).**
  - Thang A và thang B của lá số tự kiểm v2 (Kỷ Mão, Bính Tý, Mậu Ngọ, Đinh Tỵ) khớp với tính tay theo công thức.
  - 12 trường sinh, Đế vượng, vượng tướng hưu tù tử, ám hợp, củng hợp, lục phá: đúng bảng.
  - Cách cục: đúng các trường hợp Chính Tài (tháng Tý), Thương Quan (Ất sinh tháng Dần, Bính thấu), Kiến Lộc, Dương Nhận.
  - Chạy 3.000 tứ trụ ngẫu nhiên không lỗi.
- **Ảnh, vận thế, lưu nhật.**
  - Lá số dựng giống hệt `tvbt.tu_vi`: Mệnh tại Mùi, Thân tại Tỵ, Thổ Ngũ Cục ở lá số mẫu.
  - Đại vận lấy giống v2 (cùng hàm, cùng phép tính).
  - Cung tháng Giêng theo phép Đẩu Quân cùng công thức với `tvbt/docs/luan-chi-tiet.md`.
- **Hợp tác (`hoptac`).** Đúng bảng hợp, xung, hình, hại, phá, ngũ hợp. Điểm đối xứng giữa hai người. Nhận đúng thiên khắc địa xung.
- **Tự kiểm bản luận (`kiembai`).** Bài mẫu xấu bị xếp C hoặc D, bắt đủ 6 loại lỗi; bài mẫu tốt được A.
- **Rà soát độc lập.** Toàn bộ phần này đã được một lượt rà soát độc lập, tìm ra 5 lỗi nặng và 10 lỗi nhỏ. Tất cả đã được sửa và có ca thử riêng. Các lỗi đã sửa:
  - ngày lịch ghi "việc khác không nên" vẫn lọt vào nhóm chọn;
  - cảnh báo giao tiết và giờ Tý muộn không được in;
  - Kiến Lộc của can Mậu, Kỷ bị nhận sai;
  - còn báo củng hợp khi đã đủ tam hợp;
  - hội chẩn bị lệch ngày khi nhập ngày âm.

## Chạy
Tham số ngày giờ giống `tvbt.py`: `--ngay YYYY-MM-DD --gio HH:MM --gioi nam|nu --noi "<tỉnh>"`, cộng `--am`, `--nhuan`, `--kinhdo`, `--utc`, `--mien`, `--gio-dong-ho`, `--ty` khi cần. Mọi lệnh có `--help`.

```bash
python3 tvbt/nc.py vuongsuy --ngay 1990-05-17 --gio 08:30 --gioi nam --noi "Hà Nội"
python3 tvbt/nc.py anhtuvi  --ngay 1990-05-17 --gio 08:30 --gioi nam --noi "Hà Nội" --nam-xem 2026 --ten "An" --ra /tmp/an_tuvi.png
python3 tvbt/nc.py anhbattu --ngay 1990-05-17 --gio 08:30 --gioi nam --noi "Hà Nội" --ten "An" --ra /tmp/an_battu.png
python3 tvbt/nc.py vanthe   --ngay 1990-05-17 --gio 08:30 --gioi nam --noi "Hà Nội" --tu-nam 2020 --den-nam 2040 --dung "Kim+Thủy" --ky "Hỏa+Thổ" --ra /tmp/an_van.png
python3 tvbt/nc.py hoptac   --nguoi "An,1990-05-17,08:30,nam,Hà Nội" "Lan,1993-09-27,,nu" [--loai honnhan]
python3 tvbt/nc.py luunhat  --ngay 1990-05-17 --gio 08:30 --gioi nam --tu 2026-11-01 --den 2026-11-30 --dung "Kim+Thủy" --ky "Hỏa+Thổ"
python3 tvbt/nc.py luunhat  ... --ngay-xem 2026-11-12          # lưu thời 12 giờ
python3 tvbt/nc.py kiembai  --file /tmp/ban_luan.md
```

## Luận
Trình bày theo v2: (1) bảng số liệu, (2) luận theo mục, (3) lưu ý và độ chắc chắn. Không phán chắc chắn, không gieo sợ hãi, không quyết định y tế, tài chính, pháp lý thay người dùng.
Ảnh: gửi file PNG cho người dùng bằng công cụ gửi file, một dòng chú thích; không có PNG thì gửi file HTML cùng tên.

### 4.1 Vượng suy chấm điểm, cách cục Bát tự (lệnh `vuongsuy`)
**Khi nào chạy:** luôn chạy cùng phần Bát tự của v2, trước khi chọn dụng thần. Nếu có `tvbt/docs/luan-chi-tiet.md` thì vẫn làm theo quy trình dụng thần của skill đó.

**Đọc kết quả:**
- Hai thang chấm độc lập:
  - **Thang A** (đắc lệnh / đắc địa / đắc thế, có ngưỡng);
  - **Thang B** (đếm điểm ngũ hành, tỷ lệ "ta" so với tổng).
- Hai thang cùng chiều và cách xa ngưỡng: kết luận vượng/nhược với độ tin cao.
- Hai thang lệch nhau (script in `!`): bắt buộc nói "còn hai cách hiểu". Chọn một cách, có lý do (đắc lệnh, có gốc, hợp hóa…), và ưu tiên cách khớp với mốc đời thực.
- **Cách cục** (tàng can tháng thấu lên can, hoặc bản khí) cho biết cấu trúc lá số và nghề hợp:
  - Chính Quan: kỷ luật, quản lý;
  - Thực Thần: tay nghề, sáng tạo;
  - Thiên Tài: kinh doanh.
  - **Không lấy cách cục làm dụng thần.**
  - Kiến Lộc, Dương Nhận: thân thường vượng, ưa Quan Sát, Tài, Thực Thương.
  - Cách "tạp khí": độ tin thấp, nói rõ.
- **Quan hệ bổ sung:**
  - ám hợp: hợp ngầm, quan hệ kín;
  - củng hợp: chưa thành tam hợp, chờ năm hoặc vận có chi giữa;
  - cái đầu / tiệt cước: can và chi trong cùng một trụ khắc nhau, trụ đó yếu lực;
  - lục phá: hao, đổ vỡ nhỏ.

  Đây chỉ là yếu tố phụ.

### 4.2 Ảnh lá số và biểu đồ vận thế (lệnh `anhtuvi`, `anhbattu`, `vanthe`)
- **Mặc định khi lập lá số Tử vi hoặc Bát tự cho người dùng:** vẽ ảnh và gửi kèm.
  - Lệnh: `anhtuvi --nam-xem <năm> --ten "<tên>" --ra /tmp/<tên>_tuvi.png` và `anhbattu ... --ra /tmp/<tên>_battu.png`.
  - Gửi PNG bằng công cụ gửi file, kèm một dòng chú thích. Không có PNG thì gửi file HTML cùng tên.
- **Biểu đồ vận thế:** chạy sau khi đã chọn dụng thần, truyền `--dung` và `--ky` đúng như đã chọn.
  - Nếu không truyền, script dùng phù ức đơn giản và in `!`. Khi đó phải nói rõ là bản tạm.
  - Biểu đồ cho thấy **xu hướng** lên xuống giữa các năm, không phải cát hung tuyệt đối.
  - Khi viết, chỉ ra 2–3 năm đỉnh và 2–3 năm đáy, kèm căn cứ lấy từ cột căn cứ.
  - Bát tự và Tử vi ngược chiều nhau: nói rõ, không lặng lẽ bỏ một bên.

### 4.3 Hợp tác, hôn nhân (lệnh `hoptac`)
**Mỗi người một chuỗi:** `"Tên,YYYY-MM-DD,HH:MM,nam|nu"`. Ghi thêm `am` nếu là ngày âm, tên tỉnh nếu biết, và `dung=…,ky=…` nếu đã chọn dụng thần cho người đó.
- Không có giờ: để trống (`"Tên,1994-05-10,,nam"`).
- `--loai honnhan` để xét thêm sao phối ngẫu.

**Đọc kết quả** (thang 100: ≥ 75 rất hợp, 62–74 khá, 48–61 trung bình, dưới 48 cần cơ chế phối hợp rõ):
- Trụ ngày nặng nhất (35 điểm): cách làm việc và tính cách hằng ngày.
- Bổ trợ hành (25 điểm): người này mang đến hành người kia cần không.
- Vai trò theo thập thần:
  - Tài: mang cơ hội, tiền;
  - Ấn: nâng đỡ;
  - Tỷ Kiếp – Tỷ Kiếp: dễ tranh phần, cần chia quyền rõ.
- Thiên khắc địa xung: gợi ý không xếp chung một tuyến hằng ngày, nên có người trung gian.

Luôn nhắc: đây là tham khảo, không thay đánh giá năng lực, uy tín và hợp đồng rõ ràng. Không khuyên loại ai chỉ vì tuổi.

### 4.4 Lưu nhật, lưu thời (lệnh `luunhat`)
- **Dùng khi** người dùng hỏi "tháng này ngày nào thuận cho tôi" hoặc "giờ nào ký tốt". Truyền `--dung/--ky` đã chọn.
- **Lưu nhật là tầng nhỏ nhất:** chỉ dùng để chọn giữa những ngày đã ổn ở tầng năm, tháng, và đã qua lệnh `ngay` (lịch nên/kiêng). Không lấy lưu nhật để phán ngày xấu.
- **Cách tính cung ngày, cung giờ Tử vi:** theo phép Đẩu Quân, cùng mặc định với lưu nguyệt của `tvbt/docs/luan-chi-tiet.md`. Nhiều sách đếm từ cung tiểu hạn; nói rõ khi liên quan.

### 4.5 Tự kiểm bản luận trước khi gửi (lệnh `kiembai` và bảng 7 mục) – BẮT BUỘC với bản luận dài
1. Ghi bản luận ra file `.md`, chạy `python3 tvbt/nc.py kiembai --file <file>`, rồi sửa hết lỗi **[nặng]** và **[vừa]**. Chỉ gửi khi đạt hạng A hoặc B.
2. Tự rà 7 mục, chấm A–D. Mục nào dưới B thì sửa:
   1. Vượng suy, cách cục, dụng thần nhất quán với nhau và với bảng Cần / Thừa.
   2. Điều hậu khớp với kết luận (không tự thêm hành điều hậu vào dụng thần khi chưa đủ điều kiện).
   3. Mỗi kết luận có căn cứ trong ngoặc (sao gì, cung nào, can chi nào).
   4. Đã xét đại vận / đại hạn hiện tại, không chỉ lá số gốc.
   5. Trả lời đúng câu người dùng hỏi, đặt ở đầu.
   6. Không có lời tuyệt đối, cũng không nói nước đôi vô nghĩa. Năm cụ thể phải kèm lời rào đón.
   7. Có ghi độ chắc chắn. Nếu **chưa đối chiếu với mốc đời thực** của người xem, độ chắc tối đa là "trung bình".
3. Với Tử vi, kiểm thêm: Hóa Kỵ chồng tầng (gốc, đại hạn, lưu niên) phải ghi đúng cung. Kiểm ngược 3 kết luận chính bằng bảng số liệu.
4. Bản luận về giờ sinh chưa chắc chắn:
   - Giờ sinh sát ranh giới giờ âm lịch (≤ 15 phút, sau khi đã hiệu chỉnh giờ mặt trời): phải có 2 lá số và nói chọn bản nào.
   - Giờ sinh cách giờ giao tiết ≤ 30 phút: nói rằng trụ tháng (lệnh tháng) chưa chắc.

## Trường phái và giới hạn (nói rõ khi liên quan)
- **Vượng suy:** thang A theo bazi-enrich (MIT): đắc lệnh ±3–5, trường sinh, đắc địa theo tàng can, đắc thế; thang B đếm điểm (can 5; Tý Mão Dậu 8; Ngọ Hợi 5+3; chi khác 5/2/1; chi tháng tính 2 lần). Hai thang chỉ để tham khảo cho bước chọn dụng thần, không thay phán đoán.
  - Từ 11/2026 thang A xét **can âm theo hành như can dương cùng hành** (Ất như Giáp, Đinh như Bính, Kỷ như Mậu, Tân như Canh, Quý như Nhâm) khi cộng điểm trường sinh của nhật chủ ở tháng sinh – theo Trích Thiên Tủy (Nhậm Thiết Tiều chú) và cách xét theo hành ở `co-ban.md` 4.1.1. Bản bazi-enrich gốc dùng trường sinh nghịch cho can âm (Ất trường sinh ở Ngọ, tử ở Hợi…), làm thang A lệch khoảng 3 điểm so với thang B ở các tháng Ngọ, Hợi, Tý (can Ất), Dậu, Dần, Mão (Đinh, Kỷ), Tý, Tỵ (Tân), Mão, Thân, Dậu (Quý). Ví dụ 09/06/1990 12:00 Hà Nội (Ất Tỵ, tháng Ngọ): trước ra "trung hòa", nay ra "nhược", cùng chiều thang B. Phần 12 trường sinh khi luận (vd "Ất ở Ngọ là Trường sinh") vẫn ghi theo cách truyền thống, chỉ phép chấm điểm đổi.
  - Hỷ kỵ mặc định (khi không truyền `--dung/--ky` cho `vanthe`, `luunhat`, `hoptac`) là phù ức đơn giản. Khi cả hai thang cùng "cực vượng" hoặc cùng "cực nhược" (khoảng 4% lá số) script in `!` vì có thể là cách tòng / chuyên vượng, hỷ kỵ khi đó ngược với phù ức.
- **Cách cục Bát tự:** tháng Tý Ngọ Mão Dậu lấy bản khí; tháng khác lấy tàng can thấu (bỏ Tỷ Kiếp), không thấu thì lấy bản khí. Ám hợp chỉ xét bản khí. Bán hợp tính khi có chi giữa; củng hợp là cặp sinh–mộ.
- **Vận thế:** điểm là quy ước của skill (tham khảo Johnson-Jia, Apache-2.0), chỉ để thấy xu hướng.
- **Hợp tác:** thang điểm quy ước (tham khảo xuemian168, weizeW); hành cần/kỵ mặc định là phù ức đơn giản nếu không truyền.
- **Lưu nhật/lưu thời Tử vi:** phép Đẩu Quân (cùng `tvbt/docs/luan-chi-tiet.md`); lịch âm Việt Nam UTC+7.
- **Tự kiểm bản luận:** máy chỉ bắt được lỗi hình thức; bảng 7 mục vẫn phải tự rà.
