# -*- coding: utf-8 -*-
"""hannam.py - Sao hạn năm theo tục Việt Nam (lệnh: nc.py hannam).

Một năm xem cho một người, tính theo TUỔI MỤ (năm xem − năm sinh âm lịch + 1):
  - Sao chiếu mệnh (Cửu diệu): tuổi mụ chia 9 lấy dư, nam và nữ hai thứ tự khác nhau.
  - Hạn (8 hạn): cộng hai chữ số của tuổi mụ được S; nam lấy THU_TU_HAN[(S+7) % 8], nữ lấy THU_TU_HAN[(5−S) % 8].
  - Tam tai (theo nhóm tam hợp của chi năm sinh), Kim lâu, Hoang ốc (dùng khi làm nhà, cưới hỏi).
  - Phạm Thái Tuế: chi năm xem so với chi năm sinh (trùng = năm tuổi, xung, hình, hại, phá).

Đối chiếu: khớp 71/71 dòng (nam và nữ) bảng sao hạn năm 2030 của ngaydep.com; danh sách tuổi gặp
Huỳnh Tuyền, Tam Kheo, Thiên Tinh… khớp bảng hoatieu.vn (nam Huỳnh Tuyền 18, 27, 36, 45, 54, 63, 72, 81, 89, 90, 98;
nữ 14, 23, 32, 41, 49, 50, 58…); ví dụ 48 tuổi (nam Thủy Diệu, nữ Mộc Đức) của báo Hà Tĩnh.

Đây là tục dân gian, tách riêng với Tử vi và Bát tự; không dùng làm kết luận chính.

Dùng:
  python3 tvbt/nc.py hannam --nam-sinh 1986 --gioi nam [--nam-xem 2026] [--so-nam 10]
  python3 tvbt/nc.py hannam --ngay 1986-07-22 --gioi nam          (ngày dương lịch, tự đổi ra năm âm)
"""
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

# tuổi mụ % 9 -> sao
SAO_NAM = {1: "La Hầu", 2: "Thổ Tú", 3: "Thủy Diệu", 4: "Thái Bạch", 5: "Thái Dương", 6: "Vân Hớn",
           7: "Kế Đô", 8: "Thái Âm", 0: "Mộc Đức"}
SAO_NU = {1: "Kế Đô", 2: "Vân Hớn", 3: "Mộc Đức", 4: "Thái Âm", 5: "Thổ Tú", 6: "La Hầu",
          7: "Thái Dương", 8: "Thái Bạch", 0: "Thủy Diệu"}
# cách xếp phổ biến trên lịch và báo Việt Nam; ngày âm lịch hằng tháng mà tục cúng sao hay dùng
TINH_SAO = {
    "Thái Dương": ("tốt", 27, "thuận cho công việc, danh tiếng; nam tốt hơn nữ"),
    "Thái Âm": ("tốt", 26, "thuận tiền bạc, gia đạo; nữ tốt hơn nam"),
    "Mộc Đức": ("tốt", 25, "êm ấm, có quý nhân, thuận việc nhà"),
    "Thổ Tú": ("trung bình, hơi xấu", 19, "dễ có chuyện thị phi, việc nhà vướng víu"),
    "Thủy Diệu": ("trung bình", 21, "có lộc nhưng cẩn thận lời nói, sông nước"),
    "Vân Hớn": ("trung bình, hơi xấu", 29, "dễ nóng nảy, tranh cãi, giấy tờ"),
    "La Hầu": ("xấu", 8, "dễ thị phi, giấy tờ, nam nặng hơn nữ"),
    "Kế Đô": ("xấu", 18, "dễ buồn phiền, hao tài, nữ nặng hơn nam"),
    "Thái Bạch": ("xấu", 15, "dễ hao tài, nên giữ tiền, tránh đầu tư liều"),
}
THU_TU_HAN = ["Huỳnh Tuyền", "Tam Kheo", "Ngũ Mộ", "Thiên Tinh", "Toán Tận", "Thiên La", "Địa Võng", "Diêm Vương"]
Y_HAN = {   # ý chính theo cách hiểu phổ biến; nói nhẹ nhàng, không dọa
    "Huỳnh Tuyền": "nên giữ sức khỏe, khám định kỳ, tránh việc liều",
    "Tam Kheo": "cẩn thận chân tay, mắt, đi lại",
    "Ngũ Mộ": "dễ hao tài, nên chi tiêu chặt",
    "Thiên Tinh": "dễ thị phi, kiện tụng; giữ giấy tờ rõ ràng",
    "Toán Tận": "dễ hao tài, cẩn thận cho vay, đầu tư",
    "Thiên La": "dễ phiền muộn, việc chậm",
    "Địa Võng": "dễ thị phi, vướng víu; tránh việc mờ ám",
    "Diêm Vương": "để ý sức khỏe người thân, người lớn tuổi trong nhà",
}


