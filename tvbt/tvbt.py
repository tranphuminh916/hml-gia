# -*- coding: utf-8 -*-
"""tvbt.py - Lập lá số Bát tự, Tử vi, Phong thủy (tiếng Việt).
Cần: pip install lunar-python (phần Tử vi dùng tuvi_vn.py đi kèm)
Cách dùng: python3 tvbt.py --help
"""
import argparse
import datetime as dt
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lich_vn import solar_to_lunar, lunar_to_solar  # noqa: E402

from lunar_python import Solar, Lunar  # noqa: E402
from lunar_python.util import LunarUtil  # noqa: E402

# ---------------------------------------------------------------- Từ điển Hán -> Việt
CAN = dict(zip("甲乙丙丁戊己庚辛壬癸",
               ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]))
CHI = dict(zip("子丑寅卯辰巳午未申酉戌亥",
               ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]))
HANH = {"金": "Kim", "木": "Mộc", "水": "Thủy", "火": "Hỏa", "土": "Thổ"}
THAP_THAN = {"比肩": "Tỷ Kiên", "劫财": "Kiếp Tài", "食神": "Thực Thần", "伤官": "Thương Quan",
             "偏财": "Thiên Tài", "正财": "Chính Tài", "七杀": "Thất Sát", "正官": "Chính Quan",
             "偏印": "Thiên Ấn (Kiêu)", "正印": "Chính Ấn", "日主": "Nhật Chủ"}
TRUONG_SINH = {"长生": "Trường Sinh", "沐浴": "Mộc Dục", "冠带": "Quan Đới", "临官": "Lâm Quan",
               "帝旺": "Đế Vượng", "衰": "Suy", "病": "Bệnh", "死": "Tử", "墓": "Mộ",
               "绝": "Tuyệt", "胎": "Thai", "养": "Dưỡng"}
NAP_AM = {"海中金": "Hải Trung Kim", "炉中火": "Lư Trung Hỏa", "大林木": "Đại Lâm Mộc",
          "路旁土": "Lộ Bàng Thổ", "剑锋金": "Kiếm Phong Kim", "山头火": "Sơn Đầu Hỏa",
          "涧下水": "Giản Hạ Thủy", "城头土": "Thành Đầu Thổ", "白蜡金": "Bạch Lạp Kim",
          "杨柳木": "Dương Liễu Mộc", "泉中水": "Tuyền Trung Thủy", "屋上土": "Ốc Thượng Thổ",
          "霹雳火": "Tích Lịch Hỏa", "松柏木": "Tùng Bách Mộc", "长流水": "Trường Lưu Thủy",
          "沙中金": "Sa Trung Kim", "山下火": "Sơn Hạ Hỏa", "平地木": "Bình Địa Mộc",
          "壁上土": "Bích Thượng Thổ", "金箔金": "Kim Bạch Kim", "覆灯火": "Phú Đăng Hỏa",
          "天河水": "Thiên Hà Thủy", "大驿土": "Đại Dịch Thổ (Đại Trạch Thổ)", "钗钏金": "Thoa Xuyến Kim",
          "桑柘木": "Tang Đố Mộc", "大溪水": "Đại Khê Thủy", "沙中土": "Sa Trung Thổ",
          "天上火": "Thiên Thượng Hỏa", "石榴木": "Thạch Lựu Mộc", "大海水": "Đại Hải Thủy"}
TRUONG_SINH_12 = ["长生", "沐浴", "冠带", "临官", "帝旺", "衰", "病", "死", "墓", "绝", "胎", "养"]
TRUONG_SINH_GOC = {"甲": "亥", "丙": "寅", "戊": "寅", "庚": "巳", "壬": "申",
                   "乙": "午", "丁": "酉", "己": "酉", "辛": "子", "癸": "卯"}
CAN_HANH = dict(zip("甲乙丙丁戊己庚辛壬癸", "木木火火土土金金水水"))
CHI_HANH = dict(zip("子丑寅卯辰巳午未申酉戌亥", "水土木木土火火土金金土水"))
GAN_LIST = "甲乙丙丁戊己庚辛壬癸"
ZHI_LIST = "子丑寅卯辰巳午未申酉戌亥"
CHI_VN = [CHI[c] for c in ZHI_LIST]
CAN_VN = [CAN[c] for c in GAN_LIST]
_CJK = re.compile(r"[一-鿿]")


def vn(s):
    """Dịch một chuỗi Hán (can chi / thập thần / nạp âm / trường sinh) sang tiếng Việt."""
    if s is None or s == "":
        return ""
    for d in (THAP_THAN, TRUONG_SINH, NAP_AM):
        if s in d:
            return d[s]
    out = []
    for ch in s:
        out.append(CAN.get(ch) or CHI.get(ch) or HANH.get(ch) or ch)
    r = " ".join(out) if all(c in CAN or c in CHI or c in HANH for c in s) else "".join(out)
    if _CJK.search(r):
        raise ValueError("Chưa dịch được: " + s)
    return r


# ---------------------------------------------------------------- Quan hệ can chi (hợp, xung, hình, hại)
_H5 = ["Mộc", "Hỏa", "Thổ", "Kim", "Thủy"]
_LUC_HOP = {frozenset(p): h for p, h in (((0, 1), "Thổ"), ((2, 11), "Mộc"), ((3, 10), "Hỏa"), ((4, 9), "Kim"),
                                         ((5, 8), "Thủy"), ((6, 7), "Hỏa/Thổ"))}
_HAI = {frozenset(p) for p in ((0, 7), (1, 6), (2, 5), (3, 4), (8, 11), (9, 10))}
_HINH = {(2, 5), (5, 8), (8, 2), (1, 10), (10, 7), (7, 1), (0, 3), (3, 0)}   # a hình b (Dần→Tỵ→Thân, Sửu→Tuất→Mùi, Tý↔Mão)
_TU_HINH = {4, 6, 9, 11}
_TAM_HOP = [((8, 0, 4), "Thủy"), ((5, 9, 1), "Kim"), ((2, 6, 10), "Hỏa"), ((11, 3, 7), "Mộc")]
_TAM_HOI = [((2, 3, 4), "Mộc"), ((5, 6, 7), "Hỏa"), ((8, 9, 10), "Kim"), ((11, 0, 1), "Thủy")]
_CAN_HOP = {frozenset((i, i + 5)): _H5[(i + 2) % 5] for i in range(5)}   # Giáp Kỷ Thổ, Ất Canh Kim, Bính Tân Thủy...
_CAN_XUNG = {frozenset((i, i + 6)) for i in range(4)}                   # Giáp Canh, Ất Tân, Bính Nhâm, Đinh Quý


def qh_chi(a, b):
    """Các quan hệ giữa hai địa chi (chỉ số 0..11)."""
    kq = []
    if a == b:
        if a in _TU_HINH:
            kq.append("tự hình")
        return kq
    if frozenset((a, b)) in _LUC_HOP:
        kq.append("lục hợp (%s)" % _LUC_HOP[frozenset((a, b))])
    if (a - b) % 12 == 6:
        kq.append("xung")
    if (a, b) in _HINH or (b, a) in _HINH:
        kq.append("hình")
    if frozenset((a, b)) in _HAI:
        kq.append("hại")
    for nhom, h in _TAM_HOP:
        if a in nhom and b in nhom and (nhom[1] in (a, b)):
            kq.append("bán hợp %s" % h)
    return kq


def qh_can(a, b):
    kq = []
    if frozenset((a, b)) in _CAN_HOP:
        kq.append("hợp (%s)" % _CAN_HOP[frozenset((a, b))])
    if frozenset((a, b)) in _CAN_XUNG:
        kq.append("xung")
    return kq


def quan_he_moi(tru_ds, can_moi, chi_moi, them=()):
    """Quan hệ của một can chi mới (vận/năm/tháng) với các trụ.
    tru_ds, them: list (nhãn, can, chi); 'them' là các can chi đang chồng thêm (đại vận, lưu niên)."""
    kq = []
    for nhan, c, z in list(tru_ds) + list(them):
        for r in qh_can(can_moi, c):
            kq.append("%s %s %s (%s)" % (CAN_VN[can_moi], r, CAN_VN[c], nhan))
        for r in qh_chi(chi_moi, z):
            kq.append("%s %s %s (%s)" % (CHI_VN[chi_moi], r, CHI_VN[z], nhan))
    co = {z for _, _, z in list(tru_ds) + list(them)}
    for nhom, h in _TAM_HOP + _TAM_HOI:
        if chi_moi in nhom and all(x in co or x == chi_moi for x in nhom) and \
                len([x for x in nhom if x != chi_moi]) == 2:
            kq.append("đủ tam %s %s (%s)" % ("hợp" if (nhom, h) in _TAM_HOP else "hội",
                                             " ".join(CHI_VN[x] for x in nhom), h))
    return kq


def quan_he_noi_bo(tru_ds):
    """Quan hệ giữa các trụ với nhau (tứ trụ)."""
    kq = []
    for i in range(len(tru_ds)):
        for j in range(i + 1, len(tru_ds)):
            n1, c1, z1 = tru_ds[i]
            n2, c2, z2 = tru_ds[j]
            for r in qh_can(c1, c2):
                kq.append("%s (%s) %s %s (%s)" % (CAN_VN[c1], n1, r, CAN_VN[c2], n2))
            for r in qh_chi(z1, z2):
                kq.append("%s (%s) %s %s (%s)" % (CHI_VN[z1], n1, r, CHI_VN[z2], n2))
    co = {z for _, _, z in tru_ds}
    for nhom, h in _TAM_HOP + _TAM_HOI:
        if all(x in co for x in nhom):
            kq.append("đủ tam %s %s (%s)" % ("hợp" if (nhom, h) in _TAM_HOP else "hội",
                                             " ".join(CHI_VN[x] for x in nhom), h))
    return kq


# ---------------------------------------------------------------- Nơi sinh (kinh độ)
KINH_DO = {
    "ha noi": 105.85, "hai phong": 106.68, "ha long": 107.08, "quang ninh": 107.08,
    "nam dinh": 106.17, "thai binh": 106.34, "hai duong": 106.33, "bac ninh": 106.07,
    "thai nguyen": 105.84, "vinh phuc": 105.60, "phu tho": 105.40, "viet tri": 105.40,
    "thanh hoa": 105.78, "nghe an": 105.69, "vinh": 105.69, "ha tinh": 105.90,
    "lang son": 106.76, "lao cai": 103.97, "dien bien": 103.02, "son la": 103.91,
    "quang binh": 106.60, "dong hoi": 106.60, "quang tri": 107.10, "hue": 107.59,
    "da nang": 108.22, "quang nam": 108.33, "hoi an": 108.33, "quang ngai": 108.80,
    "quy nhon": 109.22, "binh dinh": 109.22, "tuy hoa": 109.32, "phu yen": 109.32,
    "nha trang": 109.19, "khanh hoa": 109.19, "phan rang": 108.99, "ninh thuan": 108.99,
    "phan thiet": 108.10, "binh thuan": 108.10, "kon tum": 108.00, "pleiku": 108.00,
    "gia lai": 108.00, "buon ma thuot": 108.05, "dak lak": 108.05, "da lat": 108.44,
    "lam dong": 108.44, "tp hcm": 106.70, "ho chi minh": 106.70, "sai gon": 106.70,
    "bien hoa": 106.82, "dong nai": 106.82, "thu dau mot": 106.65, "binh duong": 106.65,
    "vung tau": 107.08, "tay ninh": 106.10, "long an": 106.41, "tan an": 106.41,
    "my tho": 106.36, "tien giang": 106.36, "ben tre": 106.38, "vinh long": 105.97,
    "tra vinh": 106.34, "can tho": 105.78, "soc trang": 105.97, "long xuyen": 105.44,
    "an giang": 105.44, "chau doc": 105.12, "rach gia": 105.08, "kien giang": 105.08,
    "phu quoc": 103.97, "bac lieu": 105.72, "ca mau": 105.15, "cao lanh": 105.63,
    "dong thap": 105.63, "ninh binh": 105.97, "ha nam": 105.91, "phu ly": 105.91,
    "hung yen": 106.05, "hoa binh": 105.34, "bac giang": 106.20, "tuyen quang": 105.22,
    "yen bai": 104.87, "ha giang": 104.98, "cao bang": 106.26, "bac kan": 105.83,
    "lai chau": 103.46, "son tay": 105.50, "vinh linh": 107.00, "dong ha": 107.10,
    "ba ria": 107.17, "dong xoai": 106.90, "binh phuoc": 106.90, "go cong": 106.66,
    "gia nghia": 107.69, "dak nong": 107.69, "vi thanh": 105.47, "hau giang": 105.47,
}
# Tỉnh từ Quảng Trị trở vào (vĩ tuyến 17) – để biết giờ đồng hồ & lịch âm thời 1955-1975
MIEN_NAM = {k for k, v in KINH_DO.items()} - {
    "ha noi", "hai phong", "ha long", "quang ninh", "nam dinh", "thai binh", "hai duong",
    "bac ninh", "thai nguyen", "vinh phuc", "phu tho", "viet tri", "thanh hoa", "nghe an",
    "vinh", "ha tinh", "lang son", "lao cai", "dien bien", "son la", "quang binh", "dong hoi",
    "ninh binh", "ha nam", "phu ly", "hung yen", "hoa binh", "bac giang", "tuyen quang", "yen bai",
    "ha giang", "cao bang", "bac kan", "lai chau", "son tay", "vinh linh"}  # Vĩnh Linh ở phía Bắc vĩ tuyến 17


