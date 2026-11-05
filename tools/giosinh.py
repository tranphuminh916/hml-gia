# -*- coding: utf-8 -*-
"""giosinh.py - Dò giờ sinh khi không nhớ (hoặc nhớ không chắc) bằng một loạt câu hỏi ngắn (bản 2).

Cách làm: lập sẵn lá số cho mọi giờ có thể trong ngày sinh (12 giờ âm lịch, giờ Tý tách đầu/cuối ngày),
rồi chấm điểm từng giờ theo câu trả lời bằng phép Bayes: mỗi câu trả lời nhân khả năng của từng giờ với
một "hệ số hợp lý" tính từ ĐỘ TIN của câu đó. Câu yếu (dấu hiệu dân gian) chỉ nhích nhẹ; câu mạnh
(giờ gia đình nhớ, sinh mổ có hẹn) mới đẩy mạnh. Không loại hẳn giờ nào.

  1. khoang  Gia đình nhớ sinh lúc nào: giờ đồng hồ (± độ sai), tên giờ âm lịch, hoặc mốc trong ngày   – mạnh
  2. cach    Sinh mổ có hẹn trước / sinh thường / ở nhà                                                – mạnh nếu mổ hẹn
  3. xoay    Xoáy tóc: một xoáy giữa đỉnh (Tý Ngọ Mão Dậu) / lệch một bên (Dần Thân Tỵ Hợi) /
             hai xoáy trở lên (Thìn Tuất Sửu Mùi)                                                       – yếu
  4. ngu     Dáng ngủ quen: ngửa / nghiêng / sấp, cùng ba nhóm giờ như trên                             – yếu
  5. than    Mảng đời chiếm tâm sức nhất từ khoảng 30 tuổi = cung an Thân (Tý Ngọ cư Mệnh, Sửu Mùi cư
             Phúc, Dần Thân cư Quan, Mão Dậu cư Di, Thìn Tuất cư Tài, Tỵ Hợi cư Phối); có trừ "tỉ lệ nền"
             vì phần đông chọn công việc, tiền bạc                                                      – vừa
  6. tinh    Tính cách giống mô tả nào (sao chính cung Mệnh của các giờ còn khả năng)                    – vừa
  7. phoi    Tính vợ/chồng giống mô tả nào (sao chính cung Phu Thê)                                      – vừa
  8. nam     1–3 năm đời rẽ hướng rõ nhất, so với tuổi chuyển đại hạn của từng giờ                      – vừa

Câu nào không giúp phân biệt các giờ CÒN KHẢ NĂNG (theo các câu trước) thì tự bỏ qua (cờ "bo_qua").

Dùng:
  python3 giosinh.py --ngay 1990-03-15 --gioi nam --noi "Hà Nội" --cau-hoi
  python3 giosinh.py --ngay 1990-03-15 --gioi nam --noi "Hà Nội" --tra-loi '{"khoang":"sang","than":"Quan Lộc"}'
"""
import argparse
import datetime as dt
import json
import os
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tvbt as B  # noqa: E402
import tuvi_vn as T  # noqa: E402

PHIEN_BAN = 2

NHOM = {0: "chinh", 6: "chinh", 3: "chinh", 9: "chinh",
        2: "sinh", 8: "sinh", 5: "sinh", 11: "sinh",
        4: "mo", 10: "mo", 1: "mo", 7: "mo"}
TEN_NHOM = {"chinh": "Tý, Ngọ, Mão, Dậu", "sinh": "Dần, Thân, Tỵ, Hợi", "mo": "Thìn, Tuất, Sửu, Mùi"}
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

