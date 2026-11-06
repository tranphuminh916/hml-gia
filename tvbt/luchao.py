# -*- coding: utf-8 -*-
"""luchao.py - Lục hào nạp giáp (bốc dịch theo Kinh Phòng – Hỏa Châu Lâm – Tăng San Bốc Dịch).

Lập quẻ: 6 số hào (6/7/8/9), gieo 3 đồng xu, theo thời gian hoặc theo số như Mai hoa.
Tính: bát cung, thế ứng, nạp giáp quẻ chủ và quẻ biến, lục thân, lục thần, tuần không, phục thần,
nguyệt kiến – nhật thần (vượng tướng hưu tù tử, nguyệt phá, ám động, nhật phá, sinh khắc hợp),
động biến (hồi đầu sinh khắc, tiến thoái thần, phục ngâm, phản ngâm, hóa không / phá / mộ / tuyệt),
quẻ lục xung / lục hợp, dụng thần – nguyên thần – kỵ thần – cừu thần theo việc hỏi, gợi ý ứng kỳ.

Mọi bảng 64 quẻ đều SINH bằng thuật toán (bát cung từ quẻ thuần, nạp giáp từ quy tắc dương thuận âm nghịch),
rồi đối chiếu trong tu_kiem() với bảng chuẩn và ví dụ sách.
Lệnh: python3 tvbt/nc.py luchao --hao 7 8 8 6 9 8 --ngay 2026-10-31 --gio 09:30 --viec taichinh
"""
import datetime as dt
import io
import re
from contextlib import redirect_stdout

import maihoa as M

CAN_VN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI_VN = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
HANH_CHI = ["Thủy", "Thổ", "Mộc", "Mộc", "Thổ", "Hỏa", "Hỏa", "Thổ", "Kim", "Kim", "Thổ", "Thủy"]
SINH, KHAC = M.SINH, M.KHAC

# ---------------------------------------------------------------- Bát quái (lấy từ maihoa: hào dưới -> trên)
SO_QUAI = {v[0]: k for k, v in M.QUAI.items()}            # tên -> số tiên thiên
BIT = {v[0]: v[1] for v in M.QUAI.values()}               # tên -> (hào 1, 2, 3), 1 = dương
HANH_QUAI = {v[0]: v[2] for v in M.QUAI.values()}
TEN_BIT = {v: k for k, v in BIT.items()}
THU_TU_CUNG = ["Càn", "Khảm", "Cấn", "Chấn", "Tốn", "Ly", "Khôn", "Đoài"]   # thứ tự bát cung Kinh Phòng
THE_LOAI = ["Bát thuần", "Nhất thế", "Nhị thế", "Tam thế", "Tứ thế", "Ngũ thế", "Du hồn", "Quy hồn"]
# Can nạp giáp (nội, ngoại): Càn Giáp/Nhâm, Khôn Ất/Quý, Chấn Canh, Tốn Tân, Khảm Mậu, Ly Kỷ, Cấn Bính, Đoài Đinh
CAN_NAP = {"Càn": (0, 8), "Khôn": (1, 9), "Chấn": (6, 6), "Tốn": (7, 7),
           "Khảm": (4, 4), "Ly": (5, 5), "Cấn": (2, 2), "Đoài": (3, 3)}
LUC_THAN = ["Phụ Mẫu", "Huynh Đệ", "Tử Tôn", "Thê Tài", "Quan Quỷ"]
LUC_THAN_KHOA = {"phumau": "Phụ Mẫu", "huynhde": "Huynh Đệ", "tuton": "Tử Tôn", "thetai": "Thê Tài",
                 "quanquy": "Quan Quỷ"}
LUC_THAN_6 = ["Thanh Long", "Chu Tước", "Câu Trần", "Đằng Xà", "Bạch Hổ", "Huyền Vũ"]
KHOI_LUC_THAN = [0, 0, 1, 1, 2, 3, 4, 4, 5, 5]           # can ngày -> lục thần ở hào 1
TRUONG_SINH_12 = ["Trường sinh", "Mộc dục", "Quan đới", "Lâm quan", "Đế vượng", "Suy", "Bệnh", "Tử", "Mộ",
                  "Tuyệt", "Thai", "Dưỡng"]
# Trường sinh ngũ hành (Thổ theo Thủy, như Tăng San Bốc Dịch)
KHOI_TRUONG_SINH = {"Mộc": 11, "Hỏa": 2, "Kim": 5, "Thủy": 8, "Thổ": 8}
TIET_THANG = {2: "Lập Xuân ≈ 4/2", 3: "Kinh Trập ≈ 6/3", 4: "Thanh Minh ≈ 5/4", 5: "Lập Hạ ≈ 6/5",
              6: "Mang Chủng ≈ 6/6", 7: "Tiểu Thử ≈ 7/7", 8: "Lập Thu ≈ 8/8", 9: "Bạch Lộ ≈ 8/9",
              10: "Hàn Lộ ≈ 8/10", 11: "Lập Đông ≈ 7/11", 0: "Đại Tuyết ≈ 7/12", 1: "Tiểu Hàn ≈ 6/1"}


def xung(a, b):
    """Hai chi lục xung (Tý–Ngọ, Sửu–Mùi, ...)."""
    return (a - b) % 12 == 6


def hop(a, b):
    """Hai chi lục hợp (Tý–Sửu, Dần–Hợi, Mão–Tuất, Thìn–Dậu, Tỵ–Thân, Ngọ–Mùi)."""
    return (a + b) % 12 == 1


def chi_hop(a):
    return (1 - a) % 12


def chi_xung(a):
    return (a + 6) % 12


def giai_doan(hanh, chi):
    """Vị trí trong vòng trường sinh của ngũ hành `hanh` tại chi (0 = Trường sinh ... 8 = Mộ, 9 = Tuyệt)."""
    return (chi - KHOI_TRUONG_SINH[hanh]) % 12


def chi_giai_doan(hanh, k):
    return (KHOI_TRUONG_SINH[hanh] + k) % 12


def ten_luc_than(hanh_cung, hanh_hao):
    """Lục thân của hào so với ngũ hành của cung."""
    if hanh_hao == hanh_cung:
        return "Huynh Đệ"
    if SINH[hanh_hao] == hanh_cung:
        return "Phụ Mẫu"
    if SINH[hanh_cung] == hanh_hao:
        return "Tử Tôn"
    if KHAC[hanh_cung] == hanh_hao:
        return "Thê Tài"
    return "Quan Quỷ"


def hanh_cua_luc_than(hanh_cung, lt):
    return [h for h in SINH if ten_luc_than(hanh_cung, h) == lt][0]


def can_chi(can, chi):
    return "%s %s" % (CAN_VN[can], CHI_VN[chi])


def gz(i):
    """Số thứ tự 0..59 -> (can, chi)."""
    return i % 10, i % 12


def tuan_khong(gz_ngay):
    """Hai chi tuần không theo can chi ngày (0..59)."""
    dau = (gz_ngay - gz_ngay % 10) % 12
    return ((dau + 10) % 12, (dau + 11) % 12)


# ---------------------------------------------------------------- Nạp giáp (sinh bằng quy tắc)
def _chi_khoi(ten):
    """Chi hào 1 của quái: Càn Tý, Khôn Mùi; ba nam (Chấn, Khảm, Cấn) Tý/Dần/Thìn theo vị trí hào dương;
    ba nữ (Tốn, Ly, Đoài) Sửu/Mão/Tỵ theo vị trí hào âm."""
    b = BIT[ten]
    if sum(b) == 3:
        return 0
    if sum(b) == 0:
        return 7
    if sum(b) == 1:
        return 2 * b.index(1)
    return 1 + 2 * b.index(0)


def nap_giap_quai(ten):
    """6 cặp (can, chi) của quái: vị trí 0..2 dùng khi quái ở nội (hào 1-3), 3..5 khi ở ngoại (hào 4-6).
    Dương quái đi thuận cách một chi, âm quái đi nghịch."""
    buoc = 2 if sum(BIT[ten]) in (1, 3) else -2
    c0 = _chi_khoi(ten)
    noi, ngoai = CAN_NAP[ten]
    return [(noi if i < 3 else ngoai, (c0 + buoc * i) % 12) for i in range(6)]


NAP = {t: nap_giap_quai(t) for t in BIT}


def quai_cua(key):
    """key: tuple 6 bit từ hào 1 -> (nội quái, ngoại quái)."""
    return TEN_BIT[tuple(key[0:3])], TEN_BIT[tuple(key[3:6])]


def nap_giap_que(key):
    noi, ngoai = quai_cua(key)
    return [NAP[noi if i < 3 else ngoai][i] for i in range(6)]


def ten_que(key):
    noi, ngoai = quai_cua(key)
    return M.ten_que(SO_QUAI[ngoai], SO_QUAI[noi])


# ---------------------------------------------------------------- Bát cung, thế ứng (sinh bằng thuật toán)
def _sinh_bat_cung():
    """Từ quẻ thuần, biến lần lượt hào 1..5 (nhất thế .. ngũ thế), du hồn (từ ngũ thế đổi lại hào 4),
    quy hồn (nội quái trở về quái của cung)."""
    bang, theo_cung = {}, {}
    for cung in THU_TU_CUNG:
        h = list(BIT[cung]) * 2
        ds = [(tuple(h), 6)]
        for i in range(5):
            h[i] ^= 1
            ds.append((tuple(h), i + 1))
        h[3] ^= 1
        ds.append((tuple(h), 4))
        h[0:3] = BIT[cung]
        ds.append((tuple(h), 3))
        theo_cung[cung] = []
        for loai, (k, the) in enumerate(ds):
            if k in bang:
                raise RuntimeError("trùng quẻ khi sinh bát cung")
            ung = the + 3 if the <= 3 else the - 3
            bang[k] = dict(cung=cung, hanh=HANH_QUAI[cung], the=the, ung=ung, loai=loai)
            theo_cung[cung].append(k)
    return bang, theo_cung


