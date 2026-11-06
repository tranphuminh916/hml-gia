# -*- coding: utf-8 -*-
"""kiemtra.py - Tự kiểm tra TOÀN BỘ bộ script (chạy từ thư mục chứa tvbt/): python3 tvbt/kiemtra.py
Gồm: (1) phần cơ bản (Bát tự, Tử vi, Phong thủy, Kỳ môn, Lục Nhâm, Mai hoa, chọn ngày),
(2) luận chi tiết (lưu niên, lưu nguyệt, vận hạn nhiều năm, hợp tuổi), (3) Kỳ môn mở rộng,
(4) các module nâng cao (nc.py tukiem), (5) dò giờ sinh (giosinh.py), (6) các mục đối chiếu cách trình bày
Việt Nam (Mệnh chủ, Lưu Hà, cân lượng, độ sáng phụ tinh, sao lưu thêm, cung đại vận/lưu niên, nguyệt hạn tiểu hạn).
In 'TỰ KIỂM TRA TOÀN BỘ: ĐẠT' khi mọi phần đều đạt."""
import datetime as dt
import os
import subprocess
import sys

sys.path.insert(0, "tvbt")


def chay(*a):
    return subprocess.run([sys.executable, "tvbt/tvbt.py"] + list(a), capture_output=True, text=True).stdout


def thieu(t, need):
    return [x for x in need if x not in t]


