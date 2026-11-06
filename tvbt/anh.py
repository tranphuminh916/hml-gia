# -*- coding: utf-8 -*-
"""anh.py - Vẽ ảnh: lá số Tử vi (lưới 12 cung, chữ màu theo ngũ hành, Tuần/Triệt, đánh dấu hạn năm xem),
bảng Bát tự (tứ trụ, tàng can, thập thần, đại vận, vượng suy) và BIỂU ĐỒ VẬN THẾ theo năm
(điểm do script tính từ hỷ/kỵ thần, xung hình trụ ngày, trường sinh, tứ hóa lưu niên vào cung hạn).
Ảnh PNG cần Chromium + Playwright; thiếu thì chỉ ghi file HTML cùng tên.
Lệnh: nc.py anhtuvi | anhbattu | vanthe  (xem --help)
"""
import datetime as dt
import html
import os

from lunar_python.util import LunarUtil

import tvbt as B
import tuvi_vn as T
import vuongsuy as V

MAU = {"Mộc": "#2e7d32", "Hỏa": "#c62828", "Thổ": "#a1660a", "Kim": "#546e7a", "Thủy": "#1565c0", "": "#333"}
HANH_SAO = {
    "Tử Vi": "Thổ", "Thiên Cơ": "Mộc", "Thái Dương": "Hỏa", "Vũ Khúc": "Kim", "Thiên Đồng": "Thủy",
    "Liêm Trinh": "Hỏa", "Thiên Phủ": "Thổ", "Thái Âm": "Thủy", "Tham Lang": "Thủy", "Cự Môn": "Thủy",
    "Thiên Tướng": "Thủy", "Thiên Lương": "Mộc", "Thất Sát": "Kim", "Phá Quân": "Thủy",
    "Văn Xương": "Kim", "Văn Khúc": "Thủy", "Tả Phù": "Thổ", "Hữu Bật": "Thủy", "Thiên Khôi": "Hỏa",
    "Thiên Việt": "Hỏa", "Lộc Tồn": "Thổ", "Thiên Mã": "Hỏa", "Kình Dương": "Kim", "Đà La": "Kim",
    "Hỏa Tinh": "Hỏa", "Linh Tinh": "Hỏa", "Địa Không": "Hỏa", "Địa Kiếp": "Hỏa", "Thiên Hình": "Hỏa",
    "Thiên Diêu": "Thủy", "Hồng Loan": "Thủy", "Thiên Hỷ": "Thủy", "Đào Hoa": "Mộc", "Thiên Khốc": "Kim",
    "Thiên Hư": "Thủy", "Tang Môn": "Mộc", "Bạch Hổ": "Kim", "Long Trì": "Thủy", "Phượng Các": "Thổ",
    "Tam Thai": "Thổ", "Bát Tọa": "Thổ", "Ân Quang": "Mộc", "Thiên Quý": "Thổ", "Thai Phụ": "Kim",
    "Phong Cáo": "Thổ", "Thiên Quan": "Hỏa", "Thiên Phúc": "Thổ", "Cô Thần": "Thổ", "Quả Tú": "Thổ",
    "Thiên Không": "Hỏa", "Kiếp Sát": "Hỏa", "Hoa Cái": "Kim", "Phá Toái": "Hỏa", "Thiên Giải": "Hỏa",
    "Địa Giải": "Thổ", "Giải Thần": "Mộc", "Thiên Đức": "Hỏa", "Nguyệt Đức": "Hỏa", "Thiên Y": "Thủy",
    "Thiên Tài": "Thổ", "Thiên Thọ": "Thổ", "Thiên La": "Thổ", "Địa Võng": "Thổ", "Thiên Thương": "Thổ",
    "Thiên Sứ": "Thủy", "Lưu Hà": "Thủy", "Thiên Trù": "Thổ", "Quốc Ấn": "Thổ", "Đường Phù": "Mộc",
    "Văn Tinh": "Hỏa", "Đẩu Quân": "Hỏa",
}
SAT = ["Kình Dương", "Đà La", "Hỏa Tinh", "Linh Tinh", "Địa Không", "Địa Kiếp"]
CAT = ["Văn Xương", "Văn Khúc", "Tả Phù", "Hữu Bật", "Thiên Khôi", "Thiên Việt", "Lộc Tồn"]
VI_TRI_LUOI = {5: (0, 0), 6: (0, 1), 7: (0, 2), 8: (0, 3), 4: (1, 0), 9: (1, 3), 3: (2, 0), 10: (2, 3),
               2: (3, 0), 1: (3, 1), 0: (3, 2), 11: (3, 3)}
