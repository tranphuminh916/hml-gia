# -*- coding: utf-8 -*-
"""giosinh.py - Dò giờ sinh khi không nhớ (hoặc nhớ không chắc) bằng 7 câu hỏi.

Cách làm: lập sẵn lá số cho mọi giờ có thể trong ngày sinh (12 giờ âm lịch, giờ Tý tách đầu/cuối ngày),
rồi chấm điểm từng giờ theo câu trả lời. Mỗi câu chỉ nhân thêm một hệ số, không loại hẳn giờ nào,
vì các dấu hiệu dân gian không chắc chắn.

  1. Gia đình nhớ sinh lúc nào (hoặc giờ đồng hồ kèm độ sai)      – mạnh nhất
  2. Xoáy tóc trên đỉnh đầu  ┐ dấu hiệu dân gian chia 3 nhóm giờ:
  3. Tư thế ngủ quen          │ Tý Ngọ Mão Dậu (tứ chính) / Dần Thân Tỵ Hợi (tứ sinh) /
  4. Khuôn mặt                ┘ Thìn Tuất Sửu Mùi (tứ mộ)
  5. Điều chiếm tâm sức nhiều nhất từ khoảng 30 tuổi: cung an Thân (Tý Ngọ cư Mệnh, Sửu Mùi cư Phúc,
     Dần Thân cư Quan, Mão Dậu cư Di, Thìn Tuất cư Tài, Tỵ Hợi cư Phối) – chia 6 cặp giờ
  6. Tính cách giống mô tả nào (sao chính ở cung Mệnh của các giờ còn lại)
  7. Năm đời rẽ hướng rõ nhất: so với tuổi chuyển đại hạn của từng giờ

Dùng:
  python3 giosinh.py --ngay 1990-03-15 --gioi nam --noi "Hà Nội"                (liệt kê giờ + câu hỏi)
  python3 giosinh.py --ngay 1990-03-15 --gioi nam --noi "Hà Nội" --tra-loi '{"khoang":"sang","than":"Quan Lộc"}'
"""
import argparse
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tvbt as B  # noqa: E402
import tuvi_vn as T  # noqa: E402

NHOM = {0: "chinh", 6: "chinh", 3: "chinh", 9: "chinh",
        2: "sinh", 8: "sinh", 5: "sinh", 11: "sinh",
        4: "mo", 10: "mo", 1: "mo", 7: "mo"}
TEN_NHOM = {"chinh": "Tý, Ngọ, Mão, Dậu", "sinh": "Dần, Thân, Tỵ, Hợi", "mo": "Thìn, Tuất, Sửu, Mùi"}

# Khoảng giờ đồng hồ (phút trong ngày sinh) gia đình còn nhớ
KHOANG = {
    "khuya": ("Nửa đêm về sáng (23 giờ – 3 giờ)", [(0, 180), (1380, 1440)]),
    "rangsang": ("Gần sáng (3 – 7 giờ)", [(180, 420)]),
    "sang": ("Buổi sáng (7 – 11 giờ)", [(420, 660)]),
    "trua": ("Buổi trưa (11 – 15 giờ)", [(660, 900)]),
    "chieu": ("Buổi chiều (15 – 19 giờ)", [(900, 1140)]),
    "toi": ("Buổi tối (19 – 23 giờ)", [(1140, 1380)]),
    "ngay": ("Ban ngày, không rõ lúc nào (6 – 18 giờ)", [(360, 1080)]),
    "dem": ("Ban đêm, không rõ lúc nào (18 – 6 giờ)", [(0, 360), (1080, 1440)]),
}

