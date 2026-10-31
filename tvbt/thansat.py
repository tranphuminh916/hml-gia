# -*- coding: utf-8 -*-
"""Thần sát Bát tự (bảng phổ biến theo Tam Mệnh Thông Hội / Uyên Hải Tử Bình).
Chỉ số: can 0=Giáp..9=Quý; chi 0=Tý..11=Hợi. Một trụ = (can, chi)."""

CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
TEN_TRU = ["Năm", "Tháng", "Ngày", "Giờ"]

# --- theo can (ngày, có phái xét cả can năm)
QUY_NHAN = {0: (1, 7), 4: (1, 7), 6: (1, 7), 1: (0, 8), 5: (0, 8), 2: (11, 9), 3: (11, 9),
            8: (3, 5), 9: (3, 5), 7: (2, 6)}                       # Giáp Mậu Canh ngưu dương...
VAN_XUONG = [5, 6, 8, 9, 8, 9, 11, 0, 2, 3]
THAI_CUC = {0: (0, 6), 1: (0, 6), 2: (3, 9), 3: (3, 9), 4: (4, 10, 1, 7), 5: (4, 10, 1, 7),
            6: (2, 11), 7: (2, 11), 8: (5, 8), 9: (5, 8)}
LOC = [2, 3, 5, 6, 5, 6, 8, 9, 11, 0]
DUONG_NHAN = {0: 3, 2: 6, 4: 6, 6: 9, 8: 0}                        # chỉ can dương
KIM_DU = [4, 5, 7, 8, 7, 8, 10, 11, 1, 2]                          # Lộc + 2
HONG_DIEM = [6, 8, 2, 7, 4, 4, 10, 9, 0, 8]
QUOC_AN = [10, 11, 1, 2, 1, 2, 4, 5, 7, 8]
LUU_HA = [9, 10, 7, 8, 5, 6, 4, 3, 11, 2]
# --- theo chi (năm và ngày) – nhóm tam hợp: 0 Thân Tý Thìn, 1 Tỵ Dậu Sửu, 2 Dần Ngọ Tuất, 3 Hợi Mão Mùi
NHOM = lambda z: {8: 0, 0: 0, 4: 0, 5: 1, 9: 1, 1: 1, 2: 2, 6: 2, 10: 2, 11: 3, 3: 3, 7: 3}[z]
DICH_MA = [2, 11, 8, 5]
DAO_HOA = [9, 6, 3, 0]
HOA_CAI = [4, 1, 10, 7]
TUONG_TINH = [0, 9, 6, 3]
KIEP_SAT = [5, 2, 11, 8]
VONG_THAN = [11, 8, 5, 2]
# --- theo chi tháng
THIEN_DUC = {2: ("can", 3), 3: ("chi", 8), 4: ("can", 8), 5: ("can", 7), 6: ("chi", 11), 7: ("can", 0),
             8: ("can", 9), 9: ("chi", 2), 10: ("can", 2), 11: ("can", 1), 0: ("chi", 5), 1: ("can", 6)}
NGUYET_DUC = {2: 2, 6: 2, 10: 2, 8: 8, 0: 8, 4: 8, 11: 0, 3: 0, 7: 0, 5: 6, 9: 6, 1: 6}  # can
CAN_HOP = {0: 5, 5: 0, 1: 6, 6: 1, 2: 7, 7: 2, 3: 8, 8: 3, 4: 9, 9: 4}
CHI_HOP = {0: 1, 1: 0, 2: 11, 11: 2, 3: 10, 10: 3, 4: 9, 9: 4, 5: 8, 8: 5, 6: 7, 7: 6}
# --- theo trụ ngày
KHOI_CUONG = {(6, 4), (6, 10), (8, 4), (4, 10)}
AM_DUONG_SAI = {(2, 0), (2, 6), (3, 1), (3, 7), (4, 2), (4, 8), (7, 3), (7, 9), (8, 4), (8, 10), (9, 5), (9, 11)}
THAP_AC = {(0, 4), (1, 5), (2, 8), (3, 11), (4, 10), (5, 1), (6, 4), (7, 5), (8, 8), (9, 11)}
CO_LOAN = {(1, 5), (3, 5), (7, 11), (4, 8), (0, 2), (8, 0), (2, 6), (4, 6)}
THIEN_XA = {0: (4, 2), 1: (0, 6), 2: (4, 8), 3: (0, 0)}            # mùa: Xuân, Hạ, Thu, Đông


def mua(chi_thang):
    return {2: 0, 3: 0, 4: 0, 5: 1, 6: 1, 7: 1, 8: 2, 9: 2, 10: 2, 11: 3, 0: 3, 1: 3}[chi_thang]