CSS = """body{margin:0;font-family:'DejaVu Sans','Noto Sans',Arial,sans-serif;background:#faf7f0;color:#222}
.wrap{padding:14px;width:%dpx}.h1{font-size:20px;font-weight:bold;margin-bottom:6px}
.grid{display:grid;grid-template-columns:repeat(4,1fr);grid-template-rows:repeat(4,auto);gap:3px}
.c{background:#fff;border:1px solid #c9b98f;padding:5px 6px;min-height:178px;font-size:12px;position:relative}
.c.menh{border:2px solid #b71c1c}.c.than{box-shadow:inset 0 0 0 2px #6a1b9a}.c.han{background:#fff8e1}
.ten{font-weight:bold;font-size:13px}.chi{float:right;color:#555}.ct{font-weight:bold;font-size:14px}
.nho{color:#555;font-size:11px;line-height:1.35}.bd{display:inline-block;padding:2px 4px 1px;line-height:1.3;border-radius:3px;
font-size:10px;color:#fff;margin:1px}.lo{background:#2e7d32}.qu{background:#6a1b9a}.kh{background:#1565c0}
.ky{background:#b71c1c}.tt{background:#000}.ft{position:absolute;bottom:4px;left:6px;right:6px;font-size:11px;color:#444}
.mid{grid-column:2/4;grid-row:2/4;background:#fffdf6;border:1px solid #c9b98f;padding:10px;font-size:13px;line-height:1.55}
table{border-collapse:collapse;font-size:13px}td,th{border:1px solid #c9b98f;padding:5px 7px;text-align:center;background:#fff}
th{background:#f3ead2}.big{font-size:22px;font-weight:bold}.note{font-size:11px;color:#555;margin-top:8px}"""


def _e(s):
    return html.escape(str(s))


def chu_sao(ten, extra=""):
    return '<span style="color:%s">%s%s</span>' % (MAU[HANH_SAO.get(ten, "")], _e(ten), _e(extra))


def lap_tu_tt(tt):
    """Lá số Tử vi từ ThongTinSinh, làm đúng như tvbt.tu_vi."""
    t = tt.t_dia_phuong
    ngay = t.date()
    ty_muon = t.hour == 23
    if ty_muon:
        ngay = ngay + dt.timedelta(days=1)
    gio = 0 if ty_muon else B.chi_gio(t)
    d, m, y, nhuan = B.duong_sang_am(ngay, tt.lich_tz)
    so_ngay = B.do_dai_thang_am(d, m, y, nhuan, tt.lich_tz)
    can, chi = (y - 4) % 10, (y - 4) % 12
    ls = T.lap_la_so(m, d, gio, can, chi, tt.gioi, so_ngay, nhuan)
    ls["_am"] = (d, m, y, nhuan)
    return ls


def ghi_anh(html_str, duong_dan, rong):
    """Ghi file HTML; nếu có Playwright thì chụp PNG. Trả về đường dẫn file đã tạo."""
    base, ext = os.path.splitext(duong_dan)
    f_html = base + ".html"
    with open(f_html, "w", encoding="utf-8") as f:
        f.write(html_str)
    if ext.lower() != ".png":
        return f_html
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": rong + 30, "height": 600}, device_scale_factor=2)
            pg.goto("file://" + os.path.abspath(f_html))
            pg.locator(".wrap").screenshot(path=duong_dan)
            b.close()
        return duong_dan
    except Exception as e:      # noqa: BLE001
        print("! Không vẽ được PNG (%s) – dùng file HTML: %s" % (e.__class__.__name__, f_html))
        return f_html


