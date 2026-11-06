# Lục hào bốc dịch và hội chẩn ba môn (lệnh nc.py luchao, hoichan)

> Phần cài đặt và tự kiểm tra đã làm ở Bước 2 của SKILL.md (skill tu-vi-bat-tu-phong-thuy-v3). Mọi file đã có sẵn trong `tvbt/`; bỏ qua mọi chỗ nhắc tới "trích", "vá", "Bước 1/2 của skill v2" hay tên các skill cũ (v2, luan-la-so-chi-tiet, ky-mon-mo-rong, …) – nay tất cả là một bộ.

## Có gì
| Lệnh | Làm gì |
|---|---|
| `luchao` | Lập quẻ theo đồng xu / 6 số hào / thời gian / 2 số; bát cung, thế ứng, nạp giáp, lục thân, lục thần, phục thần, tuần không, nguyệt phá, ám động, nhật phá, hồi đầu sinh khắc, tiến/thoái thần, hóa không/phá/mộ/tuyệt, lục xung/lục hợp, dụng – nguyên – kỵ – cừu thần, ứng kỳ gợi ý |
| `hoichan` | Hội chẩn cùng một thời điểm: Lục hào + Mai hoa + Lục Nhâm (kèm phần Lục Nhâm nâng cao) |

## Đã kiểm chứng
- **Lục hào.**
  - Bát cung, thế ứng và nạp giáp được sinh bằng thuật toán:
    - 64 quẻ đủ, không trùng;
    - thế của 13 quẻ mẫu đúng;
    - 10 quẻ lục xung và 8 quẻ lục hợp đúng danh sách sách ghi (đoạn "何谓六冲卦" trong Tăng San);
    - nạp giáp 8 quẻ thuần đúng.
  - Lục thần khớp bảng 6×6 trong chương Lục thần của Tăng San.
  - Khớp 8 quẻ mẫu trong Tăng San Bốc Dịch (Truân biến Chấn, Bác biến Quan, Thăng, Bí, Tụy biến Bĩ, Đoài biến Tụng, Khốn biến Giải, Tỷ). Phần đã khớp: lục thân, chi, thế ứng, tuần không, phục thần, hóa tiến/thoái/không, nguyệt phá.
  - Khớp 1 quẻ có ngày giờ dương lịch đầy đủ (10/11/2013, 20:21).
  - Chạy 4.096 tổ hợp hào × 3 ngày không lỗi.
  - Rà soát 11/2026: khớp thư viện PyPI `najia` 2.0.1 (cài đặt độc lập) trên đủ 4.096 tổ hợp hào: cung, thế ứng, nạp giáp, lục thân quẻ chủ và quẻ biến, cung quẻ biến, phục thần, lục xung, lục hợp, du hồn, quy hồn; lục thần và tuần không khớp trên 60 can chi ngày. 0 lỗi.
- **Hội chẩn.** Ba phần đều dùng lại hàm đã kiểm chứng ở trên và của v2.

## Chạy
Tham số ngày giờ giống `tvbt.py`: `--ngay YYYY-MM-DD --gio HH:MM --gioi nam|nu --noi "<tỉnh>"`, cộng `--am`, `--nhuan`, `--kinhdo`, `--utc`, `--mien`, `--gio-dong-ho`, `--ty` khi cần. Mọi lệnh có `--help`.

```bash
python3 tvbt/nc.py luchao --ngay 2026-11-02 --gio 09:30 --noi "Hà Nội" --viec taichinh --xu SSN NNS SSS NSN NNN SNS
python3 tvbt/nc.py luchao --viec congviec          # lập theo giờ hỏi (bây giờ)
python3 tvbt/nc.py hoichan --viec taichinh --nam-sinh 1990 --gioi nam [--xu ...]
```

## Luận
Trình bày theo v2: (1) bảng số liệu, (2) luận theo mục, (3) lưu ý và độ chắc chắn. Không phán chắc chắn, không gieo sợ hãi, không quyết định y tế, tài chính, pháp lý thay người dùng. Chiêm việc: mỗi việc một lần lập; người dùng muốn gieo lại cùng việc thì nhắc nhẹ.

### 4.1 Lục hào – nạp giáp, bốc dịch (lệnh `luchao`)
**Khi nào dùng:** người dùng hỏi một việc cụ thể sắp xảy ra: tiền, việc làm, hôn nhân, sức khỏe, kiện tụng, đi xa, tìm đồ, thi cử. Mỗi lần hỏi một việc; cùng một việc thì không gieo lại nhiều lần.

**Lập quẻ:** `python3 tvbt/nc.py luchao --ngay YYYY-MM-DD --gio HH:MM [--noi tỉnh] --viec <việc> [--gioi nam|nu]`, thêm một trong các cách sau:
- `--xu SSN NNS SSS NSN NNN SNS`: người dùng tự gieo 3 đồng xu, 6 lần. Ghi từ lần 1 (hào 1, dưới cùng) đến lần 6.
  - N = ngửa (mặt chữ) = 3, S = sấp = 2. Người quen tính ngược lại thì thêm `--xu-dao`.
  - Phải hỏi người dùng theo quy ước nào.
