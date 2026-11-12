# -*- coding: utf-8 -*-
"""cachcuc_tv.py – Nhận diện CÁCH CỤC Tử vi trên lá số an theo cách Việt Nam (Thái Thứ Lang, tuvi_vn.py).

Lệnh con của nc.py:  cachcuc --ngay ... --gio ... --gioi nam|nu [--nam-xem N] [--tan-suat N]

Nguyên tắc:
- Chỉ số cung 0=Tý ... 11=Hợi; tên sao đúng như tuvi_vn.py ("Tả Phù", "Hữu Bật", ...).
- Mỗi cách có điều kiện CẤU TRÚC (vị trí sao) và điều kiện PHẨM CHẤT (độ sáng, Tuần/Triệt, sát tinh, Hóa Kỵ,
  cát tinh hội). Cấu trúc đủ thì nhận diện; phẩm chất quyết định mức: "thành cách" / "cách yếu" / "phá cách".
  Với cách hung, "cách yếu" nghĩa là hung đã được giảm (có sao chế, Tuần/Triệt hóa giải...).
- Mặc định xét cung Mệnh (với tam phương tứ chính: Mệnh, Quan Lộc +4, Tài Bạch +8, Thiên Di +6) và cung Thân
  (khi Thân không cùng cung Mệnh); một số cách sách ghi rõ "chỉ xét Mệnh" thì không xét ở Thân.
- Điều kiện theo sách Việt Nam (Toàn thư bản dịch La Hồng Tiên, Tân Biên Thái Thứ Lang, Tử vi Ảo bí Việt Viêm Tử,
  Tử vi Chỉ nam Song An Đỗ Văn Lưu, Tử vi Tinh điển Vũ Tài Lục, Chìa khóa Tử vi Quản Xuân Thịnh ...), đối chiếu qua các
  trang tiếng Việt ghi ở NGUON. Không sao chép điều kiện của các repo cộng đồng phái Trung Quốc.
"""
import datetime as dt
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tuvi_vn as T  # noqa: E402

CHI = T.CHI
CAN = T.CAN
TY, SUU, DAN, MAO, THIN, TI, NGO, MUI, THAN, DAU, TUAT, HOI = range(12)

SAT = ("Kình Dương", "Đà La", "Hỏa Tinh", "Linh Tinh", "Địa Không", "Địa Kiếp")   # lục sát
TU_SAT = SAT[:4]
KHONG_KIEP = ("Địa Không", "Địa Kiếp")
CAT_PHU = ("Tả Phù", "Hữu Bật", "Văn Xương", "Văn Khúc", "Thiên Khôi", "Thiên Việt")
CAT_HOA = ("Hóa Lộc", "Hóa Quyền", "Hóa Khoa")
DAO_HOA = ("Đào Hoa", "Hồng Loan", "Thiên Diêu")
TRIET_HET = "Triệt mạnh ở khoảng 3 đại hạn đầu, nhẹ dần từ khoảng 35 tuổi"

# ------------------------------------------------------------------ nguồn đối chiếu (trang tiếng Việt)
_TSK = "tuvisonkhiem.vn/thu-vien/cach-cuc/"
_TSKS = "tuvisonkhiem.vn/thu-vien/sao/"
_HVL = "hocvienlyso.org/cac-dang-cach-cuc-trong-tu-vi-phan-1.html (bản dịch 'Tử vi đẩu số cách cục luận')"
_KAB = "hoc.kabala.vn/tu-vi-dau-so-cach-cuc-luan-phan-cat-cach"
_THD = "tuvihiendai.vn/28-cach-cuc-co-ban-trong-tu-vi"
_SC = "sonchu.vn/nghien-cuu/cac-dang-cach-cuc-trong-tu-vi"
_HVL4 = "hocvienlyso.org/tiet-4-khai-luan-ve-cach-cuc.html"
_HVLHL = "hocvienlyso.org/hoa-linh-giap-menh-va-linh-xuong-da-vu.html (theo Vương Đình Chi)"
_DXX = "Đặng Xuân Xuyến, Tử vi kiến giải (NXB Thanh Hóa 2009), bài 'Tuần Triệt và những dấu hỏi'"
NGUON = {
    "tu_phu": "%s (Tử Phủ đồng cung Dần Thân, tuổi Giáp tốt nhất; Đinh Kỷ Canh Quý cát); %s ('Tử Phủ đồng cung, "
              "Đế vô quyền sở' khi gặp Tuần/Không); vị trí Dần Thân theo Tân Biên" % (_HVL, _DXX),
    "tu_phu_tv": "%s, %s (4 thế Tử Phủ chầu về: Vũ Tướng/Liêm Dần Thân, Liêm Tướng Tý Ngọ, Thiên Tướng Sửu Mùi); "
                 "%stu-phu-trieu-vien (Toàn thư, Ảo bí; trang này dùng chuẩn khác: Tử Vi tọa Mệnh, Phủ chiếu)"
                 % (_KAB, _HVL, _TSK),
    "tu_sat": "%stu-vi (Tử Sát hóa Quyền: Tử Sát Tỵ Hợi gặp Hóa Quyền, hóa sát thành quyền); Tân Biên" % _TSKS,
    "tu_tham": "%stu-vi (Đào hoa phạm Chủ: Tử Tham Mão Dậu gặp đào hoa và sát tinh; Cực cư Mão Dậu: gặp Không "
               "Kiếp/tứ sát, xa danh lợi, thiên về tu tâm)" % _TSKS,
    "tu_pha": "%stu-vi (Tử Phá Sửu Mùi; phá cách 'Tử Phá thiếu phụ tá' khi thiếu Tả Hữu, cát tinh)" % _TSKS,
    "tu_tuong": "%stu-vi (Tử Tướng Thìn Tuất – Thìn Tuất là Thiên La, Địa Võng; gắn với Phủ Tướng triều viên); "
                "%sphu-bat-cung-chu (luật 'cách cục tối kỵ Không vong, nhất là Tử Phủ Vũ Tướng')" % (_TSKS, _TSK),
    "quan_than": "%squan-than-khanh-hoi (Toàn thư Định quý cục, Tân Biên; đủ 3 nhóm phụ – văn – quý; "
                 "'loạn thế nan thành đại sự' khi gặp Kình Dương, Địa Kiếp); %sphu-bat-cung-chu (Phụ Bật củng chủ); "
                 "%stu-vi (Kim dư phù giá: Tử Vi thủ Mệnh có Tả Hữu và cát tinh phù giá)" % (_TSK, _TSK, _TSKS),
    "bach_quan": "%stu-vi ('trăm quan chầu về': Tả Hữu, Khôi Việt, Xương Khúc vây quanh Tử Vi)" % _TSKS,
    "co_quan": "%stu-vi (cô quân: Tử Vi thiếu phụ tá, 'tuy hoạch cát nhi vô đạo'; Đế ngộ hung đồ: gặp Không Kiếp, "
               "Kình Đà, nhiều sát tinh, ít cát tinh)" % _TSKS,
    "ly_minh": "%scuc-huong-ly-minh (phú 'Tử Vi cư Ngọ vô Hình Kỵ, Giáp Đinh Kỷ nhân vị chí công khanh'; Toàn thư "
               "Tổng luận phú; Ảo bí)" % _TSK,
    "phu_tuong": "%sphu-tuong-trieu-vien (nghĩa gốc theo Tử Vân, Tử vi chân thuyên: Phủ Tướng ở Tài Quan chầu về "
                 "Mệnh; Chỉ nam có thế Mệnh Sửu; Mạn đàm 218: Tướng gặp Triệt, Phủ gặp Tuần đều phá; kỵ Không Kiếp); "
                 "%s (thế Mệnh vô chính diệu)" % (_TSK, _KAB),
    "spt": "Tân Biên (bộ Sát Phá Liêm Tham); %sco-nguyet-dong-luong (vận Sát Phá Liêm Tham); %s" % (_TSK, _HVL4),
    "cndl": "%sco-nguyet-dong-luong (Mệnh Thân có Cơ Âm hoặc Mệnh Dần Thân có Đồng Lương; 'tối kỵ Hỏa Linh xâm "
            "phá'; Tân Biên, Chìa khóa Tử vi); %s" % (_TSK, _KAB),
    "co_luong": "%sco-luong-gia-hoi; %s (Cơ Lương Thìn Tuất + cát tinh); %s ('Thìn Tuất Không Vong Cơ Lương tăng "
                "đạo')" % (_TSK, _HVL, _DXX),
    "cu_nhat": "%s (Cự Nhật đồng cung Dần Thân, Dần tốt hơn; tuổi Canh Tân Quý); %scu-mon, %sthai-duong (hợp Hóa "
               "Quyền, Phượng Các, kỵ Lộc Tồn; 'thực lộc trì danh')" % (_HVL, _TSKS, _TSKS),
    "tinh_minh": "%snhat-nguyet-tinh-minh (Mệnh Tỵ Thái Dương, Dậu Thái Âm, Sửu Thiên Lương; Phú giải Thái Vân "
                 "Trình, Ảo bí, Tân Biên)" % _TSK,
    "phan_boi": "%sthai-duong (Nhật Nguyệt phản bối: Thái Dương cư Tuất, Thái Âm cư Thìn – mất ánh sáng, lao lực, "
                "gặp Hóa Kỵ dễ hao tán); %s (sao hãm gặp Tuần Triệt trở nên sáng sủa)" % (_TSKS, _DXX),
    "loi_mon": "%snhat-xuat-loi-mon (Mệnh Mão Dương Lương; cũng gọi Nhật chiếu Lôi môn, Nhật xuất Phù tang; tuổi Ất "
               "Tân Nhâm Canh; Toàn thư, Ảo bí, Chỉ nam, Tân Biên); %s (lợi người sinh ban ngày)" % (_TSK, _HVL4),
    "le_trung": "%sthai-duong ('Thái Dương cư Ngọ, gọi là Nhật lệ trung thiên'); %s (Kim sán quang huy, tuổi Canh "
                "Tân)" % (_TSKS, _HVL),
    "nguyet_lang": "%snguyet-lang-thien-mon (Mệnh Hợi Thái Âm; tuổi Bính Đinh quý, Nhâm Quý phú; sợ Kình Đà cùng "
                   "Thiên Hình, sợ Tuần Triệt, không sợ Hóa Kỵ); %s (lợi người sinh ban đêm)" % (_TSK, _HVL4),
    "thuong_hai": "%snguyet-sinh-thuong-hai (Mệnh Tý Đồng Âm; Tân Biên mục 13; Ảo bí: tuổi Bính Đinh; kỵ Thiên "
                  "Diêu, Kình Đà, Linh Hỏa, Không Kiếp, Tuần Triệt)" % _TSK,
    "minh_chau": "%s (Mệnh Mùi vô chính diệu, Dương Lương ở Mão, Thái Âm ở Hợi chiếu; tuổi Ất Bính Tân Nhâm); %s"
                 % (_HVL, _THD),
    "nn_giap": "%snhat-nguyet-giap-tai (Vũ Tham Mệnh Sửu, Thái Âm Tý – Thái Dương Dần kẹp; Vũ Tham Mùi hai vầng "
               "mờ không thành; 'Nhật Nguyệt giáp Tài, bất quyền tắc phú')" % _TSK,
    "dong_lam": "%sthai-duong (Nhật Nguyệt đồng cung Sửu Mùi chiếu Mệnh đối cung; 'Nhật Nguyệt thủ bất như hợp "
                "chiếu'); %s ('Nhật Nguyệt Sửu Mùi tối cần Kỵ, Không phả vi đại cát'); %s (Nhị diệu đồng lâm)"
                % (_TSKS, _DXX, _HVL),
    "dlxl": "%s (Dương Lương, Lộc Tồn, Văn Xương); %sthien-luong ('cách Dương Lương Xương Lộc nổi tiếng')"
            % (_HVL, _TSKS),
    "thach_trung": "%sthach-trung-an-ngoc (Đẩu số cốt tủy phú: 'Tý Ngọ Cự Môn, thạch trung ẩn ngọc'; chuẩn chặt: "
                   "Cự Hóa Lộc tuổi Tân; Tử vi kinh nghiệm: gặp Lộc Tồn thì vô vị; cung Thân không tính)" % _TSK,
    "that_sat": "%sthat-sat-trieu-dau (Ảo bí: 'Thất Sát triều đẩu, tước lộc vinh xương'; Toàn thư, Ảo bí nhận Tý Ngọ "
                "Dần Thân, Tinh điển chỉ nhận Dần Thân)" % _TSK,
    "hung_tu": "Bửu Đình, 'Liêm Trinh Dần Thân cách' (tuviungdung.blogspot.com: 'thủ Mệnh vô tứ sát ... Hùng tú "
               "triều viên chi cách; gia sát: bình thường'); %s (tuổi Giáp Mậu Canh)" % _THD,
    "anh_tinh": "%sanh-tinh-nhap-mieu (Toàn thư: 'Tý Ngọ Phá Quân, gia quan tiến lộc'; Giáp Quý mạnh nhất; phá khi "
                "tam phương có Xương Khúc)" % _TSK,
    "vu_thu": "%svu-khuc-thu-vien (Vũ Khúc độc tọa Thìn Tuất; Chìa khóa Tử vi; phá bởi Linh Xương Đà Vũ, tứ sát)"
              % _TSK,
    "tham_vu": "%s (Tham Vũ đồng hành: Tham Lang, Vũ Khúc ở tứ mộ); %s (Vũ Tham Sửu Mùi thủ Mệnh)" % (_SC, _THD),
    "hoa_tham": "%stham-hoa-tuong-phung, %stham-linh-trieu-vien (Tham Lang tọa Mệnh; Hỏa ở Mệnh/Tài/Quan, Linh ở "
                "tam phương tứ chính; tứ mộ tốt nhất; Tham hãm không thành; Tham Linh ở Mão Dậu không tính – Tử Vân, "
                "Đằng Sơn, Toàn thư, Tân Biên)" % (_TSK, _TSK),
    "ma_dau": "%sma-dau-doi-kiem (Đằng Sơn: tuổi Bính Mệnh Ngọ Kình Dương, Đồng Âm, Hóa Lộc; Chìa khóa Tử vi: "
              "'Kình thủ Mệnh tại Ngọ là hung nhất' khi không có bộ sao chế); %s ('Mã đầu đới kiếm, trấn ngự biên "
              "cương')" % (_TSK, _TSKS + "kinh-duong"),
    "kinh_mieu": "%skinh-duong-nhap-mieu (Tân Biên; 'Kình Dương nhập miếu, phú quý thanh dương'; tứ mộ; chuẩn chặt "
                 "đòi Mệnh vô chính diệu)" % _TSK,
    "loc_ma": "%sloc-ma-giao-tri (Lộc Tồn – không phải Hóa Lộc – với Thiên Mã: đồng cung mạnh nhất, xung chiếu, "
              "tam hợp yếu dần; Đà La gặp Mã là 'chiết túc mã'; Toàn thư, Tân Biên, Ảo bí)" % _TSK,
    "song_loc": "%ssong-loc-trieu-vien (Mệnh không có Lộc, Lộc Tồn và Hóa Lộc ở Tài/Quan/Di chiếu về; Tinh điển)"
                % _TSK,
    "uyen_uong": "%suyen-uong-loc-hoi (Mệnh có một Lộc, Lộc kia ở tam phương; xưa gọi Lộc hợp uyên ương; Tinh điển, "
                 "Tử vi từ điển)" % _TSK,
    "minh_am": "%suyen-uong-loc-hoi (Minh Lộc ám Lộc: một Lộc ở Mệnh, một Lộc ở cung nhị hợp – Ảo bí); %s" % (_TSK, _HVL),
    "tam_ky": "%skhoa-quyen-loc-cung (Tam kỳ gia hội: đủ Hóa Khoa, Quyền, Lộc trong tam phương tứ chính; Tinh điển, "
              "Toàn thư)" % _TSK,
    "giap_loc": "%sgiap-song-loc (Hóa Lộc và Lộc Tồn kẹp Mệnh; Phú giải Thái Vân Trình, Tổng luận §8 'lục giáp "
                "cát', có giáp Khoa Quyền Lộc)" % _TSK,
    "ta_huu": "%sgiap-ta-giap-huu (chỉ Mệnh Sửu Mùi; Tả Hữu đồng cung là thế tọa thủ, tháng 4 hoặc 10); %s (Tả Hữu "
              "đồng cung Sửu Mùi)" % (_TSK, _THD),
    "xk_giap": "%sgiap-xuong-giap-khuc (Mệnh Sửu Mùi; 4 tổ hợp tháng–giờ; 'Mệnh được Xương Khúc giáp, nếu không quý "
               "thì cũng giàu')" % _TSK,
    "van_que": "%s mục 29 ('Cung mệnh đóng tại Sửu Mùi, Văn Xương, Văn Khúc đồng cung, lại có cát tinh gia hội'; "
               "gặp hung sát tinh là phá cách)" % _SC,
    "phu_van": "%sphu-cung-van-tinh (tam phương tứ chính đủ Tả Phù, Hữu Bật, Văn Xương, Văn Khúc; chỉ 3 tổ hợp "
               "tháng–giờ; kỵ Mệnh Phá Quân, Hóa Kỵ văn tinh)" % _TSK,
    "khoi_viet": "%sthien-at-cung-menh (một sao tọa Mệnh, sao kia ở Tài/Quan/Di; giáp Khôi Việt khi Mệnh Thìn Tuất; "
                 "Phú giải, Ảo bí, Toàn thư)" % _TSK,
    "vcd": "Tân Biên (Mệnh vô chính diệu lấy chính tinh cung xung chiếu); %s ('Nhật Nguyệt ... phùng Không'; các sao "
           "Không: Tuần, Triệt, Thiên Không, Địa Không); %s (Mệnh vô chính diệu chỉ thấy Không Kiếp mà không có cát "
           "tinh là cách nghèo)" % (_DXX, _HVL4),
    "kd_giap": "%skinh-duong (Kình Đà giáp Kỵ: Lộc Tồn đồng cung Hóa Kỵ bị Kình Đà kẹp – phá cách); %s ('Dương Đà "
               "giáp' là cặp sát kẹp cung)" % (_TSKS, _HVLHL),
    "kk_giap": "%s (Không Kiếp giáp – cặp sát tinh kẹp cung sinh khuyết điểm); %s ('Không Kiếp giáp Kị' là hung cách)"
               % (_HVLHL, _HVL4),
    "hl_giap": "%s ('Hỏa Linh giáp mệnh vi bại cục'; Vũ Sát, Vũ Phủ, Liêm Sát, Tử Sát ở giữa thì gian lao nhưng vẫn "
               "phấn chấn)" % _HVLHL,
    "hinh_ky": "sonchu.vn/2022/08/17/la-hinh-ky-khong-phai-hinh-tu (Hình Kỵ giáp Ấn: Thiên Tướng bị Kình Dương – "
               "thường cùng Thiên Lương – và Cự Môn Hóa Kỵ kẹp); %sliem-trinh (Hình tù giáp Ấn: Liêm Tướng Tý Ngọ gặp "
               "Kình Dương – phá cách, kiện tụng)" % _TSKS,
    "loc_pha": "%s ('Lộc gặp xung phá, cát xứ tàng hung': Lộc Tồn/Hóa Lộc ở Mệnh Thân gặp Không, Kiếp, Kỵ, Không "
               "vong); %sloc-ton-gap-khong-kiep (Lưỡng trùng Hoa Cái khi cả hai Lộc bị phá)" % (_HVL4, _TSK),
    "luong_ma": "%sthien-luong (mục 6: 'Mã Lương phiêu đãng' – Thiên Lương hãm ở Tỵ Hợi gặp Thiên Mã, phá cách)"
                % _TSKS,
    "liem_tham": "%sliem-trinh (Liêm Tham Tỵ Hợi ham vui, dễ sa đà; gặp Tuần Triệt lại thành văn võ; Hóa Kỵ tuổi "
                 "Bính lại giải bớt; Hợi tốt hơn Tỵ); %s (Liêm Tham Tỵ Hợi – Phản vi kỳ cách khi gặp Tuần Triệt)"
                 % (_TSKS, _DXX),
    "cu_hoa": "%s (Cự Môn, Hỏa Tinh, Kình Dương hội – thành cách hay bại tùy Lộc hay Kỵ dẫn động); %scu-phung-tu-sat "
              "(Cự Môn tọa Mệnh, tam phương tứ chính đủ ba họ: Kình/Đà, Hỏa/Linh, Không/Kiếp)" % (_HVL4, _TSK),
    "lxdv": "%s (Mệnh Thìn Tuất, tam phương tứ chính hội Linh Tinh, Đà La, Văn Xương, Vũ Khúc: 'hạn chí đầu hà', "
            "đề phòng sông nước, xe cộ)" % _HVLHL,
}