# Mốc trong ngày gia đình còn nhớ: (lời, các khoảng phút theo giờ đồng hồ, lề mềm (phút), xác suất nhớ sai hẳn)
KHOANG = {
    "nuadem": ("Khoảng nửa đêm (23 – 1 giờ)", [(0, 60), (1380, 1440)], 30, 0.12),
    "khuya": ("Đêm khuya, trời còn tối hẳn (1 – 4 giờ)", [(60, 240)], 40, 0.12),
    "gagay": ("Gà gáy, tờ mờ sáng (4 – 6 giờ)", [(240, 360)], 40, 0.12),
    "sangsom": ("Sáng sớm, trời đã sáng (6 – 8 giờ)", [(360, 480)], 40, 0.12),
    "sang": ("Buổi sáng (8 – 11 giờ)", [(480, 660)], 45, 0.12),
    "trua": ("Giữa trưa (11 – 13 giờ)", [(660, 780)], 40, 0.12),
    "chieu": ("Buổi chiều (13 – 17 giờ)", [(780, 1020)], 45, 0.12),
    "chaptoi": ("Chập tối, lúc lên đèn (17 – 19 giờ)", [(1020, 1140)], 40, 0.12),
    "toi": ("Buổi tối (19 – 23 giờ)", [(1140, 1380)], 45, 0.12),
    "ngay": ("Ban ngày, không rõ lúc nào (6 – 18 giờ)", [(360, 1080)], 45, 0.15),
    "dem": ("Ban đêm, không rõ lúc nào (18 – 6 giờ)", [(0, 360), (1080, 1440)], 45, 0.15),
    # khóa của bản 1 (không hiện trong lựa chọn nữa, vẫn đọc được)
    "rangsang": ("Gần sáng (3 – 7 giờ)", [(180, 420)], 45, 0.15),
}
KHOANG_CU = {"rangsang"}

THAN_CU = {  # cung an Thân -> lời hỏi dễ hiểu
    "Quan Lộc": "Công việc, sự nghiệp, chức vụ",
    "Tài Bạch": "Tiền bạc: kiếm tiền, giữ tiền, tích lũy",
    "Phu Thê": "Vợ hoặc chồng, chuyện hôn nhân và gia đình nhỏ",
    "Thiên Di": "Đi lại, làm ăn xa, quan hệ ngoài xã hội",
    "Phúc Đức": "Gia tộc, họ hàng, mồ mả, đời sống tinh thần và tâm linh",
    "Mệnh": "Chính bản thân: tự lập, tự quyết, sống theo cách của mình",
}
# Tỉ lệ người chọn mỗi mục dù Thân cư ở đâu (phần đông chọn công việc, tiền bạc).
THAN_NEN = {"Quan Lộc": 0.34, "Tài Bạch": 0.28, "Phu Thê": 0.13, "Mệnh": 0.11, "Thiên Di": 0.07, "Phúc Đức": 0.07}

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

# Độ tin của từng câu: r = xác suất câu trả lời thật sự phản ánh giờ sinh (phần còn lại là ngẫu nhiên).
DO_TIN = {"xoay": 0.12, "ngu": 0.12, "mat": 0.06, "than": 0.15, "tinh": 0.25, "phoi": 0.22}
# Năm rẽ hướng: hệ số theo khoảng cách (năm) tới lần chuyển đại hạn gần nhất.
# Tính từ: 30% số lần rẽ hướng rơi đúng/sát lúc chuyển đại hạn (0: 50%, 1: 40%, 2: 10%), 70% ngẫu nhiên.
HE_SO_NAM = {0: 2.2, 1: 1.3, 2: 0.85}
HE_SO_NAM_XA = 0.7

