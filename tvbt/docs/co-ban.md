# Cơ bản: chạy tvbt.py và luận Bát tự, Tử vi, Phong thủy, Kỳ môn, Lục Nhâm, Mai hoa, chọn ngày

> Phần cài đặt và tự kiểm tra đã làm ở Bước 2 của SKILL.md (skill tu-vi-bat-tu-phong-thuy-v3). Mọi file đã có sẵn trong `tvbt/`; bỏ qua mọi chỗ nhắc tới "trích", "vá", "Bước 1/2 của skill v2" hay tên các skill cũ (v2, luan-la-so-chi-tiet, ky-mon-mo-rong, …) – nay tất cả là một bộ.

## Chạy

```bash
python3 tvbt/tvbt.py tatca --ngay 1990-05-17 --gio 14:30 --gioi nu --noi "Đà Nẵng" --nam-xem 2026
python3 tvbt/tvbt.py battu tuvi --ngay 1990-04-23 --am --gio 14:30 --gioi nu --noi "Đà Nẵng" --phi-hoa   # ngày ÂM lịch, kèm phi hóa
python3 tvbt/tvbt.py phongthuy --ngay 1990-05-17 --gioi nam --noi "Hà Nội" --huong 157 --nam-xay 2015 --nam-xem 2026
python3 tvbt/tvbt.py kymon lucnham maihoa --noi "Hà Nội"                       # chiêm việc ngay bây giờ
python3 tvbt/tvbt.py kymon --ngay 2026-11-02 --gio 09:20 --noi "TP HCM"        # chiêm ở một thời điểm cụ thể
python3 tvbt/tvbt.py maihoa --so 7 15 --ngay 2026-11-02 --gio 09:20             # Mai hoa theo 2 số người hỏi nghĩ ra
python3 tvbt/tvbt.py chonngay --tu 2026-12-01 --den 2027-01-31 --viec cuoi --tuoi "Cô dâu:1996" "Chú rể:1994"
```

Tham số hay dùng (xem đủ bằng `--help`):
- `battu | tuvi | phongthuy | tatca | kymon | lucnham | maihoa | chonngay`: chọn phần cần lập (chọn được nhiều phần). `tatca` = ba phần lá số.
- `--am`, `--nhuan`: ngày nhập là âm lịch, và là tháng nhuận.
- `--kinhdo 2.35 --utc 1`: sinh (hoặc đang ở) ngoài Việt Nam (bắt buộc có `--utc`, tính cả giờ mùa hè). Trong nước nhưng tỉnh/huyện không có trong bảng: dùng `--kinhdo` (tra kinh độ), giữ `--noi` để ghi tên. Nếu sinh 1955–1975 thì thêm `--mien bac|nam` (ranh giới là vĩ tuyến 17, sông Bến Hải; Vĩnh Linh thuộc miền Bắc).
- `--gio-dong-ho`: an giờ theo giờ đồng hồ thay vì giờ mặt trời thực (mặc định là giờ mặt trời thực – áp dụng cho cả Kỳ môn, Lục Nhâm, Mai hoa).
- `--ty 2`: với người sinh 23h–24h, giữ trụ ngày là ngày cũ (mặc định `--ty 1` là đã sang ngày mới). Kỳ môn, Lục Nhâm luôn tính 23h là ngày mới.
- `--nam-xem N`: năm xem vận hạn, Cửu tinh; bảng lưu niên Bát tự bắt đầu từ năm này. `--luu-nien K`: số năm lưu niên cần liệt kê.
- `--phi-hoa`: in thêm bảng Tứ hóa phi tinh 12 cung và Lai nhân cung.
- `--kymon-phep huybo|trinhuan`: phép định cục Kỳ môn (mặc định hủy bổ). Script luôn tính cả hai và in cảnh báo `!` khi hai phép ra cục khác nhau. `--nhuan-nguong 8|9|10`: ngưỡng nhuận của trí nhuận (mặc định 9 như phần mềm hiện nay; 8 theo lệ Khang Hy).
- `--so A B`: Mai hoa theo số (A → quẻ thượng, B → quẻ hạ, hào động = (A + B + số giờ) chia 6); thêm số thứ ba bất kỳ (`--so A B 0`) để hào động chỉ lấy (A + B).
- `chonngay`: `--tu`, `--den` (YYYY-MM-DD, tối đa 93 ngày), `--viec chung|cuoi|dongtho|khaitruong|xuathanh|nhaptrach`, `--tuoi "Tên:năm âm lịch sinh" ...`, `--hoang-dao-tiet` (tính Hoàng đạo theo tháng tiết khí thay vì tháng âm).

Những việc script đã tự xử lý (không cần làm tay):
- Múi giờ đồng hồ theo thời kỳ: miền Nam 1960–13/6/1975 dùng UTC+8; trước 1955 có cảnh báo.
- Giờ mặt trời thực theo kinh độ.
- Trụ năm và trụ tháng theo **tiết khí** (Lập Xuân), không theo Tết. Cục Kỳ môn theo tiết khí đang hiệu lực đến từng phút; Nguyệt tướng Lục Nhâm theo trung khí.
- Âm lịch Việt Nam UTC+7 (trước 1968, và miền Nam đến 1975, dùng UTC+8).
- Giờ Tý muộn, tháng nhuận.

**Chạy thêm phương án khi gặp cảnh báo:**
- Giờ sinh (hoặc giờ hỏi) sát ranh giới giờ âm lịch, hoặc giờ đồng hồ và giờ mặt trời thực rơi vào hai giờ khác nhau: lập cả hai (thêm `--gio-dong-ho`, hoặc dịch giờ), so sánh. Với lá số thì hỏi người dùng vài sự kiện đời thực để chọn; với Kỳ môn/Lục Nhâm thì nói rõ có hai bàn.
- Sinh 23h–24h: chạy thêm `--ty 2`, cho biết trụ ngày khác nhau ra sao.
- Ngày giao tiết mà không có giờ sinh: trụ tháng chưa xác định được; phải hỏi giờ sinh.
- Sinh trước 1955: hỏi người dùng giờ ghi trên giấy khai sinh theo múi nào, nếu biết thì dùng `--utc`.
- Chọn ngày: nếu cột ghi chú có "tính theo tháng tiết khí thì là …" thì ngày đó Hoàng/Hắc đạo tùy cách tính – nói rõ, ưu tiên ngày tốt theo cả hai cách.

## Luận giải

Trình bày theo thứ tự: (1) **Bảng số liệu** (dán gọn các bảng script in ra); (2) **Luận giải** chia theo mục; (3) **Lưu ý / độ chắc chắn**. Viết tiếng Việt, rõ ràng, có căn cứ: mỗi nhận định phải nói nó dựa vào yếu tố nào trong lá số / bàn / quẻ. Không phán chắc chắn, không gieo sợ hãi, không đưa ra quyết định y tế, tài chính hay pháp lý thay người dùng. Khi các trường phái khác nhau, nói rõ là có nhiều cách hiểu.