def phan_co_ban():
    miss = []
    t = chay("tatca", "--ngay", "2000-01-01", "--gio", "10:00", "--gioi", "nam", "--noi", "Hà Nội", "--nam-xem", "2026",
             "--huong", "180", "--nam-xay", "2010", "--phi-hoa")
    miss += thieu(t, ["| Năm | Kỷ Mão", "| Tháng | Bính Tý", "| Ngày | Mậu Ngọ", "| Giờ | Đinh Tỵ", "Cục: Thổ Ngũ Cục",
                      "Mệnh tại Mùi, Thân tại Tỵ", "| Mệnh | Mùi (Tân) | Vô chính diệu | Kình Dương(Đ)", "(Tết): Khảm",
                      "| Bắc (TỌA) | 4 | 9 | 7 |", "Cục: Song tinh đáo hướng", "| 2008 | 2017 | 10-19 | Ất Hợi",
                      "| Lộc thần (Kiến Lộc) | can ngày Mậu → Tỵ | Giờ |", "Lai nhân cung: Phu Thê (Tỵ)",
                      "| Mệnh Mùi (Tân) | Cự Môn → Thiên Di | Thái Dương → Tài Bạch | Văn Khúc → Phúc Đức | "
                      "Văn Xương → Phu Thê |",
                      "- Nhà hướng 180.0°: hướng Nam, tọa Bắc → Khảm trạch (Đông tứ trạch",
                      "hướng nhà là Diên Niên (cát), tọa là Phục Vị (tiểu cát); nhà cùng nhóm với mệnh"])
    t = chay("tatca", "--ngay", "1968-03-15", "--gio", "08:00", "--gioi", "nu", "--noi", "Hà Nội", "--nam-xem", "2026")
    miss += thieu(t, ["| Năm | Mậu Thân", "| Ngày | Giáp Thân", "| 1971 | 1980 | 4-13 | Giáp Dần", "Cục: Thủy Nhị Cục",
                      "Mệnh tại Hợi, Thân tại Mùi", "(Tết): Khảm", "CỬU TINH NĂM 2026"])
    t = chay("kymon", "lucnham", "maihoa", "--ngay", "2020-11-26", "--gio", "15:34", "--utc", "8", "--kinhdo", "116.4",
             "--gio-dong-ho")
    miss += thieu(t, ["Âm độn 8 cục, Trung nguyên (phù đầu Kỷ Tỵ)",
                      "| Càn (Tây Bắc) | Trực Phù | Thiên Xung | Quý | Thương môn (hung) | Canh | Trực phù, Trực sử |",
                      "khóa thể: Phản ngâm – Trùng thẩm", "| Chủ (hiện tại) | Sơn Địa Bác | Cấn Thổ / Khôn Thổ |",
                      "| Khôn (Tây Nam) | Chân trá | cát | Hưu môn + Bính + Thái Âm |",
                      "| Chấn (Đông) | Chu Tước đầu giang | hung | Đinh thiên bàn trên Quý địa bàn |",
                      "Vượng suy bát môn theo tháng Hợi: Khai hưu, Hưu vượng"])
    t = chay("chonngay", "--tu", "2026-11-01", "--den", "2026-11-20", "--tuoi", "Chị:1984", "--viec", "khaitruong")
    miss += thieu(t, ["| T2 09/11/2026 | 1/10 | Đinh Hợi | Kim Đường (Bảo Quang) (Hoàng đạo) | Kiến | Trương (cát) |  | +4 |",
                      "| T3 03/11/2026 | 25/9 | Tân Tỵ | Minh Đường (Hoàng đạo) | Nguy | Chủy (hung) | Dương Công kỵ nhật | -4 |",
                      "Hoang Ốc: Nhất Cát (tốt); không Tam Tai"])
    # rà soát 11/2026: Kim Lâu/Hoang Ốc/Tam Tai theo NĂM ÂM LỊCH (tháng 1/2027 dương lịch vẫn là năm Bính Ngọ 2026)
    t = chay("chonngay", "--tu", "2027-01-05", "--den", "2027-01-20", "--tuoi", "Cô dâu:1998", "--viec", "cuoi")
    miss += thieu(t, ["năm âm lịch 2026 (Bính Ngọ, tuổi mụ 29): không phạm Kim Lâu; Hoang Ốc: Ngũ Thọ Tử (xấu)"])
    if "năm âm lịch 2027" in t:
        miss.append("chonngay lấy năm dương lịch 2027 cho tháng 1/2027")
    # Thọ tử, Sát chủ dương (09/04/2026 = 22/2 Quý Sửu, kèm Tam Nương), Vãng vong
    t = chay("chonngay", "--tu", "2026-04-09", "--den", "2026-04-09", "--viec", "nhaptrach")
    miss += thieu(t, ["| T5 09/04/2026 | 22/2 | Quý Sửu |", "Sát chủ dương (kỵ làm nhà, cưới, nhà đất)"])
    import lucnham as L
    import maihoa as M
    import kymon as K
    C, Z = "甲乙丙丁戊己庚辛壬癸", "子丑寅卯辰巳午未申酉戌亥"

    def gz(s):
        return [i for i in range(60) if i % 10 == C.index(s[0]) and i % 12 == Z.index(s[1])][0]
    for d, tg, h, so in [("辛卯", "亥", "未", "亥卯未"), ("丙子", "亥", "辰", "子"), ("庚午", "未", "卯", "辰"),
                         ("壬申", "亥", "申", "巳"), ("乙丑", "丑", "丑", "辰丑戌"), ("丁丑", "午", "子", "亥未丑")]:
        got = "".join(Z[x] for x in L.lap(gz(d), Z.index(h), Z.index(tg))["truyen"])
        if not got.startswith(so):
            miss.append("Lục Nhâm %s: %s" % (d, got))
    # Đối chiếu 11/2026 với liuren-ts-lib (8.640 khóa): Phục ngâm ngày âm vô khắc, mạt trở về sơ thì lấy xung trung;
    # Bát chuyên ngày dương: sơ = can thượng thuận 3.
    for d, tg, h, tr in [("丁卯", "子", "子", "卯子午"), ("壬申", "子", "子", "亥申寅"), ("庚申", "子", "丑", "酉未未")]:
        got = "".join(Z[x] for x in L.lap(gz(d), Z.index(h), Z.index(tg))["truyen"])
        if got != tr:
            miss.append("Lục Nhâm %s %s tướng giờ %s: %s, đúng là %s" % (d, tg, h, got, tr))
    # Thiên phụ thời (天辅时): Giáp/Kỷ Kỷ Tỵ hoặc Giáp Tuất, Ất/Canh Giáp Thân, Bính/Tân Giáp Ngọ, Đinh/Nhâm Giáp Thìn,
    # Mậu/Quý Giáp Dần (trước 11/2026 ngày Giáp/Kỷ không bao giờ khớp vì bảng ghi nhầm Kỷ Hợi)
    for d, h in [("甲子", "己巳"), ("己卯", "甲戌"), ("乙丑", "甲申"), ("辛未", "甲午"), ("壬申", "甲辰"), ("戊辰", "甲寅")]:
        b = K.lap(gz(d), gz(h), "Đông Chí")
        if not any(x[1] == "Thiên phụ thời" for x in K.cach_cuc(b, 0, 2)):
            miss.append("Kỳ môn: ngày %s giờ %s phải là Thiên phụ thời" % (d, h))
    if any(x[1] == "Thiên phụ thời" for x in K.cach_cuc(K.lap(gz("甲子"), gz("己亥"), "Đông Chí"), 0, 2)):
        miss.append("Kỳ môn: Kỷ Hợi không phải giờ Thiên phụ")
    # Thời mộ (时干入墓): giờ Bính Tuất, Đinh Sửu, Mậu Tuất, Nhâm Thìn, Quý Mùi (thêm 11/2026)
    for d, h, co in [("丙寅", "戊戌", 1), ("乙丑", "丙戌", 1), ("庚午", "丁丑", 1), ("辛未", "壬辰", 1), ("乙丑", "癸未", 1),
                     ("甲子", "甲戌", 0)]:
        b = K.lap(gz(d), gz(h), "Đông Chí")
        if any(x[1].startswith("Thời mộ") for x in K.cach_cuc(b, 0, 2)) != bool(co):
            miss.append("Kỳ môn: ngày %s giờ %s Thời mộ phải là %s" % (d, h, bool(co)))
    for gy in range(60):          # niên gia: "giờ" của bàn là can chi năm, không được in thêm "Thời cách" trùng "Tuế cách"
        d_, c_, _ = K.cuc_nien_gia(1984 + gy)
        b = dict(K.ban(d_, c_, gy), gz_ngay=0, gia="nien")
        if any(x[1] == "Thời cách" for x in K.cach_cuc(b, gy, 2)):
            miss.append("Kỳ môn niên gia %s: in Thời cách theo can năm" % K.ten_gz(gy))
            break
    import lucnham2 as N
    for d, tg, h, ten in [("己巳", "酉", "寅", "Vô lộc"), ("庚辰", "亥", "辰", "Tuyệt tự")]:
        kc = [x[0] for x in N.phan_tich(gz(d), Z.index(h), Z.index(tg), 2, 0)["khoa_cach"]]
        if ten not in kc:
            miss.append("Lục Nhâm %s %s tướng giờ %s: thiếu khóa cách %s (Lục Nhâm đại toàn q.9)" % (d, tg, h, ten))
    for d, nguong, tiet, ghi in [(dt.date(2016, 6, 11), None, "Mang Chủng", "nhuận"),
                                 (dt.date(2017, 3, 8), None, "Kinh Trập", "tiếp khí 3"),
                                 (dt.date(1990, 12, 25), None, "Đông Chí", "tiếp khí 3"),
                                 (dt.date(1718, 6, 14), 8, "Mang Chủng", "nhuận"),
                                 (dt.date(1589, 12, 12), None, "Đại Tuyết", "nhuận")]:
        r = K.tiet_tri_nhuan(d, 8, nguong)
        if r[0] != tiet or ghi not in r[1]:
            miss.append("Trí nhuận %s: %s" % (d, r))
    q, _ = M.theo_thoi_gian(4, 12, 17, 8)
    if M.ten_que(*q["chu"]) != "Trạch Hỏa Cách" or M.ten_que(*q["bien"]) != "Trạch Sơn Hàm":
        miss.append("Mai hoa mẫu")
    import io
    from contextlib import redirect_stdout
    buf = io.StringIO()
    with redirect_stdout(buf):
        M.in_que(q, 2, "mẫu")
    if "Biến quái (Dụng biến thành): Cấn (Thổ) sinh Thể" not in buf.getvalue():
        miss.append("Mai hoa: biến quái phải là quái Dụng đã biến (Cấn)")
    return miss


