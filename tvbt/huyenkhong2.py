# -*- coding: utf-8 -*-
"""huyenkhong2.py - Huyền không phi tinh nâng cao (dùng kèm tvbt.py của skill tu-vi-bat-tu-phong-thuy-v2).

Lệnh con của tvbt/nc.py:
    huyenkhong --huong ĐỘ (--nam-xay N | --van V) [--nam-xem N] [--thang-xem M]
               [--nuoc "Đông,Đông Nam"] [--nui "Tây Bắc"] [--ban tu-dong|ha|the|ca-hai]

So với tvbt.huyen_khong (chỉ Hạ quái, kiêm hướng chỉ cảnh báo), module này làm thêm:
  1. Bàn Thế quái (Thay quái) theo bảng thay sao Tưởng Đại Hồng / Thẩm Trúc Nhưng, chọn bàn theo độ lệch.
  2. Thành môn quyết (chính / phó thành môn).
  3. Thất tinh đả kiếp (Ly cung = chân, Khảm cung = giả).
  4. Phục / phản ngâm, hợp thập, liên châu & phụ mẫu tam ban quái, nhập tù, cặp sao kinh điển, vượng suy.
  5. Chồng sao lưu niên / lưu nguyệt, Ngũ Hoàng, 2-5 hội, Thái Tuế, Tuế Phá.
  6. Đối chiếu nước / cửa (--nuoc) và núi / tường cao (--nui) với sơn tinh, hướng tinh.
Dùng lại hằng số và hàm của tvbt.py (SON24, CUNG_CUA_SON, VI_TRI, CUNG_SO, bay_sao, am_duong_son,
son_tu_do, van_nam, sao_nam, sao_thang, huyen_khong) – KHÔNG sửa tvbt.py. Không dùng mạng khi chạy.
"""
import datetime as dt
import io
import os
import re
import sys
import time
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tvbt as B  # noqa: E402

# ---------------------------------------------------------------- hằng số
CUNG9 = ["Giữa", "Bắc", "Đông Bắc", "Đông", "Đông Nam", "Nam", "Tây Nam", "Tây", "Tây Bắc"]
VONG8 = list(B.HUONG)                      # 8 cung theo chiều kim đồng hồ từ Bắc
LUOI = [("Đông Nam", "Nam", "Tây Nam"), ("Đông", "Giữa", "Tây"), ("Đông Bắc", "Bắc", "Tây Bắc")]
TEN_QUAI = {1: "Khảm", 2: "Khôn", 3: "Chấn", 4: "Tốn", 5: "Trung cung", 6: "Càn", 7: "Đoài", 8: "Cấn", 9: "Ly"}
TEN_SAO = {1: "Nhất Bạch", 2: "Nhị Hắc", 3: "Tam Bích", 4: "Tứ Lục", 5: "Ngũ Hoàng", 6: "Lục Bạch",
           7: "Thất Xích", 8: "Bát Bạch", 9: "Cửu Tử"}
TEN_THAY = {1: "Tham Lang", 2: "Cự Môn", 6: "Vũ Khúc", 7: "Phá Quân", 9: "Hữu Bật"}
NGUYEN = ("Địa nguyên", "Thiên nguyên", "Nhân nguyên")

# Bảng thay sao (Tưởng Đại Hồng, Thẩm Trúc Nhưng "Thẩm thị huyền không học"):
#   Tý Quý Giáp Thân → 1 Tham Lang; Nhâm Mão Ất Mùi Khôn → 2 Cự Môn; Càn Hợi Thìn Tốn Tỵ Tuất → 6 Vũ Khúc;
#   Dậu Tân Sửu Cấn Bính → 7 Phá Quân; Dần Ngọ Canh Đinh → 9 Hữu Bật.
# 11 sơn (Tý Quý Mùi Khôn Càn Hợi Tuất Dậu Tân Ngọ Đinh) thay ra đúng sao gốc của cung mình, nên bản
# "13 sơn" của phái Trung Châu cho kết quả giống hệt bản 24 sơn này (tu_kiem kiểm điều đó).
_NHOM_THAY = ((1, "Tý Quý Giáp Thân"), (2, "Nhâm Mão Ất Mùi Khôn"), (6, "Càn Hợi Thìn Tốn Tỵ Tuất"),
              (7, "Dậu Tân Sửu Cấn Bính"), (9, "Dần Ngọ Canh Đinh"))
SAO_THAY = {s: k for k, ds in _NHOM_THAY for s in ds.split()}
# sơn ở (số cung Lạc Thư, vị trí nguyên long)
SON_O = {(B.CUNG_SO[B.CUNG_CUA_SON[s]], B.VI_TRI[s]): s for s in B.SON24}

NGUONG_HA = 3.0       # lệch tâm sơn ≤ 3°: chỉ dùng Hạ quái
NGUONG_THE = 4.5      # 3–4,5°: in cả hai (mặc định Hạ quái); > 4,5°: Thế quái
KHONG_VONG = 1.0      # cách ranh giới hai sơn < 1° (lệch > 6,5°): Đại/Tiểu không vong – không lập bàn
GAN_RANH = 1.5        # cách ranh giới < 1,5°: nhắc đo lại (như v2)

NHOM_LY = ("Nam", "Đông", "Tây Bắc")       # Ly – Chấn – Càn (Lạc Thư 9-3-6)
NHOM_KHAM = ("Bắc", "Đông Nam", "Tây")     # Khảm – Tốn – Đoài (Lạc Thư 1-4-7)

# Cặp sao kinh điển (không phân thứ tự). Nghĩa ngắn; vượng/sinh thì nghiêng tốt, suy/tử thì nghiêng xấu.
CAP_SAO = {
    (1, 4): "Thủy sinh Mộc: học hành, thi cử, văn chương (suy thì dễ vướng chuyện tình cảm)",
    (1, 6): "Kim sinh Thủy (Hà đồ 1-6): quý nhân, thăng tiến, văn chương",
    (2, 2): "Nhị Hắc trùng: để ý sức khỏe",
    (2, 3): "Đấu ngưu (Mộc khắc Thổ): dễ cãi vã, thị phi, kiện tụng",
    (2, 5): "Hai sao bệnh khí gặp nhau: để ý sức khỏe, hao tổn",
    (2, 7): "Hà đồ 2-7 hợp Hỏa: vượng thì có tài, suy thì để ý hỏa khí",
    (3, 7): "Kim khắc Mộc: dễ mất mát, trộm cắp, va chạm",
    (5, 5): "Ngũ Hoàng trùng: cung cần giữ yên, tránh động thổ",
    (5, 9): "Hỏa sinh Thổ cho Ngũ Hoàng: tính xấu của sao 5 mạnh lên, để ý hỏa và sức khỏe",
    (6, 7): "Giao kiếm (hai Kim): dễ tranh chấp, va chạm",
    (6, 8): "Thổ sinh Kim: tài lộc, địa vị, quý nhân",
    (6, 9): "Hỏa khắc Kim: để ý người đứng đầu, đầu và phổi",
    (7, 9): "Hỏa khắc Kim: để ý hỏa hoạn, thị phi",
    (8, 9): "Hỏa sinh Thổ: hỷ sự, cưới hỏi, tài lộc",
}
_TU_CUNG = {"bac": "Bắc", "b": "Bắc", "dong bac": "Đông Bắc", "db": "Đông Bắc", "dong": "Đông", "d": "Đông",
            "dong nam": "Đông Nam", "dn": "Đông Nam", "nam": "Nam", "n": "Nam", "tay nam": "Tây Nam",
            "tn": "Tây Nam", "tay": "Tây", "t": "Tây", "tay bac": "Tây Bắc", "tb": "Tây Bắc"}
# 12 tiết mở đầu 12 tháng (tháng 1 = Dần ... tháng 12 = Sửu); khóa của lunar_python
_TIET = ["立春", "惊蛰", "清明", "立夏", "芒种", "小暑", "立秋", "白露", "寒露", "立冬", "大雪", "XIAO_HAN", "LI_CHUN"]
_TIET_VN = ["Lập Xuân", "Kinh Trập", "Thanh Minh", "Lập Hạ", "Mang Chủng", "Tiểu Thử", "Lập Thu", "Bạch Lộ",
            "Hàn Lộ", "Lập Đông", "Đại Tuyết", "Tiểu Hàn", "Lập Xuân"]


