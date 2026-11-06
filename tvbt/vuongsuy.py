# -*- coding: utf-8 -*-
"""vuongsuy.py - Bát tự: chấm điểm vượng suy Nhật chủ bằng HAI thang độc lập, độ tin cậy,
tự định cách cục theo nguyệt lệnh (tàng can thấu), cùng các quan hệ bổ sung: ám hợp (bản khí),
củng hợp, cái đầu / tiệt cước, lục phá, vượng tướng hưu tù tử của ngũ hành theo tháng.
Lệnh: python3 tvbt/nc.py vuongsuy --ngay 1990-05-17 --gio 08:30 --gioi nam --noi "Hà Nội"
"""
from lunar_python.util import LunarUtil

import tvbt as B

GAN = "甲乙丙丁戊己庚辛壬癸"
ZHI = "子丑寅卯辰巳午未申酉戌亥"
HANH_VN = ["Mộc", "Hỏa", "Thổ", "Kim", "Thủy"]
GAN_H = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
ZHI_H = [4, 2, 0, 0, 2, 1, 1, 2, 3, 3, 2, 4]
TANG = {z: LunarUtil.ZHI_HIDE_GAN[z] for z in ZHI}           # bản khí đứng đầu
TS12 = ["Trường Sinh", "Mộc Dục", "Quan Đới", "Lâm Quan", "Đế Vượng", "Suy", "Bệnh", "Tử", "Mộ", "Tuyệt",
        "Thai", "Dưỡng"]
TS_GOC = {"甲": 11, "丙": 2, "戊": 2, "庚": 5, "壬": 8, "乙": 6, "丁": 9, "己": 9, "辛": 0, "癸": 3}
NHOM = ["Tỷ Kiếp", "Ấn", "Thực Thương", "Tài", "Quan Sát"]


def truong_sinh(g, z):
    """Chỉ số 12 trường sinh của can g tại chi z (dương thuận, âm nghịch; Mậu theo Bính, Kỷ theo Đinh)."""
    i0 = TS_GOC[g]
    zi = ZHI.index(z)
    return (zi - i0) % 12 if GAN.index(g) % 2 == 0 else (i0 - zi) % 12


def thap_than(nc, g):
    """Thập thần của can g so với nhật chủ nc."""
    a, b = GAN_H[GAN.index(nc)], GAN_H[GAN.index(g)]
    cung_dau = GAN.index(nc) % 2 == GAN.index(g) % 2
    k = (b - a) % 5          # 0 đồng, 1 ta sinh, 2 ta khắc, 3 khắc ta, 4 sinh ta
    ten = [("Tỷ Kiên", "Kiếp Tài"), ("Thực Thần", "Thương Quan"), ("Thiên Tài", "Chính Tài"),
           ("Thất Sát", "Chính Quan"), ("Thiên Ấn", "Chính Ấn")][k]
    return ten[0] if cung_dau else ten[1]


def nhom(nc, g):
    a, b = GAN_H[GAN.index(nc)], GAN_H[GAN.index(g)]
    return {0: "Tỷ Kiếp", 1: "Thực Thương", 2: "Tài", 3: "Quan Sát", 4: "Ấn"}[(b - a) % 5]


# ---------------------------------------------------------------- Thang A (theo bazi-enrich, MIT)
LENH_A = {"Tỷ Kiếp": 5, "Ấn": 3, "Thực Thương": -3, "Quan Sát": -4, "Tài": -5}
TS_A = {0: 2, 4: 2, 3: 1, 2: 1, 1: 0, 5: 0, 6: -1, 7: -1, 8: -3, 9: -3, 10: -3, 11: -3}
DIA_A = {"Tỷ Kiếp": (2, 0.8, 0.5), "Ấn": (1, 0.5, 0.3)}
THE_A = {"Tỷ Kiếp": 1, "Ấn": 0.7, "Thực Thương": -0.5, "Tài": -1, "Quan Sát": -1.5}
NGUONG_A = [(8, "cực vượng"), (3, "vượng"), (-2.5, "trung hòa"), (-8, "nhược")]


