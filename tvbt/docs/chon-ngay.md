# Chọn ngày đầy đủ (lệnh nc.py ngay) – dùng thay chonngay

> Phần cài đặt và tự kiểm tra đã làm ở Bước 2 của SKILL.md (skill tu-vi-bat-tu-phong-thuy-v3). Mọi file đã có sẵn trong `tvbt/`; bỏ qua mọi chỗ nhắc tới "trích", "vá", "Bước 1/2 của skill v2" hay tên các skill cũ (v2, luan-la-so-chi-tiet, ky-mon-mo-rong, …) – nay tất cả là một bộ.

## Có gì
| Lệnh | Làm gì | Dùng khi |
|---|---|---|
| `ngay` | Chọn ngày đầy đủ: việc nên/kiêng theo ngày và giờ, 60 cát thần, 91 hung sát, hướng Hỷ/Tài/Phúc thần, Quý nhân, Thai thần, Bành Tổ; gộp Hoàng đạo, Trực, 28 Tú, Tam Nương, Nguyệt Kỵ, Dương Công, xung tuổi; chấm 100 điểm, chia 3 nhóm. Có `--toa`/`--huong` thì xét thêm tọa sơn của nhà, mộ | Mọi câu hỏi chọn ngày (thay `chonngay` của v2) |
| `toa` | Bảng 12 tháng của một năm cho một tọa sơn: tháng nào không dùng được, tháng nào cần cân nhắc (Hiệp Kỷ Biện Phương Thư) | Hỏi "năm nay/năm sau có làm nhà, sửa nhà, đặt mộ hướng này được không", trước khi chọn ngày cụ thể |

## Đã kiểm chứng
- **Chọn ngày (`ngay`).**
  - Từ điển phủ hết từ ngữ của dữ liệu lịch: 116 việc, 60 cát thần, 91 hung sát. Đã quét 1900–2100, cứ 3 ngày lấy một mẫu, không sót từ nào chưa dịch.
  - Hoàng đạo, Trực, 28 Tú, Tam Nương, Nguyệt Kỵ, Dương Công, xung tuổi: lấy đúng từ `chonngay` của v2, phần này đã khớp lunar-python trên 40.543 ngày.
  - Có bất biến: ngày lịch ghi kiêng đúng việc chính, hoặc ngày xung tuổi người chủ sự, không bao giờ lọt vào nhóm chọn.
- **Rà soát độc lập.** Đã có một lượt rà soát độc lập; lỗi "ngày lịch ghi 'việc khác không nên' vẫn lọt vào nhóm chọn" đã sửa và có ca thử riêng.
- **Rà soát 11/2026.**
  - Thêm Thọ tử, Sát chủ dương, Sát chủ âm, Vãng vong (theo tháng âm, nguồn lịch Việt Nam). Trước bản này, riêng 2020–2029 có 79 ngày cưới, 60 ngày nhập trạch, 53 ngày động thổ là Thọ tử / Sát chủ dương / Vãng vong mà vẫn vào nhóm "Nên chọn". Nay chạy 1950–2060: 0 ngày như vậy lọt vào nhóm chọn.
  - Kim Lâu, Hoang Ốc, Tam Tai của người chủ sự nay in trong lệnh `ngay`, tính theo **năm âm lịch** của khoảng ngày (trước đây `chonngay` lấy năm dương lịch: chọn ngày cưới 5–20/1/2027 bị tính sang năm Đinh Mùi 2027, tuổi mụ sai 1, Kim Lâu sai).
  - Sửa 3 dòng thần sát nhập sai của lunar-python (tháng Hợi ngày Kỷ Sửu, tháng Mùi ngày Quý Dậu, tháng Dậu ngày Kỷ Dậu).