def tinh(tru):
    """tru: list (can, chi) theo thứ tự Năm, Tháng, Ngày[, Giờ]. Trả về list (tên, căn cứ, [trụ có])."""
    kq = []
    n = len(tru)
    can_ngay, chi_ngay = tru[2]
    can_nam, chi_nam = tru[0]
    chi_thang = tru[1][1]
    chis = [t[1] for t in tru]
    cans = [t[0] for t in tru]

    def tim_chi(ds, bo=None):
        return [TEN_TRU[i] for i in range(n) if chis[i] in ds and i != bo]

    def them(ten, can_cu, noi):
        if noi:
            kq.append((ten, can_cu, noi))

    # theo can ngày (và can năm)
    for goc, ten_goc in ((can_ngay, "can ngày"), (can_nam, "can năm")):
        them("Thiên Ất Quý Nhân", "%s %s → %s" % (ten_goc, CAN[goc], "/".join(CHI[z] for z in QUY_NHAN[goc])),
             tim_chi(QUY_NHAN[goc]))
        them("Văn Xương", "%s %s → %s" % (ten_goc, CAN[goc], CHI[VAN_XUONG[goc]]), tim_chi([VAN_XUONG[goc]]))
        them("Thái Cực Quý Nhân", "%s %s → %s" % (ten_goc, CAN[goc], "/".join(CHI[z] for z in THAI_CUC[goc])),
             tim_chi(THAI_CUC[goc]))
    g = can_ngay
    them("Lộc thần (Kiến Lộc)", "can ngày %s → %s" % (CAN[g], CHI[LOC[g]]), tim_chi([LOC[g]]))
    if g in DUONG_NHAN:
        them("Dương Nhận", "can ngày %s → %s" % (CAN[g], CHI[DUONG_NHAN[g]]), tim_chi([DUONG_NHAN[g]]))
    them("Kim Dư", "can ngày %s → %s" % (CAN[g], CHI[KIM_DU[g]]), tim_chi([KIM_DU[g]]))
    them("Hồng Diễm", "can ngày %s → %s" % (CAN[g], CHI[HONG_DIEM[g]]), tim_chi([HONG_DIEM[g]]))
    them("Quốc Ấn", "can ngày %s → %s" % (CAN[g], CHI[QUOC_AN[g]]), tim_chi([QUOC_AN[g]]))
    them("Lưu Hà", "can ngày %s → %s" % (CAN[g], CHI[LUU_HA[g]]), tim_chi([LUU_HA[g]]))
    # theo chi năm và chi ngày (không tính chính trụ gốc)
    for goc_i, ten_goc in ((0, "chi năm"), (2, "chi ngày")):
        z = chis[goc_i]
        k = NHOM(z)
        for ten, bang in (("Dịch Mã", DICH_MA), ("Đào Hoa (Hàm Trì)", DAO_HOA), ("Hoa Cái", HOA_CAI),
                          ("Tướng Tinh", TUONG_TINH), ("Kiếp Sát", KIEP_SAT), ("Vong Thần", VONG_THAN)):
            them(ten, "%s %s → %s" % (ten_goc, CHI[z], CHI[bang[k]]), tim_chi([bang[k]], bo=goc_i))
    # theo chi năm
    z = chi_nam
    co = {11: 2, 0: 2, 1: 2, 2: 5, 3: 5, 4: 5, 5: 8, 6: 8, 7: 8, 8: 11, 9: 11, 10: 11}[z]
    qua = (co - 4) % 12
    them("Cô Thần", "chi năm %s → %s" % (CHI[z], CHI[co]), tim_chi([co], bo=0))
    them("Quả Tú", "chi năm %s → %s" % (CHI[z], CHI[qua]), tim_chi([qua], bo=0))
    hl, th = (3 - z) % 12, (9 - z) % 12
    them("Hồng Loan", "chi năm %s → %s" % (CHI[z], CHI[hl]), tim_chi([hl], bo=0))
    them("Thiên Hỷ", "chi năm %s → %s" % (CHI[z], CHI[th]), tim_chi([th], bo=0))
    # theo chi tháng
    loai, v = THIEN_DUC[chi_thang]
    ten_v = CAN[v] if loai == "can" else CHI[v]
    noi = [TEN_TRU[i] for i in range(n) if (cans[i] == v if loai == "can" else chis[i] == v)]
    them("Thiên Đức", "chi tháng %s → %s" % (CHI[chi_thang], ten_v), noi)
    hop = CAN_HOP[v] if loai == "can" else CHI_HOP[v]
    noi = [TEN_TRU[i] for i in range(n) if (cans[i] == hop if loai == "can" else chis[i] == hop)]
    them("Thiên Đức hợp", "hợp của %s → %s" % (ten_v, CAN[hop] if loai == "can" else CHI[hop]), noi)
    v = NGUYET_DUC[chi_thang]
    them("Nguyệt Đức", "chi tháng %s → %s" % (CHI[chi_thang], CAN[v]), [TEN_TRU[i] for i in range(n) if cans[i] == v])
    h = CAN_HOP[v]
    them("Nguyệt Đức hợp", "hợp của %s → %s" % (CAN[v], CAN[h]), [TEN_TRU[i] for i in range(n) if cans[i] == h])
    ty = (chi_thang - 1) % 12
    them("Thiên Y", "chi tháng %s → %s" % (CHI[chi_thang], CHI[ty]), tim_chi([ty], bo=1))
    # theo trụ ngày
    ngay = (can_ngay, chi_ngay)
    for ten, tap in (("Khôi Cương", KHOI_CUONG), ("Âm Dương Sai Thác", AM_DUONG_SAI),
                     ("Thập Ác Đại Bại", THAP_AC), ("Cô Loan Sát", CO_LOAN)):
        if ngay in tap:
            kq.append((ten, "trụ ngày %s %s" % (CAN[can_ngay], CHI[chi_ngay]), ["Ngày"]))
    if THIEN_XA[mua(chi_thang)] == ngay:
        kq.append(("Thiên Xá", "trụ ngày %s %s sinh đúng mùa" % (CAN[can_ngay], CHI[chi_ngay]), ["Ngày"]))
    # Thiên La / Địa Võng
    if 10 in chis and 11 in chis:
        kq.append(("Thiên La (Tuất–Hợi)", "có cả Tuất và Hợi", tim_chi([10, 11])))
    if 4 in chis and 5 in chis:
        kq.append(("Địa Võng (Thìn–Tỵ)", "có cả Thìn và Tỵ", tim_chi([4, 5])))
    # gộp trùng (cùng tên, cùng trụ) khi xét từ hai gốc
    gop = {}
    for ten, cc, noi in kq:
        key = ten
        if key in gop:
            gop[key][0].append(cc)
            for x in noi:
                if x not in gop[key][1]:
                    gop[key][1].append(x)
        else:
            gop[key] = [[cc], list(noi)]
    return [(ten, "; ".join(v[0]), [t for t in TEN_TRU if t in v[1]]) for ten, v in gop.items()]


