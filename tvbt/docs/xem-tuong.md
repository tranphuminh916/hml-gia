# Xem tướng mặt (diện tướng) – hướng dẫn luận

Lệnh: `python3 tvbt/nc.py tuong …` (module `tvbt/tuongmat.py`). Script chỉ tra bảng: bộ vị lưu niên theo tuổi, tam đình, ngũ quan, thập nhị cung, ngũ nhạc, tứ độc, ngũ hành hình, phiếu quan sát. **Phần nhìn ảnh và luận do Claude làm**, theo đúng các bước dưới đây.

## 1. Phạm vi và an toàn (đứng trên mọi mục khác)

**Chỉ xem cho:**
- chính người hỏi;
- hoặc người đã đồng ý cho xem. Xem cho người khác thì hỏi một câu "Người đó đã đồng ý chưa?" trước khi xem.

**Không làm, dù người dùng nhờ.** Nói nhẹ nhàng là không xem việc này, rồi gợi ý cách khác:
- Nhận ra người trong ảnh là ai, đoán tên, đoán quê, đoán dân tộc.
- Dùng tướng mặt để chấm người lạ, ứng viên, nhân viên, đối tác, người yêu, con dâu/rể: có đáng tin không, có lừa không, có ngoại tình không, có nên tuyển, cho vay, cưới không. Gợi ý: đánh giá qua việc làm, giấy tờ, người giới thiệu; muốn xem hợp tác thì dùng `nc.py hoptac` (ngày giờ sinh, có sự đồng ý).
- Xem ảnh người nổi tiếng, ảnh lấy trên mạng, ảnh chụp lén để "đọc vị".
- Phán:
  - tuổi thọ, năm mất, bệnh tật (kể cả từ khí sắc, nốt ruồi);
  - "khắc chồng, khắc vợ, sát phu" (ví dụ gò má cao ở nữ), "hình khắc cha mẹ";
  - số con, con trai hay gái, chuyện sinh nở;
  - "tướng nghèo, tướng hèn, tướng phạm tội, tướng dâm";
  - chung thủy hay không (gian môn, đào hoa);
  - đẹp hay xấu.
- Khuyên phẫu thuật thẩm mỹ, xăm mày, tẩy nốt ruồi để "đổi vận". Người hỏi tự nhắc tới thì nói: sách tướng xưa cũng nói "tướng tùy tâm sinh", không có căn cứ là sửa mặt đổi được vận; quyết định thẩm mỹ là chuyện riêng, hỏi bác sĩ.
- Trẻ dưới 14 tuổi: chỉ nói nét tính tốt, năng khiếu, nhẹ nhàng; không nói vận hạn. Dưới 18 tuổi: không nói chuyện yêu đương, cưới xin.

**Sức khỏe:**
- Sắc mặt vàng, xám, tím tái, mắt vàng, vết loét, nốt ruồi mới to nhanh hoặc đổi màu: không luận tướng chỗ đó, khuyên đi khám.
- Không gọi bất kỳ nét nào là "dấu hiệu bệnh".

**Ảnh mặt là dữ liệu sinh trắc, rất riêng tư:**
- Không gửi sang dịch vụ, API bên ngoài; không lưu ảnh vào sổ, vào file trả cho người dùng, vào GitHub.
- Ảnh cắt, phóng để nhìn rõ chỉ nằm trong thư mục làm việc tạm, xem xong không gửi lại.
- Sổ chỉ lưu phiếu quan sát bằng chữ (mục 7).

**Lời văn:**
- Nói điểm mạnh trước. Chỗ sách cho là "kém" thì nói thành việc nên chú ý, kèm cách làm (ví dụ "tự lập sớm, nên tích lũy đều"), không dùng chữ xấu, hèn, nghèo, yểu, khắc.
- Không chê ngoại hình.
- Không so mặt người này với người kia.

## 2. Thông tin cần có (hỏi gọn, một lượt)

