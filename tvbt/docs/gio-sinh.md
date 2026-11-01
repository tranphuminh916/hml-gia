# Dò giờ sinh (không biết hoặc không chắc giờ sinh)

## Khi nào dùng
- Người hỏi không biết giờ sinh, chỉ nhớ "buổi sáng", "gần trưa", hoặc nhớ giờ nhưng không chắc.
- Giờ sinh rơi sát ranh giới hai giờ âm lịch (script `tvbt.py` in cảnh báo "sát ranh giới").
- Người hỏi thấy lá số "không giống mình" và muốn kiểm tra lại giờ.

Không có giờ sinh thì không lập được lá số Tử vi, chỉ có Bát tự 3 trụ. Vì vậy nên dò giờ trước khi luận Tử vi.

## Lệnh
```
python3 tvbt/giosinh.py --ngay YYYY-MM-DD --gioi nam|nu --noi "Tỉnh" [--am] [--nhuan] --cau-hoi
python3 tvbt/giosinh.py --ngay YYYY-MM-DD --gioi nam|nu --noi "Tỉnh" --tra-loi '{JSON}'
```
- `--cau-hoi` in 7 câu hỏi kèm lựa chọn. Câu 6 (tính cách) được tính theo các câu đã trả lời trong `--tra-loi`.
- Script lập sẵn lá số cho **mọi giờ trong ngày sinh theo giờ đồng hồ**. Nó đã trừ phần lệch giờ mặt trời thực và múi giờ lịch sử. Giờ Tý tách hai khung:
  - Giờ Tý đầu ngày: 0–1h.
  - Giờ Tý cuối ngày: 23–24h, lá số tính theo ngày hôm sau.
- Output gồm bảng 12–13 khung giờ (giờ đồng hồ, trụ giờ, cung Mệnh, sao chính ở Mệnh, Thân cư, cục, phần trăm khả năng, lý do), rồi dòng KẾT LUẬN.

## Câu trả lời (khóa JSON)
| Khóa | Câu hỏi | Giá trị |
|---|---|---|
| `khoang` | Gia đình nhớ sinh lúc nào | `khuya`, `rangsang`, `sang`, `trua`, `chieu`, `toi`, `ngay`, `dem`, hoặc `{"gio":"HH:MM","sai":phút}` khi nhớ giờ đồng hồ (sai 15/30/60/120) |
| `xoay` | Xoáy tóc trên đỉnh đầu | `chinh` (một xoáy chính giữa), `sinh` (gần giữa, hơi lệch), `mo` (lệch hẳn hoặc 2–3 xoáy) |
| `ngu` | Tư thế ngủ quen từ nhỏ | `chinh` (ngửa), `sinh` (nghiêng), `mo` (sấp) |
| `mat` | Dáng khuôn mặt | `chinh` (tròn), `sinh` (vuông), `mo` (dài) |
| `than` | Từ khoảng 30 tuổi, điều gì chiếm nhiều tâm sức nhất | `Mệnh`, `Phúc Đức`, `Quan Lộc`, `Thiên Di`, `Tài Bạch`, `Phu Thê` |
| `tinh` | Tính cách giống mô tả nào | danh sách mã giờ, ví dụ `["g10"]`, lấy từ lựa chọn câu 6 |
| `nam` | Năm đời rẽ hướng rõ nhất | danh sách năm dương lịch, ví dụ `[2013, 2019]` |

Bỏ khóa nào thì câu đó coi như "không rõ".

## Cách hỏi
- Hỏi gọn, chia hai lượt. Lượt 1 hỏi câu 1–5. Chạy lệnh để lấy lựa chọn câu 6, rồi lượt 2 hỏi câu 6–7. Có công cụ hỏi trắc nghiệm thì dùng.
- Câu 1 quan trọng nhất. Hỏi thêm người nhà nếu được.
- Câu 2–4 là dấu hiệu dân gian. Nói rõ là chỉ để tham khảo.

