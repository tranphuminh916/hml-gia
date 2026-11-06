# Luận lá số chi tiết: dụng thần, lưu niên, lưu nguyệt, vận hạn nhiều năm, hợp tuổi (lệnh hoptuoi), cấu trúc bản luận

> Phần cài đặt và tự kiểm tra đã làm ở Bước 2 của SKILL.md (skill tu-vi-bat-tu-phong-thuy-v3). Mọi file đã có sẵn trong `tvbt/`; bỏ qua mọi chỗ nhắc tới "trích", "vá", "Bước 1/2 của skill v2" hay tên các skill cũ (v2, luan-la-so-chi-tiet, ky-mon-mo-rong, …) – nay tất cả là một bộ.

## Vì sao có phần này (lỗi đã gặp khi luận thật)
- **Dụng thần.** Hướng dẫn cũ "sinh mùa hạ cần Thủy" đã khiến Claude chọn Thủy làm dụng thần cho người Đinh Hỏa sinh tháng Mùi, trong khi Ấn (Mộc) đã thừa. Như vậy là sai, vì Thủy sinh thêm cho Mộc. Mục 4.1 thêm bước kiểm tra chuỗi sinh.
- **Luận một chiều.** Phần luận năm chỉ nêu mặt xấu, bỏ sót Hóa Lộc, Hóa Quyền lưu niên. Mục 4.5 thêm bảng kiểm từng năm, từng tháng.
- **Thiếu dữ liệu.** v2 không có lưu nguyệt, không có vận hạn nhiều năm, không tự tìm hợp/xung/hình/hại, không so tuổi người khác. Vì vậy bản luận kém chi tiết hơn bản luận mẫu. Script đã được thêm các phần này.

## Đã kiểm chứng
- **Không làm hỏng v2.** Sau khi vá, tự kiểm tra của v2 vẫn ĐẠT. Chạy 150 lá số ngẫu nhiên năm 1950–2015 (có miền Nam 1955–1975 và năm âm lịch có tháng nhuận): mọi dòng v2 in ra vẫn giữ nguyên, trừ những bảng được thêm cột. Không có lỗi.
- **Lưu nguyệt và vận hạn nhiều năm.** Đối chiếu với một bản luận độc lập cho một lá số mẫu:
  - lưu nguyệt Tử vi khớp đủ 24 tháng của năm 2025 (có tháng 6 nhuận) và 2026: cung tháng, tứ hóa tháng, các chỗ "Hóa Kỵ lặp hai lần";
  - vận hạn 2028–2035 khớp cả 8 năm: tiểu hạn, sao lưu, tứ hóa.
- **Hợp tuổi.** Trụ ngày của 5 người khớp bản luận đối chiếu, khớp cả các cặp thiên khắc địa xung.
- **Quan hệ can chi** theo đúng bảng ở mục 4.1.4 của v2: lục hợp, lục xung, hình, hại, bán hợp, tam hợp, tam hội, ngũ hợp, can xung.

## Chạy

```bash
# Lá số đầy đủ để luận cả đời (năm nay = 2026)
python3 tvbt/tvbt.py tatca --ngay 1990-05-17 --gio 08:30 --gioi nam --noi "Hà Nội" --nam-xem 2026 --phi-hoa --luu-nien 10 --so-nam 10 --luu-nguyet
# Lưu nguyệt của năm trước / năm sau (chỉ cần hai bảng LƯU NGUYỆT và phần VẬN HẠN)
python3 tvbt/tvbt.py battu tuvi --ngay 1990-05-17 --gio 08:30 --gioi nam --noi "Hà Nội" --nam-xem 2027 --luu-nguyet --luu-nien 1
# So tuổi cộng sự (mặc định ngày dương lịch; thêm "am" nếu là ngày âm; có giờ thì ghi HH:MM)
python3 tvbt/tvbt.py hoptuoi --ngay 1990-05-17 --gio 08:30 --gioi nam --noi "Hà Nội" --nguoi "Anh Hùng:1979-02-11" "Chị Lan:1988-06-20 am" "Em Nam:1995-10-03 08:30"
```