Y_NGHIA = {
    "Thiên Ất Quý Nhân": "quý nhân phù trợ, gặp nạn có người giúp",
    "Văn Xương": "thông minh, học hành, văn chương",
    "Thái Cực Quý Nhân": "thích nghiên cứu, huyền học, có phúc",
    "Lộc thần (Kiến Lộc)": "có lộc ăn, tự lập, gốc của nhật chủ",
    "Dương Nhận": "cương quyết, dễ nóng; đi cùng Thất Sát thì có uy",
    "Kim Dư": "được nâng đỡ, đời sống sung túc, phối ngẫu tốt",
    "Hồng Diễm": "duyên dáng, đa tình",
    "Quốc Ấn": "giữ ấn tín, hợp chức trách, quản lý",
    "Lưu Hà": "cần cẩn thận nước, máu, sinh nở (thần sát phụ)",
    "Dịch Mã": "đi lại, thay đổi, xa xứ",
    "Đào Hoa (Hàm Trì)": "duyên, sức hút; nhiều thì dễ vướng tình",
    "Hoa Cái": "nghệ thuật, tôn giáo, cô độc, thích suy tư",
    "Tướng Tinh": "có uy, khả năng lãnh đạo",
    "Kiếp Sát": "dễ hao tổn, tai bất ngờ; vượng thì mưu lược",
    "Vong Thần": "tâm cơ, dễ thị phi; được chế thì mưu trí",
    "Cô Thần": "cô độc (nặng với nam)",
    "Quả Tú": "cô quạnh (nặng với nữ)",
    "Hồng Loan": "hôn nhân, hỷ sự",
    "Thiên Hỷ": "hỷ sự, vui vẻ",
    "Thiên Đức": "phúc đức, giảm hung",
    "Thiên Đức hợp": "phúc đức (nhẹ hơn Thiên Đức)",
    "Nguyệt Đức": "phúc đức, hiền lành, giảm hung",
    "Nguyệt Đức hợp": "phúc đức (nhẹ hơn Nguyệt Đức)",
    "Thiên Y": "hợp nghề y, chăm sóc người",
    "Khôi Cương": "cương nghị, quyết đoán, thích quyền",
    "Âm Dương Sai Thác": "hôn nhân, gia đạo dễ trắc trở",
    "Thập Ác Đại Bại": "dễ hao tài, phải tự lực (tham khảo)",
    "Cô Loan Sát": "hôn nhân dễ lạnh, cô đơn (tham khảo)",
    "Thiên Xá": "được tha thứ, giải nạn",
    "Thiên La (Tuất–Hợi)": "dễ vướng mắc, nặng với nam",
    "Địa Võng (Thìn–Tỵ)": "dễ vướng mắc, nặng với nữ",
}


def in_bang(tru):
    rows = tinh(tru)
    print("THẦN SÁT BÁT TỰ (bảng phổ biến; các sách khác nhau ở vài sao – chỉ là yếu tố phụ, luận sau ngũ hành/thập thần)")
    print("| Thần sát | Căn cứ | Ở trụ | Ý nghĩa (tham khảo) |")
    print("|---|---|---|---|")
    for ten, cc, noi in rows:
        print("| %s | %s | %s | %s |" % (ten, cc, ", ".join(noi), Y_NGHIA.get(ten, "")))
    if not rows:
        print("| (không có) | | | |")
    print("(Quý nhân Bát tự theo 'Giáp Mậu Canh ngưu dương… Lục Tân phùng mã hổ'; khác Khôi/Việt trong Tử vi.)")
    print()
