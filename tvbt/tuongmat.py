# -*- coding: utf-8 -*-
"""tuongmat.py - Xem tướng mặt (diện tướng): bảng bộ vị lưu niên 1–100 tuổi, tam đình, ngũ quan, thập nhị cung,
ngũ nhạc, tứ độc, ngũ tinh lục diệu, ngũ hành hình mặt, phiếu quan sát.

Lệnh: python3 tvbt/nc.py tuong --nam-sinh N [--nam M] --gioi nam|nu [--so-nam 3]
      python3 tvbt/nc.py tuong --tuoi T --gioi nam|nu
      python3 tvbt/nc.py tuong --tim "cánh mũi"            (tìm bộ vị theo vị trí, tên Việt hoặc chữ Hán)
      python3 tvbt/nc.py tuong --bang luunien|cung|nguquan|tamdinh|nhac|tinh|hinh|bangiam|phieu|tatca

Gốc:
- "Lưu niên vận khí bộ vị ca" (流年運氣部位歌) trong Thần tướng toàn biên (神相全編, đề Trần Đoàn, Viên Trung Triệt hiệu
  đính, đời Minh) và Ma Y thần tướng (麻衣神相) quyển 1. Đối chiếu hai bản chép độc lập của bài ca (destiny.to 2003,
  secretchina 2016) và bảng tọa độ "百岁流年" của Liyucheng1997/362_mayi-xiangshu: khớp từng tuổi 1–99.
- Tam đình, ngũ quan, ngũ nhạc, tứ độc, ngũ tinh lục diệu, thập nhị cung, ngũ hành hình: Ma Y thần tướng quyển 1–2
  (theo bản "Đồ giải Ma Y thần tướng", trang 114–158, qua memilin/mayi-face-aesthetics).
- Bảy thiên Băng giám (冰鑑): Thần cốt, Cương nhu, Dung mạo, Tình thái, Tu mi, Thanh âm, Khí sắc (bản khắc 1829,
  thường gán cho Tăng Quốc Phiên nhưng có trước ông).
Tuổi trong bài ca là tuổi mụ (hư tuế). Nam xem bên trái, nữ xem bên phải (nam tả nữ hữu): "trái" là bên trái CỦA
NGƯỜI ĐƯỢC XEM, tức bên phải tấm ảnh chụp thẳng không lật gương.
"""
import datetime as dt
import os
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# (tuổi..., Hán, tên Việt, bên với NAM: 'T' trái / 'P' phải / 'G' giữa, vị trí)
# Bên ghi theo nam; nữ đảo T <-> P (nam tả nữ hữu).
LUU_NIEN = [
    ((1, 2), "天輪", "Thiên luân", "T", "vành tai trên"),
    ((3, 4), "天城", "Thiên thành", "T", "vành tai ngoài, đoạn giữa"),
    ((5, 6, 7), "天郭垂珠", "Thiên quách thùy châu", "T", "dái tai"),
    ((8, 9), "天輪", "Thiên luân", "P", "vành tai trên"),
    ((10, 11), "人輪", "Nhân luân", "P", "vành tai giữa (sách: luân phi quách phản thì xấu)"),
    ((12, 13, 14), "地輪", "Địa luân", "P", "dái tai (sách: dái tai hướng về miệng là tốt)"),
    ((15,), "火星", "Hỏa tinh", "G", "giữa trán sát chân tóc"),
    ((16,), "天中", "Thiên trung", "G", "giữa trán ngay dưới chân tóc"),
    ((17,), "日角", "Nhật giác", "T", "trán phía trên đầu mày, sát chân tóc"),
    ((18,), "月角", "Nguyệt giác", "P", "trán phía trên đầu mày, sát chân tóc"),
    ((19,), "天庭", "Thiên đình", "G", "giữa trán, phần trên"),
    ((20,), "輔角", "Phụ giác", "T", "góc trán phía trên đuôi mày"),
    ((21,), "輔角", "Phụ giác", "P", "góc trán phía trên đuôi mày"),
    ((22,), "司空", "Tư không", "G", "giữa trán, dưới thiên đình"),
    ((23,), "邊城", "Biên thành", "T", "mép trán gần thái dương"),
    ((24,), "邊城", "Biên thành", "P", "mép trán gần thái dương"),
    ((25,), "中正", "Trung chính", "G", "giữa trán, ngay trên ấn đường"),
    ((26,), "丘陵", "Khâu lăng", "T", "trán bên, ngang trung chính"),
    ((27,), "塚墓", "Trủng mộ", "P", "trán bên, ngang trung chính"),
    ((28,), "印堂", "Ấn đường", "G", "giữa hai đầu mày"),
    ((29,), "山林", "Sơn lâm", "T", "mép trán ngoài, sát tóc mai"),
    ((30,), "山林", "Sơn lâm", "P", "mép trán ngoài, sát tóc mai"),
    ((31,), "凌雲", "Lăng vân", "T", "ngay trên đầu mày"),
    ((32,), "紫氣", "Tử khí", "P", "ngay trên đầu mày"),
    ((33,), "繁霞", "Phồn hà", "T", "lông mày"),
    ((34,), "彩霞", "Thải hà", "P", "lông mày"),
    ((35,), "太陽", "Thái dương", "T", "đầu mắt (khóe trong)"),
    ((36,), "太陰", "Thái âm", "P", "đầu mắt (khóe trong)"),
    ((37,), "中陽", "Trung dương", "T", "giữa mắt"),
    ((38,), "中陰", "Trung âm", "P", "giữa mắt"),
    ((39,), "少陽", "Thiếu dương", "T", "đuôi mắt"),
    ((40,), "少陰", "Thiếu âm", "P", "đuôi mắt"),
    ((41,), "山根", "Sơn căn", "G", "gốc mũi, giữa hai mắt"),
    ((42,), "精舍", "Tinh xá", "T", "cạnh sơn căn, sát khóe mắt trong"),
    ((43,), "光殿", "Quang điện", "P", "cạnh sơn căn, sát khóe mắt trong"),
    ((44,), "年上", "Niên thượng", "G", "sống mũi đoạn trên"),
    ((45,), "壽上", "Thọ thượng", "G", "sống mũi đoạn dưới"),
    ((46,), "顴", "Quyền (gò má)", "T", "gò má"),
    ((47,), "顴", "Quyền (gò má)", "P", "gò má"),
    ((48,), "準頭", "Chuẩn đầu", "G", "đầu mũi"),
    ((49,), "蘭台", "Lan đài", "T", "cánh mũi"),
    ((50,), "廷尉", "Đình úy", "P", "cánh mũi"),
    ((51,), "人中", "Nhân trung", "G", "rãnh giữa mũi và môi trên"),
    ((52,), "仙庫", "Tiên khố", "T", "hai bên nhân trung, sát môi trên"),
    ((53,), "仙庫", "Tiên khố", "P", "hai bên nhân trung, sát môi trên"),
    ((54,), "食倉", "Thực thương", "T", "trên mép môi trên, phía ngoài"),
    ((55,), "祿倉", "Lộc thương", "P", "trên mép môi trên, phía ngoài"),
    ((56,), "法令", "Pháp lệnh", "T", "nếp từ cánh mũi xuống khóe miệng"),
    ((57,), "法令", "Pháp lệnh", "P", "nếp từ cánh mũi xuống khóe miệng"),
    ((58,), "虎耳", "Hổ nhĩ", "T", "má ngoài, ngang miệng, phía trước tai"),
    ((59,), "虎耳", "Hổ nhĩ", "P", "má ngoài, ngang miệng, phía trước tai"),
    ((60,), "水星", "Thủy tinh (miệng)", "G", "miệng, đôi môi"),
    ((61,), "承漿", "Thừa tương", "G", "chỗ lõm ngay dưới môi dưới"),
    ((62,), "地庫", "Địa khố", "T", "hai bên thừa tương, trên cằm"),
    ((63,), "地庫", "Địa khố", "P", "hai bên thừa tương, trên cằm"),
    ((64,), "陂池", "Pha trì", "T", "dưới khóe miệng, phía ngoài"),
    ((65,), "鵝鴨", "Nga áp", "P", "dưới khóe miệng, phía ngoài"),
    ((66,), "金縷", "Kim lũ", "T", "dưới khóe miệng, xuống phía cằm"),
    ((67,), "金縷", "Kim lũ", "P", "dưới khóe miệng, xuống phía cằm"),
    ((68,), "歸來", "Quy lai", "T", "chỗ gấp giữa má dưới và xương hàm"),
    ((69,), "歸來", "Quy lai", "P", "chỗ gấp giữa má dưới và xương hàm"),
    ((70,), "頌堂", "Tụng đường", "G", "giữa môi dưới và đỉnh cằm"),
    ((71,), "地閣", "Địa các", "G", "đỉnh cằm"),
    ((72,), "奴僕", "Nô bộc", "T", "hai bên cằm"),
    ((73,), "奴僕", "Nô bộc", "P", "hai bên cằm"),
    ((74,), "腮骨", "Tai cốt (xương quai hàm)", "T", "góc xương hàm"),
    ((75,), "腮骨", "Tai cốt (xương quai hàm)", "P", "góc xương hàm"),
]
# 76–99: vòng 12 chi quanh viền mặt, mỗi chi 2 năm; Tý ở dưới cằm, Ngọ ở đỉnh trán,
# Mão ở viền mặt bên trái (nam; nữ bên phải), Dậu bên đối diện (hình 百歲流年圖 thông dụng).
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
CHI_HAN = "子丑寅卯辰巳午未申酉戌亥"
CHI_VI_TRI = {
    0: ("G", "viền dưới cằm, chính giữa"), 1: ("T", "viền cằm lệch sang"), 2: ("T", "viền quai hàm"),
    3: ("T", "viền má ngang tai"), 4: ("T", "viền thái dương"), 5: ("T", "góc trán sát tóc"),
    6: ("G", "đỉnh trán sát chân tóc"), 7: ("P", "góc trán sát tóc"), 8: ("P", "viền thái dương"),
    9: ("P", "viền má ngang tai"), 10: ("P", "viền quai hàm"), 11: ("P", "viền cằm lệch sang"),
}
for _i in range(12):
    _b, _vt = CHI_VI_TRI[_i]
    LUU_NIEN.append(((76 + 2 * _i, 77 + 2 * _i), "%s位" % CHI_HAN[_i], "vị %s" % CHI[_i], _b, _vt))