- `--hao 7 8 8 6 9 8`: đã có sẵn 6 số (6 và 9 là hào động).
- `--so A B`: người dùng nghĩ ra 2 số, lập theo cách Mai hoa.
- Không có cả ba: lập theo giờ hỏi (cách Mai hoa); chỉ có 1 hào động.

Ngày giờ là lúc gieo quẻ, không phải ngày sinh. Từ 23h đã tính sang ngày hôm sau. Gặp dòng "! sát giờ giao tiết" thì nói rõ là tháng có thể khác.

Việc (`--viec`): taichinh, congviec, honnhan, suckhoe, kientung, dixa, timdo, thicu, giayto, concai, anhem, chung.
- Hỏi cho người khác thì tự chọn dụng thần bằng `--dung`: cha mẹ `phumau`, con `tuton`, vợ `thetai`, chồng `quanquy`, anh em `huynhde`, bản thân `the`, phía kia `ung`.
- Hỏi hôn nhân cần thêm `--gioi`.

**Đọc bảng theo thứ tự:**
1. **Dụng thần trước.** Bảng "DỤNG THẦN" chỉ hào đại diện cho việc hỏi. Không có trong quẻ thì lấy phục thần (hào ẩn). Thấy chưa đúng ý người hỏi thì hỏi lại rồi chạy với `--dung`.
2. **Dụng thần mạnh hay yếu** (xem cột "Trạng thái"):
   - Theo tháng: vượng, tướng là có sức; hưu, tù, tử là yếu. "Lâm nguyệt kiến" là rất mạnh.
   - Theo ngày: lâm nhật, nhật sinh, nhật phù là được giúp; nhật khắc là bị ép.
   - Tháng và ngày mạnh hơn mọi hào trong quẻ.
   - "Lực ước lượng" chỉ là điểm thô để tham khảo.
3. **Các điểm cần chú ý:**
   - Tuần không: việc chưa tới.
     - Không giả (hào động, vượng, được sinh): đến ngày xuất không là dùng được.
     - Chân không (hào suy, bị phá): khó.
   - Nguyệt phá: hào tạm mất sức; qua tháng, hoặc đến ngày gặp lại chính chi đó, thì có thể hồi.
   - Nhật phá: hào tĩnh, suy, bị nhật thần xung.
   - Ám động: hào tĩnh nhưng vượng, bị nhật thần xung, coi như đang động ngầm.
   - Nhập mộ, tuyệt: hào bị giam, bị cắt; đợi ngày xung mộ hoặc ngày được sinh.
4. **Nguyên thần, kỵ thần:**
   - Nguyên thần (sinh dụng thần) động và có sức là tốt.
   - Kỵ thần (khắc dụng thần) động và có sức là trở ngại.
   - Cừu thần động thì giúp kỵ thần.
   - Hào tĩnh có tác dụng yếu hơn hào động.
5. **Hào động biến ra gì:**
   - Hồi đầu sinh: được tiếp sức. Hồi đầu khắc: tự chuốc trở ngại.
   - Hóa tiến thần: việc tiến dần. Hóa thoái thần: việc lùi dần.
   - Phục ngâm (hóa ra cùng chi): trì trệ.
   - Phản ngâm (hóa ra chi xung): được rồi mất, lặp đi lặp lại.
   - Hóa không, hóa phá, hóa mộ, hóa tuyệt: kết quả còn trống hoặc yếu đi.
6. **Thế và Ứng:**
   - Thế là người hỏi, Ứng là phía kia.
   - Ứng sinh hoặc hợp Thế là thuận. Ứng khắc Thế là có cản trở.
   - Thế không vong: người hỏi còn lưỡng lự.
7. **Phục thần:**
   - Dễ hiện ra khi phục thần có sức, được tháng hoặc ngày sinh, hoặc phi thần (hào đè lên) bị không, bị phá, bị xung.
   - Phi thần khắc phục thần thì khó hiện.
8. **Đặc điểm cả quẻ** (chỉ là sắc thái chung, không thay cho dụng thần):
   - Lục xung: việc nhanh, dễ tan. Lục hợp: việc dễ hợp, có khi kéo dài.
   - Lục xung biến lục hợp: trước khó sau thành. Lục hợp biến lục xung: trước hợp sau tan.
   - Du hồn: lòng chưa yên. Quy hồn: quay về chỗ cũ.
9. **Lục thần** chỉ để tả thêm, không quyết định tốt xấu:
   - Thanh Long: vui, hỷ sự.
   - Chu Tước: lời nói, giấy tờ, thị phi.
   - Câu Trần: chậm, đất đai.
   - Đằng Xà: lo nghĩ, lắt léo.
   - Bạch Hổ: gấp, ốm đau, va chạm.
   - Huyền Vũ: mờ ám, mất mát.
