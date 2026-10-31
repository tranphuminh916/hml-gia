# Lục Nhâm nâng cao (lệnh nc.py lucnham2)

> Phần cài đặt và tự kiểm tra đã làm ở Bước 2 của SKILL.md (skill tu-vi-bat-tu-phong-thuy-v3). Mọi file đã có sẵn trong `tvbt/`; bỏ qua mọi chỗ nhắc tới "trích", "vá", "Bước 1/2 của skill v2" hay tên các skill cũ (v2, luan-la-so-chi-tiet, ky-mon-mo-rong, …) – nay tất cả là một bộ.

## Có gì
| Lệnh | Làm gì |
|---|---|
| `lucnham2` | Đại Lục Nhâm (khóa của v2) cộng phần bổ sung: độn can, 32 thần sát, bản mệnh – hành niên, 87 điều Tất pháp phú, 46 khóa cách, loại thần theo việc |

## Đã kiểm chứng
- **Lục Nhâm bổ sung.**
  - Thần sát của ngày mẫu khớp sách. Hành niên nam (Bính Dần) và nữ (Nhâm Thân) đúng.
  - 46 khóa ví dụ trong chú giải Tất pháp phú đều kích hoạt đúng điều tương ứng.
  - Quét 8.640 khóa (60 ngày × 12 giờ × 12 nguyệt tướng) không lỗi. Không điều nào khớp quá 50% số khóa.

## Chạy
Tham số ngày giờ giống `tvbt.py`: `--ngay YYYY-MM-DD --gio HH:MM --gioi nam|nu --noi "<tỉnh>"`, cộng `--am`, `--nhuan`, `--kinhdo`, `--utc`, `--mien`, `--gio-dong-ho`, `--ty` khi cần. Mọi lệnh có `--help`.

```bash
python3 tvbt/nc.py lucnham2 --viec tien --nam-sinh 1990 --gioi nam          # thời điểm = bây giờ
python3 tvbt/nc.py lucnham2 --ngay 2026-11-02 --gio 09:30 --noi "Hà Nội" --viec tien
```

## Luận
Trình bày theo v2: (1) bảng số liệu, (2) luận theo mục, (3) lưu ý và độ chắc chắn. Không phán chắc chắn, không gieo sợ hãi, không quyết định y tế, tài chính, pháp lý thay người dùng. Chiêm việc: chỉ trả lời câu đã hỏi.

### 4.1 Lục Nhâm bổ sung (lệnh `lucnham2`)
Lệnh này **thay** lệnh `lucnham` của v2 khi cần xem kỹ hơn. Nó in lại khóa của v2, sau đó in thêm phần bổ sung.

Lệnh: `python3 tvbt/nc.py lucnham2 --ngay YYYY-MM-DD --gio HH:MM [--nam-sinh 1990 --gioi nam] --viec tien`.
- Có năm sinh và giới tính mới tính được bản mệnh, hành niên. Nếu người dùng chưa nói thì hỏi.
- Loại việc (`--viec`): chung, tien, quan, benh, kien, matdo, honnhan, thi, hopdong, xuathanh, nha, thai, timnguoi.

**Đọc theo thứ tự:**
1. **Khóa thể và tam truyền** (phần của v2): sơ truyền là khởi đầu, trung truyền là diễn biến, mạt truyền là kết cục.
2. **Can – chi.** Can là người hỏi. Chi là việc, nhà cửa, hoặc phía bên kia.
   - Thượng thần sinh can: được giúp. Thượng thần khắc can: có sức ép.
   - Can sinh thượng thần: hao sức. Can khắc thượng thần: mình chủ động.
3. **Độn can.**
   - Lục Đinh trong truyền: chuyển động, thay đổi gấp.
   - "Độn quỷ": rủi ro ngầm chưa lộ ra.
   - Tuần không, lạc không: việc chưa thực, đến chậm, lời hứa chưa chắc.
   - Thần xấu gặp không thì nhẹ đi; thần tốt gặp không thì giảm tốt.
4. **Thần sát.** Chỉ coi trọng sao nằm trong khóa, truyền, hoặc trên năm mệnh; sao ở chỗ khác chỉ là nền.
   - Dịch Mã, Thiên Mã, Đinh thần: động.
   - Thiên Đức, Nguyệt Đức, Nhật Đức, Giải Thần: giảm hung.
   - Lộc: cơm áo.
   - Tang Môn, Điếu Khách, Tử Khí: chỉ nêu khi đúng việc hỏi, và nói nhẹ.
5. **Bản mệnh, hành niên.** Xem thượng thần đứng trên năm mệnh.
   - Thượng thần sinh can: người hỏi có sức đỡ. Khắc can: nên giữ sức.
   - Thượng thần là một truyền, hoặc chi năm mệnh nhập truyền: việc dính trực tiếp đến người hỏi.
   - Bản mệnh và hành niên hợp nhau: thuận. Xung nhau: năm đó dễ thay đổi.
6. **Tất pháp phú.** Mỗi điều chỉ là một gợi ý, không phải kết luận.
   - Chỉ nêu những điều liên quan đến việc hỏi.
   - Có cả điều tốt lẫn điều xấu cùng khớp: nói cả hai, cân nhắc theo sơ truyền và mạt truyền.
   - Các điều 3, 43, 46 hay khớp (20–30% số khóa), chỉ coi là chi tiết phụ.
7. **Khóa cách.**
   - Tam quang, Tam dương, Phú quý, Vinh hoa: nghiêng tốt.
   - Tam âm, Thiên võng, Thiên ngục, Cửu xú: nghiêng cần thận trọng.
   - Toàn cục, Nguyên thai, Liên như, Lục thuần: cho biết dáng của việc, không tự nó tốt hay xấu.
8. **Loại thần theo việc:**

   | Việc | Loại thần |
   |---|---|
   | Tiền | Thanh Long, Thê tài |
   | Công việc | Quan quỷ, Quý nhân, Thái Thường |
   | Bệnh | Bạch Hổ, Quan quỷ (bệnh); Tử tôn (thuốc) |
   | Kiện | Chu Tước, Câu Trận |
   | Mất đồ | Huyền Vũ |
   | Hôn nhân | Lục Hợp, Thiên Hậu; nam xem Thê tài, nữ xem Quan quỷ |
   | Hợp đồng | Lục Hợp, Chu Tước |

   - Xét loại thần: vượng hay suy, có không vong không, có vào khóa truyền không, quan hệ với can.
   - Loại thần vượng, không bị không, sinh hoặc hợp can: thuận.
   - Loại thần không vào khóa truyền: xem chỗ nó đứng trên thiên bàn.

**Cách nói với người dùng:** nói theo khung "dấu hiệu – gợi ý gì – nên làm gì". Ví dụ: "Lộc nằm ngay can (Tất pháp điều 7), gợi ý nên giữ việc đang có."
- Không nói "chắc chắn".
- Bệnh, kiện: luôn khuyên gặp bác sĩ, luật sư.
- Khóa lẫn lộn thì nói thật là lẫn lộn.
- Không chỉ chọn những dấu hiệu hợp ý.

## Trường phái và giới hạn (nói rõ khi liên quan)
**Lục Nhâm bổ sung**
