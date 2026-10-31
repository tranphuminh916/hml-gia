# -*- coding: utf-8 -*-
"""Vẽ bàn Kỳ môn 9 cung thành trang HTML và ảnh PNG (dùng Chromium + Playwright nếu có)."""
import html
import os

THU_TU = [4, 9, 2, 3, 5, 7, 8, 1, 6]
TEN_CUNG = {1: "Khảm · Bắc", 2: "Khôn · Tây Nam", 3: "Chấn · Đông", 4: "Tốn · Đông Nam", 5: "Trung cung",
            6: "Càn · Tây Bắc", 7: "Đoài · Tây", 8: "Cấn · Đông Bắc", 9: "Ly · Nam"}
HANH_CUNG = {1: "Thủy", 2: "Thổ", 3: "Mộc", 4: "Mộc", 5: "Thổ", 6: "Kim", 7: "Kim", 8: "Thổ", 9: "Hỏa"}
MAU_HANH = {"Thủy": "#2f6fb0", "Mộc": "#2e8b57", "Hỏa": "#c0392b", "Thổ": "#b7791f", "Kim": "#7f8c8d"}
MON_CAT = {"Khai", "Hưu", "Sinh"}
MON_HUNG = {"Tử", "Kinh", "Thương"}
THAN_CAT = {"Trực Phù", "Thái Âm", "Lục Hợp", "Cửu Địa", "Cửu Thiên", "Thái Thường"}
SAO_CAT = {"Thiên Phụ", "Thiên Cầm", "Thiên Tâm", "Thiên Nhậm", "Thiên Xung"}

CSS = """
*{box-sizing:border-box}body{margin:0;background:#f6f1e7;font-family:'DejaVu Sans','Noto Sans',Arial,sans-serif;color:#2b2b2b}
.wrap{width:1080px;padding:22px 26px 18px}
h1{font-size:25px;margin:0 0 4px;text-align:center;color:#5a3e1b}
.sub{font-size:15px;text-align:center;margin:0 0 4px;color:#444}
.q{font-size:15px;text-align:center;color:#8b1e1e;margin:0 0 12px;font-style:italic}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border:3px solid #5a3e1b;background:#fffdf8}
.o{min-height:268px;padding:10px 12px 8px;border:1px solid #cdbb9a;position:relative}
.o.ban{background:#fff4d6}
.top{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px}
.cung{font-size:12.5px;font-weight:bold;letter-spacing:.3px}
.than{font-size:19px;font-weight:bold}
.than.cat{color:#1d6b3a}.than.hung{color:#9b1c1c}
.badges span{display:inline-block;font-size:11.5px;font-weight:bold;border-radius:5px;padding:2px 6px;margin-left:4px}
.kv{background:#f1c40f;color:#222}.ma{background:#222;color:#f1c40f}.bm{background:#8b1e1e;color:#fff}.tp{background:#5a3e1b;color:#fff}
.row{display:flex;align-items:center;justify-content:space-between;margin:5px 0}
.box{width:50%;text-align:center;font-weight:bold;font-size:17px;padding:6px 4px;border-radius:7px;border:2px solid #c9a96e}
.box.cat{background:#d8f0dc;color:#1d6b3a}.box.hung{background:#f7d7d7;color:#9b1c1c}.box.binh{background:#ececec;color:#444}
.box.sao{background:#fbf3df;color:#5a3e1b}
.cans{display:flex;gap:5px}
.can{min-width:46px;height:40px;border-radius:20px;display:flex;align-items:center;justify-content:center;font-weight:bold;
font-style:italic;font-size:16px;border:2px solid #c9a96e;background:#fff;padding:0 7px;white-space:nowrap}
.can.dia{background:#f3ead8}.can.an{background:#e8e2f5;border-color:#9b8bc4;font-size:14px}
.nhan{font-size:10.5px;color:#777;text-align:right;margin-top:-3px}
.tt{font-size:12px;color:#5b4a2f;margin-top:5px;line-height:1.35}
.tt b{color:#8b1e1e}
.giua{display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;background:#fff8e8}
.giua .cuc{font-size:20px;font-weight:bold;color:#8b1e1e;margin-bottom:6px}
.giua table{font-size:14.5px;border-collapse:collapse;margin:4px auto}
.giua td{padding:2px 8px;text-align:left}
.foot{font-size:12px;color:#666;margin-top:10px;line-height:1.4}
"""


def _e(s):
    return html.escape(str(s))


def _can(ten, lop):
    return '<div class="can %s">%s</div>' % (lop, _e(ten))