# ---------------------------------------------------------------- ẢNH TỬ VI
def html_tu_vi(tt, ls, ten_nguoi="", nam_xem=None):
    d, m, y, nhuan = ls["_am"]
    vh = None
    if nam_xem:
        tuoi = nam_xem - y + 1
        if tuoi >= 1:
            vh = T.van_han(ls, (nam_xem - 4) % 10, (nam_xem - 4) % 12, tuoi)
    luu_hoa = {}
    if vh:
        for hoa, ten in vh["hoa"]:
            luu_hoa.setdefault(ls["vt"][ten], []).append(hoa.replace("Hóa ", "L.") + " " + ten)
    o = []
    for p in range(12):
        r, c = VI_TRI_LUOI[p]
        lop = ["c"]
        if p == ls["menh"]:
            lop.append("menh")
        if p == ls["than"]:
            lop.append("than")
        if vh and p in (vh["tieu_han"], vh["dai_han"]):
            lop.append("han")
        chinh = []
        for x in T.CHINH_TINH:
            if x in ls["sao"][p]:
                ds = T.do_sang_day_du(x, p)
                h = ls["hoa"].get(x)
                badge = ""
                if h:
                    badge = ' <span class="bd %s">%s</span>' % (
                        {"Hóa Lộc": "lo", "Hóa Quyền": "qu", "Hóa Khoa": "kh", "Hóa Kỵ": "ky"}[h], h.replace("Hóa ", ""))
                chinh.append('<div class="ct">%s%s</div>' % (chu_sao(x, " (%s)" % ds if ds else ""), badge))
        if not chinh:
            chinh.append('<div class="ct" style="color:#888">Vô chính diệu</div>')
        phu = []
        for x in ls["sao"][p]:
            if x in T.CHINH_TINH:
                continue
            h = ls["hoa"].get(x)
            ds_ = T.do_sang_day_du(x, p)
            phu.append(chu_sao(x, " (%s)" % ds_ if ds_ else "") + ('<span class="bd %s">%s</span>' % (
                {"Hóa Lộc": "lo", "Hóa Quyền": "qu", "Hóa Khoa": "kh", "Hóa Kỵ": "ky"}[h], h.replace("Hóa ", ""))
                if h else ""))
        dau = []
        if p in ls["tuan"]:
            dau.append('<span class="bd tt">TUẦN</span>')
        if p in ls["triet"]:
            dau.append('<span class="bd tt">TRIỆT</span>')
        han = []
        if vh:
            if p == vh["dai_han"]:
                han.append("ĐẠI HẠN")
            if p == vh["tieu_han"]:
                han.append("TIỂU HẠN %d" % nam_xem)
            for k, q in vh["luu"].items():
                if q == p and k in ("Lưu Thái Tuế", "Lưu Lộc Tồn", "Lưu Kình Dương", "Lưu Đà La", "Lưu Thiên Mã"):
                    han.append(k.replace("Lưu ", "L."))
            han += luu_hoa.get(p, [])
        a, b = ls["dai_han"][p]
        o.append('<div class="%s" style="grid-row:%d;grid-column:%d"><span class="ten">%s%s</span>'
                 '<span class="chi">%s %s</span><br>%s%s<div class="nho">%s</div>'
                 '<div class="nho" style="color:#b26a00">%s</div><div class="ft">%s · %s · ĐH %d–%d</div></div>' % (
                     " ".join(lop), r + 1, c + 1, _e(T.ten_cung(ls, p)), " (Thân)" if p == ls["than"] else "",
                     _e(T.CAN[ls["can_cung"][p]]), _e(T.CHI[p]), "".join(dau), "".join(chinh), ", ".join(phu),
                     _e(" · ".join(han)), _e(ls["trang_sinh"][p]), _e(ls["thai_tue"][p]), a, b))
    can, chi = ls["can"], ls["chi"]
    hanh_cuc = [k for k, v in T.CUC.items() if v == ls["cuc"]][0]
    mid = ('<div class="mid"><div class="big">LÁ SỐ TỬ VI</div>%s'
           '<div>Sinh: %s, giờ %s (%s)</div><div>Âm lịch: ngày %d tháng %d%s năm %s %s</div>'
           '<div>Giới tính: %s · Bản mệnh: %s</div><div>Cục: %s · Mệnh chủ: %s · Thân chủ: %s</div>'
           '<div>Tứ hóa năm sinh: %s</div>%s'
           '<div class="note">Cách an phổ biến ở Việt Nam (Thái Thứ Lang). Độ sáng: M miếu, V vượng, Đ đắc, B bình, H hãm. '
           'Viền đỏ: cung Mệnh; viền tím: cung Thân; nền vàng: cung hạn năm xem. Màu chữ theo ngũ hành của sao.</div></div>') % (
        "<div><b>%s</b></div>" % _e(ten_nguoi) if ten_nguoi else "",
        tt.dong_ho.strftime("%d/%m/%Y"), tt.dong_ho.strftime("%H:%M"), _e(tt.noi), d, m, " nhuận" if nhuan else "",
        T.CAN[can], T.CHI[chi], "Nam" if tt.gioi == "nam" else "Nữ", _e(B.hanh_nap_am_vn(can, chi)),
        T.TEN_CUC[ls["cuc"]], _e(ls["menh_chu"]), _e(ls["than_chu"].split(" (")[0]),
        _e(", ".join("%s %s" % (k, v.replace("Hóa ", "")) for k, v in ls["hoa"].items())),
        ("<div><b>Năm xem %d</b>: tiểu hạn %s, đại hạn %s</div>" % (
            nam_xem, _e(T.ten_cung(ls, vh["tieu_han"])),
            _e(T.ten_cung(ls, vh["dai_han"])) if vh["dai_han"] is not None else "-") if vh else ""))
    del hanh_cuc
    return ('<html><head><meta charset="utf-8"><style>%s</style></head><body><div class="wrap">'
            '<div class="grid">%s%s</div></div></body></html>') % (CSS % 1000, "".join(o), mid)