THAN_CU = {  # cung an Thân -> lời hỏi dễ hiểu
    "Mệnh": "Chính bản thân: tự lập, tự quyết, sống theo cách của mình",
    "Phúc Đức": "Gia tộc, họ hàng, mồ mả, đời sống tinh thần và tâm linh",
    "Quan Lộc": "Công việc, sự nghiệp, chức vụ",
    "Thiên Di": "Đi lại, làm ăn xa, giao tiếp ngoài xã hội",
    "Tài Bạch": "Tiền bạc: kiếm tiền, giữ tiền, tích lũy",
    "Phu Thê": "Vợ hoặc chồng, chuyện hôn nhân và gia đình nhỏ",
}

TINH_CACH = {
    "Tử Vi": ("đĩnh đạc, tự trọng cao, thích đứng đầu và được người khác nể", "đôi khi cố chấp, khó nghe ai"),
    "Thiên Cơ": ("nhanh trí, hay tính toán, thích tìm tòi, khéo léo", "hay lo nghĩ, dễ đổi ý"),
    "Thái Dương": ("sôi nổi, thẳng thắn, rộng rãi, thích giúp người", "nóng vội, hay ôm việc"),
    "Vũ Khúc": ("cứng rắn, thực tế, giỏi việc tiền bạc, đã làm là làm đến cùng", "ít mềm mỏng, hơi khô khan"),
    "Thiên Đồng": ("hiền hòa, dễ gần, thích an nhàn và vui vẻ", "thiếu quyết đoán, ngại va chạm"),
    "Liêm Trinh": ("có nguyên tắc, nghiêm, có chí, coi trọng danh dự", "nóng tính, dễ va chạm"),
    "Thiên Phủ": ("điềm đạm, chu đáo, biết giữ của, thích ổn định", "thận trọng quá mức, ngại thay đổi"),
    "Thái Âm": ("nhẹ nhàng, kín đáo, tinh tế, giàu cảm xúc", "hay ngại, dễ buồn lòng"),
    "Tham Lang": ("hoạt bát, nhiều tài lẻ, giao thiệp rộng, ham trải nghiệm", "ham vui, khó theo một việc lâu"),
    "Cự Môn": ("ăn nói có lý, phân tích sắc, hay soi xét kỹ", "dễ nghi ngờ, lời nói hay gây va chạm"),
    "Thiên Tướng": ("tử tế, chỉn chu, trọng lẽ phải, hay đứng ra giúp người", "dễ bị kéo vào việc của người khác"),
    "Thiên Lương": ("chín chắn, nghiêm, thích che chở và khuyên bảo người khác", "già trước tuổi, hay lên lớp"),
    "Thất Sát": ("quyết đoán, gan dạ, làm nhanh, thích tự lập", "nóng nảy, khó chịu khi bị gò bó"),
    "Phá Quân": ("thích đổi mới, dám bỏ cũ làm lại, mạnh mẽ", "thất thường, hay bỏ dở"),
}