def bo_dau(s):
    import unicodedata
    s = s.lower().replace("đ", "d").replace("tp.", "tp ").replace("thành phố", "")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z ]", " ", s).split() and " ".join(re.sub(r"[^a-z ]", " ", s).split())


def tra_noi_sinh(noi):
    key = bo_dau(noi)
    if key in KINH_DO:
        return KINH_DO[key], key in MIEN_NAM
    for k in sorted(KINH_DO, key=len, reverse=True):   # khớp theo cụm từ nguyên vẹn, ưu tiên tên dài
        if (" " + k + " ") in (" " + key + " "):
            return KINH_DO[k], k in MIEN_NAM
    return None, None


# ---------------------------------------------------------------- Múi giờ & giờ mặt trời thực
def mui_gio_dong_ho(ngay, mien_nam):
    """Độ lệch UTC (giờ) của đồng hồ ở Việt Nam tại thời điểm sinh + cảnh báo nếu không chắc."""
    canh_bao = None
    d = ngay
    if d >= dt.date(1975, 6, 13):
        return 7.0, None
    if d >= dt.date(1955, 7, 1):
        if mien_nam and d >= dt.date(1960, 1, 1):
            return 8.0, None
        return 7.0, None
    # trước 1955: nhiều vùng dùng giờ khác nhau
    if dt.date(1945, 3, 15) <= d < dt.date(1945, 9, 2):
        off = 9.0
    elif dt.date(1947, 4, 1) <= d < dt.date(1955, 7, 1):
        off = 8.0
    elif dt.date(1943, 1, 1) <= d < dt.date(1945, 3, 15):
        off = 8.0
    elif d < dt.date(1911, 5, 1):
        off = 7.0 + 6.5 / 60
    else:
        off = 7.0
    canh_bao = ("Sinh trước 1955: giờ đồng hồ khi đó không thống nhất (vùng Pháp kiểm soát dùng UTC+8, "
                "vùng kháng chiến UTC+7, 1945 có lúc UTC+9). Đang giả định UTC+%g; nếu biết chắc hãy dùng --utc." % off)
    return off, canh_bao


def phuong_trinh_thoi_gian(t_utc):
    """Equation of time (phút), công thức NOAA, sai số < 1 phút."""
    doy = t_utc.timetuple().tm_yday
    g = 2 * math.pi / 365 * (doy - 1 + (t_utc.hour + t_utc.minute / 60 - 12) / 24)
    return 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                     - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))


def gio_mat_troi_thuc(t_utc, kinh_do):
    return t_utc + dt.timedelta(minutes=4 * kinh_do + phuong_trinh_thoi_gian(t_utc))


