# Huyền không nâng cao (lệnh nc.py huyenkhong)

> Phần cài đặt và tự kiểm tra đã làm ở Bước 2 của SKILL.md (skill tu-vi-bat-tu-phong-thuy-v3). Mọi file đã có sẵn trong `tvbt/`; bỏ qua mọi chỗ nhắc tới "trích", "vá", "Bước 1/2 của skill v2" hay tên các skill cũ (v2, luan-la-so-chi-tiet, ky-mon-mo-rong, …) – nay tất cả là một bộ.

## Có gì
| Lệnh | Làm gì |
|---|---|
| `huyenkhong` | Hạ quái và thế quái, không vong, 4 cục, phục/phản ngâm, hợp thập, liên châu, tam ban, thất tinh đả kiếp, nhập tù, thành môn, cặp sao 9 cung, lưu niên/lưu nguyệt, đối chiếu sơn thủy thật |

## Đã kiểm chứng
- **Huyền không.**
  - Bàn hạ quái khớp v2 trên 24 sơn × 9 vận.
  - Thế quái khớp 8 bàn đã công bố từ 6 nguồn: vận 8 Tý sơn Ngọ hướng kiêm Quý Đinh, Nhâm sơn Bính hướng kiêm Tý Ngọ / Hợi Tỵ, Giáp sơn Canh hướng kiêm Dần Thân…
  - Thành môn khớp 6 ví dụ.
  - Thất tinh đả kiếp ra đủ 21 cục chân đả kiếp ở cung Ly.
  - Hợp thập toàn bàn khớp 24 cục.
  - Niên tinh 2024–2027 đúng.
  - Chạy 360° × 9 vận không lỗi.
  - Rà soát 11/2026: hạ quái và thế quái khớp hai bản cài đặt độc lập (voidforall/fengshui.skill theo bảng thay sao Thẩm thị; kth2/hidefate `independent_xuankong.py`, phương án sao 5 không thay) trên 9 vận × 24 sơn × 5 độ lệch (2.160 bàn); 4 cục, phục/phản ngâm, hợp thập, liên châu, phụ mẫu tam ban khớp; niên tinh 1864–2100 và nguyệt tinh 1900–2100 khớp. Sao 5 ở tọa/hướng: lấy âm dương của chính sơn tọa/hướng hay của sơn cùng nguyên long ở cung số vận đều cho cùng kết quả (cung có sao 5 luôn cùng chẵn lẻ với số vận).

## Chạy
Tham số ngày giờ giống `tvbt.py`: `--ngay YYYY-MM-DD --gio HH:MM --gioi nam|nu --noi "<tỉnh>"`, cộng `--am`, `--nhuan`, `--kinhdo`, `--utc`, `--mien`, `--gio-dong-ho`, `--ty` khi cần. Mọi lệnh có `--help`.

```bash
python3 tvbt/nc.py huyenkhong --huong 185 --nam-xay 2010 --nuoc "Nam,Đông Nam" --nui "Bắc" --nam-xem 2026 [--thang-xem 10]
```

## Luận
Trình bày theo v2: (1) bảng số liệu, (2) luận theo mục, (3) lưu ý và độ chắc chắn. Không phán chắc chắn, không gieo sợ hãi, không quyết định y tế, tài chính, pháp lý thay người dùng.

### 4.1 Huyền không nâng cao (lệnh `huyenkhong`)
Lệnh này **thay** phần Huyền không của v2 khi nhà có kiêm hướng, hoặc khi cần Thành môn, đả kiếp, lưu niên chồng bàn, bố trí theo sơn thủy thật.

**Hỏi người dùng trước khi chạy:**
1. **Độ hướng nhà.** Đứng trong nhà, nhìn ra cửa chính hoặc mặt tiền. Đo 2–3 lần, tránh xa sắt thép, xe và đồ điện. Dùng **bắc từ** (la bàn); điện thoại để "Bắc thực" thì cộng thêm khoảng 0,5° (miền Nam) đến 1,7° (Hà Nội) – đáng kể khi gần ngưỡng 3°/4,5° hoặc ranh giới sơn.
2. **Năm xây xong hoặc nhập trạch** (`--nam-xay`). Nếu từng sửa lớn (thay mái, cải tạo lớn), hỏi năm sửa, vì có phái tính lại vận theo năm đó. Đã biết vận thì dùng `--van`.
3. **Phương có cửa, đường, sân trống, hồ, sông** (`--nuoc`). **Phương có nhà cao, tường cao, núi** (`--nui`). Ghi tên phương, ví dụ "Nam,Đông Nam", hoặc viết tắt B, ĐB, Đ, ĐN, N, TN, T, TB.
4. **Năm, tháng muốn xem** (`--nam-xem`, `--thang-xem`). Tháng ở đây là tháng tiết khí: tháng 1 là tháng Dần, bắt đầu từ Lập Xuân.