### 4.1 Bát tự (Tứ trụ)
1. **Nhật chủ** = can ngày. Đánh giá **vượng/nhược** theo ba yếu tố:
   - Đắc lệnh: chi tháng sinh trợ hoặc sinh Nhật chủ. Đây là yếu tố nặng nhất.
   - Đắc địa: có gốc trong tàng can các chi.
   - Đắc thế: nhiều can chi Tỷ Kiếp, Ấn.

   Bảng "Đếm ngũ hành" chỉ để tham khảo, **không** dùng để kết luận vượng/nhược.
2. **Dụng thần / hỷ kỵ**:
   - Thân nhược: ưa Ấn và Tỷ Kiếp.
   - Thân vượng: ưa Thực Thương (tiết khí), Tài, Quan Sát.
   - Xét thêm **điều hậu**: sinh mùa đông (Hợi, Tý, Sửu) cần Hỏa sưởi ấm; sinh mùa hạ (Tỵ, Ngọ, Mùi) cần Thủy.
   - Cách cục đặc biệt (tòng, hóa, chuyên vượng) chỉ kết luận khi đủ điều kiện rõ ràng, và phải nói là nhận định.
3. **Cách cục**: xem can tàng trong chi tháng thấu lên can nào (Chính Quan cách, Thất Sát cách, Chính Tài, Thiên Tài, Thực Thần, Thương Quan, Chính Ấn, Thiên Ấn…).
4. **Quan hệ can chi**:
   - Thiên can hợp: Giáp–Kỷ (Thổ), Ất–Canh (Kim), Bính–Tân (Thủy), Đinh–Nhâm (Mộc), Mậu–Quý (Hỏa).
   - Lục hợp: Tý–Sửu, Dần–Hợi, Mão–Tuất, Thìn–Dậu, Tỵ–Thân, Ngọ–Mùi.
   - Lục xung: Tý–Ngọ, Sửu–Mùi, Dần–Thân, Mão–Dậu, Thìn–Tuất, Tỵ–Hợi.
   - Tam hợp: Thân Tý Thìn (Thủy), Hợi Mão Mùi (Mộc), Dần Ngọ Tuất (Hỏa), Tỵ Dậu Sửu (Kim).
   - Tam hội: Dần Mão Thìn (Mộc), Tỵ Ngọ Mùi (Hỏa), Thân Dậu Tuất (Kim), Hợi Tý Sửu (Thủy).
   - Hình: Dần–Tỵ–Thân, Sửu–Tuất–Mùi, Tý–Mão; tự hình Thìn, Ngọ, Dậu, Hợi.
   - Hại: Tý–Mùi, Sửu–Ngọ, Dần–Tỵ, Mão–Thìn, Thân–Hợi, Dậu–Tuất.
5. **Ý nghĩa Thập thần** (tham khảo):

   | Thập thần | Ý nghĩa |
   |---|---|
   | Tỷ Kiên / Kiếp Tài | Bản thân, anh em, cạnh tranh, hao tài |
   | Thực Thần / Thương Quan | Tài năng, biểu đạt, con cái (với nữ); Thương Quan thì phá cách, nổi loạn |
   | Chính Tài / Thiên Tài | Tiền bạc, vợ (với nam), cha; Thiên Tài là tài bất ngờ, kinh doanh |
   | Chính Quan / Thất Sát | Sự nghiệp, kỷ luật, chồng (với nữ), áp lực; Thất Sát mạnh mẽ, rủi ro |
   | Chính Ấn / Thiên Ấn | Học vấn, mẹ, quý nhân, bằng cấp; Thiên Ấn thì cô độc, chuyên môn lạ |

6. **Đại vận / Lưu niên**: xét can chi của vận/năm là hỷ hay kỵ đối với dụng thần, có xung, hợp hay hình với tứ trụ không (nhất là trụ ngày và trụ tháng). Tuổi trong bảng đại vận là **tuổi mụ**.
7. **Thần sát** (bảng script in sau phần Bát tự): chỉ là yếu tố **phụ**, dùng để tô màu cho kết luận đã rút ra từ ngũ hành – thập thần, không lấy thần sát làm căn cứ chính. Thần sát rơi vào trụ nào thì ứng với giai đoạn/quan hệ của trụ đó (năm: tổ nghiệp, tuổi nhỏ; tháng: cha mẹ, anh em, thanh niên; ngày: bản thân, vợ/chồng; giờ: con cái, hậu vận). Cát thần gặp xung, gặp không vong thì giảm. Các thần sát hung (Kiếp Sát, Vong Thần, Âm Dương Sai Thác, Cô Loan, Thập Ác…) **không được dùng để gieo sợ hãi**: nói như "xu hướng cần lưu ý", và nhắc là các sách xếp khác nhau.

### 4.2 Tử vi Đẩu số (cách an Việt Nam)
1. **Cung Mệnh** và **tam phương tứ chính**: Mệnh + Quan Lộc + Tài Bạch (tam hợp) + Thiên Di (xung chiếu). **Cung Thân** chủ hậu vận (sau khoảng 30 tuổi).
2. **Chính tinh** và **độ sáng** (M Miếu, V Vượng, Đ Đắc, B Bình, H Hãm). Cung Vô chính diệu thì mượn chính tinh ở cung xung chiếu, sức yếu hơn. Các bộ sao lớn: Tử Phủ Vũ Tướng (ổn định, quản lý), Sát Phá Tham (biến động, mạo hiểm), Cơ Nguyệt Đồng Lương (văn, phục vụ, ổn định), Cự Nhật (ngôn luận, giao tiếp).
3. **Lục cát** (Xương, Khúc, Tả, Hữu, Khôi, Việt) và **Lục sát** (Kình, Đà, Hỏa, Linh, Không, Kiếp). Thêm Lộc Tồn, Thiên Mã, Hóa Lộc (bộ Lộc Mã).
4. **Tứ hóa năm sinh**: Lộc (được), Quyền (nắm), Khoa (danh), Kỵ (vướng). Xem chúng nằm ở cung nào.
5. **Tuần, Triệt**: làm giảm cả cát lẫn hung ở 2 cung nơi chúng đóng. Kinh nghiệm phổ biến: Triệt nặng trước khoảng 30 tuổi, Tuần ảnh hưởng về sau.
6. **Âm dương thuận/nghịch lý**, **Mệnh–Cục sinh khắc** (script in sẵn): Cục sinh Mệnh thì tốt; Cục khắc Mệnh thì vất vả hơn.
7. **Vận hạn năm**:
   - Cung đại hạn 10 năm là bối cảnh lớn.
   - Tiểu hạn và Lưu Thái Tuế là trọng tâm của năm.
   - Sao lưu: Lộc Tồn, Kình, Đà, Mã, Tang Môn, Bạch Hổ, Khốc, Hư.
   - Tứ hóa lưu niên.
   - Xem sao lưu chiếu vào cung nào, rồi kết hợp với sao gốc của cung đó.
