# Chọn ngày đầy đủ (lệnh nc.py ngay) – dùng thay chonngay

> Phần cài đặt và tự kiểm tra đã làm ở Bước 2 của SKILL.md (skill tu-vi-bat-tu-phong-thuy-v3). Mọi file đã có sẵn trong `tvbt/`; bỏ qua mọi chỗ nhắc tới "trích", "vá", "Bước 1/2 của skill v2" hay tên các skill cũ (v2, luan-la-so-chi-tiet, ky-mon-mo-rong, …) – nay tất cả là một bộ.

## Có gì
| Lệnh | Làm gì | Dùng khi |
|---|---|---|
| `ngay` | Chọn ngày đầy đủ: việc nên/kiêng theo ngày và giờ, 60 cát thần, 91 hung sát, hướng Hỷ/Tài/Phúc thần, Quý nhân, Thai thần, Bành Tổ; gộp Hoàng đạo, Trực, 28 Tú, Tam Nương, Nguyệt Kỵ, Dương Công, xung tuổi; chấm 100 điểm, chia 3 nhóm | Mọi câu hỏi chọn ngày (thay `chonngay` của v2) |

## Đã kiểm chứng
- **Chọn ngày (`ngay`).**
  - Từ điển phủ hết từ ngữ của dữ liệu lịch: 116 việc, 60 cát thần, 91 hung sát. Đã quét 1900–2100, cứ 3 ngày lấy một mẫu, không sót từ nào chưa dịch.
  - Hoàng đạo, Trực, 28 Tú, Tam Nương, Nguyệt Kỵ, Dương Công, xung tuổi: lấy đúng từ `chonngay` của v2, phần này đã khớp lunar-python trên 40.543 ngày.
  - Có bất biến: ngày lịch ghi kiêng đúng việc chính, hoặc ngày xung tuổi người chủ sự, không bao giờ lọt vào nhóm chọn.
- **Rà soát độc lập.** Đã có một lượt rà soát độc lập; lỗi "ngày lịch ghi 'việc khác không nên' vẫn lọt vào nhóm chọn" đã sửa và có ca thử riêng.
- **Rà soát 11/2026.**
  - Thêm Thọ tử, Sát chủ dương, Sát chủ âm, Vãng vong (theo tháng âm, nguồn lịch Việt Nam). Trước bản này, riêng 2020–2029 có 79 ngày cưới, 60 ngày nhập trạch, 53 ngày động thổ là Thọ tử / Sát chủ dương / Vãng vong mà vẫn vào nhóm "Nên chọn". Nay chạy 1950–2060: 0 ngày như vậy lọt vào nhóm chọn.
  - Kim Lâu, Hoang Ốc, Tam Tai của người chủ sự nay in trong lệnh `ngay`, tính theo **năm âm lịch** của khoảng ngày (trước đây `chonngay` lấy năm dương lịch: chọn ngày cưới 5–20/1/2027 bị tính sang năm Đinh Mùi 2027, tuổi mụ sai 1, Kim Lâu sai).
  - Sửa 3 dòng thần sát nhập sai của lunar-python (tháng Hợi ngày Kỷ Sửu, tháng Mùi ngày Quý Dậu, tháng Dậu ngày Kỷ Dậu).

## Chạy
Tham số ngày giờ giống `tvbt.py`: `--ngay YYYY-MM-DD --gio HH:MM --gioi nam|nu --noi "<tỉnh>"`, cộng `--am`, `--nhuan`, `--kinhdo`, `--utc`, `--mien`, `--gio-dong-ho`, `--ty` khi cần. Mọi lệnh có `--help`.

```bash
python3 tvbt/nc.py ngay --tu 2026-11-01 --den 2026-11-30 --viec khaitruong --tuoi "An:1990:Thủy+Kim:Hỏa" [--thu T7,CN] [--gon]
```

## Luận
Trình bày theo v2: (1) bảng số liệu, (2) luận theo mục, (3) lưu ý và độ chắc chắn. Không phán chắc chắn, không gieo sợ hãi, không quyết định y tế, tài chính, pháp lý thay người dùng.

### 4.1 Chọn ngày đầy đủ (lệnh `ngay`)
Lệnh này **thay** lệnh `chonngay` của v2 khi người dùng cần chọn ngày cho một việc cụ thể. Nó gộp tiêu chí lịch Việt Nam của v2 với lịch nên/kiêng đầy đủ của Hiệp Kỷ Biện Phương Thư.

**Hỏi trước khi chạy:**
- việc gì;
- khoảng ngày (≤ 93 ngày);
- năm sinh âm lịch của người chủ sự;
- nếu đã luận Bát tự cho người đó: hành cần và hành kỵ. Truyền dạng `"Tên:1990:Thủy+Kim:Hỏa"`. Không có thì bỏ trống, không tự đoán.

