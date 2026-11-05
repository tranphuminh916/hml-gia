# Dò giờ sinh (không biết hoặc không chắc giờ sinh) – bản 2

## Khi nào dùng
- Người hỏi không biết giờ sinh, chỉ nhớ "buổi sáng", "gà gáy", "giờ Dần", hoặc nhớ giờ nhưng không chắc.
- Giờ sinh rơi sát ranh giới hai giờ âm lịch (script `tvbt.py` in cảnh báo "sát ranh giới").
- Giờ Tý mà không biết trước hay sau 12 giờ đêm (hai lá số khác hẳn vì khác ngày âm).
- Người hỏi thấy lá số "không giống mình" và muốn kiểm tra lại giờ.

Không có giờ sinh thì không lập được lá số Tử vi, chỉ có Bát tự 3 trụ. Vì vậy nên dò giờ trước khi luận Tử vi.

## Lệnh
```
python3 tvbt/giosinh.py --ngay YYYY-MM-DD --gioi nam|nu --noi "Tỉnh" [--am] [--nhuan] --cau-hoi
python3 tvbt/giosinh.py --ngay YYYY-MM-DD --gioi nam|nu --noi "Tỉnh" --tra-loi '{JSON}' --cau-hoi
```
- `--cau-hoi` in 8 câu hỏi kèm lựa chọn. Lựa chọn câu `tinh`, `phoi` và cờ **bỏ qua** của mỗi câu được tính theo các câu đã trả lời đứng trước trong `--tra-loi`. Câu có ghi "(bỏ qua: …)" thì không hỏi.
- Script lập sẵn lá số cho **mọi giờ trong ngày sinh theo giờ đồng hồ**. Nó đã trừ phần lệch giờ mặt trời thực và múi giờ lịch sử. Giờ Tý tách hai khung:
  - Giờ Tý đầu ngày: 0–1h (sau 12 giờ đêm).
  - Giờ Tý cuối ngày: 23–24h (trước 12 giờ đêm), lá số tính theo ngày âm hôm sau.
- Output: bảng 12–13 khung giờ (giờ đồng hồ, ngày âm, trụ giờ, cung Mệnh, sao chính ở Mệnh, sao Phu Thê, Thân cư, cục, phần trăm, lý do), dòng KẾT LUẬN, "Giờ cần so thêm", các dòng "Lưu ý", và "Câu tự bỏ qua".

## Câu trả lời (khóa JSON)
| Khóa | Câu hỏi | Giá trị |
|---|---|---|
| `khoang` | Gia đình nhớ sinh lúc nào | `{"gio":"HH:MM","sai":phút}` (sai 15/30/60/120); `"tengio:K"` với K = 0–11 (Tý…Hợi), `"tengio:ty_sau"` (Tý, sau 12 giờ đêm), `"tengio:ty_truoc"` (Tý, trước 12 giờ đêm); hoặc mốc: `nuadem` 23–1, `khuya` 1–4, `gagay` 4–6, `sangsom` 6–8, `sang` 8–11, `trua` 11–13, `chieu` 13–17, `chaptoi` 17–19, `toi` 19–23, `ngay` 6–18, `dem` 18–6 |
| `cach` | Cách sinh | `mo_hen` (mổ có hẹn trước), `mo_gap` (mổ cấp cứu), `thuong` (sinh thường ở bệnh viện, trạm xá), `nha` (sinh ở nhà) |
| `xoay` | Xoáy tóc trên đỉnh đầu | `chinh` (một xoáy chính giữa), `sinh` (một xoáy lệch hẳn một bên), `mo` (hai xoáy trở lên) |
| `ngu` | Tư thế ngủ quen từ nhỏ | `chinh` (ngửa), `sinh` (nghiêng), `mo` (sấp) |
| `than` | Từ khoảng 30 tuổi, mảng nào chiếm tâm sức nhất | `Quan Lộc`, `Tài Bạch`, `Phu Thê`, `Thiên Di`, `Phúc Đức`, `Mệnh` |
| `tinh` | Tính cách giống mô tả nào | danh sách mã giờ của mục đã chọn, ví dụ `["g6","g12"]`; `[]` = không mô tả nào giống |
| `phoi` | Tính vợ/chồng giống mô tả nào | như `tinh` (theo sao cung Phu Thê) |
| `nam` | 1–3 năm đời rẽ hướng rõ nhất | danh sách năm dương lịch, ví dụ `[2013, 2019]` |

Bỏ khóa nào thì câu đó coi như "không rõ". Khóa `mat` (khuôn mặt) của bản 1 vẫn đọc được nhưng không hỏi nữa.

## Cách hỏi
- Hỏi lần lượt theo thứ tự trên; câu bị bỏ qua thì không hỏi. Sau mỗi lượt trả lời, chạy lại lệnh với `--cau-hoi` để lấy lựa chọn câu tiếp theo (nhất là `tinh`, `phoi`). Có công cụ hỏi trắc nghiệm thì dùng.
- Câu 1 quan trọng nhất. Khuyên hỏi lại mẹ hoặc người nhà. Người nhà hay nhớ theo mốc ("gà gáy", "lên đèn", "sau bữa cơm tối") hoặc theo tên giờ ("giờ Thìn"): dùng đúng mục đó.
- Giờ Tý: luôn hỏi thêm "trước hay sau 12 giờ đêm".
- Xoáy tóc, dáng ngủ là dấu hiệu dân gian. Nói rõ là chỉ tính nhẹ.

## Căn cứ và độ tin (phép Bayes)
Khả năng ban đầu của mỗi giờ tỉ lệ độ dài khung giờ. Mỗi câu trả lời nhân với một hệ số tính từ **độ tin r** của câu đó (r = phần chắc câu trả lời phản ánh giờ sinh, phần còn lại coi như ngẫu nhiên):

