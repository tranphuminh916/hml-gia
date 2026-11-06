# -*- coding: utf-8 -*-
"""nc.py - CLI chung của các skill bổ sung (dùng kèm tu-vi-bat-tu-phong-thuy-v2).

Cách dùng: python3 tvbt/nc.py <lệnh> [tham số]   (xem: python3 tvbt/nc.py <lệnh> --help)
Các lệnh: ngay, vuongsuy, anhtuvi, anhbattu, vanthe, hoptac, luunhat, kiembai,
          luchao, huyenkhong, lucnham2, cachcuc, hoichan, hannam, tuoivn, tukiem
"""
import argparse
import datetime as dt
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MODULE = ["ngochap", "vuongsuy", "anh", "hoptac", "luunhat", "kiembai",
          "luchao", "huyenkhong2", "lucnham2", "cachcuc_tv", "hoichan", "hannam", "tuoivn"]


def them_tham_so_sinh(p, gioi_bat_buoc=False):
    """Tham số ngày giờ (sinh hoặc hỏi việc), cùng tên với tvbt.py."""
    p.add_argument("--ngay", help="YYYY-MM-DD (dương lịch; thêm --am nếu là âm lịch); bỏ trống = hôm nay")
    p.add_argument("--gio", help="HH:MM giờ đồng hồ")
    p.add_argument("--gioi", choices=["nam", "nu"], required=gioi_bat_buoc)
    p.add_argument("--noi", help="nơi sinh / nơi đang ở (tỉnh, thành Việt Nam)")
    p.add_argument("--kinhdo", type=float)
    p.add_argument("--mien", choices=["bac", "nam"])
    p.add_argument("--utc", type=float)
    p.add_argument("--am", action="store_true")
    p.add_argument("--nhuan", action="store_true")
    p.add_argument("--lich-tz", type=int, choices=[7, 8])
    p.add_argument("--gio-dong-ho", action="store_true")
    p.add_argument("--ty", type=int, default=1, choices=[1, 2])


def thoi_diem(a, can_gio=True, mac_dinh_bay_gio=True):
    """Đổi Namespace thành ThongTinSinh của tvbt (giờ mặt trời thực, tiết khí...).
    Thiếu ngày thì lấy bây giờ (giờ Việt Nam); thiếu giới tính thì tạm 'nam'."""
    import tvbt as B
    if not a.ngay and mac_dinh_bay_gio:
        now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None) + dt.timedelta(hours=7)
        a.ngay = now.strftime("%Y-%m-%d")
        a.gio = a.gio or now.strftime("%H:%M")
    if can_gio and not a.gio:
        raise SystemExit("LỖI: cần giờ (--gio HH:MM).")
    g0 = a.gioi
    a.gioi = a.gioi or "nam"
    tt = B.doc_dau_vao(a)
    a.gioi = g0
    tt.gioi_that = g0
    if not a.noi and a.kinhdo is None:
        tt.canh_bao = [c for c in tt.canh_bao if not c.startswith("Không có nơi sinh")]
        tt.noi = "Hà Nội (mặc định)"
    return tt


def main():
    p = argparse.ArgumentParser(description="Các skill bổ sung cho tvbt.py (tu-vi-nang-cao, cach-cuc-tu-vi, luc-hao-boc-dich, lucnham-huyenkhong-nang-cao)")
    sub = p.add_subparsers(dest="lenh", required=True)
    mods = {}
    for ten in MODULE:
        try:
            m = importlib.import_module(ten)
        except ImportError as e:
            if ten in str(e):
                continue            # module chưa được trích
            raise
        m.them_lenh(sub)
        mods[ten] = m
    sp = sub.add_parser("tukiem", help="chạy tự kiểm tra của mọi module")
    sp.set_defaults(_chay=lambda a: tu_kiem_tat_ca(mods))
    a = p.parse_args()
    a._chay(a)


def tu_kiem_tat_ca(mods):
    loi = []
    for ten, m in mods.items():
        try:
            r = m.tu_kiem()
        except Exception as e:      # noqa: BLE001
            r = ["%s: ngoại lệ %r" % (ten, e)]
        print("- %-12s %s" % (ten, "ĐẠT" if not r else "LỖI (%d)" % len(r)))
        loi += ["%s: %s" % (ten, x) for x in r]
    for x in loi[:40]:
        print("  " + x)
    print("TỰ KIỂM TRA NÂNG CAO:", "ĐẠT" if not loi else "LỖI")
    if loi:
        sys.exit(1)


if __name__ == "__main__":
    main()