Tham số mới:
- `--luu-nguyet` in hai bảng:
  - **LƯU NGUYỆT BÁT TỰ**: 12 tháng tiết khí tính từ Lập Xuân của năm `--nam-xem`, có ngày đổi tháng, thập thần, và quan hệ với tứ trụ, đại vận, năm;
  - **LƯU NGUYỆT TỬ VI**: các tháng âm lịch của năm âm `--nam-xem` (có cả tháng nhuận), gồm khoảng ngày dương, can chi tháng, cung tháng, tứ hóa tháng, và can chi tháng tiết khí vào giữa tháng. Trong cột tứ hóa, sao trùng với tứ hóa gốc ghi "gốc …", trùng với tứ hóa năm ghi "năm …".
- `--so-nam K`: bảng vận hạn Tử vi gọn cho K năm, tính từ `--nam-xem`.
- `--luu-nien K` (đã có trong v2): nay thêm cột tuổi mụ, đại vận đang chạy, và quan hệ với tứ trụ + đại vận.
- `hoptuoi --nguoi "Tên:YYYY-MM-DD [HH:MM] [am|amnhuan]"`: tứ trụ của từng người; họ là thập thần gì với đương số; ngũ hành nổi trội; quan hệ trụ năm, trụ ngày, quan hệ chéo. Có từ hai người trở lên thì in thêm quan hệ giữa họ với nhau (đánh dấu THIÊN KHẮC ĐỊA XUNG).

In thêm tự động, không cần tham số:
- dòng **Đắc lệnh / Đắc địa / Đắc thế** (liệt kê căn cứ để xét vượng nhược);
- gợi ý **điều hậu** khi sinh mùa hạ hoặc mùa đông;
- **quan hệ trong tứ trụ**;
- cột **quan hệ** của đại vận;
- **tứ hóa đại hạn** (theo can cung đại hạn), và ghi chú "gốc cũng Hóa …" cho tứ hóa lưu niên.

## Luận

### 4.0 Chuẩn bị
- Khi người dùng muốn luận chi tiết, hỏi thêm một lượt (không bắt buộc):
  - 3–5 mốc đời thực đã qua, như năm lập gia đình, có con, đổi việc lớn, biến cố tiền bạc hay sức khỏe;
  - bản luận hoặc buổi xem thầy trước đó, nếu có.
- Khi giờ sinh có hai phương án (sát ranh giới, giờ Tý muộn), dùng các mốc đời thực để chọn lá số. Ghi rõ đã chọn bản nào và vì sao.
- Có bản luận khác: đối chiếu từng ý trong một bảng (✅ khớp / ❌ lệch), nói lý do lệch: khác trường phái, khác dụng thần, hay một bên sai.

### 4.1 Dụng thần – làm đủ các bước, theo thứ tự
1. **Vượng hay nhược.** Dùng ba dòng Đắc lệnh / Đắc địa / Đắc thế mà script in ra.
   - Với tháng tứ quý, phải xét dư khí: Thìn còn Ất Mộc, Mùi còn Đinh Hỏa, Tuất còn Tân Kim (và Đinh), Sửu còn Quý Thủy.
   - Script ghi "HƯU" cho Hỏa sinh tháng Mùi, nhưng Hỏa vẫn còn dư khí ở Mùi.
2. **Tìm nguyên nhân.** Thân vượng vì Ấn thừa hay vì Tỷ Kiếp thừa? Thân nhược vì Tài, vì Quan Sát hay vì Thực Thương quá nhiều?
3. **Chọn theo phù ức:**

   | Tình trạng | Dụng / hỷ | Kỵ |
   |---|---|---|
   | Thân vượng do **Ấn thừa** | Tài (khắc Ấn) là chính; Thực Thương (tiết khí) | Ấn, Tỷ Kiếp; Quan Sát thường là kỵ hoặc trung tính vì sinh Ấn |
   | Thân vượng do **Tỷ Kiếp thừa** | Quan Sát (chế), Thực Thương (tiết), Tài | Tỷ Kiếp, Ấn |
   | Thân nhược do **Tài nhiều** | Tỷ Kiếp, rồi Ấn | Tài, Thực Thương |
   | Thân nhược do **Quan Sát nhiều** | Ấn (hóa Sát) là chính; Tỷ Kiếp | Tài (sinh Sát), Quan Sát |
   | Thân nhược do **Thực Thương nhiều** | Ấn (chế Thực Thương); Tỷ Kiếp | Tài, Thực Thương |