8. **Tứ hóa phi tinh** (khi chạy `--phi-hoa`, hoặc người dùng hỏi theo phái phi hóa / Khâm Thiên Môn):
   - Mỗi cung có can riêng; can đó phát 4 hóa tới cung chứa sao được hóa. Đọc là "cung A phát Lộc vào cung B": A đem duyên/lợi cho B; "A phát Kỵ vào B": A nợ, bận tâm, vướng víu vì B.
   - **Tự hóa** (★, hóa quay về chính cung): Lộc tự hóa = được rồi lại tán; Kỵ tự hóa = tự chuốc phiền, hoặc việc của cung ấy khó giữ.
   - Ưu tiên đọc: Mệnh, Tài, Quan, Phu Thê, Điền Trạch phát Lộc/Kỵ đi đâu; Kỵ của Mệnh rơi vào cung nào là nơi đương số bận lòng nhất.
   - **Lai nhân cung** (cung có can trùng can năm sinh, xét từ Dần đến Hợi): chủ đề gốc của đời người, nơi "vì đó mà đến".
   - Phải nói rõ đây là **một phái riêng**, cách luận khác với phép tam hợp truyền thống ở 4.2.1–7; khi hai cách cho kết quả khác nhau thì trình bày cả hai.

### 4.3 Phong thủy
1. **Bát trạch**:
   - Cung phi chia người thành Đông tứ mệnh (Khảm, Ly, Chấn, Tốn) và Tây tứ mệnh (Càn, Khôn, Cấn, Đoài).
   - Ưu tiên 4 hướng tốt (Sinh Khí > Thiên Y > Diên Niên > Phục Vị) cho cửa chính, hướng bàn làm việc, hướng đầu giường.
   - Bếp theo "tọa hung hướng cát" (đặt ở phương xấu, quay về hướng tốt).
   - Trạch quái tính theo hướng **tọa** (lưng nhà). Nhà Đông tứ trạch gồm tọa Bắc, Nam, Đông, Đông Nam; còn lại là Tây tứ trạch. Nhà hợp với mệnh khi cùng nhóm.
   - Có `--huong` thì script in sẵn trạch quái của nhà và du niên của hướng, tọa đối với cung phi. Hai cách xét (theo tọa – Bát trạch minh cảnh; theo hướng nhà/cửa thuộc 4 hướng tốt – cách phổ biến hiện nay) có thể vênh nhau (vd mệnh Khảm, nhà hướng Đông Nam: hướng là Sinh Khí nhưng tọa Tây Bắc là Tây tứ trạch); script ghi rõ, phải nói cả hai.
   - **Đo hướng:** la bàn phong thủy đọc theo **bắc từ**. Điện thoại để chế độ "Bắc thực" (True North) thì ở Việt Nam số đo nhỏ hơn bắc từ khoảng 0,5° (miền Nam) đến 1,7° (Hà Nội) – cộng thêm chừng ấy (mô hình WMM2025, năm 2026). Chỉ quan trọng khi hướng sát ranh giới sơn hoặc ngưỡng kiêm hướng.
   - Nếu sinh giữa Tết và Lập Xuân, script in 2 phương án: phải hỏi người dùng theo trường phái nào.
2. **Cửu tinh năm** (năm tính từ Lập Xuân, khoảng 4/2):
   - Tránh động thổ hay sửa chữa lớn ở cung **Ngũ Hoàng**, phương **Thái Tuế** và **Tuế Phá**.
   - Nhị Hắc: sức khỏe. Tam Bích: thị phi. Thất Xích: hao tài, khẩu thiệt.
   - Cát tinh truyền thống: 1, 4, 6, 8, 9. Trong vận 9: Cửu Tử là vượng khí, Nhất Bạch là sinh khí; Bát Bạch đã thành thoái khí (vẫn tốt nhưng yếu dần).
   - Cách hóa giải chỉ nêu như kinh nghiệm truyền thống (giữ yên tĩnh, sắp xếp lại không gian). Không khuyên mua vật phẩm.
3. **Huyền không phi tinh**:
   - Vận 9 kéo dài 2024–2043. Vận của nhà lấy theo năm xây xong hoặc năm nhập trạch (nếu sửa lớn thì có thể đổi vận).
   - Sao đương vận (= số vận) đến tọa thì vượng nhân đinh, đến hướng thì vượng tài.
   - Bốn cục: Vượng sơn vượng hướng (sau cần cao, trước cần thoáng/có nước); Song tinh đáo hướng (trước cần thoáng, có nước, nên có điểm cao xa); Song tinh đáo tọa (sau nên có nước, xa hơn có điểm cao); Thượng sơn hạ thủy (cần địa hình ngược lại).
   - Bàn in ra là **Hạ quái**. Nếu script cảnh báo **kiêm hướng** (> 3° có phái đã dùng Thế quái; > 4,5° gần như chắc chắn), **không vong**, **phục ngâm / phản ngâm** hoặc **năm chuyển vận**, phải nói rõ và đề nghị đo lại hay hỏi chuyên gia. Bàn **Thế quái**, Thành môn, đả kiếp, lưu niên chồng bàn: chạy `nc.py huyenkhong` (xem `docs/huyen-khong.md`).

### 4.4 Kỳ môn độn giáp (thời gia kỳ môn, chuyển bàn)
1. **Xác định dụng thần theo việc hỏi** (chọn 1–2 yếu tố chính, tìm cung chứa nó):

   | Việc | Xem chủ yếu |
   |---|---|
   | Bản thân người hỏi | Can ngày (tìm trên thiên bàn), và Trực phù |
   | Việc đang hỏi / thời cơ | Can giờ, Trực sử |
   | Tiền bạc, kinh doanh | Sinh môn, Mậu (vốn), Thiên Tâm |
   | Công việc, thăng tiến, xin việc | Khai môn, Trực phù, Thiên Phụ |
   | Hợp tác, hôn nhân | Lục Hợp; Ất (nữ) và Canh (nam); Đinh – Nhâm |
   | Thi cử, giấy tờ | Cảnh môn, Đinh, Thiên Phụ |
   | Sức khỏe | Thiên Nhuế (bệnh), Thiên Tâm (thầy thuốc), Ất (thuốc) |
   | Kiện tụng | Kinh môn, Khai môn (quan tòa), Canh |
   | Đi xa | Dịch mã, Hưu môn, Khai môn; cung của hướng định đi |