# ------------------------------------------------------------------ bàn sao: các hàm tra cứu
class _Ban:
    """Bọc dict lá số của tuvi_vn.lap_la_so cho tiện tra cứu."""

    def __init__(self, ls):
        self.ls = ls
        self.can, self.chi, self.gio = ls["can"], ls["chi"], ls["gio"]
        self.vt, self.hoa = ls["vt"], ls["hoa"]
        self.bo = {p: set(ls["sao"][p]) for p in range(12)}
        self.chinh_c = {p: [x for x in T.CHINH_TINH if x in self.bo[p]] for p in range(12)}
        self.tuan, self.triet = set(ls["tuan"]), set(ls["triet"])

    def co(self, p, *ten):
        b = self.bo[p % 12]
        return all(t in b for t in ten)

    def chinh(self, p):
        return self.chinh_c[p % 12]

    def vcd(self, p):
        return not self.chinh_c[p % 12]

    @staticmethod
    def tp(p):
        """Tam phương tứ chính: [Mệnh, Quan Lộc, Tài Bạch, Thiên Di] của cung p."""
        return [p % 12, (p + 4) % 12, (p + 8) % 12, (p + 6) % 12]

    @staticmethod
    def giap(p):
        return [(p - 1) % 12, (p + 1) % 12]

    def tim(self, ps, ds):
        """Danh sách (sao, cung) của các sao trong ds có mặt ở các cung ps."""
        return [(x, q) for q in ps for x in ds if x in self.bo[q]]

    def hoa_o(self, p, loai=None):
        return [t for t, h in self.hoa.items() if self.vt[t] == p % 12 and (loai is None or h == loai)]

    def tim_hoa(self, ps, loai):
        return [(t, self.vt[t]) for t, h in self.hoa.items() if h == loai and self.vt[t] in ps]

    def kv(self, p):
        return (["Tuần"] if p in self.tuan else []) + (["Triệt"] if p in self.triet else [])

    def loc(self, p):
        """Các 'Lộc' tại cung p: 'Lộc Tồn' và/hoặc 'Hóa Lộc (sao)'."""
        r = ["Lộc Tồn"] if self.co(p, "Lộc Tồn") else []
        return r + ["Hóa Lộc (%s)" % t for t in self.hoa_o(p, "Hóa Lộc")]

    def f(self, ten, p=None):
        p = self.vt[ten] if p is None else p
        ds = T.do_sang(ten, p) if ten in T.DO_SANG else ""
        h = self.hoa.get(ten)
        return "%s%s%s ở %s" % (ten, "(%s)" % ds if ds else "", "[%s]" % h if h else "", CHI[p])

    def fl(self, lst):
        return ", ".join(self.f(x, q) for x, q in lst)

    def fc(self, p):
        """Mô tả chính tinh của cung p."""
        c = self.chinh(p)
        return " + ".join(self.f(x, p).rsplit(" ở ", 1)[0] for x in c) if c else "vô chính diệu"

    def cat_ds(self, ps, ds=CAT_PHU + ("Lộc Tồn",)):
        r = ["%s ở %s" % (x, CHI[q]) for x, q in self.tim(ps, ds)]
        for h in CAT_HOA:
            r += ["%s (%s) ở %s" % (h, t, CHI[q]) for t, q in self.tim_hoa(ps, h)]
        return r

    def ten_cung(self, p):
        return "%s (%s)" % (T.ten_cung(self.ls, p), CHI[p])


def _ban(ls):
    return _Ban(ls)


# ------------------------------------------------------------------ danh mục cách
CACH = []


def _cach(ma, ten, nhom, nguon, than=True):
    """Đăng ký một hàm nhận diện. Hàm nhận (B, p) trả None hoặc list dict:
    co_so, yeu, pha, ghi (list chuỗi), có thể ghi đè ten, nhom."""
    def deco(fn):
        CACH.append(dict(ma=ma, ten=ten, nhom=nhom, nguon=NGUON[nguon], ham=fn, than=than))
        return fn
    return deco


def _r(co_so, yeu=(), pha=(), ghi=(), **kw):
    d = dict(co_so=list(co_so), yeu=list(yeu), pha=list(pha), ghi=list(ghi))
    d.update(kw)
    return [d]


def _tt_menh(B, p, ds, ten="Mệnh"):
    """Thêm lý do Tuần/Triệt tại cung p vào danh sách ds."""
    kv = B.kv(p)
    if kv:
        ds.append("%s tại %s %s%s" % ("/".join(kv), ten, CHI[p], " (%s)" % TRIET_HET if "Triệt" in kv else ""))
    return kv


def _sat_s(B, ps, ds=SAT):
    return B.tim(ps, ds)


# ---------------------------------------------------------- 1. nhóm Tử Vi
@_cach("tu_phu", "Tử Phủ đồng cung", "cát", "tu_phu")
def _c_tu_phu(B, p):
    if p not in (DAN, THAN) or not B.co(p, "Tử Vi", "Thiên Phủ"):
        return None
    cs = ["%s có %s + %s đồng cung" % (CHI[p], B.f("Tử Vi").rsplit(" ở", 1)[0], "Thiên Phủ")]
    yeu, pha, ghi = [], [], []
    cat = B.cat_ds(B.tp(p))
    if cat:
        cs.append("cát tinh hội: " + ", ".join(cat))
    else:
        yeu.append("tam phương không có Tả Hữu, Xương Khúc, Khôi Việt, Lộc, Khoa Quyền (sách cho là cách khó ứng)")
    kv = B.kv(p)
    if kv:
        pha.append("%s tại Mệnh – 'Đế vô quyền sở'%s" % ("/".join(kv), "; " + TRIET_HET if "Triệt" in kv else ""))
    if B.co(p, "Địa Không"):
        pha.append("Địa Không tại Mệnh – 'Đế vô quyền sở'")
    s = B.tim([p], ("Kình Dương", "Đà La", "Hỏa Tinh", "Linh Tinh", "Địa Kiếp", "Thiên Không"))
    if s:
        yeu.append("tại Mệnh có " + B.fl(s))
    k = B.hoa_o(p, "Hóa Kỵ")
    if k:
        yeu.append("Hóa Kỵ tại Mệnh (%s)" % ", ".join(k))
    if B.can == 0:
        ghi.append("tuổi Giáp: sách xếp hợp cách nhất")
    elif B.can in (3, 5, 6, 9):
        ghi.append("tuổi %s: sách xếp cát" % CAN[B.can])
    return _r(cs, yeu, pha, ghi)


_TPTV_THE = {frozenset(["Vũ Khúc", "Thiên Tướng"]): (DAN, THAN), frozenset(["Liêm Trinh"]): (DAN, THAN),
             frozenset(["Liêm Trinh", "Thiên Tướng"]): (TY, NGO), frozenset(["Thiên Tướng"]): (SUU, MUI)}


@_cach("tu_phu_tv", "Tử Phủ triều viên", "cát", "tu_phu_tv", than=False)
def _c_tu_phu_tv(B, p):
    c = frozenset(B.chinh(p))
    if p not in _TPTV_THE.get(c, ()):
        return None
    tp = B.tp(p)
    if B.vt["Tử Vi"] not in tp[1:] or B.vt["Thiên Phủ"] not in tp[1:]:
        return None
    cs = ["Mệnh %s có %s; %s và %s chầu về" % (CHI[p], B.fc(p), B.f("Tử Vi"), B.f("Thiên Phủ"))]
    yeu, pha = [], []
    cat = B.cat_ds(tp)
    if cat:
        cs.append("cát tinh: " + ", ".join(cat))
    else:
        yeu.append("không có cát tinh hội")
    _tt_menh(B, p, pha)
    for t in ("Tử Vi", "Thiên Phủ"):
        kv = B.kv(B.vt[t])
        if kv:
            yeu.append("%s tại cung có %s" % ("/".join(kv), t))
    s = _sat_s(B, tp)
    if len(s) >= 2:
        yeu.append("sát tinh hội: " + B.fl(s))
    if B.hoa_o(p, "Hóa Kỵ"):
        yeu.append("Hóa Kỵ tại Mệnh (Toàn thư: cách thành bình thường)")
    return _r(cs, yeu, pha)


@_cach("tu_sat", "Tử Sát đồng cung", "trung", "tu_sat")
def _c_tu_sat(B, p):
    if p not in (TI, HOI) or not B.co(p, "Tử Vi", "Thất Sát"):
        return None
    cs = ["%s có Tử Vi + Thất Sát" % CHI[p]]
    yeu, pha = [], []
    q_menh = B.hoa_o(p, "Hóa Quyền")
    q_tp = B.tim_hoa(B.tp(p), "Hóa Quyền")
    ten, nhom = "Tử Sát đồng cung", "trung"
    if q_menh or q_tp:
        ten, nhom = "Tử Sát hóa Quyền", "cát"
        cs.append("Hóa Quyền %s" % ", ".join("%s ở %s" % (t, CHI[q]) for t, q in q_tp))
        if not q_menh:
            yeu.append("Hóa Quyền không ở ngay Mệnh mà ở tam phương")
    else:
        yeu.append("chưa gặp Hóa Quyền để 'hóa sát vi quyền'")
    s = _sat_s(B, [p], ("Kình Dương", "Đà La", "Địa Không", "Địa Kiếp"))
    if len(s) >= 2:
        pha.append("tại Mệnh có " + B.fl(s))
    elif s:
        yeu.append("tại Mệnh có " + B.fl(s))
    _tt_menh(B, p, yeu)
    return _r(cs, yeu, pha, ten=ten, nhom=nhom)


def _muon_doi(B, p, *ten):
    """Mệnh vô chính diệu mà đối cung có đủ các sao 'ten' -> trả cung đối, ngược lại None."""
    q = (p + 6) % 12
    if B.vcd(p) and B.co(q, *ten):
        return q
    return None


@_cach("tu_tham", "Đào hoa phạm chủ", "hung", "tu_tham")
def _c_tu_tham(B, p):
    if p not in (MAO, DAU):
        return None
    goc, muon = p, False
    if not B.co(p, "Tử Vi", "Tham Lang"):
        q = _muon_doi(B, p, "Tử Vi", "Tham Lang")
        if q is None:
            return None
        goc, muon = q, True
    cs = ["Tử Vi + Tham Lang ở %s%s" % (CHI[goc], " (Mệnh vô chính diệu mượn đối cung)" if muon else "")]
    yeu = ["mượn chính tinh đối cung nên lực yếu"] if muon else []
    dao = B.tim([p, (p + 6) % 12], DAO_HOA)
    sat = _sat_s(B, B.tp(p))
    kk = [x for x in sat if x[0] in KHONG_KIEP]
    giam = B.tim(B.tp(p), ("Tả Phù", "Hữu Bật"))
    giam += [x for x in B.tim_hoa(B.tp(p), "Hóa Khoa") if x not in giam]
    kq = []
    # rà soát 11/2026: cách thành chỉ bằng vị trí (Toàn thư q.2, Tân Biên tr. 56); sao đào hoa, Xương Khúc làm nặng
    # thêm, phụ tá chế bớt. Trước đây đòi phải có sao đào hoa nên bỏ sót nhiều lá số.
    y = list(yeu)
    xk = B.tim([p, (p + 6) % 12], ("Văn Xương", "Văn Khúc"))
    if not dao and not xk:
        y.append("không có sao đào hoa, Xương Khúc đi kèm – nhẹ hơn")
    elif not sat:
        y.append("chưa có sát tinh đi kèm đào hoa")
    if giam:
        y.append("có %s chế bớt" % B.fl(giam))
    kq += _r(cs + (["sao đào hoa: " + B.fl(dao)] if dao else []) + (["Xương Khúc: " + B.fl(xk)] if xk else [])
             + (["sát tinh: " + B.fl(sat)] if sat else []), y)
    if kk or (len([x for x in sat if x[0] in TU_SAT]) >= 2):
        kq += _r(cs + ["gặp " + B.fl(kk or sat)], yeu,
                 ghi=["xu hướng xa danh lợi, thiên về đời sống tinh thần"], ten="Cực cư Mão Dậu", nhom="trung")
    return kq or None


@_cach("tu_pha", "Tử Phá đồng cung", "trung", "tu_pha")
def _c_tu_pha(B, p):
    if p not in (SUU, MUI) or not B.co(p, "Tử Vi", "Phá Quân"):
        return None
    tp = B.tp(p)
    th = B.tim(tp + B.giap(p), ("Tả Phù", "Hữu Bật"))
    cat = B.cat_ds(tp)
    cs = ["%s có Tử Vi + Phá Quân" % CHI[p]]
    if not th and not cat:
        return _r(cs + ["không có Tả Hữu và cát tinh phù tá"], ten="Tử Phá thiếu phụ tá", nhom="hung")
    yeu = []
    if th:
        cs.append("phụ tá: " + B.fl(th))
    else:
        yeu.append("thiếu Tả Hữu, chỉ có " + ", ".join(cat))
    if cat and th:
        cs.append("cát tinh: " + ", ".join(cat))
    s = _sat_s(B, [p])
    if s:
        yeu.append("sát tinh tại Mệnh: " + B.fl(s))
    _tt_menh(B, p, yeu)
    return _r(cs, yeu)


@_cach("tu_tuong", "Tử Tướng Thìn Tuất (Thiên La Địa Võng)", "trung", "tu_tuong")
def _c_tu_tuong(B, p):
    if p not in (THIN, TUAT) or not B.co(p, "Tử Vi", "Thiên Tướng"):
        return None
    tp = B.tp(p)
    cs = ["%s (%s) có Tử Vi + Thiên Tướng(%s)" % (CHI[p], "Thiên La" if p == THIN else "Địa Võng",
                                                 T.do_sang("Thiên Tướng", p))]
    yeu, pha = [], []
    giai = ["%s ở %s" % (x, CHI[q]) for x, q in B.tim(tp, ("Tả Phù", "Hữu Bật"))]
    giai += ["%s (%s) ở %s" % (h, t, CHI[q]) for h in CAT_HOA for t, q in B.tim_hoa(tp, h)]
    if giai:
        cs.append("có %s giúp thoát La Võng" % ", ".join(giai))
    else:
        yeu.append("không có Tả Hữu hay Khoa Quyền Lộc để thoát La Võng")
    kv = B.kv(p)
    if kv:
        pha.append("%s tại Mệnh (Tử Phủ Vũ Tướng tối kỵ Không vong)" % "/".join(kv))
    s = _sat_s(B, [p])
    if s:
        yeu.append("sát tinh tại Mệnh: " + B.fl(s))
    return _r(cs, yeu, pha)