Ví dụ: `python3 tvbt/nc.py huyenkhong --huong 185 --nam-xay 2010 --nuoc "Nam,Đông Nam" --nui "Bắc" --thang-xem 10`.
Muốn ép dùng một bàn: `--ban ha|the|ca-hai`.

**Đọc kết quả theo thứ tự:**
1. **Chọn bàn** (nói rõ đang dùng bàn nào và vì sao):
   - Lệch tâm sơn đến 3°: dùng bàn hạ quái.
   - Lệch 3–4,5°: script in cả hai bàn, mặc định hạ quái.
   - Lệch quá 4,5°: đây là kiêm hướng, dùng bàn **thế quái**.
   - Script báo không vong thì không lập bàn: xin người dùng đo lại.
   - Có dòng "Phái Trung Châu": nói thêm là có phái không dùng thế quái trong trường hợp này.
   - Chỉ chênh 1–2° là đã đổi bàn: chạy cả hai số đo rồi so sánh.
2. **Đọc lưới** (phía Nam ở trên):
   - S là sơn tinh: người, sức khỏe, quan hệ.
   - H là hướng tinh: tiền bạc, công việc.
   - V là vận tinh.
3. **Cục:**
   - Vượng sơn vượng hướng: hợp nhất khi sau nhà cao, trước nhà thoáng.
   - Song tinh đáo hướng: trước nhà nên vừa có nước vừa có chỗ cao.
   - Song tinh đáo tọa: sau nhà nên vừa có chỗ cao vừa có khoảng trống.
   - Thượng sơn hạ thủy: cần hình thế đảo lại thì mới đỡ.
   - Luôn gắn kết luận với nhà thật, không kết luận chỉ từ con số.
4. **Phục ngâm, phản ngâm toàn bàn.** Nói nhẹ nhàng: sách xếp đây là cách kém, cần xem thêm hình thế.
5. **Hợp thập, liên châu, phụ mẫu tam ban** là cách "thông khí", tính là điểm cộng.
6. **Thất tinh đả kiếp:**
   - Chỉ xét khi cục là song tinh đáo hướng.
   - Đả kiếp ở cung Ly là chân đả kiếp. Ở cung Khảm là giả, nhiều phái không dùng.
   - Chỉ có tác dụng khi hướng có cửa hoặc nước thật, ba cung trong nhóm thông khí với nhau, và chỉ trong vận của nhà.
7. **Thành môn:**
   - Cung ghi "DÙNG ĐƯỢC" chỉ có tác dụng khi ở đó thật sự có cửa, ngõ, ngã ba hoặc nước.
   - Vận tinh ở cung đó là 5: script ghi rõ hai cách tính.
   - Nhà thuộc vận cũ: script tính thêm theo vận hiện tại, vì các phái khác nhau ở điểm này.
8. **Nhập tù** chỉ là mốc thời gian theo Thẩm thị, không phải lời phán.
9. **Cặp sao:** trạng thái tính theo vận đang hành (vận 9 là 2024–2043).
   - Vượng, sinh, tiến: nghiêng tốt. Thoái: trung bình. Suy, tử: nghiêng xấu.
   - Sao 5 (sát): nên giữ yên.
   - Dùng lời "dễ", "nên để ý", "thiên về"; không đoán sự kiện cụ thể.
10. **Lưu niên, lưu nguyệt:**
    - Cung có Ngũ Hoàng, 2-5 hội, Thái Tuế hay Tuế Phá: khuyên giữ yên, tránh động thổ, đục phá, sửa lớn trong năm hoặc tháng đó.
    - Nếu buộc phải làm, chọn ngày bằng lệnh `ngay`.
11. **Bố trí theo sơn thủy thật:**
    - Cửa chính, chỗ làm việc: đặt ở cung có hướng tinh tốt.
    - Phòng ngủ: đặt ở cung có sơn tinh tốt và yên tĩnh.
    - Cung có sao suy hoặc sao 5: hợp làm kho, nhà vệ sinh, giữ yên.
    - Script ghi "sơn tinh rơi xuống nước" hay "hướng tinh bị chắn": giải thích bằng lời thường.

**Cách nói với người dùng:**
- Đây là gợi ý theo sách, không phải lời phán.
- Không khuyên mua vật phẩm đắt tiền.
- Quyết định xây sửa vẫn phải dựa vào kỹ thuật, an toàn và giấy phép.
- Có hai bàn hay hai phái thì nêu ngắn cả hai và nói bàn nào là chính.

## Trường phái và giới hạn (nói rõ khi liên quan)
**Huyền không**