# ---------------------------------------------------------------- ẢNH BÁT TỰ
def html_bat_tu(tt, ten_nguoi=""):
    ebk, eloc, tru = B.tu_tru(tt)
    nc = eloc.getDayGan()
    ts = LunarUtil.SHI_SHEN
    tru3 = [(nh, gz[0], gz[1]) for nh, gz in tru]
    hang = {"Thập thần": [], "Thiên can": [], "Địa chi": [], "Tàng can": [], "Nạp âm": [], "Trường sinh": []}
    for nh, gz in tru:
        g, z = gz[0], gz[1]
        hc, hz = B.HANH[B.CAN_HANH[g]], B.HANH[B.CHI_HANH[z]]
        hang["Thập thần"].append("Nhật chủ" if nh == "Ngày" else B.vn(ts[nc + g]))
        hang["Thiên can"].append('<span class="big" style="color:%s">%s</span><br>%s' % (MAU[hc], B.CAN[g], hc))
        hang["Địa chi"].append('<span class="big" style="color:%s">%s</span><br>%s' % (MAU[hz], B.CHI[z], hz))
        hang["Tàng can"].append("<br>".join('<span style="color:%s">%s</span> %s' % (
            MAU[B.HANH[B.CAN_HANH[h]]], B.CAN[h], B.vn(ts[nc + h])) for h in LunarUtil.ZHI_HIDE_GAN[z]))
        hang["Nạp âm"].append(B.vn(LunarUtil.NAYIN[gz]))
        hang["Trường sinh"].append(V.TS12[V.truong_sinh(nc, z)])
    bang = "<table><tr><th></th>%s</tr>%s</table>" % (
        "".join("<th>Trụ %s</th>" % nh for nh, _ in tru),
        "".join("<tr><th>%s</th>%s</tr>" % (k, "".join("<td>%s</td>" % x for x in v)) for k, v in hang.items()))
    dv = ""
    if tt.co_gio:
        nam_am = B.duong_sang_am(tt.t_dia_phuong.date(), tt.lich_tz)[2]
        yun = ebk.getYun(1 if tt.gioi == "nam" else 0, 2)
        o = []
        for dy in yun.getDaYun(11)[1:]:
            gz = dy.getGanZhi()
            o.append("<td>%d–%d tuổi<br>(%d)<br><b style='color:%s'>%s</b> <b style='color:%s'>%s</b><br>%s</td>" % (
                dy.getStartYear() - nam_am + 1, dy.getEndYear() - nam_am + 1, dy.getStartYear(),
                MAU[B.HANH[B.CAN_HANH[gz[0]]]], B.CAN[gz[0]], MAU[B.HANH[B.CHI_HANH[gz[1]]]], B.CHI[gz[1]],
                B.vn(ts[nc + gz[0]])))
        dv = "<div style='margin-top:10px'><b>Đại vận (%s)</b><table><tr>%s</tr></table></div>" % (
            "thuận" if yun.isForward() else "nghịch", "".join(o))
    pa, ma, _, _ = V.thang_a(tru3)
    _, _, tl, mb, hanh = V.thang_b(tru3)
    cc = V.cach_cuc(tru3)[0]
    tom = ("<div style='margin-top:10px'>Vượng suy: thang A %+.1f (%s) · thang B %.0f%% (%s) · Cách cục: %s<br>"
           "Điểm ngũ hành (thang B): %s</div>") % (
        pa, ma, 100 * tl, mb, cc, " · ".join('<span style="color:%s">%s %.0f</span>' % (
            MAU[V.HANH_VN[i]], V.HANH_VN[i], hanh[i]) for i in range(5)))
    tieu_de = "<div class='h1'>BÁT TỰ%s</div><div>Sinh %s (%s), %s, giờ mặt trời thực %s</div>" % (
        " – " + _e(ten_nguoi) if ten_nguoi else "", tt.dong_ho.strftime("%H:%M %d/%m/%Y"), _e(tt.noi),
        "Nam" if tt.gioi == "nam" else "Nữ", tt.tst.strftime("%H:%M") if tt.co_gio else "-")
    return ('<html><head><meta charset="utf-8"><style>%s</style></head><body><div class="wrap">%s%s%s%s'
            '<div class="note">Màu chữ theo ngũ hành. Điểm vượng suy chỉ để tham khảo khi chọn dụng thần.</div>'
            '</div></body></html>') % (CSS % 900, tieu_de, bang, dv, tom)


# ---------------------------------------------------------------- VẬN THẾ THEO NĂM
XUNG = lambda a, b: (a - b) % 12 == 6
HAI = {frozenset(x) for x in [(0, 7), (1, 6), (2, 5), (3, 4), (8, 11), (9, 10)]}
PHA = {frozenset(x) for x in [(0, 9), (1, 4), (2, 11), (3, 6), (5, 8), (7, 10)]}
HINH = {frozenset(x) for x in [(2, 5), (5, 8), (2, 8), (1, 10), (10, 7), (1, 7), (0, 3)]}
LUC_HOP = {frozenset(x) for x in [(0, 1), (2, 11), (3, 10), (4, 9), (5, 8), (6, 7)]}
TAM_HOP = [{8, 0, 4}, {11, 3, 7}, {2, 6, 10}, {5, 9, 1}]