BAT_CUNG, QUE_THEO_CUNG = _sinh_bat_cung()


def luc_xung_que(key):
    """Quẻ lục xung: sáu hào xung nhau từng cặp (1-4, 2-5, 3-6)."""
    c = [x[1] for x in nap_giap_que(key)]
    return all(xung(c[i], c[i + 3]) for i in range(3))


def luc_hop_que(key):
    c = [x[1] for x in nap_giap_que(key)]
    return all(hop(c[i], c[i + 3]) for i in range(3))


# ---------------------------------------------------------------- Vượng suy
def vuong_suy_thang(hanh, chi_thang):
    return M.vuong_suy(hanh, chi_thang)


def _danh_gia_ngay_thang(chi, hanh, chi_thang, chi_ngay, dong):
    """Trạng thái một chi (hào, phục thần) theo nguyệt kiến và nhật thần.
    Trả (danh sách nhãn, cờ, điểm lực thô)."""
    nhan, co, diem = [], {}, 0
    vs = vuong_suy_thang(hanh, chi_thang)
    co["thang"] = vs
    if chi == chi_thang:
        nhan.append("lâm nguyệt kiến")
        diem += 3
        co["lam_nguyet"] = True
    elif xung(chi, chi_thang):
        nhan.append("NGUYỆT PHÁ (bị nguyệt kiến xung, vượng suy theo mùa không còn tác dụng)")
        diem -= 3
        co["nguyet_pha"] = True
    else:
        nhan.append("tháng: " + vs + {"vượng": "", "tướng": " (nguyệt sinh)", "hưu": " (hào sinh tháng)",
                                      "tù": " (hào khắc tháng)", "tử": " (nguyệt khắc)"}[vs])
        diem += {"vượng": 2, "tướng": 1, "hưu": -1, "tù": -1, "tử": -2}[vs]
    if hop(chi, chi_thang):
        nhan.append("nguyệt hợp")
        diem += 1
        co["nguyet_hop"] = True
    vuong_thang = (vs in ("vượng", "tướng") or co.get("nguyet_hop")) and not co.get("nguyet_pha")
    co["vuong_thang"] = bool(vuong_thang)
    hn = HANH_CHI[chi_ngay]
    if chi == chi_ngay:
        nhan.append("lâm nhật thần")
        diem += 2
        co["lam_nhat"] = True
    elif xung(chi, chi_ngay):
        co["nhat_xung"] = True
        if dong and vuong_thang:
            nhan.append("nhật xung hào động (vượng: không hại)")
        elif dong:
            nhan.append("nhật xung hào động suy: XUNG TÁN")
            diem -= 2
            co["xung_tan"] = True
        elif vuong_thang:
            nhan.append("ÁM ĐỘNG (tĩnh, vượng, bị nhật xung)")
            co["am_dong"] = True
        else:
            nhan.append("NHẬT PHÁ (tĩnh, suy, bị nhật xung)")
            diem -= 2
            co["nhat_pha"] = True
    else:
        if hn == hanh:
            nhan.append("nhật phù (cùng hành)")
            diem += 1
        elif SINH[hn] == hanh:
            nhan.append("nhật sinh")
            diem += 2
            co["nhat_sinh"] = True
        elif KHAC[hn] == hanh:
            nhan.append("nhật khắc")
            diem -= 2
            co["nhat_khac"] = True
        if hop(chi, chi_ngay):
            nhan.append("nhật hợp (%s)" % ("động gặp hợp: hợp trú" if dong else "tĩnh gặp hợp: hợp khởi"))
            diem += 1
            co["nhat_hop"] = True
            if dong:
                co["hop_tru"] = True
    k = giai_doan(hanh, chi_ngay)
    if k == 0:
        nhan.append("trường sinh ở nhật")
        diem += 1
    elif k == 8:
        nhan.append("nhập mộ ở nhật")
        diem -= 1
        co["nhat_mo"] = True
    elif k == 9:
        nhan.append("tuyệt ở nhật")
        diem -= 1
        co["nhat_tuyet"] = True
    return nhan, co, diem


def _bien_hao(chi, hanh, b_chi, b_hanh, chi_thang, khong):
    """Quan hệ hào động -> hào biến. Trả (nhãn, cờ, điểm)."""
    nhan, co, diem = [], {}, 0
    if b_chi == chi:
        nhan.append("PHỤC NGÂM (hóa cùng chi)")
        co["phuc_ngam"] = True
        return nhan, co, diem - 1          # biến y nguyên chi: không xét thêm hóa không/phá/mộ/tuyệt
    elif b_hanh == hanh:
        d = (b_chi - chi) % 12
        if hanh == "Thổ":
            tien, thoai = d == 3, d == 9
        else:
            tien, thoai = d == 1, d == 11
        if tien:
            nhan.append("hóa TIẾN thần")
            co["tien"] = True
            diem += 1
        elif thoai:
            nhan.append("hóa THOÁI thần")
            co["thoai"] = True
            diem -= 1
        else:
            nhan.append("hóa tỷ hòa")
    elif SINH[b_hanh] == hanh:
        nhan.append("HỒI ĐẦU SINH")
        co["hoi_dau_sinh"] = True
        diem += 2
    elif KHAC[b_hanh] == hanh:
        nhan.append("HỒI ĐẦU KHẮC")
        co["hoi_dau_khac"] = True
        diem -= 2
    elif SINH[hanh] == b_hanh:
        nhan.append("hóa tiết (sinh ra hào biến)")
        diem -= 1
    else:
        nhan.append("khắc hào biến (hóa ra cái mình khắc)")
    if xung(b_chi, chi):
        nhan.append("hóa xung (PHẢN NGÂM hào)")
        co["phan_ngam"] = True
        diem -= 1
    if hop(b_chi, chi):
        nhan.append("hóa hợp")
        co["hoa_hop"] = True
    if b_chi in khong:
        nhan.append("hóa KHÔNG")
        co["hoa_khong"] = True
    if xung(b_chi, chi_thang):
        nhan.append("hóa PHÁ (biến xung nguyệt)")
        co["hoa_pha"] = True
        diem -= 1
    k = giai_doan(hanh, b_chi)
    if k == 0:
        nhan.append("hóa trường sinh")
        diem += 1
    elif k == 8:
        nhan.append("hóa MỘ")
        co["hoa_mo"] = True
        diem -= 1
    elif k == 9:
        nhan.append("hóa TUYỆT")
        co["hoa_tuyet"] = True
        diem -= 1
    return nhan, co, diem


def muc_luc(diem):
    return "mạnh" if diem >= 2 else ("vừa" if diem >= 0 else "yếu")


