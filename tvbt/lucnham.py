# -*- coding: utf-8 -*-
"""Đại Lục Nhâm: thiên địa bàn (Nguyệt tướng gia giờ), tứ khóa, tam truyền theo Cửu tông môn,
12 thiên tướng, lục thân, độn can, không vong. Chỉ số can 0=Giáp..9=Quý, chi 0=Tý..11=Hợi."""

CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
TEN_TUONG = {11: "Đăng Minh", 10: "Hà Khôi", 9: "Tòng Khôi", 8: "Truyền Tống", 7: "Tiểu Cát", 6: "Thắng Quang",
             5: "Thái Ất", 4: "Thiên Cương", 3: "Thái Xung", 2: "Công Tào", 1: "Đại Cát", 0: "Thần Hậu"}
# Trung khí -> Nguyệt tướng
NGUYET_TUONG = {"Vũ Thủy": 11, "Xuân Phân": 10, "Cốc Vũ": 9, "Tiểu Mãn": 8, "Hạ Chí": 7, "Đại Thử": 6,
                "Xử Thử": 5, "Thu Phân": 4, "Sương Giáng": 3, "Tiểu Tuyết": 2, "Đông Chí": 1, "Đại Hàn": 0}
KY_CUNG = [2, 4, 5, 7, 5, 7, 8, 10, 11, 1]
CAN_KY = {2: [0], 4: [1], 5: [2, 4], 7: [3, 5], 8: [6], 10: [7], 11: [8], 1: [9]}
HANH_CAN = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]                    # 0 Mộc 1 Hỏa 2 Thổ 3 Kim 4 Thủy
HANH_CHI = [4, 2, 0, 0, 2, 1, 1, 2, 3, 3, 2, 4]
TEN_HANH = ["Mộc", "Hỏa", "Thổ", "Kim", "Thủy"]
KHAC = lambda a, b: (b - a) % 5 == 2                          # hành a khắc hành b
SINH = lambda a, b: (b - a) % 5 == 1
HINH = {0: 3, 3: 0, 2: 5, 5: 8, 8: 2, 1: 10, 10: 7, 7: 1, 4: 4, 6: 6, 9: 9, 11: 11}
DICH_MA = {0: 2, 4: 2, 8: 2, 2: 8, 6: 8, 10: 8, 5: 11, 9: 11, 1: 11, 11: 5, 3: 5, 7: 5}
CAN_HOP = {0: 5, 5: 0, 1: 6, 6: 1, 2: 7, 7: 2, 3: 8, 8: 3, 4: 9, 9: 4}
TAM_HOP_TRUOC = {8: 0, 0: 4, 4: 8, 5: 9, 9: 1, 1: 5, 2: 6, 6: 10, 10: 2, 11: 3, 3: 7, 7: 11}
# Quý nhân (trú, dạ) theo can ngày – bản thông dụng của Lục Nhâm
QUY_NHAN = {0: (1, 7), 4: (1, 7), 6: (1, 7), 1: (0, 8), 5: (0, 8), 2: (11, 9), 3: (11, 9),
            8: (5, 3), 9: (5, 3), 7: (6, 2)}
THIEN_TUONG = ["Quý Nhân", "Đằng Xà", "Chu Tước", "Lục Hợp", "Câu Trận", "Thanh Long",
               "Thiên Không", "Bạch Hổ", "Thái Thường", "Huyền Vũ", "Thái Âm", "Thiên Hậu"]