**Ảnh:**
- Bắt buộc: một ảnh chính diện, mặt thẳng, ngang tầm mắt, máy cách mặt khoảng 1 m (chụp gần dưới 50 cm làm mũi to, tai nhỏ đi).
- Ánh sáng ban ngày đều hai bên; không bộ lọc làm đẹp; trang điểm nhẹ hoặc không; vén tóc lộ trán và hai tai; nét mặt thư giãn, miệng khép; không kính.
- Thêm nếu được: hai ảnh nghiêng (tai, sống mũi, cằm); một đoạn video ngắn đang nói chuyện, để xem thần và tình thái theo Băng giám.

**Thông tin:**
- Giới tính (nam xem bên trái, nữ bên phải).
- Năm sinh âm lịch (để tính tuổi mụ và bộ vị năm nay).
- Muốn xem gì: tổng quát, tính cách, công việc, tiền bạc, giai đoạn hiện tại.

**Cách hỏi:**
- Đã có trong sổ thì không hỏi lại, chỉ hỏi phần thiếu.
- Hỏi kiến thức chung (ấn đường là gì, tam đình là gì): trả lời luôn, không cần ảnh; dùng `--bang`.
- Không gửi ảnh được: đọc theo lời tả, ghi rõ "đọc qua lời tả – độ tin thấp", chỉ luận phần được tả.

## 3. Kiểm ảnh

**Trái, phải:**
- "Trái" là bên trái của người được xem. Với ảnh chụp thẳng không lật, đó là bên phải tấm ảnh.
- Ảnh selfie bằng camera trước thường bị lật gương. Tìm dấu hiệu (chữ trên áo bị ngược, ngôi rẽ tóc người dùng tả) rồi ghi một dòng đầu bài, ví dụ: "Em coi bên phải ảnh là bên trái của anh – anh sửa giúp nếu ảnh bị lật."

**Xếp ảnh vào một mức:**
- **Đủ**: chính diện, rõ, sáng đều.
- **Tạm**: hơi nghiêng, tóc che trán hoặc tai, ánh sáng lệch. Luận phần thấy rõ, bỏ phần bị che.
- **Không đủ**: mờ, nghiêng nhiều, bộ lọc làm đẹp, góc rộng sát mặt, đeo khẩu trang hoặc kính râm. Không luận; nói cụ thể cần chụp lại thế nào.

**Khí sắc không đọc từ ảnh:**
- Đèn, cân bằng trắng, máy và trang điểm làm sai màu da. Chỉ ghi "sắc mặt trên ảnh: …" khi rất rõ, và nói rõ là không tin cậy.
- Sách tướng coi khí sắc là phần đổi nhanh nhất, phải nhìn tận mặt dưới ánh sáng tự nhiên, buổi sáng.

**Nhìn kỹ (khi có công cụ chạy code):** cắt từng vùng (trán, mắt mày, mũi, miệng cằm), phóng to, tăng tương phản, mở bằng công cụ đọc ảnh. Đo tam đình bằng tỉ lệ:
- chân tóc → giữa hai đầu mày;
- giữa hai đầu mày → chân mũi;
- chân mũi → đáy cằm.

## 4. Phiếu quan sát

Chạy `python3 tvbt/nc.py tuong --bang phieu`, điền từng ô.
- Chỉ ghi điều thấy; ô không rõ ghi "không thấy rõ".
- Nốt ruồi, sẹo: tra tên bộ vị bằng `--tim "<vị trí>"`.
- Phiếu là "số liệu gốc": lưu vào sổ; không dán cả bảng vào bài, trừ khi người dùng hỏi.

## 5. Chạy script

- `python3 tvbt/nc.py tuong --nam-sinh <năm âm> --gioi nam|nu [--so-nam 3]`: in bộ vị năm nay, giai đoạn, ba năm tới.
- `--tim "ấn đường"`, `--tim "cánh mũi"`: tìm bộ vị và tuổi ứng với một chỗ trên mặt (ví dụ nốt ruồi).
- `--bang tatca`: in đủ các bảng khung.

## 6. Luận – ba tầng, rồi tổng kết