2. **Đánh giá cung dụng thần**: môn cát (Khai, Hưu, Sinh) hay hung (Tử, Kinh, Thương); sao, thần đi kèm (Cửu Thiên, Cửu Địa, Trực Phù, Thái Âm, Lục Hợp là cát; Bạch Hổ, Huyền Vũ, Đằng Xà nên cẩn thận); cung có **Không vong** (việc chưa thành, hư) hay **Mã** (động, nhanh).
3. **Sinh khắc** giữa cung dụng thần và cung bản thân (theo ngũ hành của cung: Khảm Thủy, Khôn Cấn Thổ, Chấn Tốn Mộc, Càn Đoài Kim, Ly Hỏa): cung việc sinh/trợ cung mình là thuận; khắc mình là nghịch.
4. **Hướng**: Kỳ môn chọn phương. Gợi ý hướng có môn cát + thần cát, tránh hướng có Tử/Kinh môn, Bạch Hổ.
5. **Hai phép định cục**: nếu script in cảnh báo hai phép (hủy bổ / trí nhuận) ra cục khác nhau, chạy thêm `--kymon-phep trinhuan`, luận cả hai bàn hoặc hỏi người dùng theo phái nào; nói rõ chỗ khác. Thường chỉ khác ở vài ngày quanh giao tiết và quanh kỳ nhuận (Mang Chủng, Đại Tuyết).
6. **Dụng thần theo can**: dòng "Dụng thần theo can" cho biết cung chứa can năm (bề trên, việc lớn), can tháng (anh em, đồng nghiệp), can ngày (người hỏi), can giờ (việc hỏi) trên thiên bàn. So cung can ngày với cung can giờ: sinh/trợ nhau là thuận, khắc nhau là trở ngại.
7. **Vượng suy bát môn** theo tháng: môn cát mà vượng/tướng thì lực mạnh; hưu/tù/tử thì yếu.
8. **Cách cục** (bảng "CÁCH CỤC NHẬN DIỆN ĐƯỢC"): chỉ nhắc các cách rơi vào cung dụng thần, cung can ngày/can giờ, hoặc cách toàn bàn (phục ngâm, phản ngâm, Ngũ bất ngộ thời, Thiên phụ thời). Ý nghĩa chính:
   - Cát: Thanh Long phản thủ, Phi điểu điệt huyệt (mưu sự thành, nên chủ động); Tam trá (Chân/Trùng/Hưu trá – lợi cầu tài, giao dịch, việc kín); Ngũ giả (Thiên/Địa/Nhân/Thần/Quỷ giả – lợi mưu kế, ẩn thân); Cửu độn (Thiên, Địa, Nhân, Thần, Quỷ, Phong, Vân, Long, Hổ độn – rất lợi cho việc tương ứng); Ngọc nữ thủ môn (hôn nhân, yến tiệc); Tam kỳ lâm lộc vị; Thiên phụ thời (giờ được tha, giải nạn).
   - Hung: Thái Bạch nhập Huỳnh / Huỳnh nhập Thái Bạch (trộm cắp, giặc đến/đi); Phục cung, Phi cung, Phục can, Phi can (tranh chấp, chủ khách bất lợi); Đại cách, Tiểu cách, Hình cách, Tuế/Nguyệt/Nhật/Thời cách (trở ngại, kiện tụng, đi xa bất lợi); Bạch Hổ xương cuồng, Thanh Long đào tẩu (hao tài, phản bội); Chu Tước đầu giang, Đằng Xà yểu kiểu (văn thư, thị phi, lo sợ hão); Thiên võng tứ trương (bế tắc); Lục nghi kích hình, Tam kỳ nhập mộ (mất lực, bị hãm); Môn bức (cát môn bị bức thì việc tốt khó thành, hung môn bị bức thì hung thêm); Tinh/Môn phục ngâm (đình trệ, nên giữ), phản ngâm (lật ngược, đi rồi về); Ngũ bất ngộ thời (giờ xấu cho việc lớn); Thời mộ – can giờ nhập mộ (việc mờ mịt, không nên khởi sự).
   - Không tự gán thêm cách cục ngoài bảng; nếu người dùng hỏi một cách không có trong bảng, nói rõ script chưa tính.
9. Chỉ trả lời câu hỏi đã nêu, nói mức độ chắc chắn.

### 4.5 Đại Lục Nhâm
1. **Khóa thể** (tên in ở dòng TAM TRUYỀN) cho biết tính chất việc: Trùng thẩm/Nguyên thủ (việc thuận chiều, rõ ràng; Trùng thẩm là dưới lấn trên, phải làm lại), Tỷ dụng (nhiều việc, chọn cái gần mình), Thiệp hại (gian nan, dây dưa, phải vượt khó), Dao khắc (việc từ xa, chậm, ít lực), Mão tinh (ẩn khuất, chờ đợi), Biệt trách (nhờ người khác, không trọn), Bát chuyên (việc trong nhà, lẫn lộn), Phục ngâm (đình trệ, chờ), Phản ngâm (lật ngược, đi về).
2. **Tam truyền**: Sơ = khởi đầu/nguyên nhân, Trung = diễn biến, Mạt = kết cục. Xem ngũ hành tam truyền **sinh hay khắc can ngày** (can ngày = người hỏi): Mạt sinh can ngày hoặc là Thê tài/Tử tôn hợp việc là tốt; Quan quỷ khắc can ngày là áp lực. Truyền rơi vào **Không vong** thì việc đó hư, chưa tới.
3. **Lục thân** theo việc: hỏi tiền xem Thê tài; hỏi công danh xem Quan quỷ (có người khắc chế là có trật tự); hỏi giấy tờ, nhà cửa xem Phụ mẫu; hỏi con cái, thuốc xem Tử tôn.
4. **Thiên tướng**: Quý Nhân, Thanh Long, Lục Hợp, Thái Thường, Thái Âm, Thiên Hậu là cát; Đằng Xà (lo sợ), Chu Tước (khẩu thiệt, giấy tờ), Câu Trận (tranh chấp, trì trệ), Thiên Không (hư), Bạch Hổ (tang bệnh, nhanh), Huyền Vũ (mất mát, mờ ám) là hung. Ưu tiên xem thiên tướng trên Sơ truyền và trên khóa 1 (người hỏi), khóa 3 (việc/nhà).
5. Lục Nhâm phức tạp; chỉ luận ở mức khóa thể, tam truyền, lục thân, thiên tướng, không vong. Không tự suy thêm thần sát Lục Nhâm.

### 4.6 Mai hoa dịch số
1. **Thể** là người hỏi/việc chính, **Dụng** là sự việc/đối phương. Script in sẵn quan hệ Dụng–Thể và vượng suy của Thể theo mùa.
2. Thứ tự đọc: quẻ Chủ (hiện tại) → Hỗ (diễn biến) → Biến (kết cục); xem từng quẻ sinh hay khắc Thể. Dụng sinh Thể hoặc Thể khắc Dụng là thuận; Dụng khắc Thể là nghịch; Thể sinh Dụng là hao.
3. Có thể nói thêm ý nghĩa tượng quẻ phổ biến (Thái = thông suốt, Bĩ = bế tắc, Cách = đổi mới…), nhưng kết luận chính dựa vào thể dụng.
4. Mai hoa coi trọng "động cơ" khởi quẻ: nếu người dùng tự đưa 2 số thì dùng `--so`; nếu không, lập theo thời gian lúc hỏi.