CAU_HOI = [
    {"id": "khoang", "hoi": "Gia đình nhớ {xg} sinh vào lúc nào?",
     "goi_y": "Nếu còn nhớ giờ đồng hồ (dù không chắc) thì chọn mục đầu và nhập giờ.",
     "lua_chon": [["giodongho", "Nhớ giờ đồng hồ, nhưng không chắc lắm"]] + [[k, v[0]] for k, v in KHOANG.items()]
                 + [["", "Hoàn toàn không biết"]]},
    {"id": "xoay", "hoi": "Xoáy tóc trên đỉnh đầu {xg} thế nào?",
     "goi_y": "Dấu hiệu dân gian. Nhờ người nhà xem hoặc chụp ảnh đỉnh đầu.",
     "lua_chon": [["chinh", "Một xoáy, nằm ngay chính giữa đỉnh đầu"],
                  ["sinh", "Một xoáy, gần giữa nhưng hơi lệch"],
                  ["mo", "Lệch hẳn sang một bên, hoặc có 2–3 xoáy"], ["", "Không rõ"]]},
    {"id": "ngu", "hoi": "Từ nhỏ {xg} quen ngủ tư thế nào nhất?",
     "goi_y": "Dấu hiệu dân gian: “Tý Ngọ Mão Dậu nằm ngửa, Dần Thân Tỵ Hợi nằm nghiêng, Thìn Tuất Sửu Mùi nằm sấp”.",
     "lua_chon": [["chinh", "Nằm ngửa"], ["sinh", "Nằm nghiêng"], ["mo", "Nằm sấp"], ["", "Không rõ"]]},
    {"id": "mat", "hoi": "Khuôn mặt {xg} gần với dáng nào nhất?",
     "goi_y": "Dấu hiệu dân gian: “Tý Ngọ Mão Dậu mặt tròn, Dần Thân Tỵ Hợi mặt vuông, Thìn Tuất Sửu Mùi mặt dài”.",
     "lua_chon": [["chinh", "Tròn, đầy đặn"], ["sinh", "Vuông, góc cạnh"], ["mo", "Dài, cằm thon"], ["", "Khó nói"]]},
    {"id": "than", "hoi": "Từ khoảng 30 tuổi, điều gì chiếm nhiều tâm sức của {xg} nhất?",
     "goi_y": "Theo Tử vi, giờ sinh quyết định cung an Thân – phần đời về sau hay xoay quanh cung đó. "
              "Chưa tới 30 tuổi thì chọn điều {xg} coi trọng nhất.",
     "lua_chon": [[k, v] for k, v in THAN_CU.items()] + [["", "Khó chọn"]]},
    {"id": "tinh", "hoi": "Mô tả nào giống tính cách {xg} nhất?",
     "goi_y": "Mỗi mô tả ứng với sao chính ở cung Mệnh của một vài giờ còn lại. Chọn cái gần nhất, không cần khớp hết.",
     "lua_chon": []},
    {"id": "nam", "hoi": "Năm nào đời {xg} rẽ hướng rõ nhất?",
     "goi_y": "Ví dụ: đổi hẳn nghề, lập gia đình, chuyển nơi ở, một biến cố lớn. Nhập 1–2 năm dương lịch; "
              "để trống nếu không có.",
     "lua_chon": []},
]

# Hệ số khi KHÔNG khớp (khớp = 1). Càng nhỏ càng tin câu đó.
HE_SO = {"xoay": 0.55, "ngu": 0.6, "mat": 0.6, "than": 0.45, "tinh": 0.5}


def _ns(ngay, gio, gioi, noi, am, nhuan, kinhdo, mien, utc):
    return argparse.Namespace(ngay=ngay, gio=gio, gioi=gioi or "nam", noi=noi or None, kinhdo=kinhdo,
                              mien=mien, utc=utc, am=bool(am), nhuan=bool(nhuan), lich_tz=None,
                              gio_dong_ho=False, ty=1)


