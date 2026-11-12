# -*- coding: utf-8 -*-
"""ngochap.py - Chọn ngày đầy đủ: việc nên/kiêng theo ngày và theo giờ, cát thần – hung sát trực nhật
(dữ liệu Hiệp Kỷ Biện Phương Thư của lunar-python), hướng Hỷ thần / Tài thần / Phúc thần / Quý nhân,
Thai thần, Bành Tổ bách kỵ; gộp với tiêu chí lịch Việt Nam của v2 (Hoàng đạo tháng âm, Trực, 28 Tú,
Tam Nương, Nguyệt Kỵ, Dương Công, xung tuổi) và chấm theo thang 100 điểm, chia 3 nhóm.
Lệnh: python3 tvbt/nc.py ngay --tu YYYY-MM-DD --den YYYY-MM-DD --viec khaitruong --tuoi "An:1990:Thủy+Kim"
"""
import datetime as dt

from lunar_python import Solar

import chonngay as CN
import toason as TS

# ---------------------------------------------------------------- Từ điển
VIEC_HV = {
    "上梁": "gác đòn nóc", "乘船": "đi thuyền", "习艺": "học nghề", "交易": "giao dịch, mua bán",
    "伐木": "chặt cây", "会亲友": "gặp họ hàng bạn bè", "作梁": "làm xà", "作灶": "làm bếp", "修坟": "sửa mộ",
    "修造": "xây sửa nhà", "修饰垣墙": "sửa sang tường rào", "入学": "nhập học", "入宅": "nhập trạch (vào nhà mới)",
    "入殓": "khâm liệm", "冠笄": "lễ trưởng thành", "出火": "xuất hỏa (dời bếp, bàn thờ tạm)", "出行": "xuất hành",
    "出货财": "xuất hàng, chi tiền", "分居": "ra ở riêng", "割蜜": "lấy mật ong", "动土": "động thổ",
    "取渔": "đánh cá", "合寿木": "đóng thọ mộc", "合帐": "may màn trướng", "合脊": "lợp nóc", "启钻": "bốc mộ, cải táng",
    "坏垣": "phá tường", "塑绘": "tô tượng, vẽ tranh", "塞穴": "lấp hang lỗ", "嫁娶": "cưới gả",
    "安床": "kê giường", "安机械": "lắp máy móc", "安碓磑": "đặt cối giã, cối xay", "安葬": "an táng",
    "安门": "lắp cửa", "安香": "an hương (lập bàn thờ)", "定磉": "đặt chân cột", "平治道涂": "sửa đường",
    "开仓": "mở kho", "开光": "khai quang (điểm nhãn tượng)", "开厕": "làm nhà vệ sinh", "开市": "khai trương",
    "开柱眼": "đục lỗ cột", "开池": "đào ao", "开渠": "đào mương", "开生坟": "làm sinh phần",
    "归岫": "quy tụ", "成服": "mặc đồ tang", "扫舍": "quét dọn nhà", "拆卸": "tháo dỡ", "挂匾": "treo biển hiệu",
    "捕捉": "săn bắt", "掘井": "đào giếng", "探病": "thăm người ốm", "放水": "tháo nước", "教牛马": "dạy trâu ngựa",
    "整手足甲": "cắt móng tay chân", "斋醮": "làm chay cúng tế", "断蚁": "diệt mối kiến", "普渡": "cúng phổ độ",
    "架马": "dựng giàn", "栽种": "trồng trọt", "求医": "tìm thầy chữa bệnh", "求嗣": "cầu con", "求财": "cầu tài",
    "沐浴": "tắm gội", "治病": "chữa bệnh", "牧养": "chăn nuôi", "理发": "cắt tóc", "畋猎": "săn bắn",
    "盖屋": "lợp nhà", "破土": "phá thổ (đào huyệt)", "破屋": "phá nhà", "祈福": "cầu phúc", "祭祀": "cúng tế",
    "移徙": "chuyển nhà", "移柩": "di quan", "立券": "ký khế ước, hợp đồng", "立碑": "dựng bia", "竖柱": "dựng cột",
    "筑堤": "đắp đê", "纳婿": "đón rể", "纳畜": "nhận gia súc", "纳财": "thu tiền, nhập hàng", "纳采": "dạm ngõ, ăn hỏi",
    "经络": "se tơ dệt vải", "结网": "đan lưới", "置产": "mua nhà đất", "行丧": "đưa tang", "补垣": "sửa tường",
    "裁衣": "cắt may", "见贵": "gặp người có chức quyền", "解除": "giải trừ, tẩy uế", "订婚": "đính hôn",
    "订盟": "đính ước, kết giao", "词讼": "kiện tụng", "诸事不宜": "MỌI VIỆC ĐỀU KHÔNG NÊN", "谢土": "tạ thổ",
    "赴任": "nhậm chức", "起基": "khởi móng", "进人口": "nhận người (thuê người, nhận nuôi)", "造仓": "làm kho",
    "造庙": "xây chùa miếu", "造桥": "làm cầu", "造畜稠": "làm chuồng trại", "造船": "đóng thuyền",
    "造车器": "đóng xe cộ", "酬神": "tạ thần", "针灸": "châm cứu", "问名": "vấn danh (lễ hỏi)", "除服": "bỏ tang",
    "雇佣": "thuê người", "雕刻": "chạm khắc", "馀事勿取": "việc khác không nên làm", "修门": "sửa cửa", "归宁": "về thăm nhà (con gái về nhà mẹ)", "无": "",
}
CAT_THAN = {
    "三合": "Tam Hợp", "不将": "Bất Tương", "临日": "Lâm Nhật", "五合": "Ngũ Hợp", "五富": "Ngũ Phú",
    "六仪": "Lục Nghi", "六合": "Lục Hợp", "司命": "Tư Mệnh", "吉期": "Cát Kỳ", "四相": "Tứ Tướng",
    "圣心": "Thánh Tâm", "天仓": "Thiên Thương", "天医": "Thiên Y", "天后": "Thiên Hậu", "天喜": "Thiên Hỷ",
    "天巫": "Thiên Vu", "天德": "Thiên Đức", "天德合": "Thiên Đức Hợp", "天恩": "Thiên Ân", "天愿": "Thiên Nguyện",
    "天赦": "Thiên Xá", "天马": "Thiên Mã", "守日": "Thủ Nhật", "官日": "Quan Nhật", "宝光": "Bảo Quang",
    "敬安": "Kính An", "时德": "Thời Đức", "时阳": "Thời Dương", "时阴": "Thời Âm", "明堂": "Minh Đường",
    "普护": "Phổ Hộ", "月德": "Nguyệt Đức", "月德合": "Nguyệt Đức Hợp", "月恩": "Nguyệt Ân", "月空": "Nguyệt Không",
    "母仓": "Mẫu Thương", "民日": "Dân Nhật", "玉堂": "Ngọc Đường", "玉宇": "Ngọc Vũ", "王日": "Vương Nhật",
    "生气": "Sinh Khí", "益后": "Ích Hậu", "相日": "Tướng Nhật", "福德": "Phúc Đức", "福生": "Phúc Sinh",
    "续世": "Tục Thế", "要安": "Yếu An", "解神": "Giải Thần", "解除": "Giải Trừ", "金匮": "Kim Quỹ",
    "金堂": "Kim Đường", "阳德": "Dương Đức", "阴德": "Âm Đức", "阴神": "Âm Thần", "除神": "Trừ Thần",
    "青龙": "Thanh Long", "驿马": "Dịch Mã", "鸣吠": "Minh Phệ", "鸣吠对": "Minh Phệ Đối", "天符": "Thiên Phù", "无": "",
}
HUNG_SAT = {
    "七鸟": "Thất Điểu", "三丧": "Tam Tang", "三阴": "Tam Âm", "九坎": "Cửu Khảm", "九焦": "Cửu Tiêu",
    "九空": "Cửu Không", "九虎": "Cửu Hổ", "了戾": "Liễu Lệ", "五墓": "Ngũ Mộ", "五离": "Ngũ Ly", "五虚": "Ngũ Hư",
    "元武": "Huyền Vũ", "八专": "Bát Chuyên", "八风": "Bát Phong", "八龙": "Bát Long", "六蛇": "Lục Xà",
    "劫煞": "Kiếp Sát", "勾陈": "Câu Trận", "厌对": "Yếm Đối", "咸池": "Hàm Trì", "四击": "Tứ Kích",
    "四废": "Tứ Phế", "四忌": "Tứ Kỵ", "四离": "Tứ Ly", "四穷": "Tứ Cùng", "四耗": "Tứ Hao", "土府": "Thổ Phủ",
    "土符": "Thổ Phù", "地囊": "Địa Nang", "地火": "Địa Hỏa", "复日": "Phục Nhật", "大会": "Đại Hội",
    "大时": "Đại Thời", "大煞": "Đại Sát", "大耗": "Đại Hao", "大败": "Đại Bại", "天刑": "Thiên Hình",
    "天吏": "Thiên Lại", "天火": "Thiên Hỏa", "天牢": "Thiên Lao", "天狗": "Thiên Cẩu", "天罡": "Thiên Cương",
    "天贼": "Thiên Tặc", "孤辰": "Cô Thần", "孤阳": "Cô Dương", "小会": "Tiểu Hội", "小时": "Tiểu Thời",
    "小耗": "Tiểu Hao", "岁薄": "Tuế Bạc", "归忌": "Quy Kỵ", "往亡": "Vãng Vong", "成日": "Thành Nhật",
    "招摇": "Chiêu Dao", "月刑": "Nguyệt Hình", "月厌": "Nguyệt Yếm", "月害": "Nguyệt Hại", "月建": "Nguyệt Kiến",
    "月煞": "Nguyệt Sát", "月破": "Nguyệt Phá", "月虚": "Nguyệt Hư", "朱雀": "Chu Tước", "死气": "Tử Khí",
    "死神": "Tử Thần", "河魁": "Hà Khôi", "游祸": "Du Họa", "灾煞": "Tai Sát", "白虎": "Bạch Hổ",
    "纯阳": "Thuần Dương", "绝阴": "Tuyệt Âm", "致死": "Trí Tử", "血忌": "Huyết Kỵ", "血支": "Huyết Chi",
    "行狠": "Hành Ngận", "触水龙": "Xúc Thủy Long", "逐阵": "Trục Trận", "重日": "Trùng Nhật", "阳错": "Dương Thác",
    "阳错阴冲": "Dương Thác Âm Xung", "阴位": "Âm Vị", "阴道冲阳": "Âm Đạo Xung Dương", "阴错": "Âm Thác",
    "阴阳交破": "Âm Dương Giao Phá", "阴阳俱错": "Âm Dương Câu Thác", "阴阳击冲": "Âm Dương Kích Xung", "七符": "Thất Phù", "单阴": "Đơn Âm",
    "大退": "Đại Thoái", "纯阴": "Thuần Âm", "绝阳": "Tuyệt Dương", "阳破阴冲": "Dương Phá Âm Xung", "鬼哭": "Quỷ Khốc", "无": "",
}
# Cát thần lớn (theo Hiệp Kỷ: các sao giải được nhiều hung sát) và hung sát nặng
CAT_LON = {"天德", "月德", "天德合", "月德合", "天赦", "天愿", "天恩", "月恩", "母仓", "四相", "时德",
           "三合", "六合", "五合", "天喜", "天医", "解神", "生气", "王日", "官日", "守日", "相日", "民日"}