CAU_HOI = [
    {"id": "khoang", "hoi": "Gia đình nhớ {xg} sinh vào lúc nào?",
     "goi_y": "Câu quan trọng nhất. Nên hỏi lại mẹ hoặc người nhà. Nhớ giờ đồng hồ (dù không chắc) thì chọn mục đầu; "
              "nhớ \"sinh giờ Dần, giờ Thìn…\" thì chọn mục thứ hai.",
     "lua_chon": [["giodongho", "Nhớ giờ đồng hồ, nhưng không chắc lắm"],
                  ["tengio", "Nhớ tên giờ âm lịch (Tý, Sửu, Dần…)"]]
                 + [[k, v[0]] for k, v in KHOANG.items() if k not in KHOANG_CU]
                 + [["", "Hoàn toàn không biết"]]},
    {"id": "cach", "hoi": "{Xg} được sinh ra thế nào?",
     "goi_y": "Sinh mổ có hẹn trước thường rơi vào giờ hành chính, nên câu này giúp thu hẹp khá nhiều.",
     "lua_chon": [["mo_hen", "Sinh mổ, có hẹn ngày giờ trước"], ["mo_gap", "Sinh mổ cấp cứu, không hẹn trước"],
                  ["thuong", "Sinh thường ở bệnh viện, trạm xá"], ["nha", "Sinh ở nhà"], ["", "Không rõ"]]},
    {"id": "xoay", "hoi": "Xoáy tóc trên đỉnh đầu {xg} thế nào?",
     "goi_y": "Dấu hiệu dân gian, chỉ nhích nhẹ kết quả. Nhờ người nhà xem hoặc chụp ảnh đỉnh đầu.",
     "lua_chon": [["chinh", "Một xoáy, nằm ngay chính giữa đỉnh đầu"],
                  ["sinh", "Một xoáy, lệch hẳn sang một bên"],
                  ["mo", "Hai xoáy trở lên"], ["", "Không rõ"]]},
    {"id": "ngu", "hoi": "Từ nhỏ {xg} quen ngủ tư thế nào nhất?",
     "goi_y": "Dấu hiệu dân gian: “Tý Ngọ Mão Dậu nằm ngửa, Dần Thân Tỵ Hợi nằm nghiêng, Thìn Tuất Sửu Mùi nằm sấp”. "
              "Chỉ nhích nhẹ kết quả.",
     "lua_chon": [["chinh", "Nằm ngửa"], ["sinh", "Nằm nghiêng"], ["mo", "Nằm sấp"], ["", "Không rõ"]]},
    {"id": "than", "hoi": "Từ khoảng 30 tuổi đến nay, mảng nào chiếm nhiều tâm sức của {xg} nhất?",
     "goi_y": "Theo Tử vi, giờ sinh quyết định cung an Thân – nửa đời sau hay xoay quanh mảng đó. "
              "Chọn theo điều thật sự chiếm thời gian, suy nghĩ, không theo điều nên coi trọng.",
     "lua_chon": [[k, v] for k, v in THAN_CU.items()] + [["", "Khó chọn"]]},
    {"id": "tinh", "hoi": "Mô tả nào giống tính cách {xg} nhất?",
     "goi_y": "Mỗi mô tả ứng với sao chính ở cung Mệnh của một vài giờ còn khả năng. Chọn cái gần nhất, nhất là phần "
              "\"nhưng…\" (nhược điểm); không cần khớp hết. Có thể hỏi thêm người thân.",
     "lua_chon": []},
    {"id": "phoi", "hoi": "Mô tả nào giống tính {vc} của {xg} nhất?",
     "goi_y": "Ứng với sao chính ở cung Phu Thê của mỗi giờ. Chưa lập gia đình thì chọn \"Bỏ qua\".",
     "lua_chon": []},
    {"id": "nam", "hoi": "Những năm nào đời {xg} rẽ hướng rõ nhất?",
     "goi_y": "Ví dụ: đổi hẳn nghề, lập gia đình, chuyển nơi ở, một biến cố lớn. Nhập 1–3 năm dương lịch; "
              "để trống nếu không có.",
     "lua_chon": []},
]
THU_TU = [c["id"] for c in CAU_HOI]


def _ns(ngay, gio, gioi, noi, am, nhuan, kinhdo, mien, utc):
    return argparse.Namespace(ngay=ngay, gio=gio, gioi=gioi or "nam", noi=noi or None, kinhdo=kinhdo,
                              mien=mien, utc=utc, am=bool(am), nhuan=bool(nhuan), lich_tz=None,
                              gio_dong_ho=False, ty=1)


def _hhmm(m):
    m = int(round(m)) % 1440 if m < 1440 else 1440
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
    return T.lap_la_so(m, d, gio, can, chi, tt.gioi, so_ngay, nhuan), (ngay, gio), y, (d, m)


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


