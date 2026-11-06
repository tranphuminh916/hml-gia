# -*- coding: utf-8 -*-
"""Mai hoa dịch số (Thiệu Khang Tiết): lập quẻ theo thời gian hoặc theo số; quẻ chủ, hỗ, biến; thể – dụng."""

# Tiên thiên bát quái: số -> (tên, hào (dưới, giữa, trên) 1=dương, hành, tượng)
QUAI = {1: ("Càn", (1, 1, 1), "Kim", "Thiên"), 2: ("Đoài", (1, 1, 0), "Kim", "Trạch"),
        3: ("Ly", (1, 0, 1), "Hỏa", "Hỏa"), 4: ("Chấn", (1, 0, 0), "Mộc", "Lôi"),
        5: ("Tốn", (0, 1, 1), "Mộc", "Phong"), 6: ("Khảm", (0, 1, 0), "Thủy", "Thủy"),
        7: ("Cấn", (0, 0, 1), "Thổ", "Sơn"), 8: ("Khôn", (0, 0, 0), "Thổ", "Địa")}
HAO_SO = {v[1]: k for k, v in QUAI.items()}
# Tên 64 quẻ theo (thượng, hạ)
_TEN = {
    ("Càn", "Càn"): "Thuần Càn", ("Khôn", "Khôn"): "Thuần Khôn", ("Khảm", "Chấn"): "Truân",
    ("Cấn", "Khảm"): "Mông", ("Khảm", "Càn"): "Nhu", ("Càn", "Khảm"): "Tụng", ("Khôn", "Khảm"): "Sư",
    ("Khảm", "Khôn"): "Tỷ", ("Tốn", "Càn"): "Tiểu Súc", ("Càn", "Đoài"): "Lý", ("Khôn", "Càn"): "Thái",
    ("Càn", "Khôn"): "Bĩ", ("Càn", "Ly"): "Đồng Nhân", ("Ly", "Càn"): "Đại Hữu", ("Khôn", "Cấn"): "Khiêm",
    ("Chấn", "Khôn"): "Dự", ("Đoài", "Chấn"): "Tùy", ("Cấn", "Tốn"): "Cổ", ("Khôn", "Đoài"): "Lâm",
    ("Tốn", "Khôn"): "Quan", ("Ly", "Chấn"): "Phệ Hạp", ("Cấn", "Ly"): "Bí", ("Cấn", "Khôn"): "Bác",
    ("Khôn", "Chấn"): "Phục", ("Càn", "Chấn"): "Vô Vọng", ("Cấn", "Càn"): "Đại Súc", ("Cấn", "Chấn"): "Di",
    ("Đoài", "Tốn"): "Đại Quá", ("Khảm", "Khảm"): "Thuần Khảm", ("Ly", "Ly"): "Thuần Ly",
    ("Đoài", "Cấn"): "Hàm", ("Chấn", "Tốn"): "Hằng", ("Càn", "Cấn"): "Độn", ("Chấn", "Càn"): "Đại Tráng",
    ("Ly", "Khôn"): "Tấn", ("Khôn", "Ly"): "Minh Di", ("Tốn", "Ly"): "Gia Nhân", ("Ly", "Đoài"): "Khuê",
    ("Khảm", "Cấn"): "Kiển", ("Chấn", "Khảm"): "Giải", ("Cấn", "Đoài"): "Tổn", ("Tốn", "Chấn"): "Ích",
    ("Đoài", "Càn"): "Quải", ("Càn", "Tốn"): "Cấu", ("Đoài", "Khôn"): "Tụy", ("Khôn", "Tốn"): "Thăng",
    ("Đoài", "Khảm"): "Khốn", ("Khảm", "Tốn"): "Tỉnh", ("Đoài", "Ly"): "Cách", ("Ly", "Tốn"): "Đỉnh",
    ("Chấn", "Chấn"): "Thuần Chấn", ("Cấn", "Cấn"): "Thuần Cấn", ("Tốn", "Cấn"): "Tiệm",
    ("Chấn", "Đoài"): "Quy Muội", ("Chấn", "Ly"): "Phong", ("Ly", "Cấn"): "Lữ", ("Tốn", "Tốn"): "Thuần Tốn",
    ("Đoài", "Đoài"): "Thuần Đoài", ("Tốn", "Khảm"): "Hoán", ("Khảm", "Đoài"): "Tiết",
    ("Tốn", "Đoài"): "Trung Phu", ("Chấn", "Cấn"): "Tiểu Quá", ("Khảm", "Ly"): "Ký Tế", ("Ly", "Khảm"): "Vị Tế",
}
SINH = {"Kim": "Thủy", "Thủy": "Mộc", "Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim"}
KHAC = {"Kim": "Mộc", "Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim"}
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]