def thang_a(tru):
    """tru: list (nhãn, can, chi) theo thứ tự Năm, Tháng, Ngày[, Giờ]. Trả (điểm, mức, chi tiết)."""
    nc = tru[2][1]
    zt = tru[1][2]
    ct = []
    tg = TANG[zt]
    n0 = nhom(nc, tg[0])
    p = LENH_A[n0]
    ct.append("đắc lệnh: bản khí %s của tháng %s là %s %+g" % (B.vn(tg[0]), B.vn(zt), n0, LENH_A[n0]))
    for g in tg[1:]:
        n = nhom(nc, g)
        if n in ("Tỷ Kiếp", "Ấn"):
            v = 1 if n == "Tỷ Kiếp" else 0.7
            p += v
            ct.append("dư khí %s (%s) %+g" % (B.vn(g), n, v))
    # Từ 11/2026: can âm xét vượng suy theo hành như can dương cùng hành (Trích Thiên Tủy – Nhậm Thiết Tiều chú:
    # không dùng "âm sinh dương tử" khi xét mạnh yếu). Bazi-enrich gốc dùng trường sinh nghịch cho can âm.
    nc_d = GAN[GAN.index(nc) - GAN.index(nc) % 2]
    i = truong_sinh(nc_d, zt)
    p += TS_A[i]
    ct.append("nhật chủ %s ở tháng %s: %s %+g%s" % (B.vn(nc), B.vn(zt), TS12[i], TS_A[i],
                                                   "" if nc_d == nc else " (theo hành, như %s)" % B.vn(nc_d)))
    dia = 0
    for nh, g, z in tru:
        if nh in ("Năm", "Ngày", "Giờ"):
            for k, h in enumerate(TANG[z][:3]):
                n = nhom(nc, h)
                if n in DIA_A:
                    dia += DIA_A[n][k]
    p += dia
    ct.append("đắc địa (tàng can chi năm/ngày/giờ): %+g" % round(dia, 2))
    the = 0
    for nh, g, z in tru:
        if nh != "Ngày":
            the += THE_A[nhom(nc, g)]
    p += the
    ct.append("đắc thế (các can còn lại): %+g" % round(the, 2))
    p = round(p, 2)
    if p >= 8:
        muc = "cực vượng"
    elif p >= 3:
        muc = "vượng"
    elif p > -2.5:
        muc = "trung hòa"
    elif p > -8:
        muc = "nhược"
    else:
        muc = "cực nhược"
    kc = min(abs(p - x) for x in (8, 3, -2.5, -8))
    return p, muc, kc, ct


# ---------------------------------------------------------------- Thang B (đếm điểm 5 hành)
def diem_chi(z):
    tg = TANG[z]
    if z in "子卯酉":
        return [(tg[0], 8)]
    if z in "午亥":
        return [(tg[0], 5), (tg[1], 3)]
    return list(zip(tg, (5, 2, 1)))


def thang_b(tru):
    """Mỗi can 5 điểm; chi Tý Mão Dậu 8; Ngọ Hợi 5+3; chi khác 5/2/1 theo tàng can; chi tháng tính 2 lần.
    Thân mạnh khi Tỷ Kiếp + Ấn (kể cả nhật chủ) vượt 48% tổng (≈ 29/60 với đủ 4 trụ)."""
    nc = tru[2][1]
    hanh = [0.0] * 5
    ta = 0.0
    tong = 0.0
    for nh, g, z in tru:
        hanh[GAN_H[GAN.index(g)]] += 5
        tong += 5
        if nhom(nc, g) in ("Tỷ Kiếp", "Ấn"):
            ta += 5
        lan = 2 if nh == "Tháng" else 1
        for h, v in diem_chi(z):
            hanh[GAN_H[GAN.index(h)]] += v * lan
            tong += v * lan
            if nhom(nc, h) in ("Tỷ Kiếp", "Ấn"):
                ta += v * lan
    ty_le = ta / tong
    muc = "vượng" if ty_le > 0.48 else "nhược"
    if ty_le >= 0.75:
        muc = "cực vượng"
    elif ty_le <= 0.2:
        muc = "cực nhược"
    elif 0.42 <= ty_le <= 0.54:
        muc = "trung hòa (nghiêng %s)" % ("vượng" if ty_le > 0.48 else "nhược")
    return ta, tong, ty_le, muc, hanh


