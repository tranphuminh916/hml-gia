# -*- coding: utf-8 -*-
"""An sao Tử vi Đẩu số theo cách an phổ biến ở Việt Nam (chủ yếu theo Tử Vi Đẩu Số Tân Biên –
Thái Thứ Lang; bảng miếu/hãm 14 chính tinh tham khảo lasotuvi (MIT, doanguyen)).
Chỉ số cung: 0=Tý, 1=Sửu, 2=Dần, ... 11=Hợi. Giờ: 0=Tý ... 11=Hợi. Can năm: 0=Giáp ... 9=Quý."""

CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
TEN_CUNG = ["Mệnh", "Phụ Mẫu", "Phúc Đức", "Điền Trạch", "Quan Lộc", "Nô Bộc",
            "Thiên Di", "Tật Ách", "Tài Bạch", "Tử Tức", "Phu Thê", "Huynh Đệ"]
CUC = {"Thủy": 2, "Mộc": 3, "Kim": 4, "Thổ": 5, "Hỏa": 6}
TEN_CUC = {2: "Thủy Nhị Cục", 3: "Mộc Tam Cục", 4: "Kim Tứ Cục", 5: "Thổ Ngũ Cục", 6: "Hỏa Lục Cục"}
# Hành nạp âm của 60 hoa giáp (theo cặp): Giáp Tý Ất Sửu Kim, Bính Dần Đinh Mão Hỏa, ...
_NAP_AM_HANH = ["Kim", "Hỏa", "Mộc", "Thổ", "Kim", "Hỏa", "Thủy", "Thổ", "Kim", "Mộc",
                "Thủy", "Thổ", "Hỏa", "Mộc", "Thủy", "Kim", "Hỏa", "Mộc", "Thổ", "Kim",
                "Hỏa", "Thủy", "Thổ", "Kim", "Mộc", "Thủy", "Thổ", "Hỏa", "Mộc", "Thủy"]