@_cach("quan_than", "Quân thần khánh hội", "cát", "quan_than")
def _c_quan_than(B, p):
    if not B.co(p, "Tử Vi"):
        return None
    tp = B.tp(p)
    vung = tp + B.giap(p)
    # rà soát 11/2026: Vương Đình Chi tính cả đồng cung, xung, hội, giáp; chỉ xét tam phương thì cách gần như không
    # thể có ở 6 can năm (do vị trí an sao) – nay xét cả hai cung giáp
    g1 = B.tim(vung, ("Tả Phù", "Hữu Bật"))
    g2 = B.tim(vung, ("Văn Xương", "Văn Khúc"))
    g3 = B.tim(vung, ("Thiên Khôi", "Thiên Việt"))
    th = B.tim(vung, ("Tả Phù", "Hữu Bật"))
    yeu, pha = [], []
    if g1 and g2 and g3:
        ten = "Quân thần khánh hội"
        cs = ["Tử Vi thủ %s; đủ ba nhóm bề tôi: %s | %s | %s" % (CHI[p], B.fl(g1), B.fl(g2), B.fl(g3))]
    elif len(th) >= 2 and len({x for x, _ in th}) == 2:
        ten = "Phụ Bật củng chủ (Kim dư phù giá)"
        cs = ["Tử Vi thủ %s có đủ Tả Phù, Hữu Bật (đồng cung, giáp hoặc tam phương): %s" % (CHI[p], B.fl(th))]
        if not (g2 or g3):
            yeu.append("chưa có thêm văn tinh, quý tinh")
    else:
        return None
    s = _sat_s(B, tp)
    if B.tim(tp, ("Kình Dương",)) and B.tim(tp, ("Địa Kiếp",)):
        pha.append("gặp Kình Dương và Địa Kiếp – 'loạn thế nan thành đại sự'")
    elif len(s) >= 2:
        yeu.append("sát tinh hội: " + B.fl(s))
    if B.tim(tp, ("Thiên Hình",)) and B.tim_hoa(tp, "Hóa Kỵ"):
        yeu.append("Thiên Hình và Hóa Kỵ cùng hội")
    _tt_menh(B, p, yeu)
    return _r(cs, yeu, pha, ten=ten)


@_cach("bach_quan", "Bách quan triều củng", "cát", "quan_than")
def _c_bach_quan(B, p):
    if not B.co(p, "Tử Vi"):
        return None
    vung = B.tp(p) + B.giap(p)
    doi = [("Tả Phù", "Hữu Bật"), ("Văn Xương", "Văn Khúc"), ("Thiên Khôi", "Thiên Việt")]
    if not all(B.tim(vung, (a,)) and B.tim(vung, (b,)) for a, b in doi):
        return None
    cs = ["Tử Vi thủ %s, đủ ba cặp Tả Hữu, Xương Khúc, Khôi Việt vây quanh (tam phương và hai cung giáp): %s"
          % (CHI[p], B.fl(B.tim(vung, CAT_PHU)))]
    yeu = []
    s = _sat_s(B, B.tp(p))
    if len(s) >= 2:
        yeu.append("sát tinh hội: " + B.fl(s))
    _tt_menh(B, p, yeu)
    return _r(cs, yeu, ten="Bách quan triều củng")


@_cach("co_quan", "Tại dã cô quân / Vô đạo chi quân", "hung", "co_quan")
def _c_co_quan(B, p):
    if not B.co(p, "Tử Vi"):
        return None
    tp = B.tp(p)
    phu = B.tim(tp + B.giap(p), CAT_PHU)
    sat = _sat_s(B, tp)
    cat_hoa = [x for h in CAT_HOA for x in B.tim_hoa(tp, h)]
    if len(sat) >= 2 and len(phu) < len(sat):
        yeu = ["vẫn có phụ tá: " + B.fl(phu)] if phu else []
        return _r(["Tử Vi thủ %s gặp %s; phụ tá ít hơn sát tinh" % (CHI[p], B.fl(sat))], yeu,
                  ten="Vô đạo chi quân (Đế ngộ hung đồ)", nhom="hung")
    if not phu:
        yeu = ["có cát hóa: " + ", ".join("%s ở %s" % (t, CHI[q]) for t, q in cat_hoa)] if cat_hoa else []
        return _r(["Tử Vi thủ %s, tam phương và hai cung giáp không có Tả Hữu, Xương Khúc, Khôi Việt" % CHI[p]],
                  yeu, ghi=["tự lực nhiều, ít người phò tá"], ten="Tại dã cô quân", nhom="trung")
    return None


@_cach("ly_minh", "Cực hướng Ly minh", "cát", "ly_minh")
def _c_ly_minh(B, p):
    if p != NGO or not B.co(p, "Tử Vi"):
        return None
    cs = ["Mệnh Ngọ có %s tọa thủ" % B.f("Tử Vi").rsplit(" ở", 1)[0]]
    yeu, pha, ghi = [], [], []
    hk = B.tim([p], ("Thiên Hình", "Kình Dương")) + [(t, p) for t in B.hoa_o(p, "Hóa Kỵ")]
    if hk:
        yeu.append("gặp Hình/Kỵ tại Mệnh (%s) – mất tầng 'công khanh'" % ", ".join(x for x, _ in hk))
    elif B.can in (0, 3, 5):
        ghi.append("tuổi %s, không Hình Kỵ: đúng câu 'Giáp Đinh Kỷ nhân vị chí công khanh'" % CAN[B.can])
    elif B.can in (2, 4):
        ghi.append("tuổi %s: Ảo bí ghi 'có thành có bại'" % CAN[B.can])
    s = _sat_s(B, B.tp(p))
    if len(s) >= 2:
        pha.append("lục sát hội (%s) – 'Đế ngộ hung đồ'" % B.fl(s))
    elif B.tim([p], KHONG_KIEP):
        yeu.append("Không Kiếp tại Mệnh – đế tinh nhu nhược")
    _tt_menh(B, p, yeu)
    return _r(cs, yeu, pha, ghi)


# ---------------------------------------------------------- 2. Phủ Tướng, bộ sao
@_cach("phu_tuong", "Phủ Tướng triều viên", "cát", "phu_tuong", than=False)
def _c_phu_tuong(B, p):
    if B.vt["Thiên Phủ"] != (p + 4) % 12:
        return None
    q_phu, q_tuong = (p + 4) % 12, (p + 8) % 12
    cs = ["Thiên Phủ ở Quan Lộc %s, %s ở Tài Bạch chầu về Mệnh %s (%s)" % (
        CHI[q_phu], B.f("Thiên Tướng").rsplit(" ở", 1)[0], CHI[p], B.fc(p))]
    yeu, pha = [], []
    if T.do_sang("Thiên Tướng", q_tuong) == "H":
        yeu.append("Thiên Tướng hãm")
    for t, q in (("Thiên Phủ", q_phu), ("Thiên Tướng", q_tuong)):
        kv = B.kv(q)
        if kv:              # rà soát 11/2026: không nguồn nào coi là phá – để yếu
            yeu.append("%s gặp %s" % (t, "/".join(kv)))
    s4 = _sat_s(B, B.tp(p), TU_SAT)
    if len(s4) >= 2:
        yeu.append("tứ sát hội: " + B.fl(s4))
    ky = B.tim_hoa(B.tp(p), "Hóa Kỵ")
    if ky:
        yeu.append("Hóa Kỵ ở tam phương: " + ", ".join("%s ở %s" % (t, CHI[q]) for t, q in ky))
    kk = B.tim([p, q_phu, q_tuong], KHONG_KIEP)
    if kk:
        pha.append("gặp Không Kiếp (%s) – 'Phủ Tướng thì đừng gặp Không Kiếp'" % B.fl(kk))
    cat = B.cat_ds(B.tp(p))
    if cat:
        cs.append("cát tinh: " + ", ".join(cat))
    else:
        yeu.append("không có cát tinh hội")
    if B.vcd(p):
        cs.append("Mệnh vô chính diệu, nhờ Phủ Tướng chầu")
    return _r(cs, yeu, pha)


@_cach("spt", "Sát Phá Tham", "trung", "spt")
def _c_spt(B, p):
    c = [x for x in ("Thất Sát", "Phá Quân", "Tham Lang") if B.co(p, x)]
    if not c or T.do_sang(c[0], p) not in ("M", "V", "Đ"):
        return None
    x = c[0]
    cs = ["Mệnh có %s đắc địa; bộ ba %s, %s, %s ở tam hợp" % (
        B.f(x).rsplit(" ở", 1)[0], B.f("Thất Sát"), B.f("Phá Quân"), B.f("Tham Lang"))]
    yeu = []
    _tt_menh(B, p, yeu)
    if B.hoa_o(p, "Hóa Kỵ"):
        yeu.append("Hóa Kỵ tại Mệnh")
    ghi = ["chủ biến động, khai phá; sát tinh đắc địa đi kèm thì thiên về võ nghiệp"]
    return _r(cs, yeu, ghi=ghi)


_CNDL = ("Thiên Cơ", "Thái Âm", "Thiên Đồng", "Thiên Lương")


@_cach("cndl", "Cơ Nguyệt Đồng Lương", "cát", "cndl")
def _c_cndl(B, p):
    if p not in (DAN, THAN):
        return None
    c = set(B.chinh(p))
    if not c or not c <= set(_CNDL):
        return None
    tp = B.tp(p)
    if any(B.vt[x] not in tp for x in _CNDL):
        return None
    cs = ["Mệnh %s có %s; đủ bốn sao Cơ Nguyệt Đồng Lương ở tam phương tứ chính" % (CHI[p], B.fc(p))]
    yeu, pha = [], []
    if p == DAN and "Thiên Cơ" in c:
        yeu.append("Cơ Âm ở Dần (hai sao kém sáng) – sách không xếp vào cách chuẩn")
    hl = B.tim(tp, ("Hỏa Tinh", "Linh Tinh"))
    if hl:
        pha.append("Hỏa Linh xâm phá (%s)" % B.fl(hl))
    kk = B.tim(tp, KHONG_KIEP)
    if kk:
        yeu.append("Không Kiếp hội: " + B.fl(kk))
    kd = B.tim(tp, ("Kình Dương", "Đà La"))
    if kd:
        yeu.append("Kình/Đà hội: " + B.fl(kd))
    _tt_menh(B, p, yeu)
    return _r(cs, yeu, pha, ghi=["hợp việc giấy tờ, hành chính, mưu tính ('tác lại nhân')"])


@_cach("co_luong", "Cơ Lương gia hội", "cát", "co_luong")
def _c_co_luong(B, p):
    if p not in (THIN, TUAT) or not B.co(p, "Thiên Cơ", "Thiên Lương"):
        return None
    tp = B.tp(p)
    cs = ["%s có Thiên Cơ + Thiên Lương" % CHI[p]]
    yeu, ghi = [], []
    cat = B.cat_ds(tp)
    if cat:
        cs.append("cát tinh: " + ", ".join(cat))
    else:
        yeu.append("không có cát tinh gia hội")
    khong = B.kv(p) + [x for x, _ in B.tim([p], ("Thiên Không", "Địa Không"))]
    if khong:
        yeu.append("gặp sao Không tại Mệnh (%s)" % ", ".join(khong))
        ghi.append("'Thìn Tuất Không Vong Cơ Lương tăng đạo' – dễ nhạt chí bon chen, thiên về triết lý, tôn giáo")
    s = _sat_s(B, [p])
    if s:
        yeu.append("sát tinh tại Mệnh: " + B.fl(s))
    return _r(cs, yeu, ghi=ghi)


@_cach("cu_nhat", "Cự Nhật đồng cung", "cát", "cu_nhat")
def _c_cu_nhat(B, p):
    if p not in (DAN, THAN):
        return None
    goc, muon = p, False
    if not B.co(p, "Cự Môn", "Thái Dương"):
        q = _muon_doi(B, p, "Cự Môn", "Thái Dương")
        if q is None:
            return None
        goc, muon = q, True
    cs = ["%s ở %s%s" % (" + ".join(B.f(x, goc).rsplit(" ở", 1)[0] for x in ("Cự Môn", "Thái Dương")), CHI[goc],
                         " (Mệnh vô chính diệu mượn đối cung)" if muon else "")]
    yeu, pha, ghi = [], [], []
    if muon:
        yeu.append("mượn chính tinh đối cung nên lực yếu")
    if goc == THAN:
        yeu.append("Thái Dương ở Thân đã ngả bóng – sách xếp Thân kém Dần")
    if B.hoa_o(p, "Hóa Quyền") or B.co(p, "Phượng Các"):
        cs.append("hợp Hóa Quyền/Phượng Các")
    if B.co(goc, "Lộc Tồn"):
        yeu.append("gặp Lộc Tồn (sách ghi kỵ)")
    k = B.hoa_o(goc, "Hóa Kỵ")
    if k:
        pha.append("Hóa Kỵ (%s)" % ", ".join(k))
    s = _sat_s(B, sorted({p, goc}))
    if len(s) >= 2:
        yeu.append("sát tinh: " + B.fl(s))
    _tt_menh(B, p, yeu)
    if B.can in (6, 7, 9):
        ghi.append("tuổi %s: sách xếp bậc trên" % CAN[B.can])
    return _r(cs, yeu, pha, ghi)


# ---------------------------------------------------------- 3. Nhật Nguyệt
def _bong(B, ten):
    return T.do_sang(ten, B.vt[ten]) == "H"


@_cach("tinh_minh", "Nhật Nguyệt tịnh minh", "cát", "tinh_minh")
def _c_tinh_minh(B, p):
    if B.vt["Thái Dương"] != TI or B.vt["Thái Âm"] != DAU:
        return None
    sao = {TI: "Thái Dương", DAU: "Thái Âm", SUU: "Thiên Lương"}.get(p)
    if sao is None or not B.co(p, sao):
        return None
    cs = ["Mệnh %s có %s; %s và %s cùng sáng chiếu hợp" % (CHI[p], sao, B.f("Thái Dương"), B.f("Thái Âm"))]
    yeu, pha = [], []
    for t in ("Thái Dương", "Thái Âm"):
        q = B.vt[t]
        kd = B.tim([q], ("Kình Dương", "Đà La"))
        if kd:
            yeu.append("%s gặp %s (Nhật Nguyệt gặp Kình Đà)" % (t, B.fl(kd)))
        kv = B.kv(q) + [x for x, _ in B.tim([q], ("Địa Không",))]
        if kv:
            yeu.append("%s gặp %s" % (t, "/".join(kv)))
    _tt_menh(B, p, yeu)
    if sao == "Thiên Lương" and B.tim(B.tp(p), KHONG_KIEP):
        yeu.append("Thiên Lương Sửu gặp Không Kiếp (Đồng Lương gặp Không Kiếp)")
    s = _sat_s(B, B.tp(p))
    if len(s) >= 4:
        pha.append("gặp đủ sát tinh (%s) – chỉ còn bình thường" % B.fl(s))
    return _r(cs, yeu, pha)


@_cach("phan_boi", "Nhật Nguyệt phản bối", "hung", "phan_boi")
def _c_phan_boi(B, p):
    if p not in (THIN, TUAT) or B.vt["Thái Dương"] != TUAT or B.vt["Thái Âm"] != THIN:
        return None
    cs = ["Mệnh %s: %s, %s – hai vầng đều mờ, trục Thìn Tuất" % (CHI[p], B.f("Thái Dương"), B.f("Thái Âm"))]
    yeu, ghi = [], []
    kv = B.kv(p)
    if kv:
        yeu.append("%s tại Mệnh – sao hãm gặp Tuần Triệt trở nên sáng hơn" % "/".join(kv))
    cat = [x for h in CAT_HOA for x in B.tim_hoa([THIN, TUAT], h) if x[0] in ("Thái Dương", "Thái Âm")]
    if cat:     # rà soát 11/2026: Toàn thư q.2 không coi cát hóa trên chính Nhật Nguyệt là cứu – chỉ ghi chú
        ghi.append("Nhật/Nguyệt được cát hóa (%s) – có sách cho là đỡ, Toàn thư không tính là cứu"
                   % ", ".join(t for t, _ in cat))
    tp = B.tp(p)
    if B.cat_ds(tp) and not _sat_s(B, tp):
        yeu.append("tam phương có cát tinh, không sát tinh")
    if [t for t in ("Thái Dương", "Thái Âm") if B.hoa.get(t) == "Hóa Kỵ"]:
        ghi.append("có Hóa Kỵ ở Nhật/Nguyệt: dễ hao tán")
    return _r(cs, yeu, ghi=ghi)


@_cach("loi_mon", "Nhật chiếu lôi môn (Nhật xuất phù tang)", "cát", "loi_mon")
def _c_loi_mon(B, p):
    if p != MAO or not B.co(p, "Thái Dương", "Thiên Lương"):
        return None
    tp = B.tp(p)
    cs = ["Mệnh Mão có %s + Thiên Lương" % B.f("Thái Dương").rsplit(" ở", 1)[0]]
    yeu, pha, ghi = [], [], []
    kd = B.tim(tp, ("Kình Dương", "Đà La"))
    if kd:
        pha.append("Kình/Đà ở tam phương tứ chính: " + B.fl(kd))
    kk = B.tim([p], KHONG_KIEP)
    if kk:
        pha.append("Không Kiếp phạm Thiên Lương: " + B.fl(kk))
    kv = B.kv(p)
    if kv:
        pha.append("%s tại Mão%s" % ("/".join(kv), " (%s)" % TRIET_HET if "Triệt" in kv else ""))
    if B.can in (1, 6, 7, 8):
        ghi.append("tuổi %s: sách xếp hợp cách" % CAN[B.can])
    ghi.append("sinh %s (giờ %s)" % ("ban ngày – hợp Thái Dương" if 3 <= B.gio <= 8 else "ban đêm – kém hơn",
                                     CHI[B.gio]))
    return _r(cs, yeu, pha, ghi)


@_cach("le_trung", "Nhật lệ trung thiên", "cát", "le_trung")
def _c_le_trung(B, p):
    if p != NGO or not B.co(p, "Thái Dương"):
        return None
    cs = ["Mệnh Ngọ có %s" % B.f("Thái Dương").rsplit(" ở", 1)[0]]
    yeu, ghi = [], []
    if B.hoa.get("Thái Dương") == "Hóa Kỵ":
        yeu.append("Thái Dương Hóa Kỵ")
    s = _sat_s(B, B.tp(p))
    if len(s) >= 2:
        yeu.append("sát tinh hội: " + B.fl(s))
    _tt_menh(B, p, yeu)
    if B.can in (6, 7):
        ghi.append("tuổi %s: Kim sán quang huy, sách xếp tốt nhất" % CAN[B.can])
    return _r(cs, yeu, ghi=ghi)


