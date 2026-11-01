# Chạy lệnh của bộ tvbt trong trình duyệt (Pyodide) và lấy chữ in ra.
import contextlib, io, os, sys, traceback
sys.path.insert(0, "/home/pyodide/tvbt")
os.chdir("/home/pyodide")


def run(prog, args):
    import importlib
    args = [str(x) for x in args]
    sys.argv = [prog + ".py"] + args
    buf = io.StringIO()
    code = 0
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        try:
            m = importlib.import_module(prog)
            m.main()
        except SystemExit as e:
            if isinstance(e.code, str):
                print(e.code)
                code = 1
            else:
                code = e.code or 0
        except Exception:
            traceback.print_exc()
            code = 1
    return [code, buf.getvalue()]


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def thong_tin(ngay, gio, gioi, noi, am=False, nhuan=False, kinhdo=None):
    """Thông tin nhanh của một người: âm lịch, năm âm lịch, năm tính từ Lập Xuân, can chi năm."""
    import argparse
    import tvbt as B
    a = argparse.Namespace(ngay=ngay, gio=gio or None, gioi=gioi or "nam", noi=noi or None,
                           kinhdo=kinhdo, mien=None, utc=None, am=bool(am), nhuan=bool(nhuan),
                           lich_tz=None, gio_dong_ho=False, ty=1)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            tt = B.doc_dau_vao(a)
            d, m, y, nh = B.duong_sang_am(tt.t_dia_phuong.date() if tt.co_gio else tt.dong_ho.date(), tt.lich_tz)
            ebk, eloc, tru = B.tu_tru(tt)
            gz = B._gz_so(ebk.getYear())
            nam_lx = tt.t_bk.year if (tt.t_bk.year - 4) % 60 == gz else tt.t_bk.year - 1
            duong = tt.dong_ho.strftime("%Y-%m-%d")
        return {"ok": True, "am": [d, m, y, bool(nh)], "nam_am": y, "nam_lx": nam_lx,
                "can_chi_nam": B.vn(ebk.getYear()), "duong": duong,
                "canh_bao": list(tt.canh_bao)}
    except SystemExit as e:
        return {"ok": False, "loi": str(e.code) if e.code else buf.getvalue()}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "loi": "%s: %s" % (type(e).__name__, e)}


def kiem_noi(noi):
    import tvbt as B
    kd, mn = B.tra_noi_sinh(noi or "")
    return {"kinhdo": kd, "mien_nam": bool(mn)}


def gio_sinh(s):
    """Dò giờ sinh: vào/ra đều là chuỗi JSON (xem tvbt/giosinh.py)."""
    import giosinh
    return giosinh.buoc_json(s)