def phan_luan_chi_tiet():
    L = ["--ngay", "1990-05-17", "--gio", "08:30", "--gioi", "nam", "--noi", "Hà Nội"]
    t = chay("battu", "tuvi", *L, "--nam-xem", "2026", "--luu-nguyet", "--so-nam", "10", "--luu-nien", "3")
    t += chay("tuvi", *L, "--nam-xem", "2025", "--luu-nguyet")
    t += chay("hoptuoi", *L, "--nguoi", "A:1982-03-14", "B:1993-09-27", "C:1987-08-05 am")
    return thieu(t, [
        "- Quan hệ trong tứ trụ: Ngọ (Năm) tự hình Ngọ (Ngày); Canh (Năm) xung Giáp (Giờ)",
        "| 2027 | 2036 | 38-47 | Ất Dậu | Thương Quan | Tân (Chính Ấn) | Tuyền Trung Thủy | Ất hợp (Kim) Canh (Năm); "
        "Ất xung Tân (Tháng); Dậu bán hợp Kim Tỵ (Tháng); Dậu lục hợp (Kim) Thìn (Giờ) |",
        "| 2027 | 38 | Đinh Mùi | Chính Tài |",
        "| T1 (Dần) | 04/02/2026 | Canh Dần | Thiên Ấn (Kiêu) |",
        "Tứ hóa đại hạn (can cung đại hạn Canh): Thái Dương Hóa Lộc (cung Mệnh – gốc cũng Hóa Lộc)",
        "Liêm Trinh Hóa Kỵ (cung Tật Ách)",
        "| 1 | 17/02/2026 – 18/03/2026 | Canh Dần | Thiên Di (Mùi) |",
        "| 9 | 10/10/2026 – 08/11/2026 | Mậu Tuất | Phúc Đức (Mão) | Tham Lang → Phụ Mẫu |",
        "| 6 nhuận | 25/07/2025 – 22/08/2025 | Quý Mùi | Phu Thê (Hợi) |",
        "Thái Âm → Mệnh; gốc Hóa Khoa; năm Hóa Kỵ",
        "| 2032 Nhâm Tý | 43 | Điền Trạch | Tử Tức | Huynh Đệ | Phu Thê |",
        "Nhâm Tuất – Quý Mão – Bính Thân",
        "Quý Dậu – Tân Dậu – Tân Hợi",
        "B ↔ C: năm: Quý–Đinh xung, Dậu–Mão xung, THIÊN KHẮC ĐỊA XUNG",
        "| C | 27/09/1987 (5/8/1987) | Đinh Mão – Kỷ Dậu – Kỷ Mão |"])