GIAI_DOAN = [
    (1, 14, "Tai (Thải thính quan)", "tuổi nhỏ: sức khỏe, nền nếp, sự chăm sóc của cha mẹ"),
    (15, 30, "Trán – thượng đình", "học hành, khởi nghiệp, sự nâng đỡ của bề trên"),
    (31, 34, "Lông mày (Bảo thọ quan)", "bạn bè, anh em, danh tiếng"),
    (35, 40, "Mắt (Giám sát quan)", "nhận định, chọn hướng sự nghiệp"),
    (41, 50, "Mũi, gò má – trung đình (Thẩm biện quan)", "sức lực tự gây dựng, tiền bạc, vị thế giữa đời"),
    (51, 60, "Nhân trung, pháp lệnh, miệng (Xuất nạp quan)", "uy tín, nói năng, ăn uống, nếp sống"),
    (61, 75, "Cằm, hàm – hạ đình", "hậu vận: nhà cửa, con cháu, người giúp việc"),
    (76, 99, "Viền mặt, vòng 12 chi", "tuổi thọ cao: xem chung thần sắc, ít dùng"),
]

TAM_DINH = [
    ("Thượng đình", "chân tóc → ấn đường (trán)", "15–30", "Thiên – sách: trán nên rộng, tròn đầy"),
    ("Trung đình", "sơn căn → chuẩn đầu (mũi, gò má, mắt mày ở hai bên)", "31–50", "Nhân – sách: mũi nên thẳng, cân"),
    ("Hạ đình", "nhân trung → địa các (miệng, cằm)", "51–75", "Địa – sách: cằm nên vuông, rộng"),
]

