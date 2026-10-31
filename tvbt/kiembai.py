# -*- coding: utf-8 -*-
"""kiembai.py - Tự kiểm bản luận trước khi gửi (máy kiểm phần kiểm được; phần còn lại theo bảng 7 mục trong SKILL.md).
Kiểm: lời tuyệt đối / gieo sợ hãi, câu nêu năm mà thiếu rào đón, mất cân đối giữa các mảng đời sống,
nói về sức khỏe mà thiếu lời "không thay khám bệnh", dụng thần nêu không nhất quán, thiếu căn cứ,
thiếu mục lưu ý / độ chắc chắn. Xếp hạng A–D.
Lệnh: nc.py kiembai --file ban_luan.md
"""
import re

TUYET_DOI = ["chắc chắn sẽ", "nhất định sẽ", "chắc chắn bị", "không thể tránh", "100%", "định mệnh",
             "số phận đã định", "chắc chắn là", "không bao giờ", "vĩnh viễn", "bắt buộc phải"]
SO_HAI = ["đại họa", "tai họa", "tai ương", "tuyệt mệnh", "chết", "mất mạng", "tử vong", "phá sản", "tù tội",
          "lao ngục", "ly hôn", "tang thương", "yểu", "đoản thọ", "tán gia bại sản", "tuyệt tự", "khắc chết"]
RAO_DON = ["có thể", "dễ", "nên", "cần lưu ý", "lưu ý", "xu hướng", "khả năng", "thường", "nghiêng", "thiên về",
           "thận trọng", "đề phòng", "tham khảo", "thuận lợi", "không thuận", "cần", "ưu tiên", "chưa chắc",
           "có dấu hiệu", "gợi ý", "phần nào", "tương đối", "nhìn chung"]
MANG = {
    "Công việc": ["công việc", "sự nghiệp", "quan lộc", "thăng tiến", "nghề", "kinh doanh", "chức"],
    "Tiền bạc": ["tiền", "tài chính", "tài bạch", "thu nhập", "đầu tư", "lộc", "tài lộc"],
    "Gia đình": ["vợ", "chồng", "hôn nhân", "con", "cha mẹ", "bố mẹ", "gia đình", "phu thê", "tử tức", "anh em"],
    "Sức khỏe": ["sức khỏe", "bệnh", "tật ách", "tạng", "ốm"],
    "Quan hệ": ["bạn bè", "đối tác", "cộng sự", "nhân viên", "nô bộc", "quý nhân", "khách hàng"],
}
HANH = ["Mộc", "Hỏa", "Thổ", "Kim", "Thủy"]


def chuan_hoa(van):
    """NFC và thống nhất cách bỏ dấu kiểu cũ (oà/oả/uỷ…) để so khớp."""
    import unicodedata
    van = unicodedata.normalize("NFC", van)
    for a, b in (("oà", "òa"), ("oá", "óa"), ("oả", "ỏa"), ("oã", "õa"), ("oạ", "ọa"), ("uỷ", "ủy"), ("uý", "úy"),
                 ("uỳ", "ùy"), ("uỹ", "ũy"), ("uỵ", "ụy"), ("Oà", "Òa"), ("Oá", "Óa"), ("Oả", "Ỏa")):
        van = van.replace(a, b)
    return van


def _co_tu(cau, tu):
    return re.search(r"(?<!\w)%s(?!\w)" % re.escape(tu), cau) is not None


def tach_cau(van):
    van = re.sub(r"\|", " . ", van)
    return [c.strip() for c in re.split(r"(?<=[.!?;\n])\s+", van) if c.strip()]