10. **Ứng kỳ** (bảng gợi ý):
    - Hào động đợi ngày hợp hoặc ngày trị. Hào tĩnh đợi ngày xung.
    - Hào không vong đợi xuất không. Hào nguyệt phá đợi qua tháng.
    - Chỉ nói "có thể quanh khoảng…", nêu hai mốc gần nhất; không hứa ngày chắc chắn.

**Cách nói với người dùng:**
- Thứ tự: tên quẻ, việc hỏi, dụng thần → dụng thần mạnh hay yếu và vì sao → lời khuyên nên làm gì.
- Không nói "chắc chắn". Quẻ xấu thì nói nhẹ, chỉ ra chỗ còn cơ hội (nguyên thần, ứng kỳ).
- Hỏi sức khỏe: chỉ nói xu hướng và luôn khuyên đi khám.
- Kiện tụng hoặc tiền lớn: nhắc người dùng hỏi người có chuyên môn.

### 4.2 Hội chẩn ba môn (lệnh `hoichan`)
**Dùng khi** người dùng muốn xem một việc quan trọng bằng nhiều môn. Lệnh lập cùng một thời điểm: Lục hào (theo thời gian), Mai hoa, Đại Lục Nhâm (kèm phần bổ sung).

**Sau khi chạy, tự lập bảng đồng thuận:** mỗi môn chấm +1 (thuận) / 0 (lẫn lộn) / −1 (nghịch) cho câu hỏi, kèm một dòng căn cứ.
- Lục hào: dụng thần vượng hay suy, có được nguyên thần sinh không, có bị kỵ thần khắc không.
- Mai hoa: quan hệ thể – dụng ở quẻ chủ, hỗ, biến.
- Lục Nhâm: mạt truyền sinh hay khắc can ngày, thiên tướng ở sơ truyền.

**Kết luận:**
- Ba môn cùng chiều: độ tin cao.
- Hai môn cùng chiều: nghiêng theo đa số, nêu môn ngược và lý do.
- Mỗi môn một chiều: nói rõ là chưa rõ ràng, không ép kết luận.

## Trường phái và giới hạn (nói rõ khi liên quan)
**Lục hào**
- Theo hệ Kinh Phòng – Hỏa Châu Lâm – Tăng San Bốc Dịch.
- Bát cung, thế ứng và nạp giáp do thuật toán sinh ra, rồi đối chiếu với bảng chuẩn và quẻ mẫu trong sách.
- Lục thần: Giáp Ất khởi Thanh Long; Bính Đinh khởi Chu Tước; Mậu khởi Câu Trần; Kỷ khởi Đằng Xà; Canh Tân khởi Bạch Hổ; Nhâm Quý khởi Huyền Vũ.
  - Cách này theo bảng trong chương Lục thần của Tăng San.
  - Bản điện tử đã đối chiếu có hai ví dụ in Câu Trần và Đằng Xà đổi chỗ cho nhau.
- Hành Thổ tính trường sinh theo Thủy: sinh ở Thân, mộ ở Thìn.
- Đồng xu: mặc định ngửa (mặt chữ) = 3. Hỏa Châu Lâm lấy mặt lưng là dương, nên có thêm tùy chọn `--xu-dao`.
- Dụng thần lưỡng hiện (hai hào cùng loại), từ 11/2026 chọn theo cổ pháp chương Lưỡng hiện 32 của Tăng San Bốc Dịch (đã đọc nguyên văn): bỏ hưu tù lấy vượng tướng, bỏ tĩnh lấy động, bỏ nguyệt phá, bỏ tuần không, bỏ hào bị thương.
  - Script tính năm tiêu chí ngang nhau. Nếu hòa thì lấy hào động, rồi hào trì thế/ứng, rồi hào có lực cao hơn.
  - Dã Hạc ghi thêm từ kinh nghiệm: ứng kỳ hay rơi vào hào tuần không / nguyệt phá. Vì vậy, khi có hào như thế, script nhắc xem cả thời điểm hào đó xuất không hoặc thực phá.
  - Đã kiểm bằng hai quẻ mẫu trong chương: Tiểu Súc (tháng Mùi, ngày Canh Tý) và Sư hóa Hoán (tháng Mùi, ngày Giáp Ngọ).
- Phản ngâm là hào hóa ra chi xung; phục ngâm là hào hóa ra cùng chi. Phản ngâm theo phương vị chỉ ghi nhẹ.
- Lập theo giờ hoặc theo số thì chỉ có 1 hào động.
- "Lực ước lượng" là điểm thô do script đặt, không có trong sách.
- Chưa tính: hình, hại, tam hợp cục, độc phát, loạn động, thần sát, quái thân.
- Ứng kỳ chỉ là gợi ý.

**Hội chẩn**
- Mai hoa lập theo thời gian như v2.
- Lục hào lập theo thời gian trừ khi người dùng gieo xu.
- Kỳ môn không đưa vào lệnh này, vì có skill vá riêng; muốn thì lập thêm bằng lệnh của v2.