def hanh_nap_am(can, chi):
    if can % 2 != chi % 2:
        raise ValueError("can chi không hợp lệ")
    idx = [i for i in range(60) if i % 10 == can and i % 12 == chi][0]
    return _NAP_AM_HANH[idx // 2]


VONG_BAC_SI = ["Bác Sĩ", "Lực Sĩ", "Thanh Long", "Tiểu Hao", "Tướng Quân", "Tấu Thư",
               "Phi Liêm", "Hỷ Thần", "Bệnh Phù", "Đại Hao", "Phục Binh", "Quan Phủ"]
VONG_THAI_TUE = ["Thái Tuế", "Thiếu Dương", "Tang Môn", "Thiếu Âm", "Quan Phù", "Tử Phù",
                 "Tuế Phá", "Long Đức", "Bạch Hổ", "Phúc Đức", "Điếu Khách", "Trực Phù"]
VONG_TRANG_SINH = ["Tràng Sinh", "Mộc Dục", "Quan Đới", "Lâm Quan", "Đế Vượng", "Suy",
                   "Bệnh", "Tử", "Mộ", "Tuyệt", "Thai", "Dưỡng"]
LOC_TON = [2, 3, 5, 6, 5, 6, 8, 9, 11, 0]
# Khôi, Việt theo can: "Giáp Mậu thị Ngưu Dương, Ất Kỷ thử hầu hương, Canh Tân phùng Mã Hổ,
# Nhâm Quý thỏ xà tàng, Bính Đinh trư kê vị"
KHOI_VIET = {0: (1, 7), 4: (1, 7), 1: (0, 8), 5: (0, 8), 6: (6, 2), 7: (6, 2),
             8: (3, 5), 9: (3, 5), 2: (11, 9), 3: (11, 9)}
THIEN_QUAN = [7, 4, 5, 2, 3, 9, 11, 9, 10, 6]
THIEN_PHUC = [9, 8, 0, 11, 3, 2, 6, 5, 6, 5]
THIEN_TRU = [5, 6, 0, 5, 6, 8, 2, 6, 9, 10]
LUU_HA = [9, 10, 7, 8, 5, 6, 4, 3, 11, 2]
# Lưu Văn Xương / Văn Khúc theo can năm xem
LUU_XUONG = [5, 6, 8, 9, 8, 9, 11, 0, 2, 3]
LUU_KHUC = [9, 8, 6, 5, 6, 5, 3, 2, 0, 11]
# Cân lượng (xương cốt) – Viên Thiên Cương; đơn vị chỉ (1 lượng = 10 chỉ). Năm theo 60 hoa giáp, bắt đầu Giáp Tý.
_CL_NAM_TU_CANH_TY = [7, 7, 9, 12, 8, 7, 13, 5, 14, 5, 9, 17, 5, 7, 12, 8, 8, 6, 19, 6, 8, 16, 10, 6, 12, 9, 6, 7, 12,
                      5, 9, 8, 7, 8, 15, 9, 16, 8, 8, 19, 12, 6, 8, 7, 5, 15, 6, 16, 15, 7, 9, 12, 10, 7, 15, 6, 5, 14,
                      14, 9]
CL_NAM = [_CL_NAM_TU_CANH_TY[(i - 36) % 60] for i in range(60)]
CL_THANG = [6, 7, 18, 9, 5, 16, 9, 15, 18, 8, 9, 5]
CL_NGAY = [5, 10, 8, 15, 16, 15, 8, 16, 8, 16, 9, 17, 8, 17, 10, 8, 9, 18, 5, 15, 10, 9, 8, 9, 15, 18, 7, 8, 16, 6]
CL_GIO = [16, 6, 7, 10, 9, 16, 10, 8, 8, 9, 6, 6]
TRIET = {0: (8, 9), 5: (8, 9), 1: (6, 7), 6: (6, 7), 2: (4, 5), 7: (4, 5),
         3: (2, 3), 8: (2, 3), 4: (0, 1), 9: (0, 1)}
# Tứ hóa (Lộc, Quyền, Khoa, Kỵ) – bảng thông dụng ở Việt Nam
TU_HOA = {0: ["Liêm Trinh", "Phá Quân", "Vũ Khúc", "Thái Dương"],
          1: ["Thiên Cơ", "Thiên Lương", "Tử Vi", "Thái Âm"],
          2: ["Thiên Đồng", "Thiên Cơ", "Văn Xương", "Liêm Trinh"],
          3: ["Thái Âm", "Thiên Đồng", "Thiên Cơ", "Cự Môn"],
          4: ["Tham Lang", "Thái Âm", "Hữu Bật", "Thiên Cơ"],
          5: ["Vũ Khúc", "Tham Lang", "Thiên Lương", "Văn Khúc"],
          6: ["Thái Dương", "Vũ Khúc", "Thái Âm", "Thiên Đồng"],
          7: ["Cự Môn", "Thái Dương", "Văn Khúc", "Văn Xương"],
          8: ["Thiên Lương", "Tử Vi", "Tả Phù", "Vũ Khúc"],
          9: ["Phá Quân", "Cự Môn", "Thái Âm", "Tham Lang"]}
HOA = ["Hóa Lộc", "Hóa Quyền", "Hóa Khoa", "Hóa Kỵ"]
MENH_CHU = ["Tham Lang", "Cự Môn", "Lộc Tồn", "Văn Khúc", "Liêm Trinh", "Vũ Khúc",
            "Phá Quân", "Vũ Khúc", "Liêm Trinh", "Văn Khúc", "Lộc Tồn", "Cự Môn"]
THAN_CHU = ["Linh Tinh", "Thiên Tướng", "Thiên Lương", "Thiên Đồng", "Văn Xương", "Thiên Cơ",
            "Hỏa Tinh", "Thiên Tướng", "Thiên Lương", "Thiên Đồng", "Văn Xương", "Thiên Cơ"]
# Miếu (M) / Vượng (V) / Đắc (Đ) / Bình (B) / Hãm (H) theo 12 cung Tý..Hợi
DO_SANG = {
    "Tử Vi": "B Đ M B V M M Đ M B V B", "Liêm Trinh": "V Đ V H M H V Đ V H M H",
    "Thiên Đồng": "V H M Đ H Đ H H M H H Đ", "Vũ Khúc": "V M V Đ M H V M V Đ M H",
    "Thái Dương": "H Đ V V V M M Đ H H H H", "Thiên Cơ": "Đ Đ H M M V Đ Đ V M M H",
    "Thái Âm": "V Đ H H H H H Đ V M M M", "Tham Lang": "H M Đ H V H H M Đ H V H",
    "Cự Môn": "V H V M H H V H Đ M H Đ", "Thiên Tướng": "V Đ M H V Đ V Đ M H V Đ",
    "Thiên Lương": "V Đ V V M H M Đ V H M H", "Thất Sát": "M Đ M H H V M Đ M H H V",
    "Phá Quân": "M V H H Đ H M V H H Đ H",
    "Kình Dương": "H Đ H H Đ H H Đ H H Đ H", "Đà La": "H Đ H H Đ H H Đ H H Đ H",
    "Hỏa Tinh": "H H Đ Đ Đ Đ Đ H H H H H", "Linh Tinh": "H H Đ Đ Đ Đ Đ H H H H H",
    "Địa Không": "H H Đ H H Đ H H Đ H H Đ", "Địa Kiếp": "H H Đ H H Đ H H Đ H H Đ",
}
# Độ sáng hiển thị thêm cho Thiên Phủ và một số phụ tinh (bảng Việt Nam, theo bài từng sao trên tuvi.vn và
# Tử Vi Đẩu Số Tân Biên). Chỉ dùng để HIỂN THỊ (do_sang_day_du); các phép chấm cách cục, vận thế vẫn dùng DO_SANG
# như cũ để không đổi kết quả đã kiểm. "-" = sao không bao giờ đóng ở cung đó hoặc sách không ghi.
DO_SANG_PHU = {
    "Thiên Phủ": "M B M B V Đ M Đ M B V Đ",      # miếu Dần Thân Tý Ngọ; vượng Thìn Tuất; đắc Tỵ Hợi Mùi; bình Mão Dậu Sửu
    "Văn Xương": "H Đ H B Đ Đ H Đ H B Đ Đ",      # đắc Tứ mộ + Tỵ Hợi (Thái Thứ Lang); hãm Tý Dần Ngọ Thân
    "Văn Khúc": "H Đ H B Đ Đ H Đ H B Đ Đ",
    "Thiên Mã": "- - V - - V - - Đ - - H",        # Dần Tỵ tốt nhất, Thân đắc, Hợi hãm (bài sao Thiên Mã, tuvi.vn)
    "Thiên Hình": "H H Đ Đ H H H H Đ Đ H H",      # đắc Dần Thân Mão Dậu
    "Thiên Diêu": "H H Đ Đ H H H H H Đ Đ H",      # đắc Dần Mão Dậu Tuất
    "Thiên Khốc": "Đ Đ H Đ H H Đ Đ H Đ H H",      # đắc Tý Ngọ Mão Dậu Sửu Mùi
    "Thiên Hư": "Đ Đ H Đ H H Đ Đ H Đ H H",
}
CHINH_TINH = ["Tử Vi", "Thiên Cơ", "Thái Dương", "Vũ Khúc", "Thiên Đồng", "Liêm Trinh",
              "Thiên Phủ", "Thái Âm", "Tham Lang", "Cự Môn", "Thiên Tướng", "Thiên Lương",
              "Thất Sát", "Phá Quân"]


def vi_tri_tu_vi(cuc, ngay):
    pos, q = 2, cuc
    while q < ngay:
        q += cuc
        pos += 1
    lech = q - ngay
    return (pos - lech if lech % 2 == 1 else pos + lech) % 12


def lap_la_so(thang, ngay, gio, can, chi, gioi, thang_do_dai=30, nhuan=False):
    """thang/ngay: tháng, ngày âm lịch; gio 0..11; can 0..9; chi 0..11 (của NĂM âm lịch);
    gioi: 'nam'|'nu'. Tháng nhuận: ngày 16 trở đi tính sang tháng sau (cách phổ biến)."""
    if nhuan and ngay > 15:
        thang = thang % 12 + 1
    g = 1 if gioi == "nam" else -1
    ad = 1 if can % 2 == 0 else -1
    chieu = g * ad                      # +1: Dương Nam/Âm Nữ (thuận); -1: Âm Nam/Dương Nữ (nghịch)
    menh = (2 + thang - 1 - gio) % 12
    than = (2 + thang - 1 + gio) % 12
    can_dan = (can % 5) * 2 + 2
    can_cung = {p: (can_dan + (p - 2) % 12) % 10 for p in range(12)}  # Dần..Sửu nối tiếp (Tý, Sửu sau Hợi)
    cuc = CUC[hanh_nap_am(can_cung[menh], menh)]
    sao = {p: [] for p in range(12)}

    def an(ten, p):
        sao[p % 12].append(ten)
        return p % 12

    vt = {}

    def dat(ten, p):
        vt[ten] = an(ten, p)
        return vt[ten]

    tv = dat("Tử Vi", vi_tri_tu_vi(cuc, ngay))
    for ten, k in (("Thiên Cơ", -1), ("Thái Dương", -3), ("Vũ Khúc", -4), ("Thiên Đồng", -5), ("Liêm Trinh", 4)):
        dat(ten, tv + k)
    tp = dat("Thiên Phủ", 4 - tv)
    for ten, k in (("Thái Âm", 1), ("Tham Lang", 2), ("Cự Môn", 3), ("Thiên Tướng", 4),
                   ("Thiên Lương", 5), ("Thất Sát", 6), ("Phá Quân", 10)):
        dat(ten, tp + k)
    lt = dat("Lộc Tồn", LOC_TON[can])
    dat("Kình Dương", lt + 1)
    dat("Đà La", lt - 1)
    dat("Văn Khúc", 4 + gio)
    dat("Văn Xương", 10 - gio)
    dat("Tả Phù", 4 + thang - 1)
    dat("Hữu Bật", 10 - (thang - 1))
    k, v = KHOI_VIET[can]
    dat("Thiên Khôi", k)
    dat("Thiên Việt", v)
    dat("Địa Kiếp", 11 + gio)
    dat("Địa Không", 11 - gio)
    nhom = chi % 4  # 0: Thân Tý Thìn, 1: Tỵ Dậu Sửu, 2: Dần Ngọ Tuất, 3: Hợi Mão Mùi
    khoi_hoa, khoi_linh = {0: (2, 10), 1: (3, 10), 2: (1, 3), 3: (9, 10)}[nhom]
    dat("Hỏa Tinh", khoi_hoa + chieu * gio)
    dat("Linh Tinh", khoi_linh - chieu * gio)
    dat("Thiên Mã", {0: 2, 1: 11, 2: 8, 3: 5}[nhom])
    dat("Hoa Cái", vt["Thiên Mã"] + 2)
    dat("Kiếp Sát", vt["Thiên Mã"] + 3)
    dat("Đào Hoa", vt["Thiên Mã"] + 7)
    dat("Long Trì", 4 + chi)
    dat("Phượng Các", 10 - chi)
    dat("Giải Thần", 10 - chi)
    dat("Thiên Hư", 6 + chi)
    dat("Thiên Khốc", 6 - chi)
    dat("Hồng Loan", 3 - chi)
    dat("Thiên Hỷ", 9 - chi)
    dat("Thiên Tài", menh + chi)
    dat("Thiên Thọ", than + chi)
    co = {11: 2, 0: 2, 1: 2, 2: 5, 3: 5, 4: 5, 5: 8, 6: 8, 7: 8, 8: 11, 9: 11, 10: 11}[chi]
    dat("Cô Thần", co)
    dat("Quả Tú", co - 4)
    dat("Phá Toái", {0: 5, 6: 5, 3: 5, 9: 5, 2: 9, 8: 9, 5: 9, 11: 9}.get(chi, 1))
    dat("Thiên Hình", 9 + thang - 1)
    dat("Thiên Diêu", 1 + thang - 1)
    dat("Thiên Y", 1 + thang - 1)
    dat("Thiên Giải", 8 + thang - 1)
    dat("Địa Giải", 7 + thang - 1)
    dat("Tam Thai", vt["Tả Phù"] + ngay - 1)
    dat("Bát Tọa", vt["Hữu Bật"] - (ngay - 1))
    dat("Ân Quang", vt["Văn Xương"] + ngay - 2)
    dat("Thiên Quý", vt["Văn Khúc"] - ngay + 2)
    dat("Thai Phụ", vt["Văn Khúc"] + 2)
    dat("Phong Cáo", vt["Văn Khúc"] - 2)
    dat("Thiên Quan", THIEN_QUAN[can])
    dat("Thiên Phúc", THIEN_PHUC[can])
    dat("Thiên Trù", THIEN_TRU[can])
    dat("Lưu Hà", LUU_HA[can])
    dat("Lưu Niên Văn Tinh", lt + 3)
    dat("Đường Phù", lt + 5)
    dat("Quốc Ấn", lt + 8)
    dat("Đẩu Quân", chi - (thang - 1) + gio)
    dat("Thiên La", 4)
    dat("Địa Võng", 10)
    dat("Thiên Thương", menh + 5)
    dat("Thiên Sứ", menh + 7)
    dat("Thiên Không", chi + 1)
    dat("Thiên Đức", chi + 9)
    dat("Nguyệt Đức", chi + 5)
    bac_si = {(lt + chieu * i) % 12: VONG_BAC_SI[i] for i in range(12)}
    thai_tue = {(chi + i) % 12: VONG_THAI_TUE[i] for i in range(12)}
    ts0 = {6: 2, 4: 5, 2: 8, 5: 8, 3: 11}[cuc]
    trang_sinh = {(ts0 + chieu * i) % 12: VONG_TRANG_SINH[i] for i in range(12)}
    hoa = {}
    for i, ten in enumerate(TU_HOA[can]):
        hoa[ten] = HOA[i]
    xun0 = (chi - can) % 12
    tuan = ((xun0 - 2) % 12, (xun0 - 1) % 12)
    triet = TRIET[can]
    dai_han = {}
    for p in range(12):
        k = ((p - menh) * chieu) % 12
        dai_han[p] = (cuc + 10 * k, cuc + 10 * k + 9)
    tieu_han_goc = {0: 10, 1: 7, 2: 4, 3: 1}[nhom]
    return dict(menh=menh, than=than, cuc=cuc, can_cung=can_cung, sao=sao, vt=vt, hoa=hoa,
                bac_si=bac_si, thai_tue=thai_tue, trang_sinh=trang_sinh, tuan=tuan, triet=triet,
                dai_han=dai_han, chieu=chieu, g=g, can=can, chi=chi, thang=thang, ngay=ngay, gio=gio,
                tieu_han_goc=tieu_han_goc, menh_chu=MENH_CHU[chi], menh_chu_cung=MENH_CHU[menh],
                than_chu=THAN_CHU[chi] + (" (có sách ghi %s)" % ("Hỏa Tinh" if chi == 0 else "Linh Tinh")
                                          if chi in (0, 6) else ""))


def ten_cung(ls, p):
    return TEN_CUNG[(p - ls["menh"]) % 12]


def do_sang(ten, p):
    s = DO_SANG.get(ten)
    return s.split()[p] if s else ""


def do_sang_day_du(ten, p):
    """Độ sáng để hiển thị: chính tinh, sát tinh (DO_SANG) + Thiên Phủ và phụ tinh (DO_SANG_PHU)."""
    s = DO_SANG.get(ten) or DO_SANG_PHU.get(ten)
    v = s.split()[p] if s else ""
    return "" if v == "-" else v


def can_luong(can, chi, thang, ngay, gio):
    """Cân lượng xương cốt: trả về (tổng chỉ, chi tiết). can/chi năm âm lịch, tháng/ngày âm lịch, giờ 0..11."""
    i = [k for k in range(60) if k % 10 == can and k % 12 == chi][0]
    ct = (CL_NAM[i], CL_THANG[thang - 1], CL_NGAY[ngay - 1], CL_GIO[gio])
    return sum(ct), ct


def cung_luu(goc):
    """Tên 12 cung lưu khi lấy cung 'goc' làm Mệnh (đi thuận như lá số gốc): dict cung -> tên."""
    return {(goc + k) % 12: TEN_CUNG[k] for k in range(12)}


def van_han(ls, nam_can, nam_chi, tuoi_mu):
    """Vận hạn một năm âm lịch (can, chi của năm xem; tuổi mụ)."""
    dh = [p for p, (a, b) in ls["dai_han"].items() if a <= tuoi_mu <= b]
    th = (ls["tieu_han_goc"] + ls["g"] * ((nam_chi - ls["chi"]) % 12)) % 12
    lt = LOC_TON[nam_can]
    luu = {"Lưu Thái Tuế": nam_chi, "Lưu Tang Môn": (nam_chi + 2) % 12,
           "Lưu Bạch Hổ": (nam_chi + 8) % 12, "Lưu Thiên Khốc": (6 - nam_chi) % 12,
           "Lưu Thiên Hư": (6 + nam_chi) % 12, "Lưu Lộc Tồn": lt, "Lưu Kình Dương": (lt + 1) % 12,
           "Lưu Đà La": (lt - 1) % 12,
           "Lưu Thiên Mã": {0: 2, 1: 11, 2: 8, 3: 5}[nam_chi % 4]}
    ma = luu["Lưu Thiên Mã"]
    khoi, viet = KHOI_VIET[nam_can]
    luu.update({"Lưu Thiên Khôi": khoi, "Lưu Thiên Việt": viet,
                "Lưu Văn Xương": LUU_XUONG[nam_can], "Lưu Văn Khúc": LUU_KHUC[nam_can],
                "Lưu Đào Hoa": (ma + 7) % 12, "Lưu Hồng Loan": (3 - nam_chi) % 12,
                "Lưu Thiên Hỷ": (9 - nam_chi) % 12, "Lưu Kiếp Sát": (ma + 3) % 12})
    hoa = list(zip(HOA, TU_HOA[nam_can]))
    return dict(dai_han=dh[0] if dh else None, tieu_han=th, luu=luu, hoa=hoa)


def phi_hoa(ls):
    """Tứ hóa phi tinh: can của mỗi cung phát 4 hóa vào cung có sao đó.
    Trả về dict cung -> list (hóa, sao, cung đích); và lai nhân cung."""
    kq = {}
    for p in range(12):
        ds = []
        for i, ten in enumerate(TU_HOA[ls["can_cung"][p]]):
            ds.append((HOA[i], ten, ls["vt"][ten]))
        kq[p] = ds
    # Lai nhân cung: cung (Dần..Hợi) có can trùng can năm sinh (Tý, Sửu trùng can với Dần, Mão nên bỏ)
    lai = [p for p in range(2, 12) if ls["can_cung"][p] == ls["can"]]
    return kq, (lai[0] if lai else None)