def kiem(van):
    """Trả về (hạng, list (mức, nội dung))."""
    van = chuan_hoa(van)
    vt = van.lower()
    cau = tach_cau(van)
    vd = []
    for c in cau:
        cl = c.lower()
        for t in TUYET_DOI:
            if t in cl:
                vd.append(("nặng", "Lời tuyệt đối '%s': %s" % (t, c[:140])))
        for t in SO_HAI:
            if re.search(r"(?<!\w)%s(?!\w)" % re.escape(t), cl):
                vd.append(("vừa", "Từ dễ gây sợ '%s' – viết lại thành 'cần lưu ý …': %s" % (t, c[:140])))
        if re.search(r"(?<!\d)(19|20)\d\d(?!\d)", c) and len(c) > 25 and not re.search(r"\|", c):
            if not any(_co_tu(cl, r) for r in RAO_DON) and not re.match(r"^\s*[-#*]?\s*(19|20)\d\d\s*[:–-]?\s*$", c):
                if re.search(r"\b(sẽ|bị|gặp|xảy ra|mất|được)\b", cl):
                    vd.append(("vừa", "Câu nêu năm cụ thể mà thiếu lời rào đón: %s" % c[:140]))
    # cân đối mảng
    dem = {k: sum(vt.count(w) for w in ws) for k, ws in MANG.items()}
    tong = sum(dem.values()) or 1
    if (dem["Công việc"] + dem["Tiền bạc"]) / tong > 0.6 and tong > 15:
        vd.append(("nhẹ", "Mất cân đối: công việc + tiền chiếm %.0f%% số lần nhắc (gia đình %d, sức khỏe %d, quan hệ %d) "
                   "– nếu là bản luận tổng quát thì cần bổ sung các mảng khác." % (
                       100 * (dem["Công việc"] + dem["Tiền bạc"]) / tong, dem["Gia đình"], dem["Sức khỏe"], dem["Quan hệ"])))
    # sức khỏe
    if dem["Sức khỏe"] and not re.search(r"không thay (cho )?(việc )?khám|bác sĩ|cơ sở y tế", vt):
        vd.append(("vừa", "Có nói về sức khỏe nhưng thiếu câu 'góc nhìn cổ học, không thay cho khám bệnh'."))
    # dụng thần nhất quán
    nhac = re.findall(r"dụng thần(?: chính)?(?: là| =|:)\s*([^.\n;(,]{1,40})", van, flags=re.I)
    nhac = [re.split(r"\b(?:hỷ|kỵ|hỉ|còn|nhưng)\b", x)[0] for x in nhac]
    tap = []
    for x in nhac:
        hs = frozenset(h for h in HANH if h in x)
        if hs:
            tap.append(hs)
    if len(set(tap)) > 1:
        vd.append(("nặng", "Dụng thần nêu không nhất quán giữa các đoạn: %s" % " / ".join(
            "+".join(sorted(t)) for t in dict.fromkeys(tap))))
    # căn cứ
    doan = [d for d in re.split(r"\n\s*\n", van) if len(d) > 160 and not d.lstrip().startswith("|")]
    co_can_cu = [d for d in doan if re.search(r"\(|vì |do |căn cứ|theo |dựa", d.lower())]
    if doan and len(co_can_cu) / len(doan) < 0.6:
        vd.append(("vừa", "Nhiều đoạn dài không nêu căn cứ (%d/%d đoạn có căn cứ) – mỗi nhận định cần ghi dựa vào yếu tố nào."
                   % (len(co_can_cu), len(doan))))
    # mục lưu ý, tham khảo, độ chắc chắn
    if "tham khảo" not in vt:
        vd.append(("vừa", "Thiếu câu nói rõ đây là tri thức truyền thống để tham khảo."))
    if not re.search(r"độ (chắc|tin)|chắc chắn đến đâu|mức độ chắc", vt):
        vd.append(("nhẹ", "Chưa nêu độ chắc chắn / độ tin của các kết luận chính."))
    n = {"nặng": 0, "vừa": 0, "nhẹ": 0}
    for m, _ in vd:
        n[m] += 1
    if n["nặng"] == 0 and n["vừa"] == 0 and n["nhẹ"] <= 1:
        hang = "A"
    elif n["nặng"] == 0 and n["vừa"] <= 2:
        hang = "B"
    elif n["nặng"] <= 1 and n["vừa"] <= 5:
        hang = "C"
    else:
        hang = "D"
    return hang, vd


def them_lenh(sub):
    p = sub.add_parser("kiembai", help="tự kiểm bản luận (file .md/.txt) trước khi gửi")
    p.add_argument("--file", required=True)
    p.set_defaults(_chay=chay)


def chay(a):
    try:
        van = open(a.file, encoding="utf-8").read()
    except OSError as e:
        raise SystemExit("LỖI: không đọc được file %s (%s)" % (a.file, e.strerror))
    hang, vd = kiem(van)
    print("TỰ KIỂM BẢN LUẬN: hạng %s (A: gửi được; B: sửa nhẹ; C: phải sửa; D: viết lại)" % hang)
    for m, t in vd:
        print("- [%s] %s" % (m, t))
    if not vd:
        print("- Không thấy lỗi máy kiểm được. Vẫn phải tự rà 7 mục trong SKILL.md.")


def tu_kiem():
    loi = []
    xau = ("Dụng thần là Thủy. Năm 2027 anh chắc chắn sẽ phá sản. Sức khỏe: bệnh gan.\n\n"
           "Dụng thần là Kim và Thổ. Công việc tiền bạc tiền tiền tiền công việc kinh doanh lộc tài chính đầu tư "
           "tiền công việc sự nghiệp thăng tiến nghề tiền lộc tài lộc thu nhập.")
    h, vd = kiem(xau)
    ts = " ".join(t for _, t in vd)
    for k in ("Lời tuyệt đối", "phá sản", "không thay cho khám", "không nhất quán", "Mất cân đối", "tham khảo"):
        if k not in ts:
            loi.append("không bắt được: %s" % k)
    if h not in ("C", "D"):
        loi.append("bài xấu phải hạng C/D, được %s" % h)
    tot = ("Tóm tắt: năm 2027 nhìn chung thuận lợi (vì can năm là hành hỷ). Dụng thần là Kim. Độ chắc chắn: trung bình.\n\n"
           "Sức khỏe nên lưu ý tiêu hóa (do Thổ bị khắc) – góc nhìn cổ học, không thay cho khám bệnh. "
           "Đây là tri thức truyền thống để tham khảo.")
    h, vd = kiem(tot)
    if h != "A":
        loi.append("bài tốt phải hạng A, được %s: %s" % (h, vd))
    h, vd = kiem("Dụng thần là Kim, hỷ thần là Thổ. Sau đó: dụng thần là Kim. Đây là tham khảo. Độ chắc chắn: trung bình.")
    if any("không nhất quán" in t for _, t in vd):
        loi.append("báo nhầm dụng thần không nhất quán khi có hỷ thần")
    h, vd = kiem("Dụng thần là Thuỷ. Phần sau: dụng thần là Hoả. Tham khảo. Độ chắc chắn thấp.")
    if not any("không nhất quán" in t for _, t in vd):
        loi.append("bỏ sót mâu thuẫn Thuỷ/Hoả viết kiểu cũ")
    h, vd = kiem("Năm 2027 anh sẽ mất việc vào thời điểm cuối năm. Tham khảo. Độ chắc chắn thấp.")
    if not any("rào đón" in t for _, t in vd):
        loi.append("'thời điểm' bị coi là lời rào đón")
    return loi