# ---------------------------------------------------------------- tính toán cơ bản
def am_duong(son):
    """+1 nếu sơn dương, -1 nếu sơn âm (theo tvbt.am_duong_son)."""
    return B.am_duong_son(B.CUNG_SO[B.CUNG_CUA_SON[son]], B.VI_TRI[son])


def _ad(x):
    return "dương" if x > 0 else "âm"


def phan_tich_huong(do):
    """Đổi độ la bàn ra sơn hướng / tọa, độ lệch tâm sơn, sơn kiêm sang, và mức kiêm:
    'ha' (≤3°), 'ca-hai' (3–4,5°), 'the' (>4,5°), 'khong-vong' (cách ranh giới < KHONG_VONG)."""
    do = do % 360
    huong, lech = B.son_tu_do(do)
    i = B.SON24.index(huong)
    toa = B.SON24[(i + 12) % 24]
    buoc = 1 if lech >= 0 else -1
    huong_kiem, toa_kiem = B.SON24[(i + buoc) % 24], B.SON24[(i + 12 + buoc) % 24]
    xuat_quai = B.CUNG_CUA_SON[huong_kiem] != B.CUNG_CUA_SON[huong]
    cach_ranh = 7.5 - abs(lech)
    if abs(lech) <= NGUONG_HA:
        muc = "ha"
    elif abs(lech) <= NGUONG_THE:
        muc = "ca-hai"
    elif cach_ranh > KHONG_VONG:
        muc = "the"
    else:
        muc = "khong-vong"
    return dict(do=do, huong=huong, toa=toa, lech=lech, cung_huong=B.CUNG_CUA_SON[huong],
                cung_toa=B.CUNG_CUA_SON[toa], huong_kiem=huong_kiem, toa_kiem=toa_kiem, xuat_quai=xuat_quai,
                cung_am_duong=am_duong(huong_kiem) == am_duong(huong), cach_ranh=cach_ranh, muc=muc)


def khoi_sao(sao_van, son, the_quai):
    """Khởi sao nhập trung cho sơn bàn / hướng bàn.
    sao_van: vận tinh ở cung tọa (hoặc hướng); son: sơn tọa (hoặc hướng).
    Hạ quái: sao_van nhập trung; thuận/nghịch theo âm dương của sơn cùng nguyên long trong cung gốc của
    sao_van (sao 5 không có cung gốc → lấy chính sơn tọa/hướng).
    Thế quái: tra sơn nguyên long đó trong bảng thay sao → sao thay nhập trung, thuận/nghịch VẪN theo âm dương
    của sơn nguyên long đó (không theo cung của sao thay). Sao 5: không thay (mặc định phổ biến)."""
    vt = B.VI_TRI[son]
    if sao_van == 5:
        nl, vao = son, 5
    else:
        nl = SON_O[(sao_van, vt)]
        vao = SAO_THAY[nl] if the_quai else sao_van
    ad = am_duong(nl)
    return dict(sao_van=sao_van, nguyen_long=nl, vao=vao, thuan=ad > 0, ban=B.bay_sao(vao, ad > 0),
                the_quai=the_quai)


def lap_ban(do, van, the_quai=False):
    """Lập bàn Huyền không (vận bàn, sơn bàn, hướng bàn) cho nhà hướng `do` độ, vận `van`."""
    ph = phan_tich_huong(do)
    vb = B.bay_sao(van, True)
    ks = khoi_sao(vb[ph["cung_toa"]], ph["toa"], the_quai)
    kh = khoi_sao(vb[ph["cung_huong"]], ph["huong"], the_quai)
    return dict(ph, van=van, the_quai=the_quai, van_ban=vb, son=ks["ban"], huong_tinh=kh["ban"],
                khoi_son=ks, khoi_huong=kh)


def ten_cuc(ban):
    """Bốn cục chính theo sao đương vận của nhà."""
    v, ct, ch = ban["van"], ban["cung_toa"], ban["cung_huong"]
    s, h = ban["son"], ban["huong_tinh"]
    if s[ct] == v and h[ch] == v:
        return "Vượng sơn vượng hướng"
    if s[ch] == v and h[ch] == v:
        return "Song tinh đáo hướng"
    if s[ct] == v and h[ct] == v:
        return "Song tinh đáo tọa"
    if s[ch] == v and h[ct] == v:
        return "Thượng sơn hạ thủy"
    return "không thuộc 4 cục chính"


def trang_thai(sao, van):
    """Vượng / sinh / tiến / thoái / suy / tử của một sao so với vận; sao 5 (ngoài vận 5) ghi 'sát'."""
    if sao == 5 and van != 5:
        return "sát"
    return {0: "vượng", 1: "sinh", 2: "tiến", 8: "thoái", 7: "suy"}.get((sao - van) % 9, "tử")


def tot(sao, van):
    return trang_thai(sao, van) in ("vượng", "sinh", "tiến")


def ngam_toan_ban(b):
    """'phục ngâm' nếu cả bàn trùng Lạc Thư gốc, 'phản ngâm' nếu đối nghịch Lạc Thư gốc, None nếu không."""
    if all(b[c] == B.CUNG_SO[c] for c in CUNG9):
        return "phục ngâm"
    if all(b[c] == 10 - B.CUNG_SO[c] for c in CUNG9):
        return "phản ngâm"
    return None


def hop_thap_toan_ban(ban):
    """Danh sách tên các kiểu hợp thập toàn bàn (mọi cung cộng lại bằng 10)."""
    vb, s, h = ban["van_ban"], ban["son"], ban["huong_tinh"]
    kq = []
    for ten, x, y in (("sơn tinh + vận tinh", s, vb), ("hướng tinh + vận tinh", h, vb), ("sơn tinh + hướng tinh", s, h)):
        if all(x[c] + y[c] == 10 for c in CUNG9):
            kq.append(ten)
    return kq


def tam_ban(ban):
    """'liên châu' nếu mọi cung có 3 sao (vận, sơn, hướng) liền nhau (vd 6-7-8, 8-9-1);
    'phụ mẫu' nếu mọi cung thành 1-4-7 / 2-5-8 / 3-6-9; None nếu không."""
    def lien(t):
        return len(set(t)) == 3 and any(set(t) == {a, a % 9 + 1, (a + 1) % 9 + 1} for a in range(1, 10))

    def pm(t):
        return len(set(t)) == 3 and len({x % 3 for x in t}) == 1
    bo = [(ban["van_ban"][c], ban["son"][c], ban["huong_tinh"][c]) for c in CUNG9]
    if all(lien(t) for t in bo):
        return "liên châu"
    if all(pm(t) for t in bo):
        return "phụ mẫu"
    return None


def da_kiep(ban):
    """Thất tinh đả kiếp theo Thẩm thị (đối chiếu danh sách 31 cục của xuankongguan.com):
    điều kiện: song tinh đáo hướng (sơn tinh và hướng tinh đương vận cùng ở cung hướng);
    cung hướng thuộc Ly–Chấn–Càn → Ly cung đả kiếp (chân); thuộc Khảm–Tốn–Đoài → Khảm cung đả kiếp (giả);
    hướng Cấn / Khôn → không có đả kiếp; sơn bàn hoặc hướng bàn phục ngâm → loại.
    Ghi chú: hướng tinh (và sơn tinh, vận tinh) của 3 cung trong một nhóm LUÔN thành tam ban (1-4-7/2-5-8/3-6-9)
    với mọi bàn phi tinh, nên điều kiện quyết định là song tinh đáo hướng + vị trí cung hướng."""
    v, ch = ban["van"], ban["cung_huong"]
    song = ban["son"][ch] == v and ban["huong_tinh"][ch] == v
    if ch in NHOM_LY:
        nhom, loai = NHOM_LY, "Ly cung đả kiếp (chân đả kiếp)"
    elif ch in NHOM_KHAM:
        nhom, loai = NHOM_KHAM, "Khảm cung đả kiếp (giả đả kiếp)"
    else:
        nhom, loai = None, None
    phuc = [t for t, b in (("sơn bàn", ban["son"]), ("hướng bàn", ban["huong_tinh"])) if ngam_toan_ban(b) == "phục ngâm"]
    phan = [t for t, b in (("sơn bàn", ban["son"]), ("hướng bàn", ban["huong_tinh"])) if ngam_toan_ban(b) == "phản ngâm"]
    sao3 = [ban["huong_tinh"][c] for c in nhom] if nhom else []
    return dict(co=bool(song and nhom and not phuc), song=song, nhom=nhom, loai=loai, sao3=sao3, phuc=phuc,
                phan=phan, chan=nhom == NHOM_LY)