4. **Kiểm tra chuỗi sinh.** Với mỗi hành định xếp vào dụng/hỷ, hỏi: hành này có sinh cho hành đang thừa không? Nếu có thì không được xếp vào dụng, cùng lắm là trung tính, trừ khi có hành khác chặn ở giữa.
   - Ví dụ: Đinh Hỏa sinh tháng Mùi, Ấn (Mộc) thừa. Thủy (Quan Sát) sinh Mộc, nên Thủy không phải dụng thần dù sinh mùa hạ. Dụng thần là Kim (Tài) và Thổ (Thực Thương).
5. **Điều hậu** chỉ được đặt lên trên phù ức khi đủ cả ba điều kiện:
   - sinh giữa mùa cực (Tỵ, Ngọ cho mùa hạ; Hợi, Tý cho mùa đông);
   - lá số thiếu hẳn hành điều hậu;
   - hành điều hậu không sinh cho hành đang thừa.

   Với tháng tứ quý, điều hậu chỉ là yếu tố phụ.
6. **Thông quan.** Hai hành mạnh ngang nhau đang khắc nhau (ví dụ Kim và Mộc) thì hành đứng giữa (Thủy) là dụng.
7. **Cách cục đặc biệt** (tòng, hóa, chuyên vượng): như v2. Chỉ kết luận khi đủ điều kiện rõ ràng.
8. **Ghi bảng Cần / Thừa / Trung tính** ở đầu bản luận. Mọi gợi ý thực tế (màu, hướng, giờ, tháng hay tuổi của cộng sự, ngành nghề, tạng phủ) phải suy ra từ đúng bảng này, theo mục 4.2.
   - Không lấy gợi ý từ nạp âm. Nạp âm (ví dụ Lư Trung Hỏa) chỉ để tham khảo; khi mâu thuẫn với dụng thần thì theo dụng thần và nói rõ.
9. **Khi chưa chắc.** Nếu dụng thần có hai cách hiểu đều có lý, nêu cả hai, chọn một và giải thích vì sao. Ưu tiên cách khớp với các mốc đời thực đã biết.

### 4.2 Bảng ứng dụng ngũ hành

| Hành | Màu | Hướng | Giờ | Tháng âm | Nhóm tuổi hợp thành cục | Ngành hay xếp | Tạng phủ (Đông y) |
|---|---|---|---|---|---|---|---|
| Mộc | xanh lá | Đông, Đông Nam | Dần, Mão (3–7h) | 1, 2 | Hợi Mão Mùi | gỗ, giấy, nông lâm, giáo dục, dệt may | gan, mật, gân, mắt |
| Hỏa | đỏ, hồng, tím | Nam | Tỵ, Ngọ (9–13h) | 4, 5 | Dần Ngọ Tuất | điện, năng lượng, ăn uống, truyền thông, làm đẹp | tim, ruột non, mạch máu, huyết áp |
| Thổ | vàng, nâu, be | Đông Bắc, Tây Nam, trung tâm | Thìn (7–9h), Mùi (13–15h), Tuất (19–21h), Sửu (1–3h) | 3, 6, 9, 12 | Thìn Tuất Sửu Mùi | bất động sản, xây dựng, kho bãi, nông sản, khoáng sản | dạ dày, lá lách, tiêu hóa, cơ |
| Kim | trắng, bạc, xám | Tây, Tây Bắc | Thân, Dậu (15–19h) | 7, 8 | Tỵ Dậu Sửu | tài chính, ngân hàng, kim loại, máy móc, xe cộ | phổi, đại tràng, da, hô hấp |
| Thủy | đen, xanh dương | Bắc | Hợi, Tý (21–1h) | 10, 11 | Thân Tý Thìn | vận tải, logistics, thương mại, du lịch, nước, thủy sản | thận, bàng quang, tai, tiết niệu |