NGU_QUAN = [
    ("Tai", "Thải thính quan (採聽官)", "1–14",
     "màu tươi, cao hơn mày, vành và quách rõ, dày, sát đầu"),
    ("Lông mày", "Bảo thọ quan (保壽官)", "31–34",
     "rộng, thanh, dài quá mắt, sợi thuận, như vầng trăng non"),
    ("Mắt", "Giám sát quan (監察官)", "35–40",
     "ẩn tàng không lộ, đen trắng phân minh, con ngươi ngay, có thần"),
    ("Mũi", "Thẩm biện quan (審辨官)", "41–50",
     "sống mũi thẳng, đầu mũi tròn, cánh mũi đầy, như túi mật treo, lỗ không lộ"),
    ("Miệng", "Xuất nạp quan (出納官)", "60 (và 51–60)",
     "vuông, rộng, môi hồng, mở ra rộng khép lại nhỏ"),
]

THAP_NHI_CUNG = [
    ("Mệnh cung", "命宮", "ấn đường, giữa hai đầu mày", "sáng, phẳng, rộng; không lõm, không vằn ngang dọc"),
    ("Tài bạch", "財帛宮", "mũi (đầu mũi, hai cánh mũi)", "đầu mũi tròn đầy, cánh mũi có thịt, sắc sáng"),
    ("Huynh đệ", "兄弟宮", "hai lông mày", "mày thanh, dài quá mắt, sợi thuận"),
    ("Điền trạch", "田宅宮", "khoảng giữa mày và mắt (mí trên)", "rộng, đầy; mắt trong"),
    ("Nam nữ (Tử tức)", "男女宮", "dưới mắt (lệ đường, ngọa tằm)", "phẳng, đầy, sắc sáng"),
    ("Nô bộc", "奴僕宮", "hai bên cằm, dưới khóe miệng", "đầy đặn, cân"),
    ("Thê thiếp (Phu thê)", "妻妾宮", "đuôi mắt đến tóc mai (gian môn)", "phẳng, sáng, không lõm"),
    ("Tật ách", "疾厄宮", "sơn căn (gốc mũi)", "cao, phẳng, liền, sắc sáng"),
    ("Thiên di", "遷移宮", "hai bên trán, trên đuôi mày (thiên thương)", "đầy, không lõm lệch"),
    ("Quan lộc", "官祿宮", "giữa trán (trung chính)", "sáng, đầy, không sẹo"),
    ("Phúc đức", "福德宮", "thiên thương hai bên trán, nối với địa các", "trán và cằm cân nhau, chầu nhau"),
    ("Tướng mạo", "相貌宮", "toàn khuôn mặt", "ngũ nhạc đầy, tam đình cân – 'tướng không xét lẻ'"),
    ("(Phụ) Phụ mẫu", "父母宮", "nhật giác, nguyệt giác (trán trên đầu mày)", "hai góc cao tròn, sáng, cân"),
]