# ---------------------------------------------------------------- Lập quẻ đầy đủ
def lap_que(hao, chi_thang, gz_ngay):
    """hao: 6 số 6/7/8/9 từ hào 1 (dưới) lên hào 6; chi_thang: chi nguyệt kiến 0..11 (Tý=0);
    gz_ngay: can chi ngày 0..59 (Giáp Tý = 0). Trả dict mô tả quẻ."""
    if len(hao) != 6 or any(v not in (6, 7, 8, 9) for v in hao):
        raise ValueError("cần đúng 6 số, mỗi số là 6, 7, 8 hoặc 9")
    ban = tuple(1 if v in (7, 9) else 0 for v in hao)
    dong = [v in (6, 9) for v in hao]
    bien = tuple(b ^ 1 if d else b for b, d in zip(ban, dong))
    bc, bb = BAT_CUNG[ban], BAT_CUNG[bien]
    hanh_cung = bc["hanh"]
    can_ngay, chi_ngay = gz(gz_ngay)
    khong = tuan_khong(gz_ngay)
    ng_ban, ng_bien = nap_giap_que(ban), nap_giap_que(bien)
    khoi = KHOI_LUC_THAN[can_ngay]
    hao_ds = []
    for i in range(6):
        can, chi = ng_ban[i]
        hanh = HANH_CHI[chi]
        h = dict(vi=i + 1, can=can, chi=chi, hanh=hanh, lt=ten_luc_than(hanh_cung, hanh), duong=ban[i],
                 dong=dong[i], so=hao[i], than=LUC_THAN_6[(khoi + i) % 6],
                 the=bc["the"] == i + 1, ung=bc["ung"] == i + 1, bien=None, phuc=[])
        nhan, co, diem = _danh_gia_ngay_thang(chi, hanh, chi_thang, chi_ngay, dong[i])
        if dong[i]:
            nhan.insert(0, "ĐỘNG")
            bcan, bchi = ng_bien[i]
            bh = HANH_CHI[bchi]
            n2, c2, d2 = _bien_hao(chi, hanh, bchi, bh, chi_thang, khong)
            h["bien"] = dict(can=bcan, chi=bchi, hanh=bh, lt=ten_luc_than(hanh_cung, bh), nhan=n2, co=c2)
            co.update(c2)
            diem += d2
        if chi in khong:
            co["khong"] = True
            gia = dong[i] or co.get("vuong_thang") or co.get("lam_nhat") or co.get("nhat_sinh") \
                or co.get("nhat_hop") or co.get("am_dong")
            chan = co.get("nguyet_pha") or (not gia)
            co["chan_khong"] = bool(chan)
            if chan and not co.get("nguyet_pha"):
                diem -= 2
            if co.get("nhat_xung"):
                nhan.append("TUẦN KHÔNG, gặp nhật xung (xung không thành thực)")
            elif chan:
                nhan.append("TUẦN KHÔNG (suy/phá: chân không)")
            else:
                nhan.append("TUẦN KHÔNG (động / vượng / được nhật sinh hợp: không giả, đợi xuất không)")
        h.update(nhan=nhan, co=co, diem=diem, luc=muc_luc(diem))
        hao_ds.append(h)
    # Phục thần: lục thân vắng -> hào cùng vị trí trong quẻ thuần của cung
    co_mat = {h["lt"] for h in hao_ds}
    thuan = QUE_THEO_CUNG[bc["cung"]][0]
    ng_thuan = nap_giap_que(thuan)
    phuc_ds = []
    for i, (can, chi) in enumerate(ng_thuan):
        hanh = HANH_CHI[chi]
        lt = ten_luc_than(hanh_cung, hanh)
        if lt in co_mat:
            continue
        phi = hao_ds[i]
        nhan, co, diem = _danh_gia_ngay_thang(chi, hanh, chi_thang, chi_ngay, False)
        if co.pop("am_dong", None):          # phục thần không ám động: vượng gặp nhật xung là xung khởi
            nhan = [("bị nhật xung (vượng: xung khởi, dễ xuất)" if x.startswith("ÁM ĐỘNG") else x) for x in nhan]
        if chi in khong:
            co["khong"] = True
            nhan.append("TUẦN KHÔNG")
        if phi["hanh"] == hanh:
            qh = "phi phục tỷ hòa"
        elif SINH[phi["hanh"]] == hanh:
            qh = "phi sinh phục (được nuôi)"
            diem += 1
        elif KHAC[phi["hanh"]] == hanh:
            qh = "phi khắc phục (bị đè, khó xuất)"
            diem -= 1
        elif KHAC[hanh] == phi["hanh"]:
            qh = "phục khắc phi (có sức xuất)"
        else:
            qh = "phục sinh phi (tiết khí)"
            diem -= 1
        de_xuat = [x for x, ok in (("phi thần tuần không", phi["co"].get("khong")),
                                   ("phi thần nguyệt phá", phi["co"].get("nguyet_pha")),
                                   ("phi thần bị nhật xung", phi["co"].get("nhat_xung"))) if ok]
        p = dict(vi=i + 1, can=can, chi=chi, hanh=hanh, lt=lt, nhan=nhan, co=co, diem=diem,
                 luc=muc_luc(diem), quan_he=qh, de_xuat=de_xuat)
        phi["phuc"].append(p)
        phuc_ds.append(p)
    ho = (ban[1], ban[2], ban[3], ban[2], ban[3], ban[4])
    q = dict(hao_so=list(hao), ban=ban, bien=bien, dong_vi=[i + 1 for i in range(6) if dong[i]],
             cung=bc["cung"], hanh_cung=hanh_cung, the=bc["the"], ung=bc["ung"], loai=bc["loai"],
             ten=ten_que(ban), ten_bien=ten_que(bien), ten_ho=ten_que(ho), ho=ho,
             cung_bien=bb["cung"], loai_bien=bb["loai"],
             luc_xung=luc_xung_que(ban), luc_hop=luc_hop_que(ban),
             bien_luc_xung=luc_xung_que(bien), bien_luc_hop=luc_hop_que(bien),
             chi_thang=chi_thang, gz_ngay=gz_ngay, can_ngay=can_ngay, chi_ngay=chi_ngay, khong=khong,
             hao=hao_ds, phuc=phuc_ds)
    q["dac_diem"] = _dac_diem_que(q)
    return q


PHUONG_DOI = {frozenset(("Càn", "Tốn")), frozenset(("Khảm", "Ly")), frozenset(("Cấn", "Khôn")),
              frozenset(("Chấn", "Đoài"))}


def _dac_diem_que(q):
    """Đặc điểm cấp quẻ: lục xung/lục hợp, du hồn/quy hồn, phản ngâm/phục ngâm nội/ngoại quái."""
    ds = []
    if q["luc_xung"]:
        ds.append("Quẻ LỤC XUNG (việc dễ tan, gấp, không bền; quẻ lục xung gặp hợp thì có khi lại thành)")
    if q["luc_hop"]:
        ds.append("Quẻ LỤC HỢP (việc dễ hợp, kéo dài; hợp gặp xung thì tan)")
    if q["dong_vi"]:
        if q["luc_xung"] and q["bien_luc_hop"]:
            ds.append("Lục xung biến lục hợp: trước tan sau hợp")
        if q["luc_hop"] and q["bien_luc_xung"]:
            ds.append("Lục hợp biến lục xung: trước hợp sau tan")
        if not q["luc_xung"] and q["bien_luc_xung"]:
            ds.append("Quẻ biến là quẻ lục xung")
        if not q["luc_hop"] and q["bien_luc_hop"]:
            ds.append("Quẻ biến là quẻ lục hợp")
    else:
        ds.append("Quẻ TĨNH (không hào động): xem dụng thần vượng suy, nhật nguyệt, ám động")
    if q["loai"] == 6:
        ds.append("Quẻ du hồn (tâm không yên, hay đi lại, dời đổi)")
    if q["loai"] == 7:
        ds.append("Quẻ quy hồn (quay về, khó đi xa, việc trở lại chỗ cũ)")
    for ten, sl in (("nội quái", slice(0, 3)), ("ngoại quái", slice(3, 6))):
        a, b = TEN_BIT[q["ban"][sl]], TEN_BIT[q["bien"][sl]]
        if a == b:
            continue
        ca = [h["chi"] for h in q["hao"][sl]]
        cb = [x[1] for x in nap_giap_que(q["bien"])[sl]]
        if ca == cb:
            ds.append("PHỤC NGÂM %s (%s biến %s, chi y nguyên): rên rỉ, trì trệ, muốn đi không được" % (ten, a, b))
        elif all(xung(x, y) for x, y in zip(ca, cb)):
            ds.append("PHẢN NGÂM %s (%s biến %s, các chi xung nhau): việc lặp đi lặp lại, được rồi mất" % (
                ten, a, b))
        elif frozenset((a, b)) in PHUONG_DOI:
            ds.append("Phản ngâm theo phương vị ở %s (%s – %s đối nhau trên Hậu thiên; chỉ một số sách xét, "
                      "các chi không xung nên nhẹ)" % (ten, a, b))
    return ds


# ---------------------------------------------------------------- Dụng thần
VIEC = {
    "chung": ("Việc chung / tự hỏi", [("Dụng thần: bản thân", "Thế"), ("Người / việc phía kia", "Ứng")],
              "Hỏi việc cụ thể thì chọn lại dụng thần theo việc (--viec hoặc --dung)."),
    "taichinh": ("Tiền bạc, làm ăn, mua bán", [("Dụng thần: tiền, hàng, lợi nhuận", "Thê Tài"),
                                               ("Bản thân", "Thế")],
                 "Tử Tôn là nguồn sinh tài; Huynh Đệ là cạnh tranh, hao tài."),
    "congviec": ("Công việc, chức vụ, xin việc, cơ quan", [("Dụng thần: công việc, chức vụ, cấp trên", "Quan Quỷ"),
                                                         ("Giấy tờ, hợp đồng, quyết định", "Phụ Mẫu"),
                                                         ("Bản thân", "Thế")],
                 "Hỏi buôn bán, lời lãi thì dùng taichinh (Thê Tài)."),
    "honnhan": ("Hôn nhân, tình cảm", None, "Nam xem Thê Tài, nữ xem Quan Quỷ; Thế là mình, Ứng là đối phương."),
    "suckhoe": ("Sức khỏe, bệnh tật", [("Dụng thần: người bệnh (tự hỏi)", "Thế"), ("Bệnh", "Quan Quỷ"),
                                      ("Thuốc, thầy thuốc", "Tử Tôn")],
                "Hỏi cho người khác thì đổi dụng thần: cha mẹ Phụ Mẫu, con Tử Tôn, vợ Thê Tài, chồng Quan Quỷ, "
                "anh em Huynh Đệ (--dung). Quan Quỷ (bệnh) nên suy, Tử Tôn (thuốc) nên vượng."),
    "kientung": ("Kiện tụng, tranh chấp", [("Dụng thần: mình", "Thế"), ("Đối phương", "Ứng"),
                                           ("Quan tòa, cơ quan xử", "Quan Quỷ"), ("Đơn từ, hồ sơ", "Phụ Mẫu")],
                 "Thế vượng hơn Ứng là lợi cho mình; Tử Tôn động thì dễ hòa giải."),
    "dixa": ("Đi xa, xuất hành", [("Dụng thần: người đi (tự hỏi)", "Thế"), ("Xe, tàu, giấy tờ đi đường", "Phụ Mẫu"),
                                  ("Bình an", "Tử Tôn"), ("Trở ngại, tai nạn", "Quan Quỷ")],
             "Hỏi cho người khác đi thì đổi dụng thần theo quan hệ (--dung)."),
    "timdo": ("Tìm đồ mất", [("Dụng thần: đồ vật, của cải", "Thê Tài"), ("Kẻ lấy", "Quan Quỷ")],
              "Đồ là giấy tờ, xe cộ thì xem Phụ Mẫu (--dung phumau); người hay vật nuôi đi lạc tùy quan hệ."),
    "thicu": ("Thi cử, học hành", [("Dụng thần: bài thi, văn bằng", "Phụ Mẫu"), ("Đỗ đạt, danh", "Quan Quỷ"),
                                   ("Bản thân", "Thế")],
              "Tử Tôn động khắc Quan Quỷ là điều kỵ khi cầu danh."),
    "giayto": ("Nhà cửa, xe, giấy tờ, hợp đồng, tin tức", [("Dụng thần", "Phụ Mẫu")], ""),
    "concai": ("Con cái, cầu con", [("Dụng thần", "Tử Tôn")], ""),
    "anhem": ("Anh em, bạn bè, đồng nghiệp ngang hàng", [("Dụng thần", "Huynh Đệ")], ""),
}


