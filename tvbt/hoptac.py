# -*- coding: utf-8 -*-
"""hoptac.py - Chấm điểm hợp tác / hôn nhân giữa các người theo Bát tự (thang 100), có ma trận nhiều người.
Tiêu chí: trụ ngày (can ngũ hợp/sinh/khắc, chi hợp/xung/hình/hại/phá), chi tháng, chi năm, hành bổ trợ dụng
thần của nhau, (hôn nhân) sao phối ngẫu và cung phối, thiên khắc địa xung.
Lệnh: nc.py hoptac --nguoi "An,1990-05-17,08:30,nam" "Bình,1988-03-05,,nam" [--loai honnhan]
  (mỗi người: tên, ngày, giờ (có thể trống), nam|nu, thêm 'am' nếu ngày âm lịch, thêm tên tỉnh nếu biết;
   thêm 'dung=Kim+Thủy' và 'ky=Hỏa' nếu đã chọn dụng thần cho người đó)
"""
import argparse
import itertools

import tvbt as B
import vuongsuy as V

XUNG = lambda a, b: (a - b) % 12 == 6
LUC_HOP = {frozenset(x) for x in [(0, 1), (2, 11), (3, 10), (4, 9), (5, 8), (6, 7)]}
TAM_HOP = [{8, 0, 4}, {11, 3, 7}, {2, 6, 10}, {5, 9, 1}]
HAI = {frozenset(x) for x in [(0, 7), (1, 6), (2, 5), (3, 4), (8, 11), (9, 10)]}
PHA = {frozenset(x) for x in [(0, 9), (1, 4), (2, 11), (3, 6), (5, 8), (7, 10)]}
HINH = {frozenset(x) for x in [(2, 5), (5, 8), (2, 8), (1, 10), (10, 7), (1, 7), (0, 3)]}
NGU_HOP = {frozenset(x) for x in [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]}


def doc_nguoi(s):
    phan = [x.strip() for x in s.split(",")]
    if len(phan) < 2:
        raise SystemExit("LỖI: --nguoi dạng 'Tên,YYYY-MM-DD[,HH:MM][,nam|nu][,am][,tỉnh][,dung=Kim+Thủy][,ky=Hỏa]'")
    ten, ngay = phan[0], phan[1]
    gio, gioi, am, noi, dung, ky = None, None, False, None, None, None
    for x in phan[2:]:
        if not x:
            continue
        if x.replace(":", "").replace("h", "").isdigit() and any(c in x for c in ":h"):
            g = x.replace("h", ":")
            gio = g + "00" if g.endswith(":") else g
        elif x in ("nam", "nu"):
            gioi = x
        elif x == "am":
            am = True
        elif x.startswith("dung="):
            dung = x[5:]
        elif x.startswith("ky="):
            ky = x[3:]
        else:
            noi = x
    ns = argparse.Namespace(ngay=ngay, gio=gio, gioi=gioi or "nam", noi=noi, kinhdo=None, mien=None, utc=None,
                            am=am, nhuan=False, lich_tz=None, gio_dong_ho=False, ty=1)
    tt = B.doc_dau_vao(ns)
    for c in tt.canh_bao:
        print("! %s: %s" % (ten, c))
    _, _, tru = B.tu_tru(tt)
    tru3 = [(nh, gz[0], gz[1]) for nh, gz in tru]
    import anh
    if dung:
        d, k = anh._doc_hanh(dung), anh._doc_hanh(ky or "")
        md = False
    else:
        d, k = anh.hy_ky_mac_dinh(tru3)
        md = True
        cb = anh.canh_bao_cuc_doan(tru3)
        if cb:
            print("! %s: %s" % (ten, cb))
    hanh = V.thang_b(tru3)[4]
    noi_bat = sorted(range(5), key=lambda i: -hanh[i])[:2]
    return dict(ten=ten, tt=tt, tru=tru3, gioi=gioi, dung=d, ky=k or set(), md=md, hanh=hanh, noi_bat=noi_bat,
                co_gio=tt.co_gio)


def _chi(p, i):
    return V.ZHI.index(p["tru"][i][2])


def _can(p, i):
    return V.GAN.index(p["tru"][i][1])


def quan_he_chi(a, b):
    """Điểm và tên quan hệ giữa hai chi (thang −3..+3)."""
    if a == b:
        return (-1, "tự hình") if a in (4, 6, 9, 11) else (0.5, "trùng")
    if XUNG(a, b):
        return -3, "xung"
    if frozenset((a, b)) in LUC_HOP:
        return 3, "lục hợp"
    if any(a in t and b in t for t in TAM_HOP):
        return 2, "tam hợp"
    if frozenset((a, b)) in HINH:
        return -1.5, "hình"
    if frozenset((a, b)) in HAI:
        return -1.5, "hại"
    if frozenset((a, b)) in PHA:
        return -1, "phá"
    return 0, "bình thường"