HUNG_NANG = {"月破", "大耗", "四废", "四离", "五离", "四穷", "四耗", "往亡", "归忌", "天贼", "月厌", "大时",
             "大败", "月煞", "劫煞", "灾煞", "天罡", "河魁", "死神", "致死", "重日", "复日", "九空", "天火", "地火",
             "阴阳交破", "阴阳俱错", "阴阳击冲", "四击", "四忌"}
HUONG = {"东北": "Đông Bắc", "东南": "Đông Nam", "正东": "Đông", "正北": "Bắc", "正南": "Nam", "正西": "Tây",
         "西北": "Tây Bắc", "西南": "Tây Nam"}
_THAI = [("占大门", "cổng lớn"), ("占房床", "giường phòng"), ("占碓磨", "cối xay"), ("占门", "cửa, "),
         ("仓库", "kho, "), ("厨灶", "bếp, "), ("房床", "giường phòng, "), ("碓磨", "cối xay, "),
         ("厕", "nhà vệ sinh"), ("床", "giường"), ("栖", "chuồng"), ("炉", "lò"), ("碓", "cối giã"), ("门", "cửa"),
         ("房内", "trong phòng phía "), ("外", "ngoài nhà phía "), ("中", "giữa")]
BANH_TO = {
    "甲": "Giáp không mở kho (hao của)", "乙": "Ất không trồng cây (khó lên)", "丙": "Bính không sửa bếp (gặp tai ương)",
    "丁": "Đinh không cạo đầu (sinh mụn nhọt)", "戊": "Mậu không nhận ruộng (chủ ruộng không lành)",
    "己": "Kỷ không hủy khế ước (hai bên cùng thiệt)", "庚": "Canh không se tơ dệt vải (khung cửi bỏ không)",
    "辛": "Tân không làm tương (chủ không được nếm)", "壬": "Nhâm không tháo nước (khó phòng giữ)",
    "癸": "Quý không kiện tụng (lý yếu, đối phương mạnh)",
    "子": "Tý không xem bói (tự chuốc họa)", "丑": "Sửu không đội mũ nhậm chức (khó về quê)",
    "寅": "Dần không cúng tế (thần không hưởng)", "卯": "Mão không đào giếng (nước không ngọt)",
    "辰": "Thìn không khóc lóc (e trùng tang)", "巳": "Tỵ không đi xa (tiền của hao)",
    "午": "Ngọ không lợp nhà (phải làm lại)", "未": "Mùi không uống thuốc (độc vào ruột)",
    "申": "Thân không kê giường (bất an)", "酉": "Dậu không tiếp khách (say sưa sinh chuyện)",
    "戌": "Tuất không ăn thịt chó (sinh chuyện lạ)", "亥": "Hợi không cưới gả (bất lợi chú rể)",
}
QUE_HUONG = {"坎": "Bắc", "坤": "Tây Nam", "震": "Đông", "巽": "Đông Nam", "乾": "Tây Bắc", "兑": "Tây",
             "艮": "Đông Bắc", "离": "Nam", "中": "Giữa"}