def phan_ky_mon():
    B = ["--utc", "8", "--kinhdo", "116.4", "--gio-dong-ho"]
    t = chay("kymon", "--ngay", "2006-12-23", "--gio", "16:00", "--kymon-ban", "phi", "--kymon-phep", "maoson", *B)
    t += chay("kymon", "--ngay", "2008-07-10", "--gio", "12:20", "--kymon-ban", "phi", "--kymon-phep", "maoson", *B)
    t += chay("kymon", "--ngay", "2005-10-06", "--gio", "20:22", "--lich-tz", "8", "--kymon-ban", "am", *B)
    t += chay("kymon", "--ngay", "2006-08-21", "--gio", "16:02", "--lich-tz", "8", "--kymon-ban", "am", *B)
    t += chay("kymon", "--ngay", "2002-05-10", "--gio", "10:00", "--kymon-gia", "nien")
    t += chay("kymon", "--ngay", "2002-05-10", "--gio", "10:00", "--kymon-gia", "nguyet")
    t += chay("kymon", "--ngay", "2002-02-26", "--gio", "10:00", "--kymon-gia", "nhat")
    t += chay("kymon", "--ngay", "2026-10-31", "--gio", "07:47", "--noi", "Hà Nội", "--nam-sinh", "1990",
              "--ve-ban", "/tmp/kmtest.png")
    miss = thieu(t, [
        "tiết Đông Chí (đã qua 31 giờ kể từ giao tiết) → Dương độn 1 cục, Thượng nguyên",
        "| Trung cung | Chu Tước | Thiên Bồng | Mậu | (không môn) | Nhâm |  |",
        "| Cấn (Đông Bắc) | Trực Phù | Thiên Phụ | Tân | Kinh môn (hung) | Bính | Mã, Trực phù |",
        "| Khôn (Tây Nam) | Lục Hợp | Thiên Nhậm | Mậu | Tử môn (hung) | Đinh | Mã, Trực sử |",
        "= 34 chia 9 dư → 7 cục",
        "| Chấn (Đông) | Trực Phù | Thiên Nhuế + Thiên Cầm | Quý + Canh | Tử môn (hung) | Nhâm | Đinh | Trực phù, Trực sử |",
        "| Trung cung |  |  |  |  | Canh | Nhâm | ký Khôn |",
        "| Khảm (Bắc) | Trực Phù | Thiên Tâm | Nhâm | Thương môn (hung) | Mậu | Đinh | Trực phù |",
        "Trực phù: Thiên Tâm → đến cung Chấn (Đông); Trực sử: Khai môn → đến cung Đoài (Tây)",
        "Trực phù: Thiên Xung → đến cung Cấn (Đông Bắc); Trực sử: Thương môn → đến cung Khôn (Tây Nam)",
        "Giáp Tý 25/02/2002, gần tiết Vũ Thủy nhất → Dương độn 7 cục",
        "| Khôn (Tây Nam) | Mậu + Đinh | Thanh Long diệu minh | cát |",
        "| Tốn (Đông Nam) | phản ngâm, môn bức (môn khắc cung) | phản ngâm, tháng phế, cung hưu | Trực Phù Thìn Mộ / Tỵ Tuyệt |",
        "| Khảm (Bắc) | phản ngâm, môn chế (cung khắc môn) | phản ngâm, tháng vượng, cung tù | Lục Hợp Tý Mộc dục | Canh: Tý Tử |",
        "can Canh nằm ở cung Khảm (Bắc)",
        "| Tốn (Đông Nam) | Khai (Kim, cát): công việc"])
    if not os.path.exists("/tmp/kmtest.html"):
        miss.append("không tạo được file HTML bàn Kỳ môn")
    return miss