def _vai_honnhan(gioi):
    if gioi == "nu":
        return [("Dụng thần: chồng / người yêu (nữ hỏi)", "Quan Quỷ"), ("Bản thân", "Thế"), ("Đối phương", "Ứng")]
    return [("Dụng thần: vợ / người yêu (nam hỏi)", "Thê Tài"), ("Bản thân", "Thế"), ("Đối phương", "Ứng")]


def chon_hao(q, muc):
    """Hào ứng với `muc` (lục thân, "Thế" hoặc "Ứng"). Trả (danh sách hào, hào chọn, ghi chú, là phục thần?)."""
    if muc == "Thế":
        h = q["hao"][q["the"] - 1]
        return [h], h, "hào Thế", False
    if muc == "Ứng":
        h = q["hao"][q["ung"] - 1]
        return [h], h, "hào Ứng", False
    ds = [h for h in q["hao"] if h["lt"] == muc]
    if not ds:
        pd = [p for p in q["phuc"] if p["lt"] == muc]
        if pd:
            return pd, pd[0], "không hiện trong quẻ, lấy PHỤC THẦN", True
        return [], None, "không có", False

    def tieu_chi(h):
        c = h["co"]
        return dict(vuong=bool(c.get("vuong_thang") or c.get("lam_nhat")),
                    dong=bool(h["dong"] or c.get("am_dong")),
                    khong_pha=not c.get("nguyet_pha"),
                    khong_khong=not c.get("khong"),
                    khong_thuong=not any(c.get(k) for k in ("nhat_khac", "nhat_pha", "xung_tan", "hoi_dau_khac")))
    if len(ds) == 1:
        return ds, ds[0], "một hào", False
    # Tăng San Bốc Dịch, Lưỡng hiện chương 32: "舍其休囚而用旺相；舍其静爻而用动爻；舍其月破而用不破；
    # 舍其旬空而用不空；舍其被伤而用不伤" (cổ pháp). Năm tiêu chí ngang nhau; hòa thì động > trì thế/ứng > lực.
    def khoa(h):
        t = tieu_chi(h)
        return (-sum(t.values()), -t["dong"], -(h["the"] or h["ung"]), -h["diem"], h["vi"])
    ds2 = sorted(ds, key=khoa)
    ghi = ("%d hào cùng loại; chọn theo cổ pháp Tăng San Bốc Dịch: bỏ hưu tù lấy vượng tướng, bỏ tĩnh lấy động, "
           "bỏ nguyệt phá, bỏ tuần không, bỏ hào bị thương (hòa thì động > trì thế/ứng > lực)" % len(ds))
    kp = [x for x in ds if x["co"].get("khong") or x["co"].get("nguyet_pha")]
    if kp:
        ghi += ("; lưu ý Dã Hạc: ứng kỳ hay rơi vào hào %s nên xem cả thời điểm hào đó xuất không / thực phá"
                % ", ".join("%d %s (%s)" % (x["vi"], CHI_VN[x["chi"]],
                                           "tuần không" if x["co"].get("khong") else "nguyệt phá") for x in kp))
    return ds, ds2[0], ghi, False


def tam_than(hanh_cung, lt):
    """Nguyên thần (sinh dụng), kỵ thần (khắc dụng), cừu thần (sinh kỵ), tiết thần (dụng sinh ra)."""
    hd = hanh_cua_luc_than(hanh_cung, lt)
    nguyen = [h for h in SINH if SINH[h] == hd][0]
    ky = [h for h in KHAC if KHAC[h] == hd][0]
    cuu = [h for h in SINH if SINH[h] == ky][0]
    tiet = SINH[hd]
    return [("Dụng thần", lt, hd), ("Nguyên thần (sinh dụng)", ten_luc_than(hanh_cung, nguyen), nguyen),
            ("Kỵ thần (khắc dụng)", ten_luc_than(hanh_cung, ky), ky),
            ("Cừu thần (sinh kỵ, khắc nguyên)", ten_luc_than(hanh_cung, cuu), cuu),
            ("Tiết thần (dụng sinh ra)", ten_luc_than(hanh_cung, tiet), tiet)]


# ---------------------------------------------------------------- In
def ky_hieu(h):
    if h["duong"]:
        return "——— O" if h["dong"] else "———"
    return "— — X" if h["dong"] else "— —"


def _mo_ta_hao(h):
    return "%s %s %s" % (h["lt"], can_chi(h["can"], h["chi"]), h["hanh"])


def _ngay_toi(ngay0, chi_ngay, chi):
    k = (chi - chi_ngay) % 12 or 12
    d = ngay0 + dt.timedelta(days=k)
    return "%s (%s)" % (d.strftime("%d/%m"), "sau %d ngày" % k)


def ung_ky(q, h, la_phuc, ngay0=None):
    """Gợi ý ứng kỳ cho hào dụng thần h. Trả list (tình trạng, gợi ý, chi gợi ý)."""
    ds = []
    c = h["chi"]
    co = h["co"]

    def ngay(chi):
        return "ngày/tháng %s%s" % (CHI_VN[chi], (", ngày gần nhất " + _ngay_toi(ngay0, q["chi_ngay"], chi))
                                    if ngay0 else "")
    if la_phuc:
        phi = q["hao"][h["vi"] - 1]
        ds.append(("Dụng thần phục dưới hào %d (%s)" % (h["vi"], CHI_VN[phi["chi"]]),
                   "phục thần đợi ngày trị (gặp chính chi) hoặc ngày xung phi thần (xung khai)",
                   "%s; xung phi: %s" % (ngay(c), ngay(chi_xung(phi["chi"])))))
    elif h["dong"]:
        ds.append(("Hào động", "động thì đợi hợp hoặc đợi trị", "hợp: %s; trị: %s" % (ngay(chi_hop(c)), ngay(c))))
    elif co.get("am_dong"):
        ds.append(("Ám động", "ám động coi như động: đợi hợp hoặc trị", "hợp: %s; trị: %s" % (
            ngay(chi_hop(c)), ngay(c))))
    else:
        ds.append(("Hào tĩnh", "tĩnh thì đợi xung (xung khởi) hoặc trị", "xung: %s; trị: %s" % (
            ngay(chi_xung(c)), ngay(c))))
    if co.get("khong"):
        ds.append(("Tuần không", "đợi xuất không / điền thực (gặp chính chi sau tuần này) hoặc ngày xung",
                   "%s; xung: %s" % (ngay(c), ngay(chi_xung(c)))))
    if co.get("nguyet_pha"):
        ds.append(("Nguyệt phá", "đợi qua tháng (xuất nguyệt), hoặc thực phá (gặp chính chi), hoặc ngày hợp",
                   "trị: %s; hợp: %s; tháng sau: từ tiết %s" % (
                       ngay(c), ngay(chi_hop(c)), TIET_THANG[(q["chi_thang"] + 1) % 12])))
    if co.get("nhat_pha"):
        ds.append(("Nhật phá", "đợi ngày trị hoặc ngày hợp", "trị: %s; hợp: %s" % (ngay(c), ngay(chi_hop(c)))))
    if co.get("hop_tru") or co.get("hoa_hop"):
        ds.append(("Bị hợp trú / hóa hợp", "hợp thì đợi xung (xung khai)", ngay(chi_xung(c))))
    if co.get("nhat_mo") or co.get("hoa_mo"):
        mo = chi_giai_doan(h["hanh"], 8)
        ds.append(("Nhập mộ", "đợi ngày xung mộ (xung khai mộ khố)", "%s (xung %s)" % (
            ngay(chi_xung(mo)), CHI_VN[mo])))
    if co.get("hoa_khong"):
        b = h["bien"]["chi"]
        ds.append(("Hóa không", "hào biến xuất không thì việc mới thành / mới hiện", ngay(b)))
    if co.get("tien"):
        ds.append(("Hóa tiến thần", "việc tiến dần; ứng khi hào biến được trị hoặc vượng", ngay(h["bien"]["chi"])))
    if co.get("thoai"):
        ds.append(("Hóa thoái thần", "việc lui dần; nếu đang vượng thì lúc vượng còn dùng được, gặp suy thì lui", ""))
    if h["diem"] >= 5:
        mo = chi_giai_doan(h["hanh"], 8)
        ds.append(("Thái vượng", "quá vượng có khi ứng vào ngày mộ hoặc ngày bị khắc, tiết", ngay(mo)))
    elif h["diem"] < 0 and not co.get("khong") and not co.get("nguyet_pha"):
        sinh = chi_giai_doan(h["hanh"], 0)
        vuong = chi_giai_doan(h["hanh"], 4)
        ds.append(("Suy yếu", "suy thì đợi ngày/tháng sinh vượng (được sinh, trường sinh, đế vượng)",
                   "sinh: %s; vượng: %s" % (ngay(sinh), ngay(vuong))))
    return ds


