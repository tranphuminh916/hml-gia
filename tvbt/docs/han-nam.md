# Sao hạn năm, Tam tai, Kim lâu, Hoang ốc, phạm Thái Tuế (tục dân gian Việt Nam)

## Khi nào dùng
- Câu hỏi kiểu "năm nay tôi sao gì, hạn gì", "có phải năm Tam tai không", "năm nào làm nhà được", "có cần cúng sao giải hạn không".
- Câu "năm nay tôi thế nào": chạy thêm lệnh này. Bài luận thêm **một dòng** về sao, hạn, Tam tai, Thái Tuế, đặt sau phần Tử vi/Bát tự.
- Chọn ngày cưới, làm nhà: chạy lệnh này cho người chủ sự trước. Năm phạm Kim lâu, Hoang ốc xấu, Tam tai thì nói ngay đầu bài.

## Lệnh
```
python3 tvbt/nc.py hannam --nam-sinh <năm âm lịch> --gioi nam|nu [--nam-xem NĂM] [--so-nam 10]
python3 tvbt/nc.py hannam --ngay YYYY-MM-DD --gioi nam|nu        # ngày dương lịch, script tự đổi ra năm âm
```
- `--so-nam 10`: bảng 10 năm liền. Dùng để tìm năm làm nhà, cưới hỏi, tức năm không phạm Kim lâu, Hoang ốc xấu, Tam tai.
- Ngày sinh trước Tết thì năm âm là năm trước. Ví dụ sinh 10/01/1990 dương lịch là tuổi Kỷ Tỵ (1989). Có `--ngay` thì script tự xét.

## Quy tắc (script tính, không nhẩm)
- **Tuổi mụ** = năm xem − năm sinh âm lịch + 1.
- **Sao chiếu mệnh (Cửu diệu)**: lấy tuổi mụ chia 9, xem số dư.

  | Dư | Nam | Nữ |
  |---|---|---|
  | 1 | La Hầu | Kế Đô |
  | 2 | Thổ Tú | Vân Hớn |
  | 3 | Thủy Diệu | Mộc Đức |
  | 4 | Thái Bạch | Thái Âm |
  | 5 | Thái Dương | Thổ Tú |
  | 6 | Vân Hớn | La Hầu |
  | 7 | Kế Đô | Thái Dương |
  | 8 | Thái Âm | Thái Bạch |
  | 0 | Mộc Đức | Thủy Diệu |

  Cách xếp phổ biến: tốt là Thái Dương, Thái Âm, Mộc Đức; trung bình là Thổ Tú, Thủy Diệu, Vân Hớn; xấu là La Hầu, Kế Đô, Thái Bạch.
- **Hạn (8 hạn)**: thứ tự Huỳnh Tuyền, Tam Kheo, Ngũ Mộ, Thiên Tinh, Toán Tận, Thiên La, Địa Võng, Diêm Vương. Cộng hai chữ số của tuổi mụ được S. Nam lấy vị trí (S + 7) mod 8, nữ lấy (5 − S) mod 8, đếm từ 0. Quy tắc này giải thích được vì sao bảng nhảy: nam Huỳnh Tuyền gặp ở 81, 89, 90; nữ ở 41, 49, 50. Tục xét hạn từ 10 tuổi. Nhiều bảng chỉ liệt kê từ 11 tuổi, nhưng không bảng nào ghi tuổi 10 khác đi. Bảng có ghi tuổi 10 (ngaydep.com, năm 2026 cho người sinh 2017) ra nam Huỳnh Tuyền, nữ Toán Tận, đúng quy tắc trên.
- **Tam tai**: tuổi Thân Tý Thìn gặp năm Dần Mão Thìn; Dần Ngọ Tuất gặp Thân Dậu Tuất; Tỵ Dậu Sửu gặp Hợi Tý Sửu; Hợi Mão Mùi gặp Tỵ Ngọ Mùi. Ba năm liền, script ghi năm thứ mấy.
- **Kim lâu** (dùng cho làm nhà, cưới hỏi): tuổi mụ chia 9 dư 1 (Thân), 3 (Thê), 6 (Tử), 8 (Lục Súc). Cưới hỏi tục xét tuổi cô dâu; có nơi xét cả chú rể.
- **Hoang ốc** (làm nhà): Nhất Cát, Nhì Nghi, Tam Địa Sát, Tứ Tấn Tài, Ngũ Thọ Tử, Lục Hoang Ốc. Hàng chục khởi ở cung tương ứng (10 tuổi ở Nhất Cát, 20 ở Nhì Nghi…), rồi đếm tiếp hàng đơn vị sang các cung sau. Tam Địa Sát, Ngũ Thọ Tử, Lục Hoang Ốc là xấu. Cách nhanh cho cùng kết quả: cộng hai chữ số, chia 6 lấy dư (dư 0 là Lục Hoang Ốc). Đã đối chiếu 6 nguồn (hoatieu, batdongsan, vnreview, chogia, dienmayxanh, fptshop): tất cả đếm tiếp như trên, không nguồn nào đếm lệch một cung.
- **Phạm Thái Tuế**: chi năm xem so với chi năm sinh.
  - Trùng chi: trực Thái Tuế, tức năm tuổi. Thìn, Ngọ, Dậu, Hợi còn tự hình.
  - Các kiểu khác: xung, hình, hại, phá.