def lap(gz_ngay, chi_gio, tuong):
    g, z = gz_ngay % 10, gz_ngay % 12
    T = {x: (tuong + x - chi_gio) % 12 for x in range(12)}
    vi_tri = {v: k for k, v in T.items()}                      # thiên chi -> địa chi bên dưới
    ky = KY_CUNG[g]
    k1 = T[ky]
    khoa = [  # (nhãn dưới, hành dưới, chi dưới (để so trùng), chi trên)
        (CAN[g], HANH_CAN[g], ky, k1),
        (CHI[k1], HANH_CHI[k1], k1, T[k1]),
        (CHI[z], HANH_CHI[z], z, T[z]),
        (CHI[T[z]], HANH_CHI[T[z]], T[z], T[T[z]]),
    ]
    duong = g % 2 == 0
    ghi = []
    phuc = tuong == chi_gio
    phan = (tuong - chi_gio) % 12 == 6
    tac = [k for k in khoa if KHAC(k[1], HANH_CHI[k[3]])]       # hạ khắc thượng (tặc)
    kh = [k for k in khoa if KHAC(HANH_CHI[k[3]], k[1])]        # thượng khắc hạ
    co_khac = bool(tac or kh)
    so = trung = mat = None
    if phuc:
        ten = "Phục ngâm"
        if co_khac:
            so = k1
            ghi.append("có khắc nên lấy can thượng thần")
        else:
            so = k1 if duong else T[z]
        if HINH[so] == so:
            khac_ = T[z] if so == k1 else k1
            trung = khac_ if khac_ != so else (so + 6) % 12
        else:
            trung = HINH[so]
        mat = HINH[trung]
        if mat == trung or mat == so:
            mat = (trung + 6) % 12
        return ket_qua(ten, ghi, khoa, T, vi_tri, so, trung, mat, g, z, chi_gio)
    if phan and not co_khac:
        so, trung, mat = DICH_MA[z], T[z], k1
        return ket_qua("Phản ngâm (vô khắc – Tỉnh lan xạ)", ghi, khoa, T, vi_tri, so, trung, mat, g, z, chi_gio)
    if co_khac:
        ds = tac if tac else kh
        loai = "tặc (hạ khắc thượng)" if tac else "khắc (thượng khắc hạ)"
        uppers = []
        for k in ds:
            if k[3] not in [u[3] for u in uppers]:
                uppers.append(k)
        if len(uppers) == 1:
            ten = "Trùng thẩm" if tac else "Nguyên thủ"
            so = uppers[0][3]
        else:
            ty = [k for k in uppers if (k[3] % 2 == 0) == duong]
            if len(ty) == 1:
                ten = "Tỷ dụng"
                so = ty[0][3]
            else:
                ten = "Thiệp hại"
                cands = ty if ty else uppers
                so, ly_do = thiep_hai(cands, vi_tri, bool(tac), duong, khoa)
                ghi.append(ly_do)
        ghi.insert(0, "có %d khóa %s" % (len(ds), loai))
        if phan:
            ten = "Phản ngâm – " + ten
    else:
        bat_chuyen = ky == z
        if bat_chuyen:
            ten = "Bát chuyên"
            so = (k1 + 2) % 12 if duong else (khoa[3][3] - 2) % 12
            trung = mat = k1
            return ket_qua(ten, ghi, khoa, T, vi_tri, so, trung, mat, g, z, chi_gio)
        hao = [k for k in khoa[1:] if KHAC(HANH_CHI[k[3]], HANH_CAN[g])]   # thần khắc can ngày
        dan = [k for k in khoa[1:] if KHAC(HANH_CAN[g], HANH_CHI[k[3]])]   # can ngày khắc thần
        ds = hao or dan
        if ds:
            ten = "Dao khắc – " + ("Hao thỉ" if hao else "Đạn xạ")
            uppers = []
            for k in ds:
                if k[3] not in uppers:
                    uppers.append(k[3])
            ty = [u for u in uppers if (u % 2 == 0) == duong]
            so = (ty or uppers)[0]
            if len(ty or uppers) > 1:
                ghi.append("nhiều thần dao khắc ngang nhau – lấy thần đầu theo thứ tự khóa (các sách xử khác nhau)")
        else:
            khac_biet = len({(k[2], k[3]) for k in khoa})
            if khac_biet == 4:
                ten = "Mão tinh"
                if duong:
                    so, trung, mat = T[9], T[z], k1
                else:
                    so, trung, mat = vi_tri[9], k1, T[z]
                return ket_qua(ten, ghi, khoa, T, vi_tri, so, trung, mat, g, z, chi_gio)
            ten = "Biệt trách"
            so = T[KY_CUNG[CAN_HOP[g]]] if duong else TAM_HOP_TRUOC[z]
            trung = mat = k1
            return ket_qua(ten, ghi, khoa, T, vi_tri, so, trung, mat, g, z, chi_gio)
    trung = T[so]
    mat = T[trung]
    return ket_qua(ten, ghi, khoa, T, vi_tri, so, trung, mat, g, z, chi_gio)


def thiep_hai(cands, vi_tri, la_tac, duong, khoa):
    """Đếm số lần bị khắc (tặc) / đi khắc (khắc) từ chỗ đang đứng (địa bàn) về nhà; sâu nhất làm sơ truyền.
    Bằng nhau: lấy thần đứng trên Mạnh (Dần Thân Tỵ Hợi), rồi Trọng (Tý Ngọ Mão Dậu), rồi can/chi thượng."""
    diem = []
    for k in cands:
        u = k[3]
        x = vi_tri[u]
        n = 0
        p = x
        while p != u:
            hanh = [HANH_CHI[p]] + [HANH_CAN[c] for c in CAN_KY.get(p, [])]
            for h in hanh:
                if (KHAC(h, HANH_CHI[u]) if la_tac else KHAC(HANH_CHI[u], h)):
                    n += 1
            p = (p + 1) % 12
        diem.append((n, k))
    m = max(d[0] for d in diem)
    top = [k for d, k in diem if d == m]
    if len(top) == 1:
        return top[0][3], "thiệp hại sâu nhất: %s (%d lần)" % (CHI[top[0][3]], m)
    for nhom, ten in (((2, 8, 5, 11), "Mạnh – Kiến cơ"), ((0, 6, 3, 9), "Trọng – Sát vi")):
        t2 = [k for k in top if vi_tri[k[3]] in nhom]
        if len(t2) == 1:
            return t2[0][3], "thiệp hại bằng nhau (%d), lấy thần lâm %s: %s" % (m, ten, CHI[t2[0][3]])
        if t2:
            top = t2
            break
    k = khoa[0] if duong else khoa[2]
    chon = k[3] if k[3] in [x[3] for x in top] else top[0][3]
    return chon, "thiệp hại bằng nhau, lấy %s thượng thần: %s (Phục đẳng)" % ("can" if duong else "chi", CHI[chon])