def thanh_mon(huong, van):
    """Thành môn quyết. Hai cung kề cung hướng (trên vòng 8 cung); cung nào cùng cung hướng thành cặp
    Hà đồ 1-6/2-7/3-8/4-9 là chính thành môn, cung kia là phó. Sơn thành môn là sơn cùng nguyên long với sơn hướng.
    Lấy vận tinh ở cung đó nhập trung, thuận/nghịch theo âm dương của sơn cùng nguyên long trong cung gốc của
    vận tinh ấy (vận tinh là 5 → theo âm dương chính sơn thành môn; phái khác theo sơn hướng – trả thêm 'khac').
    Sao đương vận bay về đúng cung đó → thành môn dùng được (thực chất: chỉ khi bay nghịch)."""
    ch = B.CUNG_CUA_SON[huong]
    n, vt = B.CUNG_SO[ch], B.VI_TRI[huong]
    k = VONG8.index(ch)
    vb = B.bay_sao(van, True)
    kq = []
    for c in (VONG8[(k - 1) % 8], VONG8[(k + 1) % 8]):
        m = B.CUNG_SO[c]
        son_tm = SON_O[(m, vt)]
        x = vb[c]
        nl = son_tm if x == 5 else SON_O[(x, vt)]
        thuan = am_duong(nl) > 0
        den = B.bay_sao(x, thuan)[c]
        khac = None
        if x == 5:
            t2 = am_duong(huong) > 0
            d2 = B.bay_sao(5, t2)[c]
            khac = dict(thuan=t2, den=d2, dung=d2 == van)
        kq.append(dict(cung=c, chinh=abs(n - m) == 5, son=son_tm, sao_van=x, nguyen_long=nl, thuan=thuan,
                       den=den, dung=den == van, khac=khac))
    kq.sort(key=lambda d: not d["chinh"])
    return kq


# ---------------------------------------------------------------- lịch: năm Lập Xuân, tháng tiết
_CACHE_TIET = {}


def bang_tiet(nam):
    """13 mốc tiết (giờ Việt Nam UTC+7) mở đầu 12 tháng tiết của năm Lập Xuân `nam` (mốc cuối = Lập Xuân năm sau)."""
    if nam not in _CACHE_TIET:
        bang = B.Solar.fromYmd(nam, 6, 1).getLunar().getJieQiTable()
        ds = []
        for k in _TIET:
            s = bang[k]
            ds.append(dt.datetime(s.getYear(), s.getMonth(), s.getDay(), s.getHour(), s.getMinute())
                      - dt.timedelta(hours=1))       # thư viện tính theo giờ Bắc Kinh (UTC+8)
        _CACHE_TIET[nam] = ds
    return _CACHE_TIET[nam]


def nam_lap_xuan(t):
    """Năm phong thủy (từ Lập Xuân) chứa thời điểm t (datetime giờ Việt Nam)."""
    return t.year if t >= bang_tiet(t.year)[0] else t.year - 1


def sao_luu(nam, thang=None):
    """(niên tinh, nguyệt tinh hoặc None) của năm Lập Xuân `nam`, tháng tiết `thang` (1 = Dần ... 12 = Sửu)."""
    nt = B.sao_nam(nam)
    return nt, (B.sao_thang((nam - 4) % 12, thang) if thang else None)


# ---------------------------------------------------------------- in
def _o(ban, c):
    tag = " (HƯỚNG)" if c == ban["cung_huong"] else (" (TỌA)" if c == ban["cung_toa"] else "")
    return "%s%s: S%d H%d V%d" % (c, tag, ban["son"][c], ban["huong_tinh"][c], ban["van_ban"][c])


def in_luoi(ban, tieu_de):
    """Lưới 3×3 kiểu sách (Nam ở trên). S = sơn tinh, H = hướng tinh, V = vận tinh."""
    print(tieu_de)
    for i, hang in enumerate(LUOI):
        print("| " + " | ".join(_o(ban, c) for c in hang) + " |")
        if i == 0:
            print("|---|---|---|")


def _dong_khoi(ten, k, cung, son):
    """Một dòng giải thích cách khởi sao nhập trung."""
    if k["sao_van"] == 5:
        s = ("%s: vận tinh ở %s (%s) là 5 (Ngũ Hoàng, không có cung gốc) → lấy âm dương của chính sơn %s (%s)"
             % (ten, "tọa" if ten == "Sơn bàn" else "hướng", cung, son, _ad(am_duong(son))))
        if k["the_quai"]:
            s += ("; thế quái: sao 5 không thay (mặc định phổ biến; có phái thay bằng sao của chính sơn %s là %d)"
                  % (son, SAO_THAY[son]))
    else:
        nl = k["nguyen_long"]
        s = ("%s: vận tinh ở %s (%s) là %d → cung %d (%s), sơn %s là %s (%s)"
             % (ten, "tọa" if ten == "Sơn bàn" else "hướng", cung, k["sao_van"], k["sao_van"],
                TEN_QUAI[k["sao_van"]], NGUYEN[B.VI_TRI[son]], nl, _ad(am_duong(nl))))
        if k["the_quai"]:
            s += ("; thế quái: %s thay bằng %d %s" % (nl, k["vao"], TEN_THAY[k["vao"]]) if k["vao"] != k["sao_van"]
                  else "; thế quái: %s thay ra đúng sao %d (không đổi)" % (nl, k["vao"]))
    return "- %s → %d nhập trung bay %s." % (s, k["vao"], "thuận" if k["thuan"] else "nghịch")


def in_ban(ban, tieu_de):
    in_luoi(ban, tieu_de)
    print(_dong_khoi("Sơn bàn", ban["khoi_son"], ban["cung_toa"], ban["toa"]))
    print(_dong_khoi("Hướng bàn", ban["khoi_huong"], ban["cung_huong"], ban["huong"]))
    print("- Cục: %s." % ten_cuc(ban))