def phan_nang_cao():
    r = subprocess.run([sys.executable, "tvbt/nc.py", "tukiem"], capture_output=True, text=True)
    print(r.stdout.rstrip())
    return [] if "TỰ KIỂM TRA NÂNG CAO: ĐẠT" in r.stdout else ["nc.py tukiem: " + (r.stdout + r.stderr)[-500:]]


def phan_gio_sinh():
    """Dò giờ sinh: bảng giờ, cách chấm, và lá số từng khung giờ phải trùng với tvbt.py."""
    import json
    miss = []

    def gs(*a):
        return subprocess.run([sys.executable, "tvbt/giosinh.py"] + list(a), capture_output=True, text=True).stdout
    t = gs("--ngay", "1990-03-15", "--gioi", "nam", "--noi", "Hà Nội", "--tra-loi",
           '{"khoang":"toi","xoay":"mo","ngu":"sinh","mat":"sinh","than":"Tài Bạch","tinh":["g10"],"nam":[2013]}')
    miss += thieu(t, ["| Giờ Tuất | 19:06–21:06 | 19/2 | Giáp Tuất | Tỵ | Tử Vi(M), Thất Sát(V) | Thiên Tướng(H) | Tài Bạch | Kim Tứ Cục | 74% |",
                      "| Giờ Tý (cuối ngày) | 23:06–24:00 | 20/2 | Bính Tý | Mão |",
                      "KẾT LUẬN: Giờ Tuất (19:06–21:06 giờ đồng hồ), 74% – khá rõ.",
                      "Giờ cần so thêm: Giờ Hợi (21:06–23:06)",
                      "Câu tự bỏ qua: cach (không giúp phân biệt); nam (các giờ còn lại chuyển đại hạn cùng tuổi)"])
    # bản 2: chỉ dấu hiệu dân gian thì không bao giờ "khá rõ"; tên giờ Tý chưa rõ trước/sau 12 giờ đêm thì có lưu ý
    t = gs("--ngay", "1986-07-22", "--gioi", "nam", "--noi", "Nam Định", "--tra-loi", '{"xoay":"chinh","ngu":"chinh","than":"Mệnh"}')
    miss += thieu(t, ["KẾT LUẬN: Giờ Ngọ (11:02–13:02 giờ đồng hồ), 23% – chưa rõ", "Lưu ý: Chưa có giờ gia đình nhớ"])
    t = gs("--ngay", "1986-07-22", "--gioi", "nam", "--noi", "Nam Định", "--tra-loi", '{"khoang":"tengio:0"}')
    miss += thieu(t, ["Lưu ý: Hai giờ Tý", "Câu tự bỏ qua: cach (giờ gia đình nhớ đã đủ hẹp)"])
    t = gs("--ngay", "1990-03-15", "--gioi", "nam", "--noi", "Hà Nội", "--tra-loi", '{"khoang":"sang","nam":[2013]}')
    miss += thieu(t, ["năm 2013 (24 tuổi) đúng lúc chuyển đại hạn (24 tuổi)"])
    t = gs("--ngay", "1970-05-10", "--gioi", "nu", "--noi", "TP Hồ Chí Minh", "--tra-loi", '{"khoang":{"gio":"23:40","sai":30}}')
    miss += thieu(t, ["lệch giờ đồng hồ -49 phút",
                      "| Giờ Hợi | 21:49–23:49 | 6/4 | Đinh Hợi | Ngọ | Thiên Lương(M) | Cự Môn(H) | Phu Thê | Mộc Tam Cục | 75% |",
                      "| Giờ Tý (cuối ngày) | 23:49–24:00 | 7/4 | Mậu Tý | Tỵ | Cự Môn(H) | Thái Âm(H) | Mệnh | Kim Tứ Cục | 18% |"])
    import giosinh as G
    for ngay, gioi, noi in [("1990-03-15", "nam", "Hà Nội"), ("1970-05-10", "nu", "TP Hồ Chí Minh")]:
        r = G.buoc({"ngay": ngay, "gioi": gioi, "noi": noi}, {})
        if len(r["ung_vien"]) != 13 or len(r["cau_hoi"]) != 8:
            miss.append("giosinh %s: %d khung giờ, %d câu" % (ngay, len(r["ung_vien"]), len(r["cau_hoi"])))
        for x in r["ung_vien"]:
            t = chay("tuvi", "--ngay", ngay, "--gio", x["gio_dai_dien"], "--gioi", gioi, "--noi", noi, "--nam-xem", "2026")
            if ("Mệnh tại %s," % x["menh"]) not in t or ("(Thân cư %s)" % x["than_cu"]) not in t or x["cuc"] not in t:
                miss.append("giosinh %s %s: lá số khác tvbt.py" % (ngay, x["ten"]))
    json.dumps(r, ensure_ascii=False)
    return miss