def luc_than(g, chi):
    a, b = HANH_CAN[g], HANH_CHI[chi]
    if a == b:
        return "Huynh đệ"
    if SINH(b, a):
        return "Phụ mẫu"
    if SINH(a, b):
        return "Tử tôn"
    if KHAC(a, b):
        return "Thê tài"
    return "Quan quỷ"


def ket_qua(ten, ghi, khoa, T, vi_tri, so, trung, mat, g, z, chi_gio):
    tru = 3 <= chi_gio <= 8
    qn = QUY_NHAN[g][0 if tru else 1]
    dia_qn = vi_tri[qn]
    thuan = dia_qn in (11, 0, 1, 2, 3, 4)
    tuong = {(qn + (k if thuan else -k)) % 12: THIEN_TUONG[k] for k in range(12)}
    xun = (z - g) % 12
    khong = ((xun + 10) % 12, (xun + 11) % 12)
    don = {(xun + i) % 12: CAN[i] for i in range(10)}
    return dict(ten=ten, ghi=ghi, khoa=khoa, T=T, truyen=[so, trung, mat], tuong=tuong, thuan=thuan,
                tru=tru, qn=qn, khong=khong, don=don, g=g, z=z)


def in_khoa(r, ten_ngay, ten_gio, nguyet_tuong, trung_khi):
    g = r["g"]
    print("ĐẠI LỤC NHÂM")
    print("- Ngày %s, giờ %s; trung khí %s → Nguyệt tướng %s (%s) gia giờ %s" % (
        ten_ngay, ten_gio, trung_khi, CHI[nguyet_tuong], TEN_TUONG[nguyet_tuong], ten_gio.split()[-1]))
    print("- Quý nhân %s ở %s (thiên bàn), %s; không vong ngày: %s" % (
        "trú" if r["tru"] else "dạ", CHI[r["qn"]], "thuận" if r["thuan"] else "nghịch",
        " ".join(CHI[x] for x in r["khong"])))
    print("| Địa bàn | " + " | ".join(CHI) + " |")
    print("|---|" + "---|" * 12)
    print("| Thiên bàn | " + " | ".join(CHI[r["T"][x]] for x in range(12)) + " |")
    print("| Thiên tướng | " + " | ".join(r["tuong"][r["T"][x]] for x in range(12)) + " |")
    print()
    print("TỨ KHÓA (thứ tự từ phải sang trái như sách: khóa 4 | 3 | 2 | 1)")
    print("| | Khóa 4 | Khóa 3 | Khóa 2 | Khóa 1 |")
    print("|---|---|---|---|---|")
    ks = r["khoa"][::-1]
    print("| Thiên tướng | " + " | ".join(r["tuong"][k[3]] for k in ks) + " |")
    print("| Thượng | " + " | ".join(CHI[k[3]] for k in ks) + " |")
    print("| Hạ | " + " | ".join(k[0] for k in ks) + " |")
    print()
    print("TAM TRUYỀN – khóa thể: %s%s" % (r["ten"], (" (" + "; ".join(r["ghi"]) + ")") if r["ghi"] else ""))
    print("| | Chi | Độn can | Lục thân | Thiên tướng | Ghi chú |")
    print("|---|---|---|---|---|---|")
    for nhan, c in zip(("Sơ truyền", "Trung truyền", "Mạt truyền"), r["truyen"]):
        print("| %s | %s (%s) | %s | %s | %s | %s |" % (
            nhan, CHI[c], TEN_HANH[HANH_CHI[c]], r["don"].get(c, "–"), luc_than(g, c), r["tuong"][c],
            "Không vong" if c in r["khong"] else ""))
    print("(Sơ truyền: khởi đầu/nguyên nhân; Trung: diễn biến; Mạt: kết cục. Quý nhân trú/dạ lấy theo giờ Mão–Thân "
          "là ngày; có phái dùng giờ mặt trời mọc/lặn. Bảng Quý nhân Lục Nhâm có dị bản ở can Canh, Tân.)")
    print()