def in_que(q, viec="chung", gioi=None, dung=None, ngay0=None, nguon=None, thong_tin=None):
    """In bảng quẻ (Markdown, tiếng Việt)."""
    print("LỤC HÀO NẠP GIÁP")
    print("| Mục | Giá trị |")
    print("|---|---|")
    for k, v in (thong_tin or []):
        print("| %s | %s |" % (k, v))
    kc, kz = gz(q["gz_ngay"])
    print("| Nguyệt kiến / Nhật thần | tháng %s (%s) / ngày %s (%s) |" % (
        CHI_VN[q["chi_thang"]], HANH_CHI[q["chi_thang"]], can_chi(kc, kz), HANH_CHI[kz]))
    print("| Tuần không (theo ngày) | %s, %s |" % (CHI_VN[q["khong"][0]], CHI_VN[q["khong"][1]]))
    if nguon:
        print("| Cách lập quẻ | %s |" % nguon)
    print("| Số hào (1 → 6) | %s; hào động: %s |" % (" ".join(map(str, q["hao_so"])),
                                                    ", ".join(map(str, q["dong_vi"])) or "không"))
    print()
    print("| Quẻ | Tên | Cung (hành) | Thế loại | Thế / Ứng | Lục xung / hợp |")
    print("|---|---|---|---|---|---|")
    xh = "lục xung" if q["luc_xung"] else ("lục hợp" if q["luc_hop"] else "—")
    print("| Chủ | %s | %s (%s) | %s | hào %d / hào %d | %s |" % (
        q["ten"], q["cung"], q["hanh_cung"], THE_LOAI[q["loai"]], q["the"], q["ung"], xh))
    if q["dong_vi"]:
        bb = BAT_CUNG[q["bien"]]
        xh2 = "lục xung" if q["bien_luc_xung"] else ("lục hợp" if q["bien_luc_hop"] else "—")
        print("| Biến | %s | %s (%s) | %s | hào %d / hào %d | %s |" % (
            q["ten_bien"], bb["cung"], bb["hanh"], THE_LOAI[bb["loai"]], bb["the"], bb["ung"], xh2))
    bh = BAT_CUNG[q["ho"]]
    print("| Hỗ | %s | %s (%s) | %s | — | — |" % (q["ten_ho"], bh["cung"], bh["hanh"], THE_LOAI[bh["loai"]]))
    print()
    for x in q["dac_diem"]:
        print("- " + x)
    print()
    print("| Hào | Lục thần | Phục thần | Bản quái | Thế/Ứng | Hào | Biến | Trạng thái |")
    print("|---|---|---|---|---|---|---|---|")
    for h in reversed(q["hao"]):
        phuc = "; ".join("%s %s %s" % (p["lt"], can_chi(p["can"], p["chi"]), p["hanh"]) for p in h["phuc"])
        tu = "Thế" if h["the"] else ("Ứng" if h["ung"] else "")
        b = h["bien"]
        bien = "%s %s %s" % (b["lt"], can_chi(b["can"], b["chi"]), b["hanh"]) if b else ""
        tt = list(h["nhan"]) + (b["nhan"] if b else [])
        print("| %d | %s | %s | %s | %s | %s | %s | %s |" % (
            h["vi"], h["than"], phuc, _mo_ta_hao(h), tu, ky_hieu(h), bien, "; ".join(tt)))
    print()
    if q["phuc"]:
        print("Phục thần (lục thân vắng trong quẻ, lấy từ quẻ thuần %s):" % ten_que(QUE_THEO_CUNG[q["cung"]][0]))
        print("| Phục thần | Dưới hào (phi thần) | Trạng thái | Phi – phục | Dễ xuất do |")
        print("|---|---|---|---|---|")
        for p in q["phuc"]:
            phi = q["hao"][p["vi"] - 1]
            print("| %s %s %s | hào %d %s | %s; lực %s | %s | %s |" % (
                p["lt"], can_chi(p["can"], p["chi"]), p["hanh"], p["vi"], _mo_ta_hao(phi),
                "; ".join(p["nhan"]), p["luc"], p["quan_he"], ", ".join(p["de_xuat"]) or "—"))
        print()
    # dụng thần
    canh_bao = []
    if dung:
        muc = "Thế" if dung == "the" else ("Ứng" if dung == "ung" else LUC_THAN_KHOA[dung])
        ten_viec, vai = "chọn tay (--dung)", [("Dụng thần", muc)]
        ghi_viec = ""
    else:
        ten_viec, vai, ghi_viec = VIEC[viec]
        if viec == "honnhan":
            if gioi not in ("nam", "nu"):
                canh_bao.append("Hỏi hôn nhân mà chưa có --gioi: tạm xem theo nam hỏi (Thê Tài). "
                                "Nữ hỏi thì dụng thần là Quan Quỷ.")
            vai = _vai_honnhan(gioi)
    print("DỤNG THẦN – việc: %s" % ten_viec)
    for c in canh_bao:
        print("! " + c)
    print("| Vai | Lục thân | Hào trong quẻ | Lực (ước lượng) |")
    print("|---|---|---|---|")
    chinh = None
    for idx, (nhan, muc) in enumerate(vai):
        ds, h, ghi, la_phuc = chon_hao(q, muc)
        if idx == 0:
            chinh = (muc, ds, h, ghi, la_phuc)
        if h is None:
            print("| %s | %s | không có trong quẻ và quẻ thuần | — |" % (nhan, muc))
            continue
        lt = h["lt"]
        mo = []
        for x in ds:
            s = "hào %d %s%s%s%s" % (x["vi"], can_chi(x["can"], x["chi"]),
                                     " (phục dưới hào %d)" % x["vi"] if la_phuc else "",
                                     " động" if x.get("dong") else "",
                                     " ← chọn" if (x is h and len(ds) > 1) else "")
            mo.append(s)
        print("| %s | %s | %s | %s |" % (nhan, lt if muc in ("Thế", "Ứng") else muc, "; ".join(mo), h["luc"]))
    print()
    if ghi_viec:
        print("- Ghi chú: " + ghi_viec)
    muc, ds, h, ghi, la_phuc = chinh
    if h is None:
        print("! Không tìm thấy dụng thần.")
        return
    lt = h["lt"]
    print("- Hào dụng thần: hào %d %s %s (%s)%s – %s." % (
        h["vi"], lt, can_chi(h["can"], h["chi"]), h["hanh"], " PHỤC THẦN" if la_phuc else "", ghi))
    print("- Trạng thái dụng thần: %s; lực ước lượng: %s." % ("; ".join(h["nhan"] + (
        h["bien"]["nhan"] if h.get("bien") else [])), h["luc"]))
    print()
    print("| Vai | Lục thân | Hành | Hào trong quẻ (động/tĩnh, lực) |")
    print("|---|---|---|---|")
    for vai_t, lt2, hanh in tam_than(q["hanh_cung"], lt):
        hs = [x for x in q["hao"] if x["lt"] == lt2]
        s = "; ".join("hào %d %s %s, %s" % (x["vi"], CHI_VN[x["chi"]], "ĐỘNG" if x["dong"] else (
            "ám động" if x["co"].get("am_dong") else "tĩnh"), x["luc"]) for x in hs)
        if not hs:
            s = "; ".join("phục dưới hào %d (%s)" % (p["vi"], CHI_VN[p["chi"]]) for p in q["phuc"] if p["lt"] == lt2) \
                or "không có"
        print("| %s | %s | %s | %s |" % (vai_t, lt2, hanh, s))
    print()
    print("ỨNG KỲ GỢI Ý (chỉ để tham khảo, không phải lời phán):")
    print("| Tình trạng dụng thần | Quy tắc | Thời điểm gợi ý |")
    print("|---|---|---|")
    for a, b, c in ung_ky(q, h, la_phuc, ngay0):
        print("| %s | %s | %s |" % (a, b, c or "—"))
    print()
    print("(Đọc quẻ: xem dụng thần trước – vượng hay suy theo tháng, ngày; có bị không, phá, mộ, tuyệt; "
          "rồi xem nguyên thần có động sinh không, kỵ thần có động khắc không. Hào động mạnh hơn hào tĩnh; "
          "nhật nguyệt mạnh hơn hào động. Thế là mình, Ứng là phía kia.)")
    print()


# ---------------------------------------------------------------- Đầu vào: hào, đồng xu, thời gian, số
def doc_hao(chuoi):
    s = re.sub(r"[\s,;/\-]", "", "".join(chuoi))
    if not re.fullmatch(r"[6789]{6}", s):
        raise SystemExit("LỖI: --hao cần đúng 6 số (6/7/8/9) từ hào 1 (dưới) lên hào 6, ví dụ --hao 7 8 8 6 9 8.")
    return [int(c) for c in s]


def doc_xu(chuoi, dao=False):
    """6 nhóm 3 đồng xu, S = sấp, N = ngửa (mặt chữ). Mặc định ngửa = 3, sấp = 2 (đảo nếu dao=True)."""
    s = re.sub(r"[\s,;/\-]", "", "".join(chuoi)).upper()
    if not re.fullmatch(r"[SN]{18}", s):
        raise SystemExit("LỖI: --xu cần 6 nhóm, mỗi nhóm 3 chữ S (sấp) / N (ngửa), từ lần gieo 1 (hào 1) đến "
                         "lần 6, ví dụ --xu SSN NNS SSS NSN NNN SNS.")
    diem = {"N": 2, "S": 3} if dao else {"N": 3, "S": 2}
    nhom = [s[i:i + 3] for i in range(0, 18, 3)]
    return [sum(diem[c] for c in g) for g in nhom], nhom


def tu_mai_hoa(q):
    """Đổi quẻ Mai hoa (thượng, hạ, hào động) sang 6 số hào."""
    th, ha = q["chu"]
    h = M.hao6(th, ha)
    v = [7 if b else 8 for b in h]
    i = q["dong"] - 1
    v[i] = 9 if h[i] else 6
    return v


def thoi_diem_que(tt):
    """Can chi năm/tháng (theo tiết khí, giờ tuyệt đối) và ngày/giờ (giờ địa phương, mặc định mặt trời thực)."""
    import tvbt as B
    ebk = B.lunar_cua(tt.t_bk).getEightChar()
    eloc = B.lunar_cua(tt.t_dia_phuong).getEightChar()
    eloc.setSect(tt.sect)
    d = dict(nam=ebk.getYear(), thang=ebk.getMonth(), ngay=eloc.getDay(), gio=eloc.getTime())
    d["chi_thang"] = B.ZHI_LIST.index(d["thang"][1])
    d["gz_ngay"] = B._gz_so(d["ngay"])
    t = tt.t_dia_phuong
    d["ngay_duong"] = t.date() + (dt.timedelta(days=1) if (t.hour == 23 and tt.sect == 1) else dt.timedelta(0))
    canh = []
    for lech in (-3, 3):
        e2 = B.lunar_cua(tt.t_bk + dt.timedelta(hours=lech)).getEightChar()
        if e2.getMonth() != d["thang"]:
            canh.append("Thời điểm gieo quẻ cách giờ giao tiết dưới 3 tiếng: nguyệt kiến có thể là tháng %s. "
                        "Nên ghi chú khi luận." % B.vn(e2.getMonth()))
            break
    d["canh_bao"] = canh
    return d