### Tầng 1 – Khung tĩnh (Ma Y thần tướng, Thần tướng toàn biên)
Xét theo thứ tự, mỗi mục 1–2 câu:
1. **Toàn mặt trước** ("tướng không xét lẻ"):
   - Hình mặt theo ngũ hành (`--bang hinh`); đa số pha hai hành.
   - Tam đình có cân không.
   - Ngũ nhạc có đầy và chầu nhau không: mũi là chủ, hai gò má đỡ hai bên, trán và cằm chầu nhau.
2. **Ngũ quan** (`--bang nguquan`): quan nào "thành" (đạt chuẩn sách), quan nào chưa. Sách: một quan thành thì tốt mười năm.
3. **Thập nhị cung** (`--bang cung`): chỉ nói các cung liên quan câu hỏi:
   - công việc: Quan lộc, Thiên di;
   - tiền: Tài bạch, Điền trạch;
   - bạn bè: Huynh đệ, Nô bộc.
   - Không luận cung Tử tức, Phu thê theo kiểu phán (mục 1).

**Bảng gợi ý ý nghĩa** (lời sách, đã viết lại theo hướng tính cách – xu hướng; dùng làm chất liệu, không đọc nguyên):

| Nét | Sách cho là | Nói với người hỏi |
|---|---|---|
| Trán rộng, cao, đầy | sớm được nâng đỡ, học hành thuận | tuổi trẻ dễ có người dìu dắt, học nhanh |
| Trán hẹp, thấp, nhiều vằn | thiếu trợ lực tuổi trẻ | tự lập sớm, thành nhờ sức mình, hợp đi đường dài |
| Ấn đường rộng, phẳng, sáng | rộng lượng, vận thông | cởi mở, dễ hòa |
| Ấn đường hẹp hoặc vằn dọc | hay lo nghĩ | cẩn thận, chu đáo; nên bớt ôm việc, thư giãn |
| Mày dài quá mắt, sợi thuận | bạn bè, anh em giúp | quan hệ rộng, có người giúp |
| Mày ngắn, rối, giao nhau | tính nóng, ít trợ lực | quyết nhanh, thẳng; nên nhẫn hơn khi làm nhóm |
| Mắt có thần, đen trắng rõ | sáng suốt | tỉnh, nhìn người nhìn việc nhanh |
| Mắt lộ, láo liên | thần tán | dễ phân tâm; ngủ đủ, việc ít mà chắc |
| Sơn căn cao, liền | giữa đời vững | sức bền tốt giữa đời (không nói bệnh) |
| Sơn căn thấp, có vằn ngang | trung niên gặp trở | khoảng 41 tuổi nên làm chắc, tránh liều |
| Mũi thẳng, đầu tròn có thịt, cánh đầy | giữ được tiền | biết làm ra và giữ tiền |
| Lỗ mũi lộ, đầu mũi nhọn | tiền ra nhanh | rộng tay; nên có quỹ để dành |
| Gò má cao có thịt, cân với mũi | có uy, quyền | có tiếng nói, hợp quản lý |
| Gò má lộ xương, mũi thấp | "quyền cao tị thấp" | chịu nhiều áp lực, việc nhiều; nên chia việc (KHÔNG nói "khắc chồng") |
| Nhân trung rõ, sâu, trên hẹp dưới rộng | nền sức tốt | bền bỉ (không nói thọ, con) |
| Pháp lệnh rõ, dài | uy tín nghề nghiệp | nghề vững, lời nói có trọng lượng |
| Miệng vuông, môi đầy, khóe lên | ăn nói, có lộc ăn | lạc quan, nói có duyên |
| Khóe miệng trễ, môi mỏng | ít lời, khó gần | kín đáo, kỹ; cười nhiều sẽ thuận người |
| Cằm vuông hoặc tròn đầy | hậu vận vững | về sau ổn định, có nơi có chốn |
| Cằm nhọn, lẹm | hậu vận phải tự lo | nên tích lũy, lo nhà cửa sớm |
| Tai cao hơn mày, dái dày | tuổi nhỏ được chăm, phúc hậu | nền nếp tốt từ nhỏ |

