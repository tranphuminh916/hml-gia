# -*- coding: utf-8 -*-
"""luunhat.py - Lưu nhật (từng ngày) và lưu thời (từng giờ) cho một lá số.
- Bát tự: can chi ngày/giờ lưu là thập thần gì, hỷ hay kỵ, quan hệ với 4 chi gốc (xung, hợp, hình, hại, phá).
- Tử vi (phép Đẩu Quân, cùng mặc định với luan-la-so-chi-tiet): cung tháng Giêng = từ cung Lưu Thái Tuế đếm nghịch
  đến tháng sinh rồi đếm thuận đến giờ sinh; tháng sau đi thuận; mùng 1 của tháng ở cung tháng, các ngày sau đi thuận;
  giờ Tý ở cung ngày, các giờ sau đi thuận. Tứ hóa ngày theo can ngày, tứ hóa giờ theo can giờ.
Lệnh: nc.py luunhat --ngay <ngày sinh> --gio <giờ sinh> --gioi nam --tu 2026-11-01 --den 2026-11-30 [--dung Kim+Thủy --ky Hỏa]
      nc.py luunhat ... --ngay-xem 2026-11-12   (lưu thời 12 giờ của một ngày)
"""
import datetime as dt

from lunar_python import Solar

import tvbt as B
import tuvi_vn as T
import vuongsuy as V
import anh

XUNG = lambda a, b: (a - b) % 12 == 6
TEN_TRU = ["năm", "tháng", "ngày", "giờ"]


def quan_he_voi_goc(z, tru3):
    import hoptac as H
    ds = []
    for i, (_, g, zg) in enumerate(tru3):
        s, t = H.quan_he_chi(z, V.ZHI.index(zg))
        if t not in ("bình thường", "trùng"):
            ds.append((s, "%s chi %s" % (t, TEN_TRU[i])))
    return ds


def cung_thang_gieng(ls, nam_am):
    """Cung tháng Giêng theo phép Đẩu Quân cho năm âm lịch nam_am."""
    tt_chi = (nam_am - 4) % 12
    return (tt_chi - (ls["thang"] - 1) + ls["gio"]) % 12


def diem_bt(gz, tru3, dung, ky):
    g, z = V.GAN.index(gz[0]), V.ZHI.index(gz[1])
    s, ly = 0.0, []
    for h, ten in ((V.GAN_H[g], "can"), (V.ZHI_H[z], "chi")):
        if h in dung:
            s += 1
            ly.append(ten + " hỷ")
        elif h in ky:
            s -= 1
            ly.append(ten + " kỵ")
    for v, t in quan_he_voi_goc(z, tru3):
        w = 1.5 if "chi ngày" in t else 0.5
        s += max(-1.5, min(1.5, v / 3 * w))
        ly.append(t)
    return round(s, 1), ly


def diem_tv(ls, cung, can):
    """Tứ hóa theo can (ngày/giờ) rơi vào cung lưu và tam phương."""
    tam = {cung, (cung + 4) % 12, (cung + 8) % 12, (cung + 6) % 12}
    s, ly = 0.0, []
    for hoa, ten in zip(T.HOA, T.TU_HOA[can]):
        q = ls["vt"][ten]
        if q == cung:
            s += {"Hóa Lộc": 1, "Hóa Quyền": 0.5, "Hóa Khoa": 0.5, "Hóa Kỵ": -1}[hoa]
            ly.append("%s %s tại cung" % (hoa.replace("Hóa ", ""), ten))
        elif q in tam:
            s += {"Hóa Lộc": 0.5, "Hóa Quyền": 0.25, "Hóa Khoa": 0.25, "Hóa Kỵ": -0.5}[hoa]
    sao = ls["sao"][cung]
    s += min(0.5, 0.25 * sum(1 for x in anh.CAT if x in sao)) - min(0.5, 0.25 * sum(1 for x in anh.SAT if x in sao))
    return round(s, 1), ly


