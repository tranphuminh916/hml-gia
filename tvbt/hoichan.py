# -*- coding: utf-8 -*-
"""hoichan.py - Hội chẩn ba môn cùng một thời điểm hỏi việc: Lục hào (lập theo thời gian, hoặc theo đồng xu/số hào
nếu truyền vào), Mai hoa dịch số, Đại Lục Nhâm (kèm phần bổ sung thần sát, Tất pháp phú).
Claude tự lập bảng đồng thuận (+1/0/−1 mỗi môn) theo hướng dẫn trong SKILL.md.
Lệnh: nc.py hoichan --viec taichinh [--ngay ... --gio ... --noi ...] [--xu ... | --hao ...] [--nam-sinh 1990 --gioi nam]
"""
import argparse

import tvbt as B

# việc của Lục hào -> việc của Lục Nhâm bổ sung
DOI_VIEC = {"chung": "chung", "taichinh": "tien", "congviec": "quan", "honnhan": "honnhan", "suckhoe": "benh",
            "kientung": "kien", "dixa": "xuathanh", "timdo": "matdo", "thicu": "thi", "giayto": "hopdong",
            "concai": "chung", "anhem": "chung"}


def them_lenh(sub):
    import nc
    p = sub.add_parser("hoichan", help="hội chẩn Lục hào + Mai hoa + Lục Nhâm cùng một thời điểm")
    nc.them_tham_so_sinh(p)
    p.add_argument("--viec", default="chung", choices=list(DOI_VIEC))
    p.add_argument("--xu", nargs="+")
    p.add_argument("--xu-dao", action="store_true")
    p.add_argument("--hao", nargs="+")
    p.add_argument("--nam-sinh", type=int)
    p.set_defaults(_chay=chay)


def _tham_so_chung(a, tt):
    """Truyền ngày DƯƠNG đã đổi (tránh lệch khi người dùng nhập ngày âm) và cách tính giờ Tý."""
    ds = ["--ngay", tt.dong_ho.strftime("%Y-%m-%d"), "--gio", tt.dong_ho.strftime("%H:%M"), "--ty", str(a.ty)]
    for ten in ("noi", "gioi", "mien", "lich_tz"):
        v = getattr(a, ten)
        if v:
            ds += ["--" + ten.replace("_", "-"), str(v)]
    for ten in ("kinhdo", "utc"):
        v = getattr(a, ten)
        if v is not None:
            ds += ["--" + ten, str(v)]
    if a.gio_dong_ho:
        ds.append("--gio-dong-ho")
    return ds


def chay(a):
    import nc
    import luchao
    tt = nc.thoi_diem(a)                 # điền ngày giờ hiện tại nếu thiếu
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="lenh")
    luchao.them_lenh(sub)
    try:
        import lucnham2
        lucnham2.them_lenh(sub)
    except ImportError:
        lucnham2 = None
    chung = _tham_so_chung(a, tt)
    print("HỘI CHẨN BA MÔN – cùng thời điểm %s (%s)" % (tt.dong_ho.strftime("%H:%M %d/%m/%Y"), tt.noi))
    print("=" * 60)
    print("MÔN 1 – LỤC HÀO")
    them = []
    if a.xu:
        them = ["--xu"] + a.xu + (["--xu-dao"] if a.xu_dao else [])
    elif a.hao:
        them = ["--hao"] + a.hao
    a1 = p.parse_args(["luchao"] + chung + ["--viec", a.viec] + them)
    a1._chay(a1)
    print("=" * 60)
    print("MÔN 2 – MAI HOA DỊCH SỐ (lập theo thời gian)")
    B.mai_hoa(tt, None)
    print("=" * 60)
    print("MÔN 3 – ĐẠI LỤC NHÂM")
    if lucnham2:
        extra = ["--viec", DOI_VIEC[a.viec]] + (["--nam-sinh", str(a.nam_sinh)] if a.nam_sinh else [])
        a3 = p.parse_args(["lucnham2"] + chung + extra)
        a3._chay(a3)
    else:
        B.luc_nham(tt)
    print("=" * 60)
    print("BẢNG ĐỒNG THUẬN (Claude tự điền theo SKILL.md, mục Hội chẩn ba môn): | Môn | Kết luận (+1 / 0 / −1) | Căn cứ chính |")


def tu_kiem():
    loi = []
    if set(DOI_VIEC) != {"chung", "taichinh", "congviec", "honnhan", "suckhoe", "kientung", "dixa", "timdo",
                         "thicu", "giayto", "concai", "anhem"}:
        loi.append("bảng đổi việc thiếu")
    import luchao
    if not set(DOI_VIEC) <= set(luchao.VIEC):
        loi.append("việc không khớp Lục hào")
    try:
        import lucnham2
        if not set(DOI_VIEC.values()) <= set(lucnham2.VIEC):
            loi.append("việc không khớp Lục Nhâm bổ sung")
    except ImportError:
        pass                     # chưa cài skill Lục Nhâm bổ sung: hội chẩn dùng Lục Nhâm của v2
    # ngày âm phải được đổi sang dương trước khi truyền cho các môn
    import nc
    ns = argparse.Namespace(ngay="2026-09-20", gio="10:00", gioi=None, noi=None, kinhdo=None, mien=None, utc=None,
                            am=True, nhuan=False, lich_tz=None, gio_dong_ho=False, ty=1)
    tt = nc.thoi_diem(ns)
    if "--am" in _tham_so_chung(ns, tt) or _tham_so_chung(ns, tt)[1] != "2026-10-29":
        loi.append("hội chẩn không đổi ngày âm sang dương: %s" % _tham_so_chung(ns, tt)[:2])
    return loi