# ---------------------------------------------------------------- Cách cục
LOC = dict(zip("甲乙丙丁戊己庚辛壬癸", "寅卯巳午巳午申酉亥子"))
NHAN = {"甲": "卯", "丙": "午", "戊": "午", "庚": "酉", "壬": "子"}


def cach_cuc(tru):
    nc = tru[2][1]
    zt = tru[1][2]
    tg = TANG[zt]
    can_lo = {g for nh, g, z in tru if nh != "Ngày"}
    i = truong_sinh(nc, zt)
    if LOC[nc] == zt:
        return ("Kiến Lộc cách", "chi tháng %s là Lộc của nhật chủ %s (có sách không lập cách này mà lấy can thấu khác)"
                % (B.vn(zt), B.vn(nc)), "cao")
    if NHAN.get(nc) == zt:
        return ("Dương Nhận cách", "chi tháng %s là Dương Nhận của nhật chủ %s%s" % (
            B.vn(zt), B.vn(nc), " (Mậu nhận ở Ngọ tùy phái)" if nc == "戊" else ""), "cao" if nc != "戊" else "trung bình")
    tt0 = thap_than(nc, tg[0])
    if zt in "子午卯酉":
        ten, ly, tin = tt0, "tháng Tý Ngọ Mão Dậu: lấy bản khí %s" % B.vn(tg[0]), "cao"
    else:
        thau = [g for g in tg if g in can_lo and nhom(nc, g) != "Tỷ Kiếp"]
        if thau:
            g = thau[0]
            ten = thap_than(nc, g)
            ly = "tàng can %s của tháng %s thấu lên can" % (B.vn(g), B.vn(zt))
            tin = "cao" if g == tg[0] else "trung bình"
        else:
            ten, ly, tin = tt0, "không tàng can nào (ngoài Tỷ Kiếp) thấu: lấy bản khí %s" % B.vn(tg[0]), "trung bình"
    if ten in ("Tỷ Kiên", "Kiếp Tài"):
        if zt in "辰戌丑未":
            return ("Tạp khí – bản khí %s (chưa thành cách rõ)" % ten,
                    ly + "; tháng tứ khố, cần xét tàng can khác và đại vận thấu xuất", "thấp")
        return "Nguyệt Kiếp cách", ly, tin
    return ten + " cách", ly, tin


# ---------------------------------------------------------------- Quan hệ bổ sung
NGU_HOP = {frozenset("甲己"), frozenset("乙庚"), frozenset("丙辛"), frozenset("丁壬"), frozenset("戊癸")}
LUC_PHA = [frozenset(x) for x in ("子酉", "丑辰", "寅亥", "卯午", "巳申", "未戌")]
CUNG_HOP = {frozenset("申辰"): "Tý", frozenset("亥未"): "Mão", frozenset("寅戌"): "Ngọ", frozenset("巳丑"): "Dậu"}
MUA_VUONG = {"寅": 0, "卯": 0, "巳": 1, "午": 1, "申": 3, "酉": 3, "亥": 4, "子": 4, "辰": 2, "未": 2, "戌": 2, "丑": 2}


