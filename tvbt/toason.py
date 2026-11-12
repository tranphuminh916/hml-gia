# -*- coding: utf-8 -*-
"""toason.py - Xét tọa sơn / hướng của nhà, công trình, mộ khi chọn ngày (năm, tháng, ngày).

Nguồn chính: Hiệp Kỷ Biện Phương Thư 協紀辨方書 (Khâm định, 1741):
  - quyển 2 (Bản nguyên): 24 sơn, song sơn, Hồng Phạm ngũ hành, mộ long biến vận, niên nguyệt khắc sơn gia,
    bát quái nạp giáp;
  - quyển 3, 8 (Nghĩa lệ): Phục binh Đại họa, Âm phủ Thái Tuế (đã sửa theo khởi lệ), Phù thiên không vong
    (đã sửa theo khởi lệ), Lục hại, Tử phù, Cứu thoái, Tuần sơn La hầu, Bệnh phù;
  - quyển 15–19 (Niên biểu): bảng thần sát từng năm theo các mục 開山立向修方凶 / 開山凶 / 立向凶;
  - quyển 33 (Lợi dụng – Tuyển trạch yếu luận): Luận phù sơn, Luận lập hướng, Luận khai sơn lập hướng khác tu sơn
    tu hướng, Chế sát yếu pháp;
  - quyển 34: Nguyệt hung thần tổng luận (Nguyệt phá, Nguyệt Âm phủ, Nguyệt khắc sơn gia, Đại/Tiểu nguyệt kiến).

Mức: "loai" = sách nói không được phạm (hoặc tool không tính được phép chế nên coi như không dùng);
     "canh" = sách xếp nhẹ hơn / có thể chế / các sách nói khác nhau: báo để thầy cân nhắc.
Kiểu công trình: "duong" = dương trạch (động thổ, xây, sửa nhà); "am" = âm trạch (an táng, xây mộ).
"""
import datetime as dt

from lunar_python import Solar
from lunar_python.util import LunarUtil

CAN = "甲乙丙丁戊己庚辛壬癸"
CHI = "子丑寅卯辰巳午未申酉戌亥"
CAN_VN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI_VN = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

# 24 sơn theo vòng la bàn (chính châm), Tý ở 0°, mỗi sơn 15°, tâm sơn i ở i*15°.
SON = ["子", "癸", "丑", "艮", "寅", "甲", "卯", "乙", "辰", "巽", "巳", "丙",
       "午", "丁", "未", "坤", "申", "庚", "酉", "辛", "戌", "乾", "亥", "壬"]
SON_VN = ["Tý", "Quý", "Sửu", "Cấn", "Dần", "Giáp", "Mão", "Ất", "Thìn", "Tốn", "Tỵ", "Bính",
          "Ngọ", "Đinh", "Mùi", "Khôn", "Thân", "Canh", "Dậu", "Tân", "Tuất", "Càn", "Hợi", "Nhâm"]
HUONG8 = ["Bắc", "Đông Bắc", "Đông", "Đông Nam", "Nam", "Tây Nam", "Tây", "Tây Bắc"]


def chi_son(z):
    """Chi z (0..11) -> chỉ số sơn."""
    return 2 * z


def can_son(c):
    """Can c (0..9) -> chỉ số sơn, None với Mậu Kỷ (24 sơn không có Mậu Kỷ)."""
    return {0: 5, 1: 7, 2: 11, 3: 13, 6: 17, 7: 19, 8: 23, 9: 1}.get(c)


QUAI_SON = {"乾": 21, "坤": 15, "艮": 3, "巽": 9, "坎": 0, "离": 12, "震": 6, "兑": 18}   # Khảm Ly Chấn Đoài dùng chi Tý Ngọ Mão Dậu
QUAI_VN = {"乾": "Càn", "坤": "Khôn", "艮": "Cấn", "巽": "Tốn", "坎": "Khảm", "离": "Ly", "震": "Chấn", "兑": "Đoài", "中": "Trung cung"}
# Cửu cung: số -> quái, và 3 sơn của mỗi cung
CUNG_QUAI = {1: "坎", 2: "坤", 3: "震", 4: "巽", 5: "中", 6: "乾", 7: "兑", 8: "艮", 9: "离"}
CUNG_SON = {"坎": (23, 0, 1), "艮": (2, 3, 4), "震": (5, 6, 7), "巽": (8, 9, 10),
            "离": (11, 12, 13), "坤": (14, 15, 16), "兑": (17, 18, 19), "乾": (20, 21, 22), "中": ()}


