# -*- coding: utf-8 -*-
"""linhchinh.py - Linh thần / Chính thần (零神 / 正神): 8 cung của nhà, 4 cung "vượng" 4 cung "suy" theo nguyên vận.

Lệnh: python3 tvbt/nc.py linhchinh [--nam N] [--huong ĐỘ|SƠN | --toa ĐỘ|SƠN] [--nuoc "Bắc,Đông"] [--nui "Nam"]

Gốc: Thanh nang tự / Thiên ngọc kinh "Nhược ngộ chính thần chính vị trang, bát thủy nhập linh đường"
(若遇正神正位裝，撥水入零堂): chính thần nên có núi, đất cao, vật đặc; linh thần nên có nước, chỗ trống, thấp.
Có ba cách định cung linh / chính, đều in ra để đối chiếu:
  A. Đại vận hai nguyên (Đại huyền không, Tam nguyên): thượng nguyên (vận 1–4) chính thần là 1-2-3-4
     (Khảm Khôn Chấn Tốn), linh thần 6-7-8-9 (Càn Đoài Cấn Ly); hạ nguyên (vận 6–9) đảo lại. Vận 5 chia đôi:
     10 năm đầu thuộc thượng nguyên, 10 năm sau thuộc hạ nguyên. Năm tính theo tam nguyên cửu vận (1864 vận 1).
  B. Đàm Dưỡng Ngô, Huyền không lục pháp (nhị nguyên bát vận): vận dài ngắn theo quái tiên thiên (hào dương 9 năm,
     hào âm 6 năm: 18, 24, 24, 24, 21, 21, 21, 27 năm từ 1864); "đại kim long" là cung số 5 bay tới khi đưa số vận
     vào trung cung (vận lẻ bay thuận, chẵn bay nghịch) – đó là linh thần; nhóm linh đổi theo từng vận:
     vận 1, 3, 6, 8 linh ở 6-7-8-9; vận 2, 4, 7, 9 linh ở 1-2-3-4.
  C. Tam nguyên cửu vận, từng vận 20 năm (Ôn Minh Viễn, Thẩm Trúc Nhưng): chính thần là cung số vận, linh thần là cung
     đối diện (hợp mười), chiếu thần là cung hợp năm theo Hà đồ (vận 9 → Tốn, vận 8 → Chấn).
Vận 9 (2024–2043) ba cách cùng kết luận: chính thần Ly, Càn, Đoài, Cấn; linh thần Khảm, Khôn, Chấn, Tốn.
"""
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SO_CUNG = [1, 2, 3, 4, 6, 7, 8, 9]
TEN = {1: "Khảm", 2: "Khôn", 3: "Chấn", 4: "Tốn", 6: "Càn", 7: "Đoài", 8: "Cấn", 9: "Ly"}
PHUONG = {1: "Bắc", 2: "Tây Nam", 3: "Đông", 4: "Đông Nam", 6: "Tây Bắc", 7: "Tây", 8: "Đông Bắc", 9: "Nam"}
SO_CUA_PHUONG = {v: k for k, v in PHUONG.items()}
# Lạc thư bay: trung cung -> Càn -> Đoài -> Cấn -> Ly -> Khảm -> Khôn -> Chấn -> Tốn
DUONG_BAY = [5, 6, 7, 8, 9, 1, 2, 3, 4]
DAI_NGUYEN_BAT_VAN = [(1, 18), (2, 24), (3, 24), (4, 24), (6, 21), (7, 21), (8, 21), (9, 27)]