NGU_NHAC = [
    ("Trán", "Nam nhạc Hành sơn"), ("Cằm", "Bắc nhạc Hằng sơn"), ("Mũi", "Trung nhạc Tung sơn (chủ phong)"),
    ("Gò má trái", "Đông nhạc Thái sơn"), ("Gò má phải", "Tây nhạc Hoa sơn"),
]
TU_DOC = [("Tai", "Giang độc"), ("Mắt", "Hà độc"), ("Miệng", "Hoài độc"), ("Mũi", "Tế độc")]
NGU_TINH_LUC_DIEU = [
    ("Tai trái", "Kim tinh", "trắng sạch"), ("Tai phải", "Mộc tinh", "chầu vào"), ("Trán", "Hỏa tinh", "vuông"),
    ("Mũi", "Thổ tinh", "dày"), ("Miệng", "Thủy tinh", "hồng"), ("Mắt trái", "Thái dương", "sáng"),
    ("Mắt phải", "Thái âm", "đen"), ("Mày trái", "La hầu", "dài"), ("Mày phải", "Kế đô", "đều"),
    ("Sơn căn", "Nguyệt bột", "thẳng"), ("Ấn đường", "Tử khí", "tròn"),
]
NGU_HANH_HINH = [
    ("Kim", "vuông vức, sắc trắng", "kim không ngại vuông"),
    ("Mộc", "gầy dài, sắc xanh", "mộc không ngại gầy"),
    ("Thủy", "tròn đầy, sắc sẫm", "thủy không ngại béo"),
    ("Hỏa", "trên nhọn dưới rộng, sắc hồng", "hỏa không ngại nhọn"),
    ("Thổ", "dày dặn, chắc nặng, sắc vàng", "thổ không ngại đục"),
]
THAP_TAM_BO_VI = ["Thiên trung", "Thiên đình", "Tư không", "Trung chính", "Ấn đường", "Sơn căn", "Niên thượng",
                  "Thọ thượng", "Chuẩn đầu", "Nhân trung", "Thủy tinh", "Thừa tương", "Địa các"]
BANG_GIAM = [
    ("Thần cốt", "thần ở hai mắt, cốt ở trán, mày, gò má; xem thần trước"),
    ("Cương nhu", "tính mạnh – mềm qua cử chỉ"),
    ("Dung mạo", "dáng người, tương xứng các phần"),
    ("Tình thái", "nét mặt, điệu bộ lúc nói, lúc nghĩ – cần gặp hoặc xem video"),
    ("Tu mi", "râu, lông mày"),
    ("Thanh âm", "giọng nói từ đan điền, tròn, vang – cần nghe tiếng"),
    ("Khí sắc", "sắc mặt theo thời điểm; ảnh chụp bị đèn, máy, trang điểm làm sai"),
]