def phan_doi_chieu_viet_nam():
    """Các mục thêm 11/2026 để khớp cách trình bày phổ biến ở Việt Nam (tuvi.vn): Mệnh chủ theo năm sinh, Lưu Hà,
    cân lượng, độ sáng phụ tinh, sao lưu Khôi Việt Xương Khúc Đào Hồng Hỷ Kiếp Sát, cung đại vận/lưu niên,
    nguyệt hạn tính từ tiểu hạn. Giá trị kỳ vọng tính tay từ quy tắc gốc (lá số mẫu, không phải dữ liệu thật)."""
    import tuvi_vn as T
    miss = []
    t = chay("tuvi", "--ngay", "2000-01-01", "--gio", "10:00", "--gioi", "nam", "--noi", "Hà Nội", "--nam-xem", "2023",
             "--luu-nguyet", "--so-nam", "2")
    miss += thieu(t, [
        "Mệnh chủ: Văn Khúc (theo chi năm sinh, cách sách Việt Nam; nếu tính theo chi cung Mệnh như sách Trung Quốc: Vũ Khúc)",
        "= 5 lượng 9 chỉ",
        "| Huynh Đệ | Ngọ (Canh) | Tử Vi(M) | Lộc Tồn, Địa Không(H) | Thiên Hỷ, Thiên Giải, Lưu Hà |",
        "Đà La(H), Văn Xương(Đ), Thiên Mã(V)", "Văn Khúc(B)[Hóa Kỵ]", "Thiên Hư(Đ)",
        "LN.Mệnh tại Sửu (gốc Thiên Di)", "ĐV.Mệnh tại Tỵ (gốc Phu Thê)",
        "Lưu Thiên Khôi tại Tài Bạch (Mão), Lưu Thiên Việt tại Phu Thê (Tỵ), Lưu Văn Xương tại Tài Bạch (Mão), "
        "Lưu Văn Khúc tại Quan Lộc (Hợi), Lưu Đào Hoa tại Nô Bộc (Tý), Lưu Hồng Loan tại Nô Bộc (Tý), "
        "Lưu Thiên Hỷ tại Huynh Đệ (Ngọ), Lưu Kiếp Sát tại Phụ Mẫu (Thân)",
        "tháng Giêng tại Điền Trạch; phép tính từ cung tiểu hạn thì tháng Giêng tại Phụ Mẫu",
        "| Giáp Dần (Thất Sát) | Phụ Mẫu (Thân) |", "| Tân Dậu (Thương Quan) | Tài Bạch (Mão) |"])
    # cân lượng: bảng năm so với các giá trị đã biết (Viên Thiên Cương), tổng một lá Bính Dần tháng 6 ngày 16 giờ Tý
    i = lambda c, z: [k for k in range(60) if k % 10 == c and k % 12 == z][0]
    mau = {(0, 0): 12, (5, 3): 19, (2, 2): 6, (4, 6): 19, (9, 11): 6, (5, 1): 7, (3, 9): 14, (8, 10): 10, (7, 11): 17}
    sai = ["năm %d %d" % k for k, v in mau.items() if T.CL_NAM[i(*k)] != v]
    if sai or T.can_luong(2, 2, 6, 16, 0)[0] != 46 or sum(T.CL_THANG) != 125 or len(T.CL_NGAY) != 30:
        miss.append("bảng cân lượng: %s" % sai)
    if [T.CHI[x] for x in T.LUU_HA] != ["Dậu", "Tuất", "Mùi", "Thân", "Tỵ", "Ngọ", "Thìn", "Mão", "Hợi", "Dần"]:
        miss.append("Lưu Hà")
    if T.DO_SANG_PHU["Văn Xương"] != T.DO_SANG_PHU["Văn Khúc"] or T.DO_SANG_PHU["Thiên Khốc"] != T.DO_SANG_PHU["Thiên Hư"]:
        miss.append("độ sáng phụ tinh")
    return miss