def hy_ky_mac_dinh(tru3):
    """Hỷ/kỵ theo phù ức đơn giản từ thang A (chỉ dùng khi người luận chưa chọn dụng thần)."""
    nc = tru3[2][1]
    h0 = V.GAN_H[V.GAN.index(nc)]
    pa, ma, _, _ = V.thang_a(tru3)
    ta = {h0, (h0 - 1) % 5}                      # Tỷ Kiếp, Ấn
    nguoi = {(h0 + 1) % 5, (h0 + 2) % 5, (h0 + 3) % 5}
    if "vượng" in ma or (ma == "trung hòa" and pa >= 0):
        return nguoi, ta
    return ta, nguoi


def canh_bao_cuc_doan(tru3):
    """Cảnh báo khi hỷ/kỵ mặc định (phù ức) có thể ngược: cả hai thang cùng cực vượng / cùng cực nhược thì có
    thể là cách tòng, chuyên vượng – khi đó sách lấy thuận thế (chuyên vượng ưa Tỷ Ấn; tòng cách ưa hành mạnh)."""
    pa, ma, _, _ = V.thang_a(tru3)
    tl, mb = V.thang_b(tru3)[2:4]
    if ("cực vượng" in ma and "cực vượng" in mb) or ("cực nhược" in ma and "cực nhược" in mb):   # ~4% lá số
        return ("Vượng suy ở mức cực đoan (thang A: %s, thang B: %s): có thể là cách tòng / chuyên vượng – hỷ kỵ "
                "mặc định theo phù ức có thể NGƯỢC; phải xét tay (4.1, mục cách cục đặc biệt) rồi truyền --dung/--ky."
                % (ma, mb))
    return None


def diem_nam(tt, tru3, ls, dung, ky, nam):
    """Điểm Bát tự và Tử vi của một năm (năm Bát tự tính từ Lập Xuân; Tử vi theo năm âm lịch)."""
    from lunar_python import Solar
    gz = Solar.fromYmd(nam, 6, 1).getLunar().getYearInGanZhiExact()
    g, z = V.GAN.index(gz[0]), V.ZHI.index(gz[1])
    hg, hz = V.GAN_H[g], V.ZHI_H[z]
    bt, ly = 0.0, []
    for h, ten in ((hg, "can năm"), (hz, "chi năm")):
        if h in dung:
            bt += 1
            ly.append("%s hỷ" % ten)
        elif h in ky:
            bt -= 1
            ly.append("%s kỵ" % ten)
    import hoptac as H
    zn = V.ZHI.index(tru3[2][2])
    sq, tq = H.quan_he_chi(z, zn)
    if tq == "xung":
        bt -= 1
        ly.append("xung chi ngày")
    elif sq < 0:
        bt -= 0.5
        ly.append("%s chi ngày" % tq)
    elif tq in ("lục hợp", "tam hợp"):
        bt += 0.5
        ly.append("%s chi ngày" % tq)
    ts = V.truong_sinh(tru3[2][1], gz[1])
    if ts in (0, 2, 3, 4):
        bt += 0.5
    elif ts in (6, 7, 8, 9):
        bt -= 0.5
    # đại vận đang chạy (nửa trọng số)
    if tt.co_gio:
        ebk, _, _ = B.tu_tru(tt)
        for dy in ebk.getYun(1 if tt.gioi == "nam" else 0, 2).getDaYun(11)[1:]:
            if dy.getStartYear() <= nam <= dy.getEndYear():
                dgz = dy.getGanZhi()
                for h in (V.GAN_H[V.GAN.index(dgz[0])], V.ZHI_H[V.ZHI.index(dgz[1])]):
                    bt += 0.5 if h in dung else (-0.5 if h in ky else 0)
                ly.append("vận %s" % B.vn(dgz))
    tv, ly_tv = None, []
    if ls is not None:
        y_am = ls["_am"][2]
        tuoi = nam - y_am + 1
        if tuoi >= 1:
            vh = T.van_han(ls, (nam - 4) % 10, (nam - 4) % 12, tuoi)
            th = vh["tieu_han"]
            tam = {th, (th + 4) % 12, (th + 8) % 12, (th + 6) % 12}
            tv = 0.0
            for hoa, ten in vh["hoa"]:
                q = ls["vt"][ten]
                if hoa == "Hóa Kỵ":
                    if q == th:
                        tv -= 1
                        ly_tv.append("Kỵ lưu vào hạn")
                    elif q in tam:
                        tv -= 0.5
                else:
                    if q == th:
                        tv += 1 if hoa == "Hóa Lộc" else 0.5
                        ly_tv.append("%s lưu vào hạn" % hoa.replace("Hóa ", ""))
                    elif q in tam:
                        tv += 0.5 if hoa == "Hóa Lộc" else 0.25
                if ls["hoa"].get(ten) == "Hóa Kỵ" and hoa == "Hóa Kỵ":
                    tv -= 0.5
                    ly_tv.append("Kỵ chồng Kỵ")
            for k in ("Lưu Kình Dương", "Lưu Đà La"):
                if vh["luu"][k] == th:
                    tv -= 0.5
            if vh["luu"]["Lưu Lộc Tồn"] == th:
                tv += 0.5
            sao = ls["sao"][th]
            for x in T.CHINH_TINH:
                if x in sao:
                    ds = T.do_sang(x, th)
                    tv += 0.5 if ds in ("M", "V") else (-0.5 if ds == "H" else 0)
            tv += min(1, 0.25 * sum(1 for x in CAT if x in sao)) - min(1, 0.25 * sum(1 for x in SAT if x in sao))
            ly_tv.append("hạn ở %s" % T.ten_cung(ls, th))
    return gz, round(bt, 2), ly, (round(tv, 2) if tv is not None else None), ly_tv