def nhan_dien(ban):
    """Các dòng nhận diện cách cục của một bàn."""
    L = []
    v, ch, ct = ban["van"], ban["cung_huong"], ban["cung_toa"]
    L.append("- Cục: %s (theo sao %d đương vận của nhà)." % (ten_cuc(ban), v))
    for ten, b in (("Sơn bàn", ban["son"]), ("Hướng bàn", ban["huong_tinh"])):
        g = ngam_toan_ban(b)
        if g:
            L.append("! %s: Ngũ Hoàng nhập trung bay %s → toàn bàn %s (%s Lạc Thư gốc). Sách xếp là cách xấu, "
                     "cần xét kỹ hình thế khi luận." % (ten, "thuận" if g == "phục ngâm" else "nghịch", g.upper(),
                                                        "trùng" if g == "phục ngâm" else "đối nghịch"))
        if v != 5 and all(b[c] == ban["van_ban"][c] for c in CUNG9):
            L.append("! %s trùng hệt vận bàn (sao và vận cùng một số ở mọi cung)." % ten)
    ht = hop_thap_toan_ban(ban)
    if ht:
        L.append("- Hợp thập toàn bàn: %s = 10 ở cả 9 cung (cách thông khí, sách xếp là tốt)." % "; ".join(ht))
    else:
        loc = []
        if ban["huong_tinh"][ch] + ban["van_ban"][ch] == 10:
            loc.append("hướng tinh + vận tinh ở cung hướng")
        if ban["son"][ct] + ban["van_ban"][ct] == 10:
            loc.append("sơn tinh + vận tinh ở cung tọa")
        if ban["son"][ch] + ban["huong_tinh"][ch] == 10:
            loc.append("sơn tinh + hướng tinh ở cung hướng")
        if loc:
            L.append("- Hợp thập riêng: %s = 10 (không phải toàn bàn)." % "; ".join(loc))
    tb = tam_ban(ban)
    if tb == "liên châu":
        L.append("- Liên châu tam ban quái: mọi cung có vận, sơn, hướng là 3 số liền nhau (cách thông khí).")
    elif tb == "phụ mẫu":
        L.append("- Phụ mẫu tam ban quái: mọi cung có vận, sơn, hướng thành 1-4-7 / 2-5-8 / 3-6-9 (cách thông khí).")
    dk = da_kiep(ban)
    if dk["co"]:
        L.append("- THẤT TINH ĐẢ KIẾP: %s. Song tinh %d đáo hướng %s; hướng tinh ở %s = %s." % (
            dk["loai"], v, ch, "–".join(dk["nhom"]), "-".join(str(x) for x in dk["sao3"])))
        L.append("  Điều kiện dùng được: cung hướng có cửa/nước thật, và ba cung %s thông khí với nhau (cửa, lối đi, "
                 "không bị bịt). Chỉ có hiệu lực trong vận %d." % ("–".join(dk["nhom"]), v))
        if not dk["chan"]:
            L.append("! Khảm cung đả kiếp là 'giả đả kiếp': nhiều phái coi là yếu hoặc không dùng; một nguồn còn loại "
                     "các cục hướng chính Bắc. Nói rõ khi luận.")
        if dk["phan"]:
            L.append("! %s phản ngâm: có phái (Trần Phong Mưu) cho rằng gặp phản/phục ngâm thì không dùng đả kiếp."
                     % " và ".join(dk["phan"]))
    elif dk["song"] and dk["nhom"] and dk["phuc"]:
        L.append("- Song tinh đáo hướng nhưng %s phục ngâm → không dùng được thất tinh đả kiếp." % " và ".join(dk["phuc"]))
    elif dk["song"] and not dk["nhom"]:
        L.append("- Song tinh đáo hướng nhưng hướng ở Cấn/Khôn → không có thất tinh đả kiếp.")
    else:
        L.append("- Không có thất tinh đả kiếp (cần song tinh đáo hướng).")
    hc = ban["huong_tinh"]["Giữa"]
    if hc == 5:
        L.append("- Hướng tinh ở trung cung là 5: các phái nói khác nhau về nhập tù, không kết luận.")
    else:
        sau = (hc - v) % 9
        L.append("- Nhập tù: hướng tinh ở trung cung là %d → đến vận %d (sau %d vận) nhà 'nhập tù' theo Thẩm thị; "
                 "giữa nhà có giếng trời/khoảng trống lớn thì có phái cho là không tù." % (hc, hc, sau))
    return L


def tom_tat(ban):
    """Một dòng tóm tắt bàn đối chiếu."""
    x = [ten_cuc(ban)]
    for ten, b in (("sơn bàn", ban["son"]), ("hướng bàn", ban["huong_tinh"])):
        g = ngam_toan_ban(b)
        if g:
            x.append("%s %s" % (ten, g))
    ht = hop_thap_toan_ban(ban)
    if ht:
        x.append("hợp thập (%s)" % "; ".join(ht))
    tb = tam_ban(ban)
    if tb:
        x.append(tb + " tam ban quái")
    dk = da_kiep(ban)
    if dk["co"]:
        x.append(dk["loai"])
    return ", ".join(x)


def in_thanh_mon(huong, van, nuoc, ghi=""):
    print("| Cung | Loại | Sơn thành môn | Vận tinh ở cung | Sơn nguyên long (âm dương) | Bay | Sao đến cung | Kết luận |")
    print("|---|---|---|---|---|---|---|---|")
    kq = thanh_mon(huong, van)
    for d in kq:
        print("| %s | %s | %s | %d | %s (%s) | %s | %d | %s |" % (
            d["cung"], "chính" if d["chinh"] else "phó", d["son"], d["sao_van"], d["nguyen_long"],
            _ad(am_duong(d["nguyen_long"])), "thuận" if d["thuan"] else "nghịch", d["den"],
            "DÙNG ĐƯỢC" if d["dung"] else "không dùng được"))
    for d in kq:
        if d["khac"] and d["khac"]["dung"] != d["dung"]:
            print("! Cung %s: vận tinh là 5 – có phái lấy âm dương của sơn hướng %s (bay %s) thì kết luận ngược lại "
                  "(%s)." % (d["cung"], huong, "thuận" if d["khac"]["thuan"] else "nghịch",
                             "dùng được" if d["khac"]["dung"] else "không dùng được"))
    dung = [d for d in kq if d["dung"]]
    if dung:
        for d in dung:
            co = d["cung"] in nuoc
            print("- Thành môn %s ở %s (sơn %s)%s: %s" % (
                "chính" if d["chinh"] else "phó", d["cung"], d["son"], ghi,
                ("đã có nước/cửa/đường theo --nuoc → nạp được vượng khí vận %d." % van) if co else
                ("chỉ phát huy khi ở đó có cửa, lối đi, ngã ba đường hoặc nước thật; nếu không có thì không tính.")))
    else:
        print("- Không có thành môn dùng được%s." % ghi)


def in_cap_sao(ban, van_xet):
    print("| Cung | Vận tinh | Sơn tinh | Hướng tinh | Cặp sơn–hướng | Gợi ý nghĩa |")
    print("|---|---|---|---|---|---|")
    for c in CUNG9:
        s, h = ban["son"][c], ban["huong_tinh"][c]
        nghia = CAP_SAO.get((min(s, h), max(s, h)), "")
        tag = " (HƯỚNG)" if c == ban["cung_huong"] else (" (TỌA)" if c == ban["cung_toa"] else "")
        print("| %s%s | %d | %d (%s) | %d (%s) | %d-%d | %s |" % (
            c, tag, ban["van_ban"][c], s, trang_thai(s, van_xet), h, trang_thai(h, van_xet), s, h, nghia or "–"))


def in_luu_nien(ban, nam, thang):
    bt = bang_tiet(nam)
    nt, ng = sao_luu(nam, thang)
    chi = (nam - 4) % 12
    tt_son, tp_son = B.CHI_VN[chi], B.CHI_VN[(chi + 6) % 12]
    tt_cung, tp_cung = B.CUNG_CUA_SON[tt_son], B.CUNG_CUA_SON[tp_son]
    nb = B.bay_sao(nt, True)
    gb = B.bay_sao(ng, True) if ng else None
    print("LƯU NIÊN NĂM %d (từ Lập Xuân %s đến trước Lập Xuân %s, giờ Việt Nam)%s" % (
        nam, bt[0].strftime("%H:%M %d/%m/%Y"), bt[12].strftime("%H:%M %d/%m/%Y"),
        (" – LƯU NGUYỆT THÁNG %d (tháng %s, từ %s %s đến trước %s %s)" % (
            thang, B.CHI_VN[(thang + 1) % 12], _TIET_VN[thang - 1], bt[thang - 1].strftime("%d/%m/%Y"),
            _TIET_VN[thang], bt[thang].strftime("%d/%m/%Y"))) if thang else ""))
    print("- Niên tinh nhập trung: %d %s%s. Thái Tuế ở sơn %s (cung %s), Tuế Phá ở sơn %s (cung %s)." % (
        nt, TEN_SAO[nt], ("; nguyệt tinh nhập trung: %d %s" % (ng, TEN_SAO[ng])) if ng else "",
        tt_son, tt_cung, tp_son, tp_cung))
    print("| Cung | Sơn | Hướng | Vận | Niên | %sĐánh dấu |" % ("Nguyệt | " if ng else ""))
    print("|---|---|---|---|---|%s---|" % ("---|" if ng else ""))
    for c in CUNG9:
        s, h, v, n = ban["son"][c], ban["huong_tinh"][c], ban["van_ban"][c], nb[c]
        g = gb[c] if gb else None
        dau = []
        if n == 5:
            dau.append("Ngũ Hoàng năm")
        if g == 5:
            dau.append("Ngũ Hoàng tháng")
        if n == 2:
            dau.append("Nhị Hắc năm")
        luu = [x for x in (n, g) if x]
        nha = {s, h}
        if 2 in nha | set(luu) and 5 in nha | set(luu) and (2 in luu or 5 in luu) and not {2, 5} <= nha:
            dau.append("2-5 hội")
        elif {2, 5} <= nha:
            dau.append("2-5 sẵn ở bàn nhà")
        if c == tt_cung:
            dau.append("Thái Tuế (%s)" % tt_son)
        if c == tp_cung:
            dau.append("Tuế Phá (%s)" % tp_son)
        tag = " (HƯỚNG)" if c == ban["cung_huong"] else (" (TỌA)" if c == ban["cung_toa"] else "")
        print("| %s%s | %d | %d | %d | %d | %s%s |" % (c, tag, s, h, v, n, ("%d | " % g) if gb else "",
                                                       ", ".join(dau) or "–"))
    print("- Cung có Ngũ Hoàng, 2-5 hội, Thái Tuế, Tuế Phá: tránh động thổ, đục phá, sửa lớn trong năm/tháng đó; "
          "giữ yên là chính.")