PHIEU = """PHIẾU QUAN SÁT (chỉ ghi điều thấy rõ; ô nào không rõ ghi "không thấy rõ"):
| Mục | Ghi nhận | Độ rõ |
|---|---|---|
| Ảnh | chính diện / nghiêng; lật gương?; ánh sáng; trang điểm, bộ lọc; khoảng cách máy (dưới 50 cm làm mũi to) | |
| Hình mặt (ngũ hành) | vuông / dài / tròn / trên nhọn dưới rộng / dày; hay pha | |
| Tam đình | trán : giữa : dưới, ước tỉ lệ (vd 1 : 1 : 0,9) | |
| Trán | rộng hẹp, cao thấp, đầy hay phẳng; chân tóc; nhật nguyệt giác | |
| Ấn đường | rộng mấy ngón, phẳng, có vằn dọc/ngang không | |
| Lông mày | dày mỏng, dài so với mắt, hình, sợi thuận hay rối, khoảng cách hai mày | |
| Mắt | to nhỏ, dài, khóe đuôi lên/xuống, đen trắng rõ, ánh mắt | |
| Dưới mắt | đầy hay trũng, ngọa tằm | |
| Sơn căn, sống mũi | cao thấp, liền hay gãy, có vằn ngang | |
| Đầu mũi, cánh mũi | tròn, nhọn, có thịt; lỗ mũi lộ khi nhìn thẳng? | |
| Gò má | cao thấp, có thịt bọc, cân với mũi | |
| Nhân trung | dài ngắn, sâu nông, trên hẹp dưới rộng? | |
| Pháp lệnh | rõ / mờ / chưa có | |
| Miệng, môi | rộng hẹp, dày mỏng, khóe lên/xuống | |
| Cằm, hàm | vuông, tròn, nhọn; đầy hay lẹm; hai bên hàm | |
| Tai (nếu thấy) | cao thấp so với mày, vành, dái tai, sát đầu | |
| Nốt ruồi, sẹo, vằn | vị trí theo bộ vị (dùng --tim), nổi hay phẳng, màu | |
| Thần (ánh mắt, nét mặt) | tỉnh, mệt, căng; chỉ ghi khi thấy rõ | |"""

GHI_CHU = """CÁCH DÙNG (nói rõ khi luận):
1. Tuổi là tuổi mụ: năm âm lịch đang xem − năm âm lịch sinh + 1. Nam xem bên trái, nữ bên phải; "trái" là trái của
   người được xem (bên phải ảnh chụp thẳng). Ảnh selfie camera trước thường bị lật gương – hỏi lại khi không chắc.
2. Bộ vị năm nay chỉ là chỗ "nên để ý" trong năm; sách xem chủ yếu bằng khí sắc chỗ đó (sáng, tối), mà ảnh chụp
   không đọc được khí sắc tin cậy. Không phán lành dữ từ một bộ vị; xem chung với cả mặt ("tướng không xét lẻ").
3. Bài ca còn "Vận khí khẩu quyết" (tính tuổi khởi theo ngũ hành) và "Thức hạn ca" (8/18/28…) – các bản chép lệch
   nhau ở vài con số, skill không dùng.
4. Qua 99 tuổi: sách ghi "thuận số triều thượng… chu nhi phục thủy" (đi lên trán rồi lặp lại); script coi 100 là
   đỉnh trán, từ 101 lặp lại từ tai như tuổi 1 – các bản giải không thống nhất."""


def bo_vi(tuoi, gioi="nam"):
    """Trả về dict bộ vị của tuổi mụ `tuoi`."""
    if tuoi < 1:
        raise ValueError("tuổi mụ phải từ 1")
    goc = tuoi
    if tuoi == 100:
        return {"tuoi": 100, "han": "火星/天中", "ten": "Hỏa tinh – Thiên trung (về đỉnh trán)", "ben": "G",
                "ben_vn": "giữa", "vi_tri": "đỉnh trán (sách: thuận số triều thượng)", "giai_doan": GIAI_DOAN[-1],
                "chu": "100 tuổi, các bản giải không thống nhất"}
    if tuoi > 100:
        tuoi = (tuoi - 101) % 100 + 1
    for tuois, han, ten, ben, vt in LUU_NIEN:
        if tuoi in tuois:
            if gioi == "nu" and ben in "TP":
                ben = "P" if ben == "T" else "T"
            gd = next(g for g in GIAI_DOAN if g[0] <= tuoi <= g[1])
            r = {"tuoi": goc, "han": han, "ten": ten, "ben": ben,
                 "ben_vn": {"T": "bên trái", "P": "bên phải", "G": "giữa"}[ben], "vi_tri": vt, "giai_doan": gd,
                 "chu": "" if goc == tuoi else "quá 100 tuổi, vòng lại như tuổi %d" % tuoi}
            return r
    raise AssertionError(tuoi)