def song_son(i):
    """Chi đồng cung theo song sơn của Hiệp Kỷ (quyển 2: 'tứ quái bát can các tại chi tiền nhất vị... dữ chi song tịnh'):
    Nhâm Tý, Quý Sửu, Cấn Dần, Giáp Mão, Ất Thìn, Tốn Tỵ, Bính Ngọ, Đinh Mùi, Khôn Thân, Canh Dậu, Tân Tuất, Càn Hợi."""
    return (i // 2) % 12 if i % 2 == 0 else ((i + 1) % 24) // 2


def vn(gc):
    """'丁未' -> 'Đinh Mùi'."""
    return "%s %s" % (CAN_VN[CAN.index(gc[0])], CHI_VN[CHI.index(gc[1])])


def viet(s):
    """Đổi mọi can chi chữ Hán trong câu sang tiếng Việt."""
    import re
    s = re.sub("[%s][%s]" % (CAN, CHI), lambda m: vn(m.group(0)), s)
    return s


def la_chi(i):
    return i % 2 == 0


def ten_son(i):
    return "%s (%s)" % (SON_VN[i], SON[i])


# ---------------------------------------------------------------- Đọc tọa / hướng
def _bo_dau(s):
    import unicodedata
    s = s.replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def doc_son(s):
    """'Tý' / '子' / 'ty' / độ la bàn '182.5' -> (chỉ số sơn, độ hoặc None, cảnh báo)."""
    s = (s or "").strip()
    if not s:
        raise SystemExit("LỖI: thiếu tên sơn hoặc độ la bàn.")
    try:
        do = float(s.replace(",", ".").rstrip("°"))
    except ValueError:
        do = None
    if do is not None:
        if not 0 <= do < 360:
            raise SystemExit("LỖI: độ la bàn phải từ 0 đến dưới 360.")
        i = int(((do + 7.5) % 360) // 15)
        lech = (do - i * 15 + 180) % 360 - 180
        cb = ""
        if abs(lech) > 6.0:
            ben = SON_VN[(i + (1 if lech > 0 else -1)) % 24]
            cb = ("độ %.1f° nằm sát ranh giới sơn %s và %s (cách tâm sơn %.1f°): nên đo lại, nếu sai sơn thì kết quả khác"
                  % (do, SON_VN[i], ben, abs(lech)))
        return i, do, cb
    if s in SON:
        return SON.index(s), None, ""
    s2 = {"離": "离", "兌": "兑"}.get(s, s)
    if s2 in QUAI_SON:
        return QUAI_SON[s2], None, ""
    for i, t in enumerate(SON_VN):
        if s.lower() == t.lower():
            return i, None, ""
    kd = _bo_dau(s)
    hop = [i for i, t in enumerate(SON_VN) if _bo_dau(t) == kd]
    if len(hop) == 1:
        return hop[0], None, ""
    if len(hop) > 1:
        raise SystemExit("LỖI: '%s' không dấu bị trùng (%s) – gõ có dấu hoặc dùng độ la bàn." % (
            s, ", ".join(SON_VN[i] for i in hop)))
    raise SystemExit("LỖI: không đọc được sơn '%s'. Dùng một trong: %s, hoặc độ la bàn 0–359." % (s, ", ".join(SON_VN)))


def mo_ta(i):
    huong = (i + 12) % 24
    return "tọa %s – hướng %s (mặt tiền nhìn về phía %s)" % (
        ten_son(i), ten_son(huong), HUONG8[int(((huong * 15 + 22.5) % 360) // 45)])


# ---------------------------------------------------------------- Thần sát năm
def tam_sat(z):
    """Tam sát theo chi (năm hoặc tháng): Thân Tý Thìn -> Tỵ Ngọ Mùi; Dần Ngọ Tuất -> Hợi Tý Sửu;
    Hợi Mão Mùi -> Thân Dậu Tuất; Tỵ Dậu Sửu -> Dần Mão Thìn (chi đối xung đế vượng và hai bên)."""
    de_vuong = {0: 0, 1: 9, 2: 6, 3: 3}[z % 4]
    t = (de_vuong + 6) % 12
    return [(t - 1) % 12, t, (t + 1) % 12]


def phuc_binh_dai_hoa(z):
    """Phục binh (can dương) / Đại họa (can âm) nằm kẹp giữa Tam sát (Lịch lệ, Khảo nguyên – quyển 3)."""
    t = tam_sat(z)[1]
    i = chi_son(t)
    return [(i - 1) % 24, (i + 1) % 24]          # hai can hai bên chi giữa của Tam sát


NAP_GIAP_KINH_PHONG = {0: "乾", 8: "乾", 1: "坤", 9: "坤", 2: "艮", 3: "兑", 4: "坎", 5: "离", 6: "震", 7: "巽"}


def am_phu(c):
    """Âm phủ Thái Tuế theo can c (năm/tháng/ngày). Hiệp Kỷ quyển 8 (sửa theo khởi lệ): hóa khí của can khắc hóa khí
    của cặp can kia; quái nạp hai can đó là chính Âm phủ, chính hai can ấy (nếu có trong 24 sơn) là bàng Âm phủ.
    Giáp Kỷ: Cấn Tốn + Bính Tân; Ất Canh: Đoài(Dậu) Càn + Đinh Nhâm; Bính Tân: Khảm(Tý) Khôn + Quý;
    Đinh Nhâm: Càn Ly(Ngọ) + Giáp; Mậu Quý: Khôn Chấn(Mão) + Ất Canh. Bỏ 'Âm phủ tam hợp' của Thông thư (sách bác)."""
    dich = ((c % 5) + 2) % 5                          # nhóm hóa khí bị khắc
    hai_can = [dich, dich + 5]
    chinh = [QUAI_SON[NAP_GIAP_KINH_PHONG[x]] for x in hai_can]
    bang = [can_son(x) for x in hai_can if can_son(x) is not None]
    return chinh, bang


# bản cung của can năm: Giáp Ất Bính Đinh Canh Tân theo nạp giáp; Mậu Kỷ theo Khảm Ly (nạp giáp gốc); Nhâm Quý theo
# 24 sơn nạp giáp (Ly nạp Nhâm, Khảm nạp Quý) – khớp khởi lệ: Nhâm Càn Giáp, Quý Khôn Ất, Mậu Khôn Ất, Kỷ Càn Giáp.
BAN_CUNG = {0: "乾", 1: "坤", 2: "艮", 3: "兑", 4: "坎", 5: "离", 6: "震", 7: "巽", 8: "离", 9: "坎"}
TRUNG_HAO_BIEN = {"乾": "离", "离": "乾", "坤": "坎", "坎": "坤", "艮": "巽", "巽": "艮", "兑": "震", "震": "兑"}
QUAI_NAP_CAN_24 = {"乾": 0, "坤": 1, "艮": 2, "兑": 3, "坎": 9, "离": 8, "震": 6, "巽": 7}


def phu_thien(c):
    """Phù thiên không vong theo can năm (Hiệp Kỷ quyển 8, sửa theo khởi lệ): quái nạp can năm làm bản cung, hào giữa
    biến ra quái Phá quân (tuyệt mệnh), lấy quái ấy và can nó nạp trong 24 sơn. Giáp: Ly Nhâm; Ất: Khảm Quý; Bính: Tốn Tân;
    Đinh: Chấn Canh; Mậu: Khôn Ất; Kỷ: Càn Giáp; Canh: Đoài Đinh; Tân: Cấn Bính; Nhâm: Càn Giáp; Quý: Khôn Ất.
    Quái Khảm Ly Chấn Đoài lấy sơn Tý Ngọ Mão Dậu (cách 24 sơn nạp giáp của sách)."""
    q = TRUNG_HAO_BIEN[BAN_CUNG[c]]
    return [QUAI_SON[q], can_son(QUAI_NAP_CAN_24[q])]


HONG_PHAM = {}
for _h, _ds in (("水", "甲寅辰巽戌子辛申"), ("土", "丑癸坤庚未"), ("木", "卯艮巳"), ("火", "午壬丙乙"), ("金", "乾亥酉丁")):
    for _x in _ds:
        HONG_PHAM[SON.index(_x)] = _h
MO_CHI = {"水": 4, "土": 4, "木": 7, "火": 10, "金": 1}         # mộ: Thủy Thổ ở Thìn, Mộc Mùi, Hỏa Tuất, Kim Sửu
NGU_TY = {0: 0, 5: 0, 1: 2, 6: 2, 2: 4, 7: 4, 3: 6, 8: 6, 4: 8, 9: 8}   # ngũ tý nguyên độn: can của giờ/tháng Tý
KHAC = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}
_HANH_VN = {"金": "Kim", "木": "Mộc", "水": "Thủy", "火": "Hỏa", "土": "Thổ"}
SINH = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}


NAP_AM = {"海中金": "Hải Trung Kim", "炉中火": "Lư Trung Hỏa", "大林木": "Đại Lâm Mộc",
          "路旁土": "Lộ Bàng Thổ", "剑锋金": "Kiếm Phong Kim", "山头火": "Sơn Đầu Hỏa",
          "涧下水": "Giản Hạ Thủy", "城头土": "Thành Đầu Thổ", "白蜡金": "Bạch Lạp Kim",
          "杨柳木": "Dương Liễu Mộc", "泉中水": "Tuyền Trung Thủy", "屋上土": "Ốc Thượng Thổ",
          "霹雳火": "Tích Lịch Hỏa", "松柏木": "Tùng Bách Mộc", "长流水": "Trường Lưu Thủy",
          "沙中金": "Sa Trung Kim", "山下火": "Sơn Hạ Hỏa", "平地木": "Bình Địa Mộc",
          "壁上土": "Bích Thượng Thổ", "金箔金": "Kim Bạch Kim", "覆灯火": "Phú Đăng Hỏa",
          "天河水": "Thiên Hà Thủy", "大驿土": "Đại Dịch Thổ", "钗钏金": "Thoa Xuyến Kim",
          "桑柘木": "Tang Đố Mộc", "大溪水": "Đại Khê Thủy", "沙中土": "Sa Trung Thổ",
          "天上火": "Thiên Thượng Hỏa", "石榴木": "Thạch Lựu Mộc", "大海水": "Đại Hải Thủy"}


def nap_am(gc):
    """'甲子' -> ('海中金', '金')."""
    t = LunarUtil.NAYIN[gc]
    return t, t[-1]


def mo_van(i, can_nam, sau_dong_chi=False):
    """Mộ vận của sơn i (Hiệp Kỷ quyển 2, Mộ long biến vận): lấy ngũ tý nguyên độn của can năm đến chi mộ của hành
    Hồng Phạm, nạp âm can chi đó. Sơn Kim sau Đông chí dùng can năm sau. -> (can chi, nạp âm, hành)."""
    h = HONG_PHAM[i]
    c = (can_nam + 1) % 10 if (h == "金" and sau_dong_chi) else can_nam
    mz = MO_CHI[h]
    gc = CAN[(NGU_TY[c] + mz) % 10] + CHI[mz]
    t, hh = nap_am(gc)
    return gc, t, hh


def khac_son_gia(i, gc_khac, can_nam, sau_dong_chi=False):
    """Nạp âm của can chi gc_khac (năm/tháng/ngày) khắc mộ vận của sơn i? -> (có khắc, mô tả)."""
    mv = mo_van(i, can_nam, sau_dong_chi)
    tk, hk = nap_am(gc_khac)
    return KHAC[hk] == mv[2], "nạp âm %s %s khắc mộ vận %s %s của sơn %s" % (
        vn(gc_khac), NAP_AM[tk], vn(mv[0]), NAP_AM[mv[1]], SON_VN[i])


def son_bi_khac(gc_khac, can_nam, sau_dong_chi=False):
    return [i for i in range(24) if khac_son_gia(i, gc_khac, can_nam, sau_dong_chi)[0]]


def luc_hai(z):
    return (7 - z) % 12             # Tý-Mùi, Sửu-Ngọ, Dần-Tỵ, Mão-Thìn, Thân-Hợi, Dậu-Tuất


def cuu_thoai(z):
    return {0: 3, 1: 0, 2: 9, 3: 6}[z % 4]   # tử phương của tam hợp: Thân Tý Thìn ở Mão...


def nam_than(gc_nam, sau_dong_chi=False):
    """Bảng thần sát năm liên quan sơn, hướng (chỉ số sơn), theo mục của Niên biểu Hiệp Kỷ."""
    c, z = CAN.index(gc_nam[0]), CHI.index(gc_nam[1])
    chinh, bang = am_phu(c)
    return {
        "thai_tue": chi_son(z), "tue_pha": chi_son((z + 6) % 12), "tam_sat": [chi_son(x) for x in tam_sat(z)],
        "phuc_binh": phuc_binh_dai_hoa(z), "phu_thien": phu_thien(c),
        "khac_son": son_bi_khac(gc_nam, c, sau_dong_chi), "am_phu": chinh, "am_phu_bang": bang,
        "luc_hai": chi_son(luc_hai(z)), "tu_phu": chi_son((z + 5) % 12), "cuu_thoai": chi_son(cuu_thoai(z)),
        "tuan_son": (chi_son(z) + 1) % 24, "benh_phu": chi_son((z - 1) % 12),
        "mau_ky": mau_ky(c), "dau_hoa": chi_son({0: 0, 1: 9, 2: 6, 3: 3}[z % 4]),
        "dai_tuong": chi_son({0: 9, 1: 9, 2: 0, 3: 0, 4: 0, 5: 3, 6: 3, 7: 3, 8: 6, 9: 6, 10: 6, 11: 9}[z]),
        "pha_bai": QUAI_SON[TRUNG_HAO_BIEN_XUNG[NAP_GIAP_KINH_PHONG[c]]],
        "kim_than": [chi_son(CHI.index(x)) for x in KIM_THAN[c % 5]],
        "thien_quan": chi_son({0: 11, 1: 8, 2: 5, 3: 2}[z % 4]), "dia_quan": chi_son((z + 4) % 12),
    }


# Phá bại ngũ quỷ = quái đối xung của quái nạp can năm (Hiệp Kỷ q.33); Kim thần theo can năm (Niên biểu)
TRUNG_HAO_BIEN_XUNG = {"乾": "巽", "巽": "乾", "坤": "艮", "艮": "坤", "坎": "离", "离": "坎", "震": "兑", "兑": "震"}
KIM_THAN = {0: "午未申酉", 1: "辰巳", 2: "子丑寅卯午未", 3: "寅卯戌亥", 4: "申酉子丑"}


def mau_ky(c):
    """Mậu Kỷ sát (Tuyển Trạch Tông Kính, chép trong Hiệp Kỷ q.33): ngũ hổ độn từ can năm đến can Mậu, Kỷ -> hai chi."""
    dan = {0: 2, 5: 2, 1: 4, 6: 4, 2: 6, 7: 6, 3: 8, 8: 8, 4: 0, 9: 0}[c]      # can của tháng Dần
    kq = []
    for k in range(12):
        if (dan + k) % 10 in (4, 5):
            kq.append(chi_son((2 + k) % 12))
    return kq


# ---------------------------------------------------------------- Thần sát tháng
def dai_nguyet_kien(z_nam, thang):
    """Đại nguyệt kiến (Hiệp Kỷ sửa): năm Tý Ngọ Mão Dậu tháng giêng khởi Cấn 8, Thìn Tuất Sửu Mùi khởi Trung 5,
    Dần Thân Tỵ Hợi khởi Khôn 2, đi nghịch cửu cung (= sao nhập trung cung của tháng). thang = 1 (Dần) .. 12 (Sửu)."""
    bd = {0: 8, 6: 8, 3: 8, 9: 8, 4: 5, 10: 5, 1: 5, 7: 5, 2: 2, 8: 2, 5: 2, 11: 2}[z_nam]
    so = (bd - 1 - (thang - 1)) % 9 + 1
    return CUNG_QUAI[so]


def tieu_nguyet_kien(z_nam, thang):
    """Tiểu nguyệt kiến (Tiểu nhi sát): năm dương tháng giêng khởi Trung cung, năm âm khởi Ly, bay thuận."""
    bd = 5 if z_nam % 2 == 0 else 9
    so = (bd - 1 + (thang - 1)) % 9 + 1
    return CUNG_QUAI[so]


def hoan_vi(z_nam, thang):
    """Đại nguyệt kiến 'hoàn vị' (về đúng cung của nguyệt kiến) – Hiệp Kỷ q.34: không thể phạm."""
    q = dai_nguyet_kien(z_nam, thang)
    return chi_son((thang + 1) % 12) in CUNG_SON[q]


# ---------------------------------------------------------------- Can chi thời điểm
def can_chi(d):
    """Ngày d (date) -> năm (theo Lập xuân), tháng (theo tiết), ngày, và cờ 'sau Đông chí' (từ Đông chí đến hết năm
    Lập xuân đó, sơn Kim dùng mộ vận của can năm sau – Hiệp Kỷ q.2). Xét lúc 12h trưa."""
    trua = Solar.fromYmdHms(d.year, d.month, d.day, 12, 0, 0)
    l = trua.getLunar()
    t = Solar.fromYmd(d.year, 7, 1).getLunar().getJieQiTable()
    sau_dc = (not trua.isBefore(t["DONG_ZHI"])) or trua.isBefore(t["立春"])
    return l.getYearInGanZhiExact(), l.getMonthInGanZhiExact(), l.getDayInGanZhi(), sau_dc


# ---------------------------------------------------------------- Xét một ngày
def xet(d, toa, kieu):
    """Xét tọa sơn toa (0..23) cho ngày d. kieu: 'duong' (xây mới – khai sơn lập hướng) | 'sua' (sửa nhà đang có –
    tu sơn: thần sát khai sơn + tu phương, hướng chỉ xét Thái Tuế, Tam sát) | 'am' (an táng, xây mộ).
    -> dict(loai=[(cấp, câu)], canh=[(cấp, câu)], nam=gc, thang=gc, ngay=gc); cấp: nam | thang | ngay."""
    gn, gt, gd, sau_dc = can_chi(d)
    # 'phu' = phụ táng vào mộ cũ, mộ tổ: xét như an táng nhưng bỏ khắc sơn gia (Hiệp Kỷ q.2 "旧茔附葬者皆不论",
    # q.34 "袝葬祖茔…亦不忌") và Âm phủ chính, bàng (q.34 "如祔葬及修造正傍俱不忌"). Sách không miễn sát nào khác.
    phu = kieu == "phu"
    if phu:
        kieu = "am"
    huong = (toa + 12) % 24
    zt = song_son(toa)
    cung_toa = next(q for q, ds in CUNG_SON.items() if toa in ds)
    loai, canh = [], []

    def L(cap, s):
        loai.append((cap, viet(s)))

    def C(cap, s):
        canh.append((cap, viet(s)))

    cn, zn = CAN.index(gn[0]), CHI.index(gn[1])
    N = nam_than(gn, sau_dc)
    st, sh = SON_VN[toa], SON_VN[huong]

    def dong_cung(son_sat):
        """Sơn chi đúng bằng sát -> 'chinh'; sơn can/duy cùng cung bát quái (chính châm) với chi sát -> 'song'.
        Hiệp Kỷ q.34 (Tuần sơn La hầu): 'Tý niên tại Quý… dữ Thái Tuế đồng cung', 'Dần niên tại Giáp… bất đồng cung'."""
        if toa == son_sat:
            return "chinh"
        if not la_chi(toa) and la_chi(son_sat) and son_sat in CUNG_SON[cung_toa]:
            return "song"
        return None

    dc_txt = "cùng cung %s" % QUAI_VN[cung_toa]

    # --- NĂM ---
    k = dong_cung(N["tue_pha"])
    if k == "chinh":
        L("nam", "Tuế phá năm %s xung tọa %s (lệ không có phép chế)" % (gn, st))
    elif k == "song":
        C("nam", "Tuế phá năm %s %s với tọa %s" % (gn, dc_txt, st))
    if toa in N["tam_sat"]:
        L("nam", "Tam sát năm %s ở tọa %s (đại hung, không ngồi được)" % (gn, st))
    elif any(dong_cung(x) == "song" for x in N["tam_sat"]):
        C("nam", "Tam sát năm %s %s với tọa %s" % (gn, dc_txt, st))
    if toa in N["phuc_binh"]:
        L("nam", "Phục binh/Đại họa năm %s ở tọa %s (tọa sát)" % (gn, st))
    if phu:
        pass
    elif toa in N["am_phu"]:
        (C if kieu == "sua" else L)("nam", "Âm phủ Thái Tuế năm %s ở tọa %s%s" % (gn, st, (
            " (sửa nhà: Tông Kính ghi tu tạo không kỵ, q.8 ghi kỵ khai sơn – cân nhắc)" if kieu == "sua" else "")))
    elif toa in N["am_phu_bang"]:
        C("nam", "Bàng Âm phủ năm %s ở tọa %s (Thông thư dùng; Hiệp Kỷ theo Khâm thiên giám chỉ dùng quái, không dùng can)" % (gn, st))
    if not phu and toa in N["khac_son"]:
        _, mt = khac_son_gia(toa, gn, cn, sau_dc)
        if kieu == "am":
            hn = nap_am(gn)[1]
            che_ngu_thang = KHAC[nap_am(gt)[1]] == hn
            che_ngay = KHAC[nap_am(gd)[1]] == hn
            hoa_thang, hoa_ngay = nap_am(gt)[1] == SINH[hn], nap_am(gd)[1] == SINH[hn]
            if che_ngu_thang:
                C("thang", "Niên khắc sơn gia (%s), có nạp âm tháng %s chế lại – an táng dùng được nếu bên chế vượng, "
                           "bên khắc hưu tù" % (mt, gt))
            elif hoa_thang:
                C("thang", "Niên khắc sơn gia (%s), nạp âm tháng %s được năm sinh ra và sinh lại mộ vận – hóa khắc thành "
                           "sinh (lời bàn Hiệp Kỷ q.34)" % (mt, gt))
            else:
                C("thang", "Niên khắc sơn gia (%s): tháng này không chế được, an táng chỉ dùng ngày có nạp âm %s (chế) "
                           "hoặc %s (hóa khắc thành sinh)" % (
                    mt, _HANH_VN[[k for k, v in KHAC.items() if v == hn][0]], _HANH_VN[SINH[hn]]))
                if che_ngay:
                    C("ngay", "Niên khắc sơn gia, có nạp âm ngày %s chế lại" % gd)
                elif hoa_ngay:
                    C("ngay", "Niên khắc sơn gia, nạp âm ngày %s hóa khắc thành sinh (lời bàn q.34)" % gd)
                else:
                    L("ngay", "Niên khắc sơn gia, nạp âm ngày %s không chế, không hóa được" % gd)
        elif kieu == "sua":
            C("nam", "Niên khắc sơn gia: %s – chỉ kỵ nếu đào móng, động nền (sửa không động móng thì Thông thư không kỵ)" % mt)
        else:
            L("nam", "Niên khắc sơn gia: %s (xây mới không chế được)" % mt)
    elif not phu and sau_dc and toa in son_bi_khac(gn, cn, False):
        C("nam", "Niên khắc sơn gia năm %s: bảng năm ghi sơn %s bị khắc; sau Đông chí mộ vận sơn Kim đã đổi nên script "
                 "không loại, vẫn nên tránh nếu được" % (gn, st))
    if toa == N["thai_tue"] and zn in (0, 3, 6, 9):
        L("nam", "Thái Tuế ở tọa %s năm %s: năm Tý Ngọ Mão Dậu Thái Tuế trùng Đại sát, hướng gặp Tam sát và Tuế phá – "
                 "ngồi cũng không tốt" % (st, gn))
    elif toa == N["thai_tue"] and (toa in N["mau_ky"] or toa == N["dau_hoa"]):
        L("nam", "Thái Tuế ở tọa %s chồng Mậu Kỷ sát (Thái Tuế điệp Mậu Kỷ thì đại hung)" % st)
    elif toa == N["thai_tue"] or dong_cung(N["thai_tue"]) == "song":
        C("nam", "Thái Tuế ở tọa %s: sách cho 'ngồi được' nếu không chồng hung sát khác và có cát tinh chiếu" % st)
    for ten, khoa in (("Lục hại", "luc_hai"), ("Tử phù", "tu_phu"), ("Cứu thoái", "cuu_thoai")):
        if toa == N[khoa]:
            C("nam", "%s năm %s ở tọa %s (mục khai sơn hung)" % (ten, gn, st))
    # hướng
    k = None
    if huong == N["thai_tue"]:
        L("nam", "Hướng %s phạm Thái Tuế năm %s ('Thái Tuế ngồi được, không hướng được')" % (sh, gn))
    if huong in N["tam_sat"]:
        if kieu == "duong":
            L("nam", "Tam sát năm %s ở hướng %s (táng còn chế được, xây thì hiểm)" % (gn, sh))
        elif kieu == "sua":
            C("nam", "Tam sát năm %s ở hướng %s: chỉ sửa vào tháng Tam sát hưu tù, có tam hợp chế" % (gn, sh))
        else:
            C("nam", "Tam sát năm %s ở hướng %s: phải chế (tháng Tam sát hưu tù, tam hợp khắc)" % (gn, sh))
    if huong in N["phuc_binh"] and kieu == "duong":
        C("nam", "Phục binh/Đại họa năm %s ở hướng %s (thứ hung, kỵ xây sửa)" % (gn, sh))
    if toa in N["phu_thien"] or (huong in N["phu_thien"] and kieu != "sua"):
        C("nam", "Phù thiên không vong năm %s ở %s %s (tiểu sát, chủ hao tài; chế bằng Lục đức, Tam kỳ, Cửu tử)" % (
            gn, "tọa" if toa in N["phu_thien"] else "hướng", st if toa in N["phu_thien"] else sh))
    if huong == N["tuan_son"]:
        if zn in (2, 5, 8, 11) or kieu == "sua":
            C("nam", "Tuần sơn La hầu năm %s ở hướng %s (cần Nhất bạch hoặc cát tinh chiếu)" % (gn, sh))
        else:
            L("nam", "Tuần sơn La hầu năm %s ở hướng %s (cùng cung Thái Tuế – không phạm được)" % (gn, sh))
    if huong == N["benh_phu"] and kieu != "sua":
        C("nam", "Bệnh phù năm %s ở hướng %s" % (gn, sh))
    if huong in N["mau_ky"] and kieu != "sua":
        L("nam", "Mậu Kỷ đô thiên năm %s ở hướng %s (Hiệp Kỷ q.33: ở hướng còn nặng hơn ở tọa; sách không có phép chế)"
          % (gn, sh))
    if toa in N["mau_ky"] and kieu != "sua" and toa != N["thai_tue"]:
        L("nam", "Mậu Kỷ đô thiên năm %s ở tọa %s (Hiệp Kỷ q.33–34 không có phép chế)" % (gn, st))
    if kieu != "am" and (toa == N["dau_hoa"] or (huong == N["dau_hoa"] and kieu == "duong")):
        C("nam", "Đả đầu hỏa (Đại sát) năm %s ở %s (kỵ tu tạo, không kỵ táng)" % (
            gn, "tọa " + st if toa == N["dau_hoa"] else "hướng " + sh))
    if kieu == "sua":
        for ten, khoa in (("Đại tướng quân", "dai_tuong"), ("Phá bại ngũ quỷ", "pha_bai")):
            if toa == N[khoa]:
                C("nam", "%s năm %s ở tọa %s (thần sát tu phương, kỵ sửa phía sau nhà)" % (ten, gn, st))
        if toa in N["kim_than"]:
            C("nam", "Kim thần năm %s ở tọa %s (tu phương; chế được trừ mùa thu)" % (gn, st))
        for ten, khoa in (("Thiên quan phù", "thien_quan"), ("Địa quan phù", "dia_quan")):
            if toa == N[khoa]:
                C("nam", "%s năm %s ở tọa %s (cần cát tinh chiếu)" % (ten, gn, st))
        if toa in N["mau_ky"]:
            L("nam", "Mậu Kỷ đô thiên năm %s ở tọa %s (Hiệp Kỷ q.33 Luận tu phương: phương Mậu Kỷ của năm 'tất bất khả "
                     "tu')" % (gn, st))
    # --- THÁNG ---
    ct, zth = CAN.index(gt[0]), CHI.index(gt[1])
    thang = (zth - 2) % 12 + 1
    k = dong_cung(chi_son((zth + 6) % 12))
    if k == "chinh":
        L("thang", "Nguyệt phá tháng %s xung tọa %s" % (gt, st))
    elif k == "song":
        C("thang", "Nguyệt phá tháng %s %s với tọa %s" % (gt, dc_txt, st))
    chinh, bang = am_phu(ct)
    if phu:
        pass
    elif toa in chinh:
        (C if kieu == "sua" else L)("thang", "Nguyệt Âm phủ tháng %s ở tọa %s" % (gt, st))
    elif toa in bang:
        C("thang", "Bàng Âm phủ tháng %s ở tọa %s" % (gt, st))
    if not phu and KHAC[nap_am(gt)[1]] == mo_van(toa, cn, sau_dc)[2]:
        _, mt = khac_son_gia(toa, gt, cn, sau_dc)
        if kieu == "am":
            ht = nap_am(gt)[1]
            if KHAC[nap_am(gn)[1]] == ht:
                C("thang", "Nguyệt khắc sơn gia (%s), có nạp âm năm chế lại" % mt)
            else:
                C("thang", "Nguyệt khắc sơn gia (%s): an táng chỉ dùng ngày có nạp âm %s (chế) hoặc %s (hóa)" % (
                    mt, _HANH_VN[[k for k, v in KHAC.items() if v == ht][0]], _HANH_VN[SINH[ht]]))
                if KHAC[nap_am(gd)[1]] == ht:
                    C("ngay", "Nguyệt khắc sơn gia, có nạp âm ngày %s chế lại" % gd)
                elif nap_am(gd)[1] == SINH[ht]:
                    C("ngay", "Nguyệt khắc sơn gia, nạp âm ngày %s hóa khắc thành sinh (lời bàn q.34)" % gd)
                else:
                    L("ngay", "Nguyệt khắc sơn gia, nạp âm ngày %s không chế, không hóa được" % gd)
        elif kieu == "sua":
            C("thang", "Nguyệt khắc sơn gia: %s – chỉ kỵ nếu đào móng, động nền" % mt)
        else:
            L("thang", "Nguyệt khắc sơn gia: %s" % mt)
    dk = dai_nguyet_kien(zn, thang)
    if toa in CUNG_SON[dk] or huong in CUNG_SON[dk]:
        vt = "tọa" if toa in CUNG_SON[dk] else "hướng"
        if hoan_vi(zn, thang):
            (L if kieu != "am" else C)("thang", 
                "Đại nguyệt kiến tháng %s ở %s (cung %s, hoàn vị – không phạm được%s)" % (
                    gt, vt, QUAI_VN[dk], "" if kieu != "am" else "; Thông thư không kỵ táng"))
        elif kieu != "am":
            C("thang", "Đại nguyệt kiến tháng %s ở %s (cung %s; kỵ động thổ, cần quý nhân lộc mã, lục đức chiếu)" % (
                gt, vt, QUAI_VN[dk]))
    tk = tieu_nguyet_kien(zn, thang)
    if kieu != "am" and (toa in CUNG_SON[tk] or huong in CUNG_SON[tk]):
        C("thang", "Tiểu nguyệt kiến tháng %s ở %s (cung %s; kỵ sửa, không kỵ táng)" % (
            gt, "tọa" if toa in CUNG_SON[tk] else "hướng", QUAI_VN[tk]))
    if toa in [chi_son(x) for x in tam_sat(zth)]:
        C("thang", "Tam sát tháng %s (Kiếp/Tai/Nguyệt sát) ở tọa %s – kỵ tu tạo, lấy đất phương này" % (gt, st))
    # --- NGÀY ---
    cd, zd = CAN.index(gd[0]), CHI.index(gd[1])
    xz = (zd + 6) % 12
    if la_chi(toa) and toa == chi_son(xz):
        if zt in (1, 4, 7, 10):
            C("ngay", "Ngày %s xung tọa %s (sơn Thìn Tuất Sửu Mùi không kỵ xung lắm, chỉ một chữ xung thì tạm được)" % (gd, st))
        else:
            L("ngay", "Ngày %s xung tọa %s ('kỵ nhất địa chi xung sơn')" % (gd, st))
    elif dong_cung(chi_son(xz)) == "song":
        C("ngay", "Ngày %s xung chi %s với tọa %s" % (gd, dc_txt, st))
    chinh, bang = am_phu(cd)
    if not phu and (toa in chinh or toa in bang):
        C("ngay", "Âm phủ ngày %s ở tọa %s (can ngày hóa khí khắc sơn)" % (gd, st))
    if not phu and KHAC[nap_am(gd)[1]] == mo_van(toa, cn, sau_dc)[2]:
        C("ngay", "Ngày khắc sơn gia: %s" % khac_son_gia(toa, gd, cn, sau_dc)[1])
    return dict(loai=loai, canh=canh, nam=gn, thang=gt, ngay=gd, sau_dc=sau_dc)


def tom_tat(tu, den, toa, kieu):
    """Các kết luận cấp năm/tháng (không phụ thuộc ngày) trong khoảng ngày: [(từ ngày, năm, tháng, loại, cảnh báo)]."""
    d, ds, thay = tu, [], set()
    while d <= den:
        gn, gt, _, sau = can_chi(d)
        if (gn, gt, sau) not in thay:
            thay.add((gn, gt, sau))
            r = xet(d, toa, kieu)
            ds.append((d, gn, gt, [x for c, x in r["loai"] if c != "ngay"], [x for c, x in r["canh"] if c != "ngay"]))
        d += dt.timedelta(days=1)
    return ds


# ---------------------------------------------------------------- Lệnh "toa": bảng năm/tháng cho một tọa
def them_lenh(sub):
    p = sub.add_parser("toa", help="xét tọa sơn / hướng nhà, mộ theo năm và từng tháng (Hiệp Kỷ Biện Phương Thư)")
    p.add_argument("--nam", type=int, required=True, help="năm dương lịch (xét 12 tháng tiết từ Lập xuân năm đó)")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--toa", help="tọa sơn: tên (Tý, Nhâm, Cấn...) hoặc độ la bàn của phía lưng")
    g.add_argument("--huong", help="hướng: tên sơn hoặc độ la bàn phía mặt tiền (tự đổi ra tọa)")
    p.add_argument("--kieu", choices=["nha", "sua", "mo", "phutang"], default="nha",
                   help="nha = xây mới, động thổ; sua = sửa nhà đang ở (tu sơn); mo = an táng, xây mộ mới; "
                        "phutang = chôn thêm vào mộ cũ, mộ tổ")
    p.set_defaults(_chay=chay)


def doc_toa(toa=None, huong=None):
    if toa:
        i, do, cb = doc_son(toa)
        return i, do, cb
    i, do, cb = doc_son(huong)
    return (i + 12) % 24, None if do is None else (do + 180) % 360, cb


def chay(a):
    toa, do, cb = doc_toa(a.toa, a.huong)
    kieu = {"nha": "duong", "sua": "sua", "mo": "am", "phutang": "phu"}[a.kieu]
    lx = lambda y: Solar.fromYmd(y, 7, 1).getLunar().getJieQiTable()["立春"]
    tu, den = lx(a.nam), lx(a.nam + 1)
    tu = dt.date(tu.getYear(), tu.getMonth(), tu.getDay())
    den = dt.date(den.getYear(), den.getMonth(), den.getDay()) - dt.timedelta(days=1)
    in_bang(tu, den, toa, kieu, nguon_do(a, do), cb)


def nguon_do(a, do):
    if do is None:
        return ""
    return " (đo %s %s°)" % ("hướng" if a.huong else "tọa", (a.huong or a.toa).strip().rstrip("°"))


def in_bang(tu, den, toa, kieu, do="", cb=""):
    print("XÉT TỌA SƠN: %s%s" % (mo_ta(toa), do))
    print("- Loại công trình: %s" % TEN_KIEU[kieu])
    if cb:
        print("- CHÚ Ý: " + cb)
    print("- Theo Hiệp Kỷ Biện Phương Thư: năm tính từ Lập xuân, tháng theo tiết khí.")
    print()
    print("| Từ ngày | Năm | Tháng | Không dùng được | Cần cân nhắc |")
    print("|---|---|---|---|---|")
    for d, gn, gt, lo, ca in tom_tat(tu, den, toa, kieu):
        print("| %s | %s | %s | %s | %s |" % (d.strftime("%d/%m/%Y"), vn(gn), vn(gt), "; ".join(lo) or "-", "; ".join(ca) or "-"))
    print()
    print(GHI_CHU)


TEN_KIEU = {"duong": "dương trạch xây mới, động thổ (khai sơn lập hướng)",
            "sua": "sửa nhà đang có (tu sơn: thần sát khai sơn + tu phương; hướng chỉ xét Thái Tuế, Tam sát)",
            "am": "âm trạch – an táng, xây mộ mới",
            "phu": "phụ táng – chôn thêm vào mộ cũ, mộ tổ (như an táng nhưng không xét khắc sơn gia và Âm phủ, theo "
                   "Hiệp Kỷ; sách không bàn hợp táng hay tuổi người đã chôn trước)"}
GHI_CHU = ("(Ngoài bảng tháng, từng ngày còn xét: chi ngày xung tọa – loại, trừ sơn Thìn Tuất Sửu Mùi chỉ cảnh báo; Âm phủ và "
           "khắc sơn gia theo ngày – cảnh báo. Đã tính phép chế, hóa khắc sơn gia bằng nạp âm tháng, ngày khi an táng. Chưa tính: chế Tam sát bằng tam hợp cục, "
           "chế sát bằng Tam kỳ, Tử bạch, quý nhân lộc mã; Bính Đinh hỏa và quan phù phi cung theo tháng; long mạch, "
           "bổ long. Cần thầy xem thêm.)")


# ---------------------------------------------------------------- Tự kiểm tra
# Trích Niên biểu Hiệp Kỷ (quyển 15–19): năm -> (Tuế phá, Tam sát, tọa sát can, Phù thiên, Niên khắc sơn gia, Âm phủ
# (chính), Lục hại, Tử phù, Cứu thoái, Tuần sơn La hầu, Bệnh phù). Sơn ghi bằng chữ Hán theo bảng; quái Khảm Ly Chấn Đoài
# của bảng tương ứng sơn Tý Ngọ Mão Dậu.
MAU_NIEN_BIEU = {
    "甲戌": ("辰", "亥子丑", "壬癸", "离壬", "乾亥兑丁", "艮巽", "酉", "卯", "酉", "乾", "酉"),
    "乙亥": ("巳", "申酉戌", "庚辛", "坎癸", "甲寅辰巽戌坎辛申丑癸坤庚未", "兑乾", "申", "辰", "午", "壬", "戌"),
}


def _quy(s):
    m = {"坎": "子", "离": "午", "震": "卯", "兑": "酉"}
    return sorted(SON.index(m.get(x, x)) for x in s)


def doi_chieu(gc, mau, sau_dong_chi=False):
    """So thuật toán với một dòng Niên biểu; trả danh sách mục lệch."""
    N = nam_than(gc, sau_dong_chi)
    ts = lambda xs: sorted(xs)
    lech = []
    if [N["tue_pha"]] != _quy(mau[0]):
        lech.append("Tuế phá")
    if ts(N["tam_sat"]) != _quy(mau[1]):
        lech.append("Tam sát")
    if ts(N["phuc_binh"]) != _quy(mau[2]):
        lech.append("Tọa sát")
    if ts(N["phu_thien"]) != _quy(mau[3]):
        lech.append("Phù thiên")
    if mau[4] is not None and ts(N["khac_son"]) != _quy(mau[4]):
        lech.append("Niên khắc")
    if ts(N["am_phu"]) != _quy(mau[5]):
        lech.append("Âm phủ")
    for k, ten, j in (("luc_hai", "Lục hại", 6), ("tu_phu", "Tử phù", 7), ("cuu_thoai", "Cứu thoái", 8),
                      ("tuan_son", "Tuần sơn", 9), ("benh_phu", "Bệnh phù", 10)):
        if [N[k]] != _quy(mau[j]):
            lech.append(ten)
    return lech


def tu_kiem():
    loi = []
    for gc, mau in MAU_NIEN_BIEU.items():
        for x in doi_chieu(gc, mau):
            loi.append("Niên biểu %s: lệch %s" % (gc, x))
    # khởi lệ q.8: Âm phủ chính (theo quái) và Phù thiên theo 10 can
    ap = "艮巽 兑乾 坎坤 乾离 坤震 艮巽 兑乾 坎坤 乾离 坤震".split()
    ft = "离壬 坎癸 巽辛 震庚 坤乙 乾甲 兑丁 艮丙 乾甲 坤乙".split()
    for c in range(10):
        if sorted(am_phu(c)[0]) != _quy(ap[c]):
            loi.append("Âm phủ can %s" % CAN[c])
        if sorted(phu_thien(c)) != _quy(ft[c]):
            loi.append("Phù thiên can %s" % CAN[c])
    if [sorted(am_phu(c)[1]) for c in range(5)] != [_quy("丙辛"), _quy("丁壬"), _quy("癸"), _quy("甲"), _quy("乙庚")]:
        loi.append("bàng Âm phủ")
    # q.2: năm Giáp Tý, tháng nào khắc sơn nào (ví dụ của sách)
    vd = {"丙寅": "乾亥兑丁", "丁卯": "乾亥兑丁", "戊辰": "震艮巳", "己巳": "震艮巳", "庚午": "", "辛未": "",
          "壬申": "甲寅辰巽戌坎辛申丑癸坤庚未", "癸酉": "甲寅辰巽戌坎辛申丑癸坤庚未", "甲戌": "乾亥兑丁",
          "乙亥": "乾亥兑丁", "丙子": "离壬丙乙", "丁丑": "离壬丙乙"}
    for gc, s in vd.items():
        if son_bi_khac(gc, 0) != _quy(s):
            loi.append("Nguyệt khắc sơn gia năm Giáp Tý tháng %s" % gc)
    if son_bi_khac("壬申", 8) != [] or son_bi_khac("壬申", 8, True) != _quy("乾亥兑丁"):
        loi.append("năm Nhâm Thân: không khắc, sau Đông chí khắc sơn Kim")
    # Đại nguyệt kiến năm Kỷ Mão (Cấn Đoài Càn Trung Tốn Chấn Khôn Khảm Ly Cấn Đoài Càn); hoàn vị
    if "".join(dai_nguyet_kien(3, m) for m in range(1, 13)) != "艮兑乾中巽震坤坎离艮兑乾":
        loi.append("Đại nguyệt kiến")
    hv = sorted((z, m) for z in range(12) for m in range(1, 13) if hoan_vi(z, m))
    if hv != sorted([(z, m) for z in (0, 3, 6, 9) for m in (1, 7)] + [(z, m) for z in (1, 4, 7, 10) for m in (8, 9)] +
                    [(z, 11) for z in (2, 5, 8, 11)]):
        loi.append("hoàn vị Đại nguyệt kiến: %s" % hv)
    if "".join(tieu_nguyet_kien(0, m) for m in range(1, 10)) != "中乾兑艮离坎坤震巽" or \
            "".join(tieu_nguyet_kien(1, m) for m in range(1, 10)) != "离坎坤震巽中乾兑艮":
        loi.append("Tiểu nguyệt kiến")
    # song sơn, đọc sơn
    if "".join(CHI[song_son(i)] for i in range(24)) != "子丑丑寅寅卯卯辰辰巳巳午午未未申申酉酉戌戌亥亥子":
        loi.append("song sơn")
    if doc_son("182")[0] != 12 or doc_son("Càn")[0] != 21 or doc_son("Cấn")[0] != 3 or doc_son("ngo")[0] != 12 or \
            doc_son("352.6")[0] != 0 or not doc_son("8.5")[2]:
        loi.append("đọc tọa sơn")
    # một ngày cụ thể: 2027 (Đinh Mùi) – tọa Sửu: Tuế phá; tọa Thìn ngày Tuất: chỉ cảnh báo
    r = xet(dt.date(2027, 3, 10), 2, "duong")
    if not any(x.startswith("Tuế phá") for _, x in r["loai"]):
        loi.append("Tuế phá tọa Sửu năm Đinh Mùi")
    d = dt.date(2027, 4, 1)
    while can_chi(d)[2][1] != "戌":
        d += dt.timedelta(days=1)
    r = xet(d, 8, "duong")
    if any(c == "ngay" for c, _ in r["loai"]) or not any(c == "ngay" and "xung tọa" in x for c, x in r["canh"]):
        loi.append("sơn Thìn ngày Tuất phải chỉ cảnh báo")
    # rà soát độc lập: năm Nhâm Tý 2032 ngồi Tý là loại; Tuần sơn (Quý) cùng cung Thái Tuế là loại; năm Dần thì chỉ cảnh báo;
    # bàng Âm phủ chỉ cảnh báo; sửa nhà gặp niên khắc sơn gia chỉ cảnh báo
    d32 = dt.date(2032, 6, 1)
    if not any("Thái Tuế ở tọa" in x for _, x in xet(d32, 0, "am")["loai"]):
        loi.append("Thái Tuế tọa Tý năm Tý")
    if not any("Tuần sơn" in x for _, x in xet(d32, 13, "duong")["loai"]):       # tọa Đinh hướng Quý
        loi.append("Tuần sơn năm Tý")
    if any("Tuần sơn" in x for _, x in xet(dt.date(2034, 6, 1), 17, "duong")["loai"]):   # Giáp Dần: Tuần sơn ở Giáp
        loi.append("Tuần sơn năm Dần phải chỉ cảnh báo")
    r = xet(dt.date(2026, 6, 1), 11, "duong")       # Bính Ngọ: Âm phủ Khảm Khôn, bàng Quý; tọa Bính không dính
    r2 = xet(dt.date(2026, 6, 1), 1, "duong")       # tọa Quý: bàng Âm phủ
    if any("Âm phủ" in x for _, x in r2["loai"] if _ == "nam") or not any("Bàng Âm phủ" in x for _, x in r2["canh"]):
        loi.append("bàng Âm phủ phải chỉ cảnh báo")
    r = xet(dt.date(2027, 3, 10), 0, "sua")
    if any("Niên khắc" in x for _, x in r["loai"]) or not any("Niên khắc" in x for _, x in r["canh"]):
        loi.append("sửa nhà: niên khắc sơn gia chỉ cảnh báo")
    # rà soát độc lập 11/2026 (Hiệp Kỷ q.2, q.33, q.34):
    # - năm Bính Ngọ Mậu Kỷ đô thiên ở Tuất, Hợi: xây mới tọa Thìn hướng Tuất là loại (không có phép chế)
    if not any("Mậu Kỷ đô thiên" in x and "hướng Tuất" in x for _, x in xet(dt.date(2026, 3, 1), 8, "duong")["loai"]):
        loi.append("Mậu Kỷ đô thiên ở hướng phải loại")
    # - tọa Đinh (Hồng Phạm Kim, mộ vận Kỷ Sửu Hỏa) năm Bính Ngọ (Thủy) bị Niên khắc; an táng ngày Nhâm Tý (Mộc):
    #   Thủy sinh Mộc, Mộc sinh Hỏa – hóa khắc thành sinh, không loại
    r = xet(dt.date(2026, 4, 8), 13, "am")
    if any("Niên khắc" in x for c, x in r["loai"]) or not any("hóa khắc thành sinh" in x for c, x in r["canh"] if c == "ngay"):
        loi.append("Niên khắc: ngày nạp âm hóa khắc thành sinh")
    # - phụ táng vào mộ cũ không xét khắc sơn gia, Âm phủ; vẫn xét các sát khác
    ra, rp = xet(dt.date(2026, 3, 1), 13, "am"), xet(dt.date(2026, 3, 1), 13, "phu")
    txt = lambda r: " ".join(x for _, x in r["loai"] + r["canh"])
    if "Niên khắc" not in txt(ra) or "Âm phủ" not in txt(ra) or "khắc sơn gia" in txt(rp) or "Âm phủ" in txt(rp):
        loi.append("phụ táng phải bỏ khắc sơn gia và Âm phủ")
    if not any("Tuế phá" in x for _, x in xet(dt.date(2026, 3, 1), 0, "phu")["loai"]):
        loi.append("phụ táng vẫn phải xét Tuế phá")
    return loi