def _hhmm(m):
    m = int(round(m))
    return "%02d:%02d" % (m // 60, m % 60)


def _la_so(tt):
    t = tt.t_dia_phuong
    ngay = t.date()
    ty_muon = t.hour == 23
    if ty_muon:
        ngay = ngay + dt.timedelta(days=1)
    gio = 0 if ty_muon else B.chi_gio(t)
    d, m, y, nhuan = B.duong_sang_am(ngay, tt.lich_tz)
    so_ngay = B.do_dai_thang_am(d, m, y, nhuan, tt.lich_tz)
    can, chi = (y - 4) % 10, (y - 4) % 12
    return T.lap_la_so(m, d, gio, can, chi, tt.gioi, so_ngay, nhuan), (ngay, gio), y


def _sao_chinh(ls, p):
    return [x for x in T.CHINH_TINH if x in ls["sao"][p]]


def _mo_ta(sao, muon=False):
    if not sao:
        return "dễ thích nghi, tính cách thay đổi theo hoàn cảnh và người bên cạnh"
    tot = [TINH_CACH[s][0] for s in sao]
    xau = [TINH_CACH[s][1] for s in sao]
    if len(sao) == 1:
        txt = "%s; nhưng %s" % (tot[0], xau[0])
    else:
        txt = "%s; lại %s; nhưng %s" % (tot[0], tot[1], xau[0])
    if muon:
        txt = "dễ thích nghi, chịu ảnh hưởng người xung quanh; nét chính: " + txt
    return txt[0].upper() + txt[1:]


def ung_vien(ngay, gioi, noi="", am=False, nhuan=False, kinhdo=None, mien=None, utc=None):
    """Mọi giờ có thể trong ngày sinh (theo giờ đồng hồ của ngày đó), mỗi giờ kèm lá số tóm tắt."""
    tt0 = B.doc_dau_vao(_ns(ngay, "12:00", gioi, noi, am, nhuan, kinhdo, mien, utc))
    lech = (tt0.tst - tt0.dong_ho).total_seconds() / 60          # giờ mặt trời thực - giờ đồng hồ (phút)
    ngay_dh = tt0.dong_ho.date()
    moc = sorted({0.0, 1440.0} | {60 * (2 * j + 1) - lech for j in range(-2, 14)
                                    if 0 < 60 * (2 * j + 1) - lech < 1440})
    ds = []
    for a, b in zip(moc, moc[1:]):
        if b - a < 1:
            continue
        giua = (a + b) / 2
        tt = B.doc_dau_vao(_ns(ngay_dh.isoformat(), _hhmm(giua), gioi, noi, False, False, tt0.kinh_do,
                               "nam" if tt0.mien_nam else "bac", tt0.utc_off))
        ls, khoa, nam_am = _la_so(tt)
        if ds and ds[-1]["_khoa"] == khoa:
            ds[-1]["dong_ho"][1] = _hhmm(b)
            ds[-1]["_doan"][1] = b
            continue
        _, eloc, tru = B.tu_tru(tt)
        g = khoa[1]
        menh = ls["menh"]
        sao = _sao_chinh(ls, menh)
        muon = not sao
        sao_xem = sao or _sao_chinh(ls, (menh + 6) % 12)
        ds.append({
            "_khoa": khoa, "_doan": [a, b],
            "gio": g, "ten": "Giờ " + T.CHI[g], "nhom": NHOM[g],
            "dong_ho": [_hhmm(a), _hhmm(b)],
            "gio_dai_dien": _hhmm(giua),
            "tru_ngay": B.vn(eloc.getDay()), "tru_gio": B.vn(eloc.getTime()),
            "menh": T.CHI[menh], "than_cu": T.ten_cung(ls, ls["than"]),
            "sao_menh": ["%s(%s)" % (s, T.do_sang(s, menh)) if T.do_sang(s, menh) else s for s in sao],
            "vo_chinh_dieu": muon, "sao_chieu": sao_xem if muon else [],
            "mo_ta": _mo_ta(sao_xem, muon),
            "cuc": T.TEN_CUC[ls["cuc"]], "dai_han": [ls["cuc"] + 10 * k for k in range(9)],
            "nam_am": nam_am,
        })
    # đặt tên phân biệt hai giờ Tý (đầu ngày / cuối ngày)
    ty = [x for x in ds if x["gio"] == 0]
    if len(ty) == 2:
        ty[0]["ten"] += " (đầu ngày)"
        ty[1]["ten"] += " (cuối ngày)"
    for i, x in enumerate(ds):
        x["id"] = "g%d" % i
        x.pop("_khoa")
    return {"lech_phut": round(lech, 1), "ngay_dong_ho": ngay_dh.isoformat(), "kinh_do": tt0.kinh_do,
            "utc": tt0.utc_off, "canh_bao": [c for c in tt0.canh_bao if "ranh giới" not in c], "ds": ds}


def _chung(doan, khoang):
    a, b = doan
    return sum(max(0.0, min(b, v) - max(a, u)) for u, v in khoang)


def _khoang_tu_tl(v):
    """-> (các khoảng phút trong ngày, mô tả, lề mềm (phút), xác suất nhớ sai hẳn).
    Giờ đồng hồ không vắt sang ngày khác: ngày sinh đã cho là ngày theo đồng hồ."""
    if isinstance(v, dict) and v.get("gio"):
        try:
            hh, mm = [int(x) for x in str(v["gio"]).split(":")[:2]]
        except ValueError:
            return None, None, 0, 0
        t = hh * 60 + mm
        sai = max(5, min(240, int(v.get("sai") or 30)))
        return [(max(0, t - sai), min(1440, t + sai))], "khoảng %s (±%d phút)" % (_hhmm(t), sai), 0, 0.1
    if isinstance(v, str) and v in KHOANG:
        return KHOANG[v][1], KHOANG[v][0], 45, 0.15
    return None, None, 0, 0


def _le(khoang, le):
    """Hai dải lề mềm hai bên mỗi khoảng (nhớ "buổi sáng" có thể là 6h45)."""
    kq = []
    for u, v in khoang:
        if le and u > 0:
            kq.append((max(0, u - le), u))
        if le and v < 1440:
            kq.append((v, min(1440, v + le)))
    return kq


def cham(uv, tl):
    """Chấm điểm. tl: dict câu trả lời. Trả về danh sách đã sắp xếp (phần trăm, lý do)."""
    ds = uv["ds"]
    # khả năng ban đầu tỉ lệ với độ dài khung giờ (hai giờ Tý đầu/cuối ngày chỉ khoảng 1 tiếng)
    w = {x["id"]: (x["_doan"][1] - x["_doan"][0]) / 120.0 for x in ds}
    ly = {x["id"]: [] for x in ds}
    kh, mo_ta_kh, le, eps = _khoang_tu_tl(tl.get("khoang"))
    if kh:
        # Hậu nghiệm ∝ (1-ε)·(phần khoảng nhớ rơi vào giờ này) + ε·(độ dài giờ / cả ngày)
        vien = _le(kh, le)
        W = sum(v - u for u, v in kh) + 0.4 * sum(v - u for u, v in vien)
        for x in ds:
            c = _chung(x["_doan"], kh)
            f = (c + 0.4 * _chung(x["_doan"], vien)) / W
            w[x["id"]] = (1 - eps) * f + eps * (x["_doan"][1] - x["_doan"][0]) / 1440
            share = c / sum(v - u for u, v in kh)
            if share >= 0.995 or c >= x["_doan"][1] - x["_doan"][0] - 0.5:
                ly[x["id"]].append("nằm trọn trong khoảng giờ gia đình nhớ" if share < 0.995 else
                                   "chứa trọn khoảng giờ gia đình nhớ")
            elif share >= 0.05:
                ly[x["id"]].append("chiếm %d%% khoảng giờ gia đình nhớ" % round(100 * share))
    ten_cau = {"xoay": "xoáy tóc", "ngu": "tư thế ngủ", "mat": "khuôn mặt"}
    for q in ("xoay", "ngu", "mat"):
        v = tl.get(q)
        if v in TEN_NHOM:
            for x in ds:
                if x["nhom"] == v:
                    ly[x["id"]].append(ten_cau[q] + " khớp nhóm " + TEN_NHOM[v])
                else:
                    w[x["id"]] *= HE_SO[q]
    v = tl.get("than")
    if v in THAN_CU:
        for x in ds:
            if x["than_cu"] == v:
                ly[x["id"]].append("Thân cư %s – khớp điều %s chú trọng từ 30 tuổi" % (v, "{xg}"))
            else:
                w[x["id"]] *= HE_SO["than"]
    v = tl.get("tinh")
    if isinstance(v, list) and v:
        for x in ds:
            if x["id"] in v:
                ly[x["id"]].append("tính cách khớp mô tả đã chọn")
            else:
                w[x["id"]] *= HE_SO["tinh"]
    nam = [int(n) for n in (tl.get("nam") or []) if str(n).strip().isdigit() and 1900 <= int(n) <= 2100]
    for n in nam:
        for x in ds:
            tuoi = n - x["nam_am"] + 1
            if tuoi < 1:
                continue
            k = min(abs(tuoi - a) for a in x["dai_han"])
            w[x["id"]] *= {0: 1.0, 1: 0.8, 2: 0.55}.get(k, 0.4)
            if k <= 1:
                ly[x["id"]].append("năm %d (%d tuổi) %s lúc chuyển đại hạn (%d tuổi)" % (
                    n, tuoi, "đúng" if k == 0 else "sát", min(x["dai_han"], key=lambda a: abs(tuoi - a))))
    tong = sum(w.values()) or 1
    kq = []
    for x in ds:
        kq.append({"id": x["id"], "pt": round(100 * w[x["id"]] / tong, 1), "ly_do": ly[x["id"]]})
    kq.sort(key=lambda r: -r["pt"])
    return kq, mo_ta_kh


def cau_tinh_cach(uv, diem, toi_da=5):
    """Lựa chọn cho câu 6: gom các giờ còn khả năng theo mô tả tính cách (trùng mô tả thì gộp)."""
    by_id = {x["id"]: x for x in uv["ds"]}
    nhom, cong = {}, 0.0
    for r in diem:
        if (cong >= 92 and len(nhom) >= 2) or r["pt"] < 2:
            break
        cong += r["pt"]
        nhom.setdefault(by_id[r["id"]]["mo_ta"], []).append(r["id"])
        if len(nhom) >= toi_da:
            break
    if len(nhom) < 2:
        return []
    return [[ids, mt] for mt, ids in nhom.items()]


def ket_luan(uv, diem):
    by_id = {x["id"]: x for x in uv["ds"]}
    a = diem[0]
    b = diem[1] if len(diem) > 1 else {"pt": 0}
    x = by_id[a["id"]]
    if a["pt"] >= 55 and a["pt"] >= 2 * b["pt"]:
        muc = "ro"
    elif a["pt"] >= 35 and a["pt"] >= 1.4 * b["pt"]:
        muc = "kha"
    else:
        muc = "chua_ro"
    return {"id": a["id"], "ten": x["ten"], "pt": a["pt"], "muc": muc,
            "dong_ho": x["dong_ho"], "gio_dai_dien": x["gio_dai_dien"],
            "nhi": [r["id"] for r in diem[1:3] if r["pt"] >= 10]}


def buoc(nguoi, tl=None):
    """Một bước cho giao diện: ứng viên, điểm hiện tại, câu hỏi (câu 6 tính theo các câu trước), kết luận."""
    tl = tl or {}
    uv = ung_vien(nguoi.get("ngay"), nguoi.get("gioi"), nguoi.get("noi") or "", nguoi.get("am"),
                  nguoi.get("nhuan"), nguoi.get("kinhdo"), nguoi.get("mien"), nguoi.get("utc"))
    tl_truoc = {k: v for k, v in tl.items() if k not in ("tinh", "nam")}
    diem_truoc, _ = cham(uv, tl_truoc)
    lc6 = cau_tinh_cach(uv, diem_truoc)
    diem, mo_ta_kh = cham(uv, tl)
    cau = json.loads(json.dumps(CAU_HOI, ensure_ascii=False))
    cau[5]["lua_chon"] = lc6
    ds = []
    for x in uv["ds"]:
        y = dict(x)
        y.pop("_doan", None)
        ds.append(y)
    r = {"ok": True, "lech_phut": uv["lech_phut"], "canh_bao": uv["canh_bao"], "ung_vien": ds,
         "diem": diem, "cau_hoi": cau, "ket_luan": ket_luan(uv, diem), "khoang_nho": mo_ta_kh}
    import contextlib
    import io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        in_ket_qua(r, "{xg}")
    r["van_ban"] = buf.getvalue()
    return r


def buoc_json(s):
    try:
        d = json.loads(s)
        return json.dumps(buoc(d.get("nguoi") or {}, d.get("tra_loi") or {}), ensure_ascii=False)
    except SystemExit as e:
        return json.dumps({"ok": False, "loi": str(e.code)}, ensure_ascii=False)
    except Exception as e:  # noqa: BLE001
        return json.dumps({"ok": False, "loi": "%s: %s" % (type(e).__name__, e)}, ensure_ascii=False)


def in_ket_qua(r, xg="anh/chị"):
    by_id = {x["id"]: x for x in r["ung_vien"]}
    print("DÒ GIỜ SINH")
    print("- Giờ mặt trời thực lệch giờ đồng hồ %+.0f phút; khung giờ dưới đây là GIỜ ĐỒNG HỒ của ngày sinh." %
          r["lech_phut"])
    for c in r["canh_bao"]:
        print("! " + c)
    print()
    print("| Giờ | Đồng hồ | Trụ giờ | Mệnh | Sao chính ở Mệnh | Thân cư | Cục | Khả năng | Lý do |")
    print("|---|---|---|---|---|---|---|---|---|")
    for d in r["diem"]:
        x = by_id[d["id"]]
        sao = ", ".join(x["sao_menh"]) or ("Vô chính diệu (mượn %s)" % ", ".join(x["sao_chieu"]))
        print("| %s | %s–%s | %s | %s | %s | %s | %s | %.0f%% | %s |" % (
            x["ten"], x["dong_ho"][0], x["dong_ho"][1], x["tru_gio"], x["menh"], sao, x["than_cu"], x["cuc"],
            d["pt"], "; ".join(d["ly_do"]).replace("{xg}", xg) or "–"))
    k = r["ket_luan"]
    print()
    muc = {"ro": "khá rõ", "kha": "nghiêng về", "chua_ro": "chưa rõ – nên đối chiếu thêm sự kiện đời thực"}[k["muc"]]
    print("KẾT LUẬN: %s (%s–%s giờ đồng hồ), %.0f%% – %s." % (k["ten"], k["dong_ho"][0], k["dong_ho"][1],
                                                              k["pt"], muc))
    if k["nhi"]:
        print("Giờ cần so thêm: " + ", ".join("%s (%s–%s)" % (by_id[i]["ten"], *by_id[i]["dong_ho"]) for i in k["nhi"]))


def main():
    p = argparse.ArgumentParser(description="Dò giờ sinh bằng 7 câu hỏi")
    p.add_argument("--ngay", required=True)
    p.add_argument("--gioi", required=True, choices=["nam", "nu"])
    p.add_argument("--noi")
    p.add_argument("--kinhdo", type=float)
    p.add_argument("--mien", choices=["bac", "nam"])
    p.add_argument("--utc", type=float)
    p.add_argument("--am", action="store_true")
    p.add_argument("--nhuan", action="store_true")
    p.add_argument("--tra-loi", default="{}", help="JSON câu trả lời: khoang, xoay, ngu, mat, than, tinh, nam")
    p.add_argument("--cau-hoi", action="store_true", help="in danh sách câu hỏi (kèm lựa chọn câu 6)")
    a = p.parse_args()
    r = buoc({"ngay": a.ngay, "gioi": a.gioi, "noi": a.noi, "kinhdo": a.kinhdo, "mien": a.mien, "utc": a.utc,
              "am": a.am, "nhuan": a.nhuan}, json.loads(a.tra_loi))
    if a.cau_hoi:
        for i, c in enumerate(r["cau_hoi"], 1):
            print("%d. %s" % (i, c["hoi"].replace("{xg}", "anh/chị")))
            for v, t in c["lua_chon"]:
                print("   - [%s] %s" % (v, t))
        print()
    in_ket_qua(r)


if __name__ == "__main__":
    main()