def van_tam_nguyen(nam):
    return ((nam - 1864) // 20) % 9 + 1


def nguyen_A(nam):
    """'thuong' | 'ha' – vận 5 chia đôi (10 năm đầu thượng, 10 năm sau hạ)."""
    return "thuong" if (nam - 1864) % 180 < 90 else "ha"


def van_B(nam):
    """Vận theo nhị nguyên bát vận của Đàm Dưỡng Ngô -> (vận, năm đầu, năm cuối)."""
    goc = 1864 + 180 * ((nam - 1864) // 180)
    t = goc
    for v, dai in DAI_NGUYEN_BAT_VAN:
        if nam < t + dai:
            return v, t, t + dai - 1
        t += dai
    raise AssertionError


def kim_long(van):
    """Cung 'đại kim long' (số 5 bay tới) khi đưa số vận vào trung cung; vận lẻ thuận, chẵn nghịch."""
    buoc = (5 - van) % 9 if van % 2 else (van - 5) % 9
    return DUONG_BAY[buoc]


def nhom(chinh_thap):
    return [1, 2, 3, 4] if chinh_thap else [6, 7, 8, 9]


def bang(nam):
    """-> dict theo 3 cách; mỗi cách: chinh=[số cung], linh=[số cung], ghi."""
    vA = van_tam_nguyen(nam)
    nA = nguyen_A(nam)
    A = dict(chinh=nhom(nA == "thuong"), linh=nhom(nA != "thuong"),
             ghi="%s nguyên (vận %d tam nguyên)" % ("Thượng" if nA == "thuong" else "Hạ", vA))
    vB, b0, b1 = van_B(nam)
    kl = kim_long(vB)
    linh_thap = kl in (1, 2, 3, 4)
    B = dict(chinh=nhom(not linh_thap), linh=nhom(linh_thap), kim_long=kl,
             ghi="vận %d nhị nguyên bát vận (%d–%d), đại kim long ở %s" % (vB, b0, b1, TEN[kl]))
    if vA == 5:
        nua_dau = (nam - 1864) % 20 < 10
        cv, lv = (4, 6) if nua_dau else (6, 4)
        C = dict(chinh=[cv], linh=[lv], chieu=[], ghi="vận 5 (%s 10 năm: chính thần %s, linh thần %s)" % (
            "nửa đầu" if nua_dau else "nửa sau", TEN[cv], TEN[lv]))
    else:
        C = dict(chinh=[vA], linh=[10 - vA], chieu=[vA - 5 if vA > 5 else vA + 5],
                 ghi="vận %d tam nguyên: chính thần %s, linh thần %s, chiếu thần %s" % (
                     vA, TEN[vA], TEN[10 - vA], TEN[vA - 5 if vA > 5 else vA + 5]))
    return dict(A=A, B=B, C=C)


def danh_gia(so, b):
    """'chinh' | 'linh' | 'khac nhau' cho một cung theo A và B (C chỉ đánh dấu điểm mạnh nhất)."""
    a = "chinh" if so in b["A"]["chinh"] else "linh"
    bb = "chinh" if so in b["B"]["chinh"] else "linh"
    return a if a == bb else "khac nhau"


def in_bang(nam, toa=None, nuoc=(), nui=(), gon=False):
    b = bang(nam)
    print("LINH THẦN – CHÍNH THẦN NĂM %d (8 cung quanh tâm nhà, mỗi cung 45°)" % nam)
    print("- A. Đại vận hai nguyên: %s → chính thần %s; linh thần %s." % (
        b["A"]["ghi"], ", ".join(TEN[x] for x in b["A"]["chinh"]), ", ".join(TEN[x] for x in b["A"]["linh"])))
    print("- B. Đàm Dưỡng Ngô (Huyền không lục pháp): %s → chính thần %s; linh thần %s." % (
        b["B"]["ghi"], ", ".join(TEN[x] for x in b["B"]["chinh"]), ", ".join(TEN[x] for x in b["B"]["linh"])))
    print("- C. Từng vận 20 năm: %s." % b["C"]["ghi"])
    dong = all(danh_gia(x, b) != "khac nhau" for x in SO_CUNG)
    print("- %s" % ("Ba cách ĐỒNG THUẬN năm này." if dong and set(b["C"]["chinh"]) <= set(b["A"]["chinh"])
                     and set(b["C"]["linh"] + b["C"]["chieu"]) <= set(b["A"]["linh"])
                     else "Các cách KHÁC NHAU năm này – nói rõ khi luận, ưu tiên cung mà các cách cùng xếp."))
    print()
    print("| Cung | Phương | A | B | C | Nên có |")
    print("|---|---|---|---|---|---|")
    for x in SO_CUNG:
        a = "chính" if x in b["A"]["chinh"] else "linh"
        bb = ("chính" if x in b["B"]["chinh"] else "linh") + (" (kim long)" if x == b["B"]["kim_long"] else "")
        c = "chính thần" if x in b["C"]["chinh"] else ("linh thần" if x in b["C"]["linh"] else
                                                     ("chiếu thần" if x in b["C"]["chieu"] else "-"))
        dg = danh_gia(x, b)
        nen = {"chinh": "cao, đặc, tĩnh: nhà cao bên ngoài, tường kín, tủ kệ nặng, phòng ngủ yên",
               "linh": "thấp, trống, động: sân, lối đi, cửa sổ lớn, chỗ có nước (bể, hồ, máng nước)",
               "khac nhau": "các cách nói khác nhau – để trung tính"}[dg]
        print("| %s %d | %s | %s | %s | %s | %s |" % (TEN[x], x, PHUONG[x], a, bb, c, nen))
    print()
    if toa is not None:
        in_toa(toa, b)
    if nuoc or nui:
        print("ĐỐI CHIẾU NƯỚC / NÚI THẬT (chính thần cần núi, linh thần cần nước):")
        for p in nuoc:
            x = SO_CUA_PHUONG[p]
            dg = danh_gia(x, b)
            print("- Nước/trống ở %s (%s): %s" % (p, TEN[x], {"linh": "hợp (bát thủy nhập linh đường)",
                                                             "chinh": "PHẠM: nước ở chính thần (linh chính điên đảo)",
                                                             "khac nhau": "các cách nói khác nhau"}[dg]))
        for p in nui:
            x = SO_CUA_PHUONG[p]
            dg = danh_gia(x, b)
            print("- Núi/nhà cao ở %s (%s): %s" % (p, TEN[x], {"chinh": "hợp (chính thần chính vị trang)",
                                                              "linh": "PHẠM: núi ở linh thần (linh chính điên đảo)",
                                                              "khac nhau": "các cách nói khác nhau"}[dg]))
        print()
    if not gon:
        print(GHI_CHU)


def in_toa(toa, b):
    import toason as TS
    huong = (toa + 12) % 24
    ct = next(q for q, ds in TS.CUNG_SON.items() if toa in ds)
    ch = next(q for q, ds in TS.CUNG_SON.items() if huong in ds)
    so = {v: k for k, v in TS.CUNG_QUAI.items()}
    st, sh = so[ct], so[ch]
    gt, gh = danh_gia(st, b), danh_gia(sh, b)
    print("NHÀ tọa %s – hướng %s (mặt tiền nhìn về phía %s):" % (TS.SON_VN[toa], TS.SON_VN[huong], PHUONG[sh]))
    print("- Lưng (tọa) ở cung %s: %s; mặt (hướng) ở cung %s: %s." % (
        TEN[st], {"chinh": "chính thần", "linh": "linh thần", "khac nhau": "các cách nói khác nhau"}[gt],
        TEN[sh], {"chinh": "chính thần", "linh": "linh thần", "khac nhau": "các cách nói khác nhau"}[gh]))
    if gt == "chinh" and gh == "linh":
        print("- 'Tọa chính hướng linh': lưng đặc ở chính thần, mặt thoáng ở linh thần – hợp cục theo phép linh chính.")
    elif gt == "linh" and gh == "chinh":
        print("- 'Tọa linh hướng chính': lưng ở linh thần, mặt ở chính thần – phép linh chính coi là điên đảo nếu "
              "phía mặt thoáng/có nước và phía lưng đặc. Tưởng Đại Hồng (Dương trạch chỉ nam) lại khen cửa mở ở cung "
              "đương nguyên vượng (vd hạ nguyên cửa Ly). Hai cách khác nhau ở chỗ cửa – nói rõ, xem thêm Huyền không.")
    else:
        print("- Lưng và mặt không chia rõ chính / linh năm này.")
    print()


GHI_CHU = """CÁCH DÙNG (nói rõ khi luận):
1. Lập cực: lấy TÂM NHÀ (giao hai đường chéo của phần có mái; nhà khuyết góc thì bù cho vuông, phần lồi nhỏ thì bỏ;
   nhà chữ L lấy trọng tâm). Đứng ở tâm đo la bàn, chia 8 cung, mỗi cung 45° (Bắc 337,5°–22,5°…). Hiệp Kỷ: "la bàn
   24 phương không co giãn" – nhà dài thì cung hẹp cung rộng, không chia ô vuông.
2. Chính thần: nên cao, đặc, tĩnh. Linh thần: nên thấp, trống, động, có nước. Đặt ngược (nước ở chính thần, núi/nhà
   cao chắn ở linh thần) gọi là linh chính điên đảo, sách cho là xấu nhất.
3. Cửa chính: phái Đàm Dưỡng Ngô cho cửa (khí khẩu) ở linh thần ("tọa chính hướng linh"); Tưởng Đại Hồng khen cửa ở
   cung đương nguyên vượng (hạ nguyên: Ly, Đoài, Cấn, Càn). Phép này không thay được Huyền không phi tinh, Bát trạch –
   dùng để đối chiếu, chỗ các phép cùng nói thì mới chắc.
4. Đổi nguyên: hạ nguyên kéo đến hết vận 9 (Lập Xuân 2044); thượng nguyên từ 2044 thì 4 cung đảo lại."""


# ---------------------------------------------------------------- CLI
def them_lenh(sub):
    p = sub.add_parser("linhchinh", help="Linh thần – chính thần: 4 cung vượng, 4 cung suy theo nguyên vận, có đối chiếu nhà")
    p.add_argument("--nam", type=int, help="năm xem (tính từ Lập Xuân); mặc định năm hiện tại")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--huong", help="hướng nhà: độ la bàn phía mặt nhà, hoặc tên sơn")
    g.add_argument("--toa", help="tọa (lưng nhà): độ la bàn hoặc tên sơn")
    p.add_argument("--nuoc", help="phương có nước / sân trống / đường thật, vd \"Bắc,Đông\"")
    p.add_argument("--nui", help="phương có núi / nhà cao / tường cao, vd \"Nam\"")
    p.set_defaults(_chay=chay)


def nam_hien_tai():
    now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None) + dt.timedelta(hours=7)
    return now.year if (now.month, now.day) >= (2, 4) else now.year - 1


def chay(a):
    import huyenkhong2 as H
    import toason as TS
    nam = a.nam or nam_hien_tai()
    if not 1864 <= nam <= 2200:
        raise SystemExit("LỖI: --nam ngoài phạm vi 1864-2200.")
    toa = None
    if a.toa or a.huong:
        toa, _, cb = TS.doc_toa(a.toa, a.huong)
        if cb:
            print("CHÚ Ý: " + cb)
    in_bang(nam, toa, H.doc_phuong(a.nuoc), H.doc_phuong(a.nui))


# ---------------------------------------------------------------- tự kiểm
def tu_kiem():
    loi = []
    # đại kim long theo Đàm Dưỡng Ngô: 1 Ly, 2 Khôn, 3 Đoài, 4 Tốn, 6 Càn, 7 Chấn, 8 Cấn, 9 Khảm
    if [kim_long(v) for v in (1, 2, 3, 4, 6, 7, 8, 9)] != [9, 2, 7, 4, 6, 3, 8, 1]:
        loi.append("đại kim long")
    # nhị nguyên bát vận: 1996–2016 vận 8, 2017–2043 vận 9, 2044 vận 1; mỗi nguyên 90 năm
    if van_B(2016)[0] != 8 or van_B(2017)[:3] != (9, 2017, 2043) or van_B(2044)[0] != 1 or van_B(1953)[0] != 4 \
            or van_B(1954)[0] != 6:
        loi.append("nhị nguyên bát vận")
    # A: 1953 thượng, 1954 hạ, 2043 hạ, 2044 thượng
    if [nguyen_A(y) for y in (1953, 1954, 2043, 2044)] != ["thuong", "ha", "ha", "thuong"]:
        loi.append("thượng / hạ nguyên")
    # vận 9: ba cách đồng thuận (sina, zggdfs, Đàm Dưỡng Ngô): chính Ly Càn Đoài Cấn, linh Khảm Khôn Chấn Tốn
    b = bang(2030)
    if b["A"]["chinh"] != [6, 7, 8, 9] or b["B"]["chinh"] != [6, 7, 8, 9] or b["C"]["chinh"] != [9] or \
            b["C"]["linh"] != [1] or b["C"]["chieu"] != [4]:
        loi.append("vận 9")
    # vận 8 tam nguyên (2004–2023): chính Cấn, linh Khôn, chiếu Chấn; năm 2010 Đàm Dưỡng Ngô là vận 8 -> linh ở 6-9
    b = bang(2010)
    if b["C"]["chinh"] != [8] or b["C"]["linh"] != [2] or b["C"]["chieu"] != [3] or b["B"]["linh"] != [6, 7, 8, 9]:
        loi.append("vận 8")
    # vận 5: 10 năm đầu Tốn chính Càn linh, 10 năm sau đảo
    if bang(1950)["C"]["chinh"] != [4] or bang(1958)["C"]["chinh"] != [6]:
        loi.append("vận 5")
    return loi