def doc_phuong(s):
    """Đọc danh sách phương: 'Đông,Đông Nam' / 'dong nam; tb' → ['Đông', 'Đông Nam', 'Tây Bắc']."""
    if not s:
        return []
    kq = []
    for x in re.split(r"[,;/+]+", s):
        k = B.bo_dau(x) if x.strip() else ""
        if not k:
            continue
        if k in ("giua", "trung cung", "giua nha"):
            print("! Bỏ qua '%s': chỉ xét 8 phương quanh nhà." % x.strip())
            continue
        if k not in _TU_CUNG:
            raise SystemExit("LỖI: không hiểu phương '%s'. Dùng: Bắc, Đông Bắc, Đông, Đông Nam, Nam, Tây Nam, Tây, "
                             "Tây Bắc (hoặc viết tắt B, ĐB, Đ, ĐN, N, TN, T, TB), cách nhau dấu phẩy." % x.strip())
        if _TU_CUNG[k] not in kq:
            kq.append(_TU_CUNG[k])
    return kq


def in_son_thuy(ban, van_xet, nuoc, nui):
    huong_tot = [c for c in VONG8 if tot(ban["huong_tinh"][c], van_xet)]
    son_tot = [c for c in VONG8 if tot(ban["son"][c], van_xet)]
    print("SƠN THỦY THỰC TẾ (vượng/sinh/tiến tính theo vận %d)" % van_xet)
    print("- Hướng tinh vượng/sinh ở: %s → hợp có cửa, lối đi, sân trống hoặc nước (lợi tài)." % (
        ", ".join("%s (%d)" % (c, ban["huong_tinh"][c]) for c in huong_tot) or "không cung nào"))
    print("- Sơn tinh vượng/sinh ở: %s → hợp có tường cao, nhà cao, núi, chỗ yên tĩnh (lợi người, sức khỏe)." % (
        ", ".join("%s (%d)" % (c, ban["son"][c]) for c in son_tot) or "không cung nào"))
    if not nuoc and not nui:
        print("- (Chưa có --nuoc / --nui: hỏi người dùng phương nào có cửa, đường, nước; phương nào có nhà cao, tường, núi.)")
        return
    for c in nuoc:
        h, s = ban["huong_tinh"][c], ban["son"][c]
        th, ts = trang_thai(h, van_xet), trang_thai(s, van_xet)
        if tot(h, van_xet):
            x = "hướng tinh %d (%s) gặp nước/cửa → lợi tài" % (h, th)
        elif th == "thoái":
            x = "hướng tinh %d (thoái) gặp nước/cửa → tài lực giảm dần, bình thường" % h
        else:
            x = "hướng tinh %d (%s) gặp nước/cửa động → không lợi; nên hạn chế làm cửa chính, để nước động" % (h, th)
        if tot(s, van_xet):
            x += "; sơn tinh %d (%s) rơi xuống nước → bất lợi về người (sức khỏe, nhân đinh)" % (s, ts)
        print("- Nước/cửa ở %s: %s." % (c, x))
    for c in nui:
        h, s = ban["huong_tinh"][c], ban["son"][c]
        th, ts = trang_thai(h, van_xet), trang_thai(s, van_xet)
        x = ("sơn tinh %d (%s) gặp núi/tường cao → lợi người" % (s, ts) if tot(s, van_xet)
             else "sơn tinh %d (%s) gặp núi/tường cao → không thêm lợi về người" % (s, ts))
        if tot(h, van_xet):
            x += "; hướng tinh %d (%s) bị chắn → tài khí khó vào" % (h, th)
        print("- Núi/tường cao ở %s: %s." % (c, x))
    thieu = [c for c in huong_tot if c not in nuoc]
    if thieu and nuoc:
        print("- Cung hướng tinh tốt chưa có nước/cửa: %s – có thể cân nhắc mở lối đi/cửa phụ nếu hợp hình thế." %
              ", ".join(thieu))