def bo_dau(s):
    s = unicodedata.normalize("NFD", s.lower().replace("đ", "d"))
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def tim(tu):
    """Tìm bộ vị theo tên Việt, chữ Hán hoặc mô tả vị trí (không phân biệt dấu)."""
    k = bo_dau(tu)
    kq = []
    for tuois, han, ten, ben, vt in LUU_NIEN:
        if k in bo_dau(ten) or k in bo_dau(vt) or tu in han:
            kq.append((tuois, han, ten, ben, vt))
    for ten, han, vt, _ in THAP_NHI_CUNG:
        if k in bo_dau(ten) or k in bo_dau(vt) or tu in han:
            kq.append(((), han, ten + " (cung)", "", vt))
    return kq


def tuoi_chuoi(t):
    return "%d" % t[0] if len(t) == 1 else "%d–%d" % (t[0], t[-1])


def in_bo_vi(r, gioi):
    print("- Tuổi mụ %d: %s (%s) – %s, %s%s." % (
        r["tuoi"], r["ten"], r["han"], r["vi_tri"], r["ben_vn"] if r["ben"] != "G" else "đường giữa",
        (" của người được xem (%s)" % ("nam" if gioi == "nam" else "nữ")) if r["ben"] != "G" else ""))
    print("  Giai đoạn: %s – %s." % (r["giai_doan"][2], r["giai_doan"][3]) + (" (%s)" % r["chu"] if r["chu"] else ""))


def in_bang(ten):
    if ten in ("luunien", "tatca"):
        print("BỘ VỊ LƯU NIÊN 1–99 TUỔI (bên ghi theo NAM; nữ đảo trái ↔ phải):")
        print("| Tuổi mụ | Bộ vị | Hán | Bên (nam) | Vị trí |")
        print("|---|---|---|---|---|")
        for tuois, han, t, ben, vt in LUU_NIEN:
            print("| %s | %s | %s | %s | %s |" % (tuoi_chuoi(tuois), t, han, {"T": "trái", "P": "phải", "G": "giữa"}[ben], vt))
        print()
    if ten in ("tamdinh", "tatca"):
        print("TAM ĐÌNH (chia mặt làm ba theo chiều dọc; sách: ba phần cân là tốt):")
        print("| Đình | Từ – đến | Tuổi (lưu niên) | Sách nói |")
        print("|---|---|---|---|")
        for r in TAM_DINH:
            print("| %s | %s | %s | %s |" % r)
        print("Thập tam bộ vị (đường giữa, trên xuống): " + ", ".join(THAP_TAM_BO_VI) + ".")
        print()
    if ten in ("nguquan", "tatca"):
        print("NGŨ QUAN (Ma Y quyển 2 'Ngũ quan tổng luận'; Đại thống phú: một quan thành, mười năm quý):")
        print("| Bộ phận | Tên quan | Tuổi | Sách cho là 'thành' khi |")
        print("|---|---|---|---|")
        for r in NGU_QUAN:
            print("| %s | %s | %s | %s |" % r)
        print()
    if ten in ("cung", "tatca"):
        print("THẬP NHỊ CUNG (Ma Y quyển 1):")
        print("| Cung | Hán | Vị trí | Sách cho là tốt khi |")
        print("|---|---|---|---|")
        for r in THAP_NHI_CUNG:
            print("| %s | %s | %s | %s |" % r)
        print()
    if ten in ("nhac", "tatca"):
        print("NGŨ NHẠC (năm chỗ nhô, nên đầy và chầu nhau): " +
              "; ".join("%s = %s" % r for r in NGU_NHAC) + ".")
        print("TỨ ĐỘC (bốn dòng sông, nên sâu, dài, có bờ): " + "; ".join("%s = %s" % r for r in TU_DOC) + ".")
        print()
    if ten in ("tinh", "tatca"):
        print("NGŨ TINH LỤC DIỆU (mỗi chỗ một chữ chuẩn):")
        print("; ".join("%s = %s (nên %s)" % r for r in NGU_TINH_LUC_DIEU) + ".")
        print()
    if ten in ("hinh", "tatca"):
        print("NGŨ HÀNH HÌNH MẶT (Ma Y quyển 2 'Ngũ hành hình'; hình hợp hành là 'nhập cách'):")
        print("| Hành | Hình, sắc | Sách nói |")
        print("|---|---|---|")
        for r in NGU_HANH_HINH:
            print("| %s | %s | %s |" % r)
        print("Đa số người pha hai hành: lấy nét nổi nhất làm chính.")
        print()
    if ten in ("bangiam", "tatca"):
        print("BẢY THIÊN BĂNG GIÁM (xem 'động': thần, tình thái, giọng – ảnh tĩnh chỉ thấy một phần):")
        for r in BANG_GIAM:
            print("- %s: %s." % r)
        print()
    if ten in ("phieu", "tatca"):
        print(PHIEU)
        print()