- **Tọa sơn (11/2026).**
  - Các lệ năm (Tuế phá, Tam sát, tọa sát/hướng sát, Phù thiên không vong, Niên khắc sơn gia kể cả lệ sau Đông chí, Âm phủ, Lục hại, Tử phù, Cứu thoái, Tuần sơn La hầu, Bệnh phù, Đại sát, Đại tướng quân, Kim thần, Phá bại ngũ quỷ) đã đối chiếu với **toàn bộ 50 bảng năm** (Giáp Tuất → Quý Hợi) trong quyển 15–19 của Hiệp Kỷ: khớp hết, chỗ lệch chỉ là lỗi chép của bản sách (vd năm Đinh Sửu ghi "艮" thay "庚").
  - Lệ tháng đối chiếu với ví dụ trong sách: năm Giáp Tý tháng nào khắc sơn nào (q.2), năm Nhâm Thân sau Đông chí khắc sơn Kim, Đại nguyệt kiến năm Kỷ Mão, các tháng "hoàn vị".
  - Âm phủ, Phù thiên theo 10 can khớp khởi lệ đã sửa của sách và khớp một bộ mã độc lập (FengShui-Skill/nianshen.py).

## Chạy
Tham số ngày giờ giống `tvbt.py`: `--ngay YYYY-MM-DD --gio HH:MM --gioi nam|nu --noi "<tỉnh>"`, cộng `--am`, `--nhuan`, `--kinhdo`, `--utc`, `--mien`, `--gio-dong-ho`, `--ty` khi cần. Mọi lệnh có `--help`.

```bash
python3 tvbt/nc.py ngay --tu 2026-11-01 --den 2026-11-30 --viec khaitruong --tuoi "An:1990:Thủy+Kim:Hỏa" [--thu T7,CN] [--gon]
python3 tvbt/nc.py ngay --tu 2027-03-01 --den 2027-05-31 --viec dongtho --huong 180 [--sua-nha] --tuoi "Chủ nhà:1980"
python3 tvbt/nc.py ngay --tu 2026-11-10 --den 2026-12-31 --viec antang --toa "Cấn" --tuoi "Người mất:1940"
python3 tvbt/nc.py toa --nam 2027 --huong "Ngọ" [--kieu nha|sua|mo]
```

## Luận
Trình bày theo v2: (1) bảng số liệu, (2) luận theo mục, (3) lưu ý và độ chắc chắn. Không phán chắc chắn, không gieo sợ hãi, không quyết định y tế, tài chính, pháp lý thay người dùng.

### 4.1 Chọn ngày đầy đủ (lệnh `ngay`)
Lệnh này **thay** lệnh `chonngay` của v2 khi người dùng cần chọn ngày cho một việc cụ thể. Nó gộp tiêu chí lịch Việt Nam của v2 với lịch nên/kiêng đầy đủ của Hiệp Kỷ Biện Phương Thư.

**Hỏi trước khi chạy:**
- việc gì;
- khoảng ngày (≤ 93 ngày);
- năm sinh âm lịch của người chủ sự;
- nếu đã luận Bát tự cho người đó: hành cần và hành kỵ. Truyền dạng `"Tên:1990:Thủy+Kim:Hỏa"`. Không có thì bỏ trống, không tự đoán.

Muốn chỉ chọn trong một số thứ trong tuần thì thêm `--thu T7,CN`.

**Các loại việc** (`--viec`):
- chung, cuoi, anhoi
- dongtho, nhaptrach, muanha
- khaitruong, kyhopdong, nhapkho, xuathang
- xuathanh, nhamchuc, thuenguoi
- chuabenh, kientung
- antang, lapbantho, kegiuong, datbep
- trongcay, nhaphoc

**Đọc kết quả:**
1. Script chia ngày thành ba nhóm: **Nên chọn** (≥ 70 điểm), **Dự phòng** (55–69), **Nên tránh**.
   - Ngày bị đưa vào nhóm tránh khi gặp một trong các trường hợp sau, dù điểm cao đến đâu:
     - lịch ghi kiêng đúng việc đó;
     - ngày "mọi việc không nên";
     - Nguyệt Phá;
     - Tam Nương, Nguyệt Kỵ, Dương Công;
     - Thọ tử (mọi việc);
     - Sát chủ dương khi cưới hỏi, ăn hỏi, động thổ, nhập trạch, mua nhà, khai trương, ký kết, nhậm chức; Sát chủ âm khi an táng, cưới hỏi, ăn hỏi, động thổ;
     - Vãng vong khi xuất hành, cưới hỏi, ăn hỏi, nhập trạch, nhậm chức, chữa bệnh, nhận người (xét cả bản tháng âm của lịch Việt Nam và bản tháng tiết của Hiệp Kỷ);
     - xung tuổi người chủ sự.
   - Gặp Sát chủ / Vãng vong với việc khác: chỉ ghi chú, không loại.
   - Đầu bảng có dòng **Kim Lâu / Hoang Ốc / Tam Tai** theo năm âm lịch: Kim Lâu xét cho cưới hỏi (tuổi mụ cô dâu) và làm nhà; Hoang Ốc, Tam Tai cho làm nhà, động thổ. Phạm thì nói các cách dân gian (mượn tuổi, lùi năm) như kinh nghiệm tham khảo.
   - Nói lý do loại khi người dùng hỏi về một ngày cụ thể.
