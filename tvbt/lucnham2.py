# -*- coding: utf-8 -*-
"""lucnham2.py – Đại Lục Nhâm bổ sung (dùng kèm lucnham.py của bộ v2, không sửa file gốc).

Phần bổ sung cho một khóa đã lập bằng lucnham.lap:
  1. Thần sát Lục Nhâm (theo chi ngày, can ngày, tuần, tháng tiết, năm) và chỗ chúng nằm trên thiên bàn.
  2. Độn can (tuần độn) cho 4 khóa và 3 truyền; đánh dấu Lục Đinh, Tuần không, lạc không, Thiên Không.
  3. Bản mệnh (chi năm sinh) và hành niên (nam 1 tuổi khởi Bính Dần đi thuận, nữ 1 tuổi khởi Nhâm Thân
     đi nghịch, tính tuổi mụ) – thượng thần, thiên tướng, quan hệ với can ngày và tam truyền.
  4. Tất pháp phú: tự nhận diện các điều có điều kiện rõ ràng, máy kiểm được (in số điều, tên, điều kiện khớp,
     ý nghĩa ngắn bằng lời mình).
  5. Loại thần theo việc hỏi (--viec) và chỗ loại thần nằm.
  6. Khóa cách / nhật thần cách ngoài Cửu tông môn (Tam quang, Tam dương, Trảm quan, Du tử, ...).

Quy ước chỉ số: can 0=Giáp..9=Quý, chi 0=Tý..11=Hợi, hành 0 Mộc 1 Hỏa 2 Thổ 3 Kim 4 Thủy (như lucnham.py).
Nguồn đối chiếu (ghi trong tu_kiem): chú giải Tất pháp phú (bản Quách Ngự Thanh chú, chép ở tianyugong.com/bff
và "Dạ Không blog" zhifou123 id=63), "Lục Nhâm thần sát tường giải" (zhifou123 id=56), "Lục Nhâm 64 khóa"
(tianyugong.com/664), "Lục Nhâm cơ sở tri thức" (zhifou123 id=54).
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lucnham as L  # noqa: E402

CHI = L.CHI
CAN = L.CAN
HC = L.HANH_CHI
HG = L.HANH_CAN
TEN_HANH = L.TEN_HANH
KHAC = L.KHAC
SINH = L.SINH
KY = L.KY_CUNG

# ---------------------------------------------------------------- bảng nền
# Trường sinh theo ngũ hành (Lục Nhâm dùng chung cho can dương/âm). Thổ theo Thủy (trường sinh Thân, mộ Thìn):
# đúng như chú Tất pháp phú điều 19 ("thủy thổ nhật thai tại Ngọ") và điều 80 ("thủy thổ nhật tử khí tại Mão").
TRUONG_SINH = [11, 2, 8, 5, 8]
SINH_, BAI, VUONG, TU, MO, TUYET, THAI = 0, 1, 4, 7, 8, 9, 10


def vong(h, k):
    """Chi ở bậc k (0 Trường sinh, 1 Mộc dục/Bại, 4 Đế vượng, 7 Tử, 8 Mộ, 9 Tuyệt, 10 Thai) của hành h."""
    return (TRUONG_SINH[h] + k) % 12


LOC = [2, 3, 5, 6, 5, 6, 8, 9, 11, 0]
# Dương nhận = "lộc tiền nhất vị (tức đế vượng)": can dương tiến 1, can âm lùi 1 (Giáp Mão, Ất Dần, Bính Mậu Ngọ...)
NHAN = [(LOC[g] + (1 if g % 2 == 0 else -1)) % 12 for g in range(10)]
NHAT_DUC = [2, 8, 5, 11, 5, 2, 8, 5, 11, 5]      # Giáp Kỷ Dần, Ất Canh Thân, Bính Tân Tỵ, Đinh Nhâm Hợi, Mậu Quý Tỵ
DU_DO = [1, 0, 2, 5, 8, 1, 0, 2, 5, 8]           # Giáp Kỷ Sửu, Ất Canh Tý, Bính Tân Dần, Đinh Nhâm Tỵ, Mậu Quý Thân
TUAN_KY = {0: 1, 10: 1, 8: 0, 6: 0, 4: 11, 2: 11}  # chi đầu tuần -> Tuần kỳ
# Thiên đức theo tháng (0 = tháng Dần): Đinh(Mùi) Khôn(Thân) Nhâm(Hợi) Tân(Tuất) Càn(Hợi) Giáp(Dần)
# Quý(Sửu) Cấn(Dần) Bính(Tỵ) Ất(Thìn) Tốn(Tỵ) Canh(Thân) – can lấy cung ký như Lục Nhâm.
THIEN_DUC = [7, 8, 11, 10, 11, 2, 1, 2, 5, 4, 5, 8]
TH_DAU = {0: 8, 1: 5, 2: 2, 3: 11}               # chi % 4 -> chi đầu tam hợp (Thân, Tỵ, Dần, Hợi)
TEN_CUC = {8: "Nhuận hạ (Thủy cục)", 5: "Tòng cách (Kim cục)", 2: "Viêm thượng (Hỏa cục)", 11: "Khúc trực (Mộc cục)"}
HANH_TUONG = {"Quý Nhân": 2, "Đằng Xà": 1, "Chu Tước": 1, "Lục Hợp": 0, "Câu Trận": 2, "Thanh Long": 0,
              "Thiên Không": 2, "Bạch Hổ": 3, "Thái Thường": 2, "Huyền Vũ": 4, "Thái Âm": 3, "Thiên Hậu": 4}
CAT_TUONG = {"Quý Nhân", "Lục Hợp", "Thanh Long", "Thái Thường", "Thái Âm", "Thiên Hậu"}
MANH, TRONG, QUY_ = (2, 5, 8, 11), (0, 3, 6, 9), (1, 4, 7, 10)
TRUNG_KHI = {"雨水": "Vũ Thủy", "春分": "Xuân Phân", "谷雨": "Cốc Vũ", "小满": "Tiểu Mãn", "夏至": "Hạ Chí",
             "大暑": "Đại Thử", "处暑": "Xử Thử", "秋分": "Thu Phân", "霜降": "Sương Giáng", "小雪": "Tiểu Tuyết",
             "冬至": "Đông Chí", "大寒": "Đại Hàn", "YU_SHUI": "Vũ Thủy", "DONG_ZHI": "Đông Chí", "DA_HAN": "Đại Hàn"}
TU_LAP = {"立春": "Lập Xuân", "立夏": "Lập Hạ", "立秋": "Lập Thu", "立冬": "Lập Đông", "LI_CHUN": "Lập Xuân"}
PHAN_CHI = {"春分": "Xuân Phân", "夏至": "Hạ Chí", "秋分": "Thu Phân", "冬至": "Đông Chí", "DONG_ZHI": "Đông Chí"}
LT = [[L.luc_than(g, c) for c in range(12)] for g in range(10)]


def hop(a, b):
    return (a + b) % 12 == 1


def xung(a, b):
    return (a - b) % 12 == 6


def hai(a, b):
    return (a + b) % 12 == 7


def hinh(a, b):
    return L.HINH[a] == b or L.HINH[b] == a


def tam_hop(ds):
    """ds là bộ 3 chi khác nhau cùng một cục tam hợp -> chi đầu cục, ngược lại None."""
    s = set(ds)
    if len(s) == 3 and len({x % 4 for x in s}) == 1:
        return TH_DAU[next(iter(s)) % 4]
    return None


def hanh_truyen(tr):
    """Hành chung của tam truyền: hành của cục nếu ba truyền tam hợp hoặc tam hội phương (Dần Mão Thìn...),
    hành chung nếu ba truyền cùng hành; ngược lại None (chú Tất pháp phú: "tam truyền giai mộc, hoặc tam hợp
    mộc cục"; ví dụ điều 13 "Mậu Tý can thượng Ngọ" có ba truyền Dần Mão Thìn)."""
    d = tam_hop(tr)
    if d is not None:
        return HC[(d + 4) % 12]
    if len(set(tr)) == 3 and len({(t - 2) % 12 // 3 for t in tr}) == 1:
        return [0, 1, 3, 4][(tr[0] - 2) % 12 // 3]
    hs = {HC[t] for t in tr}
    return hs.pop() if len(hs) == 1 else None


def luc_than_can(g, d):
    """Quan hệ của can d (độn can) với can ngày g, gọi theo lục thân."""
    a, b = HG[g], HG[d]
    if a == b:
        return "Huynh đệ"
    if SINH(b, a):
        return "Phụ mẫu"
    if SINH(a, b):
        return "Tử tôn"
    if KHAC(a, b):
        return "Thê tài"
    return "Quan quỷ (độn quỷ)"


def lt_hanh(g, h):
    """Lục thân của hành h đối với can g."""
    a = HG[g]
    return "Huynh đệ" if a == h else "Phụ mẫu" if SINH(h, a) else "Tử tôn" if SINH(a, h) else \
        "Thê tài" if KHAC(a, h) else "Quan quỷ"


def mua(h, thang):
    """Vượng / Tướng / Hưu / Tù / Tử của hành h theo hành của tháng (nguyệt kiến)."""
    m = HC[thang]
    if h == m:
        return "Vượng"
    if SINH(m, h):
        return "Tướng"
    if SINH(h, m):
        return "Hưu"
    if KHAC(h, m):
        return "Tù"
    return "Tử"


# ---------------------------------------------------------------- 1. thần sát
Y_THAN_SAT = {
    "Dịch Mã": "đi lại, thay đổi, dời chuyển", "Đào Hoa (Hàm Trì)": "tình cảm, sắc dục, tiệc tùng",
    "Kiếp Sát": "hao đoạt, việc xảy ra bất ngờ", "Hoa Cái": "che lấp, cô độc; tôn giáo, nghệ thuật",
    "Tướng Tinh": "quyền hành, người cầm đầu", "Vong Thần": "thất thoát, lo nghĩ hão",
    "Thiên Mã": "đi xa, thăng chuyển, tin nhanh", "Thiên Đức": "giải hung, được che chở",
    "Nguyệt Đức": "giải hung, được giúp đỡ", "Thiên Hỷ": "tin vui, cưới hỏi",
    "Thiên Y": "thầy thuốc, chữa trị", "Giải Thần": "gỡ rối, giải kiện, tan việc",
    "Sinh Khí": "sinh sôi, việc mới, có thai", "Tử Khí": "suy giảm, việc nguội dần",
    "Thiên Quỷ": "dịch bệnh, việc ám muội", "Thành Thần": "việc dễ thành",
    "Hoàng Ân": "ân huệ từ cấp trên", "Nguyệt Phá": "hao phá trong tháng",
    "Tuế Phá": "đổ vỡ, trái ý trong năm", "Tang Môn": "việc buồn, hiếu sự (chỉ là một dấu hiệu)",
    "Điếu Khách": "thăm viếng, buồn phiền (chỉ là một dấu hiệu)", "Bệnh Phù": "bệnh cũ, việc cũ quay lại",
    "Lộc": "lương lộc, cơm áo", "Dương Nhận": "cứng rắn, dễ va chạm, tổn thương",
    "Quý nhân trú": "người giúp (ban ngày)", "Quý nhân dạ": "người giúp (ban đêm)",
    "Nhật Đức": "đức của ngày, giải hung", "Du Đô": "chỗ kẻ gian đi lại (xem mất đồ)",
    "Lỗ Đô": "chỗ kẻ gian ẩn (đối xung Du Đô)", "Tuần Nghi": "đầu tuần; phát dụng thành Lục nghi",
    "Tuần Kỳ": "sao kỳ của tuần; phát dụng thành Tam kỳ", "Lục Đinh": "Đinh thần: động gấp, đi lại, biến đổi",
}


def than_sat(g, z, thang, nam):
    """Trả về list (tên, chi, cách tính). thang = chi nguyệt kiến (tháng tiết), nam = chi thái tuế."""
    dau = TH_DAU[z % 4]
    i = (thang - 2) % 12
    xun = (z - g) % 12
    ds = [
        ("Dịch Mã", (dau + 6) % 12, "chi ngày"), ("Đào Hoa (Hàm Trì)", (dau + 1) % 12, "chi ngày"),
        ("Kiếp Sát", (dau + 9) % 12, "chi ngày"), ("Hoa Cái", (dau + 8) % 12, "chi ngày"),
        ("Tướng Tinh", (dau + 4) % 12, "chi ngày"), ("Vong Thần", (dau + 3) % 12, "chi ngày"),
        ("Lộc", LOC[g], "can ngày"), ("Dương Nhận", NHAN[g], "can ngày"),
        ("Quý nhân trú", L.QUY_NHAN[g][0], "can ngày"), ("Quý nhân dạ", L.QUY_NHAN[g][1], "can ngày"),
        ("Nhật Đức", NHAT_DUC[g], "can ngày"), ("Du Đô", DU_DO[g], "can ngày"),
        ("Lỗ Đô", (DU_DO[g] + 6) % 12, "can ngày"),
        ("Tuần Nghi", xun, "tuần"), ("Tuần Kỳ", TUAN_KY[xun], "tuần"), ("Lục Đinh", (xun + 3) % 12, "tuần"),
        ("Thiên Mã", (6 + 2 * (i % 6)) % 12, "tháng"), ("Thiên Đức", THIEN_DUC[i], "tháng"),
        ("Nguyệt Đức", {2: 5, 0: 11, 3: 2, 1: 8}[thang % 4], "tháng"),
        ("Thiên Hỷ", [10, 1, 4, 7][i // 3], "tháng"), ("Thiên Y", (thang + 2) % 12, "tháng"),
        ("Giải Thần", (8 + 2 * (i // 2)) % 12, "tháng"), ("Sinh Khí", (thang - 2) % 12, "tháng"),
        ("Tử Khí", (thang + 4) % 12, "tháng"), ("Thiên Quỷ", (9 - 3 * (i % 4)) % 12, "tháng"),
        ("Thành Thần", (5 + 3 * i) % 12, "tháng"), ("Hoàng Ân", (7 + 2 * i) % 12, "tháng"),
        ("Nguyệt Phá", (thang + 6) % 12, "tháng"),
        ("Tuế Phá", (nam + 6) % 12, "năm"), ("Tang Môn", (nam + 2) % 12, "năm"),
        ("Điếu Khách", (nam - 2) % 12, "năm"), ("Bệnh Phù", (nam - 1) % 12, "năm"),
    ]
    return ds


# ---------------------------------------------------------------- ngữ cảnh một khóa
class NguCanh:
    """Gom mọi đại lượng của một khóa để các luật dùng chung (thiên bàn T: địa chi -> thiên chi)."""

    def __init__(self, r, tuong, gio, thang, nam, ban_menh=None, hanh_nien=None, ngay_tiet=None, gioi=None):
        self.r = r
        self.g, self.z, self.T = r["g"], r["z"], r["T"]
        T = self.T
        self.vt = [0] * 12                       # thiên chi -> địa chi nó đứng trên
        for k, v in T.items():
            self.vt[v] = k
        self.ky = KY[self.g]
        self.u1 = T[self.ky]
        self.u2 = T[self.u1]
        self.u3 = T[self.z]
        self.u4 = T[self.u3]
        self.tren = (self.u1, self.u2, self.u3, self.u4)
        self.duoi = (self.ky, self.u1, self.z, self.u3)
        self.so, self.trung, self.mat = r["truyen"]
        self.tr = (self.so, self.trung, self.mat)
        self.khong = set(r["khong"])
        self.xun = (self.z - self.g) % 12
        self.vi = (self.xun + 9) % 12            # chi cuối tuần (tuần vĩ)
        self.don = {(self.xun + i) % 12: i for i in range(10)}
        self.tuong = r["tuong"]
        self.qn, self.thuan, self.tru = r["qn"], r["thuan"], r["tru"]
        self.qn_tru, self.qn_da = L.QUY_NHAN[self.g]
        self.qn_kia = self.qn_da if self.tru else self.qn_tru
        self.hg, self.hz = HG[self.g], HC[self.z]
        self.nt, self.gio, self.thang, self.nam = tuong, gio, thang, nam
        self.phuc = tuong == gio
        self.phan = (tuong - gio) % 12 == 6
        self.ten = r["ten"]
        self.ht = hanh_truyen(self.tr)            # hành chung của tam truyền (hoặc None)
        self.lt_tr = lt_hanh(self.g, self.ht) if self.ht is not None else None
        self.ss = {}
        for ten, c, _ in than_sat(self.g, self.z, thang, nam):
            self.ss[ten] = c
        self.bm, self.hn, self.gioi = ban_menh, hanh_nien, gioi
        self.nm = []                              # (nhãn, địa chi năm mệnh, thượng thần)
        if ban_menh is not None:
            self.nm.append(("bản mệnh", ban_menh, T[ban_menh]))
        if hanh_nien is not None:
            self.nm.append(("hành niên", hanh_nien, T[hanh_nien]))
        self.ngay_tiet = ngay_tiet
        # đếm khóa hạ tặc thượng / thượng khắc hạ (khóa 1 lấy hành của can, như lucnham.lap)
        self.n_tac = sum(1 for k in r["khoa"] if KHAC(k[1], HC[k[3]]))
        self.n_khac = sum(1 for k in r["khoa"] if KHAC(HC[k[3]], k[1]))

    # tiện ích
    def lt(self, c):
        return LT[self.g][c]

    def kh(self, c):
        return c in self.khong

    def lac(self, c):
        """Lạc không: thần đứng trên địa chi tuần không."""
        return self.vt[c] in self.khong

    def idx(self, c):
        """Thứ tự thiên tướng của thiên chi c tính từ Quý nhân (0 Quý nhân, 1..5 phía trước, 7..11 phía sau)."""
        return ((c - self.qn) if self.thuan else (self.qn - c)) % 12

    def vt_mua(self, h):
        return mua(h, self.thang) in ("Vượng", "Tướng")

    def tu_mua(self, h):
        return mua(h, self.thang) in ("Tù", "Tử")

    def noi(self, c):
        """Chỗ chi c xuất hiện trong khóa truyền / năm mệnh (thiên bàn)."""
        o = ["thượng K%d" % (i + 1) for i, u in enumerate(self.tren) if u == c]
        o += [n for n, t in zip(("Sơ", "Trung", "Mạt"), self.tr) if t == c]
        o += ["trên " + n for n, _, u in self.nm if u == c]
        return o


def C(c):
    return CHI[c]


# ---------------------------------------------------------------- 4. Tất pháp phú
def _p1(c):
    o = []
    for n, x in (("can", c.u1), ("chi", c.u3)):
        if c.so == (x + 1) % 12 and c.mat == (x - 1) % 12:
            o.append("Sơ %s ở trước, Mạt %s ở sau %s thượng %s (dẫn tòng %s)" % (C(c.so), C(c.mat), n, C(x), n))
    return "; ".join(o)


def _p2(c):
    if c.u1 == c.vi and c.u3 == c.xun:
        return "can thượng %s là tuần vĩ, chi thượng %s là tuần thủ" % (C(c.u1), C(c.u3))


def _p3(c):
    o = []
    if c.u1 == c.qn_kia:
        o.append("can thượng")
    o += ["trên " + n for n, _, u in c.nm if u == c.qn_kia]
    if o:
        return "Quý nhân %s (%s) lâm %s" % ("dạ" if c.tru else "trú", C(c.qn_kia), ", ".join(o))


def _hien(c, ten):
    return [x for x in range(12) if c.tuong[x] == ten][0]


def _p4(c):
    h = _hien(c, "Bạch Hổ")
    if c.lt(h) == "Quan quỷ":
        o = (["can thượng"] if c.u1 == h else []) + ["trên " + n for n, _, u in c.nm if u == h]
        if o:
            return "Bạch Hổ cưỡi quỷ %s lâm %s%s" % (C(h), ", ".join(o), " (quỷ tuần không: tin hư)" if c.kh(h) else "")


def _p5(c):
    if c.g % 2 == 0 and all(x % 2 == 0 for x in c.tren + c.tr):
        return "can dương, 4 thượng thần và 3 truyền đều chi dương"


def _p6(c):
    if c.g % 2 == 1 and all(x % 2 == 1 for x in c.tren + c.tr):
        return "can âm, 4 thượng thần và 3 truyền đều chi âm"


def _p7(c):
    if c.u1 == LOC[c.g]:
        return "Lộc %s lâm can" % C(c.u1)


def _p8(c):
    if c.u3 == LOC[c.g]:
        return "Lộc %s lâm chi" % C(c.u3)


def _p9(c):
    if all(c.kh(t) or c.lt(t) in ("Quan quỷ", "Tử tôn") for t in c.tr) and c.lt(c.u1) == "Phụ mẫu" \
            and not c.kh(c.u1):
        return "ba truyền đều không/quỷ/thoát; can thượng %s sinh can" % C(c.u1)


def _p10(c):
    noi = {8, 9} | ({KY[c.g]} if c.g in (6, 7) else set())
    if c.vt[3] in noi and c.kh(3) and c.noi(3):
        return "Mão tuần không gia %s (thế Chước luân), ở %s" % (C(c.vt[3]), ", ".join(c.noi(3)))


def _p11(c):
    if c.lt_tr == "Quan quỷ":
        o = []
        if c.lt(c.u1) == "Tử tôn":
            o.append("can thượng %s là Tử tôn chế quỷ" % C(c.u1))
        if c.kh(c.so) or c.lac(c.so):
            o.append("sơ truyền không/lạc không")
        if o:
            return "tam truyền (cùng hành/hợp cục) là Quan quỷ nhưng " + ", ".join(o)


def _p12(c):
    if KHAC(HC[c.u1], c.hg) and KHAC(c.hz, HC[c.u1]):
        return "can thượng %s khắc can, chi ngày %s khắc lại %s" % (C(c.u1), C(c.z), C(c.u1))


def _p13(c):
    if c.lt_tr == "Quan quỷ" and mua(c.ht, c.thang) == "Vượng":
        return "tam truyền là quỷ (%s), đang vượng theo tháng %s" % (TEN_HANH[c.ht], C(c.thang))


def _p14(c):
    if c.lt_tr == "Thê tài" and c.vt_mua(c.ht):
        return "tam truyền là Thê tài (%s), %s theo tháng" % (TEN_HANH[c.ht], mua(c.ht, c.thang).lower())


def _p15(c):
    tg = c.tuong[c.u1]
    if c.lt(c.u1) == "Tử tôn" and SINH(HC[c.u1], HANH_TUONG[tg]):
        return "can sinh %s, %s lại sinh %s" % (C(c.u1), C(c.u1), tg)


def _p16(c):
    if c.tuong[c.u1] == "Thiên Không":
        if c.kh(c.u1):
            return "can thượng %s tuần không, cưỡi Thiên Không" % C(c.u1)
        if c.lt(c.u1) == "Tử tôn":
            return "can thượng %s là thoát khí, cưỡi Thiên Không (thoát không)" % C(c.u1)


def _p17(c):
    if (c.trung - c.so) % 12 == 1 and (c.mat - c.trung) % 12 == 1 and all(c.kh(t) or c.lac(t) for t in c.tr):
        return "tiến như, ba truyền đều không hoặc lạc không"


def _p18(c):
    if (c.trung - c.so) % 12 == 11 and (c.mat - c.trung) % 12 == 11 and all(c.kh(t) or c.lac(t) for t in c.tr):
        return "thoái như, ba truyền đều không hoặc lạc không"


def _thai(c, ten):
    t = vong(c.hg, THAI)
    if c.lt(t) == "Thê tài" and t == c.ss[ten] and (t in c.tren or t in c.tr):
        return "thai thần %s là Thê tài, trùng %s tháng, có trong khóa truyền" % (C(t), ten)


def _p21(c):
    if hop(c.u1, c.z) and hop(c.u3, c.ky):
        return "can thượng %s hợp chi %s, chi thượng %s hợp can (%s)" % (C(c.u1), C(c.z), C(c.u3), C(c.ky))


def _p22(c):
    if hop(c.ky, c.z) and hop(c.u1, c.u3):
        return "can (%s) hợp chi %s, can thượng %s hợp chi thượng %s" % (C(c.ky), C(c.z), C(c.u1), C(c.u3))
    if hop(c.u1, c.ky) and hop(c.u3, c.z):
        return "can hợp can thượng %s, chi hợp chi thượng %s" % (C(c.u1), C(c.u3))
    if hop(c.ky, c.z) and (c.u1 == c.z or c.u3 == c.ky):   # "干支相会格": 乙酉日酉加乙，或乙加酉 …
        return "can (%s) và chi %s lục hợp, %s" % (C(c.ky), C(c.z), "chi gia lên can" if c.u1 == c.z else
                                                 "can gia lên chi")
    if hop(c.u1, c.u3):          # chú Tất pháp phú: "独支干上神作六合格" (vd 戊辰日干上丑、支上子)
        return "riêng can thượng %s hợp chi thượng %s (độc can chi thượng thần hợp)" % (C(c.u1), C(c.u3))


def _p23(c):
    if c.u1 != c.u3 and c.so == c.u3 and c.mat == c.u1:
        return "sơ truyền là chi thượng %s, mạt truyền về can thượng %s" % (C(c.u3), C(c.u1))


def _p24(c):
    if c.u1 != c.u3 and c.so == c.u1 and c.mat == c.u3:
        return "sơ truyền là can thượng %s, mạt truyền về chi thượng %s" % (C(c.u1), C(c.u3))


def _dinh(c, cans):
    if c.g in cans:
        d = (c.xun + 3) % 12
        o = [n for n, t in zip(("sơ", "trung", "mạt"), c.tr) if t == d]
        o += (["can thượng"] if c.u1 == d else []) + (["chi thượng"] if c.u3 == d else [])
        o += ["trên " + n for n, _, u in c.nm if u == d]
        if o:
            return "Đinh thần %s ở %s" % (C(d), ", ".join(o))


def _p27(c):
    if c.lt_tr == "Thê tài":
        if c.lt(c.u1) == "Quan quỷ":
            return "ba truyền đều tài, sinh quỷ %s ở can thượng" % C(c.u1)
        if c.lt(c.u3) == "Quan quỷ":
            return "ba truyền đều tài, sinh quỷ %s ở chi thượng (hại nhà)" % C(c.u3)


def _p29(c):
    if c.ht is not None and SINH(c.ht, c.hg) and SINH(c.hz, c.ht):
        return "tam truyền (%s) sinh can mà tiết khí chi" % TEN_HANH[c.ht]


def _p30(c):
    if c.ht is not None and SINH(c.hg, c.ht) and SINH(c.ht, c.hz):
        return "tam truyền (%s) tiết khí can mà sinh chi" % TEN_HANH[c.ht]


def _p31(c):
    s, t, m = (HC[x] for x in c.tr)
    if SINH(s, t) and SINH(t, m) and SINH(m, c.hg):
        return "sơ sinh trung, trung sinh mạt, mạt sinh can"
    if SINH(m, t) and SINH(t, s) and SINH(s, c.hg):
        return "mạt sinh trung, trung sinh sơ, sơ sinh can"


def _p32(c):
    s, t, m = (HC[x] for x in c.tr)
    if KHAC(s, t) and KHAC(t, m) and KHAC(m, c.hg):
        return "sơ khắc trung, trung khắc mạt, mạt khắc can"
    if KHAC(m, t) and KHAC(t, s) and KHAC(s, c.hg):
        return "mạt khắc trung, trung khắc sơ, sơ khắc can"


def _p33(c):
    ts, mo = vong(c.hg, SINH_), vong(c.hg, MO)
    if c.so == ts and c.mat == mo:
        return "sơ là trường sinh %s, mạt là mộ %s của can (có đầu không đuôi)" % (C(ts), C(mo))
    if c.so == mo and c.mat == ts:
        return "sơ là mộ %s, mạt là trường sinh %s của can (trước khó sau dễ)" % (C(mo), C(ts))


def _p35(c):
    if SINH(c.hg, HC[c.u1]) and SINH(c.hz, HC[c.u3]):
        return "can sinh can thượng, chi sinh chi thượng (cả hai bị thoát)"
    if SINH(c.hz, HC[c.u1]) and SINH(c.hg, HC[c.u3]):
        return "can thượng thoát chi, chi thượng thoát can"


def _p36(c):
    if c.u1 == vong(c.hg, BAI) and c.u3 == vong(c.hz, BAI):
        return "can thượng %s, chi thượng %s đều là Bại (Mộc dục)" % (C(c.u1), C(c.u3))


def _p37(c):
    s, m = HC[c.so], HC[c.mat]
    if c.so != c.mat and SINH(m, s):
        if SINH(s, c.hg):
            return "mạt %s sinh sơ %s, sơ sinh can" % (C(c.mat), C(c.so))
        if KHAC(s, c.hg):
            return "mạt %s sinh sơ %s, sơ khắc can (cần năm mệnh chế mạt)" % (C(c.mat), C(c.so))
        if KHAC(c.hg, s):
            return "mạt %s sinh sơ %s, sơ là tài" % (C(c.mat), C(c.so))


def _p38(c):
    if c.so == c.vi and c.vt[c.vi] == c.xun:
        return "tuần vĩ %s gia tuần thủ %s phát dụng" % (C(c.vi), C(c.xun))
    if c.so == c.xun and c.tuong[c.xun] == "Huyền Vũ":
        return "tuần thủ %s cưỡi Huyền Vũ phát dụng" % C(c.xun)
    if c.so == c.T[c.xun] and c.tuong[c.so] == "Huyền Vũ":
        return "thần trên tuần thủ (%s) cưỡi Huyền Vũ phát dụng" % C(c.so)


def _p39(c):
    if c.tuong[c.nt] == "Huyền Vũ":
        return "Huyền Vũ cưỡi nguyệt tướng %s" % C(c.nt)


def _p40(c):
    if {c.tuong[c.u1], c.tuong[c.u3]} == {"Thiên Hậu", "Lục Hợp"}:
        return "can thượng %s, chi thượng %s" % (c.tuong[c.u1], c.tuong[c.u3])


def _p41(c):
    if c.u1 == L.DICH_MA[c.z] and c.u3 == LOC[c.g]:
        return "can thượng là Mã %s của chi, chi thượng là Lộc %s của can" % (C(c.u1), C(c.u3))


def _p42(c):
    d = [c.don.get(t) for t in c.tr]
    if None not in d and set(d) in ({0, 4, 6}, {1, 2, 3}):
        return "độn can ba truyền: " + " ".join(CAN[x] for x in d)


def _p43(c):
    o = []
    for q in (c.qn,):                      # chi đang cưỡi thiên tướng Quý nhân
        if q in c.tren or q in c.tr:
            d = c.vt[q]
            if KHAC(HC[d], HC[q]):
                o.append("Quý nhân %s bị địa bàn %s khắc" % (C(q), C(d)))
            elif hai(d, q):
                o.append("Quý nhân %s bị địa bàn %s hại" % (C(q), C(d)))
    return "; ".join(o)


def _p44(c):
    q = {c.qn_tru, c.qn_da}
    n = sum(1 for x in c.tren if x in q)
    if q <= set(c.tren) and n >= 3:
        return "%d/4 thượng thần là Quý nhân, có cả trú lẫn dạ" % n


def _p45(c):
    sau = set(c.tr) | {c.u1, c.u3} | {u for _, _, u in c.nm}
    for a, b in ((c.qn_tru, c.qn_da), (c.qn_da, c.qn_tru)):
        if c.vt[a] == b and a in sau:
            return "Quý nhân %s gia lên Quý nhân %s, có trong sáu chỗ (can, chi, 3 truyền, năm mệnh)" % (C(a), C(b))


def _p46(c):
    if c.vt[c.qn_tru] in (9, 10, 11, 0, 1, 2) and c.vt[c.qn_da] in (3, 4, 5, 6, 7, 8):
        return "Quý nhân trú %s lâm đất đêm %s, Quý nhân dạ %s lâm đất ngày %s" % (
            C(c.qn_tru), C(c.vt[c.qn_tru]), C(c.qn_da), C(c.vt[c.qn_da]))


def _p47(c):
    d = c.vt[c.qn]
    if d in (4, 10):
        if c.g in (1, 7) and d == c.ky:
            return "Quý nhân %s lâm %s là cung của can %s – quý nhân lâm thân" % (C(c.qn), C(d), CAN[c.g])
        if d == c.z:                 # chú: "如辰戌二日占之，乃为贵人入宅，非坐狱论也"
            return "Quý nhân %s lâm %s là chi ngày – quý nhân nhập trạch, không luận ngục" % (C(c.qn), C(d))
        return "Quý nhân %s lâm %s (nhập ngục)" % (C(c.qn), C(d))


def _p48(c):
    if c.tuong[c.u1] == "Quý Nhân" and c.lt(c.u1) == "Quan quỷ":
        return "can thượng %s là quỷ nhưng cưỡi Quý nhân" % C(c.u1)


def _p49(c):
    if KHAC(HC[c.vt[c.qn_tru]], HC[c.qn_tru]) and KHAC(HC[c.vt[c.qn_da]], HC[c.qn_da]):
        return "Quý nhân trú %s và dạ %s đều đứng trên đất khắc mình" % (C(c.qn_tru), C(c.qn_da))


def _p50(c):
    if all(c.kh(q) or c.lac(q) for q in (c.qn_tru, c.qn_da)):
        return "hai Quý nhân %s, %s đều không vong hoặc lạc không" % (C(c.qn_tru), C(c.qn_da))


def _p51(c):
    if c.so == 10 and c.vt[10] == 11:
        return "Tuất gia Hợi phát dụng"


def _p52(c):
    if c.T[2] == 4:
        return "Thìn gia Dần"


def _p53(c):
    if c.g == 2 and c.z == 10 and c.T[5] == 10 and c.tuong[10] == "Đằng Xà":
        return "ngày Bính Tuất, Tuất gia Tỵ cưỡi Đằng Xà"


def _p54(c):
    if c.ten.startswith("Mão tinh") and c.g % 2 == 0:
        h = _hien(c, "Bạch Hổ")
        if c.noi(h):
            return "Hổ thị (Mão tinh ngày dương), Bạch Hổ cưỡi %s ở %s" % (C(h), ", ".join(c.noi(h)))


def _p55(c):
    if c.u1 == (c.ky + 1) % 12 and c.u3 == (c.z + 1) % 12:
        return "can thượng %s là thần trước can, chi thượng %s là thần trước chi" % (C(c.u1), C(c.u3))


def _p56(c):
    mo = vong(c.hg, MO)
    if c.u1 == mo and c.bm == mo:
        return "mộ %s phủ can, người hỏi lại tuổi %s" % (C(mo), C(mo))


def _p57(c):
    sinh = [x for x, h in ((c.u1, c.hg), (c.u3, c.hz)) if SINH(HC[x], h)]
    tai = [t for t in c.tr if c.lt(t) == "Thê tài"]
    if sinh and all(c.kh(x) for x in sinh) and tai and all(c.kh(t) or c.lac(t) for t in tai):
        return "thần sinh can/chi (%s) tuần không; tài trong truyền (%s) cũng không" % (
            " ".join(C(x) for x in sinh), " ".join(C(t) for t in tai))


def _p59(c):
    mo = vong(c.hg, MO)
    if c.u1 == mo and c.u1 == (TH_DAU[c.z % 4] + 8) % 12 and c.so == mo:
        return "Hoa Cái của chi là mộ %s của can, lâm can phát dụng" % C(mo)


def _p60(c):
    if c.u3 == vong(c.hz, MO) and c.u3 == c.nt:
        return "mộ %s của chi lâm chi, lại là nguyệt tướng" % C(c.u3)


def _p61(c):
    if c.u1 == vong(c.hg, MO) and c.tuong[c.u1] == "Bạch Hổ":
        return "can thượng là mộ %s của can, cưỡi Bạch Hổ" % C(c.u1)


def _p62(c):
    if c.u3 in (vong(c.hg, MO), vong(c.hz, MO)) and c.tuong[c.u3] == "Bạch Hổ":
        return "chi thượng là mộ %s, cưỡi Bạch Hổ" % C(c.u3)


def _p63(c):
    if KHAC(HC[c.u1], c.hg) and KHAC(HC[c.u3], c.hz):
        return "can thượng %s khắc can, chi thượng %s khắc chi" % (C(c.u1), C(c.u3))


def _p64(c):
    if KHAC(HC[c.u3], c.hg) and KHAC(HC[c.u1], c.hz):
        return "chi thượng %s khắc can, can thượng %s khắc chi" % (C(c.u3), C(c.u1))


def _p65(c):
    mo = vong(c.hg, MO)
    quan = [1, 4, 7, 10][((c.thang - 2) % 12) // 3]
    if c.so == mo == quan:
        o = "; phát từ bên can (ứng người)" if c.so in (c.u1, c.u2) else (
            "; phát từ bên chi (ứng nhà)" if c.so in (c.u3, c.u4) else "")
        return "sơ truyền %s vừa là mộ của can vừa là quan thần của mùa%s" % (C(c.so), o)


def _p66(c):
    mo = vong(c.hz, MO)
    if mo != c.z and c.lt(mo) == "Thê tài" and (c.u3 == mo or c.so == mo):
        return "mộ %s của chi là tài của can, %s" % (C(mo), "lâm chi" if c.u3 == mo else "phát dụng")


def _p69(c):
    h = _hien(c, "Bạch Hổ")
    d = c.don.get(h)
    if d is not None and KHAC(HG[d], c.hg) and c.noi(h):
        return "Bạch Hổ cưỡi %s (độn %s khắc can) ở %s" % (C(h), CAN[d], ", ".join(c.noi(h)))


def _p70(c):
    if c.lt(c.u3) == "Quan quỷ" and c.lt(c.u4) == "Quan quỷ":
        return "thượng khóa 3 (%s) và khóa 4 (%s) đều là quỷ" % (C(c.u3), C(c.u4))


def _p71(c):
    bp = (c.nam - 1) % 12
    if c.u3 == bp and KHAC(HC[bp], c.hz):
        return "Bệnh phù %s lâm chi và khắc chi" % C(bp)


def _p72(c):
    if {(c.nam + 2) % 12, (c.nam - 2) % 12} <= {c.u1, c.u3}:
        return "Tang môn %s và Điếu khách %s ở can thượng/chi thượng" % (C((c.nam + 2) % 12), C((c.nam - 2) % 12))


def _p73(c):
    if all(c.kh(t) or c.lac(t) for t in c.tr) and all(c.lt(x) in ("Quan quỷ", "Tử tôn") for x in (c.u1, c.u3)):
        return "ba truyền đều không/lạc không, can thượng và chi thượng đều quỷ hoặc thoát"


def _p74(c):
    n = sum(1 for t in c.tr if c.kh(t) or c.lac(t))
    if n == 3:
        return "ba truyền đều tuần không hoặc lạc không"
    if n == 2 and tam_hop(c.tr) is not None:
        t = [x for x in c.tr if not (c.kh(x) or c.lac(x))][0]
        if c.tuong[t] == "Thiên Không":
            return "tam hợp hai truyền không, truyền còn lại %s cưỡi Thiên Không" % C(t)


def _p75(c):
    if c.u1 == c.u3 and c.u1 in (4, 6, 9, 11):
        return "can thượng và chi thượng cùng là %s (tự hình)" % C(c.u1)
    if {c.u1, c.u3} == {0, 3}:
        return "can thượng/chi thượng là Tý – Mão (vô lễ hình)"
    if set(c.tr) in ({2, 5, 8}, {1, 10, 7}):
        return "ba truyền đủ bộ tam hình " + " ".join(C(t) for t in c.tr)


def _p76(c):
    if hai(c.u1, c.u3):
        return "can thượng %s và chi thượng %s lục hại" % (C(c.u1), C(c.u3))
    if hai(c.u1, c.ky) and hai(c.u3, c.z):
        return "can với can thượng, chi với chi thượng đều lục hại"


def _p77(c):
    if SINH(HC[c.u1], c.hz) and SINH(HC[c.u3], c.hg):
        return "hỗ sinh: can thượng %s sinh chi, chi thượng %s sinh can" % (C(c.u1), C(c.u3))
    if SINH(HC[c.u1], c.hg) and SINH(HC[c.u3], c.hz):
        return "câu sinh: can thượng %s sinh can, chi thượng %s sinh chi" % (C(c.u1), C(c.u3))


def _p78(c):
    if c.u1 == vong(c.hz, VUONG) and c.u3 == vong(c.hg, VUONG):
        return "hỗ vượng: can thượng %s là vượng của chi, chi thượng %s là vượng của can" % (C(c.u1), C(c.u3))
    if c.u1 == vong(c.hg, VUONG) and c.u3 == vong(c.hz, VUONG):
        return "giai vượng: can thượng %s vượng của can, chi thượng %s vượng của chi" % (C(c.u1), C(c.u3))


def _p79(c):
    if c.u1 == vong(c.hg, TUYET) and c.u3 == vong(c.hz, TUYET):
        return "can thượng %s, chi thượng %s đều là Tuyệt" % (C(c.u1), C(c.u3))


def _p80(c):
    if c.u1 == vong(c.hz, TU) and c.u3 == vong(c.hg, TU):
        return "hỗ thừa tử khí: can thượng %s là Tử của chi, chi thượng %s là Tử của can" % (C(c.u1), C(c.u3))
    if c.u1 == vong(c.hg, TU) and c.u3 == vong(c.hz, TU):
        return "can thượng %s, chi thượng %s đều là Tử" % (C(c.u1), C(c.u3))


def _p81(c):
    if c.trung == vong(HC[c.so], MO) and c.trung != c.so:
        return "sơ %s bị trung %s mộ%s" % (C(c.so), C(c.trung), "; mạt %s là mộ của can" % C(c.mat)
                                         if c.mat == vong(c.hg, MO) else "")


def _p82(c):
    if not c.kh(c.so) and c.kh(c.trung) and c.kh(c.mat):
        return "sơ %s thực, trung %s và mạt %s đều không" % (C(c.so), C(c.trung), C(c.mat))


def _p83(c):
    d = tam_hop(c.tr)
    if d is not None:
        giua = (d + 4) % 12
        x = [n for n, u in (("can thượng", c.u1), ("chi thượng", c.u3)) if hop(u, giua)]
        if x:
            return "tam truyền tam hợp, %s lục hợp với %s" % (" và ".join(x), C(giua))


def _p84(c):
    if tam_hop(c.tr) is not None:
        for n, u in (("can thượng", c.u1), ("chi thượng", c.u3)):
            for t in c.tr:
                for ten, f in (("xung", xung), ("hại", hai), ("hình", hinh)):
                    if f(u, t):
                        return "tam truyền tam hợp, %s %s %s %s" % (n, C(u), ten, C(t))


def _p85(c):
    tg = c.tuong[c.so]
    if KHAC(HC[c.vt[c.so]], HC[c.so]) and KHAC(HANH_TUONG[tg], HC[c.so]):
        return "sơ %s bị địa bàn %s khắc và bị %s khắc" % (C(c.so), C(c.vt[c.so]), tg)


def _p86(c):
    tg = c.tuong[c.so]
    if KHAC(HC[c.vt[c.so]], HC[c.so]) and KHAC(HC[c.so], HANH_TUONG[tg]):
        return "địa bàn %s khắc sơ %s, %s khắc tướng %s" % (C(c.vt[c.so]), C(c.so), C(c.so), tg)


def _p87(c):
    if c.vt[c.ky] == vong(c.hg, MO) and c.vt[c.z] == vong(c.hz, MO):
        return "thiên bàn %s (can) ngồi trên mộ %s, %s (chi) ngồi trên mộ %s" % (
            C(c.ky), C(c.vt[c.ky]), C(c.z), C(c.vt[c.z]))


def _p88(c):
    mg, mz = vong(c.hg, MO), vong(c.hz, MO)
    if c.u1 == mg and c.u3 == mz:
        return "can thượng %s là mộ can, chi thượng %s là mộ chi" % (C(c.u1), C(c.u3))
    if mg != mz and c.u1 == mz and c.u3 == mg:
        return "can thượng %s là mộ chi, chi thượng %s là mộ can (giao nhau)" % (C(c.u1), C(c.u3))


def _p89(c):
    if c.phuc:
        o = []
        for ten in ("Lục Đinh", "Dịch Mã", "Thiên Mã"):
            x = c.ss[ten]
            if x in c.tr or x in (c.u1, c.u3) or x in [u for _, _, u in c.nm]:
                o.append("%s %s" % (ten, C(x)))
        if o:
            return "Phục ngâm có " + ", ".join(o)


def _p90(c):
    if c.phan and all(c.kh(t) or c.lac(t) for t in c.tr):
        return "Phản ngâm, ba truyền đều không hoặc lạc không"


def _p91(c):
    if c.lt(c.u1) == "Quan quỷ" and c.tuong[c.u1] == "Bạch Hổ":
        return "can thượng %s là quỷ cưỡi Bạch Hổ" % C(c.u1)


def _p92(c):
    lg = _hien(c, "Thanh Long")
    if c.lt(lg) == "Phụ mẫu" and lg == c.ss["Sinh Khí"]:
        return "Thanh Long cưỡi %s sinh can, lại là Sinh khí tháng%s" % (
            C(lg), (" (ở " + ", ".join(c.noi(lg)) + ")") if c.noi(lg) else "")


# (số, tên Hán Việt, ý nghĩa ngắn – lời mình, hàm kiểm)
TAT_PHAP = [
    (1, "Tiền hậu dẫn tòng thăng thiên cát", "được dẫn trước đỡ sau: lợi thăng tiến (bên can), lợi dời chỗ ở (bên chi)", _p1),
    (2, "Thủ vĩ tương kiến thủy chung nghi", "đầu đuôi gặp nhau: việc có trước có sau, theo đuổi được", _p2),
    (3, "Liêm mạc quý nhân cao giáp đệ", "quý nhân 'sau rèm': tốt cho thi cử, được người có chức nâng đỡ", _p3),
    (4, "Thôi quan sứ giả phó quan kỳ", "quỷ cưỡi Hổ giục quan: người có chức sớm nhận việc; người thường nên giữ sức", _p4),
    (5, "Lục dương số túc tu công dụng", "toàn dương: lợi việc công khai, việc chung; kém việc riêng tư", _p5),
    (6, "Lục âm tương kế tận hôn mê", "toàn âm: lợi việc kín, việc riêng; việc công dễ mờ mịt", _p6),
    (7, "Vượng lộc lâm thân đồ vọng tác", "lộc ở ngay thân: nên giữ cái đang có, đừng bỏ đi tìm cái khác", _p7),
    (8, "Quyền nhiếp bất chính lộc lâm chi", "lộc nằm bên nhà người: nhận việc tạm/kiêm nhiệm, phải chịu nhún", _p8),
    (9, "Tị nạn đào sinh tu khí cựu", "ba truyền không giúp, chỉ can thượng giúp: bỏ lối cũ, dựa vào chỗ đang có", _p9),
    (10, "Hủ mộc nan điêu biệt tác vi", "gỗ mục khó đẽo: nên đổi nghề/đổi hướng", _p10),
    (11, "Chúng quỷ tuy chương toàn bất úy", "quỷ nhiều nhưng có chế/không lực: lo nhưng khó thành hại", _p11),
    (12, "Tuy ưu hồ giả hổ uy nghi", "bị khắc nhưng có chỗ dựa che chắn (chi chế quỷ)", _p12),
    (13, "Quỷ tặc đương thời vô úy kỵ", "quỷ đang vượng nên tạm chưa hại; phòng khi sang mùa khác", _p13),
    (14, "Truyền tài thái vượng phản tài khuy", "tài quá vượng lại khó cầm: đợi lúc tài dịu mới lấy được", _p14),
    (15, "Thoát thượng phùng thoát phòng hư trá", "bị tiết hai lớp: phòng hao tốn, lời hứa không thật", _p15),
    (16, "Không thượng thừa không sự mạc truy", "chỗ của mình trống rỗng: tin đồn, việc không có thực", _p16),
    (17, "Tiến như không vong nghi thoái bộ", "tiến lên gặp trống: nên lùi giữ, dựa vào can chi", _p17),
    (18, "Đạp cước không vong tiến dụng nghi", "lùi lại gặp trống: nên tiến hơn là lùi", _p18),
    (19, "Thai tài sinh khí thê hoài dựng", "dấu hiệu có tin thai (với người hỏi về thai)", lambda c: _thai(c, "Sinh Khí")),
    (20, "Thai tài tử khí tổn thai suy", "thai cần giữ gìn kỹ (chỉ xét khi hỏi về thai)", lambda c: _thai(c, "Tử Khí")),
    (21, "Giao xa tương hợp giao quan lợi", "hai bên đan chéo hợp nhau: lợi giao dịch, hợp tác", _p21),
    (22, "Thượng hạ giai hợp lưỡng tâm tề", "trên dưới đều hợp: hai bên đồng lòng", _p22),
    (23, "Bỉ cầu ngã sự chi truyền can", "việc từ bên kia tìm đến mình (người ta nhờ mình)", _p23),
    (24, "Ngã cầu bỉ sự can truyền chi", "mình phải đi cầu người, việc hơi gượng", _p24),
    (25, "Kim nhật phùng Đinh hung họa động", "ngày Kim gặp Đinh: có biến động; người có chức thì sớm có lệnh", lambda c: _dinh(c, (6, 7))),
    (26, "Thủy nhật phùng Đinh tài động chi", "ngày Thủy gặp Đinh: tiền bạc chuyển động, tài từ xa", lambda c: _dinh(c, (8, 9))),
    (27, "Truyền tài hóa quỷ tài hưu mịch", "cầu tài sinh rắc rối: thận trọng với tiền", _p27),
    (29, "Quyến thuộc phong doanh cư hiệp trạch", "người đông mà nhà chật; chưa nên dời", _p29),
    (30, "Ốc trạch khoan quảng trí nhân suy", "nhà rộng mà người hao: nên tính chỗ ở hợp hơn", _p30),
    (31, "Tam truyền đệ sinh nhân cử tiến", "có người tiến cử, nâng đỡ từng bước", _p31),
    (32, "Tam truyền hỗ khắc chúng nhân khi", "bị chèn ép dây chuyền; nên tìm đồng minh", _p32),
    (33, "Hữu thủy vô chung nan biến dịch", "đầu tốt cuối kém, hoặc trước khó sau dễ (xem chiều)", _p33),
    (35, "Nhân trạch thụ thoát câu chiêu đạo", "người và nhà bị tiết: phòng hao, phòng mất đồ", _p35),
    (36, "Can chi giai bại sự khuynh đồi", "người và nhà đều kém sức: nên củng cố trước", _p36),
    (37, "Mạt trợ sơ hề tam đẳng luận", "mạt giúp sơ: kết cục bổ cho khởi đầu (tốt/xấu tùy sơ)", _p37),
    (38, "Bế khẩu quái thể lưỡng ban suy", "khóa 'ngậm miệng': việc khó nói ra, khó dò; tìm người/vật khó", _p38),
    (39, "Thái dương chiếu Vũ nghi cầm tặc", "mặt trời rọi Huyền Vũ: việc gian dễ lộ, dễ tìm ra", _p39),
    (40, "Hậu Hợp chiêm hôn khởi dụng môi", "hôn nhân đã có tình riêng từ trước, không cần mối", _p40),
    (41, "Phú quý can chi phùng lộc mã", "lộc mã đủ: người có chức được thăng; người thường thì động, đi lại nhiều", _p41),
    (42, "Tôn sùng truyền nội ngộ tam kỳ", "tam kỳ trong truyền: được tôn trọng, gặp quý nhân", _p42),
    (43, "Hại quý tụng trực tác khúc đoán", "quý nhân bị khắc/hại: nhờ người trên dễ hỏng việc, kiện có lý vẫn thiệt", _p43),
    (44, "Khóa truyền câu quý chuyển vô y", "quý nhân quá nhiều: không biết dựa ai, việc không quy về một mối", _p44),
    (45, "Trú dạ quý gia cầu lưỡng quý", "hai quý nhân chồng nhau: việc phải qua hai người có quyền", _p45),
    (46, "Quý nhân sai điệt sự sâm si", "quý nhân lệch chỗ: việc nhờ cậy không đều, lộn xộn", _p46),
    (47, "Quý tuy tại ngục nghi lâm can", "quý nhân bị giam (Thìn/Tuất): khó nhờ; trừ khi lâm đúng cung can (lâm thân) hoặc chi ngày (nhập trạch)",
     _p47),
    (48, "Quỷ thừa Thiên Ất nãi thần kỳ", "quỷ cưỡi quý nhân: không phải người hại, thường là việc tâm linh/tín ngưỡng", _p48),
    (49, "Lưỡng quý thụ khắc nan can quý", "cả hai quý nhân đều bị khắc: chưa nên nhờ người trên", _p49),
    (50, "Nhị quý giai không hư hỷ kỳ", "quý nhân rỗng: lời hứa dễ đổi, tin vui chưa chắc", _p50),
    (51, "Khôi độ thiên môn quan cách định", "Tuất qua cửa trời: việc bị ngăn cách, khó thông", _p51),
    (52, "Cương tắc quỷ hộ nhậm mưu vi", "Thìn chặn cửa quỷ: mưu việc thuận, ít bị quấy", _p52),
    (53, "Lưỡng xà giáp mộ hung nan miễn", "hai Xà kẹp mộ: việc u uất; bệnh nên khám kỹ", _p53),
    (54, "Hổ thị phùng hổ lực nan thi", "Hổ thị lại gặp Bạch Hổ: có sức mà khó dùng", _p54),
    (55, "Sở mưu đa chuyết phùng võng la", "thiên la địa võng: việc vướng víu, khó thoát", _p55),
    (56, "Thiên võng tự khỏa kỷ chiêu phi", "tự mình chuốc rắc rối, không do người", _p56),
    (57, "Phí hữu dư nhi đắc bất túc", "bỏ ra nhiều thu về ít", _p57),
    (59, "Hoa Cái phúc nhật nhân hôn hối", "bị che lấp: tâm trí mờ, khó trình bày, oan khó giải", _p59),
    (60, "Thái dương xạ trạch ốc quang huy", "nhà được chiếu sáng: nhà sáng sủa, có người trên ghé", _p60),
    (61, "Can thừa mộ hổ vô chiêm bệnh", "hỏi bệnh thì nên khám chữa sớm, thận trọng; đề phòng người có ý xấu", _p61),
    (62, "Chi thừa mộ hổ hữu phục thi", "nhà có điều u ám cũ; nên dọn dẹp, sửa sang", _p62),
    (63, "Bỉ thử toàn thương phòng lưỡng tổn", "hai bên cùng thiệt; kiện thì cả hai đều tổn", _p63),
    (64, "Phu phụ vu dâm các hữu tư", "hai bên đều có ý riêng, khó đồng lòng", _p64),
    (65, "Can mộ tịnh quan nhân trạch phế", "bị đóng chặn: người suy hoặc nhà sa sút, việc tắc", _p65),
    (66, "Chi phần tài tịnh lữ trình kê", "tài nằm trong mộ: buôn bán chậm, đi đường trễ", _p66),
    (69, "Hổ thừa độn quỷ ương phi thiển", "Bạch Hổ mang quỷ ẩn: có rủi ro ngầm, nên phòng kỹ", _p69),
    (70, "Quỷ lâm tam tứ tụng tai tùy", "quỷ ở bên nhà: kiện tụng, bệnh dễ nối nhau; nên làm phúc, giữ hòa", _p70),
    (71, "Bệnh phù khắc trạch toàn gia hoạn", "nhà dễ có người ốm; chú ý vệ sinh, sức khỏe chung", _p71),
    (72, "Tang điếu toàn phùng quải cảo y", "dấu hiệu hiếu sự trong họ (chỉ để lưu ý, xem thêm năm mệnh)", _p72),
    (73, "Tiền hậu bức bách nan tiến thoái", "tiến không được lùi cũng khó: chưa nên động", _p73),
    (74, "Không không như dã sự hưu truy", "toàn rỗng: việc không có thực, đừng đuổi theo", _p74),
    (75, "Tân chủ bất đầu hình tại thượng", "khách chủ không hợp, mỗi bên một ý", _p75),
    (76, "Bỉ thử sai kỵ hại tương tùy", "hai bên nghi kỵ nhau", _p76),
    (77, "Hỗ sinh câu sinh phàm sự ích", "hai bên sinh nhau: mọi việc có lợi", _p77),
    (78, "Hỗ vượng giai vượng tọa mưu nghi", "cả hai đều vượng: ngồi yên mà mưu thì lợi, không cần chạy", _p78),
    (79, "Can chi trị tuyệt phàm mưu quyết", "đến chỗ tuyệt: nên kết thúc việc cũ, dứt điểm", _p79),
    (80, "Nhân trạch giai tử các suy luy", "người và nhà đều yếu: chưa nên khởi việc lớn", _p80),
    (81, "Truyền mộ nhập mộ phân tăng ái", "sơ bị trung chôn: sơ là điều tốt thì tiếc, là điều xấu thì mừng", _p81),
    (82, "Bất hành truyền giả khảo sơ thời", "trung mạt rỗng: chỉ xét sơ truyền", _p82),
    (83, "Vạn sự hỷ hân tam lục hợp", "tam hợp lại thêm lục hợp: việc vui, hòa thuận", _p83),
    (84, "Hợp trung phạm sát mật trung phê", "trong hợp có phá: ngoài ngọt trong ngầm, phòng bị lừa", _p84),
    (85, "Sơ tao giáp khắc bất do kỷ", "sơ bị kẹp khắc: thân không tự chủ, bị người sai khiến", _p85),
    (86, "Tướng phùng nội chiến sở mưu nguy", "nội chiến ở phát dụng: việc sắp thành dễ bị phá ngang", _p86),
    (87, "Nhân trạch tọa mộ cam chiêu hối", "tự chọn chỗ tối: tự chuốc u ám, đừng trách người", _p87),
    (88, "Can chi thừa mộ các hôn mê", "người và nhà như trong sương: chưa nhìn rõ việc", _p88),
    (89, "Nhậm tín Đinh mã tu ngôn động", "Phục ngâm mà có Đinh/Mã: trong tĩnh muốn động, sắp có đi lại", _p89),
    (90, "Lai khứ câu không khởi động nghi", "Phản ngâm mà truyền rỗng: muốn động nhưng thật ra không động", _p90),
    (91, "Hổ lâm can quỷ hung tốc tốc", "việc xấu đến nhanh: cần xử lý sớm", _p91),
    (92, "Long gia sinh khí cát trì trì", "điều tốt đến chậm mà chắc", _p92),
]


def tat_phap(c):
    """Danh sách (số, tên, điều kiện khớp, ý nghĩa) các điều Tất pháp phú khớp với khóa."""
    out = []
    for so, ten, y, f in TAT_PHAP:
        d = f(c)
        if d:
            out.append((so, ten, d, y))
    return out


# ---------------------------------------------------------------- 6. khóa cách ngoài Cửu tông
def _k_tam_quang(c):
    if all(c.vt_mua(h) and c.tuong[x] in CAT_TUONG for h, x in ((c.hg, c.u1), (c.hz, c.u3), (HC[c.so], c.so))):
        return "can, chi, sơ truyền đều vượng/tướng và đều cưỡi cát tướng"


def _k_tam_duong(c):
    if c.thuan and all(1 <= c.idx(x) <= 5 for x in (c.u1, c.u3)) and all(
            c.vt_mua(h) for h in (c.hg, c.hz, HC[c.so])):
        return "Quý nhân thuận, can chi ở trước Quý nhân, can chi và sơ truyền vượng/tướng"


def _k_tam_am(c):
    if not c.thuan and all(7 <= c.idx(x) <= 11 for x in (c.u1, c.u3)) and c.tu_mua(HC[c.so]) \
            and c.tuong[c.so] in ("Huyền Vũ", "Bạch Hổ"):
        return "Quý nhân nghịch, can chi ở sau Quý nhân, sơ truyền tù/tử cưỡi %s" % c.tuong[c.so]


def _k_quan_tuoc(c):
    ma = {L.DICH_MA[c.nam]: "mã năm", L.DICH_MA[c.thang]: "mã tháng"}
    for n, x, _ in c.nm:
        ma.setdefault(L.DICH_MA[x], "mã " + n)
    if c.so in ma and 10 in c.tr and any(c.tuong[t] == "Thái Thường" for t in c.tr):
        return "sơ truyền là %s, trong truyền có Tuất và Thái Thường" % ma[c.so]


def _k_phu_quy(c):
    nm = [u for _, _, u in c.nm]
    if c.tuong[c.so] == "Quý Nhân" and c.vt_mua(HC[c.so]) and (
            SINH(HC[c.vt[c.so]], HC[c.so]) or SINH(HC[c.so], HC[c.vt[c.so]])) and c.so in [c.u1, c.u3] + nm:
        return "Quý nhân vượng tướng phát dụng, trên dưới tương sinh, lâm can/chi/năm mệnh"


def _k_chuoc_luan(c):
    noi = {8, 9} | ({KY[c.g]} if c.g in (6, 7) else set())
    if c.so == 3 and c.vt[3] in noi:
        return "Mão gia %s phát dụng" % C(c.vt[3])


def _k_hanh_thong(c):
    a = _p31(c)
    if a:
        return a
    if SINH(HC[c.u1], c.hz) and SINH(HC[c.u3], c.hg):
        return "can chi hỗ sinh"


def _k_tram_quan(c):
    if c.so in (4, 10) and c.so in (c.u1, c.u3):
        return "%s lâm %s phát dụng" % (C(c.so), "can" if c.so == c.u1 else "chi")


def _k_du_tu(c):
    if all(t in QUY_ for t in c.tr):
        o = [ten for ten in ("Thiên Mã", "Lục Đinh") if c.ss[ten] in c.tr]
        if o:
            return "ba truyền đều Thổ (tứ quý), trong truyền có " + ", ".join(o)


def _k_tam_giao(c):
    if c.z in TRONG and c.u3 in TRONG and all(t in TRONG for t in c.tr) and c.tuong[c.so] in ("Thái Âm", "Lục Hợp"):
        return "ngày trọng, chi thượng trọng, ba truyền đều trọng, sơ cưỡi " + c.tuong[c.so]


def _k_loan_thu(c):
    if KHAC(c.hz, c.hg):
        if c.u3 == c.ky:
            return "can gia lên chi, bị chi khắc (tự chuốc loạn)"
        if c.u1 == c.z:
            return "chi gia lên can mà khắc can (loạn đến tận cửa)"


def _k_chue_te(c):
    if KHAC(c.hg, c.hz):
        if c.u3 == c.ky:
            return "can gia lên chi, can khắc chi"
        if c.u1 == c.z:
            return "chi gia lên can, can khắc chi"


def _k_dam_dat(c):
    if c.so in (3, 9) and {c.tuong[c.so], c.tuong[c.mat]} == {"Lục Hợp", "Thiên Hậu"}:
        return "Mão/Dậu phát dụng, sơ và mạt cưỡi Lục Hợp, Thiên Hậu"


def _k_vu_dam(c):
    if len(set(zip(c.duoi, c.tren))) == 3:
        return "bốn khóa chỉ có ba (bất bị)"
    if KHAC(HC[c.u1], c.hz) and KHAC(HC[c.u3], c.hg):
        return "can thượng khắc chi, chi thượng khắc can"


def _k_co_qua(c):
    if c.kh(c.so) and c.kh(c.mat):
        return "sơ truyền (cô thần) và mạt truyền (quả tú) đều không vong"


def _k_do_ach(c):
    if c.n_khac == 3:
        return "ba khóa thượng khắc hạ (ấu độ ách)"
    if c.n_tac == 3:
        return "ba khóa hạ tặc thượng (trưởng độ ách)"


def _k_truan_phuc(c):
    if c.tu_mua(HC[c.so]) and c.tuong[c.so] not in CAT_TUONG and c.vt_mua(HC[c.mat]) \
            and c.tuong[c.mat] in CAT_TUONG:
        return "sơ tù/tử cưỡi hung tướng, mạt vượng/tướng cưỡi cát tướng (trước khó sau được)"


def _k_xam_hai(c):
    if c.so == c.u1 and hai(c.u1, c.ky):
        return "thần lục hại lâm can phát dụng"
    if c.so == c.u3 and hai(c.u3, c.z):
        return "thần lục hại lâm chi phát dụng"
    for n, x, u in c.nm:
        if c.so == u and hai(u, x):
            return "thần lục hại lâm %s phát dụng" % n


def _k_hinh_thuong(c):
    dich = [("can", c.ky), ("chi", c.z)] + [(n, x) for n, x, _ in c.nm]
    o = [n for n, x in dich if L.HINH[c.so] == x]
    if o:
        return "sơ truyền %s hình %s" % (C(c.so), ", ".join(o))


def _k_thien_phien(c):
    if c.z in TRONG and c.nt in TRONG and c.gio in TRONG and c.vt[4] in (1, 7):
        return "ngày trọng, nguyệt tướng trọng gia giờ trọng, Thìn gia %s" % C(c.vt[4])


def _k_hoa_khau(c, nhom):
    if c.ngay_tiet in nhom:
        hq = (c.z - 1) % 12
        if c.T[hq] == c.z or c.T[c.z] == hq:
            return "ngày %s, chi hôm nay và chi hôm qua gia lên nhau" % nhom[c.ngay_tiet]


def _k_thien_nguc(c):
    if (c.tu_mua(HC[c.so]) or c.so == vong(c.hg, MO)) and c.vt[4] == vong(c.hg, SINH_):
        return "sơ truyền tù/tử hoặc là mộ can; Thìn gia trường sinh %s của can" % C(c.vt[4])


def _k_tu_ky(c):
    if c.so == 4 and 4 in (c.u1, c.u3):
        return "Thìn lâm %s phát dụng" % ("can" if c.u1 == 4 else "chi")


def _k_phach_hoa(c):
    if c.tuong[c.so] == "Bạch Hổ" and c.so == c.ss["Tử Khí"] and c.so in [c.u1, c.u3] + [u for _, _, u in c.nm]:
        return "Bạch Hổ cưỡi Tử khí %s phát dụng, lâm can/chi/năm mệnh" % C(c.so)


def _k_long_chien(c):
    if c.z in (3, 9) and c.so in (3, 9):
        nm = [n for n, x, _ in c.nm if c.vt[x] in (3, 9)]
        return "ngày %s, %s phát dụng%s" % (C(c.z), C(c.so), ("; " + ", ".join(nm) + " gia Mão/Dậu") if nm else "")


def _k_le_duc(c):
    if c.vt[c.qn] in (3, 9):
        tr = lambda x: 1 <= c.idx(x) <= 5      # noqa: E731
        sa = lambda x: 7 <= c.idx(x) <= 11     # noqa: E731
        if (tr(c.u1) and tr(c.u3) and sa(c.u2) and sa(c.u4)) or (sa(c.u1) and sa(c.u3) and tr(c.u2) and tr(c.u4)):
            return "Quý nhân lâm %s; dương thần và âm thần của can chi chia hai bên Quý nhân" % C(c.vt[c.qn])


def _k_toan_cuc(c):
    d = tam_hop(c.tr)
    if d is not None:
        return TEN_CUC[d]
    if len(set(c.tr)) == 3 and all(t in QUY_ for t in c.tr):
        return "Giá sắc (ba truyền đều Thổ)"


def _k_lien_chau(c):
    a, b = (c.trung - c.so) % 12, (c.mat - c.trung) % 12
    if a == b and a in (1, 11):
        ten = "tiến như (liên tiến)" if a == 1 else "thoái như (liên thoái)"
        if len({(t - 2) % 12 // 3 for t in c.tr}) == 1:          # mạnh-trọng-quý cùng một mùa
            ten += ", ba thần cùng một mùa (liên châu)"
        return ten


def _k_cuu_xu(c):
    if (c.g, c.z) in ((4, 0), (4, 6), (8, 0), (8, 6), (1, 3), (1, 9), (5, 3), (5, 9), (7, 3), (7, 9)) \
            and c.gio in TRONG and c.u3 == 1:
        return "một trong mười ngày Cửu xú, giờ trọng, Sửu lâm chi%s" % (" phát dụng" if c.so == 1 else "")


def _k_thien_vong(c):
    if KHAC(HC[c.gio], c.hg) and KHAC(HC[c.so], c.hg):
        return "giờ %s và sơ truyền %s cùng khắc can" % (C(c.gio), C(c.so))


def _k_duc_khanh(c):
    duc = {c.ss["Nhật Đức"]: "Nhật đức (đức thần)"}           # "nhật đức (can đức, đức thần)" – sách thần sát
    if c.so in duc:
        cat = [n for n, _, u in c.nm if c.tuong[u] in CAT_TUONG]
        if not c.nm or cat:
            return "%s %s phát dụng%s" % (duc[c.so], C(c.so), ("; " + ", ".join(cat) + " cưỡi cát tướng") if cat
                                           else " (chưa có năm sinh để xét điều kiện năm mệnh)")


def _k_vinh_hoa(c):
    t = {LOC[c.g]: "Lộc", L.DICH_MA[c.z]: "Mã", c.qn_tru: "Quý nhân", c.qn_da: "Quý nhân"}
    if c.so in t and c.so in [c.u1, c.u3] + [u for _, _, u in c.nm] and c.vt_mua(HC[c.so]) and all(
            c.tuong[x] in CAT_TUONG for x in c.tr):
        return "%s %s lâm can/chi/năm mệnh phát dụng, vượng tướng, ba truyền cát tướng" % (t[c.so], C(c.so))


def _k_hoa_my(c):
    if hop(c.ky, c.u1) and hop(c.z, c.u3):
        return "can hợp can thượng, chi hợp chi thượng"
    if hop(c.ky, c.u3) and hop(c.z, c.u1):
        return "can hợp chi thượng, chi hợp can thượng"


def _k_thoi_thai(c):
    if ((c.so == c.nam and c.thang in c.tr) or (c.so == c.thang and c.nam in c.tr)) and (
            {c.tuong[c.so], c.tuong[c.mat]} & {"Thanh Long", "Lục Hợp"}) and any(
            c.lt(t) == "Thê tài" for t in c.tr) and set(c.tr) & {c.ss["Nhật Đức"], c.ss["Thiên Đức"],
                                                                c.ss["Nguyệt Đức"]}:
        return "thái tuế/nguyệt kiến phát dụng và nhập truyền, có Long/Hợp, có tài và đức thần"


KHOA_CACH = [
    ("Tam quang", "sáng sủa, việc hanh thông", _k_tam_quang),
    ("Tam dương", "được người trên đỡ, việc công thuận", _k_tam_duong),
    ("Tam âm", "mờ tối, dễ bị che giấu; nên thận trọng", _k_tam_am),
    ("Tam kỳ", "gặp may, hung giảm cát tăng", lambda c: "Tuần kỳ %s phát dụng" % C(c.so)
     if c.so == c.ss["Tuần Kỳ"] else None),
    ("Lục nghi", "có người trên che chở, lỗi được tha", lambda c: "Tuần nghi %s phát dụng" % C(c.so)
     if c.so == c.xun else None),
    ("Long đức", "ân lớn từ bề trên", lambda c: "thái tuế là nguyệt tướng, phát dụng cưỡi Quý nhân"
     if c.nam == c.nt == c.so and c.tuong[c.so] == "Quý Nhân" else None),
    ("Quan tước", "tin về chức vụ, bổ nhiệm", _k_quan_tuoc),
    ("Phú quý", "được quý nhân lớn giúp", _k_phu_quy),
    ("Hiên cái", "đi xe có lọng: thăng tiến, đi xa vẻ vang", lambda c: "Ngọ phát dụng, có Mão và Tý trong truyền"
     if c.so == 6 and 3 in c.tr and 0 in c.tr else None),
    ("Chú ấn", "đúc ấn: có văn bằng, chức vụ", lambda c: "Tuất gia Tỵ nhập truyền"      # 大全 q.8 "戌加巳中传"
     if 10 in c.tr and c.vt[10] == 5 else None),
    ("Chước luân", "đẽo bánh xe: thành tài sau rèn giũa", _k_chuoc_luan),
    ("Dẫn tòng", "có người dẫn đường, theo hầu", _p1),
    ("Hanh thông", "thông suốt", _k_hanh_thong),
    ("Trảm quan", "phá cửa ải: lợi việc vượt khó, đi gấp", _k_tram_quan),
    ("Bế khẩu", "khó nói, khó dò", _p38),
    ("Du tử", "người đi xa chưa về, xa quê", _k_du_tu),
    ("Tam giao", "việc chồng chéo, giấu kín", _k_tam_giao),
    ("Loạn thủ", "trên dưới lộn trật tự", _k_loan_thu),
    ("Chuế tế", "ở nhờ, phụ thuộc người", _k_chue_te),
    ("Dâm dật", "tình cảm không chính đáng", _k_dam_dat),
    ("Vu dâm", "hai bên không thật lòng", _k_vu_dam),
    ("Cô quả", "lẻ loi, thiếu người giúp", _k_co_qua),
    ("Độ ách", "gặp ách cần vượt (ấu: lớp dưới; trưởng: người trên)", _k_do_ach),
    # Lục Nhâm đại toàn q.9 "Vô lộc tuyệt tự khóa": "凡课四上俱克下，为无禄课 … 凡四下俱贼上，乃为绝嗣之格";
    # tượng: "上克无禄，下克绝嗣" (ví dụ: Kỷ Tỵ ngày Dậu tướng giờ Dần = vô lộc; Canh Thìn Hợi tướng giờ Thìn = tuyệt tự).
    ("Vô lộc", "trên ép dưới: người dưới chịu thiệt, chức lộc khó giữ", lambda c: "bốn khóa đều thượng khắc hạ"
     if c.n_khac == 4 else None),
    ("Tuyệt tự", "dưới phạm trên: người trên gặp hại, tiểu nhân vô lễ", lambda c: "bốn khóa đều hạ tặc thượng"
     if c.n_tac == 4 else None),
    ("Truân phúc", "trước gian sau được", _k_truan_phuc),
    ("Xâm hại", "bị xâm phạm, ngầm hại", _k_xam_hai),
    ("Hình thương", "va chạm, tổn thương", _k_hinh_thuong),
    ("Thiên phiền", "phiền nhiễu, trắc trở", _k_thien_phien),
    ("Thiên họa", "ngày Tứ lập: đề phòng biến cố", lambda c: _k_hoa_khau(c, TU_LAP)),
    ("Thiên khấu", "ngày phân/chí: phòng hao mất, trộm", lambda c: _k_hoa_khau(c, PHAN_CHI)),
    ("Thiên ngục", "bị giam hãm, bó buộc", _k_thien_nguc),
    ("Tử kỳ", "việc bế tắc", _k_tu_ky),
    ("Phách hóa", "lo âu về sức khỏe; cần thận trọng", _k_phach_hoa),
    ("Long chiến", "tranh chấp, giằng co, tiến thoái khó", _k_long_chien),
    ("Lệ đức", "người trên thăng, người dưới thoái; nên giữ đức", _k_le_duc),
    ("Toàn cục", "ba truyền hợp cục: sức tập trung một hướng", _k_toan_cuc),
    ("Nguyên thai", "việc mới thai nghén, chưa thành hình", lambda c: "ba truyền đều tứ mạnh (Dần Thân Tỵ Hợi)"
     if all(t in MANH for t in c.tr) else None),
    ("Liên như", "việc nối tiếp liên tục", _k_lien_chau),
    ("Lục thuần", "toàn dương lợi việc công, toàn âm lợi việc riêng", lambda c: _p5(c) or _p6(c)),
    ("Cửu xú", "dễ có chuyện không hay, nên giữ mình", _k_cuu_xu),
    ("Thiên võng", "như lưới trời chụp: nên tĩnh", _k_thien_vong),
    ("Đức khánh", "có đức thần giúp, vui mừng", _k_duc_khanh),
    ("Vinh hoa", "vinh hiển, được việc", _k_vinh_hoa),
    ("Hòa mỹ", "hòa thuận, dễ thỏa thuận", _k_hoa_my),
    ("Thời thái", "gặp thời, thuận", _k_thoi_thai),
]


def khoa_cach(c):
    out = []
    for ten, y, f in KHOA_CACH:
        d = f(c)
        if d:
            out.append((ten, d, y))
    return out


# ---------------------------------------------------------------- 3. bản mệnh / hành niên
def hanh_nien(tuoi, gioi):
    """Can chi (chỉ số 0..59) hành niên theo tuổi mụ: nam 1 tuổi Bính Dần đi thuận, nữ 1 tuổi Nhâm Thân đi nghịch."""
    if tuoi < 1:
        tuoi = 1
    return (2 + (tuoi - 1)) % 60 if gioi == "nam" else (8 - (tuoi - 1)) % 60


def ten_gz(i):
    return "%s %s" % (CAN[i % 10], CHI[i % 12])


def quan_he_chi(a, b):
    o = []
    if a == b:
        o.append("trùng")
    if hop(a, b):
        o.append("lục hợp")
    if xung(a, b):
        o.append("xung")
    if hinh(a, b) and a != b:
        o.append("hình")
    if hai(a, b):
        o.append("hại")
    if a != b and (a - b) % 4 == 0:
        o.append("tam hợp")
    ha, hb = HC[a], HC[b]
    if a != b:
        if SINH(ha, hb):
            o.append("sinh")
        elif SINH(hb, ha):
            o.append("được sinh")
        elif KHAC(ha, hb):
            o.append("khắc")
        elif KHAC(hb, ha):
            o.append("bị khắc")
    return ", ".join(o) or "bình hòa"


UNG = {"Huynh đệ": "tỷ hòa (giúp sức)", "Phụ mẫu": "sinh can (được cứu giúp)", "Tử tôn": "can sinh nó (hao sức)",
       "Thê tài": "can khắc nó (mình chủ động)", "Quan quỷ": "khắc can (bị áp lực)"}


def nam_menh(c):
    """Bảng thông tin bản mệnh / hành niên."""
    rows = []
    for n, x, u in c.nm:
        o = []
        if u in c.tr:
            o.append("thượng thần là %s truyền" % "/".join(nn for nn, t in zip(("sơ", "trung", "mạt"), c.tr) if t == u))
        if x in c.tr:
            o.append("chi năm mệnh %s nhập truyền" % C(x))
        o.append("với sơ truyền %s: %s" % (C(c.so), quan_he_chi(u, c.so)))
        if c.mat != c.so:
            o.append("với mạt %s: %s" % (C(c.mat), quan_he_chi(u, c.mat)))
        rows.append((n, x, u, c.tuong[u], c.lt(u), UNG[c.lt(u)], c.kh(u), c.don.get(u), "; ".join(o)))
    return rows


# ---------------------------------------------------------------- 5. loại thần theo việc
VIEC = {
    "chung": ("Việc chung", [], [], []),
    "tien": ("Cầu tài, tiền bạc", ["Thanh Long"], ["Thê tài"], ["Lộc"]),
    "quan": ("Công danh, việc làm, chức vụ", ["Quý Nhân", "Thái Thường"], ["Quan quỷ"], ["Dịch Mã", "Thiên Mã"]),
    "benh": ("Bệnh tật", ["Bạch Hổ"], ["Quan quỷ", "Tử tôn"], ["Thiên Y", "Tử Khí"]),
    "kien": ("Kiện tụng, tranh chấp", ["Chu Tước", "Câu Trận", "Quý Nhân"], ["Quan quỷ"], ["Giải Thần"]),
    "matdo": ("Mất đồ, trộm cắp", ["Huyền Vũ", "Thiên Không"], ["Thê tài"], ["Du Đô", "Lỗ Đô"]),
    "honnhan": ("Hôn nhân, tình cảm", ["Lục Hợp", "Thiên Hậu", "Thanh Long"], ["Thê tài", "Quan quỷ"],
                ["Thiên Hỷ", "Đào Hoa (Hàm Trì)"]),
    "thi": ("Thi cử, giấy tờ", ["Chu Tước", "Quý Nhân", "Thái Thường"], ["Phụ mẫu"], []),
    "hopdong": ("Hợp đồng, hợp tác, giao dịch", ["Lục Hợp", "Chu Tước", "Thanh Long"], ["Thê tài"], ["Thành Thần"]),
    "xuathanh": ("Đi xa, xuất hành, vận chuyển", ["Bạch Hổ"], [], ["Dịch Mã", "Thiên Mã", "Lục Đinh"]),
    "nha": ("Nhà cửa, đất đai", ["Câu Trận", "Thái Thường"], ["Phụ mẫu"], []),
    "thai": ("Thai sản, con cái", ["Thiên Hậu"], ["Tử tôn"], ["Sinh Khí"]),
    "timnguoi": ("Tìm người, người đi xa", ["Thái Âm", "Huyền Vũ"], [], ["Dịch Mã", "Lục Đinh", "Thiên Mã"]),
}
Y_TUONG = {"Thanh Long": "tiền của, niềm vui", "Quý Nhân": "người trên, quan tòa", "Thái Thường": "ấn tín, lễ nghi, cơm áo",
           "Bạch Hổ": "bệnh, đường đi, sự cứng rắn", "Chu Tước": "văn thư, lời nói", "Câu Trận": "tranh chấp, ruộng đất",
           "Huyền Vũ": "kẻ gian, sự mờ ám", "Thiên Không": "lừa dối, trống rỗng", "Lục Hợp": "mối lái, giao dịch",
           "Thiên Hậu": "phụ nữ, người vợ", "Thái Âm": "việc kín, người âm thầm", "Đằng Xà": "lo sợ, quấn quýt"}
Y_LT = {"Thê tài": "tiền, vợ (nam hỏi)", "Quan quỷ": "chức vụ, áp lực, bệnh, chồng (nữ hỏi)", "Tử tôn": "con cái, thuốc men",
        "Phụ mẫu": "giấy tờ, nhà cửa, cha mẹ", "Huynh đệ": "bạn bè, đối thủ cạnh tranh"}


def loai_than(c, viec):
    """Trả về (tên việc, list dòng (loại thần, chi, chỗ, ghi chú))."""
    ten_viec, tuongs, lts, sats = VIEC[viec]
    if viec == "honnhan" and c.gioi in ("nam", "nu"):   # nam hỏi xem Thê tài (vợ), nữ hỏi xem Quan quỷ (chồng)
        lts = ["Thê tài"] if c.gioi == "nam" else ["Quan quỷ"]
    rows = []
    for t in tuongs:
        x = _hien(c, t)
        rows.append(("%s (%s)" % (t, Y_TUONG.get(t, "")), x))
    for lt in lts:
        xs = sorted({x for x in c.tren + c.tr if c.lt(x) == lt})
        if xs:
            for x in xs:
                rows.append(("%s (%s)" % (lt, Y_LT[lt]), x))
        else:
            rows.append(("%s (%s)" % (lt, Y_LT[lt]), None))
    for s in sats:
        rows.append((s, c.ss[s]))
    out = []
    for nhan, x in rows:
        if x is None:
            ganh = [y for y in range(12) if c.lt(y) == nhan.split(" (")[0]]
            out.append((nhan, "–", "không có trong khóa truyền",
                        "trên thiên bàn ở: " + ", ".join("%s (lâm %s)" % (C(y), C(c.vt[y])) for y in ganh)))
            continue
        noi = c.noi(x)
        ghi = ["%s, %s" % (mua(HC[x], c.thang), c.lt(x))]
        if c.kh(x):
            ghi.append("tuần không")
        elif c.lac(x):
            ghi.append("lạc không")
        ghi.append("với can: " + UNG[c.lt(x)])
        out.append((nhan, "%s lâm %s, cưỡi %s" % (C(x), C(c.vt[x]), c.tuong[x]),
                    ", ".join(noi) if noi else "ngoài khóa truyền", "; ".join(ghi)))
    return ten_viec, out


# ---------------------------------------------------------------- tổng hợp & in
def phan_tich(gn, gio, tuong, thang, nam, nam_sinh=None, nam_xem=None, gioi=None, viec="chung", ngay_tiet=None):
    """Lập khóa (lucnham.lap) và mọi phần bổ sung. gn: chỉ số can chi ngày 0..59; gio, tuong, thang, nam: chi."""
    r = L.lap(gn, gio, tuong)
    bm = hn = None
    tuoi = hn_gz = None
    if nam_sinh is not None:
        bm = (nam_sinh - 4) % 12
        if nam_xem is not None:
            tuoi = nam_xem - nam_sinh + 1
            if gioi in ("nam", "nu"):
                hn_gz = hanh_nien(tuoi, gioi)
                hn = hn_gz % 12
    c = NguCanh(r, tuong, gio, thang, nam, bm, hn, ngay_tiet, gioi)
    return dict(r=r, c=c, than_sat=than_sat(r["g"], r["z"], thang, nam), tat_phap=tat_phap(c),
                khoa_cach=khoa_cach(c), nam_menh=nam_menh(c), loai_than=loai_than(c, viec),
                tuoi=tuoi, hn_gz=hn_gz, nam_sinh=nam_sinh)


def _dau(c, x):
    m = []
    d = c.don.get(x)
    if d == 3:
        m.append("Lục Đinh")
    if c.kh(x):
        m.append("Tuần không")
    elif c.lac(x):
        m.append("lạc không")
    if c.tuong[x] == "Thiên Không":
        m.append("Thiên Không")
    if x == c.xun:
        m.append("Tuần nghi")
    if x == c.ss["Tuần Kỳ"]:
        m.append("Tuần kỳ")
    return ", ".join(m)


def cau_hanh(a, ha, b, hb):
    """Câu ngắn nói quan hệ ngũ hành giữa hai vị (a, b là tên đã gắn nhãn)."""
    if ha == hb:
        return "%s tỷ hòa %s" % (a, b)
    if SINH(ha, hb):
        return "%s sinh %s" % (a, b)
    if KHAC(ha, hb):
        return "%s khắc %s" % (a, b)
    if SINH(hb, ha):
        return "%s sinh %s" % (b, a)
    return "%s khắc %s" % (b, a)


def in_bo_sung(kq):
    """In phần bổ sung (sau khi đã in khóa bằng lucnham.in_khoa)."""
    c = kq["c"]
    print("LỤC NHÂM BỔ SUNG")
    print("- Nguyệt kiến (tháng tiết) %s, thái tuế %s; Quý nhân trú %s, dạ %s – đang dùng %s %s, %s trị "
          "(lâm %s trên địa bàn)." % (C(c.thang), C(c.nam), C(c.qn_tru), C(c.qn_da), "trú" if c.tru else "dạ",
                                      C(c.qn), "thuận" if c.thuan else "nghịch", C(c.vt[c.qn])))
    print("- Thiên Cương (Thìn) lâm %s (%s); tuần Giáp %s (đầu tuần %s, cuối tuần %s)." % (
        C(c.vt[4]), "tứ mạnh" if c.vt[4] in MANH else ("tứ trọng" if c.vt[4] in TRONG else "tứ quý"),
        C(c.xun), C(c.xun), C(c.vi)))
    can, chi = "can %s" % CAN[c.g], "chi %s" % C(c.z)
    ct, zt = "can thượng %s" % C(c.u1), "chi thượng %s" % C(c.u3)
    print("- Can – chi (nhật thần): %s; %s; %s; %s." % (
        cau_hanh(ct, HC[c.u1], can, c.hg), cau_hanh(zt, HC[c.u3], chi, c.hz),
        cau_hanh(zt, HC[c.u3], can, c.hg), cau_hanh(ct, HC[c.u1], chi, c.hz)))
    print()
    print("ĐỘN CAN (TUẦN ĐỘN) 4 KHÓA VÀ 3 TRUYỀN")
    print("| Vị trí | Thượng thần | Độn can | Lục thân của chi | Độn can so với can ngày | Thiên tướng | Đánh dấu |")
    print("|---|---|---|---|---|---|---|")
    for nhan, x in list(zip(("Khóa 1", "Khóa 2", "Khóa 3", "Khóa 4"), c.tren)) + list(
            zip(("Sơ truyền", "Trung truyền", "Mạt truyền"), c.tr)):
        d = c.don.get(x)
        print("| %s | %s | %s | %s | %s | %s | %s |" % (nhan, C(x), CAN[d] if d is not None else "– (không)", c.lt(x),
                                                    luc_than_can(c.g, d) if d is not None else "–", c.tuong[x],
                                                    _dau(c, x)))
    kh = sorted(c.khong)
    print("- Tuần không %s: lục thân bị không là %s." % (" ".join(C(x) for x in kh),
                                                         ", ".join(sorted({c.lt(x) for x in kh}))))
    print()
    print("THẦN SÁT LỤC NHÂM")
    print("| Sao | Theo | Chi | Lâm (địa bàn) | Thiên tướng | Trong khóa/truyền | Ý nghĩa |")
    print("|---|---|---|---|---|---|---|")
    for ten, x, theo in kq["than_sat"]:
        noi = c.noi(x)
        print("| %s | %s | %s | %s | %s | %s | %s |" % (ten, theo, C(x), C(c.vt[x]), c.tuong[x],
                                                      ", ".join(noi) if noi else "–", Y_THAN_SAT[ten]))
    print()
    if kq["nam_sinh"] is not None:
        print("BẢN MỆNH / HÀNH NIÊN (năm sinh âm lịch %d%s)" % (
            kq["nam_sinh"], (", tuổi mụ %d" % kq["tuoi"]) if kq["tuoi"] is not None else ""))
        if kq["hn_gz"] is not None:
            print("- Hành niên %s (%s 1 tuổi khởi %s đi %s)." % (
                ten_gz(kq["hn_gz"]), "nam" if c.gioi == "nam" else "nữ",
                "Bính Dần" if c.gioi == "nam" else "Nhâm Thân", "thuận" if c.gioi == "nam" else "nghịch"))
        else:
            print("! Chưa có giới tính (--gioi) hoặc năm xem nên chưa tính hành niên.")
        print("| | Địa chi | Thượng thần | Thiên tướng | Lục thân | Với can ngày | Tuần không | Độn can | Quan hệ với truyền |")
        print("|---|---|---|---|---|---|---|---|---|")
        for n, x, u, tg, lt, ung, k, d, qh in kq["nam_menh"]:
            print("| %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
                n.capitalize(), C(x), C(u), tg, lt, ung, "có" if k else "–", CAN[d] if d is not None else "–", qh))
        if len(c.nm) == 2:
            print("- Bản mệnh %s với hành niên %s: %s." % (C(c.bm), C(c.hn), quan_he_chi(c.bm, c.hn)))
        print()
    print("TẤT PHÁP PHÚ – các điều khớp (máy nhận diện; chỉ là gợi ý để xem kỹ)")
    if kq["tat_phap"]:
        print("| Điều | Tên | Điều kiện khớp | Ý nghĩa ngắn |")
        print("|---|---|---|---|")
        for so, ten, d, y in kq["tat_phap"]:
            print("| %d | %s | %s | %s |" % (so, ten, d, y))
    else:
        print("- Không có điều nào trong %d điều máy kiểm được khớp." % len(TAT_PHAP))
    print()
    print("KHÓA CÁCH NGOÀI CỬU TÔNG")
    if kq["khoa_cach"]:
        print("| Khóa cách | Điều kiện khớp | Ý nghĩa ngắn |")
        print("|---|---|---|")
        for ten, d, y in kq["khoa_cach"]:
            print("| %s | %s | %s |" % (ten, d, y))
    else:
        print("- Không khớp khóa cách nào trong %d cách máy kiểm được." % len(KHOA_CACH))
    print()
    ten_viec, rows = kq["loai_than"]
    print("LOẠI THẦN – việc hỏi: %s" % ten_viec)
    if rows:
        print("| Loại thần | Ở đâu trên bàn | Trong khóa/truyền | Ghi chú |")
        print("|---|---|---|---|")
        for row in rows:
            print("| %s | %s | %s | %s |" % row)
        print("(Loại thần vắng mặt trong khóa truyền thì vẫn xét chỗ nó đứng trên thiên bàn – Tất pháp phú điều 97.)")
    else:
        print("- Chưa chọn loại việc (--viec). Gợi ý: tien, quan, benh, kien, matdo, honnhan, thi, hopdong, "
              "xuathanh, nha, thai, timnguoi.")
    print()
    print("! Ghi chú trường phái: mộ/trường sinh hành Thổ theo Thủy (Thân sinh, Thìn mộ) như chú Tất pháp phú; "
          "Dương nhận can âm lấy lùi một ngôi; Thiên đức lấy cung ký của can. Tất pháp phú và khóa cách là "
          "điều kiện máy kiểm, cần đọc cùng toàn khóa, không đọc riêng lẻ.")


def _tiet_trong_ngay(tt, B):
    """Tên tiết (Việt) nếu ngày xem là ngày Tứ lập hoặc Nhị phân nhị chí (theo giờ đồng hồ địa phương)."""
    import datetime as dt
    lun = B.lunar_cua(tt.t_bk)
    tbl = lun.getJieQiTable()
    for k, s in tbl.items():
        if k in TU_LAP or k in PHAN_CHI:
            t = dt.datetime(s.getYear(), s.getMonth(), s.getDay(), s.getHour(), s.getMinute())
            t = t - dt.timedelta(hours=8 - tt.utc_off)
            if t.date() == tt.dong_ho.date():
                return k
    return None


# ---------------------------------------------------------------- CLI
def them_lenh(sub):
    import nc
    p = sub.add_parser("lucnham2", help="Đại Lục Nhâm bổ sung: thần sát, độn can, năm mệnh, Tất pháp phú, "
                                         "khóa cách, loại thần")
    nc.them_tham_so_sinh(p)
    p.add_argument("--nam-sinh", type=int, help="năm sinh âm lịch của người hỏi (để tính bản mệnh, hành niên)")
    p.add_argument("--viec", default="chung", choices=sorted(VIEC), help="loại việc hỏi để gợi ý loại thần")
    p.set_defaults(_chay=chay)
    return p


def _so_gz(B, s):
    """Chuỗi can chi chữ Hán của lunar_python -> chỉ số 0..59 (chỉ dùng hằng số của tvbt)."""
    g, z = B.GAN_LIST.index(s[0]), B.ZHI_LIST.index(s[1])
    return [i for i in range(60) if i % 10 == g and i % 12 == z][0]


def _in_dau(tt, B):
    """Dòng đầu: thời điểm hỏi việc (giống tvbt.in_dau_thoi_diem, viết lại để không phụ thuộc hàm đó)."""
    print("THỜI ĐIỂM HỎI VIỆC: %s giờ đồng hồ (UTC%+g), %s; giờ dùng để tính: %s (%s) → giờ %s" % (
        tt.dong_ho.strftime("%H:%M %d/%m/%Y"), tt.utc_off, tt.noi, tt.t_dia_phuong.strftime("%H:%M"),
        "mặt trời thực" if tt.dung_tst else "đồng hồ", CHI[B.chi_gio(tt.t_dia_phuong)]))
    for x in tt.canh_bao:
        if not x.startswith("Sinh trước 1955") and not x.startswith("Sinh giờ Tý muộn"):
            print("! " + x.replace("Giờ sinh", "Giờ xem"))
    print()


def chay(a):
    import nc
    import tvbt as B
    tt = nc.thoi_diem(a)
    _in_dau(tt, B)
    e = B.lunar_cua(tt.t_dia_phuong).getEightChar()
    e.setSect(tt.sect)
    lbk = B.lunar_cua(tt.t_bk)
    ebk = lbk.getEightChar()
    q_han = lbk.getPrevQi(False).getName()
    q = TRUNG_KHI.get(q_han)
    if q is None:
        raise SystemExit("LỖI: không nhận ra trung khí " + repr(q_han))
    tuong = L.NGUYET_TUONG[q]
    gn, gg = _so_gz(B, e.getDay()), _so_gz(B, e.getTime())
    thang, nam = B.ZHI_LIST.index(ebk.getMonthZhi()), B.ZHI_LIST.index(ebk.getYearZhi())
    nam_xem = B.duong_sang_am(tt.t_dia_phuong.date(), tt.lich_tz)[2]
    gioi = getattr(tt, "gioi_that", None)
    if a.nam_sinh is not None and not (1900 <= a.nam_sinh <= nam_xem):
        raise SystemExit("LỖI: --nam-sinh phải là năm âm lịch từ 1900 đến năm hiện tại.")
    kq = phan_tich(gn, gg % 12, tuong, thang, nam, a.nam_sinh, nam_xem, gioi, a.viec, _tiet_trong_ngay(tt, B))
    L.in_khoa(kq["r"], B.vn(e.getDay()), B.vn(e.getTime()), tuong, q)
    if tt.t_dia_phuong.hour == 23:
        print("! Giờ Tý muộn (23h–24h): đang tính ngày theo --ty %d; phái khác lấy ngày cũ." % tt.sect)
    in_bo_sung(kq)


# ---------------------------------------------------------------- tự kiểm
def _mau(can_chi, tren, duoi, gio=6, **kw):
    """Khóa mẫu theo cách ghi trong sách: 'ngày X, thiên chi `tren` gia địa chi `duoi`, giờ `gio`'."""
    g, z = can_chi
    gn = [i for i in range(60) if i % 10 == g and i % 12 == z][0]
    tuong = (gio + tren - duoi) % 12
    kw.setdefault("thang", (13 - tuong) % 12)
    kw.setdefault("nam", 0)
    thang, nam = kw.pop("thang"), kw.pop("nam")
    return phan_tich(gn, gio, tuong, thang, nam, **kw)


def _co(kq, so):
    return any(x[0] == so for x in kq["tat_phap"])


def _co_cach(kq, ten):
    return any(x[0] == ten for x in kq["khoa_cach"])


def tu_kiem():
    """Kiểm bằng ví dụ trong chú giải Tất pháp phú / sách thần sát và các bất biến; trả về list lỗi."""
    loi = []
    G = {n: i for i, n in enumerate(CAN)}
    Z = {n: i for i, n in enumerate(CHI)}

    def gz(s):
        a, b = s.split()
        return G[a], Z[b]

    # --- A. Thần sát: bảng trong "Lục Nhâm thần sát tường giải" (Dạ Không blog, zhifou123.com id=56) ---
    ts = {t: c for t, c, _ in than_sat(0, 0, 2, 11)}     # ngày Giáp Tý, tháng Dần (tháng giêng), năm Hợi
    mong = {"Thiên Đức": 7, "Nguyệt Đức": 5, "Thiên Hỷ": 10, "Thiên Y": 4, "Thiên Mã": 6, "Giải Thần": 8,
            "Sinh Khí": 0, "Tử Khí": 6, "Thiên Quỷ": 9, "Thành Thần": 5, "Hoàng Ân": 7, "Nguyệt Phá": 8,
            "Tuế Phá": 5, "Tang Môn": 1, "Điếu Khách": 9, "Bệnh Phù": 10, "Dịch Mã": 2, "Kiếp Sát": 5,
            "Hoa Cái": 4, "Vong Thần": 11, "Tướng Tinh": 0, "Đào Hoa (Hàm Trì)": 9, "Du Đô": 1, "Lỗ Đô": 7,
            "Nhật Đức": 2, "Tuần Kỳ": 1, "Tuần Nghi": 0, "Lục Đinh": 3, "Lộc": 2, "Dương Nhận": 3}
    for k, v in mong.items():
        if ts[k] != v:
            loi.append("thần sát %s ngày Giáp Tý tháng Dần năm Hợi: %s, sách: %s" % (k, C(ts[k]), C(v)))
    # "正月丁（未），二月坤（申），三月壬（亥），四月辛（戌），五月乾（亥），六月甲（寅），七月癸（丑），八月艮（寅），
    #  九月丙（巳），十月乙（辰），十一巽（巳），十二庚（申）"
    if [dict((t, c) for t, c, _ in than_sat(0, 0, m, 0))["Thiên Đức"]
            for m in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1)] != [7, 8, 11, 10, 11, 2, 1, 2, 5, 4, 5, 8]:
        loi.append("Thiên đức không khớp bảng sách (can lấy cung ký)")
    if [dict((t, c) for t, c, _ in than_sat(0, 0, m, 0))["Thiên Hỷ"] for m in (2, 5, 8, 11)] != [10, 1, 4, 7]:
        loi.append("Thiên hỷ phải là Xuân Tuất, Hạ Sửu, Thu Thìn, Đông Mùi")
    if NHAN[1] != 2 or NHAN[2] != 6 or NHAN[4] != 6:
        loi.append("Dương nhận phải là Giáp Mão, Ất Dần, Bính Mậu Ngọ (theo sách thần sát)")
    # Hành niên: nam 1 tuổi Bính Dần, nữ 1 tuổi Nhâm Thân (zhifou123 id=54, dajiazhao.com 推行年法)
    if [ten_gz(hanh_nien(t, "nam")) for t in (1, 2, 13)] != ["Bính Dần", "Đinh Mão", "Mậu Dần"]:
        loi.append("hành niên nam sai")
    if [ten_gz(hanh_nien(t, "nu")) for t in (1, 2, 13)] != ["Nhâm Thân", "Tân Mùi", "Canh Thân"]:
        loi.append("hành niên nữ sai")

    # --- B. Khóa mẫu ví dụ trong chú Tất pháp phú (tianyugong.com/bff; zhifou123 id=63) ---
    mau = [
        # (ngày, thiên chi, gia địa chi, giờ, điều phải khớp, ghi chú tam truyền nếu sách có)
        ("Canh Thìn", "Sửu", "Thân", 6, 1, ("Dần", "Mùi", "Tý")),   # "如庚辰日干上丑" dẫn tòng
        ("Nhâm Tý", "Thìn", "Hợi", 6, 1, ("Tỵ", "Tuất", "Mão")),    # "壬子日干上辰"
        ("Tân Mão", "Hợi", "Tuất", 6, 77, None),                    # 互生 "辛卯日干上亥"
        ("Giáp Thân", "Dậu", "Dần", 6, 78, None),                   # 互旺 "甲申日干上酉"
        ("Giáp Thân", "Mão", "Dần", 6, 78, None),                   # 皆旺 "甲申日干上卯"
        ("Giáp Thân", "Mão", "Dần", 6, 55, None),                   # 天罗地网 "甲申日干上卯"
        ("Bính Thìn", "Dần", "Dậu", 6, 32, ("Dần", "Mùi", "Tý")),   # 三传互克 "丙辰日寅加酉"
        ("Bính Dần", "Thân", "Tỵ", 6, 41, None),                    # 禄马 "丙寅日干上申"
        ("Đinh Mùi", "Tý", "Mùi", 6, 12, None),                     # 狐假虎威 "丁未日干上子"
        ("Giáp Thân", "Tỵ", "Thân", 6, 38, None),                   # 闭口 "甲申日巳加申"
        ("Giáp Thân", "Tý", "Dần", 6, 36, None),                    # 干支皆败 "甲申日干上子"
        ("Đinh Hợi", "Tý", "Mùi", 6, 63, None),                     # 彼此全伤 "丁亥日干上子"
        ("Bính Tuất", "Tuất", "Tỵ", 6, 53, None),                   # 两蛇夹墓 "丙戌日戌加巳" (giờ ngày)
        ("Bính Tuất", "Tuất", "Tỵ", 0, 53, None),                   #   và giờ đêm: cả trú lẫn dạ đều Xà
        ("Tân Hợi", "Hợi", "Tuất", 10, 39, None),                   # 太阳照武 "辛亥日亥将戌时"
        ("Giáp Tý", "Thìn", "Tý", 6, 66, None),                     # 支坟财并 "甲子日辰加子"
        ("Ất Hợi", "Mùi", "Hợi", 6, 62, None),                      # 支乘墓虎 "乙亥日未加亥" giờ ngày
        ("Quý Dậu", "Dậu", "Sửu", 6, 23, None),                     # 支传干 "癸酉日干上酉"
        ("Giáp Thân", "Mùi", "Thân", 6, 43, None),                  # 害贵 "甲申日未加申"
        ("Ất Dậu", "Thìn", "Thìn", 6, 22, None),                    # 上下皆合 "乙酉日伏吟"
        ("Nhâm Thìn", "Tuất", "Mùi", 6, 11, ("Tuất", "Sửu", "Thìn")),  # 众鬼 "壬辰日戌加未" can thượng Dần
        ("Đinh Dậu", "Dậu", "Mùi", 6, 44, None),                    # 课传俱贵 "丁酉日干上酉"
        ("Giáp Thân", "Ngọ", "Dần", 6, 29, ("Thìn", "Thân", "Tý")),  # 眷属丰盈 "甲申日干上午" (thủy cục)
        ("Mậu Dần", "Dậu", "Tỵ", 6, 54, ("Sửu", "Ngọ", "Dậu")),     # 虎视逢虎 "戊寅日干上酉" (giờ ngày)
        ("Ất Mão", "Mão", "Thìn", 6, 7, None),                      # 旺禄临身 "乙卯日干上卯"
        ("Giáp Tý", "Dần", "Tý", 6, 8, None),                       # 禄临支 "甲子日寅加子"
        ("Canh Tuất", "Mão", "Thân", 6, 10, None),                  # 朽木 "庚戌日卯加申"
        ("Tân Hợi", "Mão", "Tuất", 6, 10, None),                    #       "辛亥日卯加辛"
        ("Tân Hợi", "Ngọ", "Tuất", 6, 27, None),                    # 传财化鬼 "辛亥日干上午"
        ("Đinh Hợi", "Dậu", "Mùi", 6, 24, ("Dậu", "Hợi", "Sửu")),   # 干传支 "丁亥日干上酉…支上丑为末传"
        ("Tân Mão", "Ngọ", "Tuất", 6, 48, None),                    # 鬼乘天乙 "六辛日午加干，旦占"
        ("Tân Dậu", "Sửu", "Tuất", 6, 61, None),                    # 干乘墓虎 "六辛日丑加戌，旦将乘白虎"
        ("Kỷ Tỵ", "Mão", "Mùi", 0, 91, None),                       # 虎临干鬼 "六己日卯加未夜"
        ("Nhâm Tý", "Tý", "Hợi", 6, 17, ("Dần", "Mão", "Thìn")),    # 进茹空亡 "壬子日干上子…三传寅卯辰"
        ("Mậu Thân", "Thìn", "Tỵ", 6, 18, None),                    # 踏脚空亡 "戊申日干上辰"
        ("Đinh Dậu", "Ngọ", "Dậu", 0, 38, None),                    # 闭口(2) "丁酉日午加酉" (giờ đêm)
        ("Giáp Tý", "Thìn", "Tý", 6, 38, None),                     # 闭口(3) "甲子日辰加子"
        ("Canh Tý", "Tý", "Thân", 0, 15, None),                     # 脱上脱 "六庚日干上子，夜将上乘青龙"
        ("Giáp Thân", "Mùi", "Dần", 6, 16, None),                   # 空上空 "甲申日干上未，昼占"
        ("Tân Mão", "Tý", "Tuất", 6, 16, None),                     # 脱空 "辛卯日干上子，昼占"
        ("Ất Dậu", "Dậu", "Thìn", 6, 22, None),                     # "乙酉日酉加乙"
        ("Giáp Thân", "Hợi", "Dần", 6, 22, None),                   # "甲申日干上亥"
        ("Bính Dần", "Dần", "Tỵ", 6, 77, None),                     # 俱生 "丙寅、丁酉日干上寅"
        ("Đinh Dậu", "Dần", "Mùi", 6, 77, None),
        ("Mậu Dần", "Mùi", "Tỵ", 6, 88, None),                      # 干支乘墓 "戊寅日干上未" (Thổ mộ Thìn)
    ]
    for ngay, tren, duoi, gio, so, truyen in mau:
        kq = _mau(gz(ngay), Z[tren], Z[duoi], gio)
        if truyen and tuple(C(x) for x in kq["r"]["truyen"]) != truyen:
            loi.append("%s %s gia %s: tam truyền %s, sách %s" % (ngay, tren, duoi, " ".join(
                C(x) for x in kq["r"]["truyen"]), " ".join(truyen)))
        if not _co(kq, so):
            loi.append("%s %s gia %s: không nhận ra Tất pháp phú điều %d" % (ngay, tren, duoi, so))
    # "鬼贼当时": "如戊子日干上午", ba truyền Dần Mão Thìn, xem vào mùa xuân (tháng Dần)
    if not _co(_mau(gz("Mậu Tý"), Z["Ngọ"], Z["Tỵ"], 6, thang=2), 13):
        loi.append("Mậu Tý can thượng Ngọ tháng Dần: không nhận ra điều 13")
    # Hai ví dụ sách dùng phép Thiệp hại "lấy thần lâm Mạnh trước" (khác lucnham.lap: đếm sâu trước) –
    # kiểm luật bằng tam truyền như sách: 甲辰日戌加寅 ba truyền Tuất Ngọ Dần (điều 30);
    # 庚午日干上午 ba truyền Ngọ Thìn Dần (điều 37 "mạt trợ sơ mà khắc can").
    for ngay, tren, duoi, tr, so in (("Giáp Thìn", "Tuất", "Dần", (10, 6, 2), 30),
                                     ("Canh Ngọ", "Ngọ", "Thân", (6, 4, 2), 37)):
        g_, z_ = gz(ngay)
        gn = [i for i in range(60) if i % 10 == g_ and i % 12 == z_][0]
        tg = (6 + Z[tren] - Z[duoi]) % 12
        r = dict(L.lap(gn, 6, tg))
        r["truyen"] = list(tr)
        if not [x for x in tat_phap(NguCanh(r, tg, 6, (13 - tg) % 12, 0)) if x[0] == so]:
            loi.append("%s %s gia %s (truyền theo sách): không nhận ra điều %d" % (ngay, tren, duoi, so))
    # năm mệnh: "甲申日未加寅，乃墓神覆日；如占人本命又是未生，乃名天网自裹" (điều 56)
    kq = _mau(gz("Giáp Thân"), Z["Mùi"], Z["Dần"], 6, nam_sinh=1991, nam_xem=2026, gioi="nam")
    if not _co(kq, 56):
        loi.append("Giáp Thân Mùi gia Dần, người tuổi Mùi: không nhận ra điều 56")
    # khóa cách: Dẫn tòng (64 khóa, tianyugong.com/664: "日干或日支上神的前神发用；后神为末传")
    if not _co_cach(_mau(gz("Canh Thìn"), Z["Sửu"], Z["Thân"]), "Dẫn tòng"):
        loi.append("Canh Thìn can thượng Sửu: thiếu khóa cách Dẫn tòng")
    # Bế khẩu cũng là khóa cách (cùng điều kiện điều 38)
    if not _co_cach(_mau(gz("Giáp Thân"), Z["Tỵ"], Z["Thân"]), "Bế khẩu"):
        loi.append("Giáp Thân Tỵ gia Thân: thiếu khóa cách Bế khẩu")
    # Vô lộc / Tuyệt tự (Lục Nhâm đại toàn q.9): "三月己巳日寅时酉将占，四上俱克下，为无禄格";
    # "正月庚辰日辰时亥将占，四下俱贼上，为绝嗣格"; "甲寅日亥将子时占，三传子亥戌亦是绝嗣"
    for ngay, tg, gio_, ten in (("Kỷ Tỵ", "Dậu", "Dần", "Vô lộc"), ("Canh Thìn", "Hợi", "Thìn", "Tuyệt tự"),
                                ("Giáp Dần", "Hợi", "Tý", "Tuyệt tự")):
        g_, z_ = gz(ngay)
        gn = [i for i in range(60) if i % 10 == g_ and i % 12 == z_][0]
        kq = phan_tich(gn, Z[gio_], Z[tg], (13 - Z[tg]) % 12, 0)
        if not _co_cach(kq, ten) or _co_cach(kq, {"Vô lộc": "Tuyệt tự", "Tuyệt tự": "Vô lộc"}[ten]):
            loi.append("%s %s tướng giờ %s: sách là %s" % (ngay, tg, gio_, ten))
    # Chú ấn: "丙子日未时子将，巳加子用，传遇天魁" – ba truyền Tỵ Tuất Mão, Tuất gia Tỵ
    kq = phan_tich(12, 7, 0, 1, 0)
    if not _co_cach(kq, "Chú ấn"):
        loi.append("Bính Tý Tý tướng giờ Mùi: thiếu khóa cách Chú ấn")
    if _co_cach(_mau(gz("Giáp Tý"), Z["Tỵ"], Z["Tuất"]), "Chú ấn"):
        loi.append("Tỵ gia Tuất (ngược chiều) không phải Chú ấn")
    # Điều 22 "独支干上神作六合格": 戊辰日干上丑、支上子
    if not _co(_mau(gz("Mậu Thìn"), Z["Sửu"], Z["Tỵ"]), 22):
        loi.append("Mậu Thìn can thượng Sửu, chi thượng Tý: không nhận ra điều 22")
    # Điều 47: "如辰戌二日占之，乃为贵人入宅，非坐狱论也" – Giáp Thìn, Quý nhân Sửu gia Thìn (giờ ngày)
    d47 = _p47(_mau(gz("Giáp Thìn"), Z["Sửu"], Z["Thìn"], 6)["c"])
    if not d47 or "nhập trạch" not in d47:
        loi.append("Giáp Thìn Sửu gia Thìn: điều 47 phải là quý nhân nhập trạch, được %r" % d47)

    # --- C. Chạy toàn bộ 60 ngày x 12 giờ x 12 nguyệt tướng; bất biến và tần suất ---
    rnd = random.Random(7)
    dem = {so: 0 for so, _, _, _ in TAT_PHAP}
    dem_k = {ten: 0 for ten, _, _ in KHOA_CACH}
    n = 0
    for gn in range(60):
        for gio in range(12):
            for tuong in range(12):
                thang = (13 - tuong + rnd.choice((0, 1))) % 12
                nam = rnd.randrange(12)
                ns = 1950 + rnd.randrange(60)
                gioi = rnd.choice(("nam", "nu"))
                tiet = rnd.choice((None, None, None, "立春", "春分"))
                try:
                    kq = phan_tich(gn, gio, tuong, thang, nam, ns, 2026, gioi, rnd.choice(sorted(VIEC)), tiet)
                except Exception as ex:          # noqa: BLE001
                    loi.append("ngoại lệ ngày %s giờ %s tướng %s: %r" % (ten_gz(gn), C(gio), C(tuong), ex))
                    continue
                n += 1
                c = kq["c"]
                so_khop = {x[0] for x in kq["tat_phap"]}
                for s in so_khop:
                    dem[s] += 1
                for x in kq["khoa_cach"]:
                    dem_k[x[0]] += 1
                # bất biến
                if (55 in so_khop) != ((tuong - gio) % 12 == 1):
                    loi.append("điều 55 phải khớp đúng khi thiên bàn tiến 1 ngôi")
                if (52 in so_khop) != (c.T[2] == 4):
                    loi.append("điều 52 phải khớp đúng khi Thìn gia Dần")
                if {5, 6} <= so_khop or {17, 18} <= so_khop or {23, 24} <= so_khop:
                    loi.append("hai điều loại trừ nhau cùng khớp: %s" % sorted(so_khop))
                if 77 in so_khop and 64 in so_khop and _p77(c).startswith("hỗ"):
                    loi.append("hỗ sinh và vu dâm không thể cùng khớp")
                if c.don.get((c.xun + 3) % 12) != 3 or any(x in c.don for x in c.khong) or len(c.don) != 10:
                    loi.append("độn can / Lục Đinh / tuần không sai")
                if any(not 0 <= x < 12 for _, x, _ in kq["than_sat"]) or len(kq["than_sat"]) != len(Y_THAN_SAT):
                    loi.append("thần sát ngoài miền")
                if c.vt[c.T[5]] != 5 or c.T[c.vt[7]] != 7:
                    loi.append("thiên bàn / vị trí không nghịch đảo")
                if c.hn is not None and c.hn != kq["hn_gz"] % 12:
                    loi.append("hành niên không khớp")
                if c.ten.startswith("Phục ngâm") != c.phuc:
                    loi.append("Phục ngâm không khớp với nguyệt tướng = giờ")
    for s, v in dem.items():
        if v > n / 2:
            loi.append("Tất pháp phú điều %d khớp %.0f%% số khóa – điều kiện đáng ngờ" % (s, 100.0 * v / n))
    for t, v in dem_k.items():
        if v > n / 2:
            loi.append("khóa cách %s khớp %.0f%% số khóa – điều kiện đáng ngờ" % (t, 100.0 * v / n))
    tu_kiem.thong_ke = (n, dem, dem_k)
    return loi


if __name__ == "__main__":
    import time
    t0 = time.time()
    e = tu_kiem()
    n, dem, dem_k = tu_kiem.thong_ke
    print("tu_kiem: %d lỗi, %d khóa, %.2f s" % (len(e), n, time.time() - t0))
    for x in e[:30]:
        print("  " + x)
    if "--thong-ke" in sys.argv:
        for so, ten, _, _ in TAT_PHAP:
            print("%3d %-45s %6.2f%%" % (so, ten, 100.0 * dem[so] / n))
        for ten, _, _ in KHOA_CACH:
            print("    %-45s %6.2f%%" % (ten, 100.0 * dem_k[ten] / n))