def quan_he_bo_sung(tru):
    kq = []
    for i in range(len(tru)):
        for j in range(i + 1, len(tru)):
            a, b = tru[i], tru[j]
            za, zb = a[2], b[2]
            if frozenset((TANG[za][0], TANG[zb][0])) in NGU_HOP and za != zb:
                kq.append("Ám hợp %s–%s (bản khí %s hợp %s): %s – %s" % (
                    B.vn(za), B.vn(zb), B.vn(TANG[za][0]), B.vn(TANG[zb][0]), a[0], b[0]))
            if frozenset((za, zb)) in CUNG_HOP and CUNG_HOP[frozenset((za, zb))] not in [B.vn(z) for _, _, z in tru]:
                kq.append("Củng hợp %s–%s (thiếu %s ở giữa, chưa thành tam hợp): %s – %s" % (
                    B.vn(za), B.vn(zb), CUNG_HOP[frozenset((za, zb))], a[0], b[0]))
            if frozenset((za, zb)) in LUC_PHA:
                kq.append("Lục phá %s–%s: %s – %s" % (B.vn(za), B.vn(zb), a[0], b[0]))
    for nh, g, z in tru:
        hg, hz = GAN_H[GAN.index(g)], ZHI_H[ZHI.index(z)]
        if (hz - hg) % 5 == 2:
            kq.append("Cái đầu ở trụ %s (%s khắc %s: can đè chi)" % (nh, B.vn(g), B.vn(z)))
        elif (hg - hz) % 5 == 2:
            kq.append("Tiệt cước ở trụ %s (%s khắc %s: chi chặt chân can)" % (nh, B.vn(z), B.vn(g)))
    return list(dict.fromkeys(kq))


def vuong_tuong(zt):
    """Vượng tướng hưu tù tử của 5 hành theo chi tháng (tháng tứ quý: Thổ vượng)."""
    v = MUA_VUONG[zt]
    ten = {0: "Vượng", 1: "Tướng", 2: "Tử", 3: "Tù", 4: "Hưu"}   # theo quan hệ hành lệnh -> hành x
    kq = {}
    for h in range(5):
        k = (h - v) % 5      # 0 đồng=vượng, 1 lệnh sinh=tướng, 4 sinh lệnh=hưu, 3 khắc lệnh=tù, 2 lệnh khắc=tử
        kq[HANH_VN[h]] = ten[k]
    return kq


def lay_tru(tt):
    _, _, tru = B.tu_tru(tt)
    return [(nh, gz[0], gz[1]) for nh, gz in tru]


def in_vuong_suy(tru):
    nc = tru[2][1]
    print("VƯỢNG SUY NHẬT CHỦ – CHẤM ĐIỂM HAI THANG (tham khảo cho bước chọn dụng thần)")
    print("- Tứ trụ: " + ", ".join("%s %s" % (nh, B.vn(g + z)) for nh, g, z in tru)
          + ("" if len(tru) == 4 else " (không có trụ giờ: điểm kém tin cậy)"))
    pa, ma, kc, ct = thang_a(tru)
    ta, tong, tl, mb, hanh = thang_b(tru)
    print("| Thang | Điểm | Mức | Căn cứ |")
    print("|---|---|---|---|")
    print("| A – đắc lệnh/địa/thế | %+.1f (ngưỡng: ≥8 cực vượng, ≥3 vượng, >−2,5 trung hòa, >−8 nhược) | %s | %s |" % (
        pa, ma, "; ".join(ct)))
    print("| B – đếm điểm ngũ hành | ta (Tỷ Kiếp + Ấn) %.0f / %.0f = %.0f%% (ngưỡng 48%%) | %s | %s |" % (
        ta, tong, 100 * tl, mb, ", ".join("%s %.0f" % (HANH_VN[i], hanh[i]) for i in range(5))))
    cung_chieu = ("vượng" in ma and "vượng" in mb and "nghiêng nhược" not in mb) or \
                 ("nhược" in ma and "nhược" in mb and "nghiêng vượng" not in mb) or \
                 ("trung hòa" in ma and "trung hòa" in mb)
    if not cung_chieu:
        tin = "THẤP – hai thang lệch nhau"
    elif kc > 2:
        tin = "cao"
    elif kc > 0.8:
        tin = "trung bình"
    else:
        tin = "thấp – sát ngưỡng"
    if len(tru) < 4:
        tin = "thấp – thiếu trụ giờ"
    print("- Độ tin của kết luận vượng/nhược: %s." % tin)
    if not cung_chieu:
        print("! Hai thang cho kết quả khác nhau: phải xét kỹ bằng tay (đắc lệnh có phải là yếu tố quyết định? "
              "có hợp hóa, xung phá làm mất gốc không?) và nói rõ là còn hai cách hiểu.")
    vt = vuong_tuong(tru[1][2])
    print("- Ngũ hành theo tháng %s: %s" % (B.vn(tru[1][2]), ", ".join("%s %s" % (k, v) for k, v in vt.items())))
    ten, ly, tin_cc = cach_cuc(tru)
    print("- CÁCH CỤC (theo nguyệt lệnh): %s – %s; độ tin %s. (Cách cục cho biết cấu trúc lá số, "
          "không phải dụng thần.)" % (ten, ly, tin_cc))
    qh = quan_he_bo_sung(tru)
    if qh:
        print("- Quan hệ bổ sung: " + "; ".join(qh))
    print()
    return dict(a=(pa, ma), b=(tl, mb), tin=tin, cach=ten)