Muốn chỉ chọn trong một số thứ trong tuần thì thêm `--thu T7,CN`.

**Các loại việc** (`--viec`):
- chung, cuoi, anhoi
- dongtho, nhaptrach, muanha
- khaitruong, kyhopdong, nhapkho, xuathang
- xuathanh, nhamchuc, thuenguoi
- chuabenh, kientung
- antang, lapbantho, kegiuong, datbep
- trongcay, nhaphoc

**Đọc kết quả:**
1. Script chia ngày thành ba nhóm: **Nên chọn** (≥ 70 điểm), **Dự phòng** (55–69), **Nên tránh**.
   - Ngày bị đưa vào nhóm tránh khi gặp một trong các trường hợp sau, dù điểm cao đến đâu:
     - lịch ghi kiêng đúng việc đó;
     - ngày "mọi việc không nên";
     - Nguyệt Phá;
     - Tam Nương, Nguyệt Kỵ, Dương Công;
     - Thọ tử (mọi việc);
     - Sát chủ dương khi cưới hỏi, ăn hỏi, động thổ, nhập trạch, mua nhà, khai trương, ký kết, nhậm chức; Sát chủ âm khi an táng;
     - Vãng vong khi xuất hành, cưới hỏi, ăn hỏi, nhập trạch, nhậm chức, chữa bệnh, nhận người (xét cả bản tháng âm của lịch Việt Nam và bản tháng tiết của Hiệp Kỷ);
     - xung tuổi người chủ sự.
   - Gặp Sát chủ / Vãng vong với việc khác: chỉ ghi chú, không loại.
   - Đầu bảng có dòng **Kim Lâu / Hoang Ốc / Tam Tai** theo năm âm lịch: Kim Lâu xét cho cưới hỏi (tuổi mụ cô dâu) và làm nhà; Hoang Ốc, Tam Tai cho làm nhà, động thổ. Phạm thì nói các cách dân gian (mượn tuổi, lùi năm) như kinh nghiệm tham khảo.
   - Nói lý do loại khi người dùng hỏi về một ngày cụ thể.
2. Đưa 2–3 ngày tốt nhất. Mỗi ngày gồm:
   - lý do: lịch ghi nên làm việc này, Trực hợp, Hoàng đạo, cát thần lớn như Thiên Đức, Nguyệt Đức, Thiên Xá, Thiên Nguyện, Mẫu Thương;
   - **giờ tốt**: giờ hoàng đạo, đã bỏ giờ xung tuổi và giờ lịch ghi kiêng. Dấu ★ là giờ lịch ghi nên làm đúng việc đó;
   - **hướng**:
     - xuất hành, khai trương: theo Hỷ thần hoặc Tài thần;
     - gặp người có chức quyền: theo Quý nhân;
     - nhà có người mang thai: nhắc vị trí Thai thần, tránh đục phá chỗ đó.
3. Hung sát của ngày được chọn: chỉ nêu những sao nặng (Nguyệt Phá, Tứ Phế, Tứ Ly, Vãng Vong, Quy Kỵ…). Nhắc rằng cát thần lớn có thể giải bớt hung sát nhỏ.
4. Lịch nên/kiêng tính theo tháng tiết khí (lịch Trung Quốc); Hoàng đạo tính theo tháng âm (lịch Việt Nam).
   - Hai cách có thể khác nhau ở ngày giáp tháng. Script ghi "các cách tính chưa đồng thuận" và hạ điểm độ tin.
   - Gặp trường hợp này, nói rõ cho người dùng.
5. Bành Tổ bách kỵ chỉ nhắc khi đúng việc, ví dụ ngày Hợi với cưới hỏi, ngày Tỵ với đi xa.

## Trường phái và giới hạn (nói rõ khi liên quan)
- **Chọn ngày:** việc nên/kiêng, cát thần, hung sát, hướng thần theo Hiệp Kỷ Biện Phương Thư (qua lunar-python), tính theo tháng tiết khí và giờ Bắc Kinh. Ngày giáp ranh tháng tiết có thể lệch. Hoàng đạo theo tháng âm như lịch Việt Nam. Thang 100 điểm là quy ước của skill.
- Dương Công kỵ nhật theo bản Việt Nam (có 8/7); sách Trung Quốc ghi 1/7. Thọ tử theo bản Việt Nam (một can chi mỗi tháng); bản Trung Quốc (受死) xét chi. Sát chủ âm: một nguồn đảo tháng 7/8 (script ghi chú khi an táng). Xem thêm `docs/co-ban.md` phần trường phái.