def hao_nhap(a):
    """Đọc --hao / --xu (không cần thời điểm) và kiểm --so. Trả (6 số hào, mô tả) hoặc None."""
    so_cach = sum(bool(getattr(a, k, None)) for k in ("hao", "xu", "so"))
    if so_cach > 1:
        raise SystemExit("LỖI: chỉ dùng một cách lập quẻ: --hao, --xu hoặc --so (bỏ trống cả ba = theo thời gian).")
    if getattr(a, "hao", None):
        return doc_hao(a.hao), "nhập số hào trực tiếp"
    if getattr(a, "xu", None):
        dao = bool(getattr(a, "xu_dao", False))
        v, nhom = doc_xu(a.xu, dao)
        qu = "sấp = 3, ngửa = 2 (đảo)" if dao else "ngửa (mặt chữ) = 3, sấp = 2"
        lao = ("3 sấp → 9 lão dương động, 3 ngửa → 6 lão âm động" if dao else
               "3 ngửa → 9 lão dương động, 3 sấp → 6 lão âm động")
        return v, "gieo 3 đồng xu, quy ước %s (%s): %s" % (
            qu, lao, ", ".join("hào %d %s = %d" % (i + 1, g, x) for i, (g, x) in enumerate(zip(nhom, v))))
    so = getattr(a, "so", None)
    if so and len(so) not in (2, 3):
        raise SystemExit("LỖI: --so cần 2 số (thượng, hạ; hào động = tổng + số giờ) hoặc thêm số 0 thứ ba để "
                         "không cộng giờ.")
    return None


def lap_theo_thoi_gian(a, tt):
    """Lập quẻ như Mai hoa (theo số --so hoặc theo năm/tháng/ngày âm + giờ). Trả (6 số hào, mô tả)."""
    import tvbt as B
    t = tt.t_dia_phuong
    ngay = t.date() + (dt.timedelta(days=1) if t.hour == 23 else dt.timedelta(0))
    d, m, y, _ = B.duong_sang_am(ngay, tt.lich_tz)
    gio = B.chi_gio(t)
    so = getattr(a, "so", None)
    if so:
        qm, tong = M.theo_so(so[0], so[1], gio if len(so) < 3 else None)
        mo_ta = "theo số %d và %d (Mai hoa)%s, tổng %d → hào động %d" % (
            so[0], so[1], ", cộng số giờ %s" % CHI_VN[gio] if len(so) < 3 else "", tong, qm["dong"])
    else:
        qm, (s1, s2) = M.theo_thoi_gian((y - 4) % 12, m, d, gio)
        mo_ta = ("theo thời gian (Mai hoa): năm %s (%d) + tháng %d + ngày %d = %d → thượng; + giờ %s (%d) = %d "
                 "→ hạ, hào động %d" % (CHI_VN[(y - 4) % 12], (y - 4) % 12 + 1, m, d, s1, CHI_VN[gio], gio + 1, s2,
                                       qm["dong"]))
    return tu_mai_hoa(qm), mo_ta


# ---------------------------------------------------------------- CLI
def them_lenh(sub):
    import nc
    p = sub.add_parser("luchao", help="Lục hào nạp giáp: lập quẻ (số hào / đồng xu / thời gian / số), "
                                      "thế ứng, lục thân, lục thần, phục thần, nhật nguyệt, dụng thần, ứng kỳ")
    nc.them_tham_so_sinh(p)
    p.add_argument("--hao", nargs="+", help="6 số từ hào 1 (dưới) lên hào 6: 6 lão âm (động), 7 thiếu dương, "
                                            "8 thiếu âm, 9 lão dương (động); vd --hao 7 8 8 6 9 8")
    p.add_argument("--xu", nargs="+", help="6 nhóm gieo 3 đồng xu từ lần 1 (hào 1): S = sấp, N = ngửa (mặt chữ); "
                                           "ngửa = 3, sấp = 2; vd --xu SSN NNS SSS NSN NNN SNS")
    p.add_argument("--xu-dao", action="store_true", help="đảo quy ước đồng xu: sấp = 3, ngửa = 2")
    p.add_argument("--so", type=int, nargs="+", help="lập theo số như Mai hoa: 2 số (thượng, hạ; hào động cộng "
                                                     "số giờ) hoặc thêm số 0 thứ ba để không cộng giờ")
    p.add_argument("--viec", default="chung", choices=list(VIEC), help="việc hỏi để gợi ý dụng thần")
    p.add_argument("--dung", choices=["the", "ung"] + list(LUC_THAN_KHOA),
                   help="chọn tay dụng thần (ghi đè --viec): the, ung, phumau, huynhde, tuton, thetai, quanquy")
    p.set_defaults(_chay=chay)
    return p


def chay(a):
    import nc
    import tvbt as B
    nhap = hao_nhap(a)
    khong_gio = False
    if a.ngay and not a.gio and nhap:
        a.gio, khong_gio = "12:00", True
    tt = nc.thoi_diem(a, can_gio=True)
    B.in_dau_thoi_diem(tt, "GIEO QUẺ")
    if khong_gio:
        print("! Không có giờ gieo quẻ: tạm lấy 12:00 (chỉ ảnh hưởng trụ giờ; gieo sau 23h thì ngày đã sang "
              "hôm sau – hãy nhập --gio).")
    td = thoi_diem_que(tt)
    for c in td["canh_bao"]:
        print("! " + c)
    hao, mo_ta = nhap or lap_theo_thoi_gian(a, tt)
    q = lap_que(hao, td["chi_thang"], td["gz_ngay"])
    tin = [("Can chi", "năm %s, tháng %s, ngày %s, giờ %s" % (B.vn(td["nam"]), B.vn(td["thang"]), B.vn(td["ngay"]),
                                                              "không rõ" if khong_gio else B.vn(td["gio"])))]
    in_que(q, a.viec, getattr(tt, "gioi_that", a.gioi), a.dung, td["ngay_duong"], mo_ta, tin)


# ---------------------------------------------------------------- Tự kiểm
# Bảng nạp giáp chuẩn (Kinh Phòng; Hỏa Châu Lâm; Bốc Phệ Chính Tông; Tăng San Bốc Dịch) – chỉ dùng để đối chiếu
_NAP_CHUAN = {"Càn": "甲子寅辰壬午申戌", "Khảm": "戊寅辰午戊申戌子", "Cấn": "丙辰午申丙戌子寅",
              "Chấn": "庚子寅辰庚午申戌", "Tốn": "辛丑亥酉辛未巳卯", "Ly": "己卯丑亥己酉未巳",
              "Khôn": "乙未巳卯癸丑亥酉", "Đoài": "丁巳卯丑丁亥酉未"}
_GAN, _ZHI = "甲乙丙丁戊己庚辛壬癸", "子丑寅卯辰巳午未申酉戌亥"
_LUC_XUNG = {"Thuần Càn", "Thuần Khảm", "Thuần Cấn", "Thuần Chấn", "Thuần Tốn", "Thuần Ly", "Thuần Khôn",
             "Thuần Đoài", "Thiên Lôi Vô Vọng", "Lôi Thiên Đại Tráng"}
_LUC_HOP = {"Thiên Địa Bĩ", "Địa Thiên Thái", "Địa Lôi Phục", "Lôi Địa Dự", "Thủy Trạch Tiết", "Trạch Thủy Khốn",
            "Hỏa Sơn Lữ", "Sơn Hỏa Bí"}
# Tiến thần (đề bài; Tăng San Bốc Dịch – Tiến thần thoái thần chương)
_TIEN = ["亥子", "寅卯", "巳午", "申酉", "丑辰", "辰未", "未戌", "戌丑"]

# Bảng Lục thần chương của Tăng San Bốc Dịch (bản simplelits.com, quyển 1): cột Giáp Ất, Bính Đinh, Mậu, Kỷ,
# Canh Tân, Nhâm Quý; hàng từ hào 6 xuống hào 1 (Nguyên Vũ = Huyền Vũ).
_BANG_LUC_THAN = ["元武青龙朱雀勾陈滕蛇白虎", "白虎元武青龙朱雀勾陈滕蛇", "滕蛇白虎元武青龙朱雀勾陈",
                  "勾陈滕蛇白虎元武青龙朱雀", "朱雀勾陈滕蛇白虎元武青龙", "青龙朱雀勾陈滕蛇白虎元武"]
_TEN_THAN = {"青龙": "Thanh Long", "朱雀": "Chu Tước", "勾陈": "Câu Trần", "滕蛇": "Đằng Xà", "白虎": "Bạch Hổ",
             "元武": "Huyền Vũ"}
_LT_HAN = {"父": "Phụ Mẫu", "兄": "Huynh Đệ", "子": "Tử Tôn", "财": "Thê Tài", "官": "Quan Quỷ"}