1. **Giờ gia đình nhớ** (mạnh): khả năng ∝ phần khoảng nhớ (kèm lề mềm) rơi vào giờ đó; chừa 8% (nhớ giờ đồng hồ) đến 12–15% (nhớ mốc, tên giờ) khả năng nhớ sai hẳn.
2. **Cách sinh**: mổ có hẹn trước – 85% rơi vào 7–17 giờ (mạnh). Sinh thường, sinh ở nhà – nhích nhẹ 1–8 giờ (chuyển dạ tự nhiên hay về đêm, sáng sớm). Mổ cấp cứu – không tính.
3. **Xoáy tóc, dáng ngủ** (r = 0,12, yếu): dân gian chia ba nhóm giờ – Tứ chính Tý Ngọ Mão Dậu (xoáy giữa, nằm ngửa), Tứ sinh Dần Thân Tỵ Hợi (xoáy lệch, nằm nghiêng), Tứ mộ Thìn Tuất Sửu Mùi (hai xoáy, nằm sấp). Khớp nhóm chỉ hơn không khớp khoảng 1,4 lần.
4. **Cung an Thân** (r = 0,15, vừa): Tý Ngọ cư Mệnh, Sửu Mùi cư Phúc Đức, Dần Thân cư Quan Lộc, Mão Dậu cư Thiên Di, Thìn Tuất cư Tài Bạch, Tỵ Hợi cư Phu Thê. Có trừ **tỉ lệ nền**: phần đông chọn công việc (34%) hoặc tiền bạc (28%) dù Thân cư đâu, nên chọn hai mục này tính nhẹ; chọn mục hiếm (gia tộc, đi xa) tính mạnh hơn. Người dưới 28 tuổi thì bỏ câu này.
5. **Tính cách** (r = 0,25) theo chính tinh cung Mệnh; **tính vợ/chồng** (r = 0,22) theo chính tinh cung Phu Thê. Vô chính diệu thì mượn cung đối. Hiện tối đa 8 mô tả của các giờ còn khả năng, thứ tự xáo cố định (không xếp theo khả năng). Giờ có mô tả không được hiện ra thì không bị trừ.
6. **Năm rẽ hướng**: so tuổi mụ năm đó với tuổi chuyển đại hạn (cục + 10k). Hệ số: đúng năm chuyển 2,2; lệch 1 năm 1,3; lệch 2 năm 0,85; xa hơn 0,7.

Câu nào không giúp phân biệt các giờ còn khả năng (cùng nhóm, cùng Thân cư, cùng mô tả, cùng tuổi chuyển đại hạn) thì tự bỏ qua. Không loại hẳn giờ nào.

Kết luận có bốn mức:
- "Khá rõ": giờ đầu ≥ 70%, gấp 3 giờ thứ hai, **và** có căn cứ mạnh (giờ gia đình nhớ hoặc mổ có hẹn).
- "Nghiêng về": giờ đầu ≥ 45% và gấp 1,6 lần giờ thứ hai.
- "Chưa rõ": còn lại.
- "Chưa trả lời câu nào".

Thử mô phỏng 240 bộ câu trả lời: khi script báo 80–100% thì đúng 97%; 60–80% đúng khoảng 80%; 40–60% đúng khoảng 55%. Nghĩa là phần trăm in ra gần với khả năng đúng thật (nếu giả định độ tin ở trên hợp lý).

## Cách luận kết quả
1. Mở đầu bằng giờ khả năng nhất, phần trăm, khung **giờ đồng hồ** của ngày sinh, và mức chắc chắn.
2. Nói căn cứ: câu nào khớp với giờ đó (cột Lý do). Không viện dẫn điều script không in. Nhắc các dòng "Lưu ý".
3. Nêu 1–2 giờ cần so thêm và khác biệt chính giữa các lá số: ngày âm (với hai giờ Tý), cung Mệnh, sao chính, sao Phu Thê, Thân cư, tuổi bắt đầu đại hạn.
4. Mức "chưa rõ" (hoặc chưa có giờ gia đình nhớ) thì đề nghị **đối chiếu sự kiện**:
   - Hỏi 2–3 mốc đã qua: năm cưới, năm đổi việc lớn, năm chuyển nhà, năm có biến cố.
   - Lập lá số cho từng giờ còn lại: `tvbt.py tuvi --gio <giờ đại diện> --nam-xem <năm mốc>`. Xem đại hạn, tiểu hạn và lưu niên năm đó có ứng không.
5. Kết bài:
   - Đây là ước đoán để tham khảo; có giấy chứng sinh ghi giờ thì tin giấy.
   - Dấu hiệu dân gian không phải căn cứ chắc chắn.
   - Không nói giờ nào "tốt" hay "xấu" hơn.
6. Khi người hỏi chọn được giờ: ghi vào Sổ lá số với chú thích "giờ dò qua câu hỏi, chưa chắc chắn". Từ đó khi kết luận phụ thuộc giờ sinh thì nhắc một câu.

## Lưu ý
- `--ngay` là **ngày theo đồng hồ** lúc sinh, không phải ngày âm của giờ Tý muộn.
- Sinh ở miền Nam 1960–1975 (đồng hồ UTC+8) thì giờ mặt trời lệch đồng hồ gần 50 phút. Khung giờ đồng hồ khi đó lệch hẳn so với cách chia 23–1h, 1–3h… quen thuộc. Script đã tính. Khi người nhà nhớ **tên giờ** (giờ Dần…), script hiểu theo cách chia đồng hồ quen thuộc (Dần = 3–5 giờ) và chừa lề 30 phút hai bên.
- Sinh trước 1955 thì múi giờ đồng hồ không thống nhất. Script in cảnh báo, phải nói lại cho người hỏi.