- Ngành nghề mỗi sách xếp một khác. Ví dụ vận tải có sách xếp Thủy (lưu thông), có sách xếp Hỏa hoặc Kim (xe, động cơ). Khi dùng, nói rõ cách xếp.
- Hướng theo ngũ hành (bảng này) và hướng theo Bát trạch (cung phi của v2) là hai cách khác nhau. Nêu cả hai, nói chỗ trùng, chỗ khác.

### 4.3 Lục thân và ý nghĩa cung

**Bát tự:**

| Người | Nam | Nữ |
|---|---|---|
| Cha | Thiên Tài | Thiên Tài |
| Mẹ | Chính Ấn (Thiên Ấn: mẹ kế, dì, người đỡ đầu) | Chính Ấn |
| Vợ / chồng | Chính Tài (Thiên Tài: người tình) | Chính Quan (Thất Sát: người tình) |
| Con | Quan Sát | Thực Thần, Thương Quan |
| Anh em, người ngang hàng | Tỷ Kiên, Kiếp Tài | Tỷ Kiên, Kiếp Tài |

- Mỗi trụ ứng với một giai đoạn và một nhóm người:
  - trụ năm: tổ nghiệp, ông bà, tuổi nhỏ;
  - trụ tháng: cha mẹ, anh em, tuổi thanh niên;
  - chi ngày: vợ/chồng (cung phối);
  - trụ giờ: con cái, hậu vận.
- Sao vợ/chồng là dụng thần thì người phối ngẫu giúp mình.
- Chi ngày bị hình hoặc xung (trong tứ trụ, hoặc do đại vận, lưu niên) là mốc hôn nhân dễ căng. Xem cột "Quan hệ" để tìm những năm như vậy.

**Tử vi:**
- Thái Dương đại diện cha, chồng, nam giới. Thái Âm đại diện mẹ, vợ, nữ giới.
- Sao đại diện đóng ở cung nào thì người đó gắn với chủ đề của cung ấy. Ví dụ Thái Dương ở Tật Ách: sức khỏe của cha cần quan tâm.

Khi viết cho người không chuyên, lần đầu nhắc đến cung thì ghi tên dễ hiểu kèm tên gốc:

| Tên gốc | Tên dễ hiểu |
|---|---|
| Mệnh | cung bản thân |
| Phụ Mẫu | cung Cha mẹ (cả bề trên, giấy tờ) |
| Phúc Đức | cung Phúc đức (tinh thần, họ hàng) |
| Điền Trạch | cung Nhà đất |
| Quan Lộc | cung Công việc |
| Nô Bộc | cung Bạn bè – người dưới (nhân viên, đối tác) |
| Thiên Di | cung Ra ngoài (đi xa, khách bên ngoài) |
| Tật Ách | cung Sức khỏe |
| Tài Bạch | cung Tiền bạc |
| Tử Tức | cung Con (phái phi hóa xem thêm: hợp tác, cổ đông) |
| Phu Thê | cung Vợ chồng |
| Huynh Đệ | cung Anh em (người ngang hàng, người góp vốn ngang hàng) |

### 4.4 Sức khỏe
- **Theo Bát tự:** hành quá thừa, và hành bị khắc quá mức, ứng với tạng phủ trong bảng 4.2. Ví dụ Hỏa thừa và Kim bị Hỏa khắc: tim, huyết áp, cùng phổi, đại tràng.
- **Theo Tử vi:** xem sao ở Tật Ách. Theo cách hiểu phổ biến:
  - Cự Môn: miệng, đường ăn uống, tiêu hóa;
  - Thái Dương: mắt, đầu, huyết áp;
  - Thái Âm: thận, nội tiết;
  - Liêm Trinh: máu, mạch;
  - Thiên Cơ: gan, thần kinh;
  - Vũ Khúc: phổi, hô hấp;
  - Thiên Hình: dao kéo, phẫu thuật nhỏ;
  - Kình, Đà: va chạm, chấn thương.