2. Đưa 2–3 ngày tốt nhất. Mỗi ngày gồm:
   - lý do: lịch ghi nên làm việc này, Trực hợp, Hoàng đạo, cát thần lớn như Thiên Đức, Nguyệt Đức, Thiên Xá, Thiên Nguyện, Mẫu Thương;
   - **giờ tốt**: giờ hoàng đạo, đã bỏ giờ xung tuổi và giờ lịch ghi kiêng. Dấu ★ là giờ lịch ghi nên làm đúng việc đó;
   - **hướng**:
     - xuất hành, khai trương: theo Hỷ thần hoặc Tài thần;
     - gặp người có chức quyền: theo Quý nhân;
     - nhà có người mang thai: nhắc vị trí Thai thần, tránh đục phá chỗ đó.
3. Hung sát của ngày được chọn: chỉ nêu những sao nặng (Nguyệt Phá, Tứ Phế, Tứ Ly, Vãng Vong, Quy Kỵ…). Nhắc rằng cát thần lớn có thể giải bớt hung sát nhỏ.
4. Lịch nên/kiêng tính theo tháng tiết khí (lịch Trung Quốc); Hoàng đạo tính theo tháng âm (lịch Việt Nam).
   - Hai cách có thể khác nhau ở ngày giáp tháng. Script ghi "các cách tính chưa đồng thuận" và hạ điểm độ tin.
   - Gặp trường hợp này, nói rõ cho người dùng.
5. Bành Tổ bách kỵ chỉ nhắc khi đúng việc, ví dụ ngày Hợi với cưới hỏi, ngày Tỵ với đi xa.

### 4.2 Xét tọa sơn nhà, mộ (`--toa` / `--huong`, lệnh `toa`)
Sách chọn ngày cổ (Hiệp Kỷ Biện Phương Thư, quyển 33 "Luận phù sơn", "Luận lập hướng"; quyển 34) nói: làm nhà, đặt mộ thì ngày phải hợp cả **tọa sơn** (phía lưng) và hướng, không chỉ hợp tuổi. Chỉ áp dụng cho `dongtho` (động thổ, xây, sửa) và `antang` (an táng, xây mộ).

**Hỏi trước khi chạy:** nhà/mộ quay mặt về đâu. Tốt nhất là **độ la bàn** đo ở giữa nhà nhìn ra cửa chính (vd 182°) → `--huong 182`; biết tên sơn (vd "tọa Nhâm hướng Bính") thì `--toa Nhâm`. Chỉ biết "hướng Nam" là chưa đủ: một hướng gồm 3 sơn khác nhau (Bính, Ngọ, Đinh), kết quả có thể khác – hỏi lại hoặc chạy cả 3. Sửa nhà đang ở (không xây mới) thì thêm `--sua-nha`. Chôn thêm vào mộ cũ, mộ tổ (phụ táng) thì thêm `--phu-tang` (lệnh `toa`: `--kieu phutang`).