### 4.7 Chọn ngày giờ tốt
1. Script chấm điểm gộp nhưng **phải luận từ cột chi tiết**: ưu tiên ngày **Hoàng đạo**, **Trực hợp việc**, **sao cát**, không Tam Nương, Nguyệt Kỵ, Dương Công, không xung tuổi người chủ sự.
2. **Tuổi theo năm**: Kim Lâu xét cho cưới hỏi (thường tính tuổi mụ cô dâu) và làm nhà; Hoang Ốc, Tam Tai xét khi làm nhà, động thổ. Nếu phạm, nói các cách dân gian thường làm (mượn tuổi người khác đứng ra làm, hoặc lùi năm) như kinh nghiệm tham khảo, không ép.
3. Đưa ra 2–3 ngày tốt nhất kèm **giờ Hoàng đạo**, nói lý do chọn; nếu ngày tốt rơi vào cuối tuần hay ngày người dùng tiện thì nêu.
4. `tvbt.py chonngay` dùng các tiêu chí phổ biến của lịch Việt Nam, kể cả **Thọ tử, Sát chủ dương/âm, Vãng vong** (theo tháng âm, từ 11/2026); Ngọc hạp thông thư đầy đủ (việc nên/kiêng, cát thần, hung sát) có ở `nc.py ngay` (xem `docs/chon-ngay.md`). Kim Lâu, Hoang Ốc, Tam Tai xét theo **năm âm lịch** của các ngày đang chọn (tháng 1 dương lịch trước Tết vẫn là năm âm cũ).
5. **Làm nhà, sửa nhà, đặt mộ: hỏi tọa/hướng** (độ la bàn hoặc tên sơn) rồi chạy `nc.py ngay … --toa/--huong` (từ 11/2026). Ngày phải hợp cả tọa sơn theo năm, tháng, ngày (Tuế phá, Tam sát, Âm phủ, Niên khắc sơn gia…), không chỉ hợp tuổi – xem `docs/chon-ngay.md` mục 4.2.

## Điểm khác nhau giữa các trường phái (đã chọn mặc định – nói rõ khi liên quan)
- **Trụ năm/tháng** theo tiết khí (Lập Xuân); **Tử vi và cung phi** theo năm âm lịch (Tết). Nếu cung phi theo Lập Xuân khác thì script in thêm phương án đó.
- **Giờ**: mặc định giờ mặt trời thực. Nhiều thầy ở Việt Nam dùng giờ đồng hồ (`--gio-dong-ho`). Nếu hai cách cho ra hai giờ khác nhau thì phải nêu cả hai.
- **Tử vi** an theo sách Việt Nam phổ biến (Thái Thứ Lang):
  - Hỏa/Linh: Dương Nam, Âm Nữ thì Hỏa đi thuận, Linh đi nghịch. Tuổi Tỵ Dậu Sửu: Hỏa khởi ở Mão, Linh khởi ở Tuất. Sách Vu Thiên thì Hỏa khởi ở Tuất, Linh khởi ở Mão.
  - Thiên Quý: từ Văn Khúc đếm nghịch đến ngày sinh, lùi 1 cung.
  - Khôi Việt: "Canh Tân phùng Mã Hổ" (Canh: Khôi ở Ngọ, Việt ở Dần). Có sách theo "Giáp Mậu Canh Ngưu Dương" (Canh: Sửu, Mùi).
  - Tứ hóa theo bảng chủ lưu (Toàn Tập/Trung Châu, đa số sách và web Việt Nam): Canh là Nhật, Vũ, Âm, Đồng (Thái Âm hóa Khoa, Thiên Đồng hóa Kỵ); Nhâm là Lương, Tử, Tả, Vũ. Dị bản (Toàn Thư, sách cụ Thiên Lương): Canh có Thiên Đồng Khoa, Thái Âm Kỵ; Nhâm có Thiên Phủ Khoa. Phi hóa dùng cùng bảng này.
  - Thiên Giải: từ cung Thân đếm thuận đến tháng sinh (có sách đếm nhảy cung). Phá Toái: tuổi Tý Ngọ Mão Dậu ở Tỵ, Dần Thân Tỵ Hợi ở Dậu, Thìn Tuất Sửu Mùi ở Sửu (có phần mềm đảo hai nhóm đầu).
  - Thiên Trù can Quý ở Tuất (theo sách Việt Nam; một số phần mềm Trung Quốc để Hợi).
  - Thân chủ tuổi Tý và tuổi Ngọ: sách ghi Linh Tinh hay Hỏa Tinh khác nhau.
  - Tháng nhuận: ngày 16 trở đi an như tháng sau.
  - Giờ Tý muộn (23h–24h) tính là giờ Tý của ngày hôm sau.