def sao(tuoi, gioi):
    return (SAO_NU if gioi == "nu" else SAO_NAM)[tuoi % 9]


def han(tuoi, gioi):
    s = sum(int(c) for c in str(tuoi))
    return THU_TU_HAN[(5 - s) % 8] if gioi == "nu" else THU_TU_HAN[(s + 7) % 8]


def kim_lau(tuoi):
    return {1: "Kim Lâu Thân (bản thân)", 3: "Kim Lâu Thê (vợ/chồng)", 6: "Kim Lâu Tử (con cái)",
            8: "Kim Lâu Lục Súc (tài sản, vật nuôi)"}.get(tuoi % 9)


def hoang_oc(tuoi):
    if tuoi < 10:
        return None
    ten = ["Nhất Cát (tốt)", "Nhì Nghi (tốt)", "Tam Địa Sát (xấu)", "Tứ Tấn Tài (tốt)", "Ngũ Thọ Tử (xấu)",
           "Lục Hoang Ốc (xấu)"]
    return ten[(tuoi // 10 - 1 + tuoi % 10) % 6]


def tam_tai(chi_sinh):
    """Ba chi năm Tam tai của người có chi năm sinh chi_sinh (Thân Tý Thìn -> Dần Mão Thìn …)."""
    nhom = {8: 0, 0: 0, 4: 0, 5: 1, 9: 1, 1: 1, 2: 2, 6: 2, 10: 2, 11: 3, 3: 3, 7: 3}[chi_sinh]
    return {0: (2, 3, 4), 1: (11, 0, 1), 2: (8, 9, 10), 3: (5, 6, 7)}[nhom]


HAI = {frozenset(x) for x in [(0, 7), (1, 6), (2, 5), (3, 4), (8, 11), (9, 10)]}
PHA = {frozenset(x) for x in [(0, 9), (1, 4), (2, 11), (3, 6), (5, 8), (7, 10)]}
HINH = {frozenset(x) for x in [(2, 5), (5, 8), (2, 8), (1, 10), (10, 7), (1, 7), (0, 3)]}
TU_HINH = {4, 6, 9, 11}


def thai_tue(chi_sinh, chi_nam):
    """Các kiểu phạm Thái Tuế của chi năm sinh với chi năm xem."""
    kq = []
    if chi_sinh == chi_nam:
        kq.append("trực Thái Tuế (năm tuổi)" + ("; tự hình" if chi_sinh in TU_HINH else ""))
    if (chi_sinh - chi_nam) % 12 == 6:
        kq.append("xung Thái Tuế")
    p = frozenset((chi_sinh, chi_nam))
    if p in HINH:
        kq.append("hình Thái Tuế")
    if p in HAI:
        kq.append("hại Thái Tuế")
    if p in PHA:
        kq.append("phá Thái Tuế")
    return kq


def mot_nam(nam_sinh_am, gioi, nam_xem):
    tuoi = nam_xem - nam_sinh_am + 1
    chi_sinh, chi_nam = (nam_sinh_am - 4) % 12, (nam_xem - 4) % 12
    s = sao(tuoi, gioi) if tuoi >= 1 else None
    tt = tam_tai(chi_sinh)
    return {
        "nam": nam_xem, "can_chi": "%s %s" % (CAN[(nam_xem - 4) % 10], CHI[chi_nam]), "tuoi": tuoi,
        "sao": s, "tinh_sao": TINH_SAO.get(s), "han": han(tuoi, gioi) if tuoi >= 10 else None,
        "tam_tai": chi_nam in tt, "tam_tai_nam": [CHI[c] for c in tt],
        "tam_tai_thu": (tt.index(chi_nam) + 1) if chi_nam in tt else 0,
        "kim_lau": kim_lau(tuoi) if tuoi >= 1 else None, "hoang_oc": hoang_oc(tuoi),
        "thai_tue": thai_tue(chi_sinh, chi_nam),
    }


def nam_sinh_am_tu_ngay(ngay, am=False, nhuan=False):
    import tvbt as B
    y, m, d = [int(x) for x in ngay.split("-")]
    if am:
        return y
    _, _, ya, _ = B.duong_sang_am(dt.date(y, m, d), 7)
    return ya


def in_han_nam(nam_sinh_am, gioi, nam_xem, so_nam=1):
    can_chi_sinh = "%s %s" % (CAN[(nam_sinh_am - 4) % 10], CHI[(nam_sinh_am - 4) % 12])
    print("SAO HẠN NĂM (tục dân gian Việt Nam, tính theo tuổi mụ) – %s, sinh năm âm lịch %d (%s)" % (
        "nữ" if gioi == "nu" else "nam", nam_sinh_am, can_chi_sinh))
    print("Tam tai của tuổi %s rơi vào các năm %s." % (CHI[(nam_sinh_am - 4) % 12],
                                                       ", ".join(CHI[c] for c in tam_tai((nam_sinh_am - 4) % 12))))
    print()
    print("| Năm | Tuổi mụ | Sao chiếu mệnh | Hạn | Tam tai | Phạm Thái Tuế | Kim lâu | Hoang ốc |")
    print("|---|---|---|---|---|---|---|---|")
    ds = []
    for n in range(nam_xem, nam_xem + max(1, so_nam)):
        r = mot_nam(nam_sinh_am, gioi, n)
        ds.append(r)
        if r["tuoi"] < 1:
            continue
        sao_txt = "%s (%s)" % (r["sao"], r["tinh_sao"][0]) if r["sao"] else "–"
        print("| %d %s | %d | %s | %s | %s | %s | %s | %s |" % (
            n, r["can_chi"], r["tuoi"], sao_txt, r["han"] or "– (dưới 10 tuổi)",
            ("năm thứ %d" % r["tam_tai_thu"]) if r["tam_tai"] else "không",
            "; ".join(r["thai_tue"]) or "không", r["kim_lau"] or "không", r["hoang_oc"] or "–"))
    r = ds[0]
    if r["tuoi"] >= 1:
        print()
        print("NĂM %d (%s), %d tuổi mụ:" % (r["nam"], r["can_chi"], r["tuoi"]))
        if r["tuoi"] < 10:
            print("- Dưới 10 tuổi: nhiều nơi chưa xét sao hạn; sao dưới đây chỉ để biết.")
        if r["sao"]:
            t, ngay_cung, y = r["tinh_sao"]
            print("- Sao %s – %s: %s. Tục cúng sao thường làm vào ngày %d âm lịch hằng tháng (không bắt buộc)." % (
                r["sao"], t, y, ngay_cung))
        if r["han"]:
            print("- Hạn %s: %s." % (r["han"], Y_HAN[r["han"]]))
            if r["tuoi"] == 10 and gioi != "nu":
                print("  (Một số bảng chỉ xét hạn từ 11 tuổi.)")
        if r["tam_tai"]:
            print("- Năm Tam tai thứ %d/3 (%s): tục kiêng khởi công lớn, cưới hỏi, làm nhà; nên làm việc chắc chắn." % (
                r["tam_tai_thu"], ", ".join(r["tam_tai_nam"])))
        if r["thai_tue"]:
            print("- Phạm Thái Tuế: %s – năm dễ có thay đổi, nên thận trọng việc lớn." % ", ".join(r["thai_tue"]))
        lam_nha = [x for x in (r["kim_lau"], r["hoang_oc"] if r["hoang_oc"] and "xấu" in r["hoang_oc"] else None,
                               "Tam tai" if r["tam_tai"] else None) if x]
        if r["tuoi"] < 18:
            pass
        elif lam_nha:
            print("- Làm nhà/cưới hỏi năm này phạm: %s (tục thường mượn tuổi người khác để động thổ)." % ", ".join(lam_nha))
        else:
            print("- Làm nhà/cưới hỏi năm này không phạm Kim lâu, Hoang ốc xấu, Tam tai.")
    print()
    print("(Sao hạn, Tam tai, Kim lâu, Hoang ốc là tục dân gian, các nơi tính hơi khác nhau; chỉ để tham khảo, "
          "không thay cho Tử vi, Bát tự. Không cần làm lễ tốn kém; nếu muốn cúng thì làm giản dị, tâm thành.)")
    return ds


def them_lenh(sub):
    p = sub.add_parser("hannam", help="sao hạn năm (Cửu diệu), 8 hạn, Tam tai, Kim lâu, Hoang ốc, phạm Thái Tuế")
    p.add_argument("--nam-sinh", type=int, help="năm sinh ÂM LỊCH (ví dụ 1986)")
    p.add_argument("--ngay", help="hoặc ngày sinh YYYY-MM-DD (dương lịch; thêm --am nếu là âm lịch)")
    p.add_argument("--am", action="store_true")
    p.add_argument("--nhuan", action="store_true")
    p.add_argument("--gioi", choices=["nam", "nu"], required=True)
    p.add_argument("--nam-xem", type=int, help="năm xem (mặc định năm nay)")
    p.add_argument("--so-nam", type=int, default=1, help="số năm liên tiếp (bảng)")
    p.set_defaults(_chay=chay)


def chay(a):
    if a.nam_sinh:
        ns = a.nam_sinh
    elif a.ngay:
        ns = nam_sinh_am_tu_ngay(a.ngay, a.am, a.nhuan)
    else:
        raise SystemExit("LỖI: cần --nam-sinh (năm âm lịch) hoặc --ngay.")
    nam_xem = a.nam_xem or (dt.datetime.utcnow() + dt.timedelta(hours=7)).year
    if not (1800 <= ns <= 2200 and 1800 <= nam_xem <= 2200 and 1 <= a.so_nam <= 100):
        raise SystemExit("LỖI: năm ngoài khoảng 1800–2200 hoặc số năm ngoài 1–100.")
    in_han_nam(ns, a.gioi, nam_xem, a.so_nam)


# bảng 2030 của ngaydep.com: năm sinh, sao nam, hạn nam, sao nữ, hạn nữ (mã viết tắt)
_BANG_2030 = ("1960 TA DV TB TL|1972 TD TL TT DV|1984 TT NM VH NM|1996 TA DV TB TL|2008 TD TTn TT HT|1949 LH TK KD TTi|"
              "1961 KD DVo TD DVo|1973 TB TTn TA HT|1985 LH TK KD TTi|1997 KD DVo TD DVo|2009 TB TTi TA TK|1950 MD HT TDi TTn|"
              "1962 VH DVo LH DVo|1974 TDi TTi MD TK|1986 MD HT TDi TTn|1998 VH TL LH DV|2010 TDi NM MD NM|1951 TA DV TB TL|"
              "1963 TD TL TT DV|1975 TT NM VH NM|1987 TA DV TB TL|1999 TD TTn TT HT|2011 TT TK VH TTi|1952 KD DV TD TL|"
              "1964 TB TTn TA HT|1976 LH TK KD TTi|1988 KD DVo TD DVo|2000 TB TTi TA TK|2012 LH TK KD TTi|1953 VH DVo LH DVo|"
              "1965 TDi TTi MD TK|1977 MD HT TDi TTn|1989 VH TL LH DV|2001 TDi NM MD NM|2013 MD HT TDi TTn|1954 TD TL TT DV|"
              "1966 TT NM VH NM|1978 TA DV TB TL|1990 TD TTn TT HT|2002 TT NM VH NM|2014 TA DV TB TL|1955 TB TTn TA HT|"
              "1967 LH TK KD TTi|1979 KD DVo TD DVo|1991 TB TTi TA TK|2003 LH TK KD TTi|2015 KD DVo TD DVo|1956 TDi TTi MD TK|"
              "1968 MD HT TDi TTn|1980 VH TL LH DV|1992 TDi TTi MD TK|2004 MD HT TDi TTn|2016 VH TL LH DV|1957 TT NM VH NM|"
              "1969 TA DV TB TL|1981 TD TTn TT HT|1993 TT NM VH NM|2005 TA DV TB TL|2017 TD TTn TT HT|1958 LH TK KD TTi|"
              "1970 KD DVo TD DVo|1982 TB TTn TA HT|1994 LH TK KD TTi|2006 KD DVo TD DVo|2018 TB TTi TA TK|1959 MD HT TDi TTn|"
              "1971 VH TL LH DV|1983 TDi TTi MD TK|1995 MD HT TDi TTn|2007 VH TL LH DV|2019 TDi NM MD NM")
_MA = {"LH": "La Hầu", "TT": "Thổ Tú", "TDi": "Thủy Diệu", "TB": "Thái Bạch", "TD": "Thái Dương", "VH": "Vân Hớn",
       "KD": "Kế Đô", "TA": "Thái Âm", "MD": "Mộc Đức", "HT": "Huỳnh Tuyền", "TK": "Tam Kheo", "NM": "Ngũ Mộ",
       "TTi": "Thiên Tinh", "TTn": "Toán Tận", "TL": "Thiên La", "DVo": "Địa Võng", "DV": "Diêm Vương"}


def tu_kiem():
    loi = []
    for dong in _BANG_2030.split("|"):
        y, sn, hn, su, hu = dong.split()
        t = 2030 - int(y) + 1
        got = (sao(t, "nam"), han(t, "nam"), sao(t, "nu"), han(t, "nu"))
        if got != (_MA[sn], _MA[hn], _MA[su], _MA[hu]):
            loi.append("bảng 2030 năm sinh %s: %s" % (y, got))
    if [t for t in range(10, 100) if han(t, "nam") == "Huỳnh Tuyền" and t > 10] != [18, 27, 36, 45, 54, 63, 72, 81, 89, 90, 98]:
        loi.append("tuổi Huỳnh Tuyền nam")
    if [t for t in range(10, 100) if han(t, "nu") == "Huỳnh Tuyền"] != [14, 23, 32, 41, 49, 50, 58, 67, 76, 85, 94]:
        loi.append("tuổi Huỳnh Tuyền nữ")
    if [t for t in range(10, 99) if han(t, "nam") == "Tam Kheo"] != [11, 19, 20, 28, 37, 46, 55, 64, 73, 82, 91]:
        loi.append("tuổi Tam Kheo nam")
    if sao(48, "nam") != "Thủy Diệu" or sao(48, "nu") != "Mộc Đức":
        loi.append("ví dụ 48 tuổi")
    # 1986 Bính Dần năm 2026 (41 tuổi): Tam tai Thân Dậu Tuất -> 2026 Ngọ không; 2028 Thân là Tam tai năm 1
    r = mot_nam(1986, "nam", 2026)
    if r["tuoi"] != 41 or r["tam_tai"] or not mot_nam(1986, "nam", 2028)["tam_tai"]:
        loi.append("Tam tai tuổi Dần")
    if mot_nam(1986, "nam", 2028)["thai_tue"] != ["xung Thái Tuế", "hình Thái Tuế"] or "trực" not in mot_nam(1986, "nam", 2034)["thai_tue"][0]:
        loi.append("Thái Tuế tuổi Dần")
    return loi