@_cach("nguyet_lang", "Nguyệt lãng thiên môn", "cát", "nguyet_lang")
def _c_nguyet_lang(B, p):
    if p != HOI or not B.co(p, "Thái Âm"):
        return None
    tp = B.tp(p)
    cs = ["Mệnh Hợi có %s" % B.f("Thái Âm").rsplit(" ở", 1)[0]]
    yeu, pha, ghi = [], [], []
    kd = B.tim(tp, ("Kình Dương", "Đà La"))
    hinh = B.tim(tp, ("Thiên Hình",))
    if kd and hinh:
        pha.append("Kình/Đà cùng Thiên Hình chiếu Mệnh: " + B.fl(kd + hinh))
    elif kd:
        yeu.append("Kình/Đà chiếu: " + B.fl(kd))
    if p in B.tuan:
        pha.append("Tuần tại Mệnh (vẫn giữ tên cách)")
    if p in B.triet:
        yeu.append("Triệt tại Mệnh (%s)" % TRIET_HET)
    if B.hoa.get("Thái Âm") == "Hóa Kỵ":
        ghi.append("Thái Âm Hóa Kỵ: sách nói cách này không sợ Kỵ")
    if B.can in (2, 3):
        ghi.append("tuổi %s: chủ quý" % CAN[B.can])
    elif B.can in (8, 9):
        ghi.append("tuổi %s: chủ phú" % CAN[B.can])
    ghi.append("sinh %s" % ("ban đêm – hợp Thái Âm" if B.gio >= 9 or B.gio <= 2 else "ban ngày – kém hơn"))
    return _r(cs, yeu, pha, ghi)


@_cach("thuong_hai", "Nguyệt sinh thương hải", "cát", "thuong_hai")
def _c_thuong_hai(B, p):
    if p != TY or not B.co(p, "Thiên Đồng", "Thái Âm"):
        return None
    cs = ["Mệnh Tý có Thiên Đồng + %s" % B.f("Thái Âm").rsplit(" ở", 1)[0]]
    yeu, pha, ghi = [], [], []
    if B.co(p, "Thiên Diêu"):
        pha.append("Thiên Diêu đồng cung (sách cảnh báo thành 'dâm cách')")
    if B.hoa_o(p, "Hóa Kỵ"):
        pha.append("Hóa Kỵ tại Mệnh: " + ", ".join(B.hoa_o(p, "Hóa Kỵ")))
    s = _sat_s(B, [p])
    if s:
        yeu.append("sát tinh tại Mệnh: " + B.fl(s))
    _tt_menh(B, p, yeu)
    if B.can in (2, 3):
        ghi.append("tuổi %s: Ảo bí ghi phú quý toàn mỹ" % CAN[B.can])
    return _r(cs, yeu, pha, ghi)


@_cach("minh_chau", "Minh châu xuất hải", "cát", "minh_chau")
def _c_minh_chau(B, p):
    if p != MUI or not B.vcd(p) or B.vt["Thái Dương"] != MAO or B.vt["Thái Âm"] != HOI:
        return None
    tp = B.tp(p)
    cs = ["Mệnh Mùi vô chính diệu; %s + Thiên Lương, %s chiếu hợp" % (B.f("Thái Dương"), B.f("Thái Âm"))]
    yeu, pha, ghi = [], [], []
    cat = B.cat_ds(tp)
    if cat:
        cs.append("cát tinh: " + ", ".join(cat))
    else:
        yeu.append("không có cát tinh hội")
    kk = B.tim([p], KHONG_KIEP + ("Kình Dương", "Đà La"))
    if kk:
        pha.append("sát tinh tại Mệnh: " + B.fl(kk))
    ky = [t for t in ("Thái Dương", "Thái Âm") if B.hoa.get(t) == "Hóa Kỵ"]
    if ky:
        yeu.append("%s Hóa Kỵ (tuổi Ất sách vẫn xếp thượng cách)" % ", ".join(ky))
    s = _sat_s(B, tp)
    if len(s) >= 2:
        yeu.append("sát tinh hội: " + B.fl(s))
    if B.can in (1, 2, 7, 8):
        ghi.append("tuổi %s: sách xếp thượng cách" % CAN[B.can])
    elif B.can in (3, 6):
        ghi.append("tuổi %s: sách xếp kém hơn" % CAN[B.can])
    return _r(cs, yeu, pha, ghi)


@_cach("nn_giap", "Nhật Nguyệt giáp mệnh", "cát", "nn_giap")
def _c_nn_giap(B, p):
    g = B.giap(p)
    if {B.vt["Thái Dương"], B.vt["Thái Âm"]} != set(g):
        return None
    ten = "Nhật Nguyệt giáp Tài (giáp Mệnh)" if B.co(p, "Vũ Khúc", "Tham Lang") else "Nhật Nguyệt giáp mệnh"
    cs = ["%s và %s kẹp cung %s (%s)" % (B.f("Thái Dương"), B.f("Thái Âm"), CHI[p], B.fc(p))]
    yeu, pha = [], []
    mo = [t for t in ("Thái Dương", "Thái Âm") if _bong(B, t)]
    if mo:
        yeu.append("%s hãm – hai vầng kẹp không sáng" % ", ".join(mo))
    _tt_menh(B, p, pha, "cung")
    ky = [t for t in ("Thái Dương", "Thái Âm") if B.hoa.get(t) == "Hóa Kỵ"]
    if ky:
        yeu.append("Hóa Kỵ ở " + ", ".join(ky))
    kd = B.tim(g, ("Kình Dương", "Đà La"))
    if kd:
        yeu.append("Kình/Đà theo Nhật Nguyệt: " + B.fl(kd))
    return _r(cs, yeu, pha, ten=ten)


@_cach("dong_lam", "Nhật Nguyệt đồng lâm", "cát", "dong_lam")
def _c_dong_lam(B, p):
    q = B.vt["Thái Dương"]
    if q != B.vt["Thái Âm"] or p not in (SUU, MUI):
        return None
    yeu, ghi = [], []
    if q == p:
        cs = ["Mệnh %s có Thái Dương + Thái Âm đồng cung" % CHI[p]]
        khong = B.kv(p) + [x for x, _ in B.tim([p], ("Thiên Không", "Địa Không"))]
        if khong:
            cs.append("gặp sao Không (%s) – 'tối cần Kỵ, Không'" % ", ".join(khong))
            if [t for t in ("Thái Dương", "Thái Âm") if B.hoa.get(t) == "Hóa Kỵ"]:
                ghi.append("có thêm Hóa Kỵ: sách gọi là kỳ cách")
        else:
            yeu.append("Nhật Nguyệt tọa thủ mà không gặp Tuần/Triệt/Không ('thủ bất như hợp chiếu')")
    elif q == (p + 6) % 12 and B.vcd(p):
        cs = ["Mệnh %s vô chính diệu, Thái Dương + Thái Âm đồng cung ở %s chiếu sang" % (CHI[p], CHI[q])]
        kv = B.kv(q)
        if kv:
            cs.append("%s ở cung Nhật Nguyệt – sách Việt cho là tốt ('tối cần Kỵ, Không')" % "/".join(kv))
    else:
        return None
    if not B.cat_ds(B.tp(p)):
        yeu.append("tam phương không có cát tinh (sách: phản thành hung, phú quý khó bền)")
    return _r(cs, yeu, ghi=ghi)


@_cach("dlxl", "Dương Lương Xương Lộc", "cát", "dlxl")
def _c_dlxl(B, p):
    tp = B.tp(p)
    if any(B.vt[x] not in tp for x in ("Thái Dương", "Thiên Lương", "Văn Xương")):
        return None
    loc = [(x, q) for q in tp for x in B.loc(q)]
    if not loc:
        return None
    cs = ["tam phương tứ chính có %s, %s, %s và %s" % (
        B.f("Thái Dương"), B.f("Thiên Lương"), B.f("Văn Xương"), ", ".join("%s ở %s" % (x, CHI[q]) for x, q in loc))]
    yeu = []
    if _bong(B, "Thái Dương"):
        yeu.append("Thái Dương hãm")
    if not any(B.vt[x] == p for x in ("Thái Dương", "Thiên Lương", "Văn Xương")) and not B.loc(p):
        yeu.append("Mệnh không trực tiếp có sao nào của bộ, chỉ hội chiếu")
    ky = [t for t in ("Thái Dương", "Thiên Lương", "Văn Xương") if B.hoa.get(t) == "Hóa Kỵ"]
    if ky:
        yeu.append("Hóa Kỵ ở " + ", ".join(ky))
    s = _sat_s(B, tp)
    if len(s) >= 2:
        yeu.append("sát tinh hội: " + B.fl(s))
    _tt_menh(B, p, yeu)
    return _r(cs, yeu, ghi=["lợi thi cử, học vị, danh tiếng"])


# ---------------------------------------------------------- 4. chính tinh đơn thủ đắc vị
@_cach("thach_trung", "Thạch trung ẩn ngọc", "cát", "thach_trung", than=False)
def _c_thach_trung(B, p):
    if p not in (TY, NGO) or not B.co(p, "Cự Môn"):
        return None
    tp = B.tp(p)
    h = B.hoa.get("Cự Môn")
    cs = ["Mệnh %s có %s" % (CHI[p], B.f("Cự Môn").rsplit(" ở", 1)[0])]
    yeu, pha = [], []
    # rà soát 11/2026: Tân Biên tr. 37 và sách Việt coi Tuần/Triệt (hoặc Đại, Tiểu Hao) tại Mệnh là điều kiện làm
    # "ngọc lộ ra" – thay được Cự hóa Lộc, Quyền; không còn tính là yếu
    kv = B.kv(p)
    hao = B.tim([p], ("Đại Hao", "Tiểu Hao"))
    if h in ("Hóa Lộc", "Hóa Quyền"):
        cs.append("Cự Môn %s (tuổi %s)" % (h, CAN[B.can]))
    elif kv or hao:
        cs.append("Mệnh gặp %s (sách Việt: điều kiện thành cách)" % ", ".join(kv + [x for x, _ in hao]))
    else:
        cat = [x for k in CAT_HOA for x in B.tim_hoa(tp, k)]
        yeu.append("Cự Môn không hóa Lộc/Quyền%s" % (
            "; chỉ có " + ", ".join("%s ở %s" % (t, CHI[q]) for t, q in cat) + " hội" if cat else ""))
    if h == "Hóa Kỵ":
        pha.append("Cự Môn Hóa Kỵ (tuổi Đinh)")
    if B.co(p, "Lộc Tồn"):
        pha.append("Lộc Tồn đồng cung – 'gặp Lộc Tồn thì vô vị'")
    if B.tim(tp, ("Kình Dương", "Đà La")) and B.tim(tp, ("Hỏa Tinh", "Linh Tinh")) and B.tim(tp, KHONG_KIEP):
        pha.append("Cự phùng tứ sát: " + B.fl(_sat_s(B, tp)))
    elif B.co(p, "Kình Dương"):
        yeu.append("Kình Dương tại Mệnh")
    return _r(cs, yeu, pha)


@_cach("that_sat", "Thất Sát triều đẩu", "cát", "that_sat", than=False)
def _c_that_sat(B, p):
    if p not in (TY, NGO, DAN, THAN) or not B.co(p, "Thất Sát"):
        return None
    q = (p + 6) % 12
    tp = B.tp(p)
    cs = ["Mệnh %s có %s, đối cung %s" % (CHI[p], B.f("Thất Sát").rsplit(" ở", 1)[0], B.fc(q))]
    yeu, ghi = [], []
    cat = B.tim(tp, ("Tả Phù", "Hữu Bật", "Thiên Khôi", "Thiên Việt")) + [(x, q2) for q2 in tp for x in B.loc(q2)]
    if cat:
        cs.append("có " + ", ".join("%s ở %s" % (x, CHI[q2]) for x, q2 in cat))
    else:
        yeu.append("thiếu Tả Hữu, Khôi Việt, Lộc – quyền khó thành nghiệp lâu dài")
    kv = B.kv(p)
    if kv:
        yeu.append("%s tại Mệnh – quyền không như ý" % "/".join(kv))
    if B.kv((p + 4) % 12):
        yeu.append("Tuần/Triệt ở Quan Lộc")
    kk = B.tim([p, q], KHONG_KIEP)
    if kk:
        yeu.append("Không Kiếp cùng trục (%s) – liều lĩnh, rủi ro" % B.fl(kk))
    kl = B.tim(tp, ("Kình Dương", "Linh Tinh"))
    if kl:
        yeu.append("Kình/Linh hội (%s)" % B.fl(kl))
    if p in (TY, NGO):
        ghi.append("Tý Ngọ (đối Vũ Phủ): Toàn thư, Ảo bí nhận; Tinh điển chỉ nhận Dần Thân")
    return _r(cs, yeu, ghi=ghi)


@_cach("hung_tu", "Hùng tú triều viên", "cát", "hung_tu")
def _c_hung_tu(B, p):
    if p not in (DAN, THAN) or B.chinh(p) != ["Liêm Trinh"]:
        return None
    cs = ["Mệnh %s có %s độc thủ" % (CHI[p], B.f("Liêm Trinh").rsplit(" ở", 1)[0])]
    yeu, ghi = [], []
    s = _sat_s(B, [p])
    if s:
        yeu.append("gia sát tại Mệnh (%s) – 'gia sát: bình thường'" % B.fl(s))
    hk = B.tim([p], ("Thiên Hình",)) + [(t, p) for t in B.hoa_o(p, "Hóa Kỵ")]
    if hk:
        yeu.append("gặp Hình/Kỵ: " + ", ".join(x for x, _ in hk))
    _tt_menh(B, p, yeu)
    if B.can in (0, 4, 6):
        ghi.append("tuổi %s: sách xếp tốt nhất" % CAN[B.can])
    return _r(cs, yeu, ghi=ghi)


@_cach("anh_tinh", "Anh tinh nhập miếu", "cát", "anh_tinh", than=False)
def _c_anh_tinh(B, p):
    if p not in (TY, NGO) or not B.co(p, "Phá Quân"):
        return None
    tp = B.tp(p)
    cs = ["Mệnh %s có %s" % (CHI[p], B.f("Phá Quân").rsplit(" ở", 1)[0])]
    yeu, pha, ghi = [], [], []
    xk = B.tim(tp, ("Văn Xương", "Văn Khúc"))
    if xk:
        pha.append("Phá Quân gặp Xương Khúc ở tam phương tứ chính: " + B.fl(xk))
    # rà soát 11/2026 (紫微樓, 全书 卷二): tứ sát đồng cung Mệnh là phá; Không Kiếp, Hóa Kỵ ở tam phương làm yếu;
    # tuổi Bính, Mậu "chủ khốn" (Kình ở Ngọ)
    s4 = _sat_s(B, [p], TU_SAT)
    if s4:
        pha.append("tứ sát tại Mệnh: " + B.fl(s4))
    s = _sat_s(B, tp)
    if len(s) >= 2 and not s4:
        yeu.append("sát tinh nặng: " + B.fl(s))
    kk = B.tim(tp, KHONG_KIEP) + B.tim_hoa(tp, "Hóa Kỵ")
    if kk:
        yeu.append("Không Kiếp / Hóa Kỵ ở tam phương: " + ", ".join("%s ở %s" % (x, CHI[q]) for x, q in kk))
    _tt_menh(B, p, yeu)
    if B.can in (0, 9):
        ghi.append("tuổi %s: sách xếp mạnh nhất" % CAN[B.can])
    elif B.can in (2, 4):
        yeu.append("tuổi %s: Toàn thư nói Bính, Mậu ở Tý Ngọ 'chủ khốn', giàu sang không lâu" % CAN[B.can])
    return _r(cs, yeu, pha, ghi)


@_cach("vu_thu", "Vũ Khúc thủ viên", "cát", "vu_thu", than=False)
def _c_vu_thu(B, p):
    if p not in (THIN, TUAT) or B.chinh(p) != ["Vũ Khúc"]:
        return None
    tp = B.tp(p)
    cs = ["Mệnh %s có %s độc tọa" % (CHI[p], B.f("Vũ Khúc").rsplit(" ở", 1)[0])]
    yeu, pha = [], []
    h = B.hoa.get("Vũ Khúc")
    if h == "Hóa Kỵ":
        yeu.append("Vũ Khúc Hóa Kỵ (tuổi Nhâm) – cần sao che chở")
    elif h:
        cs.append("Vũ Khúc %s" % h)
    if B.tim(tp, ("Linh Tinh",)) and B.tim(tp, ("Văn Xương",)) and B.tim(tp, ("Đà La",)):
        pha.append("Linh Xương Đà Vũ hội tam phương")
    s = _sat_s(B, [p], TU_SAT)
    if s:
        yeu.append("tứ sát tại Mệnh: " + B.fl(s))
    _tt_menh(B, p, pha)                     # tuvisonkhiem: Tuần, Triệt tại Mệnh là phá cách này (rà soát 11/2026)
    return _r(cs, yeu, pha)