- Bảng độ sáng 14 chính tinh theo sách Việt Nam (tham khảo lasotuvi, giấy phép MIT). Từ bản 11/2026 bảng lá số còn **hiển thị** độ sáng Thiên Phủ (miếu Dần Thân Tý Ngọ, vượng Thìn Tuất, đắc Tỵ Hợi Mùi, bình Mão Dậu Sửu) và 7 phụ tinh (Văn Xương, Văn Khúc, Thiên Mã, Thiên Hình, Thiên Diêu, Thiên Khốc, Thiên Hư) theo bài từng sao trên tuvi.vn; các phép chấm cách cục, vận thế vẫn dùng bảng cũ. Hai chỗ các nguồn Việt Nam không thống nhất: Thiên Mã ở Thân (bài viết tuvi.vn ghi đắc, ảnh lá số tuvi.vn ghi hãm, cụ Thiên Lương ghi "kém") và Thiên Hư ở Thân (bài viết ghi hãm, ảnh lá số tuvi.vn ghi đắc, có sách Trung Quốc ghi miếu). Script theo bài viết; nói rõ khi luận đúng hai chỗ này.
- **Mệnh chủ** an theo chi **năm sinh** (sách Việt Nam, tuvi.vn, lasotuvi); script in thêm Mệnh chủ theo chi **cung Mệnh** (sách Trung Quốc) khi hai cách khác nhau. Thân chủ theo năm sinh ở cả hai phái.
- **Lưu Hà** (cát hung theo can năm): giáp Dậu, ất Tuất, bính Mùi, đinh Thân, mậu Tỵ, kỷ Ngọ, canh Thìn, tân Mão, nhâm Hợi, quý Dần (lasotuvi đảo đinh/canh – không theo).
- **Cân lượng** (xương cốt, Viên Thiên Cương): cộng số chỉ của năm (60 hoa giáp), tháng âm, ngày âm, giờ. Bảng năm theo hai nguồn trùng nhau; một nguồn khác ghi Kỷ Sửu 8 chỉ, Quý Hợi 7 chỉ (script dùng 7 và 6). Tháng nhuận tính như tháng an sao.
- **Thần sát Bát tự**: Thiên Ất Quý Nhân theo "Giáp Mậu Canh ngưu dương… Lục Tân phùng mã hổ" (khác Khôi Việt của Tử vi); xét từ cả can ngày và can năm (cũng vậy với Văn Xương, Thái Cực). Các sao theo tam hợp xét từ cả chi năm và chi ngày. Dương Nhận chỉ tính can dương (có phần mềm tính cả can âm: Ất Dần, Đinh Tỵ…). Kim Dư, Quốc Ấn chỉ xét từ **can ngày** (có phần mềm xét thêm can năm). Hồng Diễm can Ất lấy Thân (câu "Giáp Ất Ngọ Thân" – có bản đọc Ất ở Ngọ). Thiên La/Địa Võng: tứ trụ có đủ cả Tuất và Hợi / Thìn và Tỵ (Tam Mệnh Thông Hội còn một phép theo nạp âm năm: mệnh Hỏa gặp Tuất Hợi, mệnh Thủy Thổ gặp Thìn Tỵ). Không vong chỉ xét theo tuần của trụ ngày (có phái xét thêm theo trụ năm); dòng "Tuần không" ghi trụ nào rơi vào.
- **Kỳ môn**: thời gia, **chuyển bàn**. Định cục mặc định **hủy bổ** (tiết khí theo thời điểm thực, nguyên theo phù đầu); có phép **trí nhuận** (siêu thần, tiếp khí, nhuận kỳ ở Mang Chủng/Đại Tuyết). Ngưỡng nhuận: phần mềm hiện nay nhuận khi phù đầu đến trước Hạ/Đông Chí từ 9 ngày (theo ngày lịch); lệ Khang Hy 57 nhuận ở 8 ngày (`--nhuan-nguong 8`). Phi bàn, âm bàn (phái Vương Phượng Lân), nhật/nguyệt/niên gia có ở `--kymon-ban` / `--kymon-gia` (xem `docs/ky-mon.md`); khắc gia không được tính. Trung cung ký Khôn. Tam kỳ nhập mộ lấy Ất, Bính ở Càn, Đinh ở Cấn (có sách lấy Ất ở Khôn). Phục cung/Phi cung lấy Canh–Mậu theo bảng thập can khắc ứng phổ biến; Cửu độn có dị bản (Thiên độn: Sinh môn + Bính trên Đinh hoặc Mậu). Bát thần: dương độn thuận, âm độn nghịch (Trực Phù, Đằng Xà, Thái Âm, Lục Hợp, Bạch Hổ, Huyền Vũ, Cửu Địa, Cửu Thiên); có phần mềm đặt âm độn đi thuận, và phái cổ dùng Câu Trận/Chu Tước.
- **Lục Nhâm**: Nguyệt tướng đổi theo trung khí (không theo tháng âm); Quý nhân theo "Giáp Mậu Canh ngưu dương, Ất Kỷ thử hầu, Bính Đinh trư kê, Nhâm Quý xà thố, Lục Tân mã hổ" (trú trước, dạ sau), trú/dạ theo giờ Mão–Thân; Thiệp hại đếm theo ký can của địa bàn, bằng nhau thì xét Mạnh, Trọng, rồi can/chi thượng thần. Có phái đếm theo tàng can, hoặc bỏ đếm mà xét Mạnh–Trọng–Quý ngay.
- **Mai hoa**: số năm theo chi năm âm lịch (Tý = 1), tháng và ngày âm lịch Việt Nam, giờ Tý = 1; 23h tính sang ngày mới.
- **Chọn ngày**: Hoàng/Hắc đạo mặc định theo **tháng âm lịch** (như phần lớn lịch Việt Nam); sách Trung Quốc và lunar-python tính theo tháng tiết khí (`--hoang-dao-tiet`). 12 Trực luôn theo tiết khí. Trực nào hợp việc nào là kinh nghiệm phổ biến, các sách chênh nhau.
  - Dương Công kỵ nhật theo lịch Việt Nam: 13/1, 11/2, 9/3, 7/4, 5/5, 3/6, **8/7**, 29/7, 27/8, 25/9, 23/10, 21/11, 19/12 (không xét tháng nhuận). Sách Trung Quốc (杨公忌, 6tail/lunar) ghi **1/7** thay cho 8/7.
  - Thọ tử theo lịch Việt Nam là **một can chi** mỗi tháng âm (Bính Tuất, Nhâm Thìn, Tân Hợi, Đinh Tỵ, Mậu Tý, Bính Ngọ, Ất Sửu, Quý Mùi, Giáp Dần, Mậu Thân, Tân Mão, Tân Dậu); sách Trung Quốc (受死) chỉ xét chi nên nhiều ngày hơn.
  - Sát chủ dương (Tý, Sửu, Sửu, Tuất, Thìn, Thìn, Sửu, Thìn, Sửu, Thìn, Mùi, Thìn) kỵ làm nhà, nhà đất, cưới hỏi; Sát chủ âm (Tỵ, Tý, Mùi, Mão, Thân, Tuất, Hợi, Sửu, Ngọ, Dậu, Dần, Thìn) kỵ an táng; sách *Ngọc Hạp Chánh Tông* (tr. 128–129) ghi bảng này kỵ cất nhà, cưới gả, nên script loại cả cưới hỏi và động thổ. Tháng 7 Hợi, tháng 8 Sửu theo thơ Hán văn trong sách. Bảng đảo Sửu/Hợi (theo thơ Nôm) chỉ dùng để tránh thêm khi an táng. Vãng vong theo tháng âm (Dần, Tỵ, Thân, Hợi, Mão, Ngọ, Dậu, Tý, Thìn, Mùi, Tuất, Sửu); `nc.py ngay` xét thêm bản tháng tiết (往亡 của Hiệp Kỷ).

## Giới hạn – phải nói khi liên quan
- Đây là tri thức văn hóa truyền thống để tham khảo, không phải dự báo khoa học.
- Lịch âm trước 1968, và một số ngày trăng mới rơi sát nửa đêm, có thể lệch ±1 ngày so với lịch in thời đó.
- `tvbt.py` chỉ lập phần cơ bản; các phần sau nằm ở lệnh khác: Thế quái, Thành môn, đả kiếp Huyền không (`nc.py huyenkhong`); Lục hào nạp giáp (`nc.py luchao`); Ngọc hạp thông thư khi chọn ngày (`nc.py ngay`); thần sát Lục Nhâm (`nc.py lucnham2`); Kỳ môn phi bàn / âm bàn / niên-nguyệt-nhật gia / khắc ứng đầy đủ (`--kymon-ban`, `--kymon-gia`, xem `docs/ky-mon.md`). Không tính ở đâu cả: Kỳ môn khắc gia, bột cách, Thái Ất. (Thời mộ – giờ Bính Tuất, Đinh Sửu, Mậu Tuất, Nhâm Thìn, Quý Mùi – có từ 11/2026.)
- Bảng tỉnh/thành có sẵn khoảng 90 địa danh; nơi khác thì phải tra kinh độ (sai 0,5° ≈ 2 phút giờ mặt trời).
- Nếu người dùng muốn **lưu lá số** để xem lại thì đề nghị lưu các bảng số liệu vào tài liệu hoặc project của họ.