**Ngũ hành hình** – chỉ nói xu hướng tính cách, không nói nghề "phải" làm:
- Kim (vuông): nguyên tắc, quyết.
- Mộc (dài, gầy): nghĩ sâu, có lý tưởng.
- Thủy (tròn): mềm dẻo, giỏi giao tiếp.
- Hỏa (trên nhọn dưới rộng): nhiệt, nhanh.
- Thổ (dày): chắc, kiên nhẫn, thành muộn mà bền.
Sách nói "kim không ngại vuông, mộc không ngại gầy…": hình đúng hành là hợp cách.

### Tầng 2 – Lưu niên (bộ vị năm nay)
- Lấy từ `nc.py tuong --nam-sinh … --gioi …`. Nói: năm nay vận đi qua chỗ nào trên mặt, chỗ đó trên ảnh ra sao (đầy hay lõm, có nốt ruồi, sẹo, vằn không), và giai đoạn đời đang ở (tam đình, ngũ quan).
- Sách xem lưu niên chủ yếu bằng **khí sắc** chỗ đó (sáng thì thuận, tối thì trở), mà ảnh không đọc khí sắc tin cậy được. Vì vậy:
  - chỉ nói "nên để ý";
  - không phán năm nay có hạn;
  - không dùng một bộ vị để kết luận cả năm.

### Tầng 3 – Thần và tình thái (Băng giám)
- Băng giám coi **thần ở mắt** là chính ("tinh thần của cả người nằm ở hai mắt"); rồi mới đến xương, dáng, nét mặt lúc nói, giọng.
- Có video hoặc người dùng tả: nhận xét thần (tỉnh hay mệt, vững hay dao động), tình thái (nét mặt lúc nói, lúc nghỉ), giọng (tròn, vang hay gấp).
- Chỉ có một ảnh tĩnh: ghi "ảnh tĩnh – chỉ xem được một phần thần", nói rất gọn.
- Thần, tình thái đổi theo giấc ngủ, sức khỏe, tâm trạng; sách cũng coi đây là phần **sửa được**: nghỉ ngơi, tập trung, nói chậm.

### Tổng kết
- **Chỗ đáng tin**: 2–3 ý mà hai tầng trở lên cùng nói (ghi tên tầng trong ngoặc).
- **Chỗ chưa chắc**: ý chỉ một tầng nói, hoặc ảnh chưa rõ.
- **Đối chiếu lá số** (nếu sổ có lá số tử vi, bát tự): chỉ nêu chỗ hai môn cùng chiều, ví dụ "tướng mặt và lá số cùng cho thấy giữa đời tự gây dựng". Hai môn ngược nhau thì nói thẳng là chưa thống nhất. Không tự tính lại lá số trong phần này.
- Kết bằng lời sách: "tướng tùy tâm sinh" – nếp sống, tâm tính đổi thì thần sắc đổi.

## 7. Trình bày và lưu sổ

**Trình bày** theo Bước 4 của SKILL.md:
- Kết luận 2–3 câu, điểm chính 3–5 dòng, nên làm 2–3 dòng.
- Thuật ngữ chỉ để trong ngoặc ở cuối câu (ví dụ "(ấn đường, 28 tuổi)").
- Khoảng 250–400 chữ.
- Dòng cuối in nghiêng: "Xem tướng là tri thức văn hóa truyền thống để tham khảo; nghiên cứu hiện đại không thấy khuôn mặt cho biết tính cách hay số phận."

**Lưu sổ** – theo Quy tắc bảo mật Sổ lá số:
- Doc riêng `claude/so-la-so/<ten-viet-tat>-<nam-sinh>-tuong-mat.md`, đi kèm doc chính, giống doc `-chi-tay`.
- Nội dung:
  - ngày xem;
  - mức ảnh (đủ / tạm), có lật gương không;
  - phiếu quan sát (chữ);
  - lệnh `nc.py tuong` đã chạy;
  - nhật ký `| Ngày | Hỏi gì | Kết luận chính | Thực tế sau đó |`.
- **Không lưu ảnh.** Người khác thì hỏi trước khi lưu.
- Lần sau có ảnh mới: so với phiếu cũ, nói chỗ đã đổi (khí sắc, cân nặng, nếp nhăn đổi theo thời gian).

## 8. Trường phái và nguồn

