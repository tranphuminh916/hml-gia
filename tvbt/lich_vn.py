# -*- coding: utf-8 -*-
"""Âm lịch Việt Nam (múi giờ UTC+7) theo thuật toán của Hồ Ngọc Đức.
Âm lịch Việt Nam và Trung Quốc lệch nhau ở một số tháng (ví dụ Tết 1985, 2007)
vì điểm sóc (trăng mới) được tính theo kinh tuyến 105°E thay vì 120°E."""
import math

INT = math.floor  # giống Math.floor trong bản gốc (INT() của Python cắt về 0, sai với số âm)

PI = math.pi


def jd_from_date(dd, mm, yy):
    a = (14 - mm) // 12
    y = yy + 4800 - a
    m = mm + 12 * a - 3
    jd = dd + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    if jd < 2299161:
        jd = dd + (153 * m + 2) // 5 + 365 * y + y // 4 - 32083
    return jd


def jd_to_date(jd):
    if jd > 2299160:
        a = jd + 32044
        b = (4 * a + 3) // 146097
        c = a - (b * 146097) // 4
    else:
        b = 0
        c = jd + 32082
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = b * 100 + d - 4800 + m // 10
    return day, month, year


def _new_moon(k):
    T = k / 1236.85
    T2 = T * T
    T3 = T2 * T
    dr = PI / 180
    Jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * T2 - 0.000000155 * T3
    Jd1 += 0.00033 * math.sin((166.56 + 132.87 * T - 0.009173 * T2) * dr)
    M = 359.2242 + 29.10535608 * k - 0.0000333 * T2 - 0.00000347 * T3
    Mpr = 306.0253 + 385.81691806 * k + 0.0107306 * T2 + 0.00001236 * T3
    F = 21.2964 + 390.67050646 * k - 0.0016528 * T2 - 0.00000239 * T3
    C1 = (0.1734 - 0.000393 * T) * math.sin(M * dr) + 0.0021 * math.sin(2 * dr * M)
    C1 = C1 - 0.4068 * math.sin(Mpr * dr) + 0.0161 * math.sin(dr * 2 * Mpr)
    C1 = C1 - 0.0004 * math.sin(dr * 3 * Mpr)
    C1 = C1 + 0.0104 * math.sin(dr * 2 * F) - 0.0051 * math.sin(dr * (M + Mpr))
    C1 = C1 - 0.0074 * math.sin(dr * (M - Mpr)) + 0.0004 * math.sin(dr * (2 * F + M))
    C1 = C1 - 0.0004 * math.sin(dr * (2 * F - M)) - 0.0006 * math.sin(dr * (2 * F + Mpr))
    C1 = C1 + 0.0010 * math.sin(dr * (2 * F - Mpr)) + 0.0005 * math.sin(dr * (2 * Mpr + M))
    if T < -11:
        deltat = 0.001 + 0.000839 * T + 0.0002261 * T2 - 0.00000845 * T3 - 0.000000081 * T * T3
    else:
        deltat = -0.000278 + 0.000265 * T + 0.000262 * T2
    return Jd1 + C1 - deltat


def _sun_longitude(jdn):
    T = (jdn - 2451545.0) / 36525
    T2 = T * T
    dr = PI / 180
    M = 357.52910 + 35999.05030 * T - 0.0001559 * T2 - 0.00000048 * T * T2
    L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2
    DL = (1.914600 - 0.004817 * T - 0.000014 * T2) * math.sin(dr * M)
    DL = DL + (0.019993 - 0.000101 * T) * math.sin(dr * 2 * M) + 0.000290 * math.sin(dr * 3 * M)
    L = (L0 + DL) * dr
    L = L - PI * 2 * INT(L / (PI * 2))
    if L < 0:
        L += 2 * PI
    return L


def _get_sun_longitude(day_number, tz):
    return INT(_sun_longitude(day_number - 0.5 - tz / 24) / PI * 6)


def _get_new_moon_day(k, tz):
    return INT(_new_moon(k) + 0.5 + tz / 24)


def _get_lunar_month11(yy, tz):
    off = jd_from_date(31, 12, yy) - 2415021
    k = INT(off / 29.530588853)
    nm = _get_new_moon_day(k, tz)
    if _get_sun_longitude(nm, tz) >= 9:
        nm = _get_new_moon_day(k - 1, tz)
    return nm


def _get_leap_month_offset(a11, tz):
    k = INT((a11 - 2415021.076998695) / 29.530588853 + 0.5)
    last = 0
    i = 1
    arc = _get_sun_longitude(_get_new_moon_day(k + i, tz), tz)
    while True:
        last = arc
        i += 1
        arc = _get_sun_longitude(_get_new_moon_day(k + i, tz), tz)
        if not (arc != last and i < 14):
            break
    return i - 1


def solar_to_lunar(dd, mm, yy, tz=7):
    """Trả về (ngày âm, tháng âm, năm âm, nhuận True/False)."""
    day_number = jd_from_date(dd, mm, yy)
    k = INT((day_number - 2415021.076998695) / 29.530588853)
    month_start = _get_new_moon_day(k + 1, tz)
    while month_start > day_number:  # bản gốc chỉ lùi 1 lần -> ra "ngày 0" vài trường hợp (vd 07/05/2054)
        k -= 1
        month_start = _get_new_moon_day(k + 1, tz)
    a11 = _get_lunar_month11(yy, tz)
    b11 = a11
    if a11 >= month_start:
        lunar_year = yy
        a11 = _get_lunar_month11(yy - 1, tz)
    else:
        lunar_year = yy + 1
        b11 = _get_lunar_month11(yy + 1, tz)
    lunar_day = day_number - month_start + 1
    diff = INT((month_start - a11) / 29)
    lunar_leap = False
    lunar_month = diff + 11
    if b11 - a11 > 365:
        leap_month_diff = _get_leap_month_offset(a11, tz)
        if diff >= leap_month_diff:
            lunar_month = diff + 10
            if diff == leap_month_diff:
                lunar_leap = True
    if lunar_month > 12:
        lunar_month -= 12
    if lunar_month >= 11 and diff < 4:
        lunar_year -= 1
    return lunar_day, lunar_month, lunar_year, lunar_leap


def lunar_to_solar(lunar_day, lunar_month, lunar_year, lunar_leap=False, tz=7):
    """Trả về (ngày, tháng, năm) dương lịch; None nếu tháng nhuận không tồn tại."""
    if lunar_month < 11:
        a11 = _get_lunar_month11(lunar_year - 1, tz)
        b11 = _get_lunar_month11(lunar_year, tz)
    else:
        a11 = _get_lunar_month11(lunar_year, tz)
        b11 = _get_lunar_month11(lunar_year + 1, tz)
    k = INT(0.5 + (a11 - 2415021.076998695) / 29.530588853)
    off = lunar_month - 11
    if off < 0:
        off += 12
    if b11 - a11 > 365:
        leap_off = _get_leap_month_offset(a11, tz)
        leap_month = leap_off - 2
        if leap_month < 0:
            leap_month += 12
        if lunar_leap and lunar_month != leap_month:
            return None
        elif lunar_leap or off >= leap_off:
            off += 1
    elif lunar_leap:
        return None
    month_start = _get_new_moon_day(k + off, tz)
    return jd_to_date(month_start + lunar_day - 1)