# Quẻ mẫu. Mỗi mẫu: nguồn, 6 số hào, chi tháng, can chi ngày, kỳ vọng.
# "hao": từ hào 6 xuống hào 1: "lục thân-chi" (chữ đầu lục thân Hán + chi), thế/ứng ghi "S"/"U".
# Nguồn Tăng San Bốc Dịch: bản điện tử simplelits.com (classical-08508), đối chiếu ngày 31/10/2026.
_MAU = [
    dict(nguon="Tăng San Bốc Dịch q.1: tháng Thân ngày Giáp Thìn xem bệnh anh, được Truân biến Chấn",
         hao=[7, 8, 8, 6, 9, 8], thang="申", ngay="甲辰", ten="Thủy Lôi Truân", bien="Thuần Chấn", cung="Khảm",
         the=2, ung=5, khong="寅卯",
         lt=["兄子", "官戌", "父申", "官辰", "子寅", "兄子"], bl={5: "父申", 4: "财午"},
         # Lục thần theo bảng Lục thần chương (sách in ví dụ này đảo Câu Trần / Đằng Xà ở hào 3–4)
         than=["元武", "白虎", "滕蛇", "勾陈", "朱雀", "青龙"], phuc={3: "财午"}),
    dict(nguon="Tăng San Bốc Dịch q.1: ngày Mậu Tý xem sinh nở, được Bác biến Quan",
         hao=[8, 8, 8, 8, 6, 7], thang=None, ngay="戊子", ten="Sơn Địa Bác", bien="Phong Địa Quan", cung="Càn",
         the=5, ung=2, khong="午未",
         lt=["财寅", "子子", "父戌", "财卯", "官巳", "父未"], bl={5: "官巳"},
         # hào 3–6 khớp bản in; hào 1–2 bản in ghi Đằng Xà / Câu Trần (đảo so với bảng Lục thần chương)
         than=["朱雀", "青龙", "元武", "白虎", "滕蛇", "勾陈"], phuc={5: "兄申"}),
    dict(nguon="Tăng San Bốc Dịch q.2: tháng Dậu ngày Bính Thìn xem con bệnh, được Địa Phong Thăng "
               "(Tử Tôn Ngọ hỏa phục dưới Sửu thổ; 'Sửu thổ tuần không, phục dễ xuất')",
         hao=[8, 7, 7, 8, 8, 8], thang="酉", ngay="丙辰", ten="Địa Phong Thăng", bien=None, cung="Chấn",
         the=4, ung=1, khong="子丑",
         lt=["官酉", "父亥", "财丑", "官酉", "父亥", "财丑"], bl={}, than=None, phuc={4: "子午", 2: "兄寅"}),
    dict(nguon="Tăng San Bốc Dịch q.2: tháng Mão ngày Nhâm Thìn hỏi ngày nhận giấy tờ, được Sơn Hỏa Bí "
               "('Ngọ hỏa Phụ Mẫu là dụng thần, không mà phục dưới hào 2 Sửu thổ')",
         hao=[7, 8, 7, 8, 8, 7], thang="卯", ngay="壬辰", ten="Sơn Hỏa Bí", bien=None, cung="Cấn",
         the=1, ung=4, khong="午未",
         lt=["官寅", "财子", "兄戌", "财亥", "兄丑", "官卯"], bl={}, than=None, phuc={2: "父午", 3: "子申"}),
    dict(nguon="Tăng San Bốc Dịch q.2: tháng Mão ngày Quý Dậu xem cha mẹ bệnh, được Tụy biến Bĩ "
               "(Phụ Mẫu Mùi động hóa Tuất; 'Tuất gặp tuần không')",
         hao=[8, 8, 8, 7, 7, 6], thang="卯", ngay="癸酉", ten="Trạch Địa Tụy", bien="Thiên Địa Bĩ", cung="Đoài",
         the=2, ung=5, khong="戌亥",
         lt=["父未", "兄酉", "子亥", "财卯", "官巳", "父未"], bl={6: "父戌"}, than=None, phuc={},
         trang_thai={6: ["hóa TIẾN thần", "hóa KHÔNG"]}),
    dict(nguon="Tăng San Bốc Dịch q.2: tháng Hợi ngày Kỷ Sửu hỏi có chức vị không, được Đoài biến Tụng "
               "('Thế gặp tuần không'; Quan Quỷ Tỵ bị nguyệt phá)",
         hao=[9, 7, 8, 7, 7, 6], thang="亥", ngay="己丑", ten="Thuần Đoài", bien="Thiên Thủy Tụng", cung="Đoài",
         the=6, ung=3, khong="午未",
         lt=["父未", "兄酉", "子亥", "父丑", "财卯", "官巳"], bl={6: "父戌", 1: "财寅"}, than=None, phuc={},
         trang_thai={1: ["NGUYỆT PHÁ"], 6: ["TUẦN KHÔNG"]}),
    dict(nguon="Tăng San Bốc Dịch q.2: tháng Thìn ngày Quý Sửu xem bệnh, được Khốn biến Giải "
               "('hào Thế Dần mộc gặp tuần không'; Dậu hóa Thân thoái thần)",
         hao=[8, 7, 8, 7, 9, 8], thang="辰", ngay="癸丑", ten="Trạch Thủy Khốn", bien="Lôi Thủy Giải", cung="Đoài",
         the=1, ung=4, khong="寅卯",
         lt=["父未", "兄酉", "子亥", "官午", "父辰", "财寅"], bl={5: "兄申"}, than=None, phuc={},
         trang_thai={5: ["hóa THOÁI thần"], 1: ["TUẦN KHÔNG"]}),
    dict(nguon="Tăng San Bốc Dịch q.2: tháng Tỵ ngày Nhâm Tý hỏi thi hương, được Thủy Địa Tỷ ('Mão mộc tuần không')",
         hao=[8, 8, 8, 8, 7, 8], thang="巳", ngay="壬子", ten="Thủy Địa Tỷ", bien=None, cung="Khôn",
         the=3, ung=6, khong="寅卯",
         lt=["财子", "兄戌", "子申", "官卯", "父巳", "兄未"], bl={}, than=None, phuc={}),
]
# Quẻ mẫu có ngày giờ dương lịch đầy đủ (bài "六爻（六爻八卦）", sohu.com/n/481141833, phần Án lệ):
# 2013-11-10 20:21, can chi Quý Tỵ năm, Quý Hợi tháng, Canh Thìn ngày, tuần không Thân Dậu; Khiêm biến Tụy.
_MAU_NGAY = dict(ngay="2013-11-10", gio="20:21", utc=8.0, kinhdo=116.4, hao=[8, 8, 9, 6, 6, 8],
                 can_chi=("癸巳", "癸亥", "庚辰"), khong="申酉", ten="Địa Sơn Khiêm", bien="Trạch Địa Tụy",
                 cung="Đoài", the=5, ung=2,
                 lt=["兄酉", "子亥", "父丑", "兄申", "官午", "父辰"], bl={5: "兄酉", 4: "子亥", 3: "财卯"},
                 than=["滕蛇", "勾陈", "朱雀", "青龙", "元武", "白虎"], phuc={2: "财卯"})


def _kiem_mau(m, q, loi, ten):
    if q["ten"] != m["ten"]:
        loi.append("%s: tên quẻ %s ≠ %s" % (ten, q["ten"], m["ten"]))
    if m.get("bien") and q["ten_bien"] != m["bien"]:
        loi.append("%s: quẻ biến %s ≠ %s" % (ten, q["ten_bien"], m["bien"]))
    if (q["cung"], q["the"], q["ung"]) != (m["cung"], m["the"], m["ung"]):
        loi.append("%s: cung/thế/ứng %s" % (ten, (q["cung"], q["the"], q["ung"])))
    if q["khong"] != tuple(_ZHI.index(c) for c in m["khong"]):
        loi.append("%s: tuần không sai" % ten)
    for k, x in enumerate(m["lt"]):
        h = q["hao"][5 - k]
        if (h["lt"], h["chi"]) != (_LT_HAN[x[0]], _ZHI.index(x[1])):
            loi.append("%s: hào %d %s %s" % (ten, h["vi"], h["lt"], CHI_VN[h["chi"]]))
    for vi, x in m["bl"].items():
        b = q["hao"][vi - 1]["bien"]
        if not b or (b["lt"], b["chi"]) != (_LT_HAN[x[0]], _ZHI.index(x[1])):
            loi.append("%s: hào biến %d sai" % (ten, vi))
    if m.get("than"):
        for k, x in enumerate(m["than"]):
            if q["hao"][5 - k]["than"] != _TEN_THAN[x]:
                loi.append("%s: lục thần hào %d" % (ten, 6 - k))
    phuc = {p["vi"]: (p["lt"], p["chi"]) for p in q["phuc"]}
    if phuc != {vi: (_LT_HAN[x[0]], _ZHI.index(x[1])) for vi, x in m["phuc"].items()}:
        loi.append("%s: phục thần %s" % (ten, phuc))
    for vi, nhans in m.get("trang_thai", {}).items():
        h = q["hao"][vi - 1]
        tat_ca = " ".join(h["nhan"] + (h["bien"]["nhan"] if h["bien"] else []))
        for n in nhans:
            if n not in tat_ca:
                loi.append("%s: hào %d thiếu trạng thái '%s'" % (ten, vi, n))