**Script xét gì** (năm tính từ Lập xuân, tháng theo tiết khí):
- **Loại ngày** (sách nói không được phạm hoặc phải có phép chế mà script không tính):
  - năm: Tuế phá xung tọa, Tam sát ở tọa, Phục binh/Đại họa ở tọa, Âm phủ Thái Tuế (theo quái), Niên khắc sơn gia (xây mới không chế được; an táng chỉ dùng ngày/tháng có nạp âm khắc lại nạp âm năm – "chế" – hoặc được nạp âm năm sinh ra rồi sinh lại mộ vận – "hóa khắc thành sinh", cách lời bàn q.34 ưu tiên; sửa nhà không động móng chỉ cảnh báo; phụ táng không xét), Mậu Kỷ đô thiên ở tọa hoặc hướng (Hiệp Kỷ không có phép chế; sửa nhà ở phía Mậu Kỷ cũng loại – q.33 "tất bất khả tu"), Thái Tuế ở hướng, Tam sát ở hướng (xây mới), Tuần sơn La hầu ở hướng trong năm nó cùng cung Thái Tuế (năm Tý Sửu Mão Thìn Ngọ Mùi Dậu Tuất), ngồi Thái Tuế năm Tý Ngọ Mão Dậu hoặc Thái Tuế chồng Mậu Kỷ sát;
  - tháng: Nguyệt phá xung tọa, Nguyệt Âm phủ (sửa nhà: cảnh báo; phụ táng: không xét), Nguyệt khắc sơn gia (sửa nhà: cảnh báo; phụ táng: không xét), Đại nguyệt kiến "hoàn vị" (với nhà);
  - ngày: chi ngày xung tọa (sơn Thìn Tuất Sửu Mùi thì chỉ cảnh báo – sách nói một chữ xung tạm được).
- **Cần cân nhắc** (sách xếp nhẹ hơn, có thể chế, hoặc các sách nói khác nhau): bàng Âm phủ, Phù thiên không vong, Lục hại, Tử phù, Cứu thoái, Tuần sơn La hầu, Bệnh phù, Đại sát (Đả đầu hỏa), Đại/Tiểu nguyệt kiến, Tam sát tháng, Thái Tuế ở tọa; với sửa nhà thêm Âm phủ ở tọa (Tông Kính ghi tu tạo không kỵ), Đại tướng quân, Kim thần, Phá bại ngũ quỷ, Thiên/Địa quan phù; theo ngày: Âm phủ ngày, khắc sơn gia theo ngày, xung chi đồng cung (sơn can/duy). Ngày có điều cần cân nhắc theo ngày bị trừ 5 điểm.

**Đọc kết quả:**
1. Đầu kết quả có bảng theo tháng. Cả năm bị loại (vd năm Đinh Mùi 2027 khắc 13 sơn Thủy, Thổ – nhà tọa Tý, Nhâm, Sửu, Khôn… không xây mới được) thì nói ngay đầu bài, gợi ý lùi năm hoặc hỏi thầy về phép chế; đừng chỉ đưa "không có ngày".
2. Nhắc giới hạn: script đã tính chế, hóa khắc sơn gia bằng nạp âm tháng, ngày khi an táng; **chưa tính** chế Tam sát bằng tam hợp cục, chế sát bằng tứ trụ, Tam kỳ, Tử bạch, quý nhân lộc mã; Bính Đinh hỏa, quan phù phi cung theo tháng; long mạch, bổ long. Việc lớn (xây nhà, cải táng) nên mời thầy xem thêm tại chỗ.

