# -*- coding: utf-8 -*-
"""Kỳ môn độn giáp – thời gia kỳ môn, chuyển bàn, định cục theo phép hủy bổ (拆补, phổ biến hiện nay).
Đầu vào: can chi ngày, can chi giờ (chỉ số 0..59), tên tiết khí đang hiệu lực."""

CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
# Tiết khí -> (dương độn?, cục Thượng/Trung/Hạ nguyên)
CUC = {
    "Đông Chí": (True, (1, 7, 4)), "Tiểu Hàn": (True, (2, 8, 5)), "Đại Hàn": (True, (3, 9, 6)),
    "Lập Xuân": (True, (8, 5, 2)), "Vũ Thủy": (True, (9, 6, 3)), "Kinh Trập": (True, (1, 7, 4)),
    "Xuân Phân": (True, (3, 9, 6)), "Thanh Minh": (True, (4, 1, 7)), "Cốc Vũ": (True, (5, 2, 8)),
    "Lập Hạ": (True, (4, 1, 7)), "Tiểu Mãn": (True, (5, 2, 8)), "Mang Chủng": (True, (6, 3, 9)),
    "Hạ Chí": (False, (9, 3, 6)), "Tiểu Thử": (False, (8, 2, 5)), "Đại Thử": (False, (7, 1, 4)),
    "Lập Thu": (False, (2, 5, 8)), "Xử Thử": (False, (1, 4, 7)), "Bạch Lộ": (False, (9, 3, 6)),
    "Thu Phân": (False, (7, 1, 4)), "Hàn Lộ": (False, (6, 9, 3)), "Sương Giáng": (False, (5, 8, 2)),
    "Lập Đông": (False, (6, 9, 3)), "Tiểu Tuyết": (False, (5, 8, 2)), "Đại Tuyết": (False, (4, 7, 1)),
}
TIET_HAN = {"冬至": "Đông Chí", "小寒": "Tiểu Hàn", "大寒": "Đại Hàn", "立春": "Lập Xuân", "雨水": "Vũ Thủy",
            "惊蛰": "Kinh Trập", "春分": "Xuân Phân", "清明": "Thanh Minh", "谷雨": "Cốc Vũ", "立夏": "Lập Hạ",
            "小满": "Tiểu Mãn", "芒种": "Mang Chủng", "夏至": "Hạ Chí", "小暑": "Tiểu Thử", "大暑": "Đại Thử",
            "立秋": "Lập Thu", "处暑": "Xử Thử", "白露": "Bạch Lộ", "秋分": "Thu Phân", "寒露": "Hàn Lộ",
            "霜降": "Sương Giáng", "立冬": "Lập Đông", "小雪": "Tiểu Tuyết", "大雪": "Đại Tuyết"}
NGHI = [4, 5, 6, 7, 8, 9, 3, 2, 1]        # thứ tự Tam kỳ Lục nghi: Mậu Kỷ Canh Tân Nhâm Quý Đinh Bính Ất
TUAN_NGHI = [4, 5, 6, 7, 8, 9]            # Giáp Tý Mậu, Giáp Tuất Kỷ, Giáp Thân Canh, Giáp Ngọ Tân, Giáp Thìn Nhâm, Giáp Dần Quý
SAO = {1: "Thiên Bồng", 2: "Thiên Nhuế", 3: "Thiên Xung", 4: "Thiên Phụ", 5: "Thiên Cầm",
       6: "Thiên Tâm", 7: "Thiên Trụ", 8: "Thiên Nhậm", 9: "Thiên Anh"}
MON = {1: "Hưu", 2: "Tử", 3: "Thương", 4: "Đỗ", 6: "Khai", 7: "Kinh", 8: "Sinh", 9: "Cảnh"}
THAN = ["Trực Phù", "Đằng Xà", "Thái Âm", "Lục Hợp", "Bạch Hổ", "Huyền Vũ", "Cửu Địa", "Cửu Thiên"]
VONG = [1, 8, 3, 4, 9, 2, 7, 6]           # 8 cung ngoài theo chiều kim đồng hồ: Khảm Cấn Chấn Tốn Ly Khôn Đoài Càn
CUNG = {1: "Khảm (Bắc)", 2: "Khôn (Tây Nam)", 3: "Chấn (Đông)", 4: "Tốn (Đông Nam)", 5: "Trung cung",
        6: "Càn (Tây Bắc)", 7: "Đoài (Tây)", 8: "Cấn (Đông Bắc)", 9: "Ly (Nam)"}
CUNG_CHI = {1: [0], 8: [1, 2], 3: [3], 4: [4, 5], 9: [6], 2: [7, 8], 7: [9], 6: [10, 11]}
MON_CAT = {"Khai", "Hưu", "Sinh"}
MON_HUNG = {"Tử", "Kinh", "Thương"}
DICH_MA = {0: 2, 4: 2, 8: 2, 2: 8, 6: 8, 10: 8, 5: 11, 9: 11, 1: 11, 11: 5, 3: 5, 7: 5}


def ky(p):
    return 2 if p == 5 else p


def lap(gz_ngay, gz_gio, tiet):
    duong, ba = CUC[tiet]
    fd = gz_ngay - gz_ngay % 5                  # phù đầu: ngày Giáp/Kỷ gần nhất
    z = fd % 12
    nguyen = 0 if z in (0, 6, 3, 9) else (1 if z in (2, 8, 5, 11) else 2)
    b = ban(duong, ba[nguyen], gz_gio)
    b.update(nguyen=nguyen, tiet=tiet, phu_dau=fd, gz_ngay=gz_ngay)
    return b


def dia_ban(duong, so_cuc):
    dia = {}
    for k, can in enumerate(NGHI):
        p = ((so_cuc - 1 + (k if duong else -k)) % 9) + 1
        dia[p] = can
    return dia


def ban(duong, so_cuc, gz_gio):
    """Chuyển bàn: an thiên bàn, môn, thần cho một cục và một can chi dùng làm 'giờ'
    (thời gia: can chi giờ; niên/nguyệt/nhật gia: can chi năm/tháng/ngày)."""
    dia = {}
    for k, can in enumerate(NGHI):
        p = ((so_cuc - 1 + (k if duong else -k)) % 9) + 1
        dia[p] = can
    vi_tri = {c: p for p, c in dia.items()}
    tuan = gz_gio // 10
    nghi_tuan = TUAN_NGHI[tuan]
    P = vi_tri[nghi_tuan]                       # cung của tuần thủ trên địa bàn
    sao_truc_phu = SAO[P]
    mon_truc_su = MON[ky(P)]
    can_gio = gz_gio % 10
    can_tim = nghi_tuan if can_gio == 0 else can_gio
    Q = ky(vi_tri[can_tim])                     # trực phù bay đến cung có can giờ trên địa bàn
    lech = (VONG.index(Q) - VONG.index(ky(P))) % 8
    thien_sao, thien_can = {}, {}
    for i, goc in enumerate(VONG):
        dich = VONG[(i + lech) % 8]
        thien_sao[dich] = [SAO[goc]] + (["Thiên Cầm"] if goc == 2 else [])
        thien_can[dich] = [dia[goc]] + ([dia[5]] if goc == 2 else [])
    buoc = gz_gio % 10
    D = ((P - 1 + (buoc if duong else -buoc)) % 9) + 1
    D = ky(D)
    lech_m = (VONG.index(D) - VONG.index(ky(P))) % 8
    mon = {}
    for i, goc in enumerate(VONG):
        mon[VONG[(i + lech_m) % 8]] = MON[goc]
    than = {}
    i0 = VONG.index(Q)
    for k, ten in enumerate(THAN):
        than[VONG[(i0 + (k if duong else -k)) % 8]] = ten
    xun0 = (gz_gio - gz_gio % 10)
    khong = [((xun0 % 12) + 10) % 12, ((xun0 % 12) + 11) % 12]
    return dict(duong=duong, cuc=so_cuc, dia=dia,
                tuan=tuan, nghi_tuan=nghi_tuan, P=P, truc_phu=sao_truc_phu, truc_su=mon_truc_su,
                Q=Q, D=D, thien_sao=thien_sao, thien_can=thien_can, mon=mon, than=than,
                khong=khong, ma=DICH_MA[gz_gio % 12], gz_gio=gz_gio)


def ten_gz(i):
    return "%s %s" % (CAN[i % 10], CHI[i % 12])