@_cach("tham_vu", "Tham Vũ đồng hành", "cát", "tham_vu")
def _c_tham_vu(B, p):
    yeu, pha = [], []
    if p in (SUU, MUI) and B.co(p, "Vũ Khúc", "Tham Lang"):
        cs = ["Mệnh %s có Vũ Khúc + Tham Lang đồng cung" % CHI[p]]
    elif p in (SUU, MUI) and _muon_doi(B, p, "Vũ Khúc", "Tham Lang") is not None:
        cs = ["Mệnh %s vô chính diệu mượn Vũ Tham ở %s" % (CHI[p], CHI[(p + 6) % 12])]
        yeu.append("mượn chính tinh đối cung nên lực yếu")
    elif p in (THIN, TUAT) and B.chinh(p) in (["Vũ Khúc"], ["Tham Lang"]) and \
            {B.vt["Vũ Khúc"], B.vt["Tham Lang"]} == {p, (p + 6) % 12}:
        cs = ["Mệnh %s: %s, %s đối chiếu (tứ mộ)" % (CHI[p], B.f("Vũ Khúc"), B.f("Tham Lang"))]
        yeu.append("hai sao đối chiếu chứ không đồng cung")
    else:
        return None
    if B.tim([p], KHONG_KIEP):
        pha.append("Không Kiếp tại Mệnh: " + B.fl(B.tim([p], KHONG_KIEP)))
    ky = [t for t in ("Vũ Khúc", "Tham Lang") if B.hoa.get(t) == "Hóa Kỵ"]
    if ky:
        yeu.append("Hóa Kỵ ở " + ", ".join(ky))
    _tt_menh(B, p, yeu)
    return _r(cs, yeu, pha, ghi=["'Tham Vũ bất phát thiếu niên nhân' – thường phát muộn, sau khoảng 30 tuổi"])


@_cach("hoa_tham", "Hỏa Tham / Linh Tham", "cát", "hoa_tham", than=False)
def _c_hoa_tham(B, p):
    if not B.co(p, "Tham Lang"):
        return None
    ds = T.do_sang("Tham Lang", p)
    kq = []
    for sat, vung, ten in (("Hỏa Tinh", B.tp(p)[:3], "Tham Hỏa tương phùng (Hỏa Tham)"),
                           ("Linh Tinh", B.tp(p), "Tham Linh triều viên (Linh Tham)")):
        q = B.vt[sat]
        if q not in vung:
            continue
        if sat == "Linh Tinh" and p in (MAO, DAU):
            continue                    # Tham Linh ở Mão Dậu: sách không tính là cách
        cs = ["Mệnh %s có Tham Lang(%s), %s %s" % (CHI[p], ds, B.f(sat), "đồng cung" if q == p else "hội chiếu")]
        yeu, pha = [], []
        if p in (THIN, TUAT, SUU, MUI):
            cs.append("Tham ở tứ mộ – bản mạnh nhất")
        elif p in (DAN, THAN):
            yeu.append("Tham không ở tứ mộ")
        elif p in (MAO, DAU):
            yeu.append("Tham ở Mão Dậu (cùng Tử Vi): chỉ tốt khi không có sát tinh khác")
        else:
            pha.append("Tham Lang hãm – không thành nghĩa đẹp của cách")
        # rà soát 11/2026, theo tuvisonkhiem (nguồn của cách này): Tham Hỏa gặp Kình, Đà, Địa Kiếp hoặc Xương Khúc ở
        # tam phương là phá; Tham Linh gặp Kình Dương, Đào Hoa, hoặc Hóa Kỵ kèm Không Kiếp là phá
        tp = B.tp(p)
        if sat == "Hỏa Tinh":
            xau = B.tim(tp, ("Kình Dương", "Đà La", "Địa Kiếp", "Văn Xương", "Văn Khúc"))
        else:
            xau = B.tim(tp, ("Kình Dương",)) + B.tim([p], ("Đào Hoa",))
            if B.tim_hoa(tp, "Hóa Kỵ") and B.tim(tp, KHONG_KIEP):
                xau += B.tim(tp, KHONG_KIEP)
        # sách không nói rõ vị trí: ở Mệnh hoặc cùng cung Hỏa/Linh thì phá, ở cung khác của tam phương thì yếu
        xp = [(x, q2) for x, q2 in xau if q2 in (p, q)]
        xy = [(x, q2) for x, q2 in xau if q2 not in (p, q)]
        if xp:
            pha.append("gặp " + ", ".join("%s ở %s" % (x, CHI[q2]) for x, q2 in xp))
        if xy:
            yeu.append("tam phương có " + ", ".join("%s ở %s" % (x, CHI[q2]) for x, q2 in xy))
        o = [x for x in _sat_s(B, [p], ("Đà La", "Địa Không", "Địa Kiếp")) if x not in xau]
        if o:
            yeu.append("tại Mệnh có " + B.fl(o))
        _tt_menh(B, p, yeu)
        kv = B.kv(q)
        if kv and q != p:
            yeu.append("%s gặp %s" % (sat, "/".join(kv)))
        kq += _r(cs, yeu, pha, ghi=["chủ phát nhanh, bất ngờ; cần giữ nhịp để khỏi lên nhanh xuống nhanh"], ten=ten)
    return kq or None


@_cach("ma_dau", "Mã đầu đới kiếm", "trung", "ma_dau", than=False)
def _c_ma_dau(B, p):
    if p != NGO or not B.co(p, "Kình Dương"):
        return None
    cs = ["Mệnh Ngọ có Kình Dương(H) (tuổi %s); chính tinh: %s" % (CAN[B.can], B.fc(p))]
    loc = B.hoa_o(p, "Hóa Lộc")
    if B.co(p, "Thiên Đồng", "Thái Âm") or (B.co(p, "Tham Lang") and B.can == 4):
        yeu, ghi = [], []
        if loc:
            cs.append("có Hóa Lộc (%s) nuôi 'thanh kiếm'" % ", ".join(loc))
        else:
            yeu.append("thiếu Hóa Lộc")
        if B.co(p, "Tham Lang"):
            yeu.append("bản Tham Lang + Kình (tuổi Mậu): sách luận cát có điều kiện")
        q = B.tim_hoa(B.tp(p)[1:3], "Hóa Quyền")
        if [x for x in q if x[0] == "Thiên Cơ"]:
            cs.append("tam hợp có Thiên Cơ Hóa Quyền (đúng bản Đằng Sơn)")
        s = _sat_s(B, [p], ("Đà La", "Hỏa Tinh", "Linh Tinh", "Địa Không", "Địa Kiếp"))
        if s:
            yeu.append("thêm sát tinh: " + B.fl(s))
        _tt_menh(B, p, yeu)
        ghi.append("'Mã đầu đới kiếm, trấn ngự biên cương' – uy quyền nhưng sách nói khó bền lâu")
        return _r(cs, yeu, ghi=ghi, nhom="cát")
    ghi = (["Thất Sát + Kình ở Ngọ: sách nói khác nhau – có sách xếp gắt nhất, Vương Đình Chi coi là chính cách (cát)"]
           if B.co(p, "Thất Sát") else [])
    s = _sat_s(B, [p], ("Đà La", "Hỏa Tinh", "Linh Tinh", "Địa Không", "Địa Kiếp"))
    yeu = []
    if loc or B.cat_ds([p]):
        yeu.append("có cát tinh/Hóa Lộc tại Mệnh chế bớt")
    if s:
        cs.append("thêm sát tinh: " + B.fl(s))
    return _r(cs + ["không có bộ Đồng Âm/Tham + Lộc chế ngự – 'Kình thủ Mệnh tại Ngọ là hung nhất'"], yeu,
              ghi=ghi, ten="Mã đầu đới kiếm (thế hung)", nhom="hung")


@_cach("kinh_mieu", "Kình Dương nhập miếu", "cát", "kinh_mieu", than=False)
def _c_kinh_mieu(B, p):
    if p not in (THIN, TUAT, SUU, MUI) or not B.co(p, "Kình Dương"):
        return None
    q = (p + 6) % 12
    cs = ["Mệnh %s (tứ mộ) có Kình Dương(Đ) – tuổi %s; chính tinh: %s" % (CHI[p], CAN[B.can], B.fc(p))]
    yeu, pha = [], []
    if not B.vcd(p):
        c = B.chinh(p)
        if any(T.do_sang(x, p) == "H" for x in c):
            yeu.append("chính tinh tại Mệnh hãm")         # không sách nào coi là phá (rà soát 11/2026)
        else:
            yeu.append("Mệnh có chính tinh (chuẩn chặt đòi vô chính diệu)")
    ky = B.hoa_o(p, "Hóa Kỵ") + B.hoa_o(q, "Hóa Kỵ")
    kk = B.tim([p, q], KHONG_KIEP)
    if ky or kk:
        pha.append("Hóa Kỵ/Không Kiếp xung phạm Mệnh: " + ", ".join(ky + [x for x, _ in kk]))
    _tt_menh(B, p, yeu)                                  # tuvisonkhiem: Tuần, Triệt "giảm lực" – yếu, không phá
    if not B.cat_ds(B.tp(p)):
        yeu.append("thiếu cát tinh hỗ trợ")
    return _r(cs, yeu, pha, ghi=["quý cách thiên về võ nghiệp, kỷ luật"])


# ---------------------------------------------------------- 5. Lộc, Mã, Tứ hóa
@_cach("loc_ma", "Lộc Mã giao trì", "cát", "loc_ma")
def _c_loc_ma(B, p):
    tp = B.tp(p)
    lt, ma = B.vt["Lộc Tồn"], B.vt["Thiên Mã"]
    hl = [(t, q) for t, q in B.tim_hoa(tp, "Hóa Lộc")]
    if (lt == p and ma in tp) or (ma == p and lt in tp):
        loai = "Lộc Tồn"
        q_loc = lt
    elif ma in tp and any(q == p for _, q in hl) or (ma == p and hl):
        loai = "Hóa Lộc"
        q_loc = p if ma != p else hl[0][1]
    else:
        return None
    yeu, pha = [], []
    if loai == "Lộc Tồn":
        the = "đồng cung" if lt == ma else ("xung chiếu" if (p + 6) % 12 in (lt, ma) else "tam hợp")
        cs = ["%s và %s %s tại/về Mệnh %s" % (B.f("Lộc Tồn"), B.f("Thiên Mã"), the, CHI[p])]
        if the == "tam hợp":
            yeu.append("chỉ hội ở tam hợp (thế yếu nhất)")
        ten = "Lộc Mã giao trì"
    else:
        cs = ["Hóa Lộc và %s gặp nhau ở tam phương Mệnh %s" % (B.f("Thiên Mã"), CHI[p])]
        yeu.append("dùng Hóa Lộc thay Lộc Tồn (chỉ Ảo bí và một đoạn Toàn thư nhận)")
        ten = "Lộc Mã giao trì (Hóa Lộc)"
    kk = B.tim([q_loc], KHONG_KIEP)
    if kk:
        pha.append("Lộc gặp Không Kiếp: " + B.fl(kk))
    kv = B.kv(q_loc)
    if kv:
        pha.append("%s ở cung Lộc %s" % ("/".join(kv), CHI[q_loc]))
    kvm = B.kv(ma)
    if kvm:
        yeu.append("%s ở cung Mã %s" % ("/".join(kvm), CHI[ma]))
    # rà soát 11/2026: Lộc hoặc Mã bị Hóa Kỵ ở đối cung xung phá thì hỏng cách (Vương Đình Chi, tuvisonkhiem)
    kx = [(t, (q + 6) % 12) for q in {q_loc, ma} for t in B.hoa_o((q + 6) % 12, "Hóa Kỵ")]
    if kx:
        pha.append("Hóa Kỵ xung phá: " + ", ".join("%s Hóa Kỵ ở %s" % (t, CHI[q]) for t, q in kx))
    if B.co(ma, "Đà La") or B.co((ma + 6) % 12, "Đà La"):
        yeu.append("Đà La gặp Thiên Mã – 'chiết túc mã'")
    return _r(cs, yeu, pha, ten=ten, ghi=["được tiền nhờ di chuyển, buôn bán, làm xa"])


def _loc_o(B, ps):
    return [(x, q) for q in ps for x in B.loc(q)]


@_cach("song_loc", "Song Lộc triều viên", "cát", "song_loc")
def _c_song_loc(B, p):
    if B.loc(p):
        return None
    tp = B.tp(p)[1:]
    lst = _loc_o(B, tp)
    if not any(x == "Lộc Tồn" for x, _ in lst) or not any(x.startswith("Hóa Lộc") for x, _ in lst):
        return None
    cs = ["Mệnh %s không có Lộc; %s chiếu về" % (CHI[p], ", ".join("%s ở %s" % (x, CHI[q]) for x, q in lst))]
    pha = []
    for q in {q for _, q in lst}:
        kk = B.tim([q], KHONG_KIEP)
        if kk:
            pha.append("Lộc ở %s gặp %s" % (CHI[q], B.fl(kk)))
        kv = B.kv(q)
        if kv:
            pha.append("%s ở cung Lộc %s" % ("/".join(kv), CHI[q]))
    return _r(cs, pha=pha)


@_cach("uyen_uong", "Lộc hợp uyên ương", "cát", "uyen_uong")
def _c_uyen_uong(B, p):
    m = B.loc(p)
    if not m:
        return None
    lst = _loc_o(B, B.tp(p))
    has_lt = any(x == "Lộc Tồn" for x, _ in lst)
    has_hl = any(x.startswith("Hóa Lộc") for x, _ in lst)
    if not (has_lt and has_hl):
        return None
    cs = ["Mệnh %s có %s; tam phương: %s" % (CHI[p], ", ".join(m), ", ".join("%s ở %s" % (x, CHI[q])
                                                                           for x, q in lst if q != p) or "—")]
    if all(q == p for _, q in lst):
        cs.append("hai Lộc đồng cung tại Mệnh")
    pha, ghi, yeu = [], [], []
    bi = 0
    for q in sorted({q for _, q in lst}):
        kk = B.tim([q], KHONG_KIEP)
        kv = B.kv(q)
        ky = B.hoa_o((q + 6) % 12, "Hóa Kỵ")
        if kk or ky:
            bi += 1
            pha.append("Lộc ở %s gặp %s" % (CHI[q], ", ".join([x for x, _ in kk] + ["%s Hóa Kỵ xung" % t for t in ky])))
        if kv:            # tuvisonkhiem: Tuần Triệt chỉ hạ cách "từ tốt xuống khá" (rà soát 11/2026)
            yeu.append("Lộc ở %s gặp %s" % (CHI[q], "/".join(kv)))
    if bi >= 2 or (bi == 1 and len({q for _, q in lst}) == 1):
        ghi.append("cả hai Lộc đều bị phá: 'Lưỡng trùng Hoa Cái' – phát mạnh nhưng dễ mất trắng")
    if B.co(p, "Lộc Tồn"):
        ghi.append("Lộc Tồn ở Mệnh nên luôn bị Kình Đà kẹp – cái giá đi kèm")
    return _r(cs, yeu, pha=pha, ghi=ghi, ten="Lộc hợp uyên ương (Uyên ương Lộc hội)")


@_cach("minh_am", "Minh Lộc ám Lộc", "cát", "minh_am", than=False)
def _c_minh_am(B, p):
    m = B.loc(p)
    h = (1 - p) % 12            # cung nhị hợp (lục hợp)
    a = B.loc(h)
    if not m or not a:
        return None
    if not ({"Lộc Tồn"} & set(m + a)) or not [x for x in m + a if x.startswith("Hóa Lộc")]:
        return None
    cs = ["Mệnh %s có %s (minh Lộc); cung nhị hợp %s có %s (ám Lộc)" % (CHI[p], ", ".join(m), CHI[h], ", ".join(a))]
    pha = []
    for q in (p, h):
        kk = B.tim([q], KHONG_KIEP)
        kv = B.kv(q)
        if kk or kv:
            pha.append("%s gặp %s" % (CHI[q], ", ".join([x for x, _ in kk] + kv)))
    return _r(cs, pha=pha)


@_cach("tam_ky", "Tam kỳ gia hội", "cát", "tam_ky")
def _c_tam_ky(B, p):
    tp = B.tp(p)
    hs = {h: B.tim_hoa(tp, h) for h in CAT_HOA}
    if not all(hs.values()):
        return None
    cs = ["tam phương tứ chính đủ " + ", ".join("%s (%s ở %s)" % (h, t, CHI[q]) for h in CAT_HOA for t, q in hs[h])]
    yeu = []
    if not any(q == p for v in hs.values() for _, q in v):
        yeu.append("Mệnh không có sao Hóa nào (chuẩn chặt đòi một Hóa ở Mệnh)")
    ky = B.tim_hoa(tp, "Hóa Kỵ")
    if ky:
        yeu.append("Hóa Kỵ lọt vào tam phương: " + ", ".join("%s ở %s" % (t, CHI[q]) for t, q in ky))
    s = _sat_s(B, tp)
    if len(s) >= 3:
        yeu.append("sát tinh trùng phùng: " + B.fl(s))
    for v in hs.values():
        for t, q in v:
            if B.kv(q):
                yeu.append("%s gặp %s" % (t, "/".join(B.kv(q))))
    return _r(cs, yeu, ghi=["Tam kỳ là lực nâng, không giải được cách xấu khác"])


@_cach("giap_loc", "Song Lộc giáp / Khoa Quyền Lộc giáp", "cát", "giap_loc")
def _c_giap_loc(B, p):
    a, b = B.giap(p)

    def nhan(q):
        r = ["Lộc Tồn"] if B.co(q, "Lộc Tồn") else []
        return r + [h for h in CAT_HOA for _ in B.hoa_o(q, h)]
    na, nb = nhan(a), nhan(b)
    if not na or not nb:
        return None
    if ("Lộc Tồn" in na and "Hóa Lộc" in nb) or ("Lộc Tồn" in nb and "Hóa Lộc" in na):
        ten = "Song Lộc giáp mệnh"
    else:
        ha, hb = set(na) - {"Lộc Tồn"}, set(nb) - {"Lộc Tồn"}
        if not ha or not hb or len(ha | hb) < 2:
            return None
        ten = "Khoa Quyền Lộc giáp"
    cs = ["%s có %s, %s có %s kẹp cung %s" % (CHI[a], ", ".join(na), CHI[b], ", ".join(nb), CHI[p])]
    yeu, pha, ghi = [], [], []
    bi = [q for q in (a, b) if B.tim([q], KHONG_KIEP) or B.kv(q)]
    if len(bi) == 2:
        pha.append("cả hai bên kẹp gặp Không Kiếp/Tuần Triệt")
    elif bi:
        yeu.append("bên %s gặp Không Kiếp/Tuần Triệt" % CHI[bi[0]])
    if "Lộc Tồn" in na + nb:
        ghi.append("Lộc Tồn ở cạnh Mệnh nên Kình hoặc Đà rơi vào Mệnh – chính tinh Mệnh cần đủ vững")
    return _r(cs, yeu, pha, ghi, ten=ten)