## Trường phái và giới hạn (nói rõ khi liên quan)
- **Tọa sơn:** theo Hiệp Kỷ Biện Phương Thư (bản Khâm định 1741, có sửa khởi lệ của Thông thư). Những chỗ script phải chọn cách hiểu:
  - Sơn can/duy (Nhâm, Quý, Cấn, Giáp…) "đồng cung" với chi cùng cung bát quái chính châm (Nhâm Quý với Tý; Cấn với Sửu, Dần…) – theo lời bàn Tuần sơn La hầu ở q.34; bị xung qua đồng cung chỉ cảnh báo, vì bảng năm của sách chỉ ghi Tuế phá ở sơn chi.
  - Bàng Âm phủ (theo can) chỉ cảnh báo: Hiệp Kỷ q.8 nói Khâm thiên giám chỉ dùng quái, "dùng can có lý nhưng không thân thiết nên không lấy".
  - Sơn Kim sau Đông chí: theo lệ mộ vận (q.2) thì đổi, nhưng nhiều bảng năm vẫn ghi sơn Kim bị khắc cả năm – script không loại mà cảnh báo.
  - Phụ táng (chôn thêm vào mộ cũ, mộ tổ – `--phu-tang`): bỏ Niên/Nguyệt/Ngày khắc sơn gia (q.2 "旧茔附葬者皆不论", q.34 "袝葬祖茔…亦不忌") và Âm phủ chính, bàng (q.34 dẫn Tông Kính "如祔葬及修造正傍俱不忌"); mọi sát khác xét như an táng. Hiệp Kỷ không bàn hợp táng vợ chồng hay tuổi người đã chôn trước; mệnh xét là người mới mất ("葬以亡命为主"), người chủ tế chỉ kiêng bị xung (q.33 Luận tướng chủ). Sửa không động móng cũng không xét khắc sơn gia (Thông thư).
  - Chế sát (rà soát độc lập 11/2026, đọc Hiệp Kỷ q.2, 3, 8, 11, 33–36): Tuế phá "lệ không có phép chế"; Thái Tuế chỉ dùng "hợp", không khắc; Tam sát ở tọa không chế, ở hướng, phương chế bằng tam hợp cục (tháng tam hợp đắc lệnh hoặc Tam sát hưu tù); Mậu Kỷ không có phép chế. Nguyên tắc q.34: chế sát là việc sửa phương, không phải sửa sơn hay táng – tọa sơn thì bổ, không khắc.
  - Âm phủ, Phù thiên ghi theo quái: quái Khảm Ly Chấn Đoài lấy sơn Tý Ngọ Mão Dậu (cách 24 sơn nạp giáp của sách); Âm phủ gồm cả bàng Âm phủ (hai can bị khắc). Bỏ "Âm phủ tam hợp" của Thông thư vì sách bác.
  - Mậu Kỷ đô thiên (ngũ hổ độn từ can năm ra can Mậu, Kỷ): q.33 ghi "ở hướng mạnh hơn ở sơn", phương Mậu Kỷ của năm "tất bất khả tu", không có phép chế; lời bàn q.34 chỉ bác câu của Tông Kính "Mậu Kỷ không động cũng hung". Từ 11/2026 script loại khi Mậu Kỷ ở tọa hoặc hướng (trước đó chỉ cảnh báo vì hiểu nhầm là sách nghi cả lệ này). Đại nguyệt kiến chỉ loại ở tháng "hoàn vị" theo lời bàn q.34; Tiểu nguyệt kiến không kỵ an táng (theo Thông thư, sách đồng ý).
  - Đại/Tiểu nguyệt kiến: q.33 nói xây mới (khai sơn lập hướng) không cần xét thần sát tu phương; q.34 lại nói Đại nguyệt kiến chiếm sơn, hướng đều hung – script vẫn cảnh báo (loại khi hoàn vị); chưa xét Đại nguyệt kiến chồng Mậu Kỷ, Ngũ hoàng.
  - Can chi năm/tháng tính theo giờ Bắc Kinh (lunar-python); ngày giao tiết có thể lệch.
- **Chọn ngày:** việc nên/kiêng, cát thần, hung sát, hướng thần theo Hiệp Kỷ Biện Phương Thư (qua lunar-python), tính theo tháng tiết khí và giờ Bắc Kinh. Ngày giáp ranh tháng tiết có thể lệch. Hoàng đạo theo tháng âm như lịch Việt Nam. Thang 100 điểm là quy ước của skill.
- Dương Công kỵ nhật theo bản Việt Nam (có 8/7); sách Trung Quốc ghi 1/7. Thọ tử theo bản Việt Nam (một can chi mỗi tháng); bản Trung Quốc (受死) xét chi. Sát chủ âm theo *Ngọc Hạp Chánh Tông* (Viên Tài Hà Tấn Phát), tr. 128–129, mục "Ngày Sát chủ".
  - Sách dẫn thơ Hán văn "Nhứt Tỵ, nhị Tý, tam Dương vị / Tứ Thố, ngũ Hầu, lục Khuyển qui / Thất Trư, bát Ngưu, cửu Mã thị / Thập Kê, thập nhứt Hổ, thập nhị Long", nên tháng 7 là ngày Hợi, tháng 8 là ngày Sửu. Phần giải nghĩa từng tháng trong sách cũng ghi như vậy (theo bản chép của dự án calendar-hana). Báo Lâm Đồng/Nghệ An và Chronos ghi giống sách.
  - Bảng đảo tháng 7/8 thành Sửu/Hợi đi theo một bài thơ Nôm (xemlicham, mytour, vietaa). Script chỉ dùng bảng này để tránh thêm khi an táng.
  - Sách ghi ngày Sát chủ kỵ cất nhà, cưới gả; lịch Việt Nam ngày nay ghi kỵ an táng. Từ 11/2026 script loại ngày này với cả ba việc. Xem thêm `docs/co-ban.md` phần trường phái.