- **Năm cần để ý** khi có một trong các dấu hiệu:
  - tiểu hạn, Lưu Thái Tuế hoặc Lưu Bạch Hổ vào Tật Ách;
  - Hóa Kỵ lưu niên rơi vào sao ở Tật Ách;
  - Bát tự: năm xung trụ ngày, hoặc năm làm hành kỵ thành tam hợp, tam hội.
- Ưu tiên những điểm mà hai môn cùng chỉ. Luôn ghi "góc nhìn cổ học, không thay cho khám bệnh". Không chẩn đoán bệnh.

### 4.5 Luận từng năm, từng tháng – bảng kiểm (tránh luận một chiều)
Mỗi năm phải đi đủ các bước dưới đây, ghi **cả mặt tốt lẫn mặt xấu**:
1. **Tử vi – hạn và sao lưu.** Cung tiểu hạn và sao gốc của cung đó. Lưu Thái Tuế ở cung nào. Các sao lưu ở cung nào:
   - Lộc Tồn: lộc;
   - Kình Dương, Đà La: tranh chấp, trì trệ;
   - Thiên Mã: đi lại;
   - Tang Môn, Bạch Hổ: tang, bệnh, va chạm;
   - Thiên Khốc, Thiên Hư: buồn phiền.
2. **Tứ hóa lưu niên – đủ cả bốn** (Lộc, Quyền, Khoa, Kỵ). Đọc ghi chú "gốc cũng Hóa …" mà script in ra:
   - Kỵ chồng lên Kỵ gốc là nặng (bản luận gọi là "Hóa Kỵ lặp hai lần");
   - Hóa Lộc lưu rơi vào sao có Kỵ gốc thì giải được một phần;
   - Lộc chồng Lộc thì lộc rõ.
3. **Tứ hóa đại hạn** (script in sẵn): cho biết bối cảnh của cả 10 năm.
4. **Bát tự:**
   - Can chi năm là thập thần gì, thuộc dụng hay kỵ theo bảng Cần / Thừa.
   - Đọc cột "Quan hệ":
     - xung, hình chi ngày → bản thân, hôn nhân;
     - xung chi tháng → nhà cửa, cha mẹ, anh em;
     - xung chi giờ → con cái, cấp dưới;
     - xung chi năm → gốc gác, chỗ ở, đi xa.
   - Thành đủ tam hợp hoặc tam hội: nếu ra hành kỵ thì năm nặng; nếu ra hành dụng thì năm tốt.
5. **Chấm điểm.** Chọn một mức: Tốt nhất / Rất tốt / Tốt / Khá / Trung bình / Cần thận trọng / Kém. Viết một câu tổng, rồi một bảng theo mảng: Bản thân, Tiền bạc, Công việc, Vợ/chồng, Con, Cha mẹ, Nhân sự – đối tác, Sức khỏe. Mỗi ô kèm lý do trong ngoặc.
6. **Khi hai môn ngược nhau**, nói rõ (ví dụ "Tử vi tốt, Bát tự xấu") và chấm ở mức giữa. Không lặng lẽ bỏ một bên.

**Từng tháng:**
- Tử vi: dùng bảng LƯU NGUYỆT TỬ VI (cung tháng, tứ hóa tháng; ghi chú "năm …" là sao trùng tứ hóa năm, nên tác động mạnh hơn).
- Bát tự: dùng cột "Bát tự giữa tháng", hoặc bảng LƯU NGUYỆT BÁT TỰ. Tháng tiết khí đổi vào khoảng ngày 4–8 dương lịch, lệch khoảng nửa tháng so với tháng âm.
- Ghi tháng âm kèm khoảng ngày dương. Tháng đã qua thì đánh dấu "Đã qua", viết ngắn để người dùng đối chiếu. Năm đã qua có thể gộp theo quý.