@_cach("ta_huu", "Tả Hữu giáp mệnh / đồng cung", "cát", "ta_huu")
def _c_ta_huu(B, p):
    if p not in (SUU, MUI):
        return None
    a, b = B.giap(p)
    yeu = []
    if B.co(p, "Tả Phù", "Hữu Bật"):
        ten = "Tả Hữu đồng cung"
        cs = ["Tả Phù + Hữu Bật đồng cung tại %s (sinh tháng %d)" % (CHI[p], B.ls["thang"])]
        s = _sat_s(B, [p])
        if s:
            yeu.append("sát tinh đồng cung: " + B.fl(s))
    elif {B.vt["Tả Phù"], B.vt["Hữu Bật"]} == {a, b}:
        ten = "Tả Hữu giáp mệnh"
        cs = ["%s, %s kẹp cung %s" % (B.f("Tả Phù"), B.f("Hữu Bật"), CHI[p])]
        kk = B.tim([a, b], KHONG_KIEP)
        if kk:
            yeu.append("cung kẹp có " + B.fl(kk))
        for q in (a, b):
            if B.kv(q):
                yeu.append("%s ở %s" % ("/".join(B.kv(q)), CHI[q]))
    else:
        return None
    _tt_menh(B, p, yeu, "cung")
    c = B.chinh(p)
    if ten == "Tả Hữu giáp mệnh" and (not c or any(T.do_sang(x, p) == "H" for x in c)):
        yeu.append("cung ở giữa yếu (%s)" % B.fc(p))
    return _r(cs, yeu, ten=ten)


@_cach("xk_giap", "Xương Khúc giáp mệnh", "cát", "xk_giap")
def _c_xk_giap(B, p):
    if p not in (SUU, MUI):
        return None
    a, b = B.giap(p)
    if {B.vt["Văn Xương"], B.vt["Văn Khúc"]} != {a, b}:
        return None
    cs = ["%s, %s kẹp cung %s" % (B.f("Văn Xương"), B.f("Văn Khúc"), CHI[p])]
    yeu, pha = [], []
    _tt_menh(B, p, yeu, "cung")
    for q in (a, b):
        if B.kv(q) or B.hoa_o(q, "Hóa Kỵ"):
            yeu.append("cung kẹp %s gặp %s" % (CHI[q], ", ".join(B.kv(q) + ["Hóa Kỵ"] * bool(B.hoa_o(q, "Hóa Kỵ")))))
    kk = B.tim([p], KHONG_KIEP)
    if kk:
        yeu.append("Không Kiếp tại cung: " + B.fl(kk))
    if B.co(p, "Phá Quân"):
        pha.append("cung có Phá Quân (kỵ Xương Khúc)")
    return _r(cs, yeu, pha)


@_cach("van_que", "Văn Quế văn hoa", "cát", "van_que")
def _c_van_que(B, p):
    if p not in (SUU, MUI) or not B.co(p, "Văn Xương", "Văn Khúc"):
        return None
    cs = ["Văn Xương + Văn Khúc đồng cung tại %s" % CHI[p]]
    yeu, pha = [], []
    cat = [x for x in B.cat_ds(B.tp(p)) if not x.startswith("Văn ")]
    if cat:
        cs.append("cát tinh gia hội: " + ", ".join(cat))
    else:
        yeu.append("chưa có cát tinh khác gia hội")
    s = _sat_s(B, [p])
    ky = [t for t in ("Văn Xương", "Văn Khúc") if B.hoa.get(t) == "Hóa Kỵ"]
    if s or ky:
        pha.append("gặp hung sát: " + ", ".join([B.fl(s)] * bool(s) + ["%s Hóa Kỵ" % t for t in ky]))
    _tt_menh(B, p, yeu, "cung")
    return _r(cs, yeu, pha)


@_cach("phu_van", "Phụ củng văn tinh", "cát", "phu_van")
def _c_phu_van(B, p):
    tp = B.tp(p)
    if any(B.vt[x] not in tp for x in ("Tả Phù", "Hữu Bật", "Văn Xương", "Văn Khúc")):
        return None
    cs = ["tam phương tứ chính đủ %s, %s, %s, %s" % tuple(B.f(x) for x in ("Tả Phù", "Hữu Bật", "Văn Xương",
                                                                           "Văn Khúc"))]
    yeu, pha = [], []
    if B.co(p, "Phá Quân"):
        pha.append("Mệnh có Phá Quân gặp Xương Khúc")
    ky = [t for t in ("Văn Xương", "Văn Khúc") if B.hoa.get(t) == "Hóa Kỵ"]
    if ky:
        pha.append("%s Hóa Kỵ" % ", ".join(ky))
    for t in ("Văn Xương", "Văn Khúc", "Tả Phù", "Hữu Bật"):
        q = B.vt[t]
        o = B.tim([q], ("Kình Dương", "Đà La") + KHONG_KIEP)
        if o:
            yeu.append("%s gặp %s" % (t, ", ".join(x for x, _ in o)))
    if B.vcd(p):
        yeu.append("Mệnh vô chính diệu (sách cho là hơi kém)")
    _tt_menh(B, p, yeu)
    return _r(cs, yeu, pha)


@_cach("khoi_viet", "Thiên Ất củng mệnh / Khôi Việt giáp mệnh", "cát", "khoi_viet")
def _c_khoi_viet(B, p):
    k, v = B.vt["Thiên Khôi"], B.vt["Thiên Việt"]
    tp = B.tp(p)
    yeu, pha = [], []
    if (k == p and v in tp[1:]) or (v == p and k in tp[1:]):
        ten = "Thiên Ất củng mệnh (Tọa quý hướng quý)"
        cs = ["%s, %s: một sao tọa, một sao chiếu Mệnh %s" % (B.f("Thiên Khôi"), B.f("Thiên Việt"), CHI[p])]
        kv = B.kv(p)
        kk = B.tim([p], KHONG_KIEP)
        if kv or kk:
            pha.append("Mệnh gặp %s – chắn đường quý nhân" % ", ".join(kv + [x for x, _ in kk]))
        if B.hoa_o(p, "Hóa Kỵ"):
            pha.append("Hóa Kỵ tại Mệnh")          # tuvisonkhiem: Hóa Kỵ là phá (rà soát 11/2026)
        if not [x for x in B.cat_ds(tp) if not x.startswith("Thiên ")]:
            yeu.append("thiếu cát tinh khác (Xương Khúc, Khoa, Tả Hữu)")
    elif {k, v} == set(B.giap(p)):
        ten = "Khôi Việt giáp mệnh"
        cs = ["%s, %s kẹp cung %s" % (B.f("Thiên Khôi"), B.f("Thiên Việt"), CHI[p])]
        for q in B.giap(p) + [p]:
            o = B.kv(q) + [x for x, _ in B.tim([q], KHONG_KIEP)]
            if o:
                yeu.append("%s gặp %s" % (CHI[q], ", ".join(o)))
    else:
        return None
    return _r(cs, yeu, pha, ten=ten)


@_cach("vcd", "Mệnh vô chính diệu", "trung", "vcd", than=False)
def _c_vcd(B, p):
    if not B.vcd(p):
        return None
    q = (p + 6) % 12
    cs = ["Mệnh %s vô chính diệu; mượn chính tinh đối cung %s: %s (lực khoảng 7 phần)" % (CHI[p], CHI[q], B.fc(q))]
    kq = _r(cs, ghi=["luận theo chính tinh đối cung và các sao tại Mệnh"])
    tp = B.tp(p)
    loai = set()
    if set(tp) & B.tuan:
        loai.add("Tuần")
    if set(tp) & B.triet:
        loai.add("Triệt")
    for x, _ in B.tim(tp, ("Thiên Không", "Địa Không")):
        loai.add(x)
    tai_menh = B.kv(p) + [x for x, _ in B.tim([p], ("Thiên Không", "Địa Không"))]
    if len(loai) >= 3 and tai_menh:
        kq += _r(["Mệnh vô chính diệu gặp các sao Không: %s (tại Mệnh: %s)" % (", ".join(sorted(loai)),
                                                                             ", ".join(tai_menh))],
                 ghi=["'Mệnh vô chính diệu đắc Tam Không' – sách cho là phú quý khả kỳ"],
                 ten="Mệnh vô chính diệu đắc Tam Không", nhom="cát")
    kk = B.tim(tp, KHONG_KIEP)
    if {x for x, _ in kk} == set(KHONG_KIEP) and B.tim([p], KHONG_KIEP):
        yeu = []
        if any(T.do_sang(x, q2) != "Đ" for x, q2 in B.tim([p], KHONG_KIEP)):
            yeu.append("Không/Kiếp tại Mệnh không đắc địa (đắc ở Dần Thân Tỵ Hợi)")
        if not B.cat_ds(tp):
            yeu.append("không có cát tinh – sách khác xếp vào cách nghèo")
        kq += _r(["Mệnh vô chính diệu có " + B.fl(kk)], yeu,
                 ghi=["nhiều ý tưởng, thăng trầm mạnh; các sách đánh giá khác nhau"],
                 ten="Mệnh vô chính diệu đắc Không Kiếp", nhom="trung")
    return kq


# ---------------------------------------------------------- 6. hung cách
@_cach("kd_giap", "Kình Đà giáp mệnh", "hung", "kd_giap")
def _c_kd_giap(B, p):
    if B.vt["Lộc Tồn"] != p:
        return None
    cs = ["Lộc Tồn ở %s nên %s, %s kẹp hai bên" % (CHI[p], B.f("Kình Dương"), B.f("Đà La"))]
    yeu = []
    ky = B.hoa_o(p, "Hóa Kỵ")
    if ky:
        return _r(cs + ["Hóa Kỵ (%s) đồng cung Lộc Tồn" % ", ".join(ky)], ten="Kình Đà giáp Kỵ")
    c = B.chinh(p)
    if c and not any(T.do_sang(x, p) == "H" for x in c):
        yeu.append("chính tinh vững (%s), Lộc Tồn vẫn giữ được của" % B.fc(p))
    if B.tim([p], KHONG_KIEP):
        cs.append("Lộc Tồn lại gặp " + B.fl(B.tim([p], KHONG_KIEP)))
    return _r(cs, yeu)


@_cach("kk_giap", "Không Kiếp giáp mệnh", "hung", "kk_giap")
def _c_kk_giap(B, p):
    if {B.vt["Địa Không"], B.vt["Địa Kiếp"]} != set(B.giap(p)):
        return None
    cs = ["%s, %s kẹp cung %s (%s)" % (B.f("Địa Không"), B.f("Địa Kiếp"), CHI[p], B.fc(p))]
    yeu = []
    c = B.chinh(p)
    if c and all(T.do_sang_day_du(x, p) in ("M", "V") for x in c):      # Thiên Phủ lấy bảng hiển thị (11/2026)
        yeu.append("chính tinh miếu vượng chịu được")
    return _r(cs, yeu)


@_cach("hl_giap", "Hỏa Linh giáp mệnh", "hung", "hl_giap")
def _c_hl_giap(B, p):
    if {B.vt["Hỏa Tinh"], B.vt["Linh Tinh"]} != set(B.giap(p)):
        return None
    cs = ["%s, %s kẹp cung %s (%s)" % (B.f("Hỏa Tinh"), B.f("Linh Tinh"), CHI[p], B.fc(p))]
    yeu = []
    c = set(B.chinh(p))
    for bo in ({"Vũ Khúc", "Thất Sát"}, {"Vũ Khúc", "Thiên Phủ"}, {"Liêm Trinh", "Thất Sát"}, {"Tử Vi", "Thất Sát"}):
        if c == bo:
            yeu.append("cung có %s – gian lao nhưng vẫn phấn chấn" % " + ".join(sorted(bo)))
    if B.co(p, "Kình Dương"):
        cs.append("có thêm Kình Dương – cần xét kỹ")
    return _r(cs, yeu)


@_cach("hinh_ky", "Hình Kỵ giáp ấn", "hung", "hinh_ky")
def _c_hinh_ky(B, p):
    if not B.co(p, "Thiên Tướng"):
        return None
    a, b = B.giap(p)
    kq = []
    for x, y in ((a, b), (b, a)):
        ky = B.hoa_o(y, "Hóa Kỵ")
        if not ky:
            continue
        if B.co(x, "Kình Dương"):
            kq = _r(["Thiên Tướng ở %s; %s bên này, %s Hóa Kỵ ở %s bên kia" % (
                CHI[p], B.f("Kình Dương"), ", ".join(ky), CHI[y])])
            break
        if B.co(x, "Thiên Hình"):
            kq = _r(["Thiên Tướng ở %s; Thiên Hình ở %s, %s Hóa Kỵ ở %s" % (CHI[p], CHI[x], ", ".join(ky), CHI[y])],
                    ["'Hình' đọc là Thiên Hình (sách khác đọc là Kình Dương)"])
    if not kq and B.co(p, "Liêm Trinh") and p in (TY, NGO):
        k = B.vt["Kình Dương"]
        if k in (p, a, b):
            kq = _r(["Liêm Trinh + Thiên Tướng ở %s gặp %s" % (CHI[p], B.f("Kình Dương"))],
                    ghi=["dễ vướng kiện tụng, thị phi"], ten="Hình tù giáp ấn")
    return kq or None


@_cach("loc_pha", "Lộc phùng xung phá", "hung", "loc_pha")
def _c_loc_pha(B, p):
    m = B.loc(p)
    if not m:
        return None
    q = (p + 6) % 12
    bi = []
    for x, q2 in B.tim([p], KHONG_KIEP):
        bi.append("%s đồng cung" % x)
    for x, q2 in B.tim([q], KHONG_KIEP):
        bi.append("%s xung từ %s" % (x, CHI[q]))
    if B.hoa_o(p, "Hóa Kỵ"):
        bi.append("Hóa Kỵ đồng cung")
    if B.hoa_o(q, "Hóa Kỵ"):
        bi.append("Hóa Kỵ xung từ %s" % CHI[q])
    bi += ["%s tại Mệnh" % x for x in B.kv(p)]
    if not bi:
        return None
    cs = ["%s ở %s gặp: %s" % (", ".join(m), CHI[p], ", ".join(bi))]
    yeu, ghi = [], ["'cát xứ tàng hung' – thường được trước mất sau"]
    # Rà soát 11/2026: Hóa Lộc bị Hóa Kỵ ở đối cung là định nghĩa gốc và thế nặng nhất (Vương Đình Chi; 斗數宣微) –
    # không giảm; Lộc Tồn bị Hóa Kỵ xung thì "quan hệ rất nhẹ".
    hl_ky_xung = any(x.startswith("Hóa Lộc") for x in m) and any(x.startswith("Hóa Kỵ xung") for x in bi)
    if len(bi) == 1 and "đồng cung" not in bi[0] and not hl_ky_xung:
        yeu.append("chỉ một tác nhân và không đồng cung" + (
            " (Lộc Tồn bị Hóa Kỵ xung – sách nói nhẹ)" if bi[0].startswith("Hóa Kỵ xung") else ""))
    if len(m) >= 2 and B.tim([p], KHONG_KIEP):
        ghi.append("cả hai Lộc cùng bị phá: 'Lưỡng trùng Hoa Cái'")
    return _r(cs, yeu, ghi=ghi)


@_cach("luong_ma", "Lương Mã phiêu đãng", "hung", "luong_ma", than=False)
def _c_luong_ma(B, p):
    if p not in (TI, HOI) or not B.co(p, "Thiên Lương"):
        return None
    ma = B.vt["Thiên Mã"]
    if ma == p:
        cs, yeu = ["Thiên Lương(H) + Thiên Mã đồng cung tại %s" % CHI[p]], []
    elif ma == (p + 6) % 12:
        # thế Mã ở Thiên Di chỉ có ở 斗數宣微, và sách này đòi có sát tinh, không có cát tinh (rà soát 11/2026)
        if not (_sat_s(B, B.tp(p)) or B.tim_hoa(B.tp(p), "Hóa Kỵ")) or B.cat_ds(B.tp(p)):
            return None
        cs, yeu = ["Thiên Lương(H) ở %s, Thiên Mã xung chiếu từ %s, có sát, không cát tinh" % (CHI[p], CHI[ma])], \
            ["Mã ở xung chiếu"]
    else:
        return None
    s = _sat_s(B, B.tp(p))
    if len(s) >= 2:
        cs.append("nhiều sát tinh (%s) – dễ nghèo, lênh đênh" % B.fl(s))
    return _r(cs, yeu, ghi=["nay đây mai đó, khó ổn định chỗ ở và việc làm"])


