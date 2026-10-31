# -*- coding: utf-8 -*-
"""Chọn ngày giờ tốt theo lịch Việt Nam: Hoàng/Hắc đạo, 12 Trực, Nhị thập bát tú, Tam Nương, Nguyệt Kỵ,
Dương Công kỵ nhật, xung tuổi, giờ hoàng đạo; Kim Lâu, Hoang Ốc, Tam Tai theo tuổi mụ."""
import datetime as dt

from lich_vn import jd_from_date, solar_to_lunar
from lunar_python import Solar

CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
ZHI_HAN = "子丑寅卯辰巳午未申酉戌亥"
THAN12 = ["Thanh Long", "Minh Đường", "Thiên Hình", "Chu Tước", "Kim Quỹ", "Kim Đường (Bảo Quang)",
          "Bạch Hổ", "Ngọc Đường", "Thiên Lao", "Huyền Vũ", "Tư Mệnh", "Câu Trận"]
HOANG_DAO = {0, 1, 4, 5, 7, 10}
# Thanh Long khởi tại chi nào, theo chi tháng (hoặc chi ngày khi tính giờ)
KHOI_TL = {2: 0, 8: 0, 3: 2, 9: 2, 4: 4, 10: 4, 5: 6, 11: 6, 0: 8, 6: 8, 1: 10, 7: 10}
TRUC = ["Kiến", "Trừ", "Mãn", "Bình", "Định", "Chấp", "Phá", "Nguy", "Thành", "Thu", "Khai", "Bế"]
TU28 = ["Giác", "Cang", "Đê", "Phòng", "Tâm", "Vĩ", "Cơ", "Đẩu", "Ngưu", "Nữ", "Hư", "Nguy",
        "Thất", "Bích", "Khuê", "Lâu", "Vị", "Mão", "Tất", "Chủy", "Sâm", "Tỉnh", "Quỷ", "Liễu",
        "Tinh", "Trương", "Dực", "Chẩn"]
TU_CAT = {"Giác", "Phòng", "Vĩ", "Cơ", "Đẩu", "Thất", "Bích", "Lâu", "Vị", "Tất", "Sâm", "Tỉnh", "Trương", "Chẩn"}
_TU_GOC = 2461344 - 15          # JD 30/10/2026 là sao Lâu (chỉ số 15) – đã đối chiếu lunar-python
TAM_NUONG = {3, 7, 13, 18, 22, 27}
NGUYET_KY = {5, 14, 23}
DUONG_CONG = {(13, 1), (11, 2), (9, 3), (7, 4), (5, 5), (3, 6), (8, 7), (29, 7), (27, 8), (25, 9),
              (23, 10), (21, 11), (19, 12)}
XUNG = lambda a, b: (a - b) % 12 == 6
HANH_CAN = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]          # Mộc Hỏa Thổ Kim Thủy
KHAC = lambda a, b: (b - a) % 5 == 2               # hành a khắc hành b
VIEC = {
    "chung": ("Việc chung", {"Trừ", "Định", "Chấp", "Thành", "Khai"}, {"Phá", "Nguy", "Bế"}),
    "cuoi": ("Cưới hỏi", {"Định", "Thành", "Khai"}, {"Phá", "Nguy", "Bế"}),
    "dongtho": ("Động thổ, xây sửa", {"Chấp", "Thành", "Định", "Mãn", "Bình"}, {"Kiến", "Phá", "Bế", "Khai"}),
    "khaitruong": ("Khai trương, ký kết", {"Khai", "Mãn", "Thành", "Kiến"}, {"Phá", "Nguy", "Bế"}),
    "xuathanh": ("Xuất hành, đi xa", {"Kiến", "Khai", "Thành"}, {"Phá", "Nguy", "Bế", "Chấp"}),
    "nhaptrach": ("Nhập trạch, chuyển nhà", {"Thành", "Khai", "Định", "Mãn"}, {"Phá", "Nguy", "Bế"}),
}


def can_chi_ngay(d):
    i = (jd_from_date(d.day, d.month, d.year) + 49) % 60
    return i % 10, i % 12


def chi_thang_tiet(d):
    return ZHI_HAN.index(Solar.fromYmd(d.year, d.month, d.day).getLunar().getMonthZhi())