## Đã kiểm chứng (phần cơ bản)
- Tứ trụ: so với phép tính thiên văn độc lập (ephem) và ngày Julius trên ~4.000 mẫu, gồm 1.500 mẫu sát giờ giao tiết: 0 lỗi.
- Khởi đại vận (600 mẫu) và giờ mặt trời thực (sai số dưới 1 phút).
- Âm lịch Việt Nam (UTC+7): chuyển qua lại không lỗi trong 400 năm. Đúng các mốc Việt Nam và Trung Quốc lệch nhau: Tết 1985 (21/1 so với 20/2), Tết 2007, Tết 1968; năm 1985 nhuận tháng 2.
- Tử vi: các sao mà hai phái an giống nhau thì khớp 100% với thư viện iztro trên 3.000 lá số. Gồm 14 chính tinh, Cục, can cung, đại/tiểu hạn, Tứ hóa, các vòng Tràng sinh, Bác sĩ, Thái Tuế và khoảng 40 phụ tinh.
- Cung phi 1900–2099, bảng Bát trạch, Cửu tinh năm/tháng 1901–2099, 28 cục Huyền không chuẩn: 0 lỗi.
- Thần sát Bát tự: các sao suy ra được từ vòng Trường sinh (Lộc, Dương Nhận, Văn Xương, Kim Dư, Dịch Mã, Đào Hoa, Hoa Cái, Tướng Tinh, Kiếp Sát, Vong Thần) được đối chiếu chéo với quy tắc gốc: 0 lỗi; các bảng còn lại theo Tam Mệnh Thông Hội.
- Thần sát Bát tự (rà soát 11/2026): so từng trụ với thư viện độc lập `cantian-tymext` (npm, bản 0.0.27) trên 5.000 tứ trụ ngẫu nhiên (20.000 trụ): 25 sao khớp 100% – Thiên Ất, Thái Cực, Văn Xương, Lộc thần, Lưu Hà, Dịch Mã, Đào Hoa, Hoa Cái, Tướng Tinh, Kiếp Sát, Vong Thần, Cô Thần, Quả Tú, Hồng Loan, Thiên Hỷ, Thiên Đức, Thiên Đức hợp, Nguyệt Đức, Nguyệt Đức hợp, Thiên Y, Thiên Xá, Khôi Cương, Âm Dương Sai Thác, Thập Ác Đại Bại, Cô Loan. Chỗ khác chỉ là lựa chọn trường phái đã ghi ở trên (Dương Nhận can âm, Kim Dư/Quốc Ấn theo can năm, Hồng Diễm can Ất). Từng bảng cũng được dò lại bằng tay theo câu phú gốc.
- Quan hệ can chi: lục hợp, lục xung, hình (kể cả tự hình), hại, phá trên đủ 144 cặp chi, ngũ hợp và tương xung trên đủ 100 cặp can: khớp `cantian-tymext`, 0 lỗi.
- Tử vi – các tầng vận hạn (rà soát 11/2026): so với iztro 2.6.5 (`horoscope`) trên 6.000 cặp (lá số ngẫu nhiên 1900–2098, năm xem ngẫu nhiên): tuổi mụ, cung tiểu hạn, cung đại hạn, tứ hóa đại hạn (theo can cung đại hạn), tứ hóa lưu niên, Lưu Lộc Tồn, Kình, Đà, Mã, Xương, Khúc, Hồng Loan, Thiên Hỷ, Thái Tuế, Tang Môn, Bạch Hổ, Đào Hoa, Kiếp Sát, cung tháng theo Đẩu Quân, can tháng, cung ngày (lưu nhật): 0 lỗi. Chỗ khác đều là lựa chọn đã ghi: Lưu Khôi/Việt năm Canh (Mã Hổ), tháng nhuận dùng chung cung với tháng chính (iztro chia đôi từ ngày 16).
- Chạy thử ngẫu nhiên (fuzz) 8.100 lần các lệnh `battu tuvi` (kèm `--phi-hoa --luu-nguyet --so-nam`), `tatca`, `hoptuoi`, `nc.py vuongsuy | cachcuc | vanthe | luunhat | hoptac` với ngày 1900–2099 (dồn nhiều vào 1900–1920, 2050–2099, 1955–1976), ngày âm và tháng nhuận, 23h–1h, sát tiết, miền Nam, nước ngoài, `--ty 2`, `--gio-dong-ho`: không lỗi chương trình (chỉ có thông báo LỖI đúng chỗ cho ngày âm không tồn tại).
- Chọn ngày: can chi ngày, 12 Trực, 28 Tú (kèm cát/hung), thần trực nhật Hoàng/Hắc đạo, giờ Hoàng đạo khớp lunar-python trên 40.543 ngày (1950–2060): 0 lỗi.
- Kỳ môn: khớp sao, môn, can thiên bàn và địa bàn với hai bàn mẫu đã công bố (âm độn 9 cục; âm độn 4 cục của Trần Hồng Bình); định cục hủy bổ đúng ví dụ "Tiểu Tuyết trung nguyên âm 8 cục" (26/11/2020). Định cục **trí nhuận** đúng 9 lệ siêu thần/tiếp khí/nhuận trong sách: Vạn Lịch Kỷ Sửu 1589 (Đại Tuyết nhuận kỳ – Hoàng Tông Hy, *Dịch học tượng số luận*), Khang Hy 57/1718 (Mang Chủng nhuận, khi đặt ngưỡng 8), Mang Chủng 2016 nhuận, Kinh Trập 2017 tiếp khí 3 ngày, Đông Chí 1990 tiếp khí 3 ngày, Đại Hàn 1990 siêu thần 6 ngày, Xuân Phân 1989 chính thụ…; chạy 1901–2099 không lỗi, độ lệch phù đầu luôn trong −7…+12 ngày. Chạy toàn bộ 24 tiết × 60 ngày × 60 giờ (cả nhận diện cách cục) không lỗi.
- Lục Nhâm: đúng 16/16 khóa mẫu trong sách (Tỷ dụng, Thiệp hại – Kiến cơ, Sát vi, Phục đẳng, Dao khắc – Hao thỉ, Đạn xạ, Phục ngâm, Phản ngâm), kể cả số lần khắc khi đếm thiệp hại. Phân bố 720 khóa: Mão tinh 16, Biệt trách 9, Bát chuyên 16, Phục ngâm 60, Phản ngâm 60, khớp số liệu kinh điển.
- Kỳ môn (đối chiếu 11/2026 với hai thư viện độc lập):
  - **taobi** (npm, chuyển bàn, ký Khôn): toàn bộ 18 cục × 60 giờ = 1.080 bàn trùng 100% ở địa bàn, thiên bàn (can, sao), bát môn, bát thần, trực phù.
  - Định cục hủy bổ và Mao Sơn trên 11.455 thời điểm ngẫu nhiên 1950–2050 (giờ Bắc Kinh, gồm khoảng 3.000 thời điểm cách giao tiết dưới 3 giờ): trùng hết, trừ 5 trường hợp cách giao tiết dưới 1 phút (sai số lịch thiên văn) và các lỗi của chính taobi (giờ mùa hè Trung Quốc 1986–1991, Mao Sơn đầu tháng 1).
  - **kinqimen** (Python, Kenneth Tse): cục hủy bổ trùng 230/230; khác ở bát thần dương độn (họ dùng Câu Trận/Chu Tước – khác trường phái đã ghi) và toàn bộ sao/môn/thần âm độn (thứ tự cung âm độn của họ không liền kề – lỗi của họ).
  - Thiên phụ thời ngày Giáp/Kỷ: sửa 11/2026 (bảng cũ ghi giờ Kỷ Hợi nên không bao giờ khớp); nay nhận Kỷ Tỵ và Giáp Tuất (hai phái).
  - Thử tham số: khoảng 8.000 lần chạy ngẫu nhiên 1900–2099 với mọi tổ hợp `--kymon-phep`, `--kymon-ban`, `--kymon-gia`, `--nhuan-nguong`, `--nam-sinh`, `--gio-dong-ho`, giờ Tý muộn, sát giao tiết (kèm `nc.py lucnham2`, `nc.py hoichan`): không lỗi; năm ngoài 1900–2099 báo LỖI rõ ràng.