# Việc: (tên, từ khóa chính, từ khóa phụ, trực tốt, trực kỵ, can chi Bành Tổ cần tránh)
VIEC = {
    "chung": ("Việc chung", set(), set(), CN.VIEC["chung"][1], CN.VIEC["chung"][2], ""),
    "cuoi": ("Cưới hỏi", {"嫁娶"}, {"纳采", "订婚", "订盟", "问名", "纳婿"}, CN.VIEC["cuoi"][1], CN.VIEC["cuoi"][2], "亥"),
    "anhoi": ("Ăn hỏi, dạm ngõ", {"纳采", "订婚"}, {"订盟", "问名", "嫁娶"}, CN.VIEC["cuoi"][1], CN.VIEC["cuoi"][2], ""),
    "dongtho": ("Động thổ, xây sửa", {"动土", "修造"}, {"起基", "竖柱", "上梁", "定磉", "盖屋"},
                CN.VIEC["dongtho"][1], CN.VIEC["dongtho"][2], ""),
    "khaitruong": ("Khai trương", {"开市"}, {"交易", "立券", "纳财", "挂匾"},
                   CN.VIEC["khaitruong"][1], CN.VIEC["khaitruong"][2], "甲"),
    "kyhopdong": ("Ký hợp đồng, giao dịch", {"立券", "交易"}, {"订盟", "纳财", "开市"},
                  CN.VIEC["khaitruong"][1], CN.VIEC["khaitruong"][2], "己"),
    "xuathanh": ("Xuất hành, đi xa", {"出行"}, {"乘船", "会亲友"}, CN.VIEC["xuathanh"][1], CN.VIEC["xuathanh"][2], "巳"),
    "nhaptrach": ("Nhập trạch, chuyển nhà", {"入宅", "移徙"}, {"安香", "安床", "作灶"},
                  CN.VIEC["nhaptrach"][1], CN.VIEC["nhaptrach"][2], ""),
    "muanha": ("Mua nhà đất", {"置产"}, {"立券", "交易"}, {"Thành", "Định", "Mãn", "Khai"}, {"Phá", "Nguy", "Bế"}, "戊"),
    "nhamchuc": ("Nhậm chức, nhận việc", {"赴任"}, {"见贵", "出行"}, {"Kiến", "Thành", "Khai", "Định"}, {"Phá", "Nguy", "Bế"}, "丑"),
    "nhapkho": ("Nhập hàng, thu tiền", {"纳财"}, {"开仓", "交易", "立券"}, {"Thu", "Mãn", "Thành", "Khai"}, {"Phá", "Nguy"}, ""),
    "xuathang": ("Xuất hàng, mở kho", {"出货财", "开仓"}, {"交易", "开市"}, {"Khai", "Mãn", "Thành"}, {"Phá", "Nguy", "Bế", "Thu"}, "甲"),
    "chuabenh": ("Chữa bệnh, phẫu thuật", {"求医", "治病"}, {"针灸"}, {"Trừ", "Khai", "Thành"}, {"Kiến", "Mãn", "Bình"}, "未"),
    "kientung": ("Kiện tụng", {"词讼"}, set(), {"Chấp", "Nguy", "Thành"}, set(), "癸"),
    "antang": ("An táng", {"安葬"}, {"破土", "行丧"}, {"Trừ", "Chấp", "Bình"}, {"Kiến", "Mãn", "Định"}, ""),
    "lapbantho": ("Lập bàn thờ, an hương", {"安香"}, {"祭祀", "祈福"}, {"Khai", "Thành", "Định", "Trừ"}, {"Phá", "Nguy"}, "寅"),
    "kegiuong": ("Kê giường", {"安床"}, set(), {"Định", "Thành", "Khai", "Mãn"}, {"Phá", "Nguy"}, "申"),
    "datbep": ("Làm bếp, đặt bếp", {"作灶"}, set(), {"Thành", "Khai", "Định"}, {"Phá", "Nguy"}, "丙"),
    "trongcay": ("Trồng trọt", {"栽种"}, set(), {"Thành", "Khai", "Bình", "Định"}, {"Phá", "Nguy"}, "乙"),
    "nhaphoc": ("Nhập học", {"入学"}, {"习艺"}, {"Thành", "Khai", "Kiến"}, {"Phá", "Nguy", "Bế"}, ""),
    "thuenguoi": ("Tuyển người, nhận người", {"进人口", "雇佣"}, set(), {"Thành", "Khai", "Thu"}, {"Phá", "Nguy"}, ""),
}
THU = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
HANH = ["Mộc", "Hỏa", "Thổ", "Kim", "Thủy"]
CHI_HANH = [4, 2, 0, 0, 2, 1, 1, 2, 3, 3, 2, 4]
TAM_HOP = [{8, 0, 4}, {11, 3, 7}, {2, 6, 10}, {5, 9, 1}]
LUC_HOP = {frozenset(x) for x in [(0, 1), (2, 11), (3, 10), (4, 9), (5, 8), (6, 7)]}


def _dich(ds, bang):
    return [bang[x] for x in ds if bang.get(x)]


def thai_than(s):
    r = s
    for a, b in _THAI:
        r = r.replace(a, b)
    for a, b in list(HUONG.items()) + [("东", "Đông"), ("西", "Tây"), ("南", "Nam"), ("北", "Bắc")]:
        r = r.replace(a, b)
    return r.replace(" ,", ",").replace(", ", ", ").strip(" ,")