## Căn cứ và độ tin
1. **Giờ gia đình nhớ**: mạnh nhất. Script chấm theo phần khoảng nhớ rơi vào từng giờ và chừa 10–15% khả năng nhớ sai.
2. **Xoáy tóc, dáng ngủ, khuôn mặt**: dân gian chia ba nhóm giờ:
   - Tứ chính: Tý, Ngọ, Mão, Dậu.
   - Tứ sinh: Dần, Thân, Tỵ, Hợi.
   - Tứ mộ: Thìn, Tuất, Sửu, Mùi.

   Khẩu quyết: "Tý Ngọ Mão Dậu nằm ngửa, Dần Thân Tỵ Hợi nằm nghiêng, Thìn Tuất Sửu Mùi nằm sấp"; mặt tròn, vuông, dài theo cùng thứ tự. Đây là căn cứ yếu, mỗi câu chỉ nhân hệ số 0,55–0,6 cho giờ không khớp.
3. **Cung an Thân**: do giờ sinh quyết định.
   - Tý, Ngọ: Thân cư Mệnh.
   - Sửu, Mùi: cư Phúc Đức.
   - Dần, Thân: cư Quan Lộc.
   - Mão, Dậu: cư Thiên Di.
   - Thìn, Tuất: cư Tài Bạch.
   - Tỵ, Hợi: cư Phu Thê.

   Nửa đời sau thường xoay quanh cung an Thân.
4. **Tính cách**: theo chính tinh cung Mệnh. Mệnh vô chính diệu thì mượn sao cung đối.
5. **Năm rẽ hướng**: so tuổi mụ năm đó với tuổi chuyển đại hạn (cục + 10k) của từng giờ.

Mỗi câu chỉ nhân thêm hệ số, không loại hẳn giờ nào.

Kết luận có ba mức:
- "Khá rõ": giờ đầu ≥ 55% và gấp đôi giờ thứ hai.
- "Nghiêng về": giờ đầu ≥ 35% và gấp 1,4 lần giờ thứ hai.
- Còn lại là "chưa rõ".

## Cách luận kết quả
1. Mở đầu bằng giờ khả năng nhất, phần trăm, khung **giờ đồng hồ** của ngày sinh, và mức chắc chắn.
2. Nói căn cứ: câu nào khớp với giờ đó (dùng cột Lý do). Không viện dẫn điều script không in.
3. Nêu 1–2 giờ cần so thêm (dòng "Giờ cần so thêm") và khác biệt chính giữa các lá số đó: cung Mệnh, sao chính, Thân cư, tuổi bắt đầu đại hạn.
4. Mức "chưa rõ" thì đề nghị **đối chiếu sự kiện**:
   - Hỏi 2–3 mốc đã qua: năm cưới, năm đổi việc lớn, năm chuyển nhà, năm có biến cố.
   - Lập lá số cho từng giờ còn lại: `tvbt.py tuvi --gio <giờ đại diện> --nam-xem <năm mốc>`. Xem đại hạn, tiểu hạn và lưu niên năm đó có ứng không.
5. Kết bài:
   - Đây là ước đoán để tham khảo; có giấy chứng sinh ghi giờ thì tin giấy.
   - Dấu hiệu dân gian không phải căn cứ chắc chắn.
   - Không nói giờ nào "tốt" hay "xấu" hơn.
6. Khi người hỏi chọn được giờ: ghi vào Sổ lá số với chú thích "giờ dò qua 7 câu hỏi, chưa chắc chắn". Từ đó khi kết luận phụ thuộc giờ sinh thì nhắc một câu.

## Lưu ý
- `--ngay` là **ngày theo đồng hồ** lúc sinh, không phải ngày âm của giờ Tý muộn.
- Sinh ở miền Nam 1960–1975 (đồng hồ UTC+8) thì giờ mặt trời lệch đồng hồ gần 50 phút. Khung giờ đồng hồ khi đó lệch hẳn so với cách chia 23–1h, 1–3h… quen thuộc. Script đã tính.
- Sinh trước 1955 thì múi giờ đồng hồ không thống nhất. Script in cảnh báo, phải nói lại cho người hỏi.