def in_huyen_khong(do, van, nguon_van, nam_xem, thang=None, nuoc=(), nui=(), ban_chon="tu-dong", nam_xay=None):
    """In toàn bộ phần Huyền không nâng cao."""
    ph = phan_tich_huong(do)
    van_ht = B.van_nam(nam_xem)
    print("HUYỀN KHÔNG PHI TINH NÂNG CAO – NHÀ HƯỚNG %.1f°" % ph["do"])
    print("- Hướng: sơn %s (cung %s, %s, %s); tọa: sơn %s (cung %s, %s, %s)." % (
        ph["huong"], ph["cung_huong"], NGUYEN[B.VI_TRI[ph["huong"]]], _ad(am_duong(ph["huong"])),
        ph["toa"], ph["cung_toa"], NGUYEN[B.VI_TRI[ph["toa"]]], _ad(am_duong(ph["toa"]))))
    if abs(ph["lech"]) >= 0.05:
        print("- Lệch tâm sơn %+.1f° → nghiêng về sơn %s (hướng) / %s (tọa): %s, %s âm dương." % (
            ph["lech"], ph["huong_kiem"], ph["toa_kiem"],
            "kiêm sang quái khác (xuất quái)" if ph["xuat_quai"] else "trong cùng quái",
            "cùng" if ph["cung_am_duong"] else "khác"))
    else:
        print("- Đúng tâm sơn (lệch %+.1f°)." % ph["lech"])
    print("- Vận nhà: %d (%s). Năm xem %d thuộc vận %d." % (van, nguon_van, nam_xem, van_ht))
    if nam_xay is not None and nguon_van.startswith("theo năm") and nam_xay in (1864 + 20 * k for k in range(1, 12)):
        print("! Năm %d là năm chuyển vận (đổi vận từ Lập Xuân ~4/2): nếu xây xong/nhập trạch trước Lập Xuân thì là "
              "vận %d – chạy lại với --van %d." % (nam_xay, (van - 2) % 9 + 1, (van - 2) % 9 + 1))
    if van == 5:
        print("! Vận 5: nhiều phái chia 10 năm đầu theo vận 4, 10 năm sau theo vận 6 – nói rõ khi luận.")
    if ph["muc"] == "khong-vong":
        loai = "ĐẠI KHÔNG VONG (ranh giới hai quái)" if ph["xuat_quai"] else "TIỂU KHÔNG VONG (ranh giới hai sơn cùng quái)"
        print("! Hướng chỉ cách ranh giới giữa sơn %s và sơn %s %.1f° (< %.0f°): phạm %s. Không lập bàn. Đo lại bằng "
              "la bàn ở vài điểm (tránh xa sắt thép, xe, điện); nếu đúng là sát vạch thì sách khuyên không dùng hướng "
              "này. Có số đo mới thì chạy lại." % (ph["huong"], ph["huong_kiem"], ph["cach_ranh"], KHONG_VONG, loai))
        print()
        return
    ha = lap_ban(do, van, False)
    the = lap_ban(do, van, True)
    trung = ha["son"] == the["son"] and ha["huong_tinh"] == the["huong_tinh"]
    if ban_chon == "ha":
        chinh, phu = ha, None
    elif ban_chon == "the":
        chinh, phu = the, ha
    elif ban_chon == "ca-hai":
        chinh, phu = (ha, the) if ph["muc"] in ("ha", "ca-hai") else (the, ha)
    else:
        chinh, phu = {"ha": (ha, None), "ca-hai": (ha, the), "the": (the, ha)}[ph["muc"]]
    a = abs(ph["lech"])
    if ph["muc"] == "ha":
        print("- Chọn bàn: lệch %.1f° ≤ 3° → dùng HẠ QUÁI." % a)
    elif ph["muc"] == "ca-hai":
        print("- Chọn bàn: lệch %.1f° (3–4,5°) → mặc định HẠ QUÁI; có phái đã dùng THẾ QUÁI từ mức này – in cả hai." % a)
    else:
        print("- Chọn bàn: lệch %.1f° > 4,5° → KIÊM HƯỚNG, dùng THẾ QUÁI (Thay quái); hạ quái in kèm để đối chiếu." % a)
    if ban_chon != "tu-dong":
        print("- Theo yêu cầu --ban %s: bàn chính là %s." % (ban_chon, "THẾ QUÁI" if chinh["the_quai"] else "HẠ QUÁI"))
    if ph["muc"] in ("ca-hai", "the"):
        if not ph["xuat_quai"] and ph["cung_am_duong"]:
            print("! Phái Trung Châu (Vương Đình Chi): %s kiêm %s cùng quái, cùng âm dương thì KHÔNG dùng thế quái – "
                  "theo phái này dùng bàn hạ quái." % (ph["huong"], ph["huong_kiem"]))
        if ph["xuat_quai"]:
            print("! Kiêm sang quái khác (xuất quái, 'sai thác'): khí không thuần; nhiều sách khuyên tránh hoặc phải xét "
                  "kỹ hình thế.")
    if ph["cach_ranh"] < GAN_RANH:
        print("! Hướng cách ranh giới sơn bên cạnh chỉ %.1f°: nên đo lại cho chắc trước khi luận." % ph["cach_ranh"])
    if trung and (phu is not None or chinh["the_quai"]):
        print("- Thế quái của cục này thay ra đúng sao gốc ở cả sơn bàn và hướng bàn → thế quái TRÙNG hạ quái, "
              "chỉ có một bàn.")
        phu = None
    print()
    for b in sorted([x for x in (chinh, phu) if x], key=lambda x: x["the_quai"]):
        in_ban(b, "BÀN %s%s – vận %d, %s sơn %s hướng" % (
            "THẾ QUÁI" if b["the_quai"] else "HẠ QUÁI", " (CHÍNH)" if b is chinh and phu else
            (" (ĐỐI CHIẾU)" if b is phu else ""), van, ph["toa"], ph["huong"]))
        print()
    print("NHẬN DIỆN CÁCH CỤC (bàn %s)" % ("thế quái" if chinh["the_quai"] else "hạ quái"))
    for x in nhan_dien(chinh):
        print(x)
    if phu:
        print("- Bàn %s (đối chiếu): %s." % ("thế quái" if phu["the_quai"] else "hạ quái", tom_tat(phu)))
    print()
    print("THÀNH MÔN QUYẾT (vận bàn %d; sơn thành môn cùng nguyên long với sơn hướng %s)" % (van, ph["huong"]))
    in_thanh_mon(ph["huong"], van, nuoc)
    if van_ht != van:
        print("- Theo vận đang hành %d (có phái tính thành môn theo vận hiện tại vì thành môn nạp khí của thời vận):"
              % van_ht)
        in_thanh_mon(ph["huong"], van_ht, nuoc, " (theo vận %d)" % van_ht)
    print()
    print("CẶP SAO TỪNG CUNG (vượng/sinh/tiến/thoái/suy/tử/sát tính theo vận %d%s)" % (
        van_ht, "" if van_ht == van else "; nhà vận %d" % van))
    in_cap_sao(chinh, van_ht)
    print("- Nghĩa cặp sao chỉ là gợi ý: sao vượng/sinh thì nghiêng nghĩa tốt, suy/tử thì nghiêng nghĩa xấu; "
          "phải xem cung đó dùng làm gì (cửa, phòng ngủ, bếp) và có nước/núi hay không.")
    print()
    in_luu_nien(chinh, nam_xem, thang)
    print()
    in_son_thuy(chinh, van_ht, list(nuoc), list(nui))
    print()
    import linhchinh as LC
    import toason as TS
    LC.in_bang(nam_xem, TS.doc_son("%.2f" % ((do + 180) % 360))[0], list(nuoc), list(nui), gon=True)
    print("(Linh thần – chính thần chỉ để đối chiếu; cách dùng và chỗ các phái khác nhau: nc.py linhchinh, "
          "docs/huyen-khong.md mục 4.2.)")
    print()


# ---------------------------------------------------------------- CLI
def them_lenh(sub):
    p = sub.add_parser("huyenkhong", help="Huyền không nâng cao: hạ quái + thế quái, thành môn, đả kiếp, "
                                          "cặp sao, chồng sao lưu niên/lưu nguyệt")
    p.add_argument("--huong", type=float, required=True, help="độ hướng nhà đo bằng la bàn (0-360, độ từ Bắc)")
    p.add_argument("--nam-xay", type=int, help="năm xây xong / nhập trạch / sửa lớn (để lấy vận)")
    p.add_argument("--van", type=int, choices=range(1, 10), metavar="1-9", help="ép vận của nhà (1-9)")
    p.add_argument("--nam-xem", type=int, help="năm xem lưu niên (tính từ Lập Xuân); mặc định năm hiện tại")
    p.add_argument("--thang-xem", type=int, choices=range(1, 13), metavar="1-12",
                   help="tháng tiết khí để xem lưu nguyệt: 1 = tháng Dần (từ Lập Xuân ~4/2) ... 12 = tháng Sửu "
                        "(từ Tiểu Hàn ~6/1 năm sau). Tháng dương lịch M phần lớn ứng với tháng tiết M-1")
    p.add_argument("--nuoc", help="các phương có nước / cửa / đường thật, vd \"Đông,Đông Nam\"")
    p.add_argument("--nui", help="các phương có núi / nhà cao / tường cao, vd \"Tây Bắc\"")
    p.add_argument("--ban", default="tu-dong", choices=["tu-dong", "ha", "the", "ca-hai"],
                   help="chọn bàn: tu-dong theo độ lệch (mặc định), ha, the, ca-hai")
    p.set_defaults(_chay=chay)


def chay(a):
    if not -1e6 < a.huong < 1e6:            # loại nan, inf
        raise SystemExit("LỖI: --huong phải là số độ (0-360).")
    if a.van is None and a.nam_xay is None:
        raise SystemExit("LỖI: cần --nam-xay (năm xây xong/nhập trạch) hoặc --van để biết vận của nhà. "
                         "Hãy hỏi người dùng.")
    if a.van is not None:
        van, nguon = a.van, "theo --van"
        if a.nam_xay is not None and B.van_nam(a.nam_xay) != a.van:
            print("! --van %d khác vận của năm %d (vận %d): đang dùng --van." % (a.van, a.nam_xay, B.van_nam(a.nam_xay)))
    else:
        van, nguon = B.van_nam(a.nam_xay), "theo năm xây/nhập trạch %d" % a.nam_xay
    if a.nam_xem is None:
        now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None) + dt.timedelta(hours=7)
        nam_xem = nam_lap_xuan(now)
    else:
        nam_xem = a.nam_xem
    if not 1901 <= nam_xem <= 2098:
        raise SystemExit("LỖI: --nam-xem ngoài phạm vi 1901-2098.")
    in_huyen_khong(a.huong, van, nguon, nam_xem, a.thang_xem, doc_phuong(a.nuoc), doc_phuong(a.nui), a.ban, a.nam_xay)