def quan_he_can(a, b):
    if frozenset((a, b)) in NGU_HOP:
        return 2, "ngũ hợp"
    ha, hb = V.GAN_H[a], V.GAN_H[b]
    if ha == hb:
        return 0.5, "đồng hành"
    if (hb - ha) % 5 in (1, 4):
        return 1, "tương sinh"
    if (a - b) % 10 in (4, 6) and abs(a - b) == 6:
        return -2, "can xung"
    return -1, "tương khắc"


def bo_tro(p, q):
    """q mang đến cho p bao nhiêu hành p cần (−5..+5)."""
    s = 0
    for i in q["noi_bat"]:
        if i in p["dung"]:
            s += 2.5
        elif i in p["ky"]:
            s -= 2.5
    hq = V.GAN_H[_can(q, 2)]
    s += 1 if hq in p["dung"] else (-1 if hq in p["ky"] else 0)
    return max(-5, min(5, s))


def cham_cap(p, q, loai="hoptac"):
    ct = []
    # trụ ngày (35): can 10, chi 25
    sc, tc = quan_he_can(_can(p, 2), _can(q, 2))
    sz, tz = quan_he_chi(_chi(p, 2), _chi(q, 2))
    d_ngay = 17.5 + sc * 2.5 + sz * 4.2
    ct.append("ngày: can %s, chi %s" % (tc, tz))
    tkdx = XUNG(_chi(p, 2), _chi(q, 2)) and sc < 0
    # dụng thần bổ trợ (25)
    b1, b2 = bo_tro(p, q), bo_tro(q, p)
    d_dung = 12.5 + 1.25 * (b1 + b2)
    ct.append("bổ trợ hành: %s→%s %+.1f, %s→%s %+.1f" % (q["ten"], p["ten"], b1, p["ten"], q["ten"], b2))
    # chi tháng (15), chi năm (10)
    st, tm = quan_he_chi(_chi(p, 1), _chi(q, 1))
    sy, ty_ = quan_he_chi(_chi(p, 0), _chi(q, 0))
    d_thang = 7.5 + st * 2.5
    d_nam = 5 + sy * 1.67
    ct.append("tháng: %s; năm: %s" % (tm, ty_))
    # chéo (5): chi ngày người này với chi năm người kia
    sx1, _ = quan_he_chi(_chi(p, 2), _chi(q, 0))
    sx2, _ = quan_he_chi(_chi(q, 2), _chi(p, 0))
    d_cheo = 2.5 + (sx1 + sx2) * 0.4
    # hôn nhân (10) / vai trò (10)
    d_rieng = 5
    if loai == "honnhan":
        for x, y in ((p, q), (q, p)):
            if x["gioi"]:
                sao = V.thap_than(x["tru"][2][1], y["tru"][2][1])
                muon = "Chính Tài" if x["gioi"] == "nam" else "Chính Quan"
                if sao == muon:
                    d_rieng += 2.5
                    ct.append("%s là sao phối ngẫu (%s) của %s" % (y["ten"], muon, x["ten"]))
    else:
        tt1 = V.nhom(p["tru"][2][1], q["tru"][2][1])
        tt2 = V.nhom(q["tru"][2][1], p["tru"][2][1])
        ct.append("%s là %s của %s; %s là %s của %s" % (q["ten"], tt1, p["ten"], p["ten"], tt2, q["ten"]))
        if tt1 in ("Tài", "Ấn") or tt2 in ("Tài", "Ấn"):
            d_rieng += 2.5
        if tt1 == "Tỷ Kiếp" and tt2 == "Tỷ Kiếp":
            d_rieng -= 2.5
    phan = [d_ngay, d_dung, d_thang, d_nam, d_cheo, d_rieng]
    phan = [max(0, min(m, x)) for x, m in zip(phan, (35, 25, 15, 10, 5, 10))]
    tong = round(sum(phan))
    if tkdx:
        ct.append("THIÊN KHẮC ĐỊA XUNG trụ ngày")
    return tong, [round(x, 1) for x in phan], ct, tkdx


def muc(tong):
    return ("rất hợp" if tong >= 75 else "khá hợp" if tong >= 62 else "trung bình" if tong >= 48
            else "kém hợp, cần cơ chế phối hợp rõ")