def lam_html(b, CAN, thong_tin):
    """b: bàn (dict của kymon); CAN: list tên can; thong_tin: dict tieu_de, thoi_gian, cau_hoi, tru (list (nhãn, can chi, cung)),
    cuc, trang_thai (cung -> list chuỗi), ban_menh (cung hoặc None), ten_ban_menh."""
    phi = b.get("loai") == "phi"
    an = b.get("an_can")
    tt = thong_tin.get("trang_thai", {})
    o = []
    for p in THU_TU:
        if p == 5 and not phi:
            dong = "".join("<tr><td>%s</td><td><b>%s</b></td><td>%s</td></tr>" % (_e(a), _e(c), _e(g))
                           for a, c, g in thong_tin.get("tru", []))
            o.append('<div class="o giua"><div class="cuc">%s</div><table>%s</table>'
                     '<div class="tt">Trung cung: địa bàn <b>%s</b>%s · ký Khôn</div></div>' % (
                         _e(thong_tin.get("cuc", "")), dong, _e(CAN[b["dia"][5]]),
                         (", ẩn can <b>%s</b>" % _e(CAN[an[5][0]])) if an and 5 in an else ""))
            continue
        than = b["than"].get(p, "")
        badges = []
        if p == b["Q"]:
            badges.append('<span class="tp">Trực phù</span>')
        if p == b["D"]:
            badges.append('<span class="tp">Trực sử</span>')
        if p != 5 and set(_cung_chi(p)) & set(b["khong"]):
            badges.append('<span class="kv">Kv</span>')
        if p != 5 and b["ma"] in _cung_chi(p):
            badges.append('<span class="ma">Mã</span>')
        if thong_tin.get("ban_menh") == p:
            badges.append('<span class="bm">Bản mệnh</span>')
        m = b["mon"].get(p)
        lop_m = "cat" if m in MON_CAT else ("hung" if m in MON_HUNG else "binh")
        sao = " + ".join(s.replace("Thiên ", "") for s in b["thien_sao"][p])
        tc = " ".join(CAN[c] for c in b["thien_can"][p])
        dc = " ".join(CAN[c] for c in [b["dia"][p]] + ([b["dia"][5]] if p == 2 and not phi else []))
        dong_an = _can(" ".join(CAN[c] for c in an[p]), "an") if an and p in an else ""
        mau = MAU_HANH[HANH_CUNG[p]]
        o.append(
            '<div class="o%s" style="border-top:5px solid %s">'
            '<div class="top"><div><div class="cung" style="color:%s">%s</div><div class="than %s">%s</div></div>'
            '<div class="badges">%s</div></div>'
            '<div class="row"><div class="box %s">%s</div><div class="cans">%s</div></div>'
            '<div class="row"><div class="box sao">%s</div><div class="cans">%s%s</div></div>'
            '<div class="nhan">thiên bàn ↑ · địa bàn ↓%s</div>'
            '<div class="tt">%s</div></div>' % (
                " ban" if thong_tin.get("ban_menh") == p else "", mau, mau, _e(TEN_CUNG[p]),
                "cat" if than in THAN_CAT else "hung", _e(than), "".join(badges),
                lop_m if m else "binh", _e((m + " môn") if m else "(không môn)"), _can(tc, ""),
                _e(sao), _can(dc, "dia"), dong_an, " · ẩn can (tím)" if dong_an else "",
                "<br>".join(_e(x) for x in tt.get(p, []))))
    foot = thong_tin.get("chu_thich", "")
    return ('<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8"><title>%s</title><style>%s</style></head>'
            '<body><div class="wrap"><h1>%s</h1><div class="sub">%s</div>%s<div class="grid">%s</div>'
            '<div class="foot">%s</div></div></body></html>' % (
                _e(thong_tin.get("tieu_de", "Bàn Kỳ môn")), CSS, _e(thong_tin.get("tieu_de", "Bàn Kỳ môn")),
                _e(thong_tin.get("thoi_gian", "")),
                ('<div class="q">Hỏi: %s</div>' % _e(thong_tin["cau_hoi"])) if thong_tin.get("cau_hoi") else "",
                "".join(o), _e(foot)))


def _cung_chi(p):
    return {1: [0], 8: [1, 2], 3: [3], 4: [4, 5], 9: [6], 2: [7, 8], 7: [9], 6: [10, 11], 5: []}[p]


def ve(b, CAN, thong_tin, duong_dan_png):
    """Ghi file .html cạnh file .png; trả về (đường dẫn png hoặc None, đường dẫn html, thông báo)."""
    goc = os.path.splitext(duong_dan_png)[0]
    p_html = goc + ".html"
    with open(p_html, "w", encoding="utf-8") as f:
        f.write(lam_html(b, CAN, thong_tin))
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            br = pw.chromium.launch()
            pg = br.new_page(viewport={"width": 1080, "height": 900}, device_scale_factor=2)
            pg.goto("file://" + os.path.abspath(p_html))
            pg.locator(".wrap").screenshot(path=duong_dan_png)
            br.close()
        return duong_dan_png, p_html, "đã vẽ ảnh"
    except Exception as e:  # không có trình duyệt: vẫn có file HTML
        return None, p_html, "không vẽ được PNG (%s) – dùng file HTML" % type(e).__name__