def in_luu_nhat(tt, tu, den, dung, ky, md):
    if (den - tu).days > 61 or den < tu:
        raise SystemExit("LỖI: khoảng ngày tối đa 62 ngày.")
    _, _, tru = B.tu_tru(tt)
    tru3 = [(nh, gz[0], gz[1]) for nh, gz in tru]
    ls = anh.lap_tu_tt(tt) if tt.co_gio else None
    nc = tru3[2][1]
    print("LƯU NHẬT (từng ngày) – Bát tự%s" % (" + Tử vi (phép Đẩu Quân)" if ls else " (không có giờ sinh: bỏ Tử vi)"))
    print("- Hành hỷ: %s; hành kỵ: %s%s" % (", ".join(V.HANH_VN[h] for h in sorted(dung)),
                                          ", ".join(V.HANH_VN[h] for h in sorted(ky)),
                                          " (! mặc định – nên truyền --dung/--ky đã chọn)" if md else ""))
    print("| Ngày | Âm lịch | Can chi | Thập thần | Bát tự | Căn cứ | Cung ngày (Tử vi) | Tứ hóa ngày | Tử vi | Tổng |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    thu = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
    hang = []
    d = tu
    while d <= den:
        l = Solar.fromYmd(d.year, d.month, d.day).getLunar()
        gz = l.getDayInGanZhi()
        bt, ly = diem_bt(gz, tru3, dung, ky)
        tv, cung_txt, hoa_txt, ly_tv = None, "-", "-", []
        if ls:
            dd, mm, yy, nh = B.duong_sang_am(d, B.mui_lich_am(d, tt.mien_nam))
            cung = (cung_thang_gieng(ls, yy) + (mm - 1) + (dd - 1)) % 12
            can = V.GAN.index(gz[0])
            tv, ly_tv = diem_tv(ls, cung, can)
            cung_txt = "%s (%s)" % (T.ten_cung(ls, cung), T.CHI[cung])
            hoa_txt = ", ".join("%s %s→%s" % (h.replace("Hóa ", ""), s, T.ten_cung(ls, ls["vt"][s]))
                                for h, s in zip(T.HOA, T.TU_HOA[can]))
        dd, mm, _, nh = B.duong_sang_am(d, B.mui_lich_am(d, tt.mien_nam))
        tong = round(bt + (tv or 0), 1)
        hang.append((d, tong))
        print("| %s %s | %d/%d%s | %s | %s | %+.1f | %s | %s | %s | %s | %+.1f |" % (
            thu[d.weekday()], d.strftime("%d/%m"), dd, mm, " nhuận" if nh else "", B.vn(gz),
            V.thap_than(nc, gz[0]), bt, ", ".join(ly) or "-", cung_txt, hoa_txt,
            "-" if tv is None else "%+.1f" % tv, tong))
        d += dt.timedelta(days=1)
    k = max(1, min(5, len(hang) // 2))
    tot = sorted(hang, key=lambda r: -r[1])[:k]
    xau = sorted(hang, key=lambda r: r[1])[:k]
    print("- Ngày điểm cao: %s" % ", ".join(r[0].strftime("%d/%m") for r in tot))
    print("- Ngày điểm thấp (nên thận trọng việc lớn): %s" % ", ".join(r[0].strftime("%d/%m") for r in xau))
    print("(Lưu nhật là tầng nhỏ nhất, chỉ dùng để chọn trong những ngày đã ổn ở tầng năm/tháng; kết hợp với lệnh "
          "'ngay' để có lịch nên/kiêng. Điểm là quy ước, không phải cát hung tuyệt đối.)")
    print()


def in_luu_thoi(tt, ngay_xem, dung, ky):
    _, _, tru = B.tu_tru(tt)
    tru3 = [(nh, gz[0], gz[1]) for nh, gz in tru]
    ls = anh.lap_tu_tt(tt) if tt.co_gio else None
    nc = tru3[2][1]
    dd, mm, yy, nh = B.duong_sang_am(ngay_xem, B.mui_lich_am(ngay_xem, tt.mien_nam))
    print("LƯU THỜI ngày %s (%d/%d âm)" % (ngay_xem.strftime("%d/%m/%Y"), dd, mm))
    print("| Giờ | Can chi giờ | Thập thần | Bát tự | Căn cứ | Cung giờ (Tử vi) | Tứ hóa giờ | Tử vi | Tổng |")
    print("|---|---|---|---|---|---|---|---|---|")
    cung_ngay = (cung_thang_gieng(ls, yy) + (mm - 1) + (dd - 1)) % 12 if ls else None
    for z in range(12):
        h = (2 * z) % 24
        l = Solar.fromYmdHms(ngay_xem.year, ngay_xem.month, ngay_xem.day, h, 30, 0).getLunar()
        gz = l.getTimeInGanZhi()
        bt, ly = diem_bt(gz, tru3, dung, ky)
        tv, ct, ht = None, "-", "-"
        if ls:
            cung = (cung_ngay + z) % 12
            can = V.GAN.index(gz[0])
            tv, _ = diem_tv(ls, cung, can)
            ct = "%s (%s)" % (T.ten_cung(ls, cung), T.CHI[cung])
            ht = ", ".join("%s %s→%s" % (x.replace("Hóa ", ""), s, T.ten_cung(ls, ls["vt"][s]))
                           for x, s in zip(T.HOA, T.TU_HOA[can]))
        print("| %s (%02d–%02dh) | %s | %s | %+.1f | %s | %s | %s | %s | %+.1f |" % (
            T.CHI[z], (2 * z - 1) % 24, (2 * z + 1) % 24, B.vn(gz), V.thap_than(nc, gz[0]), bt, ", ".join(ly) or "-",
            ct, ht, "-" if tv is None else "%+.1f" % tv, bt + (tv or 0)))
    print("(Giờ Tý 23–01h tính theo ngày đã chọn; can giờ theo can ngày của chính ngày đó.)")
    print()


def them_lenh(sub):
    import nc
    p = sub.add_parser("luunhat", help="lưu nhật / lưu thời Bát tự + Tử vi")
    nc.them_tham_so_sinh(p, gioi_bat_buoc=True)
    p.add_argument("--tu")
    p.add_argument("--den")
    p.add_argument("--ngay-xem", help="xem lưu thời 12 giờ của một ngày YYYY-MM-DD")
    p.add_argument("--dung")
    p.add_argument("--ky")
    p.set_defaults(_chay=chay)


def chay(a):
    if not a.ngay:
        raise SystemExit("LỖI: cần --ngay (ngày sinh).")
    tt = B.doc_dau_vao(a)
    for c in tt.canh_bao:
        print("! " + c)
    _, _, tru = B.tu_tru(tt)
    tru3 = [(nh, gz[0], gz[1]) for nh, gz in tru]
    dung, ky = anh._doc_hanh(a.dung), anh._doc_hanh(a.ky)
    md = dung is None
    if md:
        dung, ky = anh.hy_ky_mac_dinh(tru3)
    ky = ky or set()
    def f(s):
        try:
            return dt.date(*[int(v) for v in s.replace("/", "-").split("-")])
        except (ValueError, TypeError):
            raise SystemExit("LỖI: ngày phải có dạng YYYY-MM-DD: %r" % s)
    for x in (a.tu, a.ngay_xem):
        if x and f(x) < tt.dong_ho.date():
            print("! Ngày xem trước ngày sinh – bỏ qua những ngày đó khi luận.")
    if a.ngay_xem:
        in_luu_thoi(tt, f(a.ngay_xem), dung, ky)
    if a.tu and a.den:
        in_luu_nhat(tt, f(a.tu), f(a.den), dung, ky, md)
    if not a.ngay_xem and not (a.tu and a.den):
        raise SystemExit("LỖI: cần --tu và --den (lưu nhật) hoặc --ngay-xem (lưu thời).")


def tu_kiem():
    import argparse
    loi = []
    ns = argparse.Namespace(ngay="2000-01-01", gio="10:00", gioi="nam", noi="Hà Nội", kinhdo=None, mien=None,
                            utc=None, am=False, nhuan=False, lich_tz=None, gio_dong_ho=False, ty=1)
    tt = B.doc_dau_vao(ns)
    ls = anh.lap_tu_tt(tt)
    # Đẩu Quân: sinh tháng 11 giờ Tỵ (5); năm Bính Ngọ 2026 (Thái Tuế Ngọ = 6): 6 − 10 + 5 = 1 → Sửu
    if (ls["thang"], ls["gio"]) != (11, 5) or cung_thang_gieng(ls, 2026) != 1:
        loi.append("Đẩu Quân năm 2026: %s" % cung_thang_gieng(ls, 2026))
    # lưu nhật đi thuận: mùng 1 tháng Giêng ở Sửu, mùng 3 ở Mão
    if (cung_thang_gieng(ls, 2026) + 2) % 12 != 3:
        loi.append("lưu nhật đi thuận")
    # can chi ngày lấy đúng: 2026-11-09 là Đinh Hợi (khớp chonngay v2)
    gz = Solar.fromYmd(2026, 11, 9).getLunar().getDayInGanZhi()
    if B.vn(gz) != "Đinh Hợi":
        loi.append("can chi ngày 09/11/2026")
    s, ly = diem_bt("壬子", [("Năm", "己", "卯"), ("Tháng", "丙", "子"), ("Ngày", "戊", "午"), ("Giờ", "丁", "巳")],
                    {1, 2}, {0, 3, 4})
    if "xung chi ngày" not in " ".join(ly) or s >= 0:
        loi.append("ngày Nhâm Tý phải xung chi ngày Ngọ và điểm âm: %s %s" % (s, ly))
    return loi