def in_hop_tac(ds, loai="hoptac"):
    print("CHẤM ĐIỂM %s (Bát tự, thang 100)" % ("HÔN NHÂN" if loai == "honnhan" else "HỢP TÁC"))
    print("| Người | Tứ trụ | Nhật chủ | Hành nổi | Hành cần / kỵ |")
    print("|---|---|---|---|---|")
    for p in ds:
        print("| %s | %s%s | %s | %s | %s / %s%s |" % (
            p["ten"], ", ".join(B.vn(g + z) for _, g, z in p["tru"]), "" if p["co_gio"] else " (không giờ)",
            B.vn(p["tru"][2][1]) + " " + V.HANH_VN[V.GAN_H[V.GAN.index(p["tru"][2][1])]],
            ", ".join(V.HANH_VN[i] for i in p["noi_bat"]), ", ".join(V.HANH_VN[i] for i in sorted(p["dung"])),
            ", ".join(V.HANH_VN[i] for i in sorted(p["ky"])), " (mặc định)" if p["md"] else ""))
    print()
    print("| Cặp | Điểm | Mức | Ngày /35 | Hành /25 | Tháng /15 | Năm /10 | Chéo /5 | %s /10 | Căn cứ |" % (
        "Phối ngẫu" if loai == "honnhan" else "Vai trò"))
    print("|---|---|---|---|---|---|---|---|---|---|")
    kq = []
    for p, q in itertools.combinations(ds, 2):
        tong, phan, ct, tkdx = cham_cap(p, q, loai)
        kq.append((p["ten"], q["ten"], tong, tkdx))
        print("| %s – %s | %d | %s | %s | %s |" % (p["ten"], q["ten"], tong, muc(tong),
                                               " | ".join("%g" % x for x in phan), "; ".join(ct)))
    print()
    if any(x[3] for x in kq):
        print("! Có cặp thiên khắc địa xung trụ ngày: không nên xếp làm việc trực tiếp hằng ngày một tuyến; "
              "nên có người trung gian hoặc phân vai rõ.")
    if any(p["md"] for p in ds):
        print("! Hành cần/kỵ đánh dấu 'mặc định' là phù ức đơn giản theo điểm vượng suy; khi đã chọn dụng thần "
              "cho người đó, truyền lại bằng dung=…,ky=… để điểm chính xác hơn.")
    print("(Điểm chỉ phản ánh độ hòa hợp theo Bát tự; không thay cho đánh giá năng lực, uy tín và thỏa thuận rõ ràng.)")
    print()
    return kq


def them_lenh(sub):
    p = sub.add_parser("hoptac", help="chấm điểm hợp tác / hôn nhân nhiều người theo Bát tự")
    p.add_argument("--nguoi", nargs="+", required=True)
    p.add_argument("--loai", default="hoptac", choices=["hoptac", "honnhan"])
    p.set_defaults(_chay=chay)


def chay(a):
    ds = [doc_nguoi(x) for x in a.nguoi]
    if len(ds) < 2:
        raise SystemExit("LỖI: cần ít nhất 2 người.")
    in_hop_tac(ds, a.loai)


def tu_kiem():
    loi = []
    # bảng quan hệ chi
    for a, b, t in [(0, 6, "xung"), (0, 1, "lục hợp"), (8, 4, "tam hợp"), (2, 5, "hình"), (0, 7, "hại"),
                    (0, 9, "phá"), (3, 0, "hình")]:
        if quan_he_chi(a, b)[1] != t:
            loi.append("quan hệ %d-%d phải là %s" % (a, b, t))
    if quan_he_can(0, 5)[1] != "ngũ hợp" or quan_he_can(0, 6)[0] != -2 or quan_he_can(0, 4)[0] != -1:
        loi.append("quan hệ can Giáp–Kỷ / Giáp–Canh / Giáp–Mậu")
    if quan_he_chi(4, 4)[1] != "tự hình" or quan_he_chi(0, 0)[1] != "trùng":
        loi.append("tự hình Thìn")
    if doc_nguoi("D,2000-01-01,9h30,nam,Hà Nội")["tt"].dong_ho.hour != 9:
        loi.append("giờ dạng 9h30")
    p = doc_nguoi("A,2000-01-01,10:00,nam,Hà Nội")       # Mậu Ngọ
    q = doc_nguoi("B,2000-07-01,10:00,nu,Hà Nội")
    if p["tru"][2][1:] != ("戊", "午"):
        loi.append("trụ ngày A phải Mậu Ngọ")
    for x, y in ((p, q), (q, p)):
        t, phan, ct, _ = cham_cap(x, y)
        if not (0 <= t <= 100):
            loi.append("điểm ngoài 0-100")
    t1 = cham_cap(p, q)[0]
    t2 = cham_cap(q, p)[0]
    if t1 != t2:
        loi.append("điểm không đối xứng %d/%d" % (t1, t2))
    # thiên khắc địa xung: Mậu Ngọ – Nhâm Tý (Mậu khắc Nhâm, Ngọ xung Tý)
    r = doc_nguoi("C,2000-01-01,10:00,nam,Hà Nội")
    r["tru"][2] = ("Ngày", "壬", "子")
    if not cham_cap(p, r)[3]:
        loi.append("Mậu Ngọ – Nhâm Tý phải là thiên khắc địa xung")
    return loi