def in_ban(b, phep="hủy bổ", ghi_phep=""):
    if "tieu_de" in b:
        print(b["tieu_de"])
        print(b["dau"])
    else:
        print("KỲ MÔN ĐỘN GIÁP (thời gia, chuyển bàn, định cục %s)" % phep)
        print("- Ngày %s, giờ %s; tiết %s%s → %s độn %d cục, %s nguyên (phù đầu %s)" % (
            ten_gz(b["gz_ngay"]), ten_gz(b["gz_gio"]), b["tiet"], " (%s)" % ghi_phep if ghi_phep else "",
            "Dương" if b["duong"] else "Âm", b["cuc"],
            ["Thượng", "Trung", "Hạ"][b["nguyen"]], ten_gz(b["phu_dau"])))
    print("- Tuần thủ: Giáp %s ẩn dưới %s (cung %s); Trực phù: %s → đến cung %s; Trực sử: %s môn → đến cung %s" % (
        CHI[(b["tuan"] * 10) % 12], CAN[b["nghi_tuan"]], CUNG[b["P"]],
        b["truc_phu"] + (" (ký Khôn)" if b["P"] == 5 else ""), CUNG[b["Q"]], b["truc_su"], CUNG[b["D"]]))
    print("- Không vong %s: %s; Dịch mã %s: %s (cung %s)" % (
        b.get("nhan", "giờ"), ", ".join(CHI[z] for z in b["khong"]), b.get("nhan", "giờ"), CHI[b["ma"]],
        CUNG[[p for p, zs in CUNG_CHI.items() if b["ma"] in zs][0]]))
    an = b.get("an_can")
    print("| Cung | Bát thần | Cửu tinh (thiên bàn) | Can thiên bàn | Bát môn | Can địa bàn |%s Ghi chú |" % (
        " Ẩn can |" if an else ""))
    print("|---|---|---|---|---|---|---|" + ("---|" if an else ""))
    for p in [4, 9, 2, 3, 5, 7, 8, 1, 6]:
        if p == 5:
            if an and 5 in an:
                print("| %s |  |  |  |  | %s | %s | ký Khôn |" % (CUNG[5], CAN[b["dia"][5]], CAN[an[5][0]]))
            else:
                print("| %s |  |  |  |  | %s |%s ký Khôn |" % (CUNG[5], CAN[b["dia"][5]], "  |" if an else ""))
            continue
        ghi = []
        if set(CUNG_CHI[p]) & set(b["khong"]):
            ghi.append("Không vong")
        if b["ma"] in CUNG_CHI[p]:
            ghi.append("Mã")
        if p == b["Q"]:
            ghi.append("Trực phù")
        if p == b["D"]:
            ghi.append("Trực sử")
        m = b["mon"][p]
        print("| %s | %s | %s | %s | %s môn (%s) | %s |%s %s |" % (
            CUNG[p], b["than"][p], " + ".join(b["thien_sao"][p]), " + ".join(CAN[c] for c in b["thien_can"][p]),
            m, "cát" if m in MON_CAT else ("hung" if m in MON_HUNG else "bình"),
            " + ".join(CAN[c] for c in ([b["dia"][p]] + ([b["dia"][5]] if p == 2 and an else []))),
            (" %s |" % " + ".join(CAN[c] for c in an[p])) if an else "", ", ".join(ghi)))
    print("(Bố cục bảng theo hướng trên bản đồ: hàng 1 = Đông Nam, Nam, Tây Nam; hàng 2 = Đông, Giữa, Tây; "
          "hàng 3 = Đông Bắc, Bắc, Tây Bắc. Bát thần dùng Bạch Hổ/Huyền Vũ cho cả hai độn; phái cổ dùng "
          "Câu Trận/Chu Tước ở dương độn.)")
    print()


# ---------------------------------------------------------------- Định cục TRÍ NHUẬN (置闰: siêu thần, tiếp khí, nhuận)
_PINYIN = {"DA_XUE": "大雪", "DONG_ZHI": "冬至", "XIAO_HAN": "小寒", "DA_HAN": "大寒", "LI_CHUN": "立春",
           "YU_SHUI": "雨水", "JING_ZHE": "惊蛰"}
NGUONG_NHUAN = 9   # phù đầu đến trước Hạ Chí/Đông Chí từ 9 ngày trở lên thì nhuận (phần mềm hiện nay; lệ Khang Hy 57 là 8)


def _tiet_khi(y0, y1, utc_off):
    """Danh sách (giờ địa phương, tên Việt) của các tiết khí từ năm y0 đến y1."""
    import datetime as dt
    from lunar_python import Lunar
    gap = {}
    for y in range(y0, y1 + 1):
        for k, s in Lunar.fromYmd(y, 6, 1).getJieQiTable().items():
            t = dt.datetime(s.getYear(), s.getMonth(), s.getDay(), s.getHour(), s.getMinute(), s.getSecond())
            t = t - dt.timedelta(hours=8 - utc_off)
            gap[t.replace(second=0)] = TIET_HAN[_PINYIN.get(k, k)]
    return sorted(gap.items())


def _ngay_cua(t):
    """Ngày dương lịch của thời điểm giao tiết (theo lịch in thông thường)."""
    return t.date()


def tiet_tri_nhuan(ngay, utc_off=7.0, nguong=None):
    """ngay: ngày (date) theo trụ ngày (23h đã sang ngày mới). Trả về (tên tiết dùng định cục, ghi chú)."""
    import datetime as dt
    from lich_vn import jd_from_date
    terms = _tiet_khi(ngay.year - 3, ngay.year + 1, utc_off)
    ten_ds = [n for _, n in terms]
    gz = lambda d: (jd_from_date(d.day, d.month, d.year) + 49) % 60
    d = dt.date(ngay.year - 2, 1, 1)
    while gz(d) % 15:
        d += dt.timedelta(days=1)
    # neo: khối đầu tiên có một tiết lệch trong [-3, 7) ngày – chỉ một cách gán duy nhất, chắc chắn đúng
    T = None
    while T is None:
        b0 = dt.datetime(d.year, d.month, d.day) - dt.timedelta(hours=1)
        for i, (t, _) in enumerate(terms):
            if -3 <= (t - b0).total_seconds() / 86400 < 7:
                T = i
                break
        if T is None:
            d += dt.timedelta(days=15)
    da_nhuan = False
    ghi = ""
    while True:
        nxt = d + dt.timedelta(days=15)
        if nxt > ngay:
            break
        if ten_ds[T] in ("Mang Chủng", "Đại Tuyết") and not da_nhuan and \
                (_ngay_cua(terms[T + 1][0]) - nxt).days >= (nguong or NGUONG_NHUAN):
            da_nhuan = True
        else:
            T += 1
            da_nhuan = False
        d = nxt
    lech = (_ngay_cua(terms[T][0]) - d).days
    if da_nhuan:
        ghi = "nhuận kỳ (lặp lại tiết %s)" % ten_ds[T]
    elif lech > 0:
        ghi = "siêu thần %d ngày (phù đầu đến trước tiết)" % lech
    elif lech < 0:
        ghi = "tiếp khí %d ngày (tiết đến trước phù đầu)" % -lech
    else:
        ghi = "chính thụ (phù đầu và tiết cùng ngày)"
    return ten_ds[T], ghi, d


# ---------------------------------------------------------------- Cách cục, môn bức, vượng suy
HANH_CUNG = {1: "Thủy", 2: "Thổ", 3: "Mộc", 4: "Mộc", 5: "Thổ", 6: "Kim", 7: "Kim", 8: "Thổ", 9: "Hỏa"}
HANH_MON = {"Hưu": "Thủy", "Sinh": "Thổ", "Thương": "Mộc", "Đỗ": "Mộc", "Cảnh": "Hỏa", "Tử": "Thổ",
            "Kinh": "Kim", "Khai": "Kim"}
_SINH = {"Kim": "Thủy", "Thủy": "Mộc", "Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim"}
_KHAC = {"Kim": "Mộc", "Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim"}
HANH_CAN_ = ["Mộc", "Mộc", "Hỏa", "Hỏa", "Thổ", "Thổ", "Kim", "Kim", "Thủy", "Thủy"]
# Thập can khắc ứng (thiên bàn + địa bàn) – các cách có tên, thống nhất giữa các sách
KHAC_UNG = {(4, 2): ("Thanh Long phản thủ", "đại cát"), (2, 4): ("Phi điểu điệt huyệt", "đại cát"),
            (6, 2): ("Thái Bạch nhập Huỳnh (giặc đến)", "hung"), (2, 6): ("Huỳnh nhập Thái Bạch (giặc đi)", "hung"),
            (6, 4): ("Phục cung cách", "hung"), (4, 6): ("Phi cung cách", "hung"),
            (6, 5): ("Hình cách", "hung"), (6, 8): ("Tiểu cách", "hung"), (6, 9): ("Đại cách", "hung"),
            (7, 1): ("Bạch Hổ xương cuồng", "hung"), (1, 7): ("Thanh Long đào tẩu", "hung"),
            (3, 9): ("Chu Tước đầu giang", "hung"), (9, 3): ("Đằng Xà yểu kiểu", "hung"),
            (9, 9): ("Thiên võng tứ trương", "hung"), (6, 6): ("Thái Bạch đồng cung (chiến cách)", "hung")}