def them_lenh(sub):
    import nc
    p = sub.add_parser("vuongsuy", help="Bát tự: chấm điểm vượng suy 2 thang, cách cục, quan hệ bổ sung")
    nc.them_tham_so_sinh(p, gioi_bat_buoc=True)
    p.set_defaults(_chay=chay)


def chay(a):
    if not a.ngay:
        raise SystemExit("LỖI: cần --ngay (ngày sinh).")
    tt = B.doc_dau_vao(a)
    for c in tt.canh_bao:
        print("! " + c)
    in_vuong_suy(lay_tru(tt))


def tu_kiem():
    loi = []
    # 1. Lá số tự kiểm của v2: 2000-01-01 10:00 Hà Nội = Kỷ Mão, Bính Tý, Mậu Ngọ, Đinh Tỵ (tính tay theo công thức)
    tru = [("Năm", "己", "卯"), ("Tháng", "丙", "子"), ("Ngày", "戊", "午"), ("Giờ", "丁", "巳")]
    pa, ma, _, _ = thang_a(tru)
    # đắc lệnh Tài −5; Mậu ở Tý = Thai −3; đắc địa: Ngọ (Đinh Ấn 1 + Kỷ Kiếp 0,8) + Tỵ (Bính Ấn 1 + Mậu Tỷ 0,5) = 3,3;
    # đắc thế: Kỷ +1, Bính +0,7, Đinh +0,7 = 2,4  → −2,3 = trung hòa
    if abs(pa - (-2.3)) > 1e-6 or ma != "trung hòa":
        loi.append("thang A lá số 2000-01-01: %s %s" % (pa, ma))
    ta, tong, tl, mb, hanh = thang_b(tru)
    # ta = can Kỷ, Bính, Mậu, Đinh 20 + Ngọ 8 + Tỵ (Bính 5 + Mậu 1) 6 = 34; tổng = 20 + 8 + 16 + 8 + 8 = 60
    if (ta, tong) != (34, 60):
        loi.append("thang B lá số 2000-01-01: %s/%s" % (ta, tong))
    if cach_cuc(tru)[0] != "Chính Tài cách":
        loi.append("cách cục 2000-01-01: %s" % cach_cuc(tru)[0])
    # 1b. Can âm xét theo hành (từ 11/2026): Ất Tỵ sinh tháng Ngọ – Canh Ngọ, Nhâm Ngọ, Ất Tỵ, Nhâm Ngọ (09/06/1990 12:00)
    #     Ất ở Ngọ tính như Giáp ở Ngọ (Tử −1), không phải Trường sinh +2 → thang A cùng chiều thang B: nhược.
    tru = [("Năm", "庚", "午"), ("Tháng", "壬", "午"), ("Ngày", "乙", "巳"), ("Giờ", "壬", "午")]
    pa, ma, _, _ = thang_a(tru)
    if ma != "nhược" or thang_b(tru)[3] != "nhược":
        loi.append("Ất Tỵ tháng Ngọ: thang A %s (%s), thang B %s" % (ma, pa, thang_b(tru)[3]))
    # 2. Kiến Lộc / Dương Nhận / tàng can thấu
    if cach_cuc([("Năm", "壬", "子"), ("Tháng", "丙", "寅"), ("Ngày", "乙", "子"), ("Giờ", "甲", "子")])[0] != "Thương Quan cách":
        loi.append("Ất sinh tháng Dần, Bính thấu phải là Thương Quan cách")
    if cach_cuc([("Năm", "壬", "子"), ("Tháng", "壬", "寅"), ("Ngày", "甲", "子"), ("Giờ", "甲", "子")])[0] != "Kiến Lộc cách":
        loi.append("Giáp sinh tháng Dần phải là Kiến Lộc cách")
    for nc_, zt_ in (("戊", "巳"), ("己", "午"), ("辛", "酉")):
        if cach_cuc([("Năm", "壬", "子"), ("Tháng", "癸", zt_), ("Ngày", nc_, "子"), ("Giờ", "甲", "子")])[0] != "Kiến Lộc cách":
            loi.append("%s sinh tháng %s phải là Kiến Lộc cách" % (nc_, zt_))
    if "Củng" in " ".join(quan_he_bo_sung([("Năm", "甲", "申"), ("Tháng", "丙", "子"), ("Ngày", "戊", "辰"), ("Giờ", "庚", "申")])):
        loi.append("đủ Thân Tý Thìn mà vẫn báo củng hợp")
    if cach_cuc([("Năm", "壬", "子"), ("Tháng", "壬", "卯"), ("Ngày", "甲", "子"), ("Giờ", "甲", "子")])[0] != "Dương Nhận cách":
        loi.append("Giáp sinh tháng Mão phải là Dương Nhận cách")
    # 3. 12 trường sinh chuẩn: Giáp trường sinh Hợi, Ất trường sinh Ngọ, Canh Tỵ, Tân Tý, Nhâm Thân, Quý Mão
    for g, z in zip("甲乙丙丁戊己庚辛壬癸", "亥午寅酉寅酉巳子申卯"):
        if truong_sinh(g, z) != 0:
            loi.append("trường sinh %s" % g)
    if TS12[truong_sinh("甲", "卯")] != "Đế Vượng" or TS12[truong_sinh("乙", "寅")] != "Đế Vượng":
        loi.append("Đế vượng Giáp/Ất")
    # 4. Vượng tướng: tháng Dần Mộc vượng, Hỏa tướng, Thủy hưu, Kim tù, Thổ tử
    if vuong_tuong("寅") != {"Mộc": "Vượng", "Hỏa": "Tướng", "Thổ": "Tử", "Kim": "Tù", "Thủy": "Hưu"}:
        loi.append("vượng tướng tháng Dần: %s" % vuong_tuong("寅"))
    # 5. Quan hệ: Mão–Thân ám hợp, Thân–Thìn củng hợp, Tý–Dậu phá
    q = " ".join(quan_he_bo_sung([("Năm", "甲", "卯"), ("Tháng", "壬", "申"), ("Ngày", "丙", "辰"), ("Giờ", "丁", "酉")]))
    for k in ("Ám hợp Mão–Thân", "Củng hợp Thân–Thìn"):
        if k not in q:
            loi.append("thiếu %s" % k)
    if "Lục phá Tý–Dậu" not in " ".join(quan_he_bo_sung([("Năm", "甲", "子"), ("Tháng", "癸", "酉"), ("Ngày", "丙", "辰")])):
        loi.append("thiếu Lục phá Tý–Dậu")
    # 6. Chạy ngẫu nhiên không lỗi, điểm trong khoảng hợp lý
    import random
    rnd = random.Random(7)
    for _ in range(3000):
        tru = []
        for nh in ("Năm", "Tháng", "Ngày", "Giờ"):
            i = rnd.randrange(60)
            tru.append((nh, GAN[i % 10], ZHI[i % 12]))
        pa, *_ = thang_a(tru)
        tl = thang_b(tru)[2]
        cach_cuc(tru)
        quan_he_bo_sung(tru)
        if not (-25 < pa < 25 and 0 <= tl <= 1):
            loi.append("điểm bất thường %s" % tru)
            break
    return loi