def phan_ra_soat_bat_tu():
    """Rà soát 11/2026 (Bát tự ngoài tứ trụ): bảng thần sát dò lại theo câu phú gốc (Tam Mệnh Thông Hội), bảng quan hệ
    can chi đủ 144 + 100 cặp, giờ Tý muộn của người khác trong hoptuoi theo --ty, dòng Tuần không ghi trụ rơi vào,
    thông báo lỗi ngày âm theo đúng lịch của thời kỳ, khoảng năm mặc định của vanthe."""
    import thansat as S
    import tvbt as B
    miss = []
    Z, G = "子丑寅卯辰巳午未申酉戌亥", "甲乙丙丁戊己庚辛壬癸"
    z = lambda t: [Z.index(c) for c in t]
    # câu phú: "Giáp Mậu Canh ngưu dương, Ất Kỷ thử hầu hương, Bính Đinh trư kê vị, Nhâm Quý thố xà tàng, Lục Tân phùng mã hổ"
    if [sorted(S.QUY_NHAN[i]) for i in range(10)] != [sorted(z(t)) for t in
                                                       ("丑未", "子申", "亥酉", "亥酉", "丑未", "子申", "丑未", "寅午", "卯巳", "卯巳")]:
        miss.append("Thiên Ất")
    if [sorted(S.THAI_CUC[i]) for i in range(10)] != [sorted(z(t)) for t in
                                                       ("子午", "子午", "卯酉", "卯酉", "辰戌丑未", "辰戌丑未", "寅亥", "寅亥", "巳申", "巳申")]:
        miss.append("Thái Cực")
    for ten, bang, chuan in (("Văn Xương", S.VAN_XUONG, "巳午申酉申酉亥子寅卯"), ("Kim Dư", S.KIM_DU, "辰巳未申未申戌亥丑寅"),
                             ("Hồng Diễm", S.HONG_DIEM, "午申寅未辰辰戌酉子申"), ("Quốc Ấn", S.QUOC_AN, "戌亥丑寅丑寅辰巳未申"),
                             ("Lưu Hà", S.LUU_HA, "酉戌未申巳午辰卯亥寅"), ("Lộc", S.LOC, "寅卯巳午巳午申酉亥子")):
        if list(bang) != z(chuan):
            miss.append(ten)
    # Thiên Đức: "chính Đinh, nhị Thân cung, tam Nhâm, tứ Tân đồng, ngũ Hợi, lục Giáp thượng, thất Quý, bát Dần phùng,
    # cửu Bính, thập cư Ất, Tý Tỵ, Sửu Canh trung"; Nguyệt Đức: Dần Ngọ Tuất Bính, Thân Tý Thìn Nhâm, Hợi Mão Mùi Giáp, Tỵ Dậu Sửu Canh
    td = {Z.index(k): v for k, v in zip("寅卯辰巳午未申酉戌亥子丑", "丁申壬辛亥甲癸寅丙乙巳庚")}
    if any((S.THIEN_DUC[k][0] == "can" and G[S.THIEN_DUC[k][1]] != v) or (S.THIEN_DUC[k][0] == "chi" and Z[S.THIEN_DUC[k][1]] != v)
           for k, v in td.items()):
        miss.append("Thiên Đức")
    if any(G[S.NGUYET_DUC[k]] != {0: "壬", 1: "庚", 2: "丙", 3: "甲"}[[0, 1, 2, 3][S.NHOM(k)]] for k in range(12)):
        miss.append("Nguyệt Đức")
    ngay = lambda ds: {(G.index(x[0]), Z.index(x[1])) for x in ds.split()}
    if S.AM_DUONG_SAI != ngay("丙子 丙午 丁丑 丁未 戊寅 戊申 辛卯 辛酉 壬辰 壬戌 癸巳 癸亥") or \
            S.THAP_AC != ngay("甲辰 乙巳 丙申 丁亥 戊戌 己丑 庚辰 辛巳 壬申 癸亥") or \
            S.KHOI_CUONG != ngay("庚辰 庚戌 壬辰 戊戌") or S.CO_LOAN != ngay("甲寅 乙巳 丁巳 丙午 戊午 戊申 辛亥 壬子"):
        miss.append("thần sát theo trụ ngày")
    # quan hệ chi: đủ 144 cặp so với danh sách gốc
    hop, hai = ["子丑", "寅亥", "卯戌", "辰酉", "巳申", "午未"], ["子未", "丑午", "寅巳", "卯辰", "申亥", "酉戌"]
    hinh = ["寅巳", "巳申", "寅申", "丑戌", "戌未", "丑未", "子卯"]
    for i in range(12):
        for j in range(12):
            q, cap = B.qh_chi(i, j), {Z[i] + Z[j], Z[j] + Z[i]}
            if i == j:
                if (q == ["tự hình"]) != (Z[i] in "辰午酉亥"):
                    miss.append("tự hình %s" % Z[i])
                continue
            if ("xung" in q) != ((i - j) % 12 == 6) or any(x.startswith("lục hợp") for x in q) != bool(cap & set(hop)) \
                    or ("hại" in q) != bool(cap & set(hai)) or ("hình" in q) != bool(cap & set(hinh)):
                miss.append("quan hệ chi %s%s: %s" % (Z[i], Z[j], q))
    for i in range(10):
        for j in range(10):
            q = B.qh_can(i, j)
            if any(x.startswith("hợp") for x in q) != ((i - j) % 10 == 5) or ("xung" in q) != (
                    {G[i], G[j]} in ({"甲", "庚"}, {"乙", "辛"}, {"丙", "壬"}, {"丁", "癸"})):
                miss.append("quan hệ can %s%s" % (G[i], G[j]))
    # hoptuoi: người khác sinh 23h30 – trụ ngày theo --ty của đương số (lunar-python mặc định sect 2)
    base = ["--ngay", "2000-01-01", "--gio", "10:00", "--gioi", "nam", "--noi", "Hà Nội", "--nguoi", "A:1990-05-17 23:30"]
    if "Canh Ngọ – Tân Tỵ – Quý Mùi – Nhâm Tý" not in chay("hoptuoi", *base):
        miss.append("hoptuoi giờ Tý muộn (--ty 1)")
    if "Canh Ngọ – Tân Tỵ – Nhâm Ngọ – Nhâm Tý" not in chay("hoptuoi", *base, "--ty", "2"):
        miss.append("hoptuoi giờ Tý muộn (--ty 2)")
    t = chay("battu", "--ngay", "2000-01-01", "--gio", "10:00", "--gioi", "nam", "--noi", "Hà Nội")
    miss += thieu(t, ["- Tuần không (theo trụ ngày): Tý Sửu; rơi vào trụ Tháng Tý"])
    r = subprocess.run([sys.executable, "tvbt/tvbt.py", "battu", "--ngay", "2035-11-30", "--am", "--gio", "10:00",
                        "--gioi", "nam", "--noi", "Hà Nội"], capture_output=True, text=True)
    r2 = subprocess.run([sys.executable, "tvbt/tvbt.py", "battu", "--ngay", "2031-06-25", "--am", "--nhuan", "--gio",
                         "10:00", "--gioi", "nam", "--noi", "Hà Nội"], capture_output=True, text=True)
    if "chỉ có 29 ngày" not in r.stderr + r.stdout or "không có tháng 6 nhuận" not in r2.stderr + r2.stdout:
        miss.append("thông báo lỗi ngày âm sau 1968 phải theo lịch UTC+7: %r %r" % (r.stderr[-90:], r2.stderr[-90:]))
    r = subprocess.run([sys.executable, "tvbt/nc.py", "vanthe", "--ngay", "2090-03-03", "--gio", "10:00", "--gioi", "nam",
                        "--noi", "Hà Nội", "--ra", "/tmp/kt_vanthe.html"], capture_output=True, text=True)
    if "| 2091 |" not in r.stdout:
        miss.append("vanthe người sinh 2090: khoảng năm mặc định")
    return miss


if __name__ == "__main__":
    loi = 0
    for ten, ham in [("Cơ bản", phan_co_ban), ("Luận chi tiết", phan_luan_chi_tiet), ("Kỳ môn mở rộng", phan_ky_mon),
                     ("Nâng cao", phan_nang_cao), ("Dò giờ sinh", phan_gio_sinh),
                     ("Đối chiếu cách trình bày Việt Nam", phan_doi_chieu_viet_nam),
                     ("Rà soát Bát tự ngoài tứ trụ", phan_ra_soat_bat_tu)]:
        try:
            miss = ham()
        except Exception as e:      # noqa: BLE001
            miss = ["ngoại lệ %r" % e]
        print("== %s: %s" % (ten, "ĐẠT" if not miss else "LỖI – thiếu %s" % miss))
        loi += len(miss)
    print("Vẽ ảnh PNG:", "được" if os.path.exists("/tmp/kmtest.png") else "không (thiếu Chromium/Playwright) – vẫn có file HTML")
    print("TỰ KIỂM TRA TOÀN BỘ:", "ĐẠT" if not loi else "LỖI")
    sys.exit(1 if loi else 0)