def _cung_sao(ls, p):
    """Sao chính ở cung p; vô chính diệu thì mượn cung đối. -> (nhãn sao, sao dùng để tả, có mượn không)"""
    sao = _sao_chinh(ls, p)
    muon = not sao
    xem = sao or _sao_chinh(ls, (p + 6) % 12)
    nhan = ["%s(%s)" % (s, T.do_sang(s, p)) if T.do_sang(s, p) else s for s in sao]
    return nhan, xem, muon


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
        ls, khoa, nam_am, ngay_am = _la_so(tt)
        if ds and ds[-1]["_khoa"] == khoa:
            ds[-1]["dong_ho"][1] = _hhmm(b)
            ds[-1]["_doan"][1] = b
            continue
        _, eloc, tru = B.tu_tru(tt)
        g = khoa[1]
        menh = ls["menh"]
        nhan, xem, muon = _cung_sao(ls, menh)
        nhan_pt, xem_pt, muon_pt = _cung_sao(ls, (menh + 10) % 12)   # Phu Thê = Mệnh + 10
        ds.append({
            "_khoa": khoa, "_doan": [a, b],
            "gio": g, "ten": "Giờ " + T.CHI[g], "nhom": NHOM[g],
            "dong_ho": [_hhmm(a), _hhmm(b)],
            "gio_dai_dien": _hhmm(giua),
            "tru_ngay": B.vn(eloc.getDay()), "tru_gio": B.vn(eloc.getTime()),
            "ngay_am": "%d/%d" % ngay_am,
            "menh": T.CHI[menh], "than_cu": T.ten_cung(ls, ls["than"]),
            "sao_menh": nhan, "vo_chinh_dieu": muon, "sao_chieu": xem if muon else [],
            "mo_ta": _mo_ta(xem, muon),
            "sao_phoi": nhan_pt or ["Vô chính diệu (mượn %s)" % ", ".join(xem_pt)],
            "mo_ta_phoi": _mo_ta(xem_pt, muon_pt),
            "cuc": T.TEN_CUC[ls["cuc"]], "dai_han": [ls["cuc"] + 10 * k for k in range(10)],
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


# ----------------------------------------------------------------------------- câu 1: giờ gia đình nhớ
def _chung(doan, khoang):
    a, b = doan
    return sum(max(0.0, min(b, v) - max(a, u)) for u, v in khoang)


def _khoang_tu_tl(v):
    """-> (các khoảng phút trong ngày, mô tả, lề mềm (phút), xác suất nhớ sai hẳn, mạnh?).
    Giờ đồng hồ không vắt sang ngày khác: ngày sinh đã cho là ngày theo đồng hồ."""
    if isinstance(v, dict) and v.get("gio"):
        try:
            hh, mm = [int(x) for x in str(v["gio"]).split(":")[:2]]
        except ValueError:
            return None, None, 0, 0
        t = hh * 60 + mm
        sai = max(5, min(240, int(v.get("sai") or 30)))
        return ([(max(0, t - sai), min(1440, t + sai))], "khoảng %s (±%d phút)" % (_hhmm(t), sai),
                max(10, sai // 2), 0.08)
    if isinstance(v, str) and v.startswith("tengio:"):
        k = v.split(":", 1)[1]
        if k == "ty_sau":        # giờ Tý, sau 12 giờ đêm (0–1 giờ sáng của ngày đã nhập)
            return [(0, 60)], "giờ Tý, sau 12 giờ đêm (0–1 giờ)", 30, 0.12
        if k == "ty_truoc":      # giờ Tý, trước 12 giờ đêm (23–24 giờ của ngày đã nhập)
            return [(1380, 1440)], "giờ Tý, trước 12 giờ đêm (23–24 giờ)", 30, 0.12
        if k.isdigit() and 0 <= int(k) < 12:
            g = int(k)
            kh = [(0, 60), (1380, 1440)] if g == 0 else [(120 * g - 60, 120 * g + 60)]
            return kh, "giờ %s (%s)" % (CHI[g], "23–1 giờ" if g == 0 else "%d–%d giờ" % (2 * g - 1, 2 * g + 1)), 30, 0.12
        return None, None, 0, 0
    if isinstance(v, str) and v in KHOANG:
        _, kh, le, eps = KHOANG[v]
        return kh, KHOANG[v][0], le, eps
    return None, None, 0, 0


def _le(khoang, le):
    """Hai dải lề mềm hai bên mỗi khoảng (nhớ "buổi sáng" có thể là 7h45). Không vắt qua 0h/24h."""
    kq = []
    for u, v in khoang:
        if le and u > 0 and not any(v2 == u for _, v2 in khoang):
            kq.append((max(0, u - le), u))
        if le and v < 1440 and not any(u2 == v for u2, _ in khoang):
            kq.append((v, min(1440, v + le)))
    return kq


# ----------------------------------------------------------------------------- chấm điểm
def _co_can_cu_manh(tl):
    kh, _, _, _ = _khoang_tu_tl(tl.get("khoang"))
    return bool(kh) or tl.get("cach") == "mo_hen"


def _lua_chon_mo_ta(uv, w, truong, toi_da=8):
    """Các mô tả (gộp giờ trùng mô tả) cho câu tinh/phoi, lấy từ các giờ còn khả năng theo w.
    Thứ tự xáo cố định theo nội dung, không theo khả năng (để không gợi ý)."""
    tong = sum(w.values()) or 1
    xs = sorted(uv["ds"], key=lambda x: -w[x["id"]])
    nhom = {}
    for x in xs:
        if w[x["id"]] / tong < 0.01 and len(nhom) >= 2:
            break
        mt = x[truong]
        if mt not in nhom and len(nhom) >= toi_da:
            continue
        nhom.setdefault(mt, []).append(x["id"])
    if len(nhom) < 2:
        return []
    ds = [[ids, mt] for mt, ids in nhom.items()]
    ds.sort(key=lambda o: zlib.crc32(o[1].encode("utf-8")))
    return ds


def _he_so_mo_ta(uv, tl_v, lua_chon, r):
    """Hệ số cho câu chọn mô tả. Nếu mô tả thật của giờ g có trong K mục hiện ra:
    P(chọn đúng) = r + (1-r)/(K+1), P(chọn mục khác hoặc "không giống") = (1-r)/(K+1);
    nếu không có trong các mục: mỗi lựa chọn 1/(K+1)."""
    K = len(lua_chon)
    hien = {i for ids, _ in lua_chon for i in ids}
    chon = set(tl_v or [])
    kq = {}
    for x in uv["ds"]:
        i = x["id"]
        if i not in hien:
            kq[i] = 1.0 / (K + 1)
        elif i in chon:
            kq[i] = r + (1 - r) / (K + 1)
        else:
            kq[i] = (1 - r) / (K + 1)
    return kq


def _nam_hop_le(tl, nam_sinh):
    out = []
    for n in (tl.get("nam") or [])[:3]:
        try:
            n = int(n)
        except (TypeError, ValueError):
            continue
        if nam_sinh < n <= 2100 and n not in out:
            out.append(n)
    return out


def cham(uv, tl, den=None):
    """Chấm điểm theo các câu trả lời trong tl (chỉ các câu đứng trước câu `den`, nếu có).
    -> (danh sách đã sắp xếp {id, pt, ly_do}, mô tả khoảng nhớ, trọng số thô, lựa chọn câu tinh/phoi đã dùng)."""
    ds = uv["ds"]
    ids_truoc = THU_TU[:THU_TU.index(den)] if den else THU_TU + ["mat"]
    tl = {k: v for k, v in tl.items() if k in ids_truoc}
    # khả năng ban đầu tỉ lệ với độ dài khung giờ (hai giờ Tý đầu/cuối ngày chỉ khoảng 1 tiếng)
    w = {x["id"]: (x["_doan"][1] - x["_doan"][0]) / 1440.0 for x in ds}
    ly = {x["id"]: [] for x in ds}
    lc_dung = {}
    kh, mo_ta_kh, le, eps = _khoang_tu_tl(tl.get("khoang"))
    if kh:
        # Khả năng ∝ (1-ε)·(phần khoảng nhớ, kể cả lề mềm, rơi vào giờ này)/(độ dài giờ) + ε (nhớ sai hẳn)
        vien = _le(kh, le)
        W = sum(v - u for u, v in kh) + 0.4 * sum(v - u for u, v in vien)
        tong_kh = sum(v - u for u, v in kh)
        for x in ds:
            dai = x["_doan"][1] - x["_doan"][0]
            c = _chung(x["_doan"], kh)
            f = (c + 0.4 * _chung(x["_doan"], vien)) / W
            # w đang là dai/1440 -> nhân hệ số (f/dai)·1440 cho phần khớp, ε cho phần nhớ sai
            w[x["id"]] = (1 - eps) * f + eps * dai / 1440
            share = c / tong_kh
            if share >= 0.995:
                ly[x["id"]].append("chứa trọn khoảng giờ gia đình nhớ")
            elif c >= dai - 0.5:
                ly[x["id"]].append("nằm trọn trong khoảng giờ gia đình nhớ")
            elif share >= 0.05:
                ly[x["id"]].append("chiếm %d%% khoảng giờ gia đình nhớ" % round(100 * share))
    v = tl.get("cach")
    if v == "mo_hen":
        # mổ có hẹn: khoảng 85% rơi vào 7–17 giờ
        gio_hc = [(420, 1020)]
        for x in ds:
            dai = x["_doan"][1] - x["_doan"][0]
            p = _chung(x["_doan"], gio_hc) / dai
            w[x["id"]] *= p * (0.85 / 600) + (1 - p) * (0.15 / 840)
            if p > 0.5:
                ly[x["id"]].append("trong giờ hành chính (sinh mổ có hẹn)")
    elif v in ("thuong", "nha"):
        # chuyển dạ tự nhiên hay rơi vào nửa đêm về sáng: nhích nhẹ 1–8 giờ
        for x in ds:
            dai = x["_doan"][1] - x["_doan"][0]
            p = _chung(x["_doan"], [(60, 480)]) / dai
            w[x["id"]] *= 1 + 0.2 * p
    ten_cau = {"xoay": "xoáy tóc", "ngu": "tư thế ngủ", "mat": "khuôn mặt"}
    for q in ("xoay", "ngu", "mat"):
        v = tl.get(q)
        if v in TEN_NHOM:
            r = DO_TIN[q]
            for x in ds:
                if x["nhom"] == v:
                    w[x["id"]] *= r + (1 - r) / 3
                    ly[x["id"]].append(ten_cau[q] + " khớp nhóm " + TEN_NHOM[v])
                else:
                    w[x["id"]] *= (1 - r) / 3
    v = tl.get("than")
    if v in THAN_CU:
        r = DO_TIN["than"]
        for x in ds:
            if x["than_cu"] == v:
                w[x["id"]] *= r + (1 - r) * THAN_NEN[v]
                ly[x["id"]].append("Thân cư %s – khớp mảng %s chú trọng từ 30 tuổi" % (v, "{xg}"))
            else:
                w[x["id"]] *= (1 - r) * THAN_NEN[v]
    for q, truong, nhan in (("tinh", "mo_ta", "tính cách khớp mô tả đã chọn"),
                            ("phoi", "mo_ta_phoi", "tính {vc} khớp mô tả đã chọn")):
        v = tl.get(q)
        if isinstance(v, list) and q in THU_TU:
            # lựa chọn được tính lại từ các câu đứng trước, giống lúc hiện cho người dùng
            truoc, _, w_truoc, _ = cham(uv, tl, q)
            lc = _lua_chon_mo_ta(uv, w_truoc, truong)
            if lc:
                lc_dung[q] = lc
                hs = _he_so_mo_ta(uv, v, lc, DO_TIN[q])
                for x in ds:
                    w[x["id"]] *= hs[x["id"]]
                    if x["id"] in v:
                        ly[x["id"]].append(nhan)
    for n in _nam_hop_le(tl, int(uv["ngay_dong_ho"][:4])):
        for x in ds:
            tuoi = n - x["nam_am"] + 1
            if tuoi < 1:
                continue
            gan = min(x["dai_han"], key=lambda a: abs(tuoi - a))
            k = abs(tuoi - gan)
            w[x["id"]] *= HE_SO_NAM.get(k, HE_SO_NAM_XA)
            if k <= 1:
                ly[x["id"]].append("năm %d (%d tuổi) %s lúc chuyển đại hạn (%d tuổi)" % (
                    n, tuoi, "đúng" if k == 0 else "sát", gan))
    tong = sum(w.values()) or 1
    kq = [{"id": x["id"], "pt": round(100 * w[x["id"]] / tong, 1), "ly_do": ly[x["id"]]} for x in ds]
    kq.sort(key=lambda r: -r["pt"])
    return kq, mo_ta_kh, w, lc_dung


def _con_kha_nang(uv, w, nguong=0.03):
    """Các giờ còn đáng kể: gom theo khả năng giảm dần tới 97%, bỏ giờ dưới ngưỡng."""
    tong = sum(w.values()) or 1
    xs = sorted(uv["ds"], key=lambda x: -w[x["id"]])
    out, cong = [], 0.0
    for x in xs:
        p = w[x["id"]] / tong
        if out and (cong >= 0.97 or p < nguong):
            break
        out.append(x)
        cong += p
    return out


def _bo_qua(uv, tl, q, w, nguoi_tuoi):
    """Câu q có nên bỏ qua không (không giúp phân biệt các giờ còn khả năng). -> lý do hoặc ''."""
    con = _con_kha_nang(uv, w)
    if len(con) <= 1:
        return "đã đủ rõ"
    if q == "cach":
        kh, _, _, _ = _khoang_tu_tl(tl.get("khoang"))
        if kh and sum(v - u for u, v in kh) <= 180:
            return "giờ gia đình nhớ đã đủ hẹp"
        hc = [_chung(x["_doan"], [(420, 1020)]) / (x["_doan"][1] - x["_doan"][0]) for x in con]
        if min(hc) > 0.95 or max(hc) < 0.05:
            return "không giúp phân biệt"
        return ""
    if q in ("xoay", "ngu"):
        return "" if len({x["nhom"] for x in con}) > 1 else "các giờ còn lại cùng nhóm"
    if q == "than":
        if nguoi_tuoi is not None and nguoi_tuoi < 28:
            return "chưa tới tuổi xét cung Thân"
        return "" if len({x["than_cu"] for x in con}) > 1 else "các giờ còn lại cùng Thân cư"
    if q in ("tinh", "phoi"):
        return ""   # quyết định theo số lựa chọn
    if q == "nam":
        return "" if len({x["dai_han"][0] for x in con}) > 1 else "các giờ còn lại chuyển đại hạn cùng tuổi"
    return ""


def ket_luan(uv, diem, tl):
    by_id = {x["id"]: x for x in uv["ds"]}
    a = diem[0]
    b = diem[1] if len(diem) > 1 else {"pt": 0, "id": None}
    x = by_id[a["id"]]
    co_tra_loi = any(tl.get(k) not in (None, "", []) for k in THU_TU + ["mat"])
    manh = _co_can_cu_manh(tl)
    if not co_tra_loi:
        muc = "chua_tra_loi"
    elif a["pt"] >= 70 and a["pt"] >= 3 * b["pt"] and manh:
        muc = "ro"
    elif a["pt"] >= 45 and a["pt"] >= 1.6 * b["pt"]:
        muc = "kha"
    else:
        muc = "chua_ro"
    ghi_chu = []
    if co_tra_loi and not manh:
        ghi_chu.append("Chưa có giờ gia đình nhớ nên kết quả chỉ dựa vào dấu hiệu dân gian, tính cách và mốc đời; "
                       "nên hỏi thêm người nhà và đối chiếu sự kiện.")
    if b.get("id") and by_id[a["id"]]["gio"] == 0 and by_id[b["id"]]["gio"] == 0 and b["pt"] >= a["pt"] / 3:
        ghi_chu.append("Hai giờ Tý (sau 12 giờ đêm và trước 12 giờ đêm) cách nhau một ngày âm lịch nên lá số khác hẳn. "
                       "Hỏi lại người nhà sinh trước hay sau 12 giờ đêm; không rõ thì so tính cách, tính vợ/chồng "
                       "ở hai lá số.")
    return {"id": a["id"], "ten": x["ten"], "pt": a["pt"], "muc": muc,
            "dong_ho": x["dong_ho"], "gio_dai_dien": x["gio_dai_dien"],
            "nhi": [r["id"] for r in diem[1:3] if r["pt"] >= 10], "ghi_chu": ghi_chu}


def buoc(nguoi, tl=None):
    """Một bước cho giao diện: ứng viên, điểm, câu hỏi (lựa chọn và cờ bỏ qua tính theo các câu trước), kết luận."""
    tl = dict(tl or {})
    uv = ung_vien(nguoi.get("ngay"), nguoi.get("gioi"), nguoi.get("noi") or "", nguoi.get("am"),
                  nguoi.get("nhuan"), nguoi.get("kinhdo"), nguoi.get("mien"), nguoi.get("utc"))
    gioi = nguoi.get("gioi") or "nam"
    vc = "chồng" if gioi == "nu" else "vợ"
    nam_sinh = int(uv["ngay_dong_ho"][:4])
    tuoi = dt.date.today().year - nam_sinh
    cau = json.loads(json.dumps(CAU_HOI, ensure_ascii=False))
    # Đi lần lượt từng câu: lựa chọn và cờ bỏ qua chỉ tính theo các câu đứng trước (đã bỏ câu bị bỏ qua),
    # giống hệt những gì người dùng thấy khi trả lời.
    tl_dung = dict(tl)
    for c in cau:
        q = c["id"]
        _, _, w_truoc, _ = cham(uv, tl_dung, q)
        c["hoi"] = c["hoi"].replace("{vc}", vc)
        c["goi_y"] = c["goi_y"].replace("{vc}", vc)
        if q in ("tinh", "phoi"):
            c["lua_chon"] = _lua_chon_mo_ta(uv, w_truoc, "mo_ta" if q == "tinh" else "mo_ta_phoi")
            c["bo_qua"] = "" if c["lua_chon"] else "các giờ còn lại cùng mô tả"
            if q == "phoi" and not c["bo_qua"] and tuoi < 20:
                c["bo_qua"] = "chưa tới tuổi lập gia đình"
        else:
            c["bo_qua"] = _bo_qua(uv, tl_dung, q, w_truoc, tuoi)
        if c["bo_qua"]:
            tl_dung.pop(q, None)
    diem, mo_ta_kh, _, _ = cham(uv, tl_dung)
    ds = []
    for x in uv["ds"]:
        y = dict(x)
        y.pop("_doan", None)
        ds.append(y)
    r = {"ok": True, "phien_ban": PHIEN_BAN, "lech_phut": uv["lech_phut"], "canh_bao": uv["canh_bao"],
         "ung_vien": ds, "diem": diem, "cau_hoi": cau, "ket_luan": ket_luan(uv, diem, tl_dung),
         "khoang_nho": mo_ta_kh, "vc": vc}
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
    vc = r.get("vc", "vợ/chồng")
    print("DÒ GIỜ SINH")
    print("- Giờ mặt trời thực lệch giờ đồng hồ %+.0f phút; khung giờ dưới đây là GIỜ ĐỒNG HỒ của ngày sinh." %
          r["lech_phut"])
    for c in r["canh_bao"]:
        print("! " + c)
    print()
    print("| Giờ | Đồng hồ | Ngày âm | Trụ giờ | Mệnh | Sao chính ở Mệnh | Phu Thê | Thân cư | Cục | Khả năng | Lý do |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for d in r["diem"]:
        x = by_id[d["id"]]
        sao = ", ".join(x["sao_menh"]) or ("Vô chính diệu (mượn %s)" % ", ".join(x["sao_chieu"]))
        print("| %s | %s–%s | %s | %s | %s | %s | %s | %s | %s | %.0f%% | %s |" % (
            x["ten"], x["dong_ho"][0], x["dong_ho"][1], x["ngay_am"], x["tru_gio"], x["menh"], sao,
            ", ".join(x["sao_phoi"]), x["than_cu"], x["cuc"], d["pt"],
            "; ".join(d["ly_do"]).replace("{xg}", xg).replace("{vc}", vc) or "–"))
    k = r["ket_luan"]
    print()
    muc = {"ro": "khá rõ", "kha": "nghiêng về", "chua_ro": "chưa rõ – nên đối chiếu thêm sự kiện đời thực",
           "chua_tra_loi": "chưa trả lời câu nào"}[k["muc"]]
    print("KẾT LUẬN: %s (%s–%s giờ đồng hồ), %.0f%% – %s." % (k["ten"], k["dong_ho"][0], k["dong_ho"][1],
                                                              k["pt"], muc))
    if k["nhi"]:
        print("Giờ cần so thêm: " + ", ".join("%s (%s–%s)" % (by_id[i]["ten"], *by_id[i]["dong_ho"]) for i in k["nhi"]))
    for g in k.get("ghi_chu", []):
        print("Lưu ý: " + g)
    bo = [c for c in r["cau_hoi"] if c.get("bo_qua")]
    if bo:
        print("Câu tự bỏ qua: " + "; ".join("%s (%s)" % (c["id"], c["bo_qua"]) for c in bo))


def main():
    p = argparse.ArgumentParser(description="Dò giờ sinh bằng các câu hỏi ngắn (bản 2)")
    p.add_argument("--ngay", required=True)
    p.add_argument("--gioi", required=True, choices=["nam", "nu"])
    p.add_argument("--noi")
    p.add_argument("--kinhdo", type=float)
    p.add_argument("--mien", choices=["bac", "nam"])
    p.add_argument("--utc", type=float)
    p.add_argument("--am", action="store_true")
    p.add_argument("--nhuan", action="store_true")
    p.add_argument("--tra-loi", default="{}",
                   help="JSON câu trả lời: khoang, cach, xoay, ngu, than, tinh, phoi, nam")
    p.add_argument("--cau-hoi", action="store_true", help="in danh sách câu hỏi (lựa chọn tính theo câu trả lời)")
    a = p.parse_args()
    r = buoc({"ngay": a.ngay, "gioi": a.gioi, "noi": a.noi, "kinhdo": a.kinhdo, "mien": a.mien, "utc": a.utc,
              "am": a.am, "nhuan": a.nhuan}, json.loads(a.tra_loi))
    if a.cau_hoi:
        for i, c in enumerate(r["cau_hoi"], 1):
            print("%d. [%s] %s%s" % (i, c["id"], c["hoi"].replace("{xg}", "anh/chị").replace("{Xg}", "Anh/chị"),
                                     "  (bỏ qua: %s)" % c["bo_qua"] if c.get("bo_qua") else ""))
            for v, t in c["lua_chon"]:
                print("   - [%s] %s" % (v, t))
        print()
    in_ket_qua(r)


if __name__ == "__main__":
    main()