@_cach("liem_tham", "Liêm Tham Tỵ Hợi", "hung", "liem_tham")
def _c_liem_tham(B, p):
    if p not in (TI, HOI):
        return None
    goc, yeu = p, []
    if not B.co(p, "Liêm Trinh", "Tham Lang"):
        q = _muon_doi(B, p, "Liêm Trinh", "Tham Lang")
        if q is None:
            return None
        goc = q
        yeu.append("Mệnh vô chính diệu mượn Liêm Tham đối cung – nhẹ hơn")
    cs = ["Liêm Trinh(H) + Tham Lang(H) ở %s" % CHI[goc]]
    ghi = []
    kv = B.kv(p)
    if kv:
        yeu.append("%s tại Mệnh – 'phản vi kỳ cách', hóa giải tính hung" % "/".join(kv))
    if B.hoa.get("Liêm Trinh") == "Hóa Kỵ":
        yeu.append("Liêm Trinh Hóa Kỵ (tuổi Bính) – sách nói lại giải bớt hung")
    cat = B.tim(B.tp(p), ("Tả Phù", "Hữu Bật", "Thiên Khôi", "Thiên Việt")) + B.tim_hoa(B.tp(p), "Hóa Quyền")
    if cat:
        yeu.append("có cát tinh/quyền tinh nâng đỡ: " + ", ".join("%s ở %s" % (x, CHI[q]) for x, q in cat))
    if goc == HOI:
        ghi.append("ở Hợi tốt hơn ở Tỵ")
    if B.tim([goc], ("Văn Xương", "Văn Khúc")):
        ghi.append("gặp Xương Khúc: dễ hư danh")
    return _r(cs, yeu, ghi=ghi)


@_cach("cu_hoa", "Cự Hỏa Kình Dương (Cự phùng tứ sát)", "hung", "cu_hoa")
def _c_cu_hoa(B, p):
    if not B.co(p, "Cự Môn"):
        return None
    tp = B.tp(p)
    dao = B.tim(tp, ("Kình Dương", "Đà La"))
    lua = B.tim(tp, ("Hỏa Tinh", "Linh Tinh"))
    if not dao or not lua:
        return None
    kk = B.tim(tp, KHONG_KIEP)
    du4 = all(B.vt[x] in tp for x in ("Kình Dương", "Đà La", "Hỏa Tinh", "Linh Tinh"))
    hoa_kinh = B.vt["Hỏa Tinh"] in tp and B.vt["Kình Dương"] in tp
    yeu = []
    # Rà soát 11/2026: 骨髓赋 "巨火擎羊" đòi đúng Hỏa Tinh + Kình Dương; "Cự phùng tứ sát" đòi đủ Kình Đà Hỏa Linh
    # (phi tinh tứ hóa, 紫微樓); tuvisonkhiem tính ba nhóm (Kình/Đà, Hỏa/Linh, Không/Kiếp) – để mức yếu.
    if du4:
        ten = "Cự phùng tứ sát"
        cs = ["Cự Môn thủ %s; tam phương đủ Kình, Đà, Hỏa, Linh: %s" % (CHI[p], B.fl(dao + lua))]
    elif hoa_kinh:
        ten = "Cự Hỏa Kình Dương"
        cs = ["Cự Môn thủ %s gặp %s" % (CHI[p], B.fl([(x, B.vt[x]) for x in ("Hỏa Tinh", "Kình Dương")]))]
        if not (B.co(p, "Hỏa Tinh") and B.co(p, "Kình Dương")):
            yeu.append("Hỏa, Kình chỉ hội chiếu, không cùng ngồi Mệnh")
    elif kk:
        ten = "Cự phùng tứ sát"
        cs = ["Cự Môn thủ %s; tam phương có ba nhóm sát: %s" % (CHI[p], B.fl(dao + lua + kk))]
        yeu.append("chỉ đủ ba nhóm sát kể cả Không Kiếp (cách tính của tuvisonkhiem); sách cổ đòi đủ Kình Đà Hỏa Linh")
    else:
        return None
    h = B.hoa.get("Cự Môn")
    if h in ("Hóa Lộc", "Hóa Quyền"):
        yeu.append("Cự Môn %s – sách nói có thể thành cách" % h)
    elif h == "Hóa Kỵ":
        cs.append("Cự Môn Hóa Kỵ dẫn động – nặng hơn")
    return _r(cs, yeu, ten=ten, ghi=["tính nóng, dễ thị phi; cần giữ lời, tránh tranh chấp"])


@_cach("lxdv", "Linh Xương Đà Vũ", "hung", "lxdv")
def _c_lxdv(B, p):
    if p not in (THIN, TUAT):
        return None
    tp = B.tp(p)
    if any(B.vt[x] not in tp for x in ("Linh Tinh", "Văn Xương", "Đà La", "Vũ Khúc")):
        return None
    cs = ["Mệnh %s, tam phương hội %s" % (CHI[p], B.fl([(x, B.vt[x]) for x in ("Linh Tinh", "Văn Xương", "Đà La",
                                                                              "Vũ Khúc")]))]
    return _r(cs, ghi=["sách khuyên đề phòng sông nước, xe cộ trong các hạn kích động"])


# ------------------------------------------------------------------ nhận diện
MUC = ("thành cách", "cách yếu", "phá cách")
NHOM = ("cát", "trung", "hung")
_THU_TU_NHOM = {"cát": 0, "trung": 1, "hung": 2}


_RE_MENH = re.compile(r"\bMệnh\b(?! vô chính diệu đắc)")


def _hoan_tat(c, d, nhan, p):
    yeu, pha = d["yeu"], d["pha"]
    nhom = d.get("nhom", c["nhom"])
    muc = "phá cách" if pha else ("cách yếu" if yeu else "thành cách")
    if nhom == "hung" and muc == "phá cách":
        muc = "cách yếu"
    phan = list(d["co_so"])
    if not nhan.startswith("Mệnh"):          # xét ở cung Thân / cung hạn: gọi là 'cung' cho khỏi nhầm
        phan = [_RE_MENH.sub("cung", x) for x in phan]
        yeu = [_RE_MENH.sub("cung", x) for x in yeu]
        pha = [_RE_MENH.sub("cung", x) for x in pha]
        d = dict(d, ghi=[_RE_MENH.sub("cung", x) for x in d["ghi"]])
    if yeu:
        phan.append(("được giảm: " if nhom == "hung" else "giảm: ") + "; ".join(yeu))
    if pha:
        phan.append("phá: " + "; ".join(pha))
    if d["ghi"]:
        phan.append("ghi chú: " + "; ".join(d["ghi"]))
    return dict(ten=d.get("ten", c["ten"]), nhom=nhom, muc=muc, cung=nhan, ly_do=". ".join(phan),
                nguon=c["nguon"], vi_tri=p, ma=c["ma"])


def _xet(B, p, nhan, chi_menh=True):
    kq = []
    for c in CACH:
        if not chi_menh and not c["than"]:
            continue
        r = c["ham"](B, p)
        for d in r or ():
            kq.append(_hoan_tat(c, d, nhan, p))
    return kq


def nhan_dien(ls, cung_goc=None, nhan=None):
    """Nhận diện cách cục.
    - cung_goc None: xét cung Mệnh (với tam phương tứ chính), cung Thân (nếu khác Mệnh) và cách đặc thù cung Tài.
    - cung_goc = p: xét cung p như 'Mệnh' (dùng cho đại hạn / tiểu hạn); nhan là nhãn cung in ra.
    Trả list dict {ten, nhom, muc, cung, ly_do, nguon} (thêm vi_tri, ma để kiểm tra)."""
    B = _ban(ls)
    if cung_goc is not None:
        return _xet(B, cung_goc % 12, nhan or B.ten_cung(cung_goc % 12))
    m, t = ls["menh"], ls["than"]
    kq = _xet(B, m, "Mệnh (%s)" % CHI[m])
    if t != m:
        kq += _xet(B, t, "Thân cư %s (%s)" % (T.ten_cung(ls, t), CHI[t]), chi_menh=False)
    # cách đặc thù sách nêu rõ cho cung Tài Bạch: Vũ Tham ở Tài được Nhật Nguyệt kẹp
    tai = (m + 8) % 12
    if B.co(tai, "Vũ Khúc", "Tham Lang"):
        c = [x for x in CACH if x["ma"] == "nn_giap"][0]
        for d in c["ham"](B, tai) or ():
            d["ten"] = "Nhật Nguyệt giáp Tài (cung Tài Bạch)"
            kq.append(_hoan_tat(c, d, "Tài Bạch (%s)" % CHI[tai], tai))
    return kq


def _sap(kq):
    return sorted(kq, key=lambda r: (_THU_TU_NHOM[r["nhom"]], MUC.index(r["muc"]), r["ten"]))


def in_bang(kq, tieu_de):
    """In bảng Markdown: Cách | Nhóm | Mức | Cung | Căn cứ, kèm danh sách nguồn."""
    print(tieu_de)
    if not kq:
        print("- Không nhận diện được cách nào trong danh mục.")
        print()
        return
    nguon = []
    print("| Cách | Nhóm | Mức | Cung | Căn cứ |")
    print("|---|---|---|---|---|")
    for r in kq:
        if r["nguon"] not in nguon:
            nguon.append(r["nguon"])
        print("| %s | %s | %s | %s | %s [%d] |" % (r["ten"], r["nhom"], r["muc"], r["cung"],
                                                 r["ly_do"].replace("|", "/"), nguon.index(r["nguon"]) + 1))
    print("Nguồn đối chiếu:")
    for i, n in enumerate(nguon, 1):
        print("[%d] %s" % (i, n))
    print()


# ------------------------------------------------------------------ lập lá số từ thông tin sinh
def lap_tu_tt(tt):
    """Lập lá số (dict của tuvi_vn.lap_la_so) từ ThongTinSinh của tvbt, làm đúng như tvbt.tu_vi:
    sinh 23h-24h tính giờ Tý của ngày hôm sau; tháng nhuận ngày 16 trở đi tính sang tháng sau; số ngày tháng âm
    theo lịch đang dùng. Thêm các khóa: nam_am, thang_am_goc, ngay_am, nhuan, ty_muon."""
    import tvbt as B
    if not tt.co_gio:
        raise SystemExit("LỖI: cần giờ sinh để an cung Mệnh (Tử vi).")
    t = tt.t_dia_phuong
    ngay = t.date()
    ty_muon = t.hour == 23
    if ty_muon:
        ngay = ngay + dt.timedelta(days=1)
    gio = 0 if ty_muon else B.chi_gio(t)
    d, m, y, nhuan = B.duong_sang_am(ngay, tt.lich_tz)
    so_ngay = B.do_dai_thang_am(d, m, y, nhuan, tt.lich_tz)
    can, chi = (y - 4) % 10, (y - 4) % 12
    ls = T.lap_la_so(m, d, gio, can, chi, tt.gioi, so_ngay, nhuan)
    ls.update(nam_am=y, thang_am_goc=m, ngay_am=d, nhuan=nhuan, ty_muon=ty_muon)
    return ls