def chi_gio(t):
    """Chỉ số chi giờ 0..11 (Tý..Hợi) theo giờ địa phương t."""
    return ((t.hour + 1) // 2) % 12


def sat_ranh_gioi_gio(t, phut=10):
    """True nếu t cách ranh giới giờ âm lịch (giờ lẻ: 23,1,3,...) dưới `phut` phút."""
    m = t.hour * 60 + t.minute + t.second / 60
    k = min(abs(m - (60 * h)) for h in range(-1, 26, 2))
    return k < phut


# ---------------------------------------------------------------- Lịch âm theo thời kỳ
def mui_lich_am(ngay, mien_nam):
    """Âm lịch Việt Nam: trước 1968 (và miền Nam đến 1975) dùng lịch theo UTC+8 như Trung Quốc."""
    if ngay < dt.date(1968, 1, 1):
        return 8
    if mien_nam and ngay < dt.date(1976, 1, 1):
        return 8
    return 7


def duong_sang_am(ngay, tz):
    if tz == 8:
        l = Solar.fromYmd(ngay.year, ngay.month, ngay.day).getLunar()
        return l.getDay(), abs(l.getMonth()), l.getYear(), l.getMonth() < 0
    return solar_to_lunar(ngay.day, ngay.month, ngay.year, tz)


def am_sang_duong(d, m, y, nhuan, tz):
    if tz == 8:
        try:
            s = Lunar.fromYmd(y, -m if nhuan else m, d).getSolar()
        except Exception:
            raise SystemExit("LỖI: ngày âm %d/%d%s/%d không tồn tại trong lịch (UTC+8) của năm đó." % (
                d, m, " nhuận" if nhuan else "", y))
        b = s.getLunar()
        if (b.getYear(), b.getMonth(), b.getDay()) != (y, -m if nhuan else m, d):
            raise SystemExit("LỖI: ngày âm %d/%d%s/%d không tồn tại trong lịch (UTC+8) của năm đó." % (
                d, m, " nhuận" if nhuan else "", y))
        return dt.date(s.getYear(), s.getMonth(), s.getDay())
    r = lunar_to_solar(d, m, y, nhuan, tz)
    if r is None:
        raise SystemExit("LỖI: năm %d âm lịch (lịch Việt Nam) không có tháng %d nhuận." % (y, m))
    if solar_to_lunar(r[0], r[1], r[2], tz) != (d, m, y, nhuan):
        raise SystemExit("LỖI: ngày âm %d/%d%s/%d không tồn tại (tháng đó chỉ có 29 ngày)." % (
            d, m, " nhuận" if nhuan else "", y))
    return dt.date(r[2], r[1], r[0])


# ---------------------------------------------------------------- Chuẩn hoá đầu vào
class ThongTinSinh:
    pass


def doc_dau_vao(a):
    tt = ThongTinSinh()
    tt.gioi = a.gioi
    tt.canh_bao = []
    # nơi sinh
    if a.kinhdo is not None:
        tt.kinh_do = a.kinhdo
        mn = tra_noi_sinh(a.noi)[1] if a.noi else None
        tt.mien_nam = (a.mien == "nam") if a.mien else bool(mn)
        tt.can_mien = a.mien is None and mn is None and 102 <= a.kinhdo <= 110
        if not (102 <= a.kinhdo <= 110) and a.utc is None:
            raise SystemExit("LỖI: nơi sinh ngoài Việt Nam – cần --utc <độ lệch giờ đồng hồ lúc sinh so với UTC> "
                             "(tính cả giờ mùa hè nếu có), ví dụ Paris mùa đông --utc 1, mùa hè --utc 2.")
    elif a.noi:
        tt.can_mien = False
        kd, mn = tra_noi_sinh(a.noi)
        if kd is None:
            raise SystemExit("LỖI: không có kinh độ cho '%s'. Hãy tra kinh độ và chạy lại với --kinhdo <độ>." % a.noi)
        tt.kinh_do, tt.mien_nam = kd, mn
        if a.mien:
            tt.mien_nam = a.mien == "nam"
    else:
        tt.can_mien = False
        tt.kinh_do, tt.mien_nam = 105.85, False
        tt.canh_bao.append("Không có nơi sinh: tạm dùng kinh độ Hà Nội (105,85°E).")
    tt.noi = a.noi or "(không rõ)"
    # ngày
    try:
        y, m, d = [int(x) for x in a.ngay.replace("/", "-").split("-")]
        if y < 100:
            raise ValueError
    except ValueError:
        raise SystemExit("LỖI: --ngay phải có dạng YYYY-MM-DD (năm-tháng-ngày), ví dụ 1990-05-17.")
    if not (1 <= m <= 12 and 1 <= d <= 31 and 1900 <= y <= 2099):
        raise SystemExit("LỖI: ngày/tháng/năm ngoài phạm vi (tháng 1-12, ngày 1-31, năm 1900-2099).")
    if a.nhuan and not a.am:
        raise SystemExit("LỖI: --nhuan chỉ dùng kèm --am (ngày âm lịch).")
    if a.am:
        if d > 30:
            raise SystemExit("LỖI: ngày âm lịch tối đa là 30.")
        # chọn lịch (UTC+7 hay UTC+8) sao cho khớp với thời kỳ của chính ngày dương tìm được
        ngay, tz_dung, loi = None, None, None
        for tz in ([a.lich_tz] if a.lich_tz else [7, 8]):
            try:
                cand = am_sang_duong(d, m, y, a.nhuan, tz)
            except (SystemExit, Exception) as e:
                loi = e
                continue
            if a.lich_tz or mui_lich_am(cand, tt.mien_nam) == tz:
                ngay, tz_dung = cand, tz
                break
        if ngay is None:
            goi_y = (" Lưu ý: miền Bắc dùng lịch UTC+7 từ 1968, miền Nam đến hết 1975 vẫn dùng lịch UTC+8 – "
                     "nếu sinh ở miền Nam hãy thêm --mien nam (hoặc --noi tỉnh)." if 1966 <= y <= 1976 else "")
            raise SystemExit((str(loi) if isinstance(loi, SystemExit) and str(loi) else
                             "LỖI: ngày âm %d/%d%s/%d không tồn tại trong lịch âm Việt Nam của thời kỳ đó." % (
                                 d, m, " nhuận" if a.nhuan else "", y)) + goi_y)
        tt.lich_tz_nhap = tz_dung
        tt.nhap = "âm lịch %02d/%02d/%d%s" % (d, m, y, " (tháng nhuận)" if a.nhuan else "")
    else:
        try:
            ngay = dt.date(y, m, d)
        except ValueError:
            raise SystemExit("LỖI: ngày dương lịch %02d/%02d/%d không tồn tại." % (d, m, y))
        tt.nhap = "dương lịch %02d/%02d/%d" % (d, m, y)
    if tt.can_mien and dt.date(1955, 7, 1) <= ngay < dt.date(1976, 1, 1):
        raise SystemExit("LỖI: sinh giai đoạn 1955-1975 – cần cho biết miền: thêm --mien bac hoặc --mien nam "
                         "(hoặc --noi kèm tên tỉnh) vì miền Nam khi đó dùng giờ UTC+8 và lịch âm khác.")
    # giờ
    if a.gio is None:
        tt.co_gio = False
        hh, mm = 12, 0
        tt.canh_bao.append("KHÔNG CÓ GIỜ SINH: không có trụ giờ, không an được lá số tử vi, không tính được "
                           "ngày khởi đại vận; chỉ dùng phần năm/tháng/ngày (tạm lấy 12:00 để tính).")
    else:
        tt.co_gio = True
        try:
            hh, mm = [int(x) for x in a.gio.replace("h", ":").split(":")[:2]]
            dt.time(hh, mm)
        except (ValueError, TypeError):
            raise SystemExit("LỖI: --gio phải có dạng HH:MM (24 giờ), ví dụ 08:30 hoặc 14:05.")
    tt.dong_ho = dt.datetime(ngay.year, ngay.month, ngay.day, hh, mm)
    if a.utc is not None:
        tt.utc_off = a.utc
    else:
        tt.utc_off, cb = mui_gio_dong_ho(ngay, tt.mien_nam)
        if cb:
            tt.canh_bao.append(cb)
    tt.t_utc = tt.dong_ho - dt.timedelta(hours=tt.utc_off)
    tt.t_bk = tt.t_utc + dt.timedelta(hours=8)          # giờ Bắc Kinh: chuẩn tính tiết khí của thư viện
    tt.tst = gio_mat_troi_thuc(tt.t_utc, tt.kinh_do)     # giờ mặt trời thực tại nơi sinh
    tt.dung_tst = not a.gio_dong_ho
    tt.t_dia_phuong = tt.tst if tt.dung_tst else tt.dong_ho
    tt.lich_tz = a.lich_tz or mui_lich_am(tt.t_dia_phuong.date(), tt.mien_nam)
    tt.sect = a.ty
    if not tt.co_gio:
        d0 = dt.datetime(ngay.year, ngay.month, ngay.day, 0, 0) - dt.timedelta(hours=tt.utc_off - 8)
        d1 = d0 + dt.timedelta(hours=23, minutes=59)
        g0, g1 = lunar_cua(d0).getEightChar(), lunar_cua(d1).getEightChar()
        if g0.getMonth() != g1.getMonth():
            tt.canh_bao.append("NGÀY SINH LÀ NGÀY GIAO TIẾT: trụ tháng%s đổi trong ngày (%s -> %s). "
                               "Không có giờ sinh thì không xác định được – cần hỏi giờ sinh."
                               % (" và trụ năm" if g0.getYear() != g1.getYear() else "",
                                  vn(g0.getMonth()), vn(g1.getMonth())))
    if tt.co_gio and sat_ranh_gioi_gio(tt.t_dia_phuong):
        tt.canh_bao.append("Giờ sinh nằm sát ranh giới giữa hai giờ âm lịch (dưới 10 phút). "
                           "Nên lập thêm lá số với giờ bên cạnh và đối chiếu sự kiện đời thực.")
    if tt.co_gio and chi_gio(tt.dong_ho) != chi_gio(tt.tst):
        tt.canh_bao.append("Giờ đồng hồ (%s) và giờ mặt trời thực (%s) rơi vào HAI giờ âm lịch khác nhau "
                           "(%s và %s). Mặc định dùng giờ mặt trời thực; muốn dùng giờ đồng hồ thêm --gio-dong-ho."
                           % (tt.dong_ho.strftime("%H:%M"), tt.tst.strftime("%H:%M"),
                              CHI_VN[chi_gio(tt.dong_ho)], CHI_VN[chi_gio(tt.tst)]))
    if tt.co_gio and tt.t_dia_phuong.hour == 23:
        tt.canh_bao.append("Sinh giờ Tý muộn (23h-24h): có 2 trường phái về trụ ngày. "
                           "Đang dùng --ty %d (%s). Xem thêm bản còn lại." %
                           (tt.sect, "23h đã sang ngày mới" if tt.sect == 1 else "trụ ngày vẫn là ngày cũ"))
    return tt


def lunar_cua(t):
    return Solar.fromYmdHms(t.year, t.month, t.day, t.hour, t.minute, t.second).getLunar()


def fmt_t(t):
    return t.strftime("%H:%M %d/%m/%Y")


def in_dau(tt):
    print("THÔNG TIN SINH")
    print("- Nhập: %s, giờ %s, giới tính %s, nơi sinh %s (kinh độ %.2f°E%s)" % (
        tt.nhap, tt.dong_ho.strftime("%H:%M") if tt.co_gio else "không rõ",
        "Nam" if tt.gioi == "nam" else "Nữ", tt.noi, tt.kinh_do,
        ", phía Nam vĩ tuyến 17" if tt.mien_nam else ""))
    print("- Giờ đồng hồ: %s (UTC%+g)" % (fmt_t(tt.dong_ho), tt.utc_off))
    if tt.co_gio:
        print("- Giờ mặt trời thực tại nơi sinh: %s (lệch %+d phút)" % (
            fmt_t(tt.tst), round((tt.tst - tt.dong_ho).total_seconds() / 60)))
        print("- Giờ dùng để an giờ: %s -> giờ %s" % (
            "mặt trời thực" if tt.dung_tst else "đồng hồ", CHI_VN[chi_gio(tt.t_dia_phuong)]))
    am = duong_sang_am(tt.t_dia_phuong.date() if tt.co_gio else tt.dong_ho.date(), tt.lich_tz)
    print("- Âm lịch (lịch Việt Nam, UTC+%d): ngày %d tháng %d%s năm %d" % (
        tt.lich_tz, am[0], am[1], " NHUẬN" if am[3] else "", am[2]))
    for c in tt.canh_bao:
        print("! " + c)
    print()


# ---------------------------------------------------------------- BÁT TỰ
def tu_tru(tt):
    """Trả về (ebk, eloc, danh sách trụ). Năm/tháng theo thời điểm tuyệt đối so với tiết khí
    (thư viện tính tiết khí theo giờ Bắc Kinh nên đưa vào giờ Bắc Kinh tương ứng);
    ngày/giờ theo giờ địa phương (mặc định giờ mặt trời thực)."""
    ebk = lunar_cua(tt.t_bk).getEightChar()
    ebk.setSect(tt.sect)
    eloc = lunar_cua(tt.t_dia_phuong).getEightChar()
    eloc.setSect(tt.sect)
    tru = [("Năm", ebk.getYear()), ("Tháng", ebk.getMonth()), ("Ngày", eloc.getDay())]
    if tt.co_gio:
        tru.append(("Giờ", eloc.getTime()))
    return ebk, eloc, tru


def bat_tu(tt, so_nam_luu=0, nam_xem=None, luu_nguyet=False):
    ebk, eloc, tru = tu_tru(tt)
    nam_am_sinh = duong_sang_am(tt.t_dia_phuong.date(), tt.lich_tz)[2]   # tuổi mụ tính theo năm âm lịch (Tết)
    nhat_chu = eloc.getDayGan()
    ts = LunarUtil.SHI_SHEN
    cs_idx = {g: i for i, g in enumerate(GAN_LIST)}

    def truong_sinh(gan, zhi):
        # nơi Trường Sinh của 10 can; can dương đi thuận, can âm đi nghịch
        goc = ZHI_LIST.index(TRUONG_SINH_GOC[gan])
        zi = ZHI_LIST.index(zhi)
        buoc = (zi - goc) % 12 if cs_idx[gan] % 2 == 0 else (goc - zi) % 12
        return TRUONG_SINH_12[buoc]

    print("BÁT TỰ (TỨ TRỤ)")
    print("| Trụ | Can chi | Thập thần (can) | Tàng can (thập thần) | Nạp âm | Trường sinh của Nhật chủ |")
    print("|---|---|---|---|---|---|")
    dem = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
    for ten, gz in tru:
        g, z = gz[0], gz[1]
        dem[CAN_HANH[g]] += 1
        dem[CHI_HANH[z]] += 1
        tt_can = "Nhật Chủ" if ten == "Ngày" else vn(ts[nhat_chu + g])
        tang = ", ".join("%s %s (%s)" % (CAN[h], HANH[CAN_HANH[h]], vn(ts[nhat_chu + h]))
                         for h in LunarUtil.ZHI_HIDE_GAN[z])
        print("| %s | %s %s (%s %s / %s %s) | %s | %s | %s | %s |" % (
            ten, CAN[g], CHI[z], CAN[g], HANH[CAN_HANH[g]], CHI[z], HANH[CHI_HANH[z]],
            tt_can, tang, vn(LunarUtil.NAYIN[gz]), vn(truong_sinh(nhat_chu, z))))
    print()
    am_duong = "Dương" if cs_idx[nhat_chu] % 2 == 0 else "Âm"
    print("- Nhật chủ: %s %s (%s %s), sinh tháng %s" % (
        CAN[nhat_chu], HANH[CAN_HANH[nhat_chu]], am_duong, HANH[CAN_HANH[nhat_chu]], CHI[ebk.getMonthZhi()]))
    print("- Đếm ngũ hành (chỉ thiên can + địa chi, chưa tính tàng can, chưa trọng số): " +
          ", ".join("%s %d" % (HANH[k], v) for k, v in dem.items()))
    # ba yếu tố vượng/nhược – liệt kê căn cứ, Claude tự cân nhắc
    hnc = HANH[CAN_HANH[nhat_chu]]
    sinh_nc = [k for k, v in HANH_SINH.items() if v == hnc][0]
    zt = ebk.getMonthZhi()
    mua = {"寅": "Mộc", "卯": "Mộc", "巳": "Hỏa", "午": "Hỏa", "申": "Kim", "酉": "Kim", "亥": "Thủy", "子": "Thủy"}.get(zt, "Thổ")
    trang_thai = ("vượng" if hnc == mua else "tướng" if HANH_SINH[mua] == hnc else "hưu" if HANH_SINH[hnc] == mua
                  else "tù" if HANH_KHAC[hnc] == mua else "tử")
    du_khi = {"辰": "Ất Mộc (dư khí xuân)", "未": "Đinh Hỏa (dư khí hạ)", "戌": "Tân Kim (dư khí thu)",
              "丑": "Quý Thủy (dư khí đông)"}.get(zt)
    print("- Đắc lệnh: tháng %s thuộc mùa %s → Nhật chủ %s ở thế %s%s; trường sinh tại tháng: %s" % (
        CHI[zt], mua, hnc, trang_thai.upper(), (" (tháng tứ quý, còn %s – xét thêm)" % du_khi) if du_khi else "",
        vn(truong_sinh(nhat_chu, zt))))
    goc = []
    for ten, gz in tru:
        for h in LunarUtil.ZHI_HIDE_GAN[gz[1]]:
            hh = HANH[CAN_HANH[h]]
            if hh in (hnc, sinh_nc):
                goc.append("%s %s (%s %s)" % (ten, CHI[gz[1]], CAN[h], "Tỷ Kiếp" if hh == hnc else "Ấn"))
    print("- Đắc địa (gốc Tỷ Kiếp/Ấn trong tàng can các chi): " + (", ".join(goc) or "không có"))
    the = ["%s %s (%s)" % (ten, CAN[gz[0]], vn(ts[nhat_chu + gz[0]])) for ten, gz in tru
           if ten != "Ngày" and HANH[CAN_HANH[gz[0]]] in (hnc, sinh_nc)]
    print("- Đắc thế (can Tỷ Kiếp/Ấn lộ ra): " + (", ".join(the) or "không có"))
    if zt in "巳午未":
        print("- Điều hậu: sinh mùa hạ (%s) – cần cân nhắc Thủy; nhưng Thủy chỉ là dụng thần khi không sinh thêm cho "
              "hành đang thừa (xem 4.1).%s" % (CHI[zt], " Tháng Mùi là cuối hạ, nhu cầu điều hậu nhẹ hơn Tỵ, Ngọ."
                                                  if zt == "未" else ""))
    if zt in "亥子丑":
        print("- Điều hậu: sinh mùa đông (%s) – cần cân nhắc Hỏa; nhưng Hỏa chỉ là dụng thần khi không sinh thêm cho "
              "hành đang thừa (xem 4.1).%s" % (CHI[zt], " Tháng Sửu là cuối đông, nhu cầu điều hậu nhẹ hơn Hợi, Tý."
                                                  if zt == "丑" else ""))
    tru_ds = [(ten, GAN_LIST.index(gz[0]), ZHI_LIST.index(gz[1])) for ten, gz in tru]
    nb = quan_he_noi_bo(tru_ds)
    print("- Quan hệ trong tứ trụ: " + ("; ".join(nb) if nb else "không có hợp/xung/hình/hại"))
    print("- Tuần không (theo trụ ngày): %s" % " ".join(CHI[c] for c in eloc.getDayXunKong()))
    print("- Thai nguyên: %s" % vn(ebk.getTaiYuan()))
    dv_ds = []
    # đại vận
    if tt.co_gio:
        yun = ebk.getYun(1 if tt.gioi == "nam" else 0, 2)
        chieu = "thuận" if yun.isForward() else "nghịch"
        print("- Đại vận %s; khởi vận sau khi sinh %d năm %d tháng %d ngày (khoảng %s)" % (
            chieu, yun.getStartYear(), yun.getStartMonth(), yun.getStartDay(),
            yun.getStartSolar().toYmd()))
        print()
        print("ĐẠI VẬN (tuổi mụ tính theo năm âm lịch sinh %d; mỗi vận bắt đầu khoảng tháng %d dương lịch "
              "của năm ghi ở cột 'Từ năm'; thường can chủ 5 năm đầu, chi chủ 5 năm sau)" % (
                  nam_am_sinh, yun.getStartSolar().getMonth()))
        print("| Từ năm | Đến năm | Tuổi mụ | Can chi | Thập thần can | Tàng can chi (thập thần) | Nạp âm | Quan hệ với tứ trụ |")
        print("|---|---|---|---|---|---|---|---|")
        for dy in yun.getDaYun(11)[1:]:
            gz = dy.getGanZhi()
            c, z = GAN_LIST.index(gz[0]), ZHI_LIST.index(gz[1])
            dv_ds.append((dy.getStartYear(), dy.getEndYear(), c, z))
            print("| %d | %d | %d-%d | %s %s | %s | %s | %s | %s |" % (
                dy.getStartYear(), dy.getEndYear(), dy.getStartYear() - nam_am_sinh + 1, dy.getEndYear() - nam_am_sinh + 1,
                CAN[gz[0]], CHI[gz[1]],
                vn(ts[nhat_chu + gz[0]]),
                ", ".join("%s (%s)" % (CAN[h], vn(ts[nhat_chu + h])) for h in LunarUtil.ZHI_HIDE_GAN[gz[1]]),
                vn(LunarUtil.NAYIN[gz]), "; ".join(quan_he_moi(tru_ds, c, z)) or "–"))
    else:
        print("- Đại vận: cần giờ sinh để tính ngày khởi vận chính xác (chiều vận theo trụ năm ở trên: %s; "
              "nếu có cảnh báo giao tiết Lập Xuân thì chiều vận cũng chưa chắc)." % (
            "thuận" if (tt.gioi == "nam") == (cs_idx[ebk.getYearGan()] % 2 == 0) else "nghịch"))

    def dv_cua(y):
        for a, b, c, z in dv_ds:
            if a <= y <= b:
                return [("vận %s %s" % (CAN_VN[c], CHI_VN[z]), c, z)]
        return []

    if so_nam_luu:
        print()
        nam0 = nam_xem or dt.date.today().year
        print("LƯU NIÊN (can chi năm tính từ Lập Xuân; quan hệ xét với tứ trụ và đại vận đang chạy – năm đổi vận "
              "thì vận mới bắt đầu giữa năm)")
        print("| Năm | Tuổi mụ | Can chi | Thập thần can | Tàng can chi (thập thần) | Đại vận | Quan hệ với tứ trụ, đại vận |")
        print("|---|---|---|---|---|---|---|")
        for y in range(nam0, nam0 + so_nam_luu):
            gz = Solar.fromYmd(y, 6, 1).getLunar().getYearInGanZhiExact()
            c, z = GAN_LIST.index(gz[0]), ZHI_LIST.index(gz[1])
            dv = dv_cua(y)
            print("| %d | %d | %s %s | %s | %s | %s | %s |" % (
                y, y - nam_am_sinh + 1, CAN[gz[0]], CHI[gz[1]], vn(ts[nhat_chu + gz[0]]),
                ", ".join("%s (%s)" % (CAN[h], vn(ts[nhat_chu + h])) for h in LunarUtil.ZHI_HIDE_GAN[gz[1]]),
                dv[0][0].replace("vận ", "") if dv else "–", "; ".join(quan_he_moi(tru_ds, c, z, dv)) or "–"))
    if luu_nguyet:
        nam0 = nam_xem or dt.date.today().year
        print()
        print("LƯU NGUYỆT BÁT TỰ NĂM %d (tháng tiết khí, từ Lập Xuân %d đến Lập Xuân %d; quan hệ xét với tứ trụ, "
              "đại vận và năm)" % (nam0, nam0, nam0 + 1))
        print("| Tháng | Từ ngày (dương lịch) | Can chi | Thập thần can | Tàng can chi (thập thần) | Quan hệ |")
        print("|---|---|---|---|---|---|")
        gz_nam = Solar.fromYmd(nam0, 6, 1).getLunar().getYearInGanZhiExact()
        nam_ds = [("năm %s %s" % (CAN[gz_nam[0]], CHI[gz_nam[1]]), GAN_LIST.index(gz_nam[0]), ZHI_LIST.index(gz_nam[1]))]
        def gz_thang(d):
            return Solar.fromYmdHms(d.year, d.month, d.day, 12, 0, 0).getLunar().getMonthInGanZhiExact()
        d = dt.date(nam0, 1, 25)
        truoc, doi = gz_thang(d), []
        while d <= dt.date(nam0 + 1, 2, 15):
            d += dt.timedelta(days=1)
            m = gz_thang(d)
            if m != truoc:
                doi.append((d, m))
            truoc = m
        i0 = [i for i, (_, m) in enumerate(doi) if m[1] == "寅"][0]
        for k, (d, m) in enumerate(doi[i0:i0 + 12], 1):
            c, z = GAN_LIST.index(m[0]), ZHI_LIST.index(m[1])
            print("| T%d (%s) | %s | %s %s | %s | %s | %s |" % (
                k, CHI[m[1]], d.strftime("%d/%m/%Y"), CAN[m[0]], CHI[m[1]], vn(ts[nhat_chu + m[0]]),
                ", ".join("%s (%s)" % (CAN[h], vn(ts[nhat_chu + h])) for h in LunarUtil.ZHI_HIDE_GAN[m[1]]),
                "; ".join(quan_he_moi(tru_ds, c, z, dv_cua(d.year) + nam_ds)) or "–"))
        print("(Ngày đổi tháng là ngày giao tiết theo giờ Bắc Kinh tính lúc 12h trưa – có thể lệch 1 ngày.)")
    print()
    import thansat
    thansat.in_bang([(GAN_LIST.index(gz[0]), ZHI_LIST.index(gz[1])) for _, gz in tru])
    return tru


# ---------------------------------------------------------------- TỬ VI
def do_dai_thang_am(d, m, y, nhuan, tz):
    """Số ngày của tháng âm (29/30) theo lịch đang dùng."""
    dau = am_sang_duong(1, m, y, nhuan, tz)
    ngay30 = dau + dt.timedelta(days=29)
    return 30 if duong_sang_am(ngay30, tz)[0] == 30 else 29


def tu_vi(tt, nam_xem, phi=False, so_nam=1, luu_nguyet=False):
    import tuvi_vn as T
    if not tt.co_gio:
        print("TỬ VI: cần giờ sinh để an cung Mệnh. Bỏ qua.")
        print()
        return
    t = tt.t_dia_phuong
    ngay = t.date()
    ty_muon = t.hour == 23
    if ty_muon:                      # 23h-24h: giờ Tý của ngày hôm sau (cách tính phổ biến ở VN)
        ngay = ngay + dt.timedelta(days=1)
    gio = 0 if ty_muon else chi_gio(t)
    d, m, y, nhuan = duong_sang_am(ngay, tt.lich_tz)
    so_ngay = do_dai_thang_am(d, m, y, nhuan, tt.lich_tz)
    can, chi = (y - 4) % 10, (y - 4) % 12
    ls = T.lap_la_so(m, d, gio, can, chi, tt.gioi, so_ngay, nhuan)
    ad = "Dương" if can % 2 == 0 else "Âm"
    ban_menh = hanh_nap_am_vn(can, chi)
    hanh_cuc = [k for k, v in T.CUC.items() if v == ls["cuc"]][0]
    print("TỬ VI ĐẨU SỐ (cách an phổ biến ở Việt Nam – Thái Thứ Lang)")
    print("- Ngày âm dùng an sao: ngày %d tháng %d%s năm %s %s (%d), giờ %s%s" % (
        d, m, " NHUẬN" if nhuan else "", T.CAN[can], T.CHI[chi], y, T.CHI[gio],
        " (sinh 23h-24h: tính giờ Tý của ngày hôm sau)" if ty_muon else ""))
    if nhuan:
        print("  Tháng nhuận: ngày 1-15 an như tháng %d, từ ngày 16 an như tháng %d (cách phổ biến). "
              "Lá số này an theo tháng %d." % (m, m % 12 + 1, ls["thang"]))
    thuan_ly = (can % 2 == 0) == (ls["menh"] % 2 == 0)
    print("- %s %s, Mệnh ở cung %s → âm dương %s; đại hạn đi %s" % (
        ad, "Nam" if tt.gioi == "nam" else "Nữ", "dương" if ls["menh"] % 2 == 0 else "âm",
        "thuận lý" if thuan_ly else "nghịch lý", "thuận" if ls["chieu"] == 1 else "nghịch"))
    print("- Bản mệnh: %s; Cục: %s; quan hệ: %s" % (
        ban_menh, T.TEN_CUC[ls["cuc"]], quan_he_hanh(T.hanh_nap_am(can, chi), hanh_cuc, "Mệnh", "Cục")))
    print("- Mệnh tại %s, Thân tại %s (Thân cư %s); Mệnh chủ: %s; Thân chủ: %s" % (
        T.CHI[ls["menh"]], T.CHI[ls["than"]], T.ten_cung(ls, ls["than"]), ls["menh_chu"], ls["than_chu"]))
    print("- Tuần tại %s–%s; Triệt tại %s–%s" % tuple(T.CHI[i] for i in ls["tuan"] + ls["triet"]))
    print("- Tứ hóa năm sinh %s: %s" % (T.CAN[can], ", ".join(
        "%s %s (cung %s)" % (ten, hoa, T.ten_cung(ls, ls["vt"][ten])) for ten, hoa in ls["hoa"].items())))
    print()
    print("| Cung | Địa chi (can) | Chính tinh | Phụ tinh, sát tinh, hóa | Sao nhỏ | Tràng sinh | Bác sĩ | Thái Tuế | Đại hạn |")
    print("|---|---|---|---|---|---|---|---|---|")
    PHU = ["Lộc Tồn", "Kình Dương", "Đà La", "Văn Xương", "Văn Khúc", "Tả Phù", "Hữu Bật",
           "Thiên Khôi", "Thiên Việt", "Địa Không", "Địa Kiếp", "Hỏa Tinh", "Linh Tinh", "Thiên Mã"]
    for k in range(12):
        p = (ls["menh"] + k) % 12
        def fmt(ten):
            ds = T.do_sang(ten, p)
            h = ls["hoa"].get(ten)
            return ten + ("(%s)" % ds if ds else "") + ("[%s]" % h if h else "")
        chinh = [fmt(x) for x in T.CHINH_TINH if x in ls["sao"][p]]
        phu = [fmt(x) for x in PHU if x in ls["sao"][p]]
        nho = [x for x in ls["sao"][p] if x not in T.CHINH_TINH and x not in PHU]
        if p in ls["tuan"]:
            nho.insert(0, "TUẦN")
        if p in ls["triet"]:
            nho.insert(0, "TRIỆT")
        a, b = ls["dai_han"][p]
        print("| %s%s | %s (%s) | %s | %s | %s | %s | %s | %s | %d-%d |" % (
            T.ten_cung(ls, p), " (THÂN)" if p == ls["than"] else "", T.CHI[p], T.CAN[ls["can_cung"][p]],
            ", ".join(chinh) or "Vô chính diệu", ", ".join(phu), ", ".join(nho),
            ls["trang_sinh"][p], ls["bac_si"][p], ls["thai_tue"][p], a, b))
    print("(Độ sáng: M miếu, V vượng, Đ đắc, B bình, H hãm. Chính tinh chính chiếu từ cung đối diện khi Vô chính diệu.)")
    print()
    if phi:
        pf, lai = T.phi_hoa(ls)
        print("TỨ HÓA PHI TINH (can cung phát hóa; ★ = tự hóa, hóa quay về chính cung)")
        print("- Lai nhân cung: %s (%s) – cung có can trùng can năm sinh %s" % (
            T.ten_cung(ls, lai), T.CHI[lai], T.CAN[can]) if lai is not None else "- Lai nhân cung: không xác định")
        print("| Cung phát (can) | Hóa Lộc → | Hóa Quyền → | Hóa Khoa → | Hóa Kỵ → |")
        print("|---|---|---|---|---|")
        for k in range(12):
            p = (ls["menh"] + k) % 12
            print("| %s %s (%s) | %s |" % (T.ten_cung(ls, p), T.CHI[p], T.CAN[ls["can_cung"][p]], " | ".join(
                "%s → %s%s" % (sao, T.ten_cung(ls, q), " ★" if q == p else "") for _, sao, q in pf[p])))
        print("(Phi hóa theo bảng tứ hóa chủ lưu; luận theo phái Tứ hóa phi tinh: Lộc là duyên/được, Kỵ là nợ/vướng; "
              "Kỵ phát từ cung A vào cung B nghĩa là A 'nợ' B. Đây là phái riêng, khác cách luận Tam hợp truyền thống.)")
        print()
    nc, nz = (nam_xem - 4) % 10, (nam_xem - 4) % 12
    tuoi = nam_xem - y + 1
    if tuoi < 1:
        print("VẬN HẠN: năm xem %d trước năm sinh âm lịch %d – bỏ qua." % (nam_xem, y))
        print()
        return
    vh = T.van_han(ls, nc, nz, tuoi)
    print("VẬN HẠN NĂM %s %s %d (tuổi mụ %d; năm âm lịch tính từ Tết)" % (T.CAN[nc], T.CHI[nz], nam_xem, tuoi))
    if vh["dai_han"] is not None:
        a, b = ls["dai_han"][vh["dai_han"]]
        print("- Đại hạn %d-%d tuổi: cung %s (%s)" % (a, b, T.ten_cung(ls, vh["dai_han"]), T.CHI[vh["dai_han"]]))
    else:
        print("- Chưa vào đại hạn đầu (đại hạn đầu bắt đầu từ %d tuổi)." % ls["cuc"] if tuoi < ls["cuc"]
              else "- Tuổi %d vượt quá 12 đại hạn của lá số." % tuoi)
    print("- Tiểu hạn: cung %s (%s)" % (T.ten_cung(ls, vh["tieu_han"]), T.CHI[vh["tieu_han"]]))
    print("- Sao lưu: " + ", ".join("%s tại %s (%s)" % (k, T.ten_cung(ls, p), T.CHI[p]) for k, p in vh["luu"].items()))
    def ghi_goc(ten):
        g = ls["hoa"].get(ten)
        return " – gốc cũng %s" % g if g else ""

    if vh["dai_han"] is not None:
        cdh = ls["can_cung"][vh["dai_han"]]
        print("- Tứ hóa đại hạn (can cung đại hạn %s): " % T.CAN[cdh] + ", ".join(
            "%s %s (cung %s%s)" % (ten, T.HOA[i], T.ten_cung(ls, ls["vt"][ten]), ghi_goc(ten))
            for i, ten in enumerate(T.TU_HOA[cdh])))
    print("- Tứ hóa lưu niên (can %s): " % T.CAN[nc] + ", ".join(
        "%s %s (cung %s%s)" % (ten, hoa, T.ten_cung(ls, ls["vt"][ten]), ghi_goc(ten)) for hoa, ten in vh["hoa"]))
    print()
    if luu_nguyet:
        import lich_vn
        tz = mui_lich_am(dt.date(nam_xem, 6, 1), tt.mien_nam)
        thang_ds = []
        for m in range(1, 13):
            for nh in (False, True):
                r = lich_vn.lunar_to_solar(1, m, nam_xem, nh, tz) if tz == 7 else None
                if tz != 7:
                    try:
                        sl = Lunar.fromYmd(nam_xem, -m if nh else m, 1).getSolar()
                        r = (sl.getDay(), sl.getMonth(), sl.getYear())
                    except Exception:
                        r = None
                if r is None:
                    continue
                d0 = dt.date(r[2], r[1], r[0])
                if duong_sang_am(d0, tz) != (1, m, nam_xem, nh):
                    continue
                thang_ds.append((m, nh, d0))
        het = am_sang_duong(1, 1, nam_xem + 1, False, 7 if tz == 7 else 8)
        dq = (nz - (ls["thang"] - 1) + ls["gio"]) % 12
        dq_vn = (vh["tieu_han"] - (ls["thang"] - 1) + ls["gio"]) % 12
        can1 = ((nc % 5) * 2 + 2) % 10
        ebk_, eloc_, _ = tu_tru(tt)
        nchu = eloc_.getDayGan()
        print("LƯU NGUYỆT TỬ VI NĂM %s %s %d (tháng âm lịch; cung tháng theo phép Đẩu Quân: từ cung Lưu Thái Tuế đếm "
              "nghịch đến tháng sinh, rồi thuận đến giờ sinh là tháng Giêng – tháng Giêng tại %s; phép tính từ cung "
              "tiểu hạn thì tháng Giêng tại %s)" % (T.CAN[nc], T.CHI[nz], nam_xem, T.ten_cung(ls, dq),
                                                     T.ten_cung(ls, dq_vn)))
        print("| Tháng âm | Dương lịch | Can chi tháng | Cung tháng (Đẩu Quân) | Hóa Lộc | Hóa Quyền | Hóa Khoa | Hóa Kỵ | "
              "Bát tự giữa tháng |")
        print("|---|---|---|---|---|---|---|---|---|")
        for i, (m, nh, d0) in enumerate(thang_ds):
            d1 = (thang_ds[i + 1][2] if i + 1 < len(thang_ds) else het) - dt.timedelta(days=1)
            cm, zm = (can1 + m - 1) % 10, (m + 1) % 12
            cung = (dq + m - 1) % 12
            hn = {ten: hoa_ for hoa_, ten in vh["hoa"]}
            hoa = ["%s → %s%s%s" % (ten, T.ten_cung(ls, ls["vt"][ten]), ghi_goc(ten).replace(" – gốc cũng", "; gốc"),
                                    "; năm %s" % hn[ten] if ten in hn else "")
                   for ten in T.TU_HOA[cm]]
            giua = d0 + dt.timedelta(days=14)
            gm = Solar.fromYmdHms(giua.year, giua.month, giua.day, 12, 0, 0).getLunar().getMonthInGanZhiExact()
            print("| %d%s | %s – %s | %s %s | %s (%s) | %s | %s %s (%s) |" % (
                m, " nhuận" if nh else "", d0.strftime("%d/%m/%Y"), d1.strftime("%d/%m/%Y"), T.CAN[cm], T.CHI[zm],
                T.ten_cung(ls, cung), T.CHI[cung], " | ".join(hoa), CAN[gm[0]], CHI[gm[1]], vn(LunarUtil.SHI_SHEN[nchu + gm[0]])))
        print("(Tháng nhuận dùng cùng can chi và cung với tháng chính; có phái chia đôi. Cột cuối: can chi tháng tiết khí "
              "vào ngày 15 âm – xem bảng LƯU NGUYỆT BÁT TỰ để biết ngày đổi tháng.)")
        print()
    if so_nam > 1:
        print("VẬN HẠN TỬ VI NHIỀU NĂM (cung chứa sao lưu; tứ hóa lưu niên ghi cung mà sao được hóa đang đóng)")
        print("| Năm | Tuổi mụ | Đại hạn | Tiểu hạn | Thái Tuế | Lộc Tồn | Kình / Đà | Mã | Tang / Hổ | Khốc / Hư | "
              "Lộc | Quyền | Khoa | Kỵ |")
        print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for ny in range(nam_xem, nam_xem + so_nam):
            c2, z2 = (ny - 4) % 10, (ny - 4) % 12
            v2 = T.van_han(ls, c2, z2, ny - y + 1)
            L = v2["luu"]
            tc = lambda p: T.ten_cung(ls, p)
            print("| %d %s %s | %d | %s | %s | %s | %s | %s / %s | %s | %s / %s | %s / %s | %s |" % (
                ny, T.CAN[c2], T.CHI[z2], ny - y + 1, tc(v2["dai_han"]) if v2["dai_han"] is not None else "–",
                tc(v2["tieu_han"]), tc(L["Lưu Thái Tuế"]), tc(L["Lưu Lộc Tồn"]), tc(L["Lưu Kình Dương"]),
                tc(L["Lưu Đà La"]), tc(L["Lưu Thiên Mã"]), tc(L["Lưu Tang Môn"]), tc(L["Lưu Bạch Hổ"]),
                tc(L["Lưu Thiên Khốc"]), tc(L["Lưu Thiên Hư"]),
                " | ".join("%s (%s%s)" % (ten, tc(ls["vt"][ten]), ghi_goc(ten).replace(" – gốc cũng", "; gốc"))
                           for _, ten in v2["hoa"])))
        print()


HANH_SINH = {"Kim": "Thủy", "Thủy": "Mộc", "Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim"}
HANH_KHAC = {"Kim": "Mộc", "Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim"}


def quan_he_hanh(a, b, ten_a, ten_b):
    if a == b:
        return "%s và %s cùng hành %s (bình hòa)" % (ten_a, ten_b, a)
    if HANH_SINH[a] == b:
        return "%s (%s) sinh %s (%s)" % (ten_a, a, ten_b, b)
    if HANH_SINH[b] == a:
        return "%s (%s) sinh %s (%s)" % (ten_b, b, ten_a, a)
    if HANH_KHAC[a] == b:
        return "%s (%s) khắc %s (%s)" % (ten_a, a, ten_b, b)
    return "%s (%s) khắc %s (%s)" % (ten_b, b, ten_a, a)


def hanh_nap_am_vn(can, chi):
    return vn(LunarUtil.NAYIN[GAN_LIST[can] + ZHI_LIST[chi]])


# ---------------------------------------------------------------- PHONG THỦY
HUONG = ["Bắc", "Đông Bắc", "Đông", "Đông Nam", "Nam", "Tây Nam", "Tây", "Tây Bắc"]
# quẻ: (tên, số Lạc Thư, hướng, hào (dưới, giữa, trên) 1=dương, hành)
QUE = {"Khảm": (1, "Bắc", (0, 1, 0), "Thủy"), "Khôn": (2, "Tây Nam", (0, 0, 0), "Thổ"),
       "Chấn": (3, "Đông", (1, 0, 0), "Mộc"), "Tốn": (4, "Đông Nam", (0, 1, 1), "Mộc"),
       "Càn": (6, "Tây Bắc", (1, 1, 1), "Kim"), "Đoài": (7, "Tây", (1, 1, 0), "Kim"),
       "Cấn": (8, "Đông Bắc", (0, 0, 1), "Thổ"), "Ly": (9, "Nam", (1, 0, 1), "Hỏa")}
SO_QUE = {v[0]: k for k, v in QUE.items()}
DONG_TU = {"Khảm", "Ly", "Chấn", "Tốn"}
# Du niên: hào bị biến -> sao
DU_NIEN = [("Sinh Khí", (0, 0, 1), "đại cát"), ("Thiên Y", (1, 1, 0), "cát"),
           ("Diên Niên", (1, 1, 1), "cát"), ("Phục Vị", (0, 0, 0), "tiểu cát"),
           ("Họa Hại", (1, 0, 0), "hung"), ("Lục Sát", (1, 0, 1), "hung"),
           ("Ngũ Quỷ", (0, 1, 1), "hung"), ("Tuyệt Mệnh", (0, 1, 0), "đại hung")]
SAO9 = {1: "Nhất Bạch (Thủy)", 2: "Nhị Hắc (Thổ, bệnh)", 3: "Tam Bích (Mộc, thị phi)",
        4: "Tứ Lục (Mộc, văn xương)", 5: "Ngũ Hoàng (Thổ, đại hung)", 6: "Lục Bạch (Kim)",
        7: "Thất Xích (Kim, trộm cắp/khẩu thiệt)", 8: "Bát Bạch (Thổ, tài)", 9: "Cửu Tử (Hỏa, hỷ sự)"}
# đường bay Lạc Thư: giữa, TB, T, ĐB, N, B, TN, Đ, ĐN
DUONG_BAY = ["Giữa", "Tây Bắc", "Tây", "Đông Bắc", "Nam", "Bắc", "Tây Nam", "Đông", "Đông Nam"]
CUNG_SO = {"Bắc": 1, "Tây Nam": 2, "Đông": 3, "Đông Nam": 4, "Giữa": 5, "Tây Bắc": 6,
           "Tây": 7, "Đông Bắc": 8, "Nam": 9}


def cung_phi(nam, gioi):
    """Cung phi Bát trạch theo năm (năm tính từ Lập Xuân hoặc Tết - truyền vào)."""
    if gioi == "nam":
        k = 9 - ((nam - 1864) + 8) % 9
        if k == 5:
            k = 2
    else:
        k = ((nam - 1864) + 4) % 9 + 1
        if k == 5:
            k = 8
    return SO_QUE[k]


def bat_trach(que):
    hao = QUE[que][2]
    kq = []
    for ten, bien, tinh in DU_NIEN:
        moi = tuple(h ^ b for h, b in zip(hao, bien))
        q = [k for k, v in QUE.items() if v[2] == moi][0]
        kq.append((ten, QUE[q][1], tinh, q))
    return kq


def bay_sao(giua, thuan=True):
    pos = {}
    for i, cung in enumerate(DUONG_BAY):
        s = (giua - 1 + (i if thuan else -i)) % 9 + 1
        pos[cung] = s
    return pos


def sao_nam(nam_lx):
    return (1 - (nam_lx - 1864)) % 9 or 9


def sao_thang(nam_lx_chi, thang_tiet):
    """thang_tiet: 1 = tháng Dần (từ Lập Xuân), ..., 12 = tháng Sửu."""
    nhom = ZHI_LIST[nam_lx_chi]
    dau = 8 if nhom in "子午卯酉" else (5 if nhom in "辰戌丑未" else 2)
    return (dau - 1 - (thang_tiet - 1)) % 9 + 1


# 24 sơn theo chiều kim đồng hồ từ Tý (0°); (tên, cung Lạc Thư, vị trí địa/thiên/nhân 0/1/2, âm dương +1/-1)
SON24 = ["Tý", "Quý", "Sửu", "Cấn", "Dần", "Giáp", "Mão", "Ất", "Thìn", "Tốn", "Tỵ", "Bính",
         "Ngọ", "Đinh", "Mùi", "Khôn", "Thân", "Canh", "Dậu", "Tân", "Tuất", "Càn", "Hợi", "Nhâm"]
CUNG_CUA_SON = {}
for i, s in enumerate(SON24):
    CUNG_CUA_SON[s] = ["Bắc", "Đông Bắc", "Đông", "Đông Nam", "Nam", "Tây Nam", "Tây", "Tây Bắc"][((i + 1) % 24) // 3]
# vị trí trong cung: 0 = Địa nguyên, 1 = Thiên nguyên, 2 = Nhân nguyên
VI_TRI = {s: ((i + 1) % 24) % 3 for i, s in enumerate(SON24)}
# âm dương của 3 sơn trong cung: tứ chính (1,3,7,9): + - - ; tứ duy (2,4,6,8): - + +
def am_duong_son(so_cung, vi_tri):
    if so_cung in (1, 3, 7, 9):
        return (1, -1, -1)[vi_tri]
    return (-1, 1, 1)[vi_tri]


def son_tu_do(do):
    do = do % 360
    i = int(((do + 7.5) % 360) // 15)
    tam = i * 15
    lech = ((do - tam + 180) % 360) - 180
    return SON24[i], lech


def van_nam(nam_lx):
    return ((nam_lx - 1864) // 20) % 9 + 1


def huyen_khong(huong_do, van):
    huong, lech = son_tu_do(huong_do)
    toa, _ = son_tu_do(huong_do + 180)
    van_ban = bay_sao(van, True)
    cung_huong = CUNG_CUA_SON[huong]
    cung_toa = CUNG_CUA_SON[toa]

    def bay_tinh(sao_vao, son_goc):
        vt = VI_TRI[son_goc]
        if sao_vao == 5:
            ad = am_duong_son(CUNG_SO[CUNG_CUA_SON[son_goc]], vt)
        else:
            ad = am_duong_son(sao_vao, vt)
        return bay_sao(sao_vao, ad > 0), ad

    son_tinh, ad_s = bay_tinh(van_ban[cung_toa], toa)
    huong_tinh, ad_h = bay_tinh(van_ban[cung_huong], huong)
    return dict(huong=huong, toa=toa, lech=lech, cung_huong=cung_huong, cung_toa=cung_toa,
                van_ban=van_ban, son=son_tinh, huong_tinh=huong_tinh, ad_s=ad_s, ad_h=ad_h)


def phong_thuy(tt, a):
    nam_tet = duong_sang_am(tt.dong_ho.date(), tt.lich_tz)[2]
    lx = lunar_cua(tt.t_bk).getYearInGanZhiExact()
    nam_lx = tt.dong_ho.year if Solar.fromYmd(tt.dong_ho.year, 6, 1).getLunar().getYearInGanZhiExact() == lx else tt.dong_ho.year - 1
    print("PHONG THỦY")
    q1 = cung_phi(nam_tet, tt.gioi)
    q2 = cung_phi(nam_lx, tt.gioi)
    if q1 != q2:
        print("! Sinh giữa Tết và Lập Xuân (hoặc ngược lại): tính theo năm âm lịch (Tết) là cung %s; "
              "theo Lập Xuân (Bát trạch chính tông) là cung %s. Hỏi người dùng theo trường phái nào." % (q1, q2))
    for nhan, q, nam in (("theo năm âm lịch %d (Tết)" % nam_tet, q1, nam_tet),) + (
            (("theo Lập Xuân, năm %d" % nam_lx, q2, nam_lx),) if q1 != q2 else ()):
        print("- Cung phi (Bát trạch) %s: %s – hành %s – %s tứ mệnh" % (
            nhan, q, QUE[q][3], "Đông" if q in DONG_TU else "Tây"))
        print("| Du niên | Hướng | Tính chất |")
        print("|---|---|---|")
        for ten, huong, tinh, _ in bat_trach(q):
            print("| %s | %s | %s |" % (ten, huong, tinh))
    print()
    nam = a.nam_xem
    lx_y = nam
    print("CỬU TINH NĂM %d (tính từ Lập Xuân %d đến Lập Xuân %d)" % (nam, nam, nam + 1))
    sg = sao_nam(lx_y)
    pos = bay_sao(sg, True)
    print("| Cung | Sao |")
    print("|---|---|")
    for c in ["Giữa", "Bắc", "Đông Bắc", "Đông", "Đông Nam", "Nam", "Tây Nam", "Tây", "Tây Bắc"]:
        print("| %s | %s |" % (c, SAO9[pos[c]]))
    chi_nam = ZHI_LIST.index(Solar.fromYmd(nam, 6, 1).getLunar().getYearZhiExact())
    print("- Thái Tuế năm %d ở %s; Tuế Phá ở %s." % (nam, CHI_VN[chi_nam], CHI_VN[(chi_nam + 6) % 12]))
    print("- Sao trung cung từng tháng (tháng tiết khí, từ Lập Xuân): " + ", ".join(
        "T%d(%s): %d" % (i, CHI_VN[(i + 1) % 12], sao_thang(chi_nam, i)) for i in range(1, 13)))
    print()
    if a.huong is not None:
        if not a.van and not a.nam_xay:
            print("HUYỀN KHÔNG PHI TINH: cần --nam-xay (năm xây xong/nhập trạch) hoặc --van để biết vận của nhà. "
                  "Bỏ qua phần này – hãy hỏi người dùng.")
            print()
            return
        van = a.van or van_nam(a.nam_xay)
        hk = huyen_khong(a.huong, van)
        print("HUYỀN KHÔNG PHI TINH – NHÀ HƯỚNG %.1f°" % (a.huong % 360))
        print("- Hướng: sơn %s (cung %s), tọa: sơn %s (cung %s); lệch tâm sơn %+.1f°" % (
            hk["huong"], hk["cung_huong"], hk["toa"], hk["cung_toa"], hk["lech"]))
        print("- Vận %d (%s)" % (van, "theo --van" if a.van else "theo năm xây/nhập trạch %d" % a.nam_xay))
        if not a.van and a.nam_xay in (1864 + 20 * k for k in range(1, 12)):
            print("! Năm %d là năm chuyển vận (đổi vận từ Lập Xuân ~4/2): nếu xây xong/nhập trạch trước Lập Xuân "
                  "thì là vận %d – chạy lại với --van %d." % (a.nam_xay, (van - 2) % 9 + 1, (van - 2) % 9 + 1))
        if abs(hk["lech"]) > 4.5:
            print("! Hướng lệch tâm sơn > 4,5°: là KIÊM HƯỚNG, có thể phải dùng Thế quái (Thay quái). "
                  "Bàn dưới đây là Hạ quái; cần chuyên gia xác nhận.")
        elif abs(hk["lech"]) > 3:
            print("! Hướng lệch tâm sơn %.1f° (> 3°): một số phái đã coi là kiêm hướng và dùng Thế quái – nêu rõ khi luận."
                  % abs(hk["lech"]))
        if abs(abs(hk["lech"]) - 7.5) < 1.5:
            print("! Hướng nằm sát ranh giới hai sơn (Tiểu/Đại Không Vong) – đo lại bằng la bàn, tránh dùng hướng này.")
        print("| Cung | Vận tinh | Sơn tinh | Hướng tinh |")
        print("|---|---|---|---|")
        for c in ["Giữa", "Bắc", "Đông Bắc", "Đông", "Đông Nam", "Nam", "Tây Nam", "Tây", "Tây Bắc"]:
            print("| %s%s | %d | %d | %d |" % (
                c, " (TỌA)" if c == hk["cung_toa"] else (" (HƯỚNG)" if c == hk["cung_huong"] else ""),
                hk["van_ban"][c], hk["son"][c], hk["huong_tinh"][c]))
        s_toa, h_huong = hk["son"][hk["cung_toa"]], hk["huong_tinh"][hk["cung_huong"]]
        s_huong, h_toa = hk["son"][hk["cung_huong"]], hk["huong_tinh"][hk["cung_toa"]]
        if s_toa == van and h_huong == van:
            cuc = "Vượng sơn vượng hướng"
        elif s_huong == van and h_huong == van:
            cuc = "Song tinh đáo hướng"
        elif s_toa == van and h_toa == van:
            cuc = "Song tinh đáo tọa"
        elif s_huong == van and h_toa == van:
            cuc = "Thượng sơn hạ thủy"
        else:
            cuc = "(không thuộc 4 cục chính)"
        print("- Cục: %s" % cuc)
        for ten, ban in (("Sơn tinh", hk["son"]), ("Hướng tinh", hk["huong_tinh"])):
            if ban["Giữa"] == 5:
                thuan = ban["Tây Bắc"] == 6
                print("! %s: Ngũ Hoàng nhập trung cung bay %s → toàn bàn %s (Lạc Thư %s) – cách xấu, cần lưu ý khi luận."
                      % (ten, "thuận" if thuan else "nghịch", "PHỤC NGÂM" if thuan else "PHẢN NGÂM",
                         "trùng nguyên vị" if thuan else "đối nghịch nguyên vị"))
        print()


# ---------------------------------------------------------------- HỢP TUỔI (so tứ trụ với người khác)
def tru_nguoi_khac(chuoi):
    """'Tên:YYYY-MM-DD [HH:MM] [am|amnhuan]' (mặc định dương lịch, giờ đồng hồ Việt Nam)."""
    if ":" not in chuoi:
        raise SystemExit("LỖI: --nguoi dạng 'Tên:YYYY-MM-DD [HH:MM] [am]', vd 'Anh Hùng:1979-02-11' hoặc "
                         "'Chị Lan:1988-06-20 am'.")
    ten, rest = chuoi.split(":", 1)
    tk = rest.split()
    try:
        y, m, d = [int(x) for x in tk[0].split("-")]
    except ValueError:
        raise SystemExit("LỖI: ngày của '%s' phải dạng YYYY-MM-DD." % ten)
    gio = next((x for x in tk[1:] if ":" in x), None)
    am = next((x for x in tk[1:] if x.startswith("am")), None)
    if am:
        tz = 7 if y >= 1968 else 8
        ngay = am_sang_duong(d, m, y, am == "amnhuan", tz)
    else:
        ngay = dt.date(y, m, d)
    canh = []
    off, cb = mui_gio_dong_ho(ngay, False)
    if cb or (dt.date(1955, 7, 1) <= ngay < dt.date(1975, 6, 13)):
        canh.append("sinh trước 1975: giả định giờ miền Bắc UTC+%g" % off)
    hh, mm = (int(gio.split(":")[0]), int(gio.split(":")[1])) if gio else (12, 0)
    t = dt.datetime(ngay.year, ngay.month, ngay.day, hh, mm)
    t_bk = t - dt.timedelta(hours=off - 8)
    ebk = lunar_cua(t_bk).getEightChar()
    eloc = lunar_cua(t).getEightChar()
    tru = [("năm", ebk.getYear()), ("tháng", ebk.getMonth()), ("ngày", eloc.getDay())]
    if gio:
        tru.append(("giờ", eloc.getTime()))
    else:
        g0 = lunar_cua(dt.datetime(ngay.year, ngay.month, ngay.day, 0, 0) - dt.timedelta(hours=off - 8)).getEightChar()
        g1 = lunar_cua(dt.datetime(ngay.year, ngay.month, ngay.day, 23, 59) - dt.timedelta(hours=off - 8)).getEightChar()
        if g0.getMonth() != g1.getMonth():
            canh.append("NGÀY GIAO TIẾT, trụ tháng chưa chắc (%s/%s) – cần giờ sinh" % (vn(g0.getMonth()), vn(g1.getMonth())))
    am_l = duong_sang_am(ngay, 7 if ngay.year >= 1968 else 8)
    return dict(ten=ten.strip(), ngay=ngay, am=am_l, tru=tru, canh=canh)


def hop_tuoi(tt, ds):
    _, eloc, tru = tu_tru(tt)
    nc = eloc.getDayGan()
    toi = [(ten.lower(), GAN_LIST.index(gz[0]), ZHI_LIST.index(gz[1])) for ten, gz in tru]
    ts = LunarUtil.SHI_SHEN
    print("HỢP TUỔI – so tứ trụ người khác với đương số (Nhật chủ %s %s; trụ ngày %s, trụ năm %s)" % (
        CAN[nc], HANH[CAN_HANH[nc]], vn(tru[2][1]), vn(tru[0][1])))
    print("| Người | Ngày sinh (âm) | Tứ trụ | Nhật chủ | Họ là gì với đương số | Ngũ hành nổi (can+chi) | "
          "Quan hệ trụ năm / trụ ngày | Quan hệ chéo khác |")
    print("|---|---|---|---|---|---|---|---|")
    nguoi = [tru_nguoi_khac(x) for x in ds]
    for n in nguoi:
        dem = {}
        for _, gz in n["tru"]:
            for h in (HANH[CAN_HANH[gz[0]]], HANH[CHI_HANH[gz[1]]]):
                dem[h] = dem.get(h, 0) + 1
        noi = ", ".join("%s %d" % (k, v) for k, v in sorted(dem.items(), key=lambda x: -x[1]) if v >= 2) or "cân bằng"
        nd = n["tru"][2][1]
        ho = [(ten, GAN_LIST.index(gz[0]), ZHI_LIST.index(gz[1])) for ten, gz in n["tru"]]
        chinh, cheo = [], []
        for (tn, cn_, zn), (tm, cm, zm) in ((ho[0], toi[0]), (ho[2], toi[2])):
            for r in qh_can(cn_, cm):
                chinh.append("%s %s %s %s" % (tn, CAN_VN[cn_], r, CAN_VN[cm]))
            for r in qh_chi(zn, zm):
                chinh.append("%s %s %s %s" % (tn, CHI_VN[zn], r, CHI_VN[zm]))
        for tn, cn_, zn in ho:
            for tm, cm, zm in toi:
                if (tn, tm) in (("năm", "năm"), ("ngày", "ngày")):
                    continue
                for r in qh_chi(zn, zm):
                    cheo.append("%s họ %s %s %s %s" % (tn, CHI_VN[zn], r, CHI_VN[zm], tm))
        print("| %s | %s (%d/%d%s/%d)%s | %s | %s %s | %s; đương số là %s của họ | %s | %s | %s |" % (
            n["ten"], n["ngay"].strftime("%d/%m/%Y"), n["am"][0], n["am"][1], " nhuận" if n["am"][3] else "", n["am"][2],
            (" ! " + "; ".join(n["canh"])) if n["canh"] else "",
            " – ".join(vn(gz) for _, gz in n["tru"]), CAN[nd[0]], HANH[CAN_HANH[nd[0]]],
            vn(ts[nc + nd[0]]), vn(ts[nd[0] + nc]), noi, "; ".join(chinh) or "–", "; ".join(cheo) or "–"))
    if len(nguoi) > 1:
        print()
        print("QUAN HỆ GIỮA CÁC NGƯỜI KHÁC VỚI NHAU (trụ năm, trụ ngày)")
        for i in range(len(nguoi)):
            for j in range(i + 1, len(nguoi)):
                a, b = nguoi[i], nguoi[j]
                kq = []
                for k, nhan in ((0, "năm"), (2, "ngày")):
                    ga, gb = a["tru"][k][1], b["tru"][k][1]
                    ca, za, cb_, zb = GAN_LIST.index(ga[0]), ZHI_LIST.index(ga[1]), GAN_LIST.index(gb[0]), ZHI_LIST.index(gb[1])
                    r = ["%s %s" % (CAN_VN[ca] + "–" + CAN_VN[cb_], x) for x in qh_can(ca, cb_)] + \
                        ["%s %s" % (CHI_VN[za] + "–" + CHI_VN[zb], x) for x in qh_chi(za, zb)]
                    can_khac = HANH_KHAC[HANH[CAN_HANH[ga[0]]]] == HANH[CAN_HANH[gb[0]]] or \
                        HANH_KHAC[HANH[CAN_HANH[gb[0]]]] == HANH[CAN_HANH[ga[0]]]
                    if can_khac and (za - zb) % 12 == 6:
                        r.append("THIÊN KHẮC ĐỊA XUNG")
                    if r:
                        kq.append("%s: %s" % (nhan, ", ".join(r)))
                if kq:
                    print("- %s ↔ %s: %s" % (a["ten"], b["ten"], "; ".join(kq)))
    print("(Tứ trụ người khác tính theo giờ đồng hồ, không có giờ thì chỉ 3 trụ. 'Họ là gì với đương số' = thập thần "
          "của Nhật chủ họ so với Nhật chủ đương số: vd Chính Tài là người mang tiền/hợp vợ, Ấn là người nâng đỡ, "
          "Tỷ Kiếp là người ngang hàng/cạnh tranh, Quan Sát là người quản/áp lực, Thực Thương là người mình dìu dắt.)")
    print()


# ---------------------------------------------------------------- KỲ MÔN, LỤC NHÂM, MAI HOA (theo thời điểm hỏi)
def _chi_so(s):
    return ZHI_LIST.index(s)


def _gz_so(s):
    return [i for i in range(60) if i % 10 == GAN_LIST.index(s[0]) and i % 12 == ZHI_LIST.index(s[1])][0]


def ky_mon(tt, phep="huybo", nguong=None, loai="chuyen", gia="thoi", khong_bay=False, nam_sinh=None, ve=None,
           cau_hoi=None):
    import kymon as K
    e = lunar_cua(tt.t_dia_phuong).getEightChar()
    e.setSect(1)
    ebk = lunar_cua(tt.t_bk).getEightChar()
    gn, gg = _gz_so(e.getDay()), _gz_so(e.getTime())
    gy, gm = _gz_so(ebk.getYear()), _gz_so(ebk.getMonth())
    ngay = tt.t_dia_phuong.date() + (dt.timedelta(days=1) if tt.t_dia_phuong.hour == 23 else dt.timedelta(0))
    ten_ban = "phi bàn" if loai == "phi" else "chuyển bàn"
    cthang = _chi_so(ebk.getMonthZhi())

    def xong(b, cuc_txt, tieu, **kw):
        K.in_bo_sung(b, gy, gm, cthang, **kw)
        tt_o = K.trang_thai(b, cthang)
        K.in_trang_thai(b, tt_o)
        K.in_loai_tuong(b)
        bm = None
        if nam_sinh:
            gz_s = (nam_sinh - 4) % 60
            bm = K.tim_cung(b, gz_s)
            print("- Bản mệnh: năm sinh %d (%s) → can %s%s nằm ở cung %s trên thiên bàn. Năm sinh tính từ Lập Xuân "
                  "(sinh tháng 1 hoặc đầu tháng 2 dương lịch thì có thể là năm trước)." % (
                      nam_sinh, K.ten_gz(gz_s), K.CAN[gz_s % 10],
                      " (ẩn dưới %s)" % K.CAN[K._an(gz_s)] if gz_s % 10 == 0 else "", K.CUNG[bm] if bm else "?"))
            tt_o.setdefault(bm, []).insert(0, "★ Cung bản mệnh (%s %d)" % (K.CAN[gz_s % 10], nam_sinh))
            print()
        if ve:
            import vebankymon as V
            gz_n = kw.get("gz_ngay", gn)
            tru = [(n, K.ten_gz(g), K.CUNG[K.tim_cung(b, g)].split(" (")[0] if K.tim_cung(b, g) else "?")
                   for n, g in (("Năm", gy), ("Tháng", gm), ("Ngày", gz_n), ("Giờ", gg))]
            if nam_sinh:
                tru.append(("Mệnh", "%s %d" % (K.CAN[(nam_sinh - 4) % 10], nam_sinh),
                            K.CUNG[bm].split(" (")[0] if bm else "?"))
            info = dict(tieu_de=tieu, cau_hoi=cau_hoi, tru=tru, cuc=cuc_txt, ban_menh=bm,
                        thoi_gian="%s (giờ %s, %s) · %s" % (tt.dong_ho.strftime("%H:%M %d/%m/%Y"),
                                                           CHI_VN[chi_gio(tt.t_dia_phuong)],
                                                           "giờ mặt trời thực" if tt.dung_tst else "giờ đồng hồ", tt.noi),
                        trang_thai=dict(tt_o),
                        chu_thich="Màu môn: xanh = cát, đỏ = hung, xám = bình. Kv = không vong, Mã = dịch mã. "
                                  "Thiên bàn ở trên, địa bàn ở dưới%s. Tính bằng skill ky-mon-mo-rong; chỉ để tham khảo." % (
                                      ", ẩn can màu tím" if b.get("an_can") else ""))
            png, htm, tb = V.ve(b, K.CAN, info, ve)
            print("- Ảnh bàn: %s (%s); HTML: %s" % (png or "không có", tb, htm))
    dung = lambda d, c, g: K.ban_phi(d, c, g) if loai == "phi" else K.ban(d, c, g)
    if gia != "thoi" and loai == "am":
        raise SystemExit("LỖI: âm bàn chỉ dùng cho thời gia (--kymon-gia thoi).")
    if gia != "thoi":
        if gia == "nien":
            nam = tt.t_bk.year if (tt.t_bk.year - 4) % 60 == gy else tt.t_bk.year - 1
            d, c, ng = K.cuc_nien_gia(nam)
            b = dung(d, c, gy)
            tieu = "KỲ MÔN ĐỘN GIÁP – NIÊN GIA (%s; xem khí vận cả năm, việc lớn, phương hướng trong năm)" % ten_ban
            dau = ("- Năm %s %d (năm tính từ Lập Xuân) → %s nguyên, Âm độn %d cục. Niên gia luôn âm độn; mỗi nguyên 60 năm "
                   "(1864 thượng, 1924 trung, 1984–2043 hạ). Can chi năm đóng vai trò 'giờ': trực phù theo can năm, "
                   "trực sử theo chi năm." % (K.ten_gz(gy), nam, ["Thượng", "Trung", "Hạ"][ng], c))
            gz_dung = gy
        elif gia == "nguyet":
            d, c, ng, dau_k = K.cuc_nguyet_gia(gy)
            b = dung(d, c, gm)
            tieu = "KỲ MÔN ĐỘN GIÁP – NGUYỆT GIA (%s; xem khí vận cả tháng)" % ten_ban
            dau = ("- Tháng %s (tháng tiết khí), năm %s; khối 5 năm mở đầu bằng năm %s → %s nguyên, Âm độn %d cục. "
                   "Nguyệt gia luôn âm độn (phái Vương Thụy Dân: Dần Thân Tỵ Hợi thượng 1, Tý Ngọ Mão Dậu trung 7, "
                   "Thìn Tuất Sửu Mùi hạ 4). Can chi tháng đóng vai trò 'giờ'." % (
                       K.ten_gz(gm), K.ten_gz(gy), K.ten_gz(dau_k), ["Thượng", "Trung", "Hạ"][ng], c))
            gz_dung = gm
        else:
            d, c, gt, moc = K.cuc_nhat_gia(ngay, tt.utc_off)
            b = dung(d, c, gn)
            tieu = "KỲ MÔN ĐỘN GIÁP – NHẬT GIA (%s; xem khí vận cả ngày, chọn phương đi trong ngày)" % ten_ban
            dau = ("- Ngày %s; chu kỳ 60 ngày mở đầu bằng ngày Giáp Tý %s, gần tiết %s nhất → %s độn %d cục "
                   "(Kỳ môn pháp khiếu: Đông Chí, Vũ Thủy, Cốc Vũ dương 1-7-4; Hạ Chí, Xử Thử, Sương Giáng âm 9-3-6). "
                   "Can chi ngày đóng vai trò 'giờ'." % (K.ten_gz(gn), gt.strftime("%d/%m/%Y"), moc,
                                                      "Dương" if d else "Âm", c))
            gz_dung = gn
        b["nhan"] = {"nien": "năm", "nguyet": "tháng", "nhat": "ngày"}[gia]
        if loai == "phi":
            K.in_ban_phi(b, tieu + "\n" + dau)
        else:
            b.update(tieu_de=tieu, dau=dau)
            K.in_ban(b)
        print("! %s là phép ít dùng, các sách khác nhau về cách định cục; chỉ dùng để xem khái quát, việc cụ thể "
              "vẫn dựa vào thời gia." % {"nien": "Niên gia", "nguyet": "Nguyệt gia", "nhat": "Nhật gia"}[gia])
        print()
        b["gia"] = gia
        xong(b, "%s độn %d cục · %s" % ("Dương" if d else "Âm", c, {"nien": "niên gia", "nguyet": "nguyệt gia",
                                                                    "nhat": "nhật gia"}[gia]), tieu,
             gz_ngay=gn, gz_gio=gg)
        return
    jq = lunar_cua(tt.t_bk).getPrevJieQi(False)
    tiet_hb = K.TIET_HAN[jq.getName()]
    if loai == "am":
        duong = K.CUC[tiet_hb][0]
        cz = _chi_so(ebk.getYearZhi())
        cgio = gg % 12
        am = duong_sang_am(ngay, tt.lich_tz)
        cuc, tong = K.cuc_am_ban(cz, am[1], am[0], cgio)
        b = K.ban(duong, cuc, gg)
        b["gz_ngay"] = gn
        b["an_can"], ghi_an = K.an_can(b, duong, khong_bay)
        b["tieu_de"] = "KỲ MÔN ĐỘN GIÁP (thời gia, ÂM BÀN – phái Vương Phượng Lân)"
        b["dau"] = ("- Ngày %s, giờ %s; %s độn (tiết %s: từ Đông Chí đến trước Hạ Chí là dương độn); cục = (chi năm %s %d "
                    "+ tháng âm %d%s + ngày âm %d + chi giờ %s %d) = %d chia 9 dư → %d cục" % (
                        K.ten_gz(gn), K.ten_gz(gg), "Dương" if duong else "Âm", tiet_hb, CHI_VN[cz], cz + 1, am[1],
                        " nhuận" if am[3] else "", am[0], CHI_VN[cgio], cgio + 1, tong, cuc))
        K.in_ban(b)
        print("- Ẩn can: %s." % ghi_an)
        am8 = duong_sang_am(ngay, 8)
        if tt.lich_tz != 8 and (am8[0], am8[1]) != (am[0], am[1]):
            c8, _ = K.cuc_am_ban(cz, am8[1], am8[0], cgio)
            if c8 != cuc:
                print("! Âm lịch Việt Nam (UTC+7) và Trung Quốc (UTC+8) lệch nhau hôm nay (%d/%d so với %d/%d): theo lịch "
                      "Trung Quốc là %d cục. Sách Vương Phượng Lân dùng lịch Trung Quốc – nói rõ, có thể chạy thêm "
                      "--lich-tz 8." % (am[0], am[1], am8[0], am8[1], c8))
        if am[3]:
            print("! Tháng âm nhuận: đang lấy số tháng thường (%d) – sách không nói rõ cách tính tháng nhuận." % am[1])
        print()
        xong(b, "%s độn %d cục · âm bàn" % ("Dương" if duong else "Âm", cuc),
             "Kỳ môn độn giáp – thời gia, âm bàn (Vương Phượng Lân)")
        return
    js = jq.getSolar()
    gio_qua = (tt.t_bk - dt.datetime(js.getYear(), js.getMonth(), js.getDay(), js.getHour(), js.getMinute())
               ).total_seconds() / 3600
    tiet_tn, ghi_tn, _ = K.tiet_tri_nhuan(ngay, tt.utc_off, nguong)
    ms_ng = K.nguyen_mao_son(gio_qua)
    phuong_an = {"huybo": (tiet_hb, None, "hủy bổ", ""),
                 "trinhuan": (tiet_tn, None, "trí nhuận", ghi_tn),
                 "maoson": (tiet_hb, ms_ng, "Mao Sơn", "đã qua %d giờ kể từ giao tiết" % gio_qua)}
    cuc_cua = {}
    for k, (tiet, ng, _, _) in phuong_an.items():
        bb = K.lap(gn, gg, tiet)
        if ng is not None:
            bb["nguyen"], bb["cuc"] = ng, K.CUC[tiet][1][ng]
        cuc_cua[k] = (bb["duong"], bb["cuc"], bb["nguyen"], tiet)
    duong, cuc, ng, tiet = cuc_cua[phep]
    _, _, ten, ghi = phuong_an[phep]
    b = dung(duong, cuc, gg)
    b.update(nguyen=ng, tiet=tiet, phu_dau=gn - gn % 5, gz_ngay=gn)
    if loai == "phi":
        K.in_ban_phi(b, "KỲ MÔN ĐỘN GIÁP (thời gia, phi bàn, định cục %s)\n- Ngày %s, giờ %s; tiết %s%s → %s độn %d cục, "
                     "%s nguyên" % (ten, K.ten_gz(gn), K.ten_gz(gg), tiet, " (%s)" % ghi if ghi else "",
                                    "Dương" if duong else "Âm", cuc, ["Thượng", "Trung", "Hạ"][ng]))
    else:
        K.in_ban(b, ten, ghi)
    khac = {}
    for k, v in cuc_cua.items():
        if k != phep and v[:2] != (duong, cuc):
            khac.setdefault(v[:2] + (v[3],), []).append(phuong_an[k][2])
    if khac:
        print("! Các phép định cục cho kết quả KHÁC nhau: " + "; ".join(
            "theo %s là %s độn %d cục (tiết %s)" % (" và ".join(n), "Dương" if v[0] else "Âm", v[1], v[2])
            for v, n in khac.items()) +
              ". Nói rõ với người dùng; có thể chạy thêm --kymon-phep huybo|trinhuan|maoson để xem bàn đó.")
    else:
        print("- Hủy bổ, trí nhuận và Mao Sơn cho cùng một cục (trí nhuận: %s)." % ghi_tn)
    xong(b, "%s độn %d cục · %s nguyên · %s" % ("Dương" if duong else "Âm", cuc, ["thượng", "trung", "hạ"][ng], ten),
         "Kỳ môn độn giáp – thời gia, %s" % ten_ban)


def luc_nham(tt):
    import lucnham as L
    import kymon as K
    e = lunar_cua(tt.t_dia_phuong).getEightChar()
    e.setSect(1)
    q = K.TIET_HAN[lunar_cua(tt.t_bk).getPrevQi(False).getName()]
    tuong = L.NGUYET_TUONG[q]
    gn, gg = _gz_so(e.getDay()), _gz_so(e.getTime())
    r = L.lap(gn, gg % 12, tuong)
    L.in_khoa(r, vn(e.getDay()), vn(e.getTime()), tuong, q)


def mai_hoa(tt, so):
    import maihoa as M
    t = tt.t_dia_phuong
    ngay = t.date() + (dt.timedelta(days=1) if t.hour == 23 else dt.timedelta(0))
    d, m, y, _ = duong_sang_am(ngay, tt.lich_tz)
    gio = chi_gio(t)
    chi_thang = _chi_so(lunar_cua(tt.t_bk).getEightChar().getMonthZhi())
    if so:
        q, tong = M.theo_so(so[0], so[1], gio if len(so) < 3 else None)
        nguon = "theo số %d và %d%s (tổng %d)" % (so[0], so[1], ", cộng số giờ %s" % CHI_VN[gio] if len(so) < 3 else "",
                                                  tong)
    else:
        q, (s1, s2) = M.theo_thoi_gian((y - 4) % 12, m, d, gio)
        nguon = "theo thời gian: năm %s (%d) + tháng %d + ngày %d = %d; + giờ %s (%d) = %d" % (
            CHI_VN[(y - 4) % 12], (y - 4) % 12 + 1, m, d, s1, CHI_VN[gio], gio + 1, s2)
    M.in_que(q, chi_thang, nguon)


def in_dau_thoi_diem(tt, ten):
    print("THỜI ĐIỂM %s: %s giờ đồng hồ (UTC%+g), %s; giờ dùng để tính: %s (%s) → giờ %s" % (
        ten, tt.dong_ho.strftime("%H:%M %d/%m/%Y"), tt.utc_off, tt.noi,
        tt.t_dia_phuong.strftime("%H:%M"), "mặt trời thực" if tt.dung_tst else "đồng hồ",
        CHI_VN[chi_gio(tt.t_dia_phuong)]))
    for c in tt.canh_bao:
        if not c.startswith("Sinh trước 1955") and not c.startswith("Sinh giờ Tý muộn"):
            print("! " + c.replace("Giờ sinh", "Giờ xem"))
    print()


# ---------------------------------------------------------------- main
def main():
    p = argparse.ArgumentParser(description="Lập lá số Bát tự / Tử vi / Phong thủy, Kỳ môn, Lục Nhâm, Mai hoa, "
                                            "chọn ngày (tiếng Việt)")
    p.add_argument("phan", nargs="+", choices=["battu", "tuvi", "phongthuy", "tatca",
                                               "kymon", "lucnham", "maihoa", "chonngay", "hoptuoi"],
                   help="phần cần lập")
    p.add_argument("--ngay", help="YYYY-MM-DD (dương lịch; thêm --am nếu là âm lịch). Kỳ môn/Lục Nhâm/Mai hoa: "
                                  "ngày giờ hỏi việc, bỏ trống = bây giờ")
    p.add_argument("--gio", help="HH:MM giờ đồng hồ lúc sinh (hoặc lúc hỏi việc); bỏ trống nếu không biết")
    p.add_argument("--gioi", choices=["nam", "nu"], help="bắt buộc với battu/tuvi/phongthuy")
    p.add_argument("--phi-hoa", action="store_true", help="in thêm bảng Tứ hóa phi tinh trong phần Tử vi")
    p.add_argument("--so", type=int, nargs="+", help="Mai hoa theo số: 2 số (thượng, hạ; hào động cộng số giờ) "
                                                     "hoặc thêm số 0 thứ ba để không cộng giờ")
    p.add_argument("--tu", help="chọn ngày: từ ngày YYYY-MM-DD")
    p.add_argument("--den", help="chọn ngày: đến ngày YYYY-MM-DD (tối đa 93 ngày)")
    p.add_argument("--tuoi", nargs="*", default=[], help="chọn ngày: người liên quan, dạng Tên:năm âm lịch sinh, "
                                                          "vd Chồng:1990 Vợ:1992")
    p.add_argument("--viec", default="chung", choices=["chung", "cuoi", "dongtho", "khaitruong", "xuathanh", "nhaptrach"])
    p.add_argument("--hoang-dao-tiet", action="store_true", help="chọn ngày: tính Hoàng đạo theo tháng tiết khí")
    p.add_argument("--kymon-phep", default="huybo", choices=["huybo", "trinhuan", "maoson"],
                   help="Kỳ môn thời gia: định cục hủy bổ (mặc định), trí nhuận hay Mao Sơn")
    p.add_argument("--kymon-ban", default="chuyen", choices=["chuyen", "phi", "am"],
                   help="Kỳ môn: chuyển bàn (mặc định), phi bàn, hay âm bàn (Vương Phượng Lân, chỉ thời gia)")
    p.add_argument("--an-can-khong-bay", action="store_true",
                   help="Âm bàn: khi can giờ đã ở cung trực sử thì giữ ẩn can trùng địa bàn (mặc định: nhập trung bay)")
    p.add_argument("--kymon-gia", default="thoi", choices=["thoi", "nhat", "nguyet", "nien"],
                   help="Kỳ môn: thời gia (mặc định), nhật gia, nguyệt gia, niên gia")
    p.add_argument("--nam-sinh", type=int, help="Kỳ môn: năm sinh (dương lịch, tính từ Lập Xuân) để đánh dấu cung bản mệnh")
    p.add_argument("--ve-ban", help="Kỳ môn: đường dẫn file .png để vẽ bàn 9 cung (kèm file .html cùng tên)")
    p.add_argument("--cau-hoi", help="Kỳ môn: câu hỏi, in lên ảnh bàn")
    p.add_argument("--nhuan-nguong", type=int, choices=[8, 9, 10],
                   help="Kỳ môn trí nhuận: số ngày phù đầu đến trước Hạ/Đông Chí thì nhuận (mặc định 9; lệ Khang Hy 8)")
    p.add_argument("--noi", help="nơi sinh (tỉnh/thành Việt Nam)")
    p.add_argument("--kinhdo", type=float, help="kinh độ nơi sinh (độ Đông) nếu không có trong bảng")
    p.add_argument("--mien", choices=["bac", "nam"], help="bắt buộc kèm --kinhdo nếu sinh 1955-1975")
    p.add_argument("--utc", type=float, help="ép độ lệch UTC của đồng hồ lúc sinh (vd 8 hoặc 7)")
    p.add_argument("--am", action="store_true", help="--ngay là ngày âm lịch")
    p.add_argument("--nhuan", action="store_true", help="tháng âm lịch nhuận")
    p.add_argument("--lich-tz", type=int, choices=[7, 8], help="ép múi giờ của lịch âm (7=VN sau 1968, 8=TQ)")
    p.add_argument("--gio-dong-ho", action="store_true", help="dùng giờ đồng hồ thay vì giờ mặt trời thực")
    p.add_argument("--ty", type=int, default=1, choices=[1, 2],
                   help="giờ Tý muộn 23-24h: 1 = sang ngày mới (mặc định), 2 = trụ ngày vẫn ngày cũ")
    p.add_argument("--luu-nien", type=int, default=5, help="số năm lưu niên bát tự cần liệt kê")
    p.add_argument("--so-nam", type=int, default=1, help="Tử vi: số năm vận hạn cần liệt kê từ --nam-xem (bảng gọn)")
    p.add_argument("--luu-nguyet", action="store_true", help="in lưu nguyệt Bát tự và Tử vi của năm --nam-xem")
    p.add_argument("--nguoi", nargs="*", default=[], help="hoptuoi: người cần so, dạng 'Tên:YYYY-MM-DD [HH:MM] [am]'")
    p.add_argument("--nam-xem", type=int, default=dt.date.today().year, help="năm xem vận hạn / cửu tinh")
    p.add_argument("--huong", type=float, help="độ hướng nhà (la bàn, 0-360) cho Huyền không")
    p.add_argument("--nam-xay", type=int, help="năm xây xong / nhập trạch (để lấy vận)")
    p.add_argument("--van", type=int, help="ép vận Huyền không (1-9)")
    a = p.parse_args()
    phan = set(a.phan)
    if "tatca" in phan:
        phan = (phan - {"tatca"}) | {"battu", "tuvi", "phongthuy"}
    la_so = phan & {"battu", "tuvi", "phongthuy", "hoptuoi"}
    if la_so and (not a.gioi or not a.ngay):
        raise SystemExit("LỖI: battu/tuvi/phongthuy/hoptuoi cần --ngay và --gioi của đương số.")
    if "hoptuoi" in phan and not a.nguoi:
        raise SystemExit("LỖI: hoptuoi cần --nguoi 'Tên:YYYY-MM-DD' ...")
    if "chonngay" in phan:
        import chonngay as CN
        if not a.tu or not a.den:
            raise SystemExit("LỖI: chonngay cần --tu YYYY-MM-DD và --den YYYY-MM-DD.")
        nguoi = []
        for x in a.tuoi:
            ten, _, nam = x.rpartition(":")
            try:
                nguoi.append((ten or nam, int(nam)))
            except ValueError:
                raise SystemExit("LỖI: --tuoi dạng Tên:năm, vd Vợ:1984 (năm âm lịch sinh).")
        try:
            tu, den = [dt.date(*[int(v) for v in s.split("-")]) for s in (a.tu, a.den)]
        except (ValueError, TypeError):
            raise SystemExit("LỖI: --tu/--den dạng YYYY-MM-DD.")
        CN.in_chon_ngay(tu, den, nguoi, a.viec, a.hoang_dao_tiet)
    hoi = phan & {"kymon", "lucnham", "maihoa"}
    if hoi:
        if not a.ngay:
            now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None) + dt.timedelta(hours=7)
            a.ngay = now.strftime("%Y-%m-%d")
            a.gio = a.gio or now.strftime("%H:%M")
        if not a.gio:
            raise SystemExit("LỖI: Kỳ môn/Lục Nhâm/Mai hoa cần giờ (--gio HH:MM).")
        g0 = a.gioi
        a.gioi = a.gioi or "nam"
        th = doc_dau_vao(a)
        a.gioi = g0
        if not a.noi and a.kinhdo is None:
            th.canh_bao = [c for c in th.canh_bao if not c.startswith("Không có nơi sinh")]
            th.noi = "Hà Nội (mặc định)"
        in_dau_thoi_diem(th, "HỎI VIỆC")
        if "kymon" in phan:
            ky_mon(th, a.kymon_phep, a.nhuan_nguong, a.kymon_ban, a.kymon_gia, a.an_can_khong_bay, a.nam_sinh, a.ve_ban,
                   a.cau_hoi)
        if "lucnham" in phan:
            luc_nham(th)
        if "maihoa" in phan:
            mai_hoa(th, a.so)
    if la_so:
        tt = doc_dau_vao(a)
        in_dau(tt)
        if "battu" in phan:
            bat_tu(tt, a.luu_nien, a.nam_xem, a.luu_nguyet)
        if "tuvi" in phan:
            tu_vi(tt, a.nam_xem, a.phi_hoa, a.so_nam, a.luu_nguyet)
        if "phongthuy" in phan:
            phong_thuy(tt, a)
        if "hoptuoi" in phan:
            hop_tuoi(tt, a.nguoi)


if __name__ == "__main__":
    main()