- **Ma Y thần tướng** (麻衣神相): đề Ma Y đạo giả, đời Tống; bản lưu hành hiện nay là bản biên tập đời Minh – Thanh. Có bộ khung: thập tam bộ vị, lưu niên bộ vị, thập nhị cung, ngũ quan, ngũ nhạc, tứ độc, tam đình lục phủ, ngũ hành hình. Nguồn chính của skill.
- **Thần tướng toàn biên** (神相全編): đề Trần Đoàn, Viên Trung Triệt (袁忠徹) đời Minh hiệu đính. Có bài "Lưu niên vận khí bộ vị ca" mà script dùng.
- **Liễu Trang tướng pháp** (柳莊相法): Viên Củng (袁珙) đời Minh. Nặng về khí sắc và thần.
- **Băng giám** (冰鑑): bảy thiên – Thần cốt, Cương nhu, Dung mạo, Tình thái, Tu mi, Thanh âm, Khí sắc. Bản khắc năm 1829 đã có, nên không phải do Tăng Quốc Phiên viết (ông chỉ được gán tên về sau). Nặng về xem người khi gặp, nói chuyện.
- **Tứ khố toàn thư** (thuật số loại, tướng thư): Nguyệt ba động trung ký, Ngọc quản chiếu thần cục, Thái thanh thần giám, Nhân luân đại thống phú. Là các tướng thư cổ hơn; skill chưa dùng trực tiếp.
- **Sách tiếng Việt**: Nhân tướng học của Trường Minh và Hy Trương (hai quyển: các nét tướng, lý tướng – thần, khí, sắc, phương pháp xem). Ca dao, tục ngữ Việt về tướng người: nghiên cứu của Đặng Quốc Minh Dương (Tạp chí Khoa học ĐHSP TP.HCM, 2025) khảo 210 câu.
- **Skill cộng đồng đã tham khảo** (chỉ dùng làm dữ liệu đối chiếu):
  - brucewu905/face-reading-skill: khung báo cáo.
  - timerzz/kanxiang: tham chiếu diện tướng, cốt tướng.
  - memilin/mayi-face-aesthetics: bản đọc thẩm mỹ, không phán mệnh, ghi trang sách – nguồn trích chính cho vị trí 12 cung.
  - Liyucheng1997/362_mayi-xiangshu: tọa độ bảng bách tuế lưu niên – đối chiếu từng tuổi.
- **Khoa học hiện đại**: Alexander Todorov, *Face Value* (Princeton, 2017). Người ta hình thành ấn tượng về khuôn mặt rất nhanh và khá giống nhau, nhưng các phán đoán tính cách từ mặt phần lớn không chính xác; khuôn mặt không phải "bản đồ" của tính cách. Vì vậy skill coi xem tướng là văn hóa, chỉ nói xu hướng, và cấm dùng để chấm người khác (mục 1).

## 9. Đã kiểm chứng
- Bảng lưu niên 1–99 tuổi:
  - đối chiếu hai bản chép độc lập của "Lưu niên vận khí bộ vị ca": destiny.to (2003) và secretchina (2016);
  - đối chiếu bảng tọa độ của 362_mayi-xiangshu: tên và bên trái/phải khớp từng tuổi;
  - `tu_kiem` kiểm 50 mốc, mỗi tuổi đúng một bộ vị, nam tả nữ hữu.
- 76–99 tuổi: hai bản bài ca khớp nhau (Tý 76–77 … Hợi 98–99; "Thái công chi niên thiêm nhất tuế" = 80–81 ở Dần).
- Vị trí từng chi trên viền mặt theo hình thông dụng: Tý dưới cằm, Ngọ đỉnh trán, Mão bên trái nam. Bài ca không tả chi tiết – **cần xác nhận**.
- Tuổi 100 trở đi: các bản giải không thống nhất (mục 4 của ghi chú script).
- Vị trí 12 cung: theo Ma Y quyển 1 (bản đồ giải, trang 123–133). Các skill cộng đồng lệch nhau ở cung Thiên di và Phúc đức (cùng vùng thiên thương); skill theo Ma Y.