def sua_than_sat(cat, hung, chi_thang, can_chi_ngay):
    """Sửa hai dòng nhập liệu sai trong bảng thần sát của lunar-python 1.4.8 (rà soát 11/2026; đối chiếu quy tắc
    Hiệp Kỷ – Hà Khôi tháng Hợi ở Dần, Nguyệt Yếm tháng Hợi ở Sửu / tháng Dậu ở Mão, Quy Kỵ tháng mạnh ở Sửu, Nguyệt
    Hình tháng Dậu ở Dậu – khớp thư viện cnlunar, và với các ngày cùng chi trong cùng tháng của chính lunar-python):
    - tháng Hợi ngày Kỷ Sửu: cả dòng cát thần / hung sát là của ngày khác (Hà Khôi, Thiên Lao, Lục Hợp...) → thay bằng
      bộ chung của các ngày Sửu tháng Hợi (Nguyệt Yếm, Địa Hỏa, Cửu Không, Đại Sát, Quy Kỵ | Thủ Nhật, Thiên Vu, Phúc
      Đức, Ngọc Vũ, Ngọc Đường) cộng Nguyệt Đức Hợp (can Kỷ, tháng Hợi);
    - tháng Mùi ngày Quý Dậu: dòng hung sát là của ngày khác (Kiếp Sát, Thiên Tặc, Ngũ Hư) → bộ chung của các ngày Dậu
      tháng Mùi (Tai Sát, Thiên Hỏa, Huyết Kỵ, Ngũ Ly, Câu Trận);
    - tháng Dậu ngày Kỷ Dậu: ghi Nguyệt Yếm thay cho Nguyệt Hình."""
    cat, hung = list(cat), list(hung)
    if chi_thang == "亥" and can_chi_ngay == "己丑" and "河魁" in hung:
        hung = ["月厌", "地火", "九空", "大煞", "归忌"]
        cat = ["月德合", "守日", "天巫", "福德", "玉宇", "玉堂"]
    if chi_thang == "未" and can_chi_ngay == "癸酉" and "劫煞" in hung:
        hung = ["灾煞", "天火", "血忌", "五离", "勾陈"]
    if chi_thang == "酉" and can_chi_ngay == "己酉" and "月厌" in hung:
        hung[hung.index("月厌")] = "月刑"
    return cat, hung


def du_lieu_ngay(d):
    l = Solar.fromYmd(d.year, d.month, d.day).getLunar()
    cat, hung = sua_than_sat(l.getDayJiShen(), l.getDayXiongSha(), l.getMonthZhi(), l.getDayInGanZhi())
    return dict(yi=l.getDayYi(), ji=l.getDayJi(), cat=cat, hung=hung,
                hy=HUONG[l.getDayPositionXiDesc()], tai=HUONG[l.getDayPositionCaiDesc()],
                phuc=HUONG[l.getDayPositionFuDesc()], qn_duong=HUONG[l.getDayPositionYangGuiDesc()],
                qn_am=HUONG[l.getDayPositionYinGuiDesc()], thai=thai_than(l.getDayPositionTai()),
                banh_to=[BANH_TO[l.getDayGan()], BANH_TO[l.getDayZhi()]], gan=l.getDayGan(), zhi=l.getDayZhi())


def gio_trong_ngay(d, chi):
    """Việc nên/kiêng của giờ (chi 0..11) trong ngày d (giờ Tý lấy 0h của chính ngày đó)."""
    h = (2 * chi) % 24
    l = Solar.fromYmdHms(d.year, d.month, d.day, h, 30, 0).getLunar()
    return l.getTimeYi(), l.getTimeJi()


def doc_tuoi(ds):
    """'Tên:năm[:Hành+Hành dụng[:Hành+Hành kỵ]]' -> list (tên, năm, can, chi, (set dụng, set kỵ))."""
    kq = []
    for x in ds:
        phan = x.split(":")
        phan += [""] * (4 - len(phan))
        if not phan[1]:
            ten, nam, dung, ky = phan[0], phan[0], "", ""
        else:
            ten, nam, dung, ky = phan[:4]
        try:
            y = int(nam)
        except ValueError:
            raise SystemExit("LỖI: --tuoi dạng Tên:năm[:Hành+Hành], vd An:1990:Thủy+Kim")
        hs = []
        for chuoi in (dung, ky):
            tap = set()
            for h in chuoi.replace(",", "+").split("+"):
                h = h.strip()
                if h:
                    if h not in HANH:
                        raise SystemExit("LỖI: hành phải là một trong %s" % ", ".join(HANH))
                    tap.add(HANH.index(h))
            hs.append(tap)
        kq.append((ten or nam, y, (y - 4) % 10, (y - 4) % 12, tuple(hs)))
    return kq