KICH_HINH = {4: 3, 5: 2, 6: 8, 7: 9, 8: 4, 9: 4}          # Lục nghi kích hình: nghi -> cung
NHAP_MO = {1: (6, "Ất kỳ nhập mộ (có sách lấy cung Khôn)"), 2: (6, "Bính kỳ nhập mộ"), 3: (8, "Đinh kỳ nhập mộ")}
LOC_VI = {1: 3, 2: 4, 3: 9}                                 # Tam kỳ lâm lộc vị (Ất Mão, Bính Tỵ, Đinh Ngọ)
# Thiên phụ thời (天辅时): can ngày -> các giờ (chỉ số 60). Giáp/Kỷ: Kỷ Tỵ (5, Kim hàm ngọc kính) hoặc Giáp Tuất
# (10, Lưu Quảng Bân); Ất Canh Giáp Thân, Bính Tân Giáp Ngọ, Đinh Nhâm Giáp Thìn, Mậu Quý Giáp Dần (các sách thống nhất).
THIEN_PHU_THOI = {0: (5, 10), 5: (5, 10), 1: (20,), 6: (20,), 2: (30,), 7: (30,), 3: (40,), 8: (40,), 4: (50,), 9: (50,)}


def _an(gz):
    """Can 'hiện' của một can chi: Giáp ẩn dưới nghi của tuần."""
    return TUAN_NGHI[gz // 10] if gz % 10 == 0 else gz % 10


def vuong_suy(hanh, chi_thang):
    mua = {2: "Mộc", 3: "Mộc", 5: "Hỏa", 6: "Hỏa", 8: "Kim", 9: "Kim", 11: "Thủy", 0: "Thủy"}.get(chi_thang, "Thổ")
    if hanh == mua:
        return "vượng"
    if _SINH[mua] == hanh:
        return "tướng"
    if _SINH[hanh] == mua:
        return "hưu"
    if _KHAC[hanh] == mua:
        return "tù"
    return "tử"


# Thời can nhập mộ (时干入墓): giờ Bính Tuất, Đinh Sửu, Mậu Tuất, Nhâm Thìn, Quý Mùi
THOI_MO = {i for i in range(60) if (i % 10, i % 12) in {(2, 10), (3, 1), (4, 10), (8, 4), (9, 7)}}


def cach_cuc(b, gz_nam, gz_thang):
    """Trả về list (cung hoặc 0 = toàn bàn, tên cách, tính chất, ghi chú)."""
    kq = []
    dia = dict(b["dia"])
    dia_set = {p: [dia[p]] + ([dia[5]] if p == 2 else []) for p in VONG}
    can_ngay, can_gio = _an(b["gz_ngay"]), _an(b["gz_gio"])
    can_nam, can_thang = _an(gz_nam), _an(gz_thang)
    for p in VONG:
        for tc in b["thien_can"][p]:
            for dc in dia_set[p]:
                if (tc, dc) in KHAC_UNG:
                    ten, tinh = KHAC_UNG[(tc, dc)]
                    kq.append((p, ten, tinh, "%s thiên bàn trên %s địa bàn" % (CAN[tc], CAN[dc])))
                if tc == 6:
                    for c, nhan in ((can_nam, "Tuế"), (can_thang, "Nguyệt"), (can_ngay, "Nhật"), (can_gio, "Thời")):
                        if nhan == "Thời" and b.get("gia"):
                            continue    # niên/nguyệt/nhật gia: 'giờ' của bàn là can chi năm/tháng/ngày, đã xét ở trên
                        if dc == c and c != 6:
                            kq.append((p, "%s cách" % nhan, "hung", "Canh thiên bàn trên can %s %s" % (
                                {"Tuế": "năm", "Nguyệt": "tháng", "Nhật": "ngày", "Thời": "giờ"}[nhan], CAN[c])))
                if tc == can_ngay and dc == 6 and can_ngay != 6:
                    kq.append((p, "Phi can cách", "hung", "can ngày %s trên Canh" % CAN[can_ngay]))
                if tc == 6 and dc == can_ngay and can_ngay != 6:
                    kq.append((p, "Phục can cách", "hung", "Canh trên can ngày %s" % CAN[can_ngay]))
            if KICH_HINH.get(tc) == p:
                kq.append((p, "Lục nghi kích hình", "hung", "%s (Giáp %s) lâm cung %s" % (
                    CAN[tc], CHI[[0, 10, 8, 6, 4, 2][TUAN_NGHI.index(tc)]], CUNG[p])))
            if tc in NHAP_MO and NHAP_MO[tc][0] == p:
                kq.append((p, NHAP_MO[tc][1], "hung", "%s lâm %s" % (CAN[tc], CUNG[p])))
            if LOC_VI.get(tc) == p:
                kq.append((p, "Tam kỳ lâm lộc vị", "cát", "%s lâm %s" % (CAN[tc], CUNG[p])))
        m, th = b["mon"][p], b["than"][p]
        tcs = b["thien_can"][p]
        hm, hc = HANH_MON[m], HANH_CUNG[p]
        if _KHAC[hm] == hc:
            kq.append((p, "Môn bức", "cát môn bị bức – việc tốt khó thành" if m in MON_CAT else "hung môn bị bức – hung thêm",
                       "%s môn (%s) khắc cung (%s)" % (m, hm, hc)))
        ky_ = {1, 2, 3} & set(tcs)
        if m in MON_CAT and ky_:
            for than_ten, ten in (("Thái Âm", "Chân trá"), ("Cửu Địa", "Trùng trá"), ("Lục Hợp", "Hưu trá")):
                if th == than_ten:
                    kq.append((p, ten, "cát", "%s môn + %s + %s" % (m, "/".join(CAN[c] for c in ky_), th)))
        gia = [("Cảnh", {1, 2, 3}, "Cửu Thiên", "Thiên giả"), ("Đỗ", {3, 5, 9}, "Cửu Địa", "Địa giả"),
               ("Kinh", {8}, "Cửu Thiên", "Nhân giả"), ("Thương", {3, 5, 9}, "Cửu Địa", "Thần giả"),
               ("Tử", {3, 5, 9}, "Cửu Địa", "Quỷ giả")]
        for mm, cs, tt_, ten in gia:
            if m == mm and th == tt_ and set(tcs) & cs:
                kq.append((p, ten, "cát (dùng việc kín, mưu)", "%s môn + %s + %s" % (m, "/".join(
                    CAN[c] for c in set(tcs) & cs), th)))
        # Cửu độn (bản phổ biến)
        cat3 = m in MON_CAT
        if 2 in tcs and m == "Sinh" and set(dia_set[p]) & {3, 4}:
            kq.append((p, "Thiên độn", "đại cát", "Bính + Sinh môn + địa bàn %s" % "/".join(
                CAN[c] for c in set(dia_set[p]) & {3, 4})))
        if 1 in tcs and m == "Khai" and 5 in dia_set[p]:
            kq.append((p, "Địa độn", "đại cát", "Ất + Khai môn + địa bàn Kỷ"))
        if 3 in tcs and m == "Hưu" and th == "Thái Âm":
            kq.append((p, "Nhân độn", "đại cát", "Đinh + Hưu môn + Thái Âm"))
        if 2 in tcs and m == "Sinh" and th == "Cửu Thiên":
            kq.append((p, "Thần độn", "đại cát", "Bính + Sinh môn + Cửu Thiên"))
        if 3 in tcs and m in ("Đỗ", "Khai") and th == "Cửu Địa":
            kq.append((p, "Quỷ độn", "cát", "Đinh + %s môn + Cửu Địa" % m))
        if 1 in tcs and cat3 and p == 4:
            kq.append((p, "Phong độn", "cát", "Ất + %s môn + cung Tốn" % m))
        if 1 in tcs and cat3 and 7 in dia_set[p]:
            kq.append((p, "Vân độn", "cát", "Ất + %s môn + địa bàn Tân" % m))
        if 1 in tcs and cat3 and (p == 1 or 9 in dia_set[p]):
            kq.append((p, "Long độn", "cát", "Ất + %s môn + %s" % (m, "cung Khảm" if p == 1 else "địa bàn Quý")))
        if 1 in tcs and m in ("Hưu", "Sinh") and 7 in dia_set[p] and p == 8:
            kq.append((p, "Hổ độn", "cát", "Ất + %s môn + địa bàn Tân + cung Cấn" % m))
    if 3 in dia_set.get(b["D"], []):
        kq.append((b["D"], "Ngọc nữ thủ môn", "cát", "Trực sử %s môn lâm cung có Đinh địa bàn" % b["truc_su"]))
    # toàn bàn
    lech = (VONG.index(b["Q"]) - VONG.index(ky(b["P"]))) % 8
    lech_m = (VONG.index(b["D"]) - VONG.index(ky(b["P"]))) % 8
    if lech == 0:
        kq.append((0, "Tinh phục ngâm", "hung (việc đình trệ, nên giữ)", "cửu tinh nằm nguyên cung"))
    elif lech == 4:
        kq.append((0, "Tinh phản ngâm", "hung (việc lật ngược, đi về)", "cửu tinh ở cung đối diện"))
    if lech_m == 0:
        kq.append((0, "Môn phục ngâm", "hung", "bát môn nằm nguyên cung"))
    elif lech_m == 4:
        kq.append((0, "Môn phản ngâm", "hung", "bát môn ở cung đối diện"))
    cg, cn = b["gz_gio"] % 10, b["gz_ngay"] % 10
    if b.get("gia"):            # niên/nguyệt/nhật gia: không xét các cách theo giờ
        return kq
    if cg % 2 == cn % 2 and _KHAC[HANH_CAN_[cg]] == HANH_CAN_[cn]:
        kq.append((0, "Ngũ bất ngộ thời", "hung", "can giờ %s khắc can ngày %s (cùng âm dương)" % (CAN[cg], CAN[cn])))
    if b["gz_gio"] in THIEN_PHU_THOI[cn]:
        kq.append((0, "Thiên phụ thời", "cát", "giờ %s của ngày can %s%s" % (
            ten_gz(b["gz_gio"]), CAN[cn], " (ngày Giáp/Kỷ: sách lấy Kỷ Tỵ hoặc Giáp Tuất, tùy phái)" if cn in (0, 5) else "")))
    if b["gz_gio"] in THOI_MO:
        kq.append((0, "Thời mộ (can giờ nhập mộ)", "hung – việc mờ mịt, khó mở, không nên khởi sự",
                   "giờ %s" % ten_gz(b["gz_gio"])))
    return kq


def in_bo_sung(b, gz_nam, gz_thang, chi_thang, gz_ngay=None, gz_gio=None):
    """In vượng suy, vị trí dụng thần (can năm/tháng/ngày/giờ), thập can khắc ứng và cách cục."""
    phi = b.get("loai") == "phi"
    gz_ngay = b.get("gz_ngay") if gz_ngay is None else gz_ngay
    gz_gio = b["gz_gio"] if gz_gio is None else gz_gio
    tim = {}
    for p in ([1, 2, 3, 4, 5, 6, 7, 8, 9] if phi else VONG):
        for c in b["thien_can"][p]:
            tim.setdefault(c, p)
    dong = []
    for nhan, gz in (("năm", gz_nam), ("tháng", gz_thang), ("ngày (người hỏi)", gz_ngay), ("giờ (việc hỏi)", gz_gio)):
        c = _an(gz)
        p = tim.get(c)
        dong.append("can %s %s%s → cung %s" % (nhan, CAN[gz % 10], " (ẩn dưới %s)" % CAN[c] if gz % 10 == 0 else "",
                                                CUNG[p] if p else "?"))
    print("- Dụng thần theo can (tìm trên thiên bàn): " + "; ".join(dong))
    print("- Vượng suy bát môn theo tháng %s: " % CHI[chi_thang] + ", ".join(
        "%s %s" % (m, vuong_suy(HANH_MON[m], chi_thang)) for m in ["Khai", "Hưu", "Sinh", "Thương", "Đỗ", "Cảnh", "Tử", "Kinh"]))
    xn = gz_ngay - gz_ngay % 10
    print("- Không vong ngày: %s" % ", ".join(CHI[(xn % 12 + k) % 12] for k in (10, 11)))
    print()
    in_khac_ung(b)
    if phi:
        print("(Bảng cách cục tổng hợp – tam trá, ngũ giả, cửu độn, môn bức… – hiện chỉ tính cho chuyển bàn; "
              "với phi bàn hãy luận từ khắc ứng, môn, tinh, thần ở trên.)")
        print()
        return
    cc = cach_cuc(dict(b, gz_ngay=gz_ngay), gz_nam, gz_thang)
    print()
    print("CÁCH CỤC NHẬN DIỆN ĐƯỢC (thập can khắc ứng, kích hình, nhập mộ, môn bức, tam trá ngũ giả, cửu độn, phục/phản ngâm)")
    if not cc:
        print("- Không có cách cục nổi bật trong danh sách.")
    else:
        print("| Cung | Cách | Tính chất | Căn cứ |")
        print("|---|---|---|---|")
        for p, ten, tinh, ghi in sorted(cc, key=lambda x: (x[0] != 0, x[0])):
            print("| %s | %s | %s | %s |" % ("Toàn bàn" if p == 0 else CUNG[p], ten, tinh, ghi))
    print("(Danh sách theo Kỳ môn Độn giáp toàn thư và các bảng phổ biến; tên một số cách – nhất là Cửu độn, Tam kỳ nhập mộ – "
          "có dị bản. Cách cục chỉ bổ sung cho việc xét môn, tinh, thần và sinh khắc cung dụng thần.)")
    print()

# ---------------------------------------------------------------- Thập can khắc ứng đầy đủ (81 cặp; Giáp ẩn dưới Mậu)
# (can thiên bàn, can địa bàn) -> (tên cách, tính chất, ý nghĩa). Tên theo bảng phổ biến (Kỳ môn Độn giáp thống tông,
# Bí cấp đại toàn); dị danh ghi trong ngoặc. 0 Giáp 1 Ất 2 Bính 3 Đinh 4 Mậu 5 Kỷ 6 Canh 7 Tân 8 Nhâm 9 Quý.
KHAC_UNG_DU = {
    (4, 4): ("Phục ngâm (Thanh Long phục ngâm)", "hung", "mọi việc bế tắc, nên giữ yên, không nên tiến"),
    (4, 5): ("Quý nhân nhập ngục", "hung", "công tư đều bất lợi, tạm bị vây, chờ thời"),
    (4, 6): ("Trực phù phi cung", "hung", "việc tốt hóa không tốt, việc xấu thêm xấu; chủ đổi chỗ, đổi người"),
    (4, 7): ("Thanh Long chiết túc", "hung (cát môn còn dùng được)", "cát môn còn mưu được; hung môn hao tài, đau chân"),
    (4, 8): ("Thanh Long nhập thiên lao", "hung", "việc âm việc dương đều không tốt, vận xuống"),
    (4, 9): ("Thanh Long hoa cái", "bình", "cát môn chiêu phúc, hung môn nhiều vướng víu"),
    (4, 3): ("Thanh Long diệu minh", "cát", "lợi gặp quý nhân, cầu danh; gặp mộ, bức thì sinh thị phi"),
    (4, 2): ("Thanh Long phản thủ", "đại cát", "hành động đại cát; gặp bức, mộ, kích hình thì cát hóa hung"),
    (4, 1): ("Thanh Long hợp linh (hợp hội)", "bình", "môn cát thì việc cát, môn hung thì việc hung"),
    (5, 4): ("Khuyển ngộ Thanh Long", "bình", "môn cát thì mưu vọng toại ý, môn hung thì uổng công"),
    (5, 5): ("Địa hộ phùng quỷ", "hung", "người bệnh nguy, trăm việc không thuận"),
    (5, 6): ("Hình cách phản danh", "hung", "kiện tụng ai động trước thì thua, có người ngầm hại"),
    (5, 7): ("Du hồn nhập mộ", "hung", "âm tà quấy nhiễu, trong nhà bất an"),
    (5, 8): ("Địa võng cao trương", "hung", "gian tình, tranh chấp ngầm, thương tổn"),
    (5, 9): ("Địa hình Huyền Vũ", "hung", "bệnh nặng, tù ngục, kiện tụng"),
    (5, 3): ("Chu Tước nhập mộ", "bình", "giấy tờ, kiện tụng: trước cong sau thẳng"),
    (5, 2): ("Hỏa bội địa hộ", "hung", "oan oan tương hại; nữ đề phòng bị ô nhục"),
    (5, 1): ("Mộ thần bất minh (Địa hộ phùng tinh)", "hung", "tiền đồ mờ mịt, nên ẩn mình"),
    (6, 4): ("Trực phù phục cung (Thiên Ất phục cung)", "hung", "trăm việc không nên mưu, hao tài, tổn người"),
    (6, 5): ("Quan phủ hình cách", "hung", "kiện tụng, quan sự bị phạt nặng"),
    (6, 6): ("Thái Bạch đồng cung (chiến cách)", "hung", "tai họa quan sự, anh em đồng nghiệp tranh nhau"),
    (6, 7): ("Bạch Hổ can cách", "hung", "đi xa hỏng xe, cầu tài đại hung"),
    (6, 8): ("Tiểu cách (Di đãng cách)", "hung", "đi xa lạc đường, tin tức không thông"),
    (6, 9): ("Đại cách", "hung", "người đi không đến, quan sự không dứt, sản phụ nguy"),
    (6, 3): ("Đình đình chi cách", "hung", "vì tình riêng mà sinh kiện; môn cát thì có cứu"),
    (6, 2): ("Thái Bạch nhập Huỳnh", "hung", "giặc đến; khách lợi, chủ hao tài"),
    (6, 1): ("Thái Bạch phùng tinh", "hung", "lui thì cát, tiến thì hung"),
    (7, 4): ("Khốn long bị thương", "hung", "kiện thua, nên nhẫn nhịn giữ phận, động bừa chuốc họa"),
    (7, 5): ("Nhập ngục tự hình", "hung", "người dưới phản chủ, kiện khó thắng"),
    (7, 6): ("Bạch Hổ xuất lực", "hung", "chủ khách tàn hại nhau, lui nhường thì đỡ"),
    (7, 7): ("Phục ngâm thiên đình", "hung", "bỏ công theo tư, tự chuốc tội danh"),
    (7, 8): ("Hung xà nhập ngục", "hung", "hai nam tranh một nữ, kiện tụng không dứt"),
    (7, 9): ("Thiên lao hoa cái", "hung", "nhật nguyệt mất sáng, lầm vào lưới trời"),
    (7, 3): ("Ngục thần đắc kỳ", "cát", "buôn bán lời gấp bội, người tù gặp ân xá"),
    (7, 2): ("Can hợp bội sư", "bình", "trong hợp sinh khẩu thiệt, vì tiền sinh kiện; môn cát thì cát"),
    (7, 1): ("Bạch Hổ xương cuồng", "đại hung", "nhà suy người tán, đi xa nhiều tai ương"),
    (8, 4): ("Tiểu xà hóa long", "cát", "nam phát đạt, nữ sinh con"),
    (8, 5): ("Hung xà nhập ngục (Phản ngâm xà hình)", "hung", "họa lớn sắp đến, giữ thuận thì yên; kiện thì đuối lý"),
    (8, 6): ("Thái Bạch cầm xà", "bình", "hình ngục công bằng, phân rõ chính tà"),
    (8, 7): ("Đằng Xà tương triền", "hung", "dù cát môn cũng không yên, bị lừa dối"),
    (8, 8): ("Xà nhập địa la", "hung", "trong ngoài vướng víu; cát môn cát tinh thì đỡ"),
    (8, 9): ("Ấu nữ gian dâm", "hung", "chuyện xấu trong nhà lộ ra ngoài"),
    (8, 3): ("Can hợp xà hình", "hung", "giấy tờ liên lụy, quý nhân vội vã"),
    (8, 2): ("Thủy xà nhập hỏa", "hung", "tai họa quan sự, tù tội liên miên"),
    (8, 1): ("Tiểu xà đắc thế", "cát", "nữ nhu thuận, lợi hỏi chuyện thai nghén"),
    (9, 4): ("Thiên Ất hội hợp", "cát", "cát môn: tài, hỷ, hôn nhân; hung môn: quan phi"),
    (9, 5): ("Hoa cái địa hộ", "bình", "tin tức đều tắc; tránh nạn, ẩn mình thì cát"),
    (9, 6): ("Thái Bạch nhập võng", "hung", "tranh kiện bằng bạo lực, việc tốt thành không"),
    (9, 7): ("Võng cái thiên lao", "hung", "hỏi bệnh, hỏi kiện đại hung"),
    (9, 8): ("Phục kiến Đằng Xà", "hung", "hôn nhân trắc trở, tái giá"),
    (9, 9): ("Thiên võng tứ trương", "hung", "người đi lạc bạn, bệnh và kiện đều xấu, nên tĩnh"),
    (9, 3): ("Đằng Xà yểu kiểu", "hung", "giấy tờ quan sự, đề phòng hỏa hoạn"),
    (9, 2): ("Hoa cái bội sư", "bình", "lợi người bề trên; người âm (phụ nữ, tiểu nhân) hại việc"),
    (9, 1): ("Hoa cái phùng tinh", "cát", "quý nhân được lộc vị, người thường bình an"),
    (3, 4): ("Thanh Long chuyển quang", "cát", "quan chức thăng tiến, người thường hưng vượng"),
    (3, 5): ("Hỏa nhập Câu Trận", "hung", "tư tình, thù oán, việc do phụ nữ"),
    (3, 6): ("Văn thư trở cách (Niên nguyệt nhật thời cách)", "hung", "giấy tờ bị cản; người đi xa ắt về"),
    (3, 7): ("Chu Tước nhập ngục", "hung", "quan chức mất vị; người tù được thả"),
    (3, 8): ("Ngũ thần hỗ hợp", "cát", "quý nhân ban ơn, kiện tụng công bằng"),
    (3, 9): ("Chu Tước đầu giang", "hung", "giấy tờ khẩu thiệt, tin tức chìm mất"),
    (3, 3): ("Tinh kỳ phục ngâm (Kỳ nhập Thái Âm)", "cát", "giấy tờ sắp đến, hỷ sự toại lòng; có sách nói phục ngâm bất lợi"),
    (3, 2): ("Tinh tùy nguyệt chuyển", "cát (lẫn hung)", "quý nhân thăng vượt cấp; người thường vui quá hóa buồn"),
    (3, 1): ("Nhân độn cát cách (Ngọc nữ sinh kỳ)", "cát", "quý nhân thăng chức, người thường có hỷ, tài, hôn nhân"),
    (2, 4): ("Phi điểu điệt huyệt", "đại cát", "trăm việc cát, mưu sự thông suốt; gặp bức, mộ, kích hình lại hung"),
    (2, 5): ("Hỏa bội nhập hình", "hung", "người tù chịu hình, giấy tờ không thông; môn cát cát, môn hung hung"),
    (2, 6): ("Huỳnh nhập Thái Bạch", "hung", "nhà cửa phá bại, trộm cắp hao mất (giặc đi)"),
    (2, 7): ("Mưu sự tựu thành (Nguyệt kỳ tương hợp)", "cát", "mưu sự thành, người bệnh không nguy"),
    (2, 8): ("Hỏa nhập thiên la", "hung", "làm khách bất lợi, nhiều thị phi"),
    (2, 9): ("Hoa cái bội sư (Nguyệt kỳ địa võng)", "hung", "người âm hại việc, tai họa liên tiếp"),
    (2, 3): ("Nguyệt kỳ Chu Tước", "cát", "quý nhân, giấy tờ cát; được tam cát môn là Thiên độn"),
    (2, 2): ("Nguyệt kỳ bội sư", "hung", "giấy tờ thúc ép, hao mất"),
    (2, 1): ("Nhật nguyệt tịnh hành", "cát", "việc công việc tư đều cát"),
    (1, 4): ("Lợi âm hại dương", "hung", "lợi việc âm, bất lợi việc dương; môn hung hao tài tổn người"),
    (1, 5): ("Nhật kỳ nhập mộ (nhập vụ)", "hung", "mờ mịt bị cản; được cát môn là Địa độn"),
    (1, 6): ("Nhật kỳ bị hình", "hung", "tranh chấp tài sản, vợ chồng mỗi người một ý"),
    (1, 7): ("Thanh Long đào tẩu", "đại hung", "người dưới bỏ trốn, gia súc tổn, người tài ly tán"),
    (1, 8): ("Nhật kỳ nhập địa (nhập thiên la)", "hung", "trên dưới đảo lộn, quan tụng, có người mưu hại"),
    (1, 9): ("Hoa cái phùng tinh (Nhật kỳ địa võng)", "bình", "nên ẩn mình tránh nạn, động thì sa lưới"),
    (1, 3): ("Kỳ nghi tương tá", "cát", "giấy tờ cát, trăm việc làm được"),
    (1, 2): ("Kỳ nghi thuận toại", "cát", "cát tinh thì thăng chức; hung tinh thì vợ chồng ly biệt"),
    (1, 1): ("Nhật kỳ phục ngâm", "hung (bình)", "không nên cầu danh gặp quý, chỉ nên giữ phận"),
}


def khac_ung_cung(b, cac_cung=None):
    """Danh sách (cung, can thiên, can địa, tên, tính chất, ý nghĩa) cho mọi cặp can trong mỗi cung."""
    kq = []
    phi = b.get("loai") == "phi"
    for p in (cac_cung or ([4, 9, 2, 3, 5, 7, 8, 1, 6] if phi else [4, 9, 2, 3, 7, 8, 1, 6])):
        tcs = b["thien_can"].get(p, [])
        dcs = [b["dia"][p]] + ([b["dia"][5]] if p == 2 and not phi else [])
        for tc in tcs:
            for dc in dcs:
                ten, tinh, y = KHAC_UNG_DU[(tc, dc)]
                kq.append((p, tc, dc, ten, tinh, y))
    return kq


def in_khac_ung(b):
    print("THẬP CAN KHẮC ỨNG TỪNG CUNG (can thiên bàn + can địa bàn; Giáp ẩn dưới Mậu nên Giáp + X đọc như Mậu + X)")
    print("| Cung | Thiên + Địa | Cách | Tính chất | Ý nghĩa (tham khảo) |")
    print("|---|---|---|---|---|")
    for p, tc, dc, ten, tinh, y in khac_ung_cung(b):
        print("| %s | %s + %s | %s | %s | %s |" % (CUNG[p], CAN[tc], CAN[dc], ten, tinh, y))
    print("(Tên và cát hung theo bảng phổ biến; các sách khác nhau ở một số tên. Khắc ứng luôn xét cùng môn: "
          "cách cát gặp hung môn, môn bức, nhập mộ, kích hình thì giảm hoặc hóa hung.)")
    print()


# ---------------------------------------------------------------- PHI BÀN (phi cung kỳ môn, phái Mao Sơn / Đạo Âm)
SAO_SO = ["", "Thiên Bồng", "Thiên Nhuế", "Thiên Xung", "Thiên Phụ", "Thiên Cầm", "Thiên Tâm", "Thiên Trụ",
          "Thiên Nhậm", "Thiên Anh"]
MON_NGOAI = [1, 2, 3, 4, 6, 7, 8, 9]                       # cung nhà của 8 môn theo số Lạc Thư (trung cung không môn)
THAN9_DUONG = ["Trực Phù", "Đằng Xà", "Thái Âm", "Lục Hợp", "Câu Trận", "Thái Thường", "Chu Tước", "Cửu Địa", "Cửu Thiên"]
THAN9_AM = ["Trực Phù", "Đằng Xà", "Thái Âm", "Lục Hợp", "Bạch Hổ", "Thái Thường", "Huyền Vũ", "Cửu Địa", "Cửu Thiên"]


def _bay(p, k, duong):
    return (p - 1 + (k if duong else -k)) % 9 + 1


def ban_phi(duong, so_cuc, gz_gio):
    """Phi bàn: sao, can, thần bay theo đường Lạc Thư qua cả 9 cung (dương thuận, âm nghịch); Thiên Cầm không ký cung;
    môn: trực sử đếm từ cung tuần thủ theo can giờ (tính cả trung cung), rơi trung cung thì dương ký Cấn, âm ký Khôn,
    rồi 8 môn bay qua 8 cung ngoài (bỏ trung cung)."""
    dia = dia_ban(duong, so_cuc)
    vi_tri = {c: p for p, c in dia.items()}
    tuan = gz_gio // 10
    nghi_tuan = TUAN_NGHI[tuan]
    P = vi_tri[nghi_tuan]
    can_gio = gz_gio % 10
    Q = vi_tri[nghi_tuan if can_gio == 0 else can_gio]       # trực phù tinh bay đến cung can giờ (có thể là 5)
    thien_sao, thien_can = {}, {}
    for k in range(9):
        so = (P - 1 + k) % 9 + 1                             # sao thứ k sau trực phù (theo số Lạc Thư)
        dich = _bay(Q, k, duong)
        thien_sao[dich] = [SAO_SO[so]]
        thien_can[dich] = [dia[so]]
    if P == 5:
        mon_ts = "Sinh" if duong else "Tử"
    else:
        mon_ts = MON[P]
    D = _bay(P, can_gio, duong)
    ghi_D = ""
    if D == 5:
        D, ghi_D = (8, "rơi trung cung, dương độn ký Cấn") if duong else (2, "rơi trung cung, âm độn ký Khôn")
    i0 = MON_NGOAI.index([h for h in MON_NGOAI if MON[h] == mon_ts][0])
    j0 = MON_NGOAI.index(D)
    mon = {}
    for k in range(8):
        mon[MON_NGOAI[(j0 + (k if duong else -k)) % 8]] = MON[MON_NGOAI[(i0 + k) % 8]]
    ds_than = THAN9_DUONG if duong else THAN9_AM
    than = {_bay(Q, k, duong): ten for k, ten in enumerate(ds_than)}
    xun0 = gz_gio - gz_gio % 10
    khong = [((xun0 % 12) + 10) % 12, ((xun0 % 12) + 11) % 12]
    return dict(loai="phi", duong=duong, cuc=so_cuc, dia=dia, tuan=tuan, nghi_tuan=nghi_tuan, P=P,
                truc_phu=SAO_SO[P], truc_su=mon_ts, Q=Q, D=D, ghi_D=ghi_D, thien_sao=thien_sao,
                thien_can=thien_can, mon=mon, than=than, khong=khong, ma=DICH_MA[gz_gio % 12], gz_gio=gz_gio)


def in_ban_phi(b, tieu_de):
    print(tieu_de)
    print("- Tuần thủ: Giáp %s ẩn dưới %s (cung %s); Trực phù: %s → bay đến cung %s; Trực sử: %s môn → cung %s%s" % (
        CHI[(b["tuan"] * 10) % 12], CAN[b["nghi_tuan"]], CUNG[b["P"]], b["truc_phu"], CUNG[b["Q"]],
        b["truc_su"], CUNG[b["D"]], " (%s)" % b["ghi_D"] if b["ghi_D"] else ""))
    print("- Không vong: %s; Dịch mã: %s (cung %s)" % (
        ", ".join(CHI[z] for z in b["khong"]), CHI[b["ma"]],
        CUNG[[p for p, zs in CUNG_CHI.items() if b["ma"] in zs][0]]))
    print("| Cung | Cửu thần | Cửu tinh | Can thiên bàn | Bát môn | Can địa bàn | Ghi chú |")
    print("|---|---|---|---|---|---|---|")
    for p in [4, 9, 2, 3, 5, 7, 8, 1, 6]:
        ghi = []
        if p != 5 and set(CUNG_CHI[p]) & set(b["khong"]):
            ghi.append("Không vong")
        if p != 5 and b["ma"] in CUNG_CHI[p]:
            ghi.append("Mã")
        if p == b["Q"]:
            ghi.append("Trực phù")
        if p == b["D"]:
            ghi.append("Trực sử")
        m = b["mon"].get(p)
        print("| %s | %s | %s | %s | %s | %s | %s |" % (
            CUNG[p], b["than"][p], b["thien_sao"][p][0], CAN[b["thien_can"][p][0]],
            ("%s môn (%s)" % (m, "cát" if m in MON_CAT else ("hung" if m in MON_HUNG else "bình"))) if m else "(không môn)",
            CAN[b["dia"][p]], ", ".join(ghi)))
    print("(Phi bàn: sao và thần bay qua cả trung cung; cửu thần có Thái Thường; dương độn dùng Câu Trận, Chu Tước, "
          "âm độn dùng Bạch Hổ, Huyền Vũ. Phái khác có thể cho mọi thứ đều bay thuận hoặc ký Khôn cả hai độn.)")
    print()


# ---------------------------------------------------------------- Định cục MAO SƠN (giao tiết dùng ngay thượng nguyên)
def nguyen_mao_son(gio_tu_giao_tiet):
    """Số giờ kể từ lúc giao tiết khí: < 120 giờ thượng nguyên, < 240 trung nguyên, còn lại hạ nguyên."""
    return 0 if gio_tu_giao_tiet < 120 else (1 if gio_tu_giao_tiet < 240 else 2)


# ---------------------------------------------------------------- NIÊN GIA, NGUYỆT GIA, NHẬT GIA
def cuc_nien_gia(nam_lx):
    """Niên gia: luôn âm độn; 60 năm một nguyên: 1864 thượng (âm 1), 1924 trung (âm 4), 1984 hạ (âm 7)."""
    nguyen = ((nam_lx - 1864) // 60) % 3
    return False, (1, 4, 7)[nguyen], nguyen


def cuc_nguyet_gia(gz_nam):
    """Nguyệt gia (phái Vương Thụy Dân / Trần Bỉnh Duật): 5 năm một nguyên, lấy chi của năm Giáp/Kỷ mở đầu khối:
    Dần Thân Tỵ Hợi → thượng (âm 1), Tý Ngọ Mão Dậu → trung (âm 7), Thìn Tuất Sửu Mùi → hạ (âm 4). Luôn âm độn."""
    dau = gz_nam - gz_nam % 5
    z = dau % 12
    nguyen = 0 if z in (2, 8, 5, 11) else (1 if z in (0, 6, 3, 9) else 2)
    return False, (1, 7, 4)[nguyen], nguyen, dau


# Nhật gia (Kỳ môn pháp khiếu): ngày Giáp Tý gần tiết nào nhất thì 60 ngày đó dùng cục của tiết ấy
NHAT_GIA_MOC = {"Đông Chí": (True, 1), "Vũ Thủy": (True, 7), "Cốc Vũ": (True, 4),
                "Hạ Chí": (False, 9), "Xử Thử": (False, 3), "Sương Giáng": (False, 6)}


def cuc_nhat_gia(ngay, utc_off=7.0):
    """ngay: date (theo trụ ngày). Trả về (dương?, cục, ngày Giáp Tý mở đầu, tiết mốc)."""
    import datetime as dt
    from lich_vn import jd_from_date
    gz = (jd_from_date(ngay.day, ngay.month, ngay.year) + 49) % 60
    gt = ngay - dt.timedelta(days=gz)
    moc = [(t, n) for t, n in _tiet_khi(gt.year - 1, gt.year + 1, utc_off) if n in NHAT_GIA_MOC]
    t, n = min(moc, key=lambda x: abs((x[0].date() - gt).days))
    duong, cuc = NHAT_GIA_MOC[n]
    return duong, cuc, gt, n


# ---------------------------------------------------------------- ÂM BÀN (phái Vương Phượng Lân)
def cuc_am_ban(chi_nam, thang_am, ngay_am, chi_gio):
    """Cục = (số chi năm + tháng âm + ngày âm + số chi giờ) chia 9 lấy dư (dư 0 là 9); Tý = 1 … Hợi = 12."""
    tong = (chi_nam + 1) + thang_am + ngay_am + (chi_gio + 1)
    return tong % 9 or 9, tong


def an_can(b, duong, ky_khong_bay=False):
    """Ẩn can: xoay nguyên vòng địa bàn 8 cung (trung cung đi theo Khôn) để can giờ đến cung trực sử.
    Nếu can giờ vốn đã ở cung trực sử: can giờ nhập trung cung rồi bay 9 cung (dương thuận, âm nghịch);
    ky_khong_bay=True thì giữ ẩn can trùng địa bàn (một số bàn trong sách in như vậy)."""
    dia = b["dia"]
    cg = b["gz_gio"] % 10
    cg = TUAN_NGHI[b["gz_gio"] // 10] if cg == 0 else cg
    tap = {p: [dia[p]] + ([dia[5]] if p == 2 else []) for p in VONG}
    X = [p for p in VONG if cg in tap[p]][0]
    D = b["D"]
    if X != D:
        lech = (VONG.index(D) - VONG.index(X)) % 8
        return {VONG[(i + lech) % 8]: tap[VONG[i]] for i in range(8)}, "xoay vòng địa bàn"
    if ky_khong_bay:
        return dict(tap), "can giờ đã ở cung trực sử – ẩn can trùng địa bàn"
    k0 = NGHI.index(cg)
    kq = {(5 - 1 + (k if duong else -k)) % 9 + 1: [NGHI[(k0 + k) % 9]] for k in range(9)}
    return kq, "can giờ đã ở cung trực sử – nhập trung cung rồi bay %s 9 cung" % ("thuận" if duong else "nghịch")


# ---------------------------------------------------------------- LOẠI TƯỢNG (ý nghĩa tham khảo của từng yếu tố)
LOAI_TUONG_MON = {
    "Khai": ("Kim", "cát", "công việc, sự nghiệp, công ty, cửa hàng; khai trương, khởi sự, sáng lập; cấp trên"),
    "Hưu": ("Thủy", "cát", "nghỉ ngơi, thư thả, an dưỡng; quý nhân, gặp lãnh đạo; hôn nhân, hòa giải"),
    "Sinh": ("Thổ", "cát", "tài lộc, lợi nhuận, kinh doanh, sinh sôi; nhà đất, xây dựng"),
    "Thương": ("Mộc", "hung", "tổn thương, va chạm, cạnh tranh; xe cộ, đi lại; lợi đòi nợ, thi đấu, bắt giữ"),
    "Đỗ": ("Mộc", "bình", "bế tắc, che chắn, giữ kín; kỹ thuật, công nghệ; lợi ẩn náu, phòng thủ"),
    "Cảnh": ("Hỏa", "bình", "văn thư, giấy tờ, hợp đồng, thi cử, quảng cáo, danh tiếng; cũng chủ thị phi, máu lửa"),
    "Tử": ("Thổ", "hung", "đình trệ, kết thúc, bế tắc; đất đai cũ, mồ mả; lợi tang lễ, săn bắt"),
    "Kinh": ("Kim", "hung", "kinh sợ, lo âu, tin dữ; kiện tụng, tranh cãi; lợi luật sư, nghề ăn nói"),
}
LOAI_TUONG_SAO = {
    "Thiên Bồng": ("Thủy", "hung", "táo bạo, mưu trí, liều lĩnh; rủi ro lớn, mất mát, trộm cắp"),
    "Thiên Nhuế": ("Thổ", "hung", "bệnh, vấn đề, khuyết điểm cần sửa; học trò, người học việc"),
    "Thiên Xung": ("Mộc", "cát", "xông xáo, hành động nhanh, quyết đoán; nóng vội; thể thao, quân sự"),
    "Thiên Phụ": ("Mộc", "cát", "văn hóa, giáo dục, đào tạo, tư vấn; thầy, quý nhân phò trợ"),
    "Thiên Cầm": ("Thổ", "cát", "trung tâm, người đứng đầu, ổn định, điều phối"),
    "Thiên Tâm": ("Kim", "cát", "mưu lược, quản lý, kế hoạch, tài chính; y dược, chữa trị"),
    "Thiên Trụ": ("Kim", "hung", "khẩu thiệt, phá hoại, trở ngại; ngôn luận, phát ngôn"),
    "Thiên Nhậm": ("Thổ", "cát", "bền bỉ, gánh vác, trách nhiệm; bất động sản, nông nghiệp, kho bãi"),
    "Thiên Anh": ("Hỏa", "bình", "hình ảnh, danh tiếng, truyền thông; nóng nảy, hư danh"),
}
LOAI_TUONG_THAN = {
    "Trực Phù": "lãnh đạo, quý nhân, người có quyền; sức che chở",
    "Đằng Xà": "lo hão, quái dị, dây dưa, lừa dối, rối rắm",
    "Thái Âm": "âm thầm, mưu kín, che chở ngầm; nữ quý nhân",
    "Lục Hợp": "hợp tác, hôn nhân, môi giới, trung gian, đối tác",
    "Bạch Hổ": "uy lực, cứng rắn, sát phạt; tai nạn, bệnh, quân cảnh",
    "Huyền Vũ": "mờ ám, lừa đảo, trộm cắp, tiểu nhân; cũng chủ trí tuệ, tính toán",
    "Cửu Địa": "ổn định, bền, chậm, giữ gìn; đất đai, kho bãi, phòng thủ",
    "Cửu Thiên": "mạnh, công khai, mở rộng, vươn xa; xuất hành, quảng bá",
    "Câu Trận": "tranh chấp, kiện tụng, trì trệ; đất đai",
    "Chu Tước": "văn thư, tin tức, khẩu thiệt, cãi vã",
    "Thái Thường": "yến tiệc, lễ nghi, ăn uống, áo mũ, hỷ sự",
}
LOAI_TUONG_CAN = {
    4: "Mậu (Giáp ẩn): vốn, tiền, đầu tư; người có quyền đứng sau",
    5: "Kỷ: mưu tính ngầm, kế hoạch; ruộng đất; ám muội",
    6: "Canh: trở ngại, đối thủ, cạnh tranh, kẻ thù; chồng (người nam)",
    7: "Tân: sai sót, lỗi lầm, phiền phức, sửa chữa",
    8: "Nhâm: lưu động, vận tải, hàng hóa đi lại; cũng chủ trói buộc",
    9: "Quý: ẩn giấu, mạng lưới, dây dưa; thị phi ngầm",
    1: "Ất (Nhật kỳ): phụ nữ, vợ; thuốc, y; mềm mỏng, uyển chuyển",
    2: "Bính (Nguyệt kỳ): uy quyền, đột phá, rực rỡ; quyền lực",
    3: "Đinh (Tinh kỳ): văn thư, hợp đồng, tin tức, hy vọng",
}


def in_loai_tuong(b):
    """In ý nghĩa của môn, sao, thần, can có mặt trong bàn (tham khảo khi luận)."""
    print("LOẠI TƯỢNG CÁC YẾU TỐ TRONG BÀN (ý nghĩa tham khảo; luận phải đặt vào câu hỏi cụ thể)")
    print("| Cung | Môn | Sao | Thần |")
    print("|---|---|---|---|")
    cac = [4, 9, 2, 3, 5, 7, 8, 1, 6] if b.get("loai") == "phi" else [4, 9, 2, 3, 7, 8, 1, 6]
    for p in cac:
        m = b["mon"].get(p)
        sao = b["thien_sao"][p][0]
        th = b["than"][p]
        print("| %s | %s | %s | %s |" % (
            CUNG[p], ("%s (%s, %s): %s" % ((m,) + LOAI_TUONG_MON[m])) if m else "(không môn)",
            "%s (%s, %s): %s" % ((sao.replace("Thiên ", ""),) + LOAI_TUONG_SAO[sao]),
            "%s: %s" % (th, LOAI_TUONG_THAN.get(th, ""))))
    print("- Can: " + "; ".join(LOAI_TUONG_CAN[c] for c in [4, 5, 6, 7, 8, 9, 3, 2, 1]))
    print()


# ---------------------------------------------------------------- TRẠNG THÁI TỪNG CUNG
def tim_cung(b, gz):
    """Cung chứa can (hiện) của một can chi trên thiên bàn."""
    c = _an(gz)
    for p in ([1, 2, 3, 4, 5, 6, 7, 8, 9] if b.get("loai") == "phi" else VONG):
        if c in b["thien_can"].get(p, []):
            return p
    return None


TS12 = ["Trường sinh", "Mộc dục", "Quan đới", "Lâm quan", "Đế vượng", "Suy", "Bệnh", "Tử", "Mộ", "Tuyệt", "Thai", "Dưỡng"]
TS_CAN = {0: 11, 1: 6, 2: 2, 3: 9, 4: 2, 5: 9, 6: 5, 7: 0, 8: 8, 9: 3}     # nơi Trường sinh của 10 can (Mậu theo Bính, Kỷ theo Đinh)
TS_HANH = {"Mộc": 11, "Hỏa": 2, "Kim": 5, "Thủy": 8, "Thổ": 8}           # cho thần: Thổ theo Thủy (thủy thổ cộng mộ Thìn)
HANH_SAO = {"Thiên Bồng": "Thủy", "Thiên Nhuế": "Thổ", "Thiên Xung": "Mộc", "Thiên Phụ": "Mộc", "Thiên Cầm": "Thổ",
            "Thiên Tâm": "Kim", "Thiên Trụ": "Kim", "Thiên Nhậm": "Thổ", "Thiên Anh": "Hỏa"}
NHA_SAO = {"Thiên Bồng": 1, "Thiên Nhuế": 2, "Thiên Xung": 3, "Thiên Phụ": 4, "Thiên Cầm": 5, "Thiên Tâm": 6,
           "Thiên Trụ": 7, "Thiên Nhậm": 8, "Thiên Anh": 9}
NHA_MON = {"Hưu": 1, "Tử": 2, "Thương": 3, "Đỗ": 4, "Khai": 6, "Kinh": 7, "Sinh": 8, "Cảnh": 9}
DOI = {1: 9, 9: 1, 2: 8, 8: 2, 3: 7, 7: 3, 4: 6, 6: 4}
HANH_THAN = {"Trực Phù": "Thổ", "Đằng Xà": "Hỏa", "Thái Âm": "Kim", "Lục Hợp": "Mộc", "Bạch Hổ": "Kim",
             "Huyền Vũ": "Thủy", "Cửu Địa": "Thổ", "Cửu Thiên": "Kim", "Câu Trận": "Thổ", "Chu Tước": "Hỏa",
             "Thái Thường": "Thổ"}
MO_HANH = {"Kim": 8, "Mộc": 2, "Thủy": 4, "Thổ": 4, "Hỏa": 6}           # cung mộ theo hành (Sửu Cấn, Mùi Khôn, Thìn Tốn, Tuất Càn)
CAN_MO = {0: 2, 9: 2, 1: 6, 2: 6, 4: 6, 3: 8, 5: 8, 6: 8, 7: 4, 8: 4}   # can nhập mộ: Giáp Quý Khôn; Ất Bính Mậu Càn; Đinh Kỷ Canh Cấn; Tân Nhâm Tốn
HANH_THANG = lambda z: {2: "Mộc", 3: "Mộc", 5: "Hỏa", 6: "Hỏa", 8: "Kim", 9: "Kim", 11: "Thủy", 0: "Thủy"}.get(z, "Thổ")


def ts_tai(goc, duong, chi):
    """Vị trí trong vòng 12 trường sinh khi khởi Trường sinh ở chi `goc`, dương thuận / âm nghịch."""
    return TS12[(chi - goc) % 12 if duong else (goc - chi) % 12]


def vs_sao(hanh_sao, hanh_ref):
    """Vượng suy cửu tinh (Yên Ba điếu tẩu ca): ta sinh = vượng, đồng = tướng, ta khắc = hưu, khắc ta = tù, sinh ta = phế."""
    if hanh_sao == hanh_ref:
        return "tướng"
    if _SINH[hanh_sao] == hanh_ref:
        return "vượng"
    if _KHAC[hanh_sao] == hanh_ref:
        return "hưu"
    if _KHAC[hanh_ref] == hanh_sao:
        return "tù"
    return "phế"


def quan_he_mon(m, p):
    hm, hc = HANH_MON[m], HANH_CUNG[p]
    if hm == hc:
        return "môn cung tỷ hòa"
    if _KHAC[hm] == hc:
        return "môn bức (môn khắc cung)"
    if _KHAC[hc] == hm:
        return "môn chế (cung khắc môn)"
    if _SINH[hc] == hm:
        return "môn nghĩa (cung sinh môn)"
    return "môn hòa (môn sinh cung; có sách gọi môn tướng)"


def trang_thai(b, chi_thang):
    """Trạng thái từng cung: dict cung -> list chuỗi ngắn; kèm b['trang_thai_bang'] để in bảng."""
    kq, bang = {}, {}
    hm_thang = HANH_THANG(chi_thang)
    phi = b.get("loai") == "phi"
    for p in ([4, 9, 2, 3, 5, 7, 8, 1, 6] if phi else [4, 9, 2, 3, 7, 8, 1, 6]):
        chis = CUNG_CHI.get(p, [])
        dong = []
        m = b["mon"].get(p)
        tm = []
        if m:
            if NHA_MON[m] == p:
                tm.append("phục ngâm")
            elif DOI.get(NHA_MON[m]) == p:
                tm.append("phản ngâm")
            tm.append(quan_he_mon(m, p))
            if MO_HANH[HANH_MON[m]] == p:
                tm.append("nhập mộ")
        sao = b["thien_sao"][p][0]
        ts_ = []
        if NHA_SAO[sao] == p:
            ts_.append("phục ngâm")
        elif DOI.get(NHA_SAO[sao]) == p:
            ts_.append("phản ngâm")
        ts_.append("tháng %s" % vs_sao(HANH_SAO[sao], hm_thang))
        if p != 5:
            ts_.append("cung %s" % vs_sao(HANH_SAO[sao], HANH_CUNG[p]))
        th = b["than"][p]
        tth = " / ".join("%s %s" % (CHI[z], ts_tai(TS_HANH[HANH_THAN[th]], True, z)) for z in chis) if chis else ""
        tcan = []
        for c in (b["thien_can"][p] if chis else []):
            x = " / ".join("%s %s" % (CHI[z], ts_tai(TS_CAN[c], c % 2 == 0, z)) for z in chis)
            tcan.append("%s: %s%s" % (CAN[c], x, " – nhập mộ" if CAN_MO.get(c) == p else ""))
        bang[p] = (", ".join(tm) or "(không môn)", ", ".join(ts_), tth, "; ".join(tcan))
        if tm:
            dong.append("Môn: " + ", ".join(x.split(" (")[0] for x in tm))
        dong.append("Sao: " + ", ".join(ts_))
        if tth:
            dong.append("%s: %s" % (th, tth))
        if tcan:
            dong.append("Can " + "; ".join(tcan))
        y = []
        if m:
            y.append("%s – %s" % (m, LOAI_TUONG_MON[m][2].split(",")[0]))
        y.append("%s – %s" % (sao.replace("Thiên ", ""), LOAI_TUONG_SAO[sao][2].split(",")[0]))
        y.append("%s – %s" % (th, LOAI_TUONG_THAN.get(th, "").split(",")[0]))
        dong.append("Ý: " + " · ".join(y))
        kq[p] = dong
    b["trang_thai_bang"] = bang
    return kq


def in_trang_thai(b, tt):
    bang = b.get("trang_thai_bang", {})
    print("TRẠNG THÁI TỪNG CUNG (môn: phục/phản ngâm, quan hệ với cung, nhập mộ; sao: phục/phản ngâm, vượng suy theo "
          "tháng và theo cung; thần và can thiên bàn: 12 trường sinh tại các chi của cung)")
    print("| Cung | Môn | Sao | Thần (trường sinh) | Can thiên bàn (trường sinh) |")
    print("|---|---|---|---|---|")
    for p, (a, s_, t, c) in bang.items():
        print("| %s | %s | %s | %s %s | %s |" % (CUNG[p], a, s_, b["than"][p], t, c))
    print("(Vượng suy cửu tinh theo Yên Ba điếu tẩu ca: ta sinh = vượng, đồng hành = tướng, ta khắc = hưu, khắc ta = tù, "
          "sinh ta = phế; 'tháng' so với hành tháng, 'cung' so với hành cung – các phần mềm khác nhau chọn một trong hai, "
          "có phái đảo hưu/phế. Bát môn vượng suy theo tháng in ở trên (ngũ hành thông thường). Trường sinh của thần lấy "
          "theo hành của thần, Thổ theo Thủy (có phái lấy Trực Phù theo Giáp Mộc); can: dương thuận âm nghịch, Mậu theo "
          "Bính, Kỷ theo Đinh. Cung góc có hai chi nên ghi cả hai. Môn sinh cung: sách cổ gọi 'hòa', sách mới gọi 'tướng'.)")
    print()