## Đã đối chiếu
- Bảng sao hạn năm 2030 của ngaydep.com: khớp 71/71 dòng, cả nam và nữ.
- Danh sách tuổi gặp từng hạn của hoatieu.vn, ví dụ nam Huỳnh Tuyền 18, 27, 36, 45, 54, 63, 72, 81, 89, 90, 98.
- Bảng năm 2025 của thuvienphapluat.vn: Bính Dần 1986, nam Thái Bạch – Thiên Tinh, nữ Thái Âm – Tam Kheo.
- Ví dụ 48 tuổi của báo Hà Tĩnh: nam Thủy Diệu, nữ Mộc Đức.
- Tuổi 10 của ngaydep.com: nam Huỳnh Tuyền, nữ Toán Tận.
- Hoang ốc: 45 và 54 Tam Địa Sát, 41 Ngũ Thọ Tử, 33 Lục Hoang Ốc, 34 Nhất Cát (hoatieu, batdongsan, vnreview, chogia).
- Các phép này có trong `kiemtra.py` (module hannam).

## Cách nói kết quả
1. Một dòng: năm nay sao gì (tốt/xấu), hạn gì, có Tam tai, phạm Thái Tuế không. Nói giờ đồng hồ, tháng dương lịch khi cần.
2. Nói rõ đây là **tục dân gian**, tách khỏi Tử vi/Bát tự. Hai bên nói khác nhau thì ưu tiên Tử vi/Bát tự. Sao xấu chỉ nghĩa là năm nên cẩn thận hơn, không phải điềm chắc chắn.
3. **Không dọa**, không dùng chữ "đại hạn", "chết", "tai họa". Ví dụ nói: "năm nay nên giữ sức khỏe, khám định kỳ" thay cho "hạn Huỳnh Tuyền rất xấu".
4. **Cúng sao giải hạn**:
   - Chỉ nói là tục, không bắt buộc. Làm thì giản dị, tại nhà, tâm thành.
   - Ngày cúng theo tục: Thái Dương 27, Thái Âm 26, Mộc Đức 25, Vân Hớn 29, Thổ Tú 19, Thủy Diệu 21, Thái Bạch 15, La Hầu 8, Kế Đô 18 âm lịch.
   - Số nến, hướng lạy mỗi sách một khác, không nói như sự thật.
   - Nhiều nhà sư cho rằng kinh Phật không có lễ dâng sao; cốt lõi là cầu an và sống thiện.
   - **Không bao giờ** khuyên làm lễ tốn tiền, mua vật phẩm, bùa, hay thuê "thầy giải hạn".
5. Làm nhà mà năm phạm Kim lâu, Hoang ốc xấu, Tam tai:
   - Nói tục **mượn tuổi**: người được mượn tuổi phải không phạm trong năm đó, và đứng ra động thổ. Hoặc chọn năm khác trong bảng `--so-nam 10`.
   - Đây là tục, quyết định là của gia đình.