def cham(d, viec, nguoi, thu_ok=None, theo_tiet=False, toa=None, kieu_toa=None):
    """Trả về dict kết quả một ngày, kèm điểm thang 100 và lý do loại. toa = chỉ số tọa sơn (toason) nếu xét nhà/mộ,
    kieu_toa = duong | sua | am (mặc định theo việc)."""
    ten_viec, chinh, phu, truc_tot, truc_xau, bt_tranh = VIEC[viec]
    v2 = CN.xet_ngay(d, [(t, c, z) for t, _, c, z, _ in nguoi], "chung", theo_tiet)
    dl = du_lieu_ngay(d)
    yi, ji = set(dl["yi"]), set(dl["ji"])
    loai, ghi, canh_ngay = [], [], []
    # 1. Hợp việc (35): nên/kiêng 25 + trực 10
    if "诸事不宜" in yi or "诸事不宜" in ji:
        p1 = 0
        loai.append("mọi việc đều không nên")
    elif "馀事勿取" in yi and not (chinh & yi) and (chinh or not (yi - {"馀事勿取", "无"})):
        p1 = 0
        loai.append("lịch chỉ cho vài việc, việc khác không nên")
    elif chinh & ji:
        p1 = 0
        loai.append("kiêng " + ", ".join(VIEC_HV[x] for x in sorted(chinh & ji)))
    elif chinh & yi:
        p1 = 25
    elif phu & yi:
        p1 = 18
    elif not chinh:
        p1 = 15 if len(yi) >= len(ji) else 10
    else:
        p1 = 10
    if phu & ji and p1:
        p1 = max(p1 - 5, 0)
        ghi.append("kiêng " + ", ".join(VIEC_HV[x] for x in sorted(phu & ji)))
    p_truc = 10 if v2["truc"] in truc_tot else (0 if v2["truc"] in truc_xau else 5)
    # 2. Can chi ngày (25): hoàng đạo 10 + tú 5 + thần sát 10, trừ ngày kỵ dân gian
    p_hd = 10 if v2["hd"] else 0
    p_tu = 5 if v2["tu"] in CN.TU_CAT else 0
    n_cat = len(set(dl["cat"]) & CAT_LON)
    n_hung = len(set(dl["hung"]) & HUNG_NANG)
    p_ts = max(0, min(10, 5 + 2 * n_cat - 2 * n_hung))
    p2 = p_hd + p_tu + p_ts
    for k, tru in (("Tam Nương", 6), ("Nguyệt Kỵ", 6), ("Dương Công", 10)):
        if any(k in g for g in v2["ghi"]):
            p2 -= tru
            loai.append(k)
    p2 = max(p2, 0)
    if "月破" in dl["hung"]:
        loai.append("Nguyệt Phá")
    # Ngày kỵ theo tháng âm lịch Việt Nam (Thọ tử, Sát chủ, Vãng vong); Vãng vong xét cả bản tháng tiết (往亡 lunar-python)
    ky = list(v2["ky"])
    if "往亡" in dl["hung"] and "Vãng vong" not in ky:
        ky.append("Vãng vong")
    kl = CN.ky_loai(ky, viec)
    loai += kl
    ghi += [k for k in ky if k not in kl and not k.startswith("Sát chủ âm")]
    if toa is not None:
        rt = TS.xet(d, toa, kieu_toa or KIEU_TOA[viec])
        loai += ["tọa: " + ngan_gon(x) for _, x in rt["loai"]]
        canh_ngay = ["tọa: " + x for c, x in rt["canh"] if c == "ngay"]
        ghi += canh_ngay
    if "诸事不宜" not in yi and bt_tranh and (dl["gan"] == bt_tranh or dl["zhi"] == bt_tranh):
        ghi.append("Bành Tổ: " + BANH_TO[bt_tranh])
        p2 = max(p2 - 4, 0)
    # 3. Hợp người chủ sự (20)
    if nguoi:
        ds = []
        for ten, y, c, z, hs in nguoi:
            if CN.XUNG(v2["chi"], z):
                ds.append(0)
                loai.append("xung tuổi " + ten)
                continue
            s = 10
            if any(v2["chi"] in th and z in th for th in TAM_HOP) or frozenset((v2["chi"], z)) in LUC_HOP:
                s += 3
            dung, ky = hs
            for h in (CN.HANH_CAN[v2["can"]], CHI_HANH[v2["chi"]]):
                s += 4 if h in dung else (-4 if h in ky else 0)
            ds.append(max(0, min(20, s)))
        p3 = round(sum(ds) / len(ds))
    else:
        p3 = 10
    # 4. Khả thi (15)
    p4 = 15 if (thu_ok is None or d.weekday() in thu_ok) else 0
    if p4 == 0:
        ghi.append("ngoài các thứ trong tuần anh/chị muốn")
    # 5. Độ tin (5): các cách tính đồng thuận
    dong_thuan = not any("tính theo tháng" in g for g in v2["ghi"]) and not (
        (chinh & yi and v2["truc"] in truc_xau) or (v2["hd"] and chinh & ji))
    # Tiết rơi 00:00–00:59 giờ Bắc Kinh = 23:xx giờ Việt Nam hôm trước: lịch Việt Nam đã sang tháng mới, còn trực, thần
    # sát ngày (lunar-python, giờ Bắc Kinh) vẫn tính tháng cũ – báo rõ và hạ độ tin (kiểm chéo 11/2026)
    lp = TS.lech_lich_trung_quoc(d)
    if lp:
        dong_thuan = False
        g = TS.giao_tiet(d)
        ghi.append("ngày giao tiết %s theo giờ Việt Nam (%s): trực, thần sát theo lịch Trung Quốc còn tính tháng %s, "
                   "có thể khác lịch Việt Nam" % (g[0] if g else "", g[1] if g else "?", TS.vn(lp)))
    p5 = 5 if dong_thuan else 2
    if not dong_thuan:
        ghi.append("các cách tính chưa đồng thuận")
    diem = p1 + p_truc + p2 + p3 + p4 + p5
    if toa is not None and canh_ngay:
        diem -= 5                   # ngày có điều cần cân nhắc với tọa sơn (Âm phủ, khắc sơn gia, xung song sơn)
    if not chinh and "馀事勿取" in yi:
        diem = min(diem, 54)
    if loai:
        nhom = "Tránh"
    elif diem >= 70:
        nhom = "Nên chọn"
    elif diem >= 55:
        nhom = "Dự phòng"
    else:
        nhom = "Bình thường"
    return dict(d=d, v2=v2, dl=dl, diem=diem, nhom=nhom, loai=loai, ghi=ghi + [g for g in v2["ghi"] if "tính theo" in g],
                phan=(p1 + p_truc, p2, p3, p4, p5), n_cat=n_cat, n_hung=n_hung)


KIEU_TOA = {"dongtho": "duong", "antang": "am"}


def ngan_gon(x):
    """Câu kết luận tọa sơn -> nhãn ngắn cho cột ghi chú."""
    return x.split(" (")[0].split(":")[0]


def gio_tot(r, viec, nguoi):
    """Giờ hoàng đạo của ngày, đánh dấu giờ nên/kiêng việc và giờ xung tuổi."""
    chinh, phu = VIEC[viec][1], VIEC[viec][2]
    kq = []
    for z in r["v2"]["gio"]:
        yi, ji = gio_trong_ngay(r["d"], z)
        xung = [t for t, _, _, zz, _ in nguoi if CN.XUNG(z, zz)]
        if xung:
            continue
        if (chinh | phu) & set(ji):
            continue
        dau = "★" if (chinh | phu) & set(yi) else ""
        if z == 0:
            kq.append("Tý%s (00–01h; 23h đêm đó đã là giờ Tý ngày sau)" % dau)
        else:
            kq.append("%s%s (%02d–%02dh)" % (CN.CHI[z], dau, (2 * z - 1) % 24, (2 * z + 1) % 24))
    return kq


