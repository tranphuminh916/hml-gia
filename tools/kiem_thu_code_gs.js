// Kiểm thử Code.gs (một số điện thoại = một tài khoản) bằng giả lập Google Sheet. Chạy: node tools/kiem_thu_code_gs.js apps-script/Code.gs
const fs = require('fs'), vm = require('vm');
function makeSheet() {
  const rows = [];  // mảng hàng, mỗi hàng là mảng giá trị (1-based khi truy cập)
  const sh = {
    rows,
    getLastRow: () => rows.length,
    getLastColumn: () => rows.reduce((m, r) => Math.max(m, r.length), 0),
    getSheetId: () => 1,
    setFrozenRows() {},
    appendRow(a) { rows.push(a.map(x => typeof x === 'string' && x.startsWith("'") ? x.slice(1) : x)); },
    getRange(r, c, nr = 1, nc = 1) {
      const rg = {
        getValues: () => Array.from({ length: nr }, (_, i) => Array.from({ length: nc }, (_, j) => { const row = rows[r - 1 + i] || []; const v = row[c - 1 + j]; return v === undefined ? '' : v; })),
        getValue: () => rg.getValues()[0][0],
        setValues(vals) { vals.forEach((row, i) => row.forEach((v, j) => { while (rows.length < r + i) rows.push([]); const R = rows[r - 1 + i]; while (R.length < c + j) R.push(''); R[c - 1 + j] = typeof v === 'string' && v.startsWith("'") ? v.slice(1) : v; })); return rg; },
        setValue(v) { return rg.setValues([[v]]); },
        setFontWeight() { return rg; }, setBackground() { return rg; },
        createTextFinder(t) { let whole = false; const f = { matchEntireCell(b) { whole = b; return f; }, findNext() {
          for (let i = 0; i < nr; i++) for (let j = 0; j < nc; j++) { const v = String(rg.getValues()[i][j]); if (whole ? v === String(t) : v.includes(String(t))) return { getRow: () => r + i }; } return null; } }; return f; }
      };
      return rg;
    }
  };
  return sh;
}
const sheets = {};
const ss = { getSheetByName: n => sheets[n] || null, insertSheet: n => (sheets[n] = makeSheet()), getUrl: () => 'https://sheet' };
const props = { CAN_KICH_HOAT: '1', LUOT_XEM_MOI_KHACH: '3', BAO_EMAIL: '', FIREBASE_CONFIG: '' };
let NGAY = ['13/11/2026', '20261113'];
const cache = {};
const mails = [];
const ctx = {
  SpreadsheetApp: { getActiveSpreadsheet: () => ss },
  PropertiesService: { getScriptProperties: () => ({ getProperty: k => props[k] ?? null, setProperty: (k, v) => { props[k] = String(v); },
    getKeys: () => Object.keys(props), deleteProperty: k => { delete props[k]; } }) },
  LockService: { getScriptLock: () => { return { waitLock() { if (ctx.__locked) throw new Error('khóa lồng nhau'); ctx.__locked = true; }, releaseLock() { ctx.__locked = false; } }; } },
  CacheService: { getScriptCache: () => ({ get: k => cache[k] ?? null, put: (k, v) => { cache[k] = v; }, remove: k => { delete cache[k]; } }) },
  Utilities: { formatDate: (d, tz, f) => f === 'yyyyMMdd' ? NGAY[1] : f === 'dd/MM/yyyy' ? NGAY[0] : f === 'HH:mm' ? '14:30' : NGAY[0] + ' 14:30:00',
    getUuid: () => require('crypto').randomUUID(),
    computeHmacSha256Signature: (v, k) => [...require('crypto').createHmac('sha256', k).update(v).digest()],
    base64EncodeWebSafe: b => Buffer.from(b).toString('base64').replace(/\+/g, '-').replace(/\//g, '_') },
  ScriptApp: { getService: () => ({ getUrl: () => 'https://script.google.com/macros/s/X/exec' }) },
  MailApp: { sendEmail: (...a) => mails.push(a) },
  Session: { getEffectiveUser: () => ({ getEmail: () => 'owner@x' }) },
  HtmlService: { createHtmlOutput: h => { const o = { html: h, setTitle: () => o, addMetaTag: () => o }; return o; } }, ContentService: {}, UrlFetchApp: {},
  console
};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(process.argv[2], 'utf8').replace(/var FIREBASE_CFG = \{[^;]*\};/, 'var FIREBASE_CFG = null;'), ctx);
const api = (khachId, body) => ctx.api({ ...body, khachId });
let ok = 0, fail = 0;
const kt = (ten, dk, x) => { if (dk) ok++; else { fail++; console.log('SAI:', ten, JSON.stringify(x)); } };
const K = () => sheets['Khách'].rows, dongCua = id => K().find(r => r[0] === id);
const khach = (ten, sdt) => ({ ten, gioi: 'nam', ngay: '1990-01-01', gio: '08:00', noi: 'Hà Nội', lienHe: sdt });
const luot = (id, n) => api(id, { action: 'dungluot', luotId: 'L' + id + n + 'xxxx', luot: { khach: 'x', xemCho: {}, muc: 'Lá số', chiTiet: '' } });

// 1. Máy A đăng ký, kích hoạt bằng mã, xem hết 3 lượt
let r = api('mayAaaaa', { action: 'dangky', khach: khach('Khách Một', '0912 345 678') });
kt('đăng ký A', r.ok && r.trangThai === 'cho', r);
const maA = String(dongCua('mayAaaaa')[13]);
r = api('mayAaaaa', { action: 'kichhoat', maKichHoat: maA });
kt('kích hoạt A', r.ok && r.trangThai === 'da' && !r.khachIdMoi, r);
for (let i = 1; i <= 3; i++) kt('A xem lượt ' + i, luot('mayAaaaa', i).ok);
r = luot('mayAaaaa', 4); kt('A hết lượt', !r.ok && r.ma_loi === 'het_luot_xem', r);

// 2. Máy B (điện thoại khác) đăng ký cùng số: chờ kích hoạt, mã giống A; kích hoạt xong dùng chung tài khoản A
r = api('mayBbbbb', { action: 'dangky', khach: khach('Khách Một', '+84912345678') });
kt('đăng ký B chờ', r.ok && r.trangThai === 'cho', r);
kt('mã B = mã A', String(dongCua('mayBbbbb')[13]) === maA, dongCua('mayBbbbb'));
r = luot('mayBbbbb', 1); kt('B chưa kích hoạt không xem được', !r.ok, r);
r = api('mayBbbbb', { action: 'kichhoat', maKichHoat: maA });
kt('kích hoạt B -> đổi sang mã A', r.ok && r.khachIdMoi === 'mayAaaaa', r);
kt('dòng B ghi gộp', String(dongCua('mayBbbbb')[12]).startsWith('Gộp vào mayAaaaa'), dongCua('mayBbbbb'));
r = luot('mayBbbbb', 2); kt('B (mã cũ) vẫn hết lượt', !r.ok && r.ma_loi === 'het_luot_xem' && r.khachIdMoi === 'mayAaaaa', r);
r = api('mayBbbbb', { action: 'toi' }); kt('toi B: lượt 3/3, mã mới A', r.ok && r.trangThai === 'da' && r.luot.da === 3 && r.luot.duoc === 3 && r.khachIdMoi === 'mayAaaaa', r);

// 3. Chủ cấp thêm 2 lượt cho A: B dùng được, đếm chung
dongCua('mayAaaaa')[15] = 5;
kt('B xem lượt 4 (đếm chung)', luot('mayAaaaa', 5).ok);
r = api('mayAaaaa', { action: 'toi' }); kt('toi A 4/5', r.luot.da === 4 && r.luot.duoc === 5, r);

// 4. Hai máy đã kích hoạt riêng từ trước (dữ liệu cũ): mở trang thì gộp, cộng lượt đã xem
const KH = sheets['Khách'];
KH.appendRow(['cuCCCCCC', 't', 't', 'Khách Hai', 'Nam', '1985', 'Dương', '', '', '0987654321', 3, 2, 'Đã kích hoạt', '111111', 't', 3, '']);
KH.appendRow(['cuDDDDDD', 't', 't', 'Khách Hai', 'Nam', '1985', 'Dương', '', '', '0987654321', 2, 1, 'Đã kích hoạt', '111111', 't', 4, '']);
r = api('cuDDDDDD', { action: 'toi' });
kt('gộp dữ liệu cũ: D -> C, đã xem 5, được xem 4', r.ok && r.khachIdMoi === 'cuCCCCCC' && r.luot.da === 5 && r.luot.duoc === 4, r);
kt('số lần luận cộng', dongCua('cuCCCCCC')[11] === 3, dongCua('cuCCCCCC'));
r = api('cuCCCCCC', { action: 'toi' }); kt('toi C không gộp lại lần nữa', r.ok && !r.khachIdMoi && r.luot.da === 5, r);

// 5. Máy cũ kích hoạt muộn (dòng cũ hơn) khi máy mới đã kích hoạt: vẫn về một tài khoản
r = api('mayEeeee', { action: 'dangky', khach: khach('Khách Ba', '0901111222') });
r = api('mayFffff', { action: 'dangky', khach: khach('Khách Ba', '0901111222') });
const maE = String(dongCua('mayEeeee')[13]);
r = api('mayFffff', { action: 'kichhoat', maKichHoat: maE }); kt('F kích hoạt trước', r.ok && !r.khachIdMoi, r);
kt('F xem 1', luot('mayFffff', 1).ok);
r = api('mayEeeee', { action: 'kichhoat', maKichHoat: maE }); kt('E kích hoạt sau -> E là dòng chính, F gộp vào', r.ok && !r.khachIdMoi, r);
r = api('mayFffff', { action: 'toi' }); kt('F đổi sang E, đã xem 1', r.khachIdMoi === 'mayEeeee' && r.luot.da === 1, r);

// 6. Đổi số điện thoại trên tài khoản đã kích hoạt: phải kích hoạt lại, mã theo số mới
r = api('mayAaaaa', { action: 'dangky', khach: khach('Khách Một', '0912345678') });
kt('sửa thông tin cùng số: vẫn đã kích hoạt', r.ok && r.trangThai === 'da', r);
r = api('mayEeeee', { action: 'dangky', khach: khach('Khách Ba', '0912345678') });
kt('đổi sang số của A: phải kích hoạt lại', r.ok && r.trangThai === 'cho', r);
kt('mã mới là mã của số A (chủ số A mới có)', String(dongCua('mayEeeee')[13]) === maA, dongCua('mayEeeee'));

// 7. Tài khoản bị khóa: máy mới cùng số kích hoạt xong cũng bị khóa
dongCua('cuCCCCCC')[12] = 'Khóa';
r = api('mayGgggg', { action: 'dangky', khach: khach('Khách Hai', '0987654321') });
r = api('mayGgggg', { action: 'kichhoat', maKichHoat: '111111' });
kt('máy mới của số bị khóa: khóa', !r.ok && r.ma_loi === 'khoa' && r.khachIdMoi === 'cuCCCCCC', r);

// 8. Lượt xem ghi bằng mã cũ (trước khi gộp) vẫn được luận / xem lại
kt('cùng khách (mã cũ đã gộp)', ctx.cungKhach_('mayBbbbb', 'mayAaaaa') && !ctx.cungKhach_('mayAaaaa', 'cuCCCCCC'));

// 9. Khách xin thêm lượt, chủ bấm số trong thư: được thêm đúng số đó, chỉ trong ngày
const thuCuoi = () => mails[mails.length - 1][0];
const linkSo = (thu, n) => { const m = thu.htmlBody.match(new RegExp('href="([^"]*&amp;n=' + n + '&amp;[^"]*)"')); return m && m[1].replace(/&amp;/g, '&'); };
const bam = url => { const q = Object.fromEntries(new URL(url).searchParams); return ctx.doGet({ parameter: q }).html; };
r = api('mayAaaaa', { action: 'toi' }); const goc = r.luot.duoc;          // 5 (chủ đã sửa ô P ở bước 3)
while (luot('mayAaaaa', 'h' + Math.random().toString(36).slice(2, 6)).ok);   // xem đến hết lượt
r = api('mayAaaaa', { action: 'xinluot', soLuot: 2, loiNhan: 'xem cho con' });
kt('xin thêm: gửi thư', r.ok && mails.length && /xin thêm 2 lượt xem/.test(thuCuoi().subject), r);
kt('thư có nút 1 2 3 5 10', [1, 2, 3, 5, 10].every(n => linkSo(thuCuoi(), n)), thuCuoi().htmlBody.slice(0, 300));
let h = bam(linkSo(thuCuoi(), 2));
kt('bấm 2: trang báo đã duyệt', /Đã duyệt/.test(h) && /2 lượt xem/.test(h), h.slice(0, 300));
kt('cột V ghi +2 hôm nay', dongCua('mayAaaaa')[21] === '13/11/2026: +2', dongCua('mayAaaaa'));
r = api('mayAaaaa', { action: 'toi' }); kt('được xem = gốc + 2', r.luot.duoc === goc + 2, r);
const thuXem = thuCuoi();
h = bam(linkSo(thuXem, 5)); r = api('mayAaaaa', { action: 'toi' });
kt('bấm số khác (5) cho cùng yêu cầu: thay số cũ', r.luot.duoc === goc + 5 && dongCua('mayAaaaa')[21] === '13/11/2026: +5', r);
h = bam(linkSo(thuXem, 5)); r = api('mayAaaaa', { action: 'toi' });
kt('bấm lại cùng số: không cộng dồn', r.luot.duoc === goc + 5, r);
kt('xem được thêm', luot('mayAaaaa', 'z1').ok);
h = bam(linkSo(thuXem, 3).replace(/s=[^&]+/, 's=sai'));
kt('link sửa chữ ký: từ chối', /không hợp lệ/.test(h), h.slice(0, 200));
h = bam(linkSo(thuXem, 3).replace('n=3', 'n=30'));
kt('link sửa số: từ chối', /không hợp lệ/.test(h), h.slice(0, 200));
kt('máy B (đã gộp) thấy cùng số', api('mayBbbbb', { action: 'toi' }).luot.duoc === goc + 5);
NGAY = ['14/11/2026', '20261114'];
r = api('mayAaaaa', { action: 'toi' }); kt('qua ngày: số cấp thêm hết hạn', r.luot.duoc === goc, r);
NGAY = ['13/11/2026', '20261113'];
// 10. Xin thêm lần luận trọn đời, chủ bấm 1
r = api('mayAaaaa', { action: 'xinluan', loai: 'trondoi', soLan: 1 });
kt('xin luận: thư', r.ok && /xin thêm 1 lần luận trọn đời/.test(thuCuoi().subject), thuCuoi().subject);
kt('luận trước khi duyệt: 0 thêm', ctx.themLuan_('mayAaaaa', 'trondoi') === 0);
h = bam(linkSo(thuCuoi(), 1));
kt('duyệt 1 lần trọn đời', /1 lần trọn đời/.test(h) && dongCua('mayAaaaa')[22] === '13/11/2026: trọn đời +1', [h.slice(0, 200), dongCua('mayAaaaa')[22]]);
kt('themLuan_ trọn đời = 1, luận giải = 0', ctx.themLuan_('mayAaaaa', 'trondoi') === 1 && ctx.themLuan_('mayAaaaa', 'luan') === 0);
dongCua('mayAaaaa')[18] = 2;   // chủ cấp lâu dài 2 (cột S)
kt('cộng lâu dài + hôm nay', ctx.themLuan_('mayAaaaa', 'trondoi') === 3);
NGAY = ['14/11/2026', '20261114'];
kt('qua ngày: chỉ còn lâu dài', ctx.themLuan_('mayAaaaa', 'trondoi') === 2);
NGAY = ['22/11/2026', '20261122'];
h = bam(linkSo(thuXem, 2)); kt('link quá 7 ngày: hết hạn', /hết hạn/.test(h), h.slice(0, 200));
console.log(`ĐẠT ${ok}, SAI ${fail}`);
process.exit(fail ? 1 : 0);