def _lap_nhanh(ngay, gio24, gioi):
    """Lập lá số nhanh cho kiểm thử: giờ đồng hồ coi như giờ địa phương, lịch theo thời kỳ (miền Bắc)."""
    import lich_vn as L
    if gio24 == 23:
        ngay = ngay + dt.timedelta(days=1)
    gio = 0 if gio24 == 23 else ((gio24 + 1) // 2) % 12
    tz = 8 if ngay < dt.date(1968, 1, 1) else 7          # lịch âm miền Bắc theo thời kỳ
    d, m, y, nhuan = L.solar_to_lunar(ngay.day, ngay.month, ngay.year, tz)
    can, chi = (y - 4) % 10, (y - 4) % 12
    ls = T.lap_la_so(m, d, gio, can, chi, gioi, 30, nhuan)
    ls.update(nam_am=y)
    return ls


# ------------------------------------------------------------------ CLI
def them_lenh(sub):
    import nc
    p = sub.add_parser("cachcuc", help="nhận diện cách cục Tử vi (cách an Việt Nam) trên lá số gốc và hạn")
    nc.them_tham_so_sinh(p)
    p.add_argument("--nam-xem", type=int, help="xét thêm cách trên cung đại hạn và tiểu hạn của năm này")
    p.add_argument("--tan-suat", type=int, metavar="N",
                   help="(kiểm tra) in tần suất mỗi cách trên N lá số ngẫu nhiên 1930-2020 rồi thoát")
    p.set_defaults(_chay=chay)


def _in_dau(tt, ls):
    print("THÔNG TIN SINH")
    print("- Giờ đồng hồ %s (UTC%+g), nơi sinh %s; giờ dùng an sao: %s (%s) → giờ %s" % (
        tt.dong_ho.strftime("%H:%M %d/%m/%Y"), tt.utc_off, tt.noi, tt.t_dia_phuong.strftime("%H:%M"),
        "mặt trời thực" if tt.dung_tst else "đồng hồ", CHI[ls["gio"]]))
    print("- Âm lịch: ngày %d tháng %d%s năm %s %s (%d)%s; %s" % (
        ls["ngay_am"], ls["thang_am_goc"], " nhuận" if ls["nhuan"] else "", CAN[ls["can"]], CHI[ls["chi"]],
        ls["nam_am"], " – sinh 23h-24h: tính giờ Tý ngày hôm sau" if ls["ty_muon"] else "",
        "Nam" if tt.gioi == "nam" else "Nữ"))
    Bn = _ban(ls)
    print("- Mệnh tại %s (%s); Thân cư %s (%s); %s; Tuần %s–%s, Triệt %s–%s" % (
        CHI[ls["menh"]], Bn.fc(ls["menh"]), T.ten_cung(ls, ls["than"]), CHI[ls["than"]], T.TEN_CUC[ls["cuc"]],
        *[CHI[i] for i in ls["tuan"] + ls["triet"]]))
    if ls["nhuan"] and ls["thang"] != ls["thang_am_goc"]:
        print("- Tháng nhuận, sinh từ ngày 16: an sao như tháng %d (cách phổ biến)." % ls["thang"])
    for c in tt.canh_bao:
        print("! " + c)
    print()


def chay(a):
    if a.tan_suat:
        in_tan_suat(a.tan_suat)
        return
    if not a.ngay or not a.gio:
        raise SystemExit("LỖI: cachcuc cần --ngay YYYY-MM-DD và --gio HH:MM (giờ sinh).")
    if not a.gioi:
        raise SystemExit("LỖI: cachcuc cần --gioi nam hoặc --gioi nu (chiều đại hạn, Hỏa Linh phụ thuộc giới tính).")
    import nc
    tt = nc.thoi_diem(a)
    ls = lap_tu_tt(tt)
    _in_dau(tt, ls)
    in_bang(_sap(nhan_dien(ls)), "CÁCH CỤC TỬ VI – LÁ SỐ GỐC (cung Mệnh, Thân; tam phương tứ chính)")
    if a.nam_xem:
        in_han(ls, a.nam_xem)
    print("(Mức: thành cách = đủ điều kiện; cách yếu = đủ cấu trúc nhưng thiếu phẩm chất, hoặc với cách hung là "
          "đã được giảm; phá cách = cấu trúc có nhưng bị phá. Cách là tín hiệu tổng quát, phải luận cùng toàn lá số.)")


def in_han(ls, nam_xem):
    """In cách cục trên cung đại hạn và tiểu hạn của năm xem, kèm sao lưu chạm tam phương cung hạn."""
    nc_, nz = (nam_xem - 4) % 10, (nam_xem - 4) % 12
    tuoi = nam_xem - ls["nam_am"] + 1
    if tuoi < 1:
        print("! Năm xem %d trước năm sinh âm lịch %d – bỏ qua phần hạn." % (nam_xem, ls["nam_am"]))
        return
    vh = T.van_han(ls, nc_, nz, tuoi)
    B = _ban(ls)
    cac_han = []
    if vh["dai_han"] is not None:
        a_, b_ = ls["dai_han"][vh["dai_han"]]
        cac_han.append(("Đại hạn %d-%d" % (a_, b_), vh["dai_han"]))
    else:
        print("! Tuổi mụ %d chưa vào hoặc đã quá các đại hạn của lá số." % tuoi)
    cac_han.append(("Tiểu hạn %d" % nam_xem, vh["tieu_han"]))
    for nhan, p in cac_han:
        kq = nhan_dien(ls, cung_goc=p, nhan="%s: %s" % (nhan, B.ten_cung(p)))
        in_bang(_sap(kq), "CÁCH CỤC TRÊN CUNG %s – %s (năm %s %s %d, tuổi mụ %d; xét cung hạn như Mệnh, sao gốc)"
                % (nhan.upper(), B.ten_cung(p), CAN[nc_], CHI[nz], nam_xem, tuoi))
        tp = B.tp(p)
        luu = ["%s %s ở %s" % (h, s, CHI[ls["vt"][s]]) for h, s in vh["hoa"] if ls["vt"][s] in tp]
        luu += ["%s ở %s" % (k, CHI[q]) for k, q in vh["luu"].items()
                if k in ("Lưu Lộc Tồn", "Lưu Kình Dương", "Lưu Đà La", "Lưu Thiên Mã") and q in tp]
        print("- Sao lưu năm %d chạm tam phương cung hạn: %s" % (nam_xem, ", ".join(luu) or "không có"))
        if any(x.startswith("Hóa Kỵ") for x in luu):
            print("! Lưu Hóa Kỵ vào tam phương cung hạn: cách tốt của hạn này dễ giảm, nên thận trọng việc lớn.")
        print()


# ------------------------------------------------------------------ tần suất và tự kiểm
def _ngau_nhien(n, seed=2026):
    rnd = random.Random(seed)
    d0 = dt.date(1930, 1, 1)
    so = (dt.date(2020, 12, 31) - d0).days
    for _ in range(n):
        yield _lap_nhanh(d0 + dt.timedelta(days=rnd.randrange(so + 1)), rnd.randrange(24), rnd.choice(("nam", "nu")))


def tan_suat(n=5000, seed=2026):
    """Đếm số lá số (trên n lá số ngẫu nhiên 1930-2020) có mỗi cách tại cung Mệnh; trả (dict, lỗi)."""
    dem, loi = {}, []
    for ls in _ngau_nhien(n, seed):
        try:
            kq = nhan_dien(ls)
        except Exception as e:      # noqa: BLE001
            loi.append("ngoại lệ %r (năm %d)" % (e, ls["nam_am"]))
            continue
        for ten in {r["ten"] for r in kq if r["cung"].startswith("Mệnh")}:
            dem[ten] = dem.get(ten, 0) + 1
    return dem, loi


def in_tan_suat(n):
    dem, loi = tan_suat(n)
    print("TẦN SUẤT CÁCH CỤC TẠI CUNG MỆNH TRÊN %d LÁ SỐ NGẪU NHIÊN 1930-2020" % n)
    print("| Cách | Số lá số | Tỷ lệ |")
    print("|---|---|---|")
    for ten, k in sorted(dem.items(), key=lambda x: -x[1]):
        print("| %s | %d | %.2f%% |" % (ten, k, 100.0 * k / n))
    for x in loi[:10]:
        print("! " + x)
    print()


def _ls_tham_so(thang, gio, can=0, chi=0, ngay=1, gioi="nam"):
    return T.lap_la_so(thang, ngay, gio, can, chi, gioi)


def _co(ls, ten_dau, cung="Mệnh"):
    return [r for r in nhan_dien(ls) if r["ten"].startswith(ten_dau) and r["cung"].startswith(cung)]


# Lá số mẫu có ngày giờ sinh (Hà Nội): ngày giờ được chọn sao cho rơi đúng các thế mà nguồn nêu rõ
# (bảng tháng–giờ, can năm, vị trí sao trong các trang tuvisonkhiem.vn đã dẫn ở NGUON); lập qua toàn bộ chuỗi
# doc_dau_vao -> lap_tu_tt để kiểm cả phần đổi lịch.
LA_SO_MAU = [
    # (ngày dương, giờ đồng hồ, giới, tên cách phải có tại Mệnh, cung Mệnh, mức chờ đợi hoặc None, căn cứ nguồn)
    ("1990-03-29", "04:00", "nam", "Phụ củng văn tinh", DAN, "thành cách",
     "tsk phu-cung-van-tinh: tháng 3 giờ Dần, Mệnh Dần; Tả Phụ, Văn Khúc ở Ngọ; Hữu Bật, Văn Xương ở Thân"),
    ("1991-09-10", "16:00", "nu", "Xương Khúc giáp mệnh", SUU, None,
     "tsk giap-xuong-giap-khuc: tháng 8 giờ Thân, Mệnh Sửu"),
    ("1992-05-03", "20:00", "nam", "Tả Hữu đồng cung", MUI, None,
     "tsk giap-ta-giap-huu: Tả Hữu đồng cung Mệnh Sửu/Mùi khi sinh tháng 4 hoặc 10"),
    ("1993-03-23", "18:00", "nu", "Tả Hữu giáp mệnh", MUI, "cách yếu",
     "tsk giap-ta-giap-huu: tháng 3 – Không/Kiếp đóng cùng Hữu Bật ở cung kẹp (3 trong 4 tổ hợp)"),
    ("1985-02-15", "04:00", "nam", "Thiên Ất củng mệnh", TY, None,
     "tsk thien-at-cung-menh: tuổi Ất, Khôi Tý – Việt Thân, Mệnh Tý (ngày này đã là tháng Giêng Ất Sửu theo "
     "lịch Việt Nam, còn là năm Giáp Tý theo lịch Trung Quốc)"),
    ("1983-04-13", "06:00", "nu", "Kình Dương nhập miếu", SUU, "phá cách",
     "tsk kinh-duong-nhap-mieu: tuổi Quý Kình ở Sửu; Triệt Tý–Sửu đè Mệnh chỉ 'giảm lực rõ'; phá vì Tham Lang Hóa Kỵ "
     "ở Mùi xung Mệnh (Hóa Kỵ xung phá nặng nhất)"),
    ("1986-07-09", "02:00", "nam", "Mã đầu đới kiếm (thế hung)", NGO, None,
     "tsk ma-dau-doi-kiem: tuổi Bính Kình ở Ngọ; không có bộ Đồng Âm + Hóa Lộc thì luận hung (Chìa khóa Tử vi)"),
    ("1988-02-22", "02:00", "nam", "Nhật Nguyệt giáp Tài", SUU, None,
     "tsk nhat-nguyet-giap-tai: Vũ Tham Mệnh Sửu, Thái Âm Tý – Thái Dương Dần tự kẹp"),
    ("1988-04-18", "18:00", "nam", "Nhật Nguyệt giáp Tài", MUI, "cách yếu",
     "tsk nhat-nguyet-giap-tai: Vũ Tham ở Mùi hai vầng kẹp đều mờ – không thành chuẩn"),
    ("1979-03-08", "02:00", "nu", "Tử Phủ đồng cung", DAN, "thành cách",
     "hocvienlyso / Tân Biên: Tử Phủ đồng cung tại Dần, có cát tinh hội"),
    ("1996-03-04", "06:00", "nam", "Nguyệt lãng thiên môn", HOI, None,
     "tsk nguyet-lang-thien-mon: Mệnh Hợi Thái Âm, đi kèm Tử Vi ở Ngọ, Dương Lương ở Mão"),
    ("1982-02-24", "22:00", "nu", "Khôi Việt giáp mệnh", THIN, None,
     "tsk thien-at-cung-menh: tuổi Nhâm Quý Khôi Mão – Việt Tỵ kẹp Mệnh Thìn"),
    ("1974-02-20", "16:00", "nam", "Cực hướng Ly minh", NGO, "thành cách",
     "tsk cuc-huong-ly-minh: Mệnh Ngọ Tử Vi, tuổi Giáp không Hình Kỵ"),
    ("1981-02-22", "04:00", "nam", "Thạch trung ẩn ngọc", TY, None,
     "tsk thach-trung-an-ngoc: Mệnh Tý Cự Môn Hóa Lộc tuổi Tân"),
]


def tu_kiem():
    """Tự kiểm: (a) bảng/ví dụ nguồn, (b) 5.000 lá số ngẫu nhiên, (c) bất biến. Trả list lỗi."""
    loi = []
    # ---- (a1) Phụ củng văn tinh: đúng 3 tổ hợp tháng–giờ (tuvisonkhiem phu-cung-van-tinh)
    s = {(m, g) for m in range(1, 13) for g in range(12) if _co(_ls_tham_so(m, g), "Phụ củng văn tinh")}
    if s != {(3, DAN), (3, THIN), (5, THIN)}:
        loi.append("Phụ củng văn tinh: tổ hợp tháng–giờ %s khác bảng nguồn {3-Dần, 3-Thìn, 5-Thìn}" % sorted(s))
    # ---- (a2) Xương Khúc giáp: 4 tổ hợp (tuvisonkhiem giap-xuong-giap-khuc)
    s = {(m, g) for m in range(1, 13) for g in range(12) if _co(_ls_tham_so(m, g), "Xương Khúc giáp")}
    if s != {(8, THAN), (10, TUAT), (8, DAN), (10, THIN)}:
        loi.append("Xương Khúc giáp: %s khác bảng nguồn" % sorted(s))
    # ---- (a3) Tả Hữu đồng cung: chỉ tháng 4, 10 (Mệnh Mùi, Sửu); giáp Tả Hữu: chỉ Sửu Mùi, riêng tháng 5 giờ Hợi
    #      hai cung kẹp không có Không Kiếp (tuvisonkhiem giap-ta-giap-huu)
    s = {(m, g) for m in range(1, 13) for g in range(12) if _co(_ls_tham_so(m, g), "Tả Hữu đồng cung")}
    if s != {(4, TUAT), (10, TUAT)}:
        loi.append("Tả Hữu đồng cung tại Mệnh: %s, nguồn: tháng 4 và 10" % sorted(s))
    sach = set()
    for m in range(1, 13):
        for g in range(12):
            ls = _ls_tham_so(m, g)
            r = _co(ls, "Tả Hữu giáp")
            if r:
                if r[0]["vi_tri"] not in (SUU, MUI):
                    loi.append("Tả Hữu giáp ngoài Sửu Mùi")
                if "Không" not in r[0]["ly_do"] and "Kiếp" not in r[0]["ly_do"]:
                    sach.add((m, g))
    if sach != {(5, HOI)}:
        loi.append("giáp Tả Hữu không vướng Không Kiếp: %s, nguồn: chỉ tháng 5 giờ Hợi" % sorted(sach))
    # ---- (a4) Thiên Ất củng mệnh theo can (tuvisonkhiem thien-at-cung-menh); Canh bỏ vì bảng Khôi Việt VN
    #      'Canh Tân phùng Mã Hổ' khác bản nguồn
    mong = {0: {SUU, MUI}, 4: {SUU, MUI}, 1: {TY, THAN}, 5: {TY, THAN}, 7: {DAN, NGO},
            2: set(), 3: set(), 8: set(), 9: set()}
    for can, ky_vong in mong.items():
        s = set()
        for m in range(1, 13):
            for g in range(12):
                r = _co(_ls_tham_so(m, g, can=can, chi=can % 2), "Thiên Ất")
                s |= {x["vi_tri"] for x in r}
        if s != ky_vong:
            loi.append("Thiên Ất củng mệnh tuổi %s: Mệnh %s, nguồn %s" % (CAN[can], sorted(s), sorted(ky_vong)))
        s2 = set()
        for m in range(1, 13):
            for g in range(12):
                s2 |= {x["vi_tri"] for x in _co(_ls_tham_so(m, g, can=can, chi=can % 2), "Khôi Việt giáp")}
        kv = {8: {THIN}, 9: {THIN}, 2: {TUAT}, 3: {TUAT}}.get(can, set())
        if s2 != kv:
            loi.append("Khôi Việt giáp tuổi %s: %s, nguồn %s" % (CAN[can], sorted(s2), sorted(kv)))
    # ---- (a5) Kình Dương nhập miếu theo can; Mã đầu đới kiếm chỉ tuổi Bính, Mậu (tuvisonkhiem)
    for can in range(10):
        s, ma = set(), False
        for m in range(1, 13):
            for g in range(12):
                ls = _ls_tham_so(m, g, can=can, chi=can % 2)
                s |= {x["vi_tri"] for x in _co(ls, "Kình Dương nhập miếu")}
                ma = ma or bool(_co(ls, "Mã đầu đới kiếm"))
        kv = {1: {THIN}, 7: {TUAT}, 9: {SUU}, 3: {MUI}, 5: {MUI}}.get(can, set())
        if s != kv:
            loi.append("Kình Dương nhập miếu tuổi %s: %s, nguồn %s" % (CAN[can], sorted(s), sorted(kv)))
        if ma != (can in (2, 4)):
            loi.append("Mã đầu đới kiếm xuất hiện sai tuổi %s" % CAN[can])
    # ---- (a6) lá số mẫu có ngày giờ sinh, lập qua toàn chuỗi đổi lịch
    loi += _kiem_la_so_mau()
    # ---- (b) 5.000 lá số ngẫu nhiên: không lỗi, tần suất hợp lý; (c) bất biến
    BAT_BIEN = {"Tử Phủ đồng cung": {DAN, THAN}, "Tử Sát": {TI, HOI}, "Đào hoa phạm chủ": {MAO, DAU},
                "Cực cư Mão Dậu": {MAO, DAU}, "Tử Phá": {SUU, MUI}, "Tử Tướng": {THIN, TUAT},
                "Cực hướng Ly minh": {NGO}, "Nhật chiếu lôi môn": {MAO}, "Nguyệt lãng": {HOI},
                "Nguyệt sinh": {TY}, "Minh châu": {MUI}, "Thạch trung": {TY, NGO}, "Nhật lệ": {NGO},
                "Thất Sát triều đẩu": {TY, NGO, DAN, THAN}, "Hùng tú": {DAN, THAN}, "Anh tinh": {TY, NGO},
                "Vũ Khúc thủ viên": {THIN, TUAT}, "Mã đầu": {NGO}, "Kình Dương nhập miếu": {THIN, TUAT, SUU, MUI},
                "Tả Hữu": {SUU, MUI}, "Xương Khúc giáp": {SUU, MUI}, "Văn Quế": {SUU, MUI},
                "Không Kiếp giáp": {TI, HOI}, "Liêm Tham": {TI, HOI}, "Lương Mã": {TI, HOI},
                "Cơ Lương": {THIN, TUAT}, "Cự Nhật": {DAN, THAN}, "Nhật Nguyệt đồng lâm": {SUU, MUI},
                "Nhật Nguyệt phản bối": {THIN, TUAT}, "Nhật Nguyệt tịnh minh": {TI, DAU, SUU},
                "Tham Vũ": {SUU, MUI, THIN, TUAT}, "Linh Xương Đà Vũ": {THIN, TUAT},
                "Cơ Nguyệt Đồng Lương": {DAN, THAN}, "Khôi Việt giáp": {THIN, TUAT},
                "Tử Phủ triều viên": {DAN, THAN, TY, NGO, SUU, MUI}}
    n = 5000
    dem = {}
    cjk = re.compile("[" + chr(0x3400) + "-" + chr(0x9fff) + "]")
    for ls in _ngau_nhien(n):
        try:
            kq = nhan_dien(ls)
        except Exception as e:      # noqa: BLE001
            loi.append("ngoại lệ trên lá số ngẫu nhiên: %r" % e)
            break
        da = set()
        for r in kq:
            if r["muc"] not in MUC or r["nhom"] not in NHOM or not r["nguon"] or not r["ly_do"]:
                loi.append("kết quả thiếu/ sai trường: %s" % r["ten"])
            if cjk.search(r["ly_do"] + r["nguon"] + r["ten"]):
                loi.append("có chữ Hán trong kết quả: %s" % r["ten"])
            for k, v in BAT_BIEN.items():
                if r["ten"].startswith(k) and r["vi_tri"] not in v and not r["cung"].startswith("Tài Bạch"):
                    loi.append("bất biến: %s ở %s" % (r["ten"], CHI[r["vi_tri"]]))
            # Phụ củng văn tinh tại Mệnh chỉ có ở Tý, Dần (bảng 3 tổ hợp tháng–giờ của nguồn)
            if r["ten"] == "Phụ củng văn tinh" and r["cung"].startswith("Mệnh") and r["vi_tri"] not in (TY, DAN):
                loi.append("bất biến: Phụ củng văn tinh tại Mệnh %s" % CHI[r["vi_tri"]])
            key = (r["ten"], r["cung"])
            if key in da:
                loi.append("trùng cách %s tại %s" % key)
            da.add(key)
            if r["cung"].startswith("Mệnh"):
                dem[r["ten"]] = dem.get(r["ten"], 0) + 1
        # bất biến cấu trúc
        m = ls["menh"]
        if bool([r for r in kq if r["ten"].startswith("Kình Đà giáp") and r["cung"].startswith("Mệnh")]) != \
                (ls["vt"]["Lộc Tồn"] == m):
            loi.append("bất biến: Kình Đà giáp mệnh phải tương đương Lộc Tồn ở Mệnh")
        if bool([r for r in kq if r["ten"] == "Phủ Tướng triều viên"]) != (ls["vt"]["Thiên Phủ"] == (m + 4) % 12):
            loi.append("bất biến: Phủ Tướng triều viên phải tương đương Thiên Phủ ở Quan Lộc")
        if len(loi) > 30:
            break
    for ten, k in dem.items():
        if k > 0.25 * n:
            loi.append("tần suất đáng ngờ: %s %.1f%% > 25%%" % (ten, 100.0 * k / n))
    ky_vong = {"Tử Phủ đồng cung": (0.5 / 72, 2.0 / 72), "Cực hướng Ly minh": (0.4 / 144, 2.0 / 144),
               "Phủ Tướng triều viên": (0.06, 0.11), "Kình Đà giáp mệnh": (0.04, 0.11)}
    for ten, (lo, hi) in ky_vong.items():
        x = sum(v for k, v in dem.items() if k.startswith(ten)) / n
        if not lo <= x <= hi:
            loi.append("tần suất %s = %.2f%% ngoài khoảng lý thuyết %.2f–%.2f%%" % (ten, 100 * x, 100 * lo, 100 * hi))
    thieu = [c["ten"] for c in CACH if c["ma"] in ("tu_phu", "loc_ma", "tam_ky", "spt", "vcd", "quan_than")
             and not any(k.startswith(c["ten"].split(" (")[0].split(" /")[0]) for k in dem)]
    if thieu:
        loi.append("không gặp lần nào trên %d lá số: %s" % (n, ", ".join(thieu)))
    if not 40 <= len(CACH) <= 55:
        loi.append("số mục cách %d ngoài 40–55" % len(CACH))
    return loi


def _kiem_la_so_mau():
    """Lập các lá số mẫu qua nc.thoi_diem (đủ chuỗi đổi giờ, đổi lịch) và so cách tại Mệnh."""
    import argparse
    import nc
    loi = []
    for ngay, gio, gioi, ten, cung, muc, _ in LA_SO_MAU:
        a = argparse.Namespace(ngay=ngay, gio=gio, gioi=gioi, noi="Hà Nội", kinhdo=None, mien=None, utc=None,
                               am=False, nhuan=False, lich_tz=None, gio_dong_ho=False, ty=1)
        tt = nc.thoi_diem(a)
        ls = lap_tu_tt(tt)
        if ls["menh"] != cung:
            loi.append("lá số mẫu %s %s: Mệnh %s, chờ %s" % (ngay, gio, CHI[ls["menh"]], CHI[cung]))
            continue
        r = _co(ls, ten)
        if not r:
            loi.append("lá số mẫu %s %s: không thấy '%s' tại Mệnh" % (ngay, gio, ten))
        elif muc and r[0]["muc"] != muc:
            loi.append("lá số mẫu %s %s: '%s' mức %s, chờ %s" % (ngay, gio, ten, r[0]["muc"], muc))
        if ten == "Nguyệt lãng thiên môn" and (ls["vt"]["Tử Vi"] != NGO or ls["vt"]["Thái Dương"] != MAO
                                              or ls["vt"]["Thiên Lương"] != MAO):
            loi.append("Nguyệt lãng thiên môn: bàn sao đi kèm khác nguồn (Tử Vi Ngọ, Dương Lương Mão)")
    if len(LA_SO_MAU) < 8:
        loi.append("cần ít nhất 8 lá số mẫu (hiện %d)" % len(LA_SO_MAU))
    return loi