- Lục Nhâm (đối chiếu 11/2026 toàn bộ 8.640 khóa = 60 ngày × 12 nguyệt tướng × 12 giờ với **liuren-ts-lib**, npm): thiên bàn, tứ khóa, thiên tướng (Quý nhân trú/dạ và chiều thuận/nghịch), độn can, không vong trùng 100%; tam truyền trùng 8.400/8.640. 240 khóa khác (20 khóa × 12 giờ) đều là Thiệp hại: thư viện xét Mạnh – Trọng ngay, script đếm sâu trước (trường phái đã ghi). **kinliuren** (Python) sai nhiều ở Phục ngâm, Bát chuyên, Tỷ dụng nên không dùng làm chuẩn.
- Mai hoa: đúng ví dụ kinh điển "Quan mai chiêm" (Trạch Hỏa Cách, hào 1 động, hỗ Thiên Phong Cấu, biến Trạch Sơn Hàm); 64 quẻ không trùng. Rà soát 11/2026: quẻ chủ/hỗ/biến khớp thư viện PyPI `meihuayishu` 0.1.3 trên đủ 64 quẻ × 6 hào động (384 tổ hợp); công thức lập theo thời gian (51.840 tổ hợp năm/tháng/ngày/giờ) và theo 2 số (3.481 cặp) khớp. Dòng "Biến quái" chỉ xét quái Dụng đã biến (quái kia của quẻ biến chính là Thể).
- Huyền không (rà soát 11/2026): vận bàn, sơn tinh, hướng tinh của **hạ quái và thế quái** khớp hai bản cài đặt độc lập trên GitHub (voidforall/fengshui.skill – bảng thay sao Thẩm thị; kth2/hidefate `independent_xuankong.py`, phương án sao 5 không thay) ở 9 vận × 24 sơn × 5 độ lệch trong sơn (2.160 bàn, 0 lỗi); 4 cục, phục/phản ngâm, hợp thập, liên châu, phụ mẫu tam ban khớp; niên tinh 1864–2100 và nguyệt tinh 1900–2100 khớp. Ranh giới sơn: script tính [tâm − 7,5°, tâm + 7,5°) (đúng 7,5° thuộc sơn sau); có bản tính (…] – chỉ khác đúng ở vạch, nơi đã báo không vong.
- Lục hào (rà soát 11/2026): khớp thư viện PyPI `najia` 2.0.1 trên đủ 4.096 tổ hợp hào (cung, thế ứng, nạp giáp, lục thân quẻ chủ và quẻ biến, cung quẻ biến, phục thần, lục xung, lục hợp, du hồn, quy hồn) và 60 can chi ngày (lục thần, tuần không): 0 lỗi.
- Chọn ngày (rà soát 11/2026): Tam Nương, Nguyệt Kỵ, Dương Công (13 ngày bản Việt Nam), Tam Tai, Hoang Ốc (10 tuổi khởi Nhất Cát, mỗi chục sang một cung, số lẻ đếm tiếp), Kim Lâu (tuổi mụ chia 9 dư 1, 3, 6, 8) khớp nguồn lịch Việt Nam; Thọ tử, Sát chủ, Vãng vong theo 2–4 nguồn (xem phần trường phái). Bất biến 1950–2060: ngày Thọ tử không bao giờ vào nhóm chọn; Sát chủ dương không vào nhóm chọn khi cưới, làm nhà, nhập trạch, khai trương; Vãng vong không vào nhóm chọn khi đi xa, cưới, nhập trạch; Sát chủ âm không vào nhóm chọn khi an táng, cưới, động thổ. lunar-python 1.4.8 có 3 dòng thần sát nhập sai (tháng Hợi ngày Kỷ Sửu: cả dòng cát/hung là của ngày khác, có Hà Khôi, Lục Hợp mà thiếu Nguyệt Yếm, Quy Kỵ; tháng Mùi ngày Quý Dậu: dòng hung sát của ngày khác; tháng Dậu ngày Kỷ Dậu: Nguyệt Yếm thay Nguyệt Hình – 170 ngày trong 1950–2060), `nc.py ngay` đã tự sửa; Thiên Cương, Hà Khôi, Nguyệt Yếm, Nguyệt Phá, Vãng Vong, Quy Kỵ đối chiếu quy tắc gốc (và cnlunar) trên 40.543 ngày: ngoài 3 dòng trên không lệch. Một vài dòng khác có dấu hiệu lệch nhưng chưa đủ căn cứ để sửa (vd tháng Thân ngày Mậu Ngọ thiếu Tai Sát, Thiên Hỏa).
- Phong thủy (rà soát 11/2026): độ → 24 sơn → cung đúng ở mọi ranh giới 7,5° + 15°k; bảng du niên 8 cung phi × 8 hướng khớp "Đại du niên ca" (thượng biến Sinh Khí, trung Ngũ Quỷ, hạ Diên Niên, trung Lục Sát, thượng Họa Hại, trung Thiên Y, hạ Tuyệt Mệnh, trung Phục Vị). Chạy thử ngẫu nhiên 600 lệnh phongthuy/huyenkhong/luchao/maihoa/chonngay/ngay: chỉ còn lỗi khi `--huong nan/inf` – đã chặn.