def in_ngay(tu, den, viec, nguoi, thu_ok=None, theo_tiet=False, top=5, chi_tiet=True, toa=None, toa_ghi="", kieu_toa=None):
    if (den - tu).days > 92:
        raise SystemExit("LỖI: khoảng ngày tối đa 93 ngày – chia nhỏ ra.")
    if den < tu:
        raise SystemExit("LỖI: --den phải sau --tu.")
    ten_viec = VIEC[viec][0]
    print("CHỌN NGÀY ĐẦY ĐỦ: %s, từ %s đến %s" % (ten_viec, tu.strftime("%d/%m/%Y"), den.strftime("%d/%m/%Y")))
    if VIEC[viec][1]:
        print("- Việc tra trong lịch: %s (chính); %s (phụ)" % (
            ", ".join(VIEC_HV[x] for x in sorted(VIEC[viec][1])),
            ", ".join(VIEC_HV[x] for x in sorted(VIEC[viec][2])) or "-"))
    for ten, y, c, z, hs in nguoi:
        print("- Người chủ sự %s: sinh năm %s %s (%d)%s%s" % (ten, CN.CAN[c], CN.CHI[z], y,
              "; hành cần " + ", ".join(HANH[h] for h in sorted(hs[0])) if hs[0] else "",
              "; hành kỵ " + ", ".join(HANH[h] for h in sorted(hs[1])) if hs[1] else ""))
    if nguoi:
        nam_am = CN.nam_am_cua_khoang(tu, den)
        print("TUỔI THEO NĂM (Kim Lâu xét cho cưới hỏi – thường tính tuổi cô dâu – và làm nhà; Hoang Ốc, Tam Tai xét "
              "khi làm nhà, động thổ; năm tính theo âm lịch):")
        for ten, y, c, z, hs in nguoi:
            print(CN.dong_tuoi(ten, y, nam_am))
    print("- Việc nên/kiêng, cát thần, hung sát theo Hiệp Kỷ Biện Phương Thư (lịch Trung Quốc, tính theo tháng tiết khí); "
          "Hoàng đạo theo %s như lịch Việt Nam." % ("tháng tiết khí" if theo_tiet else "tháng âm"))
    if toa is not None:
        kieu_toa = kieu_toa or KIEU_TOA[viec]
        print()
        print("TỌA SƠN %s: %s%s" % ("MỘ" if kieu_toa in ("am", "phu") else "NHÀ / CÔNG TRÌNH", TS.mo_ta(toa), toa_ghi))
        print("- Loại: %s" % TS.TEN_KIEU[kieu_toa])
        print("Thần sát theo năm, tháng (Hiệp Kỷ Biện Phương Thư – Luận phù sơn, Luận lập hướng, Nguyệt hung thần):")
        print("| Từ ngày | Năm | Tháng | Không dùng được | Cần cân nhắc |")
        print("|---|---|---|---|---|")
        for d0, gn, gt, lo, ca in TS.tom_tat(tu, den, toa, kieu_toa):
            print("| %s | %s | %s | %s | %s |" % (d0.strftime("%d/%m/%Y"), TS.vn(gn), TS.vn(gt), "; ".join(lo) or "-",
                                               "; ".join(ca) or "-"))
        print(TS.GHI_CHU)
    print()
    rows = []
    d = tu
    while d <= den:
        rows.append(cham(d, viec, nguoi, thu_ok, theo_tiet, toa, kieu_toa))
        d += dt.timedelta(days=1)
    if chi_tiet:
        print("| Ngày | Âm lịch | Can chi | Hoàng/Hắc đạo | Trực | Tú | Nên | Kiêng | Điểm | Nhóm | Ghi chú |")
        print("|---|---|---|---|---|---|---|---|---|---|---|")
        for r in rows:
            v2, dl, al = r["v2"], r["dl"], r["v2"]["am"]
            dau = [x for x in ("诸事不宜", "馀事勿取") if x in dl["yi"]]
            nen = ", ".join([VIEC_HV[x].upper() for x in dau] +
                            _dich([x for x in dl["yi"] if x not in dau], VIEC_HV)[:8])
            kieng = ", ".join(_dich(dl["ji"], VIEC_HV)[:8])
            print("| %s %s | %d/%d%s | %s %s | %s | %s | %s | %s | %s | %d | %s | %s |" % (
                THU[r["d"].weekday()], r["d"].strftime("%d/%m"), al[0], al[1], " nhuận" if al[3] else "",
                CN.CAN[v2["can"]], CN.CHI[v2["chi"]], ("Hoàng đạo " if v2["hd"] else "Hắc đạo ") + v2["than"],
                v2["truc"], v2["tu"], nen or "-", kieng or "-", r["diem"], r["nhom"],
                "; ".join(r["loai"] + r["ghi"]) or ""))
        print()
    for nhom in ("Nên chọn", "Dự phòng"):
        ds = sorted([r for r in rows if r["nhom"] == nhom], key=lambda r: (-r["diem"], r["d"]))[:top]
        print("%s:" % nhom.upper())
        if not ds:
            print("- (không có)")
        for r in ds:
            dl, v2 = r["dl"], r["v2"]
            print("- %s %s (%d/%d âm, %s %s) – %d điểm [việc %d, ngày %d, người %d, khả thi %d, độ tin %d]" % (
                THU[r["d"].weekday()], r["d"].strftime("%d/%m/%Y"), v2["am"][0], v2["am"][1],
                CN.CAN[v2["can"]], CN.CHI[v2["chi"]], r["diem"], *r["phan"]))
            print("  Cát thần: %s | Hung sát: %s" % (", ".join(_dich(dl["cat"], CAT_THAN)) or "-",
                                                   ", ".join(_dich(dl["hung"], HUNG_SAT)) or "-"))
            print("  Giờ tốt (★ = giờ đó lịch ghi nên làm việc này; đã bỏ giờ xung tuổi, giờ kiêng): %s" %
                  (", ".join(gio_tot(r, viec, nguoi)) or "-"))
            print("  Hướng: Hỷ thần %s, Tài thần %s, Phúc thần %s, Quý nhân (ngày) %s / (đêm) %s; Thai thần: %s" % (
                dl["hy"], dl["tai"], dl["phuc"], dl["qn_duong"], dl["qn_am"], dl["thai"]))
            if r["ghi"]:
                print("  Lưu ý: " + "; ".join(r["ghi"]))
    tranh = [r for r in rows if r["nhom"] == "Tránh"]
    print("NÊN TRÁNH (%d ngày): %s" % (len(tranh), "; ".join(
        "%s (%s)" % (r["d"].strftime("%d/%m"), ", ".join(dict.fromkeys(r["loai"]))) for r in tranh[:31])))
    print("(Thang 100 điểm: hợp việc 35 = nên/kiêng 25 + trực 10; ngày 25 = Hoàng đạo 10 + tú 5 + thần sát 10 "
          "(trừ Tam Nương, Nguyệt Kỵ, Dương Công); người chủ sự 20; khả thi 15; độ tin 5. "
          "Ngày bị loại: lịch ghi kiêng đúng việc này, mọi việc không nên, Nguyệt Phá, Tam Nương, Nguyệt Kỵ, "
          "Dương Công, Thọ tử, xung tuổi người chủ sự; Sát chủ dương với cưới hỏi, làm nhà, nhà đất, khai trương, "
          "ký kết, nhậm chức; Sát chủ âm với an táng, cưới hỏi, động thổ; Vãng vong với đi xa, cưới hỏi, chuyển nhà, nhậm chức, chữa bệnh, "
          "nhận người%s.)" % ("; với nhà/mộ đã cho tọa: phạm thần sát tọa sơn ở bảng trên, chi ngày xung tọa (ngày có điều cần "
          "cân nhắc với tọa bị trừ 5 điểm)" if toa is not None else ""))
    return rows