def them_lenh(sub):
    p = sub.add_parser("tuong", help="Tướng mặt: bộ vị lưu niên theo tuổi, bảng tam đình / ngũ quan / 12 cung, phiếu quan sát")
    p.add_argument("--nam-sinh", type=int, help="năm sinh ÂM LỊCH (người sinh trước Tết thì lấy năm trước)")
    p.add_argument("--nam", type=int, help="năm âm lịch đang xem; mặc định năm hiện tại")
    p.add_argument("--tuoi", type=int, help="tuổi mụ (thay cho --nam-sinh)")
    p.add_argument("--gioi", choices=["nam", "nu"], help="nam xem bên trái, nữ bên phải")
    p.add_argument("--so-nam", type=int, default=3, help="số năm tới in thêm (mặc định 3)")
    p.add_argument("--tim", help="tìm bộ vị theo vị trí hoặc tên, vd \"cánh mũi\", \"ấn đường\", \"印堂\"")
    p.add_argument("--bang", choices=["luunien", "cung", "nguquan", "tamdinh", "nhac", "tinh", "hinh", "bangiam",
                                      "phieu", "tatca"], help="in bảng tra")
    p.set_defaults(_chay=chay)


def nam_am_hien_tai():
    now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None) + dt.timedelta(hours=7)
    try:
        import lich_vn as L
        return L.solar_to_lunar(now.day, now.month, now.year)[2]
    except Exception:           # noqa: BLE001
        return now.year if (now.month, now.day) >= (2, 10) else now.year - 1


def chay(a):
    lam = False
    if a.bang:
        in_bang(a.bang)
        lam = True
    if a.tim:
        kq = tim(a.tim)
        print("TÌM \"%s\":" % a.tim)
        if not kq:
            print("- Không thấy. Thử từ khác (vd: trán, mày, mắt, mũi, má, miệng, cằm, tai) hoặc --bang luunien.")
        for tuois, han, ten, ben, vt in kq:
            if tuois:
                nu = {"T": "phải", "P": "trái", "G": "giữa"}[ben]
                print("- %s (%s): %s; tuổi mụ %s – nam bên %s, nữ bên %s." % (
                    ten, han, vt, tuoi_chuoi(tuois), {"T": "trái", "P": "phải", "G": "giữa"}[ben], nu))
            else:
                print("- %s (%s): %s." % (ten, han, vt))
        print()
        lam = True
    if a.tuoi or a.nam_sinh:
        if not a.gioi:
            raise SystemExit("LỖI: cần --gioi nam|nu (nam xem bên trái, nữ bên phải).")
        if a.tuoi:
            tuoi0 = a.tuoi
            print("BỘ VỊ LƯU NIÊN (%s, tuổi mụ %d):" % ("nam" if a.gioi == "nam" else "nữ", tuoi0))
        else:
            nam = a.nam or nam_am_hien_tai()
            tuoi0 = nam - a.nam_sinh + 1
            if tuoi0 < 1:
                raise SystemExit("LỖI: năm xem trước năm sinh.")
            print("BỘ VỊ LƯU NIÊN (%s, sinh năm âm %d, năm âm %d → tuổi mụ %d):" % (
                "nam" if a.gioi == "nam" else "nữ", a.nam_sinh, nam, tuoi0))
        in_bo_vi(bo_vi(tuoi0, a.gioi), a.gioi)
        if a.so_nam > 0:
            print("Các năm tới:")
            for i in range(1, a.so_nam + 1):
                r = bo_vi(tuoi0 + i, a.gioi)
                nam_i = "" if a.tuoi else " (năm %d)" % ((a.nam or nam_am_hien_tai()) + i)
                print("  - %d tuổi%s: %s (%s), %s." % (r["tuoi"], nam_i, r["ten"], r["vi_tri"], r["ben_vn"]))
        if tuoi0 < 14:
            print("! Trẻ dưới 14 tuổi: chỉ nói nét tính tốt, năng khiếu, nhẹ nhàng; không nói vận hạn.")
        print()
        print(GHI_CHU)
        lam = True
    if not lam:
        raise SystemExit("Cần --nam-sinh/--tuoi kèm --gioi, hoặc --tim, hoặc --bang. Xem --help.")