def svg_duong(nam_ds, chuoi, nam_nay):
    """chuoi: list (tên, màu, list giá trị|None)."""
    w, h, l, r, t, b = 960, 320, 46, 14, 16, 34
    vals = [v for _, _, ds in chuoi for v in ds if v is not None]
    vmax = max(3, max(abs(v) for v in vals)) if vals else 3
    n = len(nam_ds)
    x = lambda i: l + (w - l - r) * (i / max(1, n - 1))
    y = lambda v: t + (h - t - b) * (0.5 - v / (2 * vmax))
    o = ['<svg width="%d" height="%d" xmlns="http://www.w3.org/2000/svg" style="background:#fff">' % (w, h)]
    for k in range(-int(vmax), int(vmax) + 1):
        o.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"/>' % (
            l, w - r, y(k), y(k), "#888" if k == 0 else "#eee", 1.2 if k == 0 else 1))
        o.append('<text x="%d" y="%.1f" font-size="11" text-anchor="end" fill="#666">%+d</text>' % (l - 6, y(k) + 4, k))
    for i, nam in enumerate(nam_ds):
        if nam % 5 == 0 or n <= 16 or nam == nam_nay:
            o.append('<text x="%.1f" y="%d" font-size="11" text-anchor="middle" fill="%s">%d</text>' % (
                x(i), h - 12, "#b71c1c" if nam == nam_nay else "#555", nam))
        if nam == nam_nay:
            o.append('<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" stroke="#b71c1c" stroke-dasharray="4 3"/>' % (
                x(i), x(i), t, h - b))
    for ten, mau, ds in chuoi:
        pts = ["%.1f,%.1f" % (x(i), y(v)) for i, v in enumerate(ds) if v is not None]
        if pts:
            o.append('<polyline fill="none" stroke="%s" stroke-width="%s" points="%s"/>' % (
                mau, 3 if ten == "Tổng" else 1.6, " ".join(pts)))
    lx = l + 10
    for ten, mau, _ in chuoi:
        o.append('<rect x="%d" y="%d" width="14" height="4" fill="%s"/><text x="%d" y="%d" font-size="12">%s</text>' % (
            lx, t + 2, mau, lx + 18, t + 7, ten))
        lx += 110
    o.append("</svg>")
    return "".join(o)


def van_the(tt, tu_nam, den_nam, dung=None, ky=None):
    _, _, tru = B.tu_tru(tt)
    tru3 = [(nh, gz[0], gz[1]) for nh, gz in tru]
    mac_dinh = dung is None
    if mac_dinh:
        dung, ky = hy_ky_mac_dinh(tru3)
    ls = lap_tu_tt(tt) if tt.co_gio else None
    hang = []
    for nam in range(tu_nam, den_nam + 1):
        gz, bt, ly, tv, ly_tv = diem_nam(tt, tru3, ls, dung, ky, nam)
        tong = round(bt + (tv if tv is not None else 0), 2)
        hang.append((nam, gz, bt, ly, tv, ly_tv, tong))
    return hang, dung, ky, mac_dinh