def than_truc_nhat(chi_goc, chi):
    return (chi - KHOI_TL[chi_goc]) % 12


def tu28(d):
    return TU28[(jd_from_date(d.day, d.month, d.year) - _TU_GOC) % 28]


def gio_hoang_dao(chi_ngay):
    return [z for z in range(12) if than_truc_nhat(chi_ngay, z) in HOANG_DAO]


def kim_lau(tuoi):
    r = tuoi % 9
    return {1: "Kim Lâu Thân (hại bản thân)", 3: "Kim Lâu Thê (hại vợ/chồng)",
            6: "Kim Lâu Tử (hại con)", 8: "Kim Lâu Lục Súc (hại tài sản, vật nuôi)"}.get(r)


def hoang_oc(tuoi):
    ten = ["Nhất Cát (tốt)", "Nhì Nghi (tốt)", "Tam Địa Sát (xấu)", "Tứ Tấn Tài (tốt)",
           "Ngũ Thọ Tử (xấu)", "Lục Hoang Ốc (xấu)"]
    if tuoi < 10:
        return None
    return ten[(tuoi // 10 - 1 + tuoi % 10) % 6]


def tam_tai(chi_sinh):
    return {0: (2, 3, 4), 1: (11, 0, 1), 2: (8, 9, 10), 3: (5, 6, 7)}[
        {8: 0, 0: 0, 4: 0, 5: 1, 9: 1, 1: 1, 2: 2, 6: 2, 10: 2, 11: 3, 3: 3, 7: 3}[chi_sinh]]


def xet_ngay(d, tuoi_list, viec, theo_tiet=False):
    """tuoi_list: list (tên, can năm sinh, chi năm sinh)."""
    ten_viec, tot, xau = VIEC[viec]
    al = solar_to_lunar(d.day, d.month, d.year, 7)
    cn, zn = can_chi_ngay(d)
    zt = chi_thang_tiet(d)
    za = (al[1] + 1) % 12                       # chi tháng âm lịch: tháng 1 = Dần
    zh = zt if theo_tiet else za
    than = than_truc_nhat(zh, zn)
    than_kia = than_truc_nhat(za if theo_tiet else zt, zn)
    truc = TRUC[(zn - zt) % 12]
    tu = tu28(d)
    diem, ghi = 0, []
    if than in HOANG_DAO:
        diem += 2
    else:
        diem -= 1
    if (than in HOANG_DAO) != (than_kia in HOANG_DAO):
        ghi.append("tính theo tháng %s thì là %s" % ("âm" if theo_tiet else "tiết khí", THAN12[than_kia]))
    if truc in tot:
        diem += 1
    elif truc in xau:
        diem -= 2
    diem += 1 if tu in TU_CAT else -1
    if al[0] in TAM_NUONG:
        diem -= 2
        ghi.append("Tam Nương")
    if al[0] in NGUYET_KY:
        diem -= 2
        ghi.append("Nguyệt Kỵ")
    if (al[0], al[1]) in DUONG_CONG and not al[3]:
        diem -= 3
        ghi.append("Dương Công kỵ nhật")
    for ten, c, z in tuoi_list:
        if XUNG(zn, z):
            if KHAC(HANH_CAN[cn], HANH_CAN[c]) or KHAC(HANH_CAN[c], HANH_CAN[cn]):
                diem -= 4
                ghi.append("THIÊN KHẮC ĐỊA XUNG tuổi %s" % ten)
            else:
                diem -= 3
                ghi.append("xung tuổi %s" % ten)
    return dict(ngay=d, am=al, can=cn, chi=zn, than=THAN12[than], hd=than in HOANG_DAO, truc=truc, tu=tu,
                diem=diem, ghi=ghi, gio=gio_hoang_dao(zn))


def in_chon_ngay(tu, den, nguoi, viec, theo_tiet=False, top=5):
    """nguoi: list (tên, năm âm lịch sinh)."""
    if (den - tu).days > 92:
        raise SystemExit("LỖI: khoảng ngày tối đa 93 ngày – chia nhỏ ra.")
    if den < tu:
        raise SystemExit("LỖI: --den phải sau --tu.")
    tuoi_list = [(ten, (y - 4) % 10, (y - 4) % 12) for ten, y in nguoi]
    ten_viec = VIEC[viec][0]
    print("CHỌN NGÀY: %s, từ %s đến %s" % (ten_viec, tu.strftime("%d/%m/%Y"), den.strftime("%d/%m/%Y")))
    print("- Hoàng/Hắc đạo theo %s; 12 Trực theo tiết khí; Trực tốt cho việc này: %s; Trực kỵ: %s" % (
        "tháng tiết khí" if theo_tiet else "tháng âm lịch (cách phổ biến ở lịch Việt Nam)",
        ", ".join(sorted(VIEC[viec][1])), ", ".join(sorted(VIEC[viec][2]))))
    for ten, y in nguoi:
        c, z = (y - 4) % 10, (y - 4) % 12
        dong = []
        for nam in sorted({tu.year, den.year}):
            tuoi = nam - y + 1
            tt = tam_tai(z)
            nz = (nam - 4) % 12
            dong.append("năm %d (%s %s, tuổi mụ %d): %s; Hoang Ốc: %s; %s" % (
                nam, CAN[(nam - 4) % 10], CHI[nz], tuoi, kim_lau(tuoi) or "không phạm Kim Lâu",
                hoang_oc(tuoi) or "-", "PHẠM TAM TAI" if nz in tt else "không Tam Tai"))
        print("- %s (sinh năm %s %s %d; Tam Tai các năm %s): %s" % (
            ten, CAN[c], CHI[z], y, "/".join(CHI[x] for x in tam_tai(z)), " | ".join(dong)))
    print("  (Kim Lâu xét cho cưới hỏi – thường tính tuổi cô dâu – và làm nhà; Hoang Ốc, Tam Tai xét khi làm nhà, "
          "động thổ, việc lớn. Năm tính theo âm lịch, đổi từ Tết.)")
    print()
    rows = []
    d = tu
    while d <= den:
        rows.append(xet_ngay(d, tuoi_list, viec, theo_tiet))
        d += dt.timedelta(days=1)
    print("| Dương lịch | Âm lịch | Ngày | Thần trực nhật | Trực | Sao (28 tú) | Ghi chú | Điểm |")
    print("|---|---|---|---|---|---|---|---|")
    thu = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
    for r in rows:
        al = r["am"]
        print("| %s %s | %d/%d%s | %s %s | %s %s | %s | %s (%s) | %s | %+d |" % (
            thu[r["ngay"].weekday()], r["ngay"].strftime("%d/%m/%Y"), al[0], al[1], " nhuận" if al[3] else "",
            CAN[r["can"]], CHI[r["chi"]], r["than"], "(Hoàng đạo)" if r["hd"] else "(Hắc đạo)", r["truc"],
            r["tu"], "cát" if r["tu"] in TU_CAT else "hung", "; ".join(r["ghi"]), r["diem"]))
    print()
    tot = sorted([r for r in rows if r["diem"] > 0 and not any(
        k in g for g in r["ghi"] for k in ("xung", "XUNG", "Dương Công", "Tam Nương", "Nguyệt Kỵ"))],
                 key=lambda r: (-r["diem"], r["ngay"]))[:top]
    print("NGÀY NỔI BẬT (điểm cao nhất; đã loại ngày xung tuổi, Dương Công, Tam Nương, Nguyệt Kỵ) và GIỜ HOÀNG ĐẠO:")
    for r in tot:
        print("- %s (%d/%d âm, %s %s): giờ hoàng đạo %s" % (
            r["ngay"].strftime("%d/%m/%Y"), r["am"][0], r["am"][1], CAN[r["can"]], CHI[r["chi"]],
            ", ".join("%s (%02d-%02dh)" % (CHI[z], (2 * z - 1) % 24, (2 * z + 1) % 24) for z in r["gio"])))
    if not tot:
        print("- Không có ngày đạt điểm dương trong khoảng này – nới khoảng ngày hoặc xem xét lại tiêu chí.")
    print("(Điểm là quy ước gộp: Hoàng đạo +2/Hắc đạo −1; Trực hợp việc +1/kỵ −2; sao cát +1/hung −1; "
          "Tam Nương, Nguyệt Kỵ −2; Dương Công −3; xung tuổi −3, thiên khắc địa xung −4. Luận phải nhìn cột chi tiết.)")
    print()