def them_lenh(sub):
    p = sub.add_parser("ngay", help="chọn ngày đầy đủ: nên/kiêng, thần sát, hướng thần, chấm 100 điểm")
    p.add_argument("--tu", required=True)
    p.add_argument("--den", required=True)
    p.add_argument("--viec", default="chung", choices=list(VIEC))
    p.add_argument("--tuoi", nargs="*", default=[], help='người chủ sự: "Tên:năm âm lịch sinh[:hành cần, vd Thủy+Kim[:hành kỵ, vd Hỏa]]"')
    p.add_argument("--thu", help="chỉ muốn các thứ, vd T7,CN")
    p.add_argument("--hoang-dao-tiet", action="store_true")
    p.add_argument("--gon", action="store_true", help="không in bảng từng ngày")
    p.add_argument("--top", type=int, default=5)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--toa", help="tọa sơn nhà/mộ (dùng với --viec dongtho hoặc antang): tên sơn (Tý, Nhâm, Cấn...) hoặc độ la bàn phía lưng")
    g.add_argument("--huong", help="hướng nhà/mộ: tên sơn hoặc độ la bàn phía mặt tiền (tự đổi ra tọa)")
    p.add_argument("--sua-nha", action="store_true", help="với --toa/--huong và dongtho: chỉ sửa nhà đang có, không xây mới")
    p.add_argument("--phu-tang", action="store_true",
                   help="với --toa/--huong và antang: chôn thêm vào mộ cũ, mộ tổ (bỏ khắc sơn gia và Âm phủ theo Hiệp Kỷ)")
    p.set_defaults(_chay=chay)


def chay(a):
    try:
        tu, den = [dt.date(*[int(v) for v in s.replace("/", "-").split("-")]) for s in (a.tu, a.den)]
    except (ValueError, TypeError):
        raise SystemExit("LỖI: --tu/--den dạng YYYY-MM-DD.")
    thu_ok = None
    if a.thu:
        thu_ok = set()
        for x in a.thu.split(","):
            x = x.strip().upper()
            if not x:
                continue
            if x not in THU:
                raise SystemExit("LỖI: --thu chỉ nhận T2, T3, T4, T5, T6, T7, CN (cách nhau bằng dấu phẩy).")
            thu_ok.add(THU.index(x))
    toa, toa_ghi = None, ""
    if a.toa or a.huong:
        if a.viec not in KIEU_TOA:
            raise SystemExit("LỖI: --toa/--huong chỉ dùng với --viec dongtho (động thổ, xây sửa) hoặc antang (an táng, xây mộ).")
        toa, do, cb = TS.doc_toa(a.toa, a.huong)
        toa_ghi = TS.nguon_do(a, do) + ("\nCHÚ Ý: " + cb if cb else "")
    if a.sua_nha and not (toa is not None and a.viec == "dongtho"):
        raise SystemExit("LỖI: --sua-nha dùng cùng --viec dongtho và --toa/--huong.")
    if a.phu_tang and not (toa is not None and a.viec == "antang"):
        raise SystemExit("LỖI: --phu-tang dùng cùng --viec antang và --toa/--huong.")
    in_ngay(tu, den, a.viec, doc_tuoi(a.tuoi), thu_ok, a.hoang_dao_tiet, a.top, not a.gon, toa, toa_ghi,
            "sua" if a.sua_nha else ("phu" if a.phu_tang else None))