def in_van_the(hang, dung, ky, mac_dinh):
    print("VẬN THẾ THEO NĂM (điểm do script tính – xem xu hướng lên/xuống, KHÔNG phải cát hung tuyệt đối)")
    print("- Hành hỷ: %s; hành kỵ: %s%s" % (", ".join(V.HANH_VN[h] for h in sorted(dung)),
                                          ", ".join(V.HANH_VN[h] for h in sorted(ky)),
                                          " (! mặc định theo phù ức đơn giản – nên truyền --dung/--ky đã chọn khi luận)"
                                          if mac_dinh else ""))
    print("| Năm | Can chi | Bát tự | Căn cứ Bát tự | Tử vi | Căn cứ Tử vi | Tổng |")
    print("|---|---|---|---|---|---|---|")
    for nam, gz, bt, ly, tv, ly_tv, tong in hang:
        print("| %d | %s | %+.1f | %s | %s | %s | %+.1f |" % (nam, B.vn(gz), bt, ", ".join(ly), "-" if tv is None else
                                                          "%+.1f" % tv, ", ".join(ly_tv), tong))
    k = max(1, min(3, len(hang) // 2))
    tot = sorted(hang, key=lambda r: -r[6])[:k]
    xau = sorted(hang, key=lambda r: r[6])[:k]
    print("- Năm điểm cao: %s; năm điểm thấp: %s" % (", ".join(str(r[0]) for r in tot), ", ".join(str(r[0]) for r in xau)))
    print("(Bát tự: can/chi năm hỷ +1, kỵ −1; xung chi ngày −1, hình/hại/phá −0,5, hợp +0,5; trường sinh của nhật chủ "
          "±0,5; đại vận ±0,5 mỗi can/chi. Tử vi: tứ hóa lưu niên vào cung tiểu hạn và tam phương, Kỵ chồng Kỵ, "
          "Lưu Kình/Đà/Lộc Tồn, độ sáng chính tinh và cát/sát tinh ở cung hạn.)")
    print()


def html_van_the(hang, ten_nguoi, nam_nay, dung, ky):
    nam_ds = [r[0] for r in hang]
    chuoi = [("Bát tự", "#1565c0", [r[2] for r in hang])]
    if any(r[4] is not None for r in hang):
        chuoi.append(("Tử vi", "#ef6c00", [r[4] for r in hang]))
        chuoi.append(("Tổng", "#2e7d32", [r[6] for r in hang]))
    return ('<html><head><meta charset="utf-8"><style>%s</style></head><body><div class="wrap">'
            '<div class="h1">VẬN THẾ THEO NĂM%s</div>%s<div class="note">Hành hỷ: %s · hành kỵ: %s. Điểm do script '
            'tính từ hỷ/kỵ thần, quan hệ với trụ ngày, trường sinh, đại vận (Bát tự) và tứ hóa lưu niên, sao ở cung '
            'tiểu hạn (Tử vi). Chỉ để thấy xu hướng; không phải lời đoán cát hung.</div></div></body></html>') % (
        CSS % 980, " – " + _e(ten_nguoi) if ten_nguoi else "", svg_duong(nam_ds, chuoi, nam_nay),
        ", ".join(V.HANH_VN[h] for h in sorted(dung)), ", ".join(V.HANH_VN[h] for h in sorted(ky)))


def _doc_hanh(s):
    if not s:
        return None
    kq = set()
    for h in s.replace(",", "+").split("+"):
        h = h.strip()
        if h not in V.HANH_VN:
            raise SystemExit("LỖI: hành phải là một trong %s" % ", ".join(V.HANH_VN))
        kq.add(V.HANH_VN.index(h))
    return kq


def them_lenh(sub):
    import nc
    p = sub.add_parser("anhtuvi", help="vẽ lá số Tử vi thành ảnh PNG")
    nc.them_tham_so_sinh(p, gioi_bat_buoc=True)
    p.add_argument("--ten", default="")
    p.add_argument("--nam-xem", type=int)
    p.add_argument("--ra", default="/tmp/la_so_tu_vi.png")
    p.set_defaults(_chay=chay_tu_vi)
    p = sub.add_parser("anhbattu", help="vẽ bảng Bát tự thành ảnh PNG")
    nc.them_tham_so_sinh(p, gioi_bat_buoc=True)
    p.add_argument("--ten", default="")
    p.add_argument("--ra", default="/tmp/la_so_bat_tu.png")
    p.set_defaults(_chay=chay_bat_tu)
    p = sub.add_parser("vanthe", help="bảng và biểu đồ vận thế theo năm")
    nc.them_tham_so_sinh(p, gioi_bat_buoc=True)
    p.add_argument("--ten", default="")
    p.add_argument("--tu-nam", type=int)
    p.add_argument("--den-nam", type=int)
    p.add_argument("--dung", help="hành hỷ/dụng đã chọn, vd Kim+Thủy")
    p.add_argument("--ky", help="hành kỵ đã chọn, vd Hỏa+Mộc")
    p.add_argument("--ra", default="/tmp/van_the.png")
    p.set_defaults(_chay=chay_van_the)


def _tt(a):
    if not a.ngay:
        raise SystemExit("LỖI: cần --ngay (ngày sinh).")
    tt = B.doc_dau_vao(a)
    for c in tt.canh_bao:
        print("! " + c)
    return tt


def chay_tu_vi(a):
    tt = _tt(a)
    if not tt.co_gio:
        raise SystemExit("LỖI: Tử vi cần giờ sinh.")
    f = ghi_anh(html_tu_vi(tt, lap_tu_tt(tt), a.ten, a.nam_xem), a.ra, 1000)
    print("Đã vẽ lá số Tử vi: %s" % f)


def chay_bat_tu(a):
    tt = _tt(a)
    f = ghi_anh(html_bat_tu(tt, a.ten), a.ra, 900)
    print("Đã vẽ bảng Bát tự: %s" % f)


def chay_van_the(a):
    tt = _tt(a)
    nam_nay = dt.date.today().year
    tu = max(a.tu_nam or max(tt.dong_ho.year + 1, nam_nay - 10), tt.dong_ho.year)
    den = a.den_nam or max(nam_nay + 15, tu + 15)      # người sinh sau năm nay + 15 vẫn có khoảng mặc định
    if a.tu_nam and a.tu_nam < tt.dong_ho.year:
        print("! Bỏ các năm trước năm sinh: bắt đầu từ %d." % tu)
    if den - tu > 100 or den < tu:
        raise SystemExit("LỖI: khoảng năm không hợp lệ (tối đa 100 năm).")
    dung, ky = _doc_hanh(a.dung), _doc_hanh(a.ky)
    if (dung is None) != (ky is None):
        raise SystemExit("LỖI: cần cả --dung và --ky (hoặc bỏ cả hai).")
    hang, dung, ky, md = van_the(tt, tu, den, dung, ky)
    if md:
        _, _, tru = B.tu_tru(tt)
        cb = canh_bao_cuc_doan([(nh, gz[0], gz[1]) for nh, gz in tru])
        if cb:
            print("! " + cb)
    in_van_the(hang, dung, ky, md)
    f = ghi_anh(html_van_the(hang, a.ten, nam_nay, dung, ky), a.ra, 980)
    print("Đã vẽ biểu đồ vận thế: %s" % f)


def tu_kiem():
    import argparse
    loi = []
    ns = argparse.Namespace(ngay="2000-01-01", gio="10:00", gioi="nam", noi="Hà Nội", kinhdo=None, mien=None,
                            utc=None, am=False, nhuan=False, lich_tz=None, gio_dong_ho=False, ty=1)
    tt = B.doc_dau_vao(ns)
    ls = lap_tu_tt(tt)
    # khớp tự kiểm v2: Mệnh tại Mùi, Thân tại Tỵ, Thổ Ngũ Cục
    if (ls["menh"], ls["than"], ls["cuc"]) != (7, 5, 5):
        loi.append("lá số 2000-01-01 lệch v2")
    h = html_tu_vi(tt, ls, "Mẫu", 2026)
    for k in ("Mệnh", "Vô chính diệu", "Kình Dương", "TIỂU HẠN 2026", "Thổ Ngũ Cục"):
        if k not in h:
            loi.append("ảnh Tử vi thiếu %s" % k)
    if h.count('style="grid-row:') != 12:
        loi.append("ảnh Tử vi không đủ 12 cung")
    hb = html_bat_tu(tt)
    for k in ("Kỷ", "Bính", "Mậu", "Đinh", "Chính Tài cách", "Đại vận"):
        if k not in hb:
            loi.append("ảnh Bát tự thiếu %s" % k)
    hang, dung, ky, md = van_the(tt, 2020, 2030)
    if len(hang) != 11 or any(r[4] is None for r in hang):
        loi.append("vận thế thiếu năm")
    # năm 2026 (Bính Ngọ) xung? chi ngày Ngọ -> không xung; năm 2020 Canh Tý xung chi ngày Ngọ: phải có "xung chi ngày"
    if "xung chi ngày" not in hang[0][3]:
        loi.append("2020 Tý phải xung chi ngày Ngọ")
    if "<polyline" not in html_van_the(hang, "", 2026, dung, ky):
        loi.append("biểu đồ không có đường")
    # cảnh báo cực đoan: Giáp sinh tháng Mão, toàn Mộc Thủy (cực vượng) phải cảnh báo; lá số 2000-01-01 thì không
    cuc = [("Năm", "甲", "寅"), ("Tháng", "乙", "卯"), ("Ngày", "甲", "寅"), ("Giờ", "癸", "亥")]
    if not canh_bao_cuc_doan(cuc) or canh_bao_cuc_doan([("Năm", "己", "卯"), ("Tháng", "丙", "子"),
                                                         ("Ngày", "戊", "午"), ("Giờ", "丁", "巳")]):
        loi.append("cảnh báo cực vượng/cực nhược cho hỷ kỵ mặc định")
    return loi