def tu_kiem():
    """Kiểm bảng sinh bằng thuật toán với bảng chuẩn, quẻ mẫu trong sách, và chạy hết 4096 tổ hợp."""
    loi = []
    # (a) 64 quẻ đủ, không trùng, mỗi cung 8 quẻ, tên khớp maihoa
    if len(BAT_CUNG) != 64:
        loi.append("bát cung có %d quẻ" % len(BAT_CUNG))
    if {len(v) for v in QUE_THEO_CUNG.values()} != {8}:
        loi.append("có cung không đủ 8 quẻ")
    ten_all = [ten_que(k) for k in BAT_CUNG]
    if len(set(ten_all)) != 64:
        loi.append("tên quẻ trùng")
    for k, v in BAT_CUNG.items():
        if abs(v["the"] - v["ung"]) != 3:
            loi.append("thế/ứng sai ở %s" % ten_que(k))
        if v["loai"] in (0, 7) and quai_cua(k)[0] != v["cung"]:
            loi.append("nội quái quẻ thuần/quy hồn sai ở %s" % ten_que(k))
    # (b) thế ứng / cung các quẻ mẫu (Bốc Phệ Chính Tông – bảng bát cung; Tăng San Bốc Dịch)
    the_mau = [("Thiên Phong Cấu", "Càn", 1, 1), ("Địa Thiên Thái", "Khôn", 3, 3), ("Hỏa Địa Tấn", "Càn", 4, 6),
               ("Hỏa Thiên Đại Hữu", "Càn", 3, 7), ("Lôi Trạch Quy Muội", "Đoài", 3, 7),
               ("Thủy Hỏa Ký Tế", "Khảm", 3, 3), ("Phong Trạch Trung Phu", "Cấn", 4, 6),
               ("Thuần Càn", "Càn", 6, 0), ("Sơn Địa Bác", "Càn", 5, 5), ("Thủy Lôi Truân", "Khảm", 2, 2),
               ("Địa Phong Thăng", "Chấn", 4, 4), ("Sơn Hỏa Bí", "Cấn", 1, 1), ("Thủy Địa Tỷ", "Khôn", 3, 7)]
    theo_ten = {ten_que(k): v for k, v in BAT_CUNG.items()}
    for ten, cung, the, loai in the_mau:
        v = theo_ten.get(ten)
        if not v or (v["cung"], v["the"], v["loai"]) != (cung, the, loai):
            loi.append("bát cung sai: %s %s" % (ten, v and (v["cung"], v["the"], THE_LOAI[v["loai"]])))
    # (c) lục xung / lục hợp tính từ nạp giáp khớp danh sách sách
    xung_ds = {ten_que(k) for k in BAT_CUNG if luc_xung_que(k)}
    hop_ds = {ten_que(k) for k in BAT_CUNG if luc_hop_que(k)}
    if xung_ds != _LUC_XUNG:
        loi.append("lục xung lệch: %s" % (xung_ds ^ _LUC_XUNG))
    if hop_ds != _LUC_HOP:
        loi.append("lục hợp lệch: %s" % (hop_ds ^ _LUC_HOP))
    # (d) nạp giáp 8 quẻ thuần so với bảng chuẩn
    for ten, s in _NAP_CHUAN.items():
        k = QUE_THEO_CUNG[ten][0]
        chuan = [(_GAN.index(s[0]), _ZHI.index(c)) for c in s[1:4]] + [(_GAN.index(s[4]), _ZHI.index(c))
                                                                      for c in s[5:8]]
        if nap_giap_que(k) != chuan:
            loi.append("nạp giáp quẻ thuần %s sai" % ten)
        if {ten_luc_than(HANH_QUAI[ten], HANH_CHI[c]) for _, c in chuan} != set(LUC_THAN):
            loi.append("quẻ thuần %s không đủ 5 lục thân" % ten)
    # tiến thần / thoái thần / phục ngâm
    for p in _TIEN:
        a, b = _ZHI.index(p[0]), _ZHI.index(p[1])
        n, _, _ = _bien_hao(a, HANH_CHI[a], b, HANH_CHI[b], 3, ())
        n2, _, _ = _bien_hao(b, HANH_CHI[b], a, HANH_CHI[a], 3, ())
        if "hóa TIẾN thần" not in n or "hóa THOÁI thần" not in n2:
            loi.append("tiến/thoái thần sai ở cặp %s" % B_vn(p))
    dem_tien = 0
    for a in range(12):
        for b in range(12):
            n, _, _ = _bien_hao(a, HANH_CHI[a], b, HANH_CHI[b], 3, ())
            dem_tien += "hóa TIẾN thần" in n
            if a == b and ("PHỤC NGÂM (hóa cùng chi)" not in n or any("TIẾN" in x or "THOÁI" in x for x in n)):
                loi.append("phục ngâm hào bị gán sai")
    if dem_tien != 8:
        loi.append("số cặp tiến thần = %d" % dem_tien)
    # lục thần theo bảng Lục thần chương (Tăng San Bốc Dịch)
    cot = [(0, 1), (2, 3), (4,), (5,), (6, 7), (8, 9)]
    for r, hang in enumerate(_BANG_LUC_THAN):
        vi = 5 - r
        for j, cans in enumerate(cot):
            ten_t = _TEN_THAN[hang[2 * j:2 * j + 2]]
            for c in cans:
                if LUC_THAN_6[(KHOI_LUC_THAN[c] + vi) % 6] != ten_t:
                    loi.append("lục thần can %s hào %d" % (CAN_VN[c], vi + 1))
    # tuần không: Giáp Tý -> Tuất Hợi, Giáp Ngọ -> Thìn Tỵ, Quý Hợi -> Tý Sửu
    for g, kv in ((0, (10, 11)), (30, (4, 5)), (59, (0, 1)), (9, (10, 11)), (10, (8, 9))):
        if tuan_khong(g) != kv:
            loi.append("tuần không sai ở ngày %d" % g)
    # (e) quẻ mẫu trong sách
    for m in _MAU:
        gzn = [i for i in range(60) if _GAN[i % 10] == m["ngay"][0] and _ZHI[i % 12] == m["ngay"][1]][0]
        thang = _ZHI.index(m["thang"]) if m["thang"] else 0
        q = lap_que(m["hao"], thang, gzn)
        _kiem_mau(m, q, loi, m["nguon"][:40])
    # quẻ mẫu có ngày giờ đầy đủ: đi qua cả đường tính ngày tháng của tvbt
    try:
        import argparse
        import nc
        import tvbt as B
        m = _MAU_NGAY
        a = argparse.Namespace(ngay=m["ngay"], gio=m["gio"], gioi=None, noi=None, kinhdo=m["kinhdo"], mien=None,
                               utc=m["utc"], am=False, nhuan=False, lich_tz=None, gio_dong_ho=False, ty=1)
        tt = nc.thoi_diem(a)
        td = thoi_diem_que(tt)
        cc = (td["nam"], td["thang"], td["ngay"])
        if cc != m["can_chi"]:
            loi.append("mẫu 2013-11-10: can chi %s" % B.vn("".join(cc)))
        q = lap_que(m["hao"], td["chi_thang"], td["gz_ngay"])
        _kiem_mau(m, q, loi, "mẫu sohu 2013-11-10")
    except SystemExit as e:
        loi.append("mẫu ngày giờ: %s" % e)
    # (f) chạy hết 4096 tổ hợp hào × 3 ngày, mọi việc; in thử một phần
    ngay_thu = [(2, 0), (7, 33), (10, 59)]
    for n in range(4096):
        hao = [6 + (n >> (2 * i)) % 4 for i in range(6)]
        for ct, g in ngay_thu:
            q = lap_que(hao, ct, g)
            if len(q["phuc"]) != 5 - len({h["lt"] for h in q["hao"]}):
                loi.append("phục thần thiếu ở %s" % hao)
            if not any(h["the"] for h in q["hao"]) or not any(h["ung"] for h in q["hao"]):
                loi.append("thiếu thế/ứng ở %s" % hao)
            for lt in LUC_THAN:
                if chon_hao(q, lt)[1] is None:
                    loi.append("không chọn được %s ở %s" % (lt, hao))
        if n % 97 == 0:
            buf = io.StringIO()
            with redirect_stdout(buf):
                for v in list(VIEC)[n % len(VIEC):] [:2]:
                    in_que(q, v, "nu" if n % 2 else None, None, dt.date(2026, 1, 1), "thử", [("Thử", "x")])
                in_que(q, "chung", None, ["the", "phumau", "quanquy"][n % 3], None, None, None)
            s = buf.getvalue()
            if re.search(r"[一-鿿]", s):
                loi.append("in ra chữ Hán ở %s" % hao)
    # dụng thần lưỡng hiện: hai quẻ mẫu chương 32 Tăng San Bốc Dịch
    q = lap_que([7, 7, 7, 8, 7, 7], 7, 36)        # Tiểu Súc, tháng Mùi ngày Canh Tý
    ds, h, ghi, _ = chon_hao(q, "Thê Tài")
    if [x["chi"] for x in ds] != [4, 7] or h["chi"] != 7 or "hào 3 Thìn (tuần không)" not in ghi:
        loi.append("lưỡng hiện Tiểu Súc: chọn %s, ghi %s" % (h and h["chi"], ghi))
    q = lap_que([8, 7, 8, 8, 6, 6], 7, 30)        # Sư hóa Hoán, tháng Mùi ngày Giáp Ngọ
    ds, h, ghi, _ = chon_hao(q, "Quan Quỷ")
    if sorted(x["chi"] for x in ds) != [1, 4] or "Thìn (tuần không)" not in ghi or "Sửu (nguyệt phá)" not in ghi:
        loi.append("lưỡng hiện Sư hóa Hoán: %s" % ghi)
    # xu và thời gian
    v, _ = doc_xu(["SSS", "NNN", "SSN", "NNS", "SNS", "NSN"])
    if v != [6, 9, 7, 8, 7, 8]:
        loi.append("đổi đồng xu sai: %s" % v)
    v, _ = doc_xu(["SSS", "NNN", "SSN", "NNS", "SNS", "NSN"], dao=True)
    if v != [9, 6, 8, 7, 8, 7]:
        loi.append("đổi đồng xu (đảo) sai: %s" % v)
    qm = M.lap(1, 5, 1)       # Càn trên, Tốn dưới, hào 1 động -> Thiên Phong Cấu, hào 1 âm động
    if tu_mai_hoa(qm) != [6, 7, 7, 7, 7, 7]:
        loi.append("đổi quẻ Mai hoa sang số hào sai")
    return loi


def B_vn(s):
    return " ".join(CHI_VN[_ZHI.index(c)] for c in s)
