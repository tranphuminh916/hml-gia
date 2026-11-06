# -*- coding: utf-8 -*-
"""tuoivn.py - Xem tuổi theo cách phổ biến ở Việt Nam (lệnh: nc.py tuoivn).

Hai người (vợ chồng, làm ăn) so theo NĂM SINH ÂM LỊCH, 5 tiêu chí, mỗi tiêu chí ghi Tốt / Bình / Xấu:
  1. Mệnh (ngũ hành nạp âm năm sinh): sinh nhau là tốt, khắc nhau là xấu, cùng hành là bình.
  2. Thiên can năm: ngũ hợp là tốt; xung (Giáp–Canh, Ất–Tân, Bính–Nhâm, Đinh–Quý) là xấu.
  3. Địa chi năm: tam hợp, lục hợp là tốt; xung, hình, hại, phá là xấu; tự hình là xấu.
  4. Cung phi Bát trạch (nam, nữ khác công thức): du niên giữa hai cung phi – Sinh Khí, Thiên Y,
     Diên Niên, Phục Vị là tốt; Họa Hại, Lục Sát, Ngũ Quỷ, Tuyệt Mệnh là xấu.
  5. Ngũ hành cung phi ("thiên mệnh năm sinh"): sinh nhau tốt, khắc nhau xấu.
Không cộng thành một điểm hay một lời phán; đây là tục xem tuổi, chỉ để tham khảo, đặt cạnh phần
so Bát tự (`nc.py hoptac`), không thay.

Thêm: chọn năm sinh con hợp tuổi bố mẹ (--con-tu, --con-den): so mệnh, can, chi của từng năm với cả hai.

Dùng:
  python3 tvbt/nc.py tuoivn --nguoi 1986:nam 1990:nu
  python3 tvbt/nc.py tuoivn --nguoi 1986:nam 1990:nu --con-tu 2026 --con-den 2032
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tvbt as B  # noqa: E402
import hoptac as H  # noqa: E402

CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
HANH = ["Mộc", "Hỏa", "Thổ", "Kim", "Thủy"]
CAN_XUNG = {frozenset((i, i + 6)) for i in range(4)}
NGU_HOP = {frozenset((i, i + 5)) for i in range(5)}


def nap_am(nam):
    ten = B.hanh_nap_am_vn((nam - 4) % 10, (nam - 4) % 12)
    h = [w for w in ten.split("(")[0].split() if w in HANH]
    return ten, h[-1]


def sinh_khac(a, b):
    """Quan hệ ngũ hành giữa hai hành (tên). -> (mức, lời)."""
    ia, ib = HANH.index(a), HANH.index(b)
    if ia == ib:
        return "Bình", "cùng hành %s" % a
    if (ib - ia) % 5 == 1:
        return "Tốt", "%s sinh %s" % (a, b)
    if (ia - ib) % 5 == 1:
        return "Tốt", "%s sinh %s" % (b, a)
    if (ib - ia) % 5 == 2:
        return "Xấu", "%s khắc %s" % (a, b)
    return "Xấu", "%s khắc %s" % (b, a)


def can(a, b):
    if frozenset((a, b)) in NGU_HOP:
        return "Tốt", "%s hợp %s" % (CAN[a], CAN[b])
    if frozenset((a, b)) in CAN_XUNG:
        return "Xấu", "%s xung %s" % (CAN[a], CAN[b])
    return "Bình", "%s – %s không hợp không xung" % (CAN[a], CAN[b])


def chi(a, b):
    _, ten = H.quan_he_chi(a, b)
    muc = {"lục hợp": "Tốt", "tam hợp": "Tốt", "xung": "Xấu", "hình": "Xấu", "hại": "Xấu", "phá": "Xấu",
           "tự hình": "Xấu"}.get(ten, "Bình")
    loi = {"trùng": "cùng chi %s" % CHI[a], "bình thường": "%s – %s không hợp không xung" % (CHI[a], CHI[b])}.get(
        ten, "%s %s %s" % (CHI[a], ten, CHI[b]))
    return muc, loi


def du_nien(q1, q2):
    for ten, huong, tinh, q in B.bat_trach(q1):
        if q == q2:
            return ("Tốt" if "cát" in tinh else "Xấu"), "%s – %s: %s (%s)" % (q1, q2, ten, tinh)
    raise ValueError(q1 + q2)


def doc_nguoi(s):
    try:
        nam, gioi = s.split(":")
        nam = int(nam)
    except ValueError:
        raise SystemExit("LỖI: --nguoi dạng NĂM_ÂM:nam|nu, ví dụ 1986:nam")
    if gioi not in ("nam", "nu") or not 1800 <= nam <= 2200:
        raise SystemExit("LỖI: --nguoi dạng NĂM_ÂM:nam|nu, năm 1800–2200")
    return nam, gioi


def mo_ta(nam, gioi):
    q = B.cung_phi(nam, gioi)
    ten_na, h = nap_am(nam)
    return {"nam": nam, "gioi": gioi, "can": (nam - 4) % 10, "chi": (nam - 4) % 12, "nap_am": ten_na, "hanh": h,
            "phi": q, "hanh_phi": B.QUE[q][3], "nhom": "Đông tứ mệnh" if q in B.DONG_TU else "Tây tứ mệnh"}


def so_hai(p, q):
    return [("Mệnh (nạp âm)",) + sinh_khac(p["hanh"], q["hanh"]),
            ("Thiên can năm",) + can(p["can"], q["can"]),
            ("Địa chi năm",) + chi(p["chi"], q["chi"]),
            ("Cung phi (Bát trạch)",) + du_nien(p["phi"], q["phi"]),
            ("Ngũ hành cung phi",) + sinh_khac(p["hanh_phi"], q["hanh_phi"])]


def in_tuoi(p, q, con_tu=None, con_den=None):
    print("XEM TUỔI THEO CÁCH PHỔ BIẾN Ở VIỆT NAM (theo năm sinh âm lịch)")
    for x in (p, q):
        print("- %d %s %s (%s): mệnh %s; cung phi %s – hành %s, %s" % (
            x["nam"], CAN[x["can"]], CHI[x["chi"]], "nữ" if x["gioi"] == "nu" else "nam", x["nap_am"], x["phi"],
            x["hanh_phi"], x["nhom"]))
    print()
    print("| Tiêu chí | Kết quả | Vì sao |")
    print("|---|---|---|")
    rs = so_hai(p, q)
    for ten, muc, loi in rs:
        print("| %s | %s | %s |" % (ten, muc, loi))
    dem = {m: sum(1 for _, x, _ in rs if x == m) for m in ("Tốt", "Bình", "Xấu")}
    print("- Tổng: %d tốt, %d bình, %d xấu (5 tiêu chí; không quy ra điểm hay lời phán)." % (
        dem["Tốt"], dem["Bình"], dem["Xấu"]))
    if con_tu:
        con_den = con_den or con_tu
        print()
        print("NĂM SINH CON (so mệnh, can, chi năm của con với từng người; tuổi con theo năm âm lịch)")
        print("| Năm | Mệnh con | Với %d | Với %d | Tốt / Xấu |" % (p["nam"], q["nam"]))
        print("|---|---|---|---|---|")
        for n in range(con_tu, con_den + 1):
            c = mo_ta(n, "nam")
            o = []
            t = x = 0
            for cha in (p, q):
                ss = [sinh_khac(c["hanh"], cha["hanh"]), can(c["can"], cha["can"]), chi(c["chi"], cha["chi"])]
                t += sum(1 for m, _ in ss if m == "Tốt")
                x += sum(1 for m, _ in ss if m == "Xấu")
                o.append("; ".join(l for m, l in ss if m != "Bình") or "bình")
            print("| %d %s %s | %s | %s | %s | %d / %d |" % (n, CAN[c["can"]], CHI[c["chi"]], c["nap_am"], o[0], o[1], t, x))
        print("(Cung phi của con tùy con trai hay gái nên không xét ở bảng này.)")
    print()
    print("(Xem tuổi theo năm sinh là tục phổ biến; mỗi sách cân các tiêu chí khác nhau. Không dùng để quyết định "
          "chuyện hôn nhân hay sinh con; muốn sâu hơn thì so Bát tự đủ giờ sinh bằng `nc.py hoptac`.)")
    return rs


def them_lenh(sub):
    p = sub.add_parser("tuoivn", help="xem tuổi kiểu Việt Nam (mệnh, can, chi, cung phi, ngũ hành cung phi), năm sinh con")
    p.add_argument("--nguoi", nargs=2, required=True, help="hai người dạng NĂM_ÂM:nam|nu")
    p.add_argument("--con-tu", type=int)
    p.add_argument("--con-den", type=int)
    p.set_defaults(_chay=chay)


def chay(a):
    p, q = [mo_ta(*doc_nguoi(s)) for s in a.nguoi]
    if a.con_tu and (a.con_den or a.con_tu) - a.con_tu > 30:
        raise SystemExit("LỖI: tối đa 30 năm.")
    in_tuoi(p, q, a.con_tu, a.con_den)


def tu_kiem():
    loi = []
    p, q = mo_ta(1986, "nam"), mo_ta(1990, "nu")
    if p["nap_am"] != "Lư Trung Hỏa" or q["nap_am"] != "Lộ Bàng Thổ":
        loi.append("nạp âm 1986/1990: %s/%s" % (p["nap_am"], q["nap_am"]))
    if p["phi"] != "Khôn" or q["phi"] != "Cấn":
        loi.append("cung phi 1986 nam Khôn, 1990 nữ Cấn: %s/%s" % (p["phi"], q["phi"]))
    rs = dict((t, (m, l)) for t, m, l in so_hai(p, q))
    if rs["Mệnh (nạp âm)"][0] != "Tốt":                       # Hỏa sinh Thổ
        loi.append("Hỏa – Thổ phải tốt")
    if rs["Địa chi năm"][0] != "Tốt":                         # Dần – Ngọ tam hợp
        loi.append("Dần – Ngọ tam hợp")
    if "Sinh Khí" not in rs["Cung phi (Bát trạch)"][1]:        # Khôn – Cấn
        loi.append("Khôn – Cấn phải Sinh Khí")
    if "Tuyệt Mệnh" not in du_nien("Khôn", "Khảm")[1]:
        loi.append("Khôn – Khảm phải Tuyệt Mệnh")
    for y in range(1900, 2101):
        try:
            nap_am(y)
        except IndexError:
            loi.append("nạp âm năm %d" % y)
    if can(0, 6)[0] != "Xấu" or can(0, 5)[0] != "Tốt" or chi(0, 6)[0] != "Xấu" or chi(2, 11)[0] != "Tốt":
        loi.append("can/chi cơ bản")
    for a in ("Khảm", "Ly", "Chấn", "Tốn", "Càn", "Khôn", "Cấn", "Đoài"):
        for b in ("Khảm", "Ly", "Chấn", "Tốn", "Càn", "Khôn", "Cấn", "Đoài"):
            if du_nien(a, b)[0] != du_nien(b, a)[0]:
                loi.append("du niên không đối xứng %s %s" % (a, b))
            if (du_nien(a, b)[0] == "Tốt") != ((a in B.DONG_TU) == (b in B.DONG_TU)):
                loi.append("du niên tốt phải cùng nhóm %s %s" % (a, b))
    return loi