### 4.6 Hợp tuổi, cộng sự (lệnh `hoptuoi`)
Đọc theo thứ tự:
1. **Ngũ hành.** Hành Nhật chủ và ngũ hành nổi của người kia có nằm trong bảng Cần của đương số không. Ví dụ lá số gần như toàn Kim mang Kim đến cho người cần Kim.
2. **Thập thần** – cột "Họ là gì với đương số":

   | Thập thần | Ý nghĩa với đương số |
   |---|---|
   | Tài | người mang tiền, cơ hội |
   | Ấn | người nâng đỡ, cố vấn |
   | Tỷ Kiếp | người ngang hàng, dễ tranh phần |
   | Quan Sát | người quản lý, tạo kỷ luật hoặc áp lực |
   | Thực Thương | người mình dìu dắt, người làm ra sản phẩm |

3. **Trụ ngày:** hợp, xung, hình, hại → cách làm việc hằng ngày, tính cách.
4. **Trụ năm:** gốc gác, đại cục.
5. **Quan hệ chéo** giữa các trụ khác.

Giữa các thành viên với nhau:
- Thiên khắc địa xung ở trụ ngày → không xếp chung một tuyến, nên có người trung gian.
- Gợi ý vai theo hành và thập thần: Kim → tài chính, kiểm soát; Thổ → vận hành, kho; Thủy → đối ngoại, giao thương; Hỏa → truyền thông, bán hàng; Mộc → phát triển, đào tạo.
- Đây chỉ là tham khảo, không thay việc đánh giá năng lực thực tế. Không khuyên loại ai chỉ vì tuổi.

**Hình mẫu cộng sự hợp:** tháng sinh âm lịch, năm sinh, can chi trụ ngày mang hành dụng thần (tra bảng 4.2). Tránh tháng và năm thuộc hành kỵ.

### 4.7 Cấu trúc bản luận "chi tiết cuộc đời"
Bản luận dài là thứ người dùng giữ lại, nên làm thành **tài liệu**: dùng loại Docs nếu phiên có; không có thì làm file. Trong chat chỉ tóm tắt vài dòng. Thứ tự các mục:
1. **Tóm tắt** 2–3 câu: cả đời, cộng với năm nay và năm sau.
2. **Thông tin lá số** (bảng): ngày giờ sinh; nơi sinh dùng để tính; giờ đã chọn và lý do; Tử vi tóm tắt; Bát tự tóm tắt; bảng Cần / Thừa.
3. **Con người:** điểm mạnh, điểm cần lưu ý.
4. **Công việc và tiền bạc:** ngành hợp, cách kiếm, cách giữ, phát sớm hay muộn.
5. **Gia đình:** cha mẹ, anh em và người ngang hàng, vợ/chồng, con.
6. **Sức khỏe**, kèm các năm cần để ý.
7. **Hành trình đã qua:** bảng theo chặng 10 năm, gộp đại hạn Tử vi và đại vận Bát tự. Hai môn chia mốc khác nhau, ghi cả hai.
8. **Năm trước, năm nay, năm sau:** mỗi năm có đánh giá, bảng theo mảng, và bảng từng tháng (tháng âm, ngày dương, đánh giá, lý do).
9. **Tương lai:** bảng các giai đoạn lớn đến cuối đời, và bảng từng năm cho 8–10 năm tới.
10. **Hợp tác** (nếu có ngày sinh của người khác).
11. **Đối chiếu** với bản luận hoặc buổi xem thầy trước (nếu có).
12. **Gợi ý nên làm:** đánh số, mỗi gợi ý kèm lý do.
13. **Những thứ hợp:** màu, hướng, giờ, tháng và con giáp, ngành nghề. Tất cả lấy từ bảng Cần / Thừa.
14. **Lưu ý:** giờ và nơi sinh đã dùng; các phái riêng đã dùng (phi hóa, Đẩu Quân); tính chất tham khảo.