def tu_kiem():
    loi = []
    # 1. Từ điển phủ hết từ ngữ của thư viện (quét 2 năm + mẫu thưa 1900-2100)
    ngay = [dt.date(2025, 1, 1) + dt.timedelta(i) for i in range(300)]
    ngay += [dt.date(1900, 1, 1) + dt.timedelta(i * 97) for i in range(520)]
    for d in ngay:
        dl = du_lieu_ngay(d)
        for x in dl["yi"] + dl["ji"]:
            if x not in VIEC_HV:
                loi.append("thiếu việc %r" % x)
        for x in dl["cat"]:
            if x not in CAT_THAN:
                loi.append("thiếu cát thần %r" % x)
        for x in dl["hung"]:
            if x not in HUNG_SAT:
                loi.append("thiếu hung sát %r" % x)
        if any("一" <= ch <= "鿿" for ch in dl["thai"]):
            loi.append("Thai thần chưa dịch hết: %s" % dl["thai"])
    for d in ngay[:40]:
        for z in range(12):
            yi, ji = gio_trong_ngay(d, z)
            for x in yi + ji:
                if x not in VIEC_HV:
                    loi.append("thiếu việc (giờ) %r" % x)
    # 2. Đối chiếu dữ liệu cố định với lịch vạn niên đã in (lunar-python 1.4.8, ngày 08/11/2026)
    dl = du_lieu_ngay(dt.date(2026, 11, 8))
    if not ("入宅" in dl["ji"] and "安床" in dl["yi"] and "月煞" in dl["hung"] and "金匮" in dl["cat"]):
        loi.append("dữ liệu 08/11/2026 lệch")
    if (dl["hy"], dl["tai"], dl["phuc"]) != ("Tây Nam", "Tây Nam", "Tây Bắc"):
        loi.append("hướng thần 08/11/2026 lệch: %s" % ((dl["hy"], dl["tai"], dl["phuc"]),))
    # 3. Bất biến: ngày lịch ghi kiêng đúng việc chính không bao giờ vào nhóm Nên chọn/Dự phòng
    ng = doc_tuoi(["A:1990:Thủy+Kim:Hỏa", "B:1988"])
    for v in ("khaitruong", "cuoi", "dongtho", "kyhopdong", "xuathanh", "nhaptrach"):
        for d in ngay[:200]:
            r = cham(d, v, ng)
            if VIEC[v][1] & set(r["dl"]["ji"]) and r["nhom"] != "Tránh":
                loi.append("%s %s kiêng mà không bị loại" % (v, d))
            if any(CN.XUNG(r["v2"]["chi"], z) for _, _, _, z, _ in ng) and r["nhom"] != "Tránh":
                loi.append("%s %s xung tuổi mà không bị loại" % (v, d))
            if not (0 <= r["diem"] <= 100):
                loi.append("điểm ngoài 0-100: %s" % r["diem"])
    # 3b. Ngày 17/02/2026 lịch chỉ cho cúng tế, an táng ("việc khác không nên") -> động thổ phải bị loại
    r = cham(dt.date(2026, 2, 17), "dongtho", [])
    if "馀事勿取" in r["dl"]["yi"] and r["nhom"] != "Tránh":
        loi.append("ngày 'việc khác không nên' không bị loại")
    # 3c. Ngày kỵ theo tháng âm lịch (rà soát 11/2026): 09/04/2026 = 22/2 Quý Sửu là Sát chủ dương (baolamdong.vn);
    #     Thọ tử tháng Giêng là Bính Tuất; Thọ tử bị loại với mọi việc, Sát chủ dương với cưới/nhập trạch/động thổ,
    #     Vãng vong với xuất hành/cưới/nhập trạch.
    if "Sát chủ dương" not in CN.xet_ngay(dt.date(2026, 4, 9), [], "chung")["ky"]:
        loi.append("Sát chủ dương 09/04/2026")
    if CN.ngay_ky_thang((1, 1, 2026, False), 2, 10) != ["Thọ tử"]:
        loi.append("Thọ tử tháng Giêng")
    d0 = dt.date(2026, 1, 1)
    for i in range(0, 400, 1):
        d = d0 + dt.timedelta(i)
        ky = CN.xet_ngay(d, [], "chung")["ky"]
        vv = "Vãng vong" in ky or "往亡" in du_lieu_ngay(d)["hung"]
        for v in ("cuoi", "nhaptrach", "dongtho", "xuathanh", "antang"):
            if not (ky or vv):
                break
            r = cham(d, v, [])
            xau = ("Thọ tử" in ky or ("Sát chủ dương" in ky and v in ("cuoi", "nhaptrach", "dongtho"))
                   or (vv and v in ("cuoi", "nhaptrach", "xuathanh"))
                   or ("Sát chủ âm" in ky and v in ("antang", "cuoi", "dongtho")))
            if xau and r["nhom"] != "Tránh":
                loi.append("%s %s ngày kỵ %s mà không bị loại" % (v, d, ky))
    # 3c2. Sát chủ âm tháng 7/8: các nguồn chia đôi, an táng loại cả ngày Hợi lẫn ngày Sửu
    #      (17/08/2026 = 5/7 Quý Hợi, 19/08/2026 = 7/7 Ất Sửu, 12/09/2026 = 2/8 Kỷ Sửu, 22/09/2026 = 12/8 Kỷ Hợi)
    for d in (dt.date(2026, 8, 17), dt.date(2026, 8, 19), dt.date(2026, 9, 12), dt.date(2026, 9, 22)):
        r = cham(d, "antang", [])
        if r["nhom"] != "Tránh" or not any(k.startswith("Sát chủ âm") for k in r.get("loai", [])):
            loi.append("an táng %s (Sát chủ âm tháng 7/8) không bị loại" % d)
    if any(k.startswith("Sát chủ âm") for k in cham(dt.date(2026, 9, 22), "cuoi", [])["loai"]):
        loi.append("bản đảo Sát chủ âm loại nhầm việc cưới")
    # Ngọc Hạp Chánh Tông: ngày Sát chủ (bảng chính) kỵ cất nhà, cưới gả -> 12/09/2026 (2/8 Kỷ Sửu) loại cưới, động thổ
    for v in ("cuoi", "dongtho"):
        r = cham(dt.date(2026, 9, 12), v, [])
        if r["nhom"] != "Tránh" or "Sát chủ âm" not in r["loai"]:
            loi.append("Sát chủ âm 12/09/2026 không loại %s" % v)
    # 3d. Sửa dữ liệu lunar-python: 04/12/1953 tháng Hợi ngày Kỷ Sửu là Nguyệt Yếm (không phải Hà Khôi);
    #     11/09/1950 tháng Dậu ngày Kỷ Dậu có Nguyệt Hình, không có Nguyệt Yếm.
    d1, h2 = du_lieu_ngay(dt.date(1953, 12, 4)), du_lieu_ngay(dt.date(1950, 9, 11))["hung"]
    h1 = d1["hung"]
    h3 = du_lieu_ngay(dt.date(1950, 8, 6))["hung"]          # tháng Mùi ngày Quý Dậu
    if "月厌" not in h1 or "归忌" not in h1 or "河魁" in h1 or "六合" in d1["cat"] or "月厌" in h2 or "月刑" not in h2 \
            or "劫煞" in h3 or "灾煞" not in h3:
        loi.append("sửa Hà Khôi / Nguyệt Yếm của lunar-python")
    # 3e. Kim Lâu / Hoang Ốc / Tam Tai theo năm âm lịch: 05–20/01/2027 vẫn là năm Bính Ngọ 2026
    if CN.nam_am_cua_khoang(dt.date(2027, 1, 5), dt.date(2027, 1, 20)) != [2026] or \
            CN.nam_am_cua_khoang(dt.date(2027, 1, 20), dt.date(2027, 3, 1)) != [2026, 2027]:
        loi.append("năm âm lịch của khoảng chọn ngày sai")
    # 4. Khớp v2: Hoàng đạo/Trực/Tú lấy đúng từ chonngay của v2
    r = cham(dt.date(2026, 11, 9), "khaitruong", doc_tuoi(["Chị:1984"]))
    if not (r["v2"]["truc"] == "Kiến" and r["v2"]["tu"] == "Trương" and r["v2"]["hd"]):
        loi.append("lệch v2 ngày 09/11/2026")
    # 5. Tọa sơn (Hiệp Kỷ): năm Đinh Mùi 2027 khắc sơn Thủy Thổ -> tọa Tý xây mới loại cả tháng 3/2027;
    #    an táng tọa Cấn 19/12/2026 chỉ cảnh báo (Âm phủ/khắc sơn theo ngày) và bị trừ 5 điểm; tháng Kỷ Hợi Âm phủ ở Cấn.
    if any("tọa: Niên khắc sơn gia" not in cham(dt.date(2027, 3, d), "dongtho", [], toa=0)["loai"] for d in (1, 15, 31)):
        loi.append("tọa Tý năm Đinh Mùi không bị loại vì niên khắc sơn gia")
    a, b = cham(dt.date(2026, 12, 19), "antang", [], toa=3), cham(dt.date(2026, 12, 19), "antang", [])
    if a["loai"] or a["diem"] != b["diem"] - 5 or not any(g.startswith("tọa: Ngày khắc sơn gia") for g in a["ghi"]):
        loi.append("an táng tọa Cấn 19/12/2026")
    if "tọa: Nguyệt Âm phủ tháng Kỷ Hợi ở tọa Cấn" not in cham(dt.date(2026, 11, 20), "antang", [], toa=3)["loai"]:
        loi.append("Nguyệt Âm phủ tháng Kỷ Hợi tọa Cấn")
    # 6. Kiểm chéo 11/2026: Lập đông 2023 lúc 23:35 giờ Việt Nam (00:35 ngày 8 giờ Bắc Kinh) – ngày 7/11/2023 phải báo
    #    lệch tháng giữa lịch Việt Nam và trực, thần sát của lịch Trung Quốc; ngày 5/3/2026 (Kinh trập 20:59) thì không
    if not any("ngày giao tiết Lập đông" in g for g in cham(dt.date(2023, 11, 7), "dongtho", [])["ghi"]) or \
            any("ngày giao tiết" in g for g in cham(dt.date(2026, 3, 5), "dongtho", [])["ghi"]):
        loi.append("báo lệch tháng ngày giao tiết 23:xx giờ Việt Nam")
    return sorted(set(loi))[:30]