def ten_que(th, ha):
    a, b = QUAI[th], QUAI[ha]
    t = _TEN[(a[0], b[0])]
    return t if t.startswith("Thuần") else "%s %s %s" % (a[3], b[3], t)


def que_tu_hao(hao6):
    return HAO_SO[tuple(hao6[3:6])], HAO_SO[tuple(hao6[0:3])]


def hao6(th, ha):
    return list(QUAI[ha][1]) + list(QUAI[th][1])


def quan_he_the(the, khac_hanh):
    if khac_hanh == the:
        return "tỷ hòa (cát)"
    if SINH[khac_hanh] == the:
        return "sinh Thể (đại cát)"
    if KHAC[the] == khac_hanh:
        return "bị Thể khắc (cát, việc thành nhưng vất vả)"
    if SINH[the] == khac_hanh:
        return "Thể sinh ra (hao tổn, tiết khí)"
    return "khắc Thể (hung)"


def vuong_suy(hanh, chi_thang):
    mua = {2: "Mộc", 3: "Mộc", 5: "Hỏa", 6: "Hỏa", 8: "Kim", 9: "Kim", 11: "Thủy", 0: "Thủy"}.get(chi_thang, "Thổ")
    if hanh == mua:
        return "vượng"
    if SINH[mua] == hanh:
        return "tướng"
    if SINH[hanh] == mua:
        return "hưu"
    if KHAC[hanh] == mua:
        return "tù"
    return "tử"


def lap(th, ha, dong):
    """th, ha: số tiên thiên 1..8; dong: hào động 1..6 (tính từ dưới lên)."""
    h = hao6(th, ha)
    ho = que_tu_hao([h[1], h[2], h[3], h[2], h[3], h[4]])
    hb = list(h)
    hb[dong - 1] ^= 1
    bien = que_tu_hao(hb)
    if dong <= 3:
        the, dung = th, ha
    else:
        the, dung = ha, th
    return dict(chu=(th, ha), ho=ho, bien=bien, dong=dong, the=the, dung=dung)


def in_que(q, chi_thang, nguon):
    the_h = QUAI[q["the"]][2]
    print("MAI HOA DỊCH SỐ – %s" % nguon)
    print("| Quẻ | Tên | Thượng / Hạ |")
    print("|---|---|---|")
    for nhan, (a, b) in (("Chủ (hiện tại)", q["chu"]), ("Hỗ (diễn biến)", q["ho"]), ("Biến (kết quả)", q["bien"])):
        print("| %s | %s | %s %s / %s %s |" % (nhan, ten_que(a, b), QUAI[a][0], QUAI[a][2], QUAI[b][0], QUAI[b][2]))
    print("- Hào động: hào %d (%s)" % (q["dong"], "quẻ hạ" if q["dong"] <= 3 else "quẻ thượng"))
    print("- Thể: %s (%s, %s theo tháng %s); Dụng: %s (%s) → Dụng %s" % (
        QUAI[q["the"]][0], the_h, vuong_suy(the_h, chi_thang), CHI[chi_thang],
        QUAI[q["dung"]][0], QUAI[q["dung"]][2], quan_he_the(the_h, QUAI[q["dung"]][2])))
    a, b = q["ho"]
    print("- Hỗ quái: %s" % "; ".join("%s (%s) %s" % (QUAI[x][0], QUAI[x][2], quan_he_the(the_h, QUAI[x][2]))
                                      for x in (a, b)))
    # Biến: Thể không động nên quái của Thể giữ nguyên trong quẻ biến; chỉ xét quái Dụng đã biến.
    x = q["bien"][1] if q["dong"] <= 3 else q["bien"][0]
    print("- Biến quái (Dụng biến thành): %s (%s) %s; quái còn lại của quẻ biến chính là Thể (không xét)" % (
        QUAI[x][0], QUAI[x][2], quan_he_the(the_h, QUAI[x][2])))
    print("(Luận: Thể là mình/việc chính, Dụng là sự việc/đối phương. Dụng sinh Thể hoặc Thể khắc Dụng là thuận; "
          "Dụng khắc Thể là nghịch. Hỗ xem quá trình, Biến xem kết cục; Thể vượng theo mùa thì có sức.)")
    print()


def theo_thoi_gian(chi_nam, thang_am, ngay_am, chi_gio):
    """Số chi: Tý=1..Hợi=12."""
    s = (chi_nam + 1) + thang_am + ngay_am
    th = s % 8 or 8
    s2 = s + chi_gio + 1
    ha = s2 % 8 or 8
    dong = s2 % 6 or 6
    return lap(th, ha, dong), (s, s2)


def theo_so(a, b, chi_gio=None):
    th = a % 8 or 8
    ha = b % 8 or 8
    t = a + b + (chi_gio + 1 if chi_gio is not None else 0)
    return lap(th, ha, t % 6 or 6), t