# ---------------------------------------------------------------- tự kiểm
def tu_kiem():
    loi = []
    # mỗi tuổi 1–99 có đúng một bộ vị
    dem = {}
    for tuois, *_ in LUU_NIEN:
        for t in tuois:
            dem[t] = dem.get(t, 0) + 1
    if sorted(dem) != list(range(1, 100)) or any(v != 1 for v in dem.values()):
        loi.append("bảng lưu niên không phủ đúng 1–99")
    # đối chiếu bài ca (神相全編 / 麻衣神相): các mốc chính
    mau = {1: "天輪", 5: "天郭垂珠", 10: "人輪", 14: "地輪", 15: "火星", 16: "天中", 17: "日角", 18: "月角",
           19: "天庭", 22: "司空", 25: "中正", 26: "丘陵", 27: "塚墓", 28: "印堂", 31: "凌雲", 32: "紫氣",
           33: "繁霞", 34: "彩霞", 35: "太陽", 36: "太陰", 37: "中陽", 38: "中陰", 39: "少陽", 40: "少陰",
           41: "山根", 42: "精舍", 43: "光殿", 44: "年上", 45: "壽上", 48: "準頭", 49: "蘭台", 50: "廷尉",
           51: "人中", 54: "食倉", 55: "祿倉", 60: "水星", 61: "承漿", 64: "陂池", 65: "鵝鴨", 70: "頌堂",
           71: "地閣", 76: "子位", 78: "丑位", 80: "寅位", 81: "寅位", 82: "卯位", 88: "午位", 90: "未位",
           92: "申位", 94: "酉位", 96: "戌位", 99: "亥位"}
    for t, h in mau.items():
        if bo_vi(t)["han"] != h:
            loi.append("tuổi %d phải là %s" % (t, h))
    # nam tả nữ hữu
    if bo_vi(17, "nam")["ben"] != "T" or bo_vi(17, "nu")["ben"] != "P" or bo_vi(28, "nu")["ben"] != "G":
        loi.append("nam tả nữ hữu")
    if bo_vi(1, "nam")["ben"] != "T" or bo_vi(8, "nu")["ben"] != "T":
        loi.append("thứ tự hai tai")
    # tọa độ bảng 362_mayi-xiangshu: bên trái người được xem có x > 200 (ảnh nhìn thẳng)
    toa_do_trai = {17: 224, 20: 252, 23: 282, 26: 262, 29: 306, 31: 232, 33: 276, 35: 245, 37: 261, 39: 278,
                   42: 222, 46: 290, 49: 224, 52: 214, 54: 242, 56: 254, 58: 292, 62: 228, 64: 268, 66: 256,
                   68: 236, 72: 216, 74: 300}
    for t in toa_do_trai:
        if bo_vi(t, "nam")["ben"] != "T" or bo_vi(t + 1, "nam")["ben"] != "P":
            loi.append("bên trái/phải tuổi %d–%d" % (t, t + 1))
    if bo_vi(100)["ben"] != "G" or bo_vi(101)["han"] != "天輪":
        loi.append("quá 99 tuổi")
    if not tim("cánh mũi") or not tim("an duong") or not tim("印堂"):
        loi.append("tìm bộ vị")
    if len(THAP_NHI_CUNG) != 13 or len(NGU_QUAN) != 5 or len(TAM_DINH) != 3 or len(THAP_TAM_BO_VI) != 13:
        loi.append("bảng khung")
    return loi


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="lenh", required=True)
    them_lenh(sp)
    x = ap.parse_args()
    x._chay(x)