Văn phong:
- Lời thường, câu ngắn.
- Thuật ngữ lần đầu kèm giải nghĩa ngắn, ví dụ: Hóa Lộc = thuận, có lộc; Hóa Quyền = nắm quyền; Hóa Khoa = có tiếng, được giúp; Hóa Kỵ = vướng mắc.
- Mọi nhận định kèm lý do trong ngoặc.
- Không gieo sợ hãi: sao hung viết thành "cần lưu ý".

## Trường phái (nói rõ khi liên quan)
- **Nguyệt hạn Tử vi – hai phép, script in cả hai cột.**
  - **Đẩu Quân** (lưu nguyệt Thái Tuế): từ cung Lưu Thái Tuế đếm nghịch đến tháng sinh, rồi đếm thuận đến giờ sinh, được cung tháng Giêng. Sách cổ coi đây là phần "ngoại" – việc từ bên ngoài đến.
  - **Tính từ tiểu hạn** (lưu nguyệt tiểu hạn): đếm như trên nhưng khởi từ cung tiểu hạn. Đây là phép tuvi.vn và nhiều sách Việt Nam dùng (nhãn "Th.1 … Th.12" trên lá số tuvi.vn); sách cổ coi là phần "nội" – vận của bản thân.
  - Tứ hóa tháng (theo can tháng) giống nhau ở hai phép; chỉ cung tháng khác.
  - Khi luận tháng: người dùng đối chiếu với tuvi.vn hoặc sách Việt Nam thì lấy cột tiểu hạn làm chính; không nói gì thì luận theo cột tiểu hạn và nhắc một dòng rằng phép Đẩu Quân cho cung khác. Lưu nhật/lưu thời (`nc.py luunhat`) vẫn theo Đẩu Quân.
- **Cung đại vận, cung lưu niên** (nhãn "ĐV." và "LN." trên lá số tuvi.vn): lấy cung đại hạn (hoặc tiểu hạn) làm Mệnh rồi đặt 12 tên cung đi thuận. Script in đủ 12 cung trong phần VẬN HẠN.
- **Sao lưu thêm** (từ 11/2026): Lưu Khôi, Lưu Việt (theo can năm xem, cùng bảng Khôi Việt), Lưu Văn Xương, Lưu Văn Khúc (theo can năm xem), Lưu Đào Hoa, Lưu Hồng Loan, Lưu Thiên Hỷ, Lưu Kiếp Sát (theo chi năm xem). Đã khớp với các sao "L." trên lá số tuvi.vn năm Quý Mão.
- **Tháng nhuận** dùng cùng can chi, cùng cung với tháng chính. Có phái chia đôi tháng nhuận.
- **Tứ hóa đại hạn** theo can của cung đại hạn. Phái phi hóa dùng nhiều; phái tam hợp truyền thống ít dùng.
- **Đại vận Bát tự.** Cách đọc phổ biến: can chủ 5 năm đầu, chi chủ 5 năm sau. Có phái xét cả 10 năm cùng lúc.
- **Bán hợp** chỉ tính cặp có chi ở giữa (Tý, Ngọ, Mão, Dậu); không tính "củng hợp" (cặp sinh – mộ). **Hình** ba ngôi (Dần–Tỵ–Thân, Sửu–Tuất–Mùi) được tính theo từng cặp.

## Giới hạn
- `hoptuoi` tính theo giờ đồng hồ, không dùng giờ mặt trời thực. Người sinh trước 1975 được giả định theo giờ miền Bắc. Không có giờ sinh thì chỉ có 3 trụ; ngày giao tiết thì script cảnh báo. Người sinh 23h–24h: trụ ngày theo `--ty` của đương số (mặc định đã sang ngày mới), giống `battu` và `nc.py hoptac`.
- Ngày đổi tháng trong lưu nguyệt Bát tự tính theo 12h trưa giờ Bắc Kinh, có thể lệch 1 ngày.
- Chưa tính sao lưu theo tháng (Kình, Đà… của tháng). Lưu nhật, lưu thời có ở `nc.py luunhat` (`tu-vi-nang-cao.md`).
- Chỉ so tuổi khi người dùng tự đưa ngày sinh của người kia.