# ---------------------------------------------------------------- tự kiểm
def tu_kiem():
    """Kiểm bằng ví dụ đã công bố + bất biến. Trả về list lỗi (rỗng = đạt)."""
    loi = []
    t0 = time.time()

    def kiem(dk, msg):
        if not dk:
            loi.append(msg)

    # 0. bảng thay sao: đủ 24 sơn, mỗi sơn một lần; 11 sơn thay ra đúng sao gốc của cung mình
    kiem(sorted(SAO_THAY) == sorted(B.SON24), "bảng thay sao không phủ đủ 24 sơn")
    tu_than = sorted(s for s in B.SON24 if SAO_THAY[s] == B.CUNG_SO[B.CUNG_CUA_SON[s]])
    kiem(tu_than == sorted("Tý Quý Mùi Khôn Càn Hợi Tuất Dậu Tân Ngọ Đinh".split()),
         "11 sơn không cần thay sai: %s" % tu_than)

    # 1. Hạ quái khớp tvbt.huyen_khong (v2) trên 24 sơn × 9 vận, tại tâm sơn và lệch ±2°, ±4°
    for van in range(1, 10):
        for i in range(24):
            for d in (0, -2, 2, -4, 4):
                do = (i * 15 + d) % 360
                h1, h2 = B.huyen_khong(do, van), lap_ban(do, van, False)
                if (h1["son"], h1["huong_tinh"], h1["van_ban"]) != (h2["son"], h2["huong_tinh"], h2["van_ban"]):
                    loi.append("hạ quái lệch v2: vận %d, %.0f°" % (van, do))

    # 2. Thế quái: ví dụ đã công bố (sao nhập trung + chiều bay + vài cung)
    #   [N1] phongthuyhuyenkhonghoc.net/the-quai/ và [N2] phongthuychanthu.com/2018/01/the-quai-kiem-huong.html:
    #        185° (Tý sơn Ngọ hướng kiêm Quý Đinh 5°) vận 8: sơn 4→Tốn→6 thuận (7 TB, 8 T, 9 ĐB);
    #        hướng 3→Mão→2 nghịch (1 TB, 9 T, 8 ĐB). Cùng nhà vận 1: hướng tinh 5 không thay, Ngọ âm → nghịch.
    #        320° (Tốn sơn Càn hướng kiêm Tỵ Hợi) vận 8: hướng 9→Ngọ→9 (không đổi), nghịch → 8 đến Tây Bắc.
    #   [N3] 163.com/dy/article/DU57N4FD0528KPTC.html (Trần Ích Phong): vận 8 Tý Ngọ kiêm Nhâm Bính = kiêm Quý Đinh
    #        (6 thuận / 2 nghịch); vận 8 Nhâm sơn Bính hướng kiêm Tý Ngọ: 6 nghịch (Thìn âm) / 1 thuận (Giáp dương).
    #   [N4] cafengshuinet.com/m/show_detail.php?id=957: vận 8 Nhâm sơn Bính hướng kiêm Hợi Tỵ: 6 nghịch / 1 thuận.
    #   [N5] zggdfs.com/read/999_1_.html: vận 8 Giáp sơn Canh hướng kiêm Dần Thân: sơn 6 (Tuất không thay) nghịch,
    #        hướng 1→Nhâm→2 thuận.
    #   [N6] fengshuied.com/substitute-star-natal-charts: vận 8, tọa Bính hướng Nhâm 339°: sơn 3→Giáp→1 thuận,
    #        hướng 4→Thìn→6 nghịch.
    mau = [  # (độ, vận, (sơn vào, thuận), (hướng vào, thuận), {cung: (sơn, hướng)}, nguồn)
        (185, 8, (6, True), (2, False), {"Tây Bắc": (7, 1), "Tây": (8, 9), "Đông Bắc": (9, 8)}, "N1/N2/N3"),
        (175, 8, (6, True), (2, False), {}, "N3 (kiêm Nhâm Bính)"),
        (185, 1, None, (5, False), {}, "N1/N2 (vận 1)"),
        (320, 8, (7, False), (9, False), {"Tây Bắc": (None, 8)}, "N1/N2 (320°)"),
        (170, 8, (6, False), (1, True), {}, "N3 (Nhâm Bính kiêm Tý Ngọ)"),
        (160, 8, (6, False), (1, True), {}, "N4 (Nhâm Bính kiêm Hợi Tỵ)"),
        (250, 8, (6, False), (2, True), {}, "N5 (Giáp Canh kiêm Dần Thân)"),
        (339, 8, (1, True), (6, False), {}, "N6 (Bính Nhâm 339°)"),
    ]
    for do, van, ks, kh, cung, nguon in mau:
        b = lap_ban(do, van, True)
        if ks:
            kiem((b["khoi_son"]["vao"], b["khoi_son"]["thuan"]) == ks,
                 "thế quái sơn sai %s: được %s" % (nguon, (b["khoi_son"]["vao"], b["khoi_son"]["thuan"])))
        kiem((b["khoi_huong"]["vao"], b["khoi_huong"]["thuan"]) == kh,
             "thế quái hướng sai %s: được %s" % (nguon, (b["khoi_huong"]["vao"], b["khoi_huong"]["thuan"])))
        for c, (s, h) in cung.items():
            kiem(s is None or b["son"][c] == s, "thế quái %s: sơn tinh %s sai" % (nguon, c))
            kiem(h is None or b["huong_tinh"][c] == h, "thế quái %s: hướng tinh %s sai" % (nguon, c))
    kiem(phan_tich_huong(185)["muc"] == "the" and phan_tich_huong(183.5)["muc"] == "ca-hai"
         and phan_tich_huong(182)["muc"] == "ha" and phan_tich_huong(187)["muc"] == "khong-vong"
         and phan_tich_huong(157)["xuat_quai"], "ngưỡng kiêm hướng sai")
    # bất biến: hạ quái bàn 108s/cafengshuinet [N4]: vận 8 Ngọ sơn Tý hướng: sơn 3 nghịch, hướng 4 thuận
    b = lap_ban(0, 8, False)
    kiem((b["khoi_son"]["vao"], b["khoi_son"]["thuan"], b["khoi_huong"]["vao"], b["khoi_huong"]["thuan"])
         == (3, False, 4, True) and b["son"]["Đông Nam"] == 4 and b["huong_tinh"]["Tây Bắc"] == 5,
         "hạ quái vận 8 Ngọ sơn Tý hướng sai")
    # bất biến: thế quái trùng hạ quái ⇔ sao thay = sao gốc ở cả hai bàn
    for van in range(1, 10):
        for i in range(24):
            h, t = lap_ban(i * 15 + 6, van, False), lap_ban(i * 15 + 6, van, True)
            same = all(k["vao"] == k["sao_van"] for k in (t["khoi_son"], t["khoi_huong"]))
            kiem(same == (h["son"] == t["son"] and h["huong_tinh"] == t["huong_tinh"]), "bất biến trùng bàn sai")

    # 3. Thành môn – [T1] 163.com/dy/article/G75MHF1V05523MC5.html và cafengshuinet.com id=2981:
    #   vận 4 Tý sơn Ngọ hướng: Tốn (chính) và Khôn (phó) đều dùng được;
    #   vận 7 Dậu sơn Mão hướng: chỉ Cấn (chính); vận 1 Ngọ sơn Tý hướng: không có;
    #   vận 1 Tuất sơn Thìn hướng: chỉ phó thành môn Giáp (Chấn), chính (Bính, vận tinh 5) không dùng được;
    #   vận 8 Tý sơn Ngọ hướng: chính thành môn Tốn dùng được.
    #   vận 6 Tý sơn Ngọ hướng: 5 đến Tốn, theo phái lấy âm dương sơn hướng Ngọ (âm) thì dùng được (cafengshuinet).
    def tm(huong, van):
        return {d["cung"]: (d["chinh"], d["dung"]) for d in thanh_mon(huong, van)}
    kiem(tm("Ngọ", 4) == {"Đông Nam": (True, True), "Tây Nam": (False, True)}, "thành môn vận 4 Ngọ sai")
    kiem(tm("Mão", 7) == {"Đông Bắc": (True, True), "Đông Nam": (False, False)}, "thành môn vận 7 Mão sai")
    kiem(tm("Tý", 1) == {"Tây Bắc": (True, False), "Đông Bắc": (False, False)}, "thành môn vận 1 Tý sai")
    kiem(tm("Thìn", 1) == {"Nam": (True, False), "Đông": (False, True)}, "thành môn vận 1 Thìn sai")
    kiem(tm("Ngọ", 8)["Đông Nam"] == (True, True), "thành môn vận 8 Ngọ sai")
    d6 = [d for d in thanh_mon("Ngọ", 6) if d["cung"] == "Đông Nam"][0]
    kiem(d6["sao_van"] == 5 and d6["khac"] and d6["khac"]["dung"], "thành môn vận 6 Ngọ (phái theo sơn hướng) sai")
    # bất biến: thành môn dùng được ⇔ bay nghịch
    for van in range(1, 10):
        for s in B.SON24:
            for d in thanh_mon(s, van):
                kiem(d["dung"] == (not d["thuan"]), "bất biến thành môn sai: %s vận %d" % (s, van))

    # 4. Thất tinh đả kiếp – [K1] xuankongguan.com (七星打劫): 21 cục Ly cung (chân) sau khi loại phục ngâm;
    #    10 cục Khảm cung (giả) là tập con của bộ ta tính (nguồn loại thêm các cục hướng Bắc vì 'nhập tù');
    #    [K2] blog.sina.com.cn/s/blog_5bc171940102vfi1: vận 2 và vận 4 Ngọ sơn Tý hướng là Khảm cung đả kiếp.
    ly21 = {(1, "Ngọ"), (1, "Đinh"), (1, "Tuất"), (1, "Giáp"), (2, "Mão"), (2, "Ất"), (2, "Bính"), (3, "Ngọ"),
            (3, "Đinh"), (4, "Tuất"), (4, "Bính"), (6, "Ngọ"), (6, "Đinh"), (7, "Bính"), (8, "Ngọ"), (8, "Đinh"),
            (8, "Giáp"), (9, "Mão"), (9, "Càn"), (9, "Hợi"), (9, "Ất")}           # (vận, sơn hướng)
    kham10 = {(1, "Dậu"), (1, "Tốn"), (1, "Tỵ"), (1, "Tân"), (2, "Canh"), (6, "Thìn"), (8, "Dậu"), (8, "Tân"),
              (9, "Thìn"), (9, "Canh"), (2, "Tý"), (4, "Tý")}
    ly, kham = set(), set()
    for van in range(1, 10):
        for i, s in enumerate(B.SON24):
            dk = da_kiep(lap_ban(i * 15, van, False))
            if dk["co"]:
                (ly if dk["chan"] else kham).add((van, s))
            if dk["nhom"]:
                vals = sorted(x % 3 for x in dk["sao3"])
                kiem(vals[0] == vals[2] and len(set(dk["sao3"])) == 3, "bất biến tam ban 3 cung sai")
    kiem(ly == ly21, "Ly cung đả kiếp lệch nguồn: thừa %s, thiếu %s" % (sorted(ly - ly21), sorted(ly21 - ly)))
    kiem(kham10 <= kham, "Khảm cung đả kiếp thiếu: %s" % sorted(kham10 - kham))

    # 5. Hợp thập toàn bàn (hạ quái) – [H1] blog.sina.com.cn/s/blog_67cfcf33010312e1 (Vương Minh): đúng 24 cục:
    #    vận 1, 9: Càn Tốn, Tốn Càn, Tỵ Hợi, Hợi Tỵ; vận 2, 8: Sửu Mùi, Mùi Sửu; vận 3, 7: Tý Ngọ, Ngọ Tý, Quý Đinh,
    #    Đinh Quý; vận 4, 6: Canh Giáp, Giáp Canh  (sơn → hướng).
    ht = set()
    for van in range(1, 10):
        for i, s in enumerate(B.SON24):
            b = lap_ban(i * 15, van, False)
            if any("vận" in x for x in hop_thap_toan_ban(b)):
                ht.add((van, b["toa"], b["huong"]))
    mau_ht = set()
    for vs, cap in (((1, 9), "Càn-Tốn Tốn-Càn Tỵ-Hợi Hợi-Tỵ"), ((2, 8), "Sửu-Mùi Mùi-Sửu"),
                    ((3, 7), "Tý-Ngọ Ngọ-Tý Quý-Đinh Đinh-Quý"), ((4, 6), "Canh-Giáp Giáp-Canh")):
        for v in vs:
            for x in cap.split():
                mau_ht.add((v,) + tuple(x.split("-")))
    kiem(ht == mau_ht, "hợp thập lệch nguồn: thừa %s, thiếu %s" % (sorted(ht - mau_ht), sorted(mau_ht - ht)))

    # 6. Liên châu tam ban – [L1] blog.sina.cn ... blog_5bc171940100yzl8: vận 7 Hợi sơn Tỵ hướng là liên châu.
    kiem(tam_ban(lap_ban(B.SON24.index("Tỵ") * 15, 7, False)) == "liên châu", "liên châu vận 7 Hợi sơn sai")

    # 7. Niên tinh 2024–2027 (Lập Xuân): 3, 2, 1, 9; Ngũ Hoàng ở Tây, Đông Bắc, Nam, Bắc.
    for nam, sao, ngu in ((2024, 3, "Tây"), (2025, 2, "Đông Bắc"), (2026, 1, "Nam"), (2027, 9, "Bắc")):
        nt = sao_luu(nam)[0]
        kiem(nt == sao, "niên tinh %d sai: %d" % (nam, nt))
        kiem([c for c, x in B.bay_sao(nt, True).items() if x == 5] == [ngu], "Ngũ Hoàng %d sai" % nam)
    # năm tính từ Lập Xuân (4/2/2026 ~03:02 giờ VN); nguyệt tinh tháng Dần: Ngọ 8, Tỵ 2, Thìn 5
    kiem(nam_lap_xuan(dt.datetime(2026, 2, 3, 12)) == 2025 and nam_lap_xuan(dt.datetime(2026, 2, 5)) == 2026,
         "năm Lập Xuân sai")
    kiem((sao_luu(2026, 1)[1], sao_luu(2025, 1)[1], sao_luu(2024, 1)[1]) == (8, 2, 5), "nguyệt tinh tháng Dần sai")
    bt = bang_tiet(2026)
    kiem(bt[0].date() == dt.date(2026, 2, 4) and bt[12].date() == dt.date(2027, 2, 4)
         and bt[10].year == 2026 and bt[10].month == 12 and bt[11].year == 2027 and bt[11].month == 1,
         "bảng tiết 2026 sai")

    # 8. Chạy toàn bộ 360 độ × 9 vận (in vào bộ nhớ) không lỗi; đọc phương
    kiem(doc_phuong("Đông, dong nam;TB") == ["Đông", "Đông Nam", "Tây Bắc"], "đọc phương sai")
    buf = io.StringIO()
    for van in range(1, 10):
        for do in range(360):
            try:
                with redirect_stdout(buf):
                    in_huyen_khong(do + 0.3 * (van % 3), van, "theo --van", 2026, (do % 12) + 1,
                                   ["Đông"] if do % 2 else [], ["Tây"] if do % 3 == 0 else [])
            except Exception as e:  # noqa: BLE001
                loi.append("lỗi chạy %d° vận %d: %r" % (do, van, e))
                break
    kiem(not re.search(r"[一-鿿]", buf.getvalue()), "output có chữ Hán")
    if time.time() - t0 > 5:
        loi.append("tu_kiem chạy quá 5 giây (%.1f s)" % (time.time() - t0))
    return loi


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Huyền không phi tinh nâng cao")
    sp = ap.add_subparsers(dest="lenh", required=True)
    them_lenh(sp)
    sp.add_parser("tukiem").set_defaults(_chay=lambda a: print("\n".join(tu_kiem()) or "ĐẠT"))
    ns = ap.parse_args()
    ns._chay(ns)
