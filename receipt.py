# -*- coding: utf-8 -*-
"""Diagnosis Report — bank-receipt jaisi professional printable receipt.

Receipt par: header, Report ID, date/time, result, treatment, dept contact,
QR code (scan karne se report ki details text me khul jati hain — koi server
nahi chahiye, data QR ke andar hai), aur ek saaf disclaimer ke ye AI-based
advice hai. Jhooti 'sarkari verified' mohar NAHI banai gayi — seal par
sirf 'FasalShield AI — Diagnosis Report' likha hai, jo sach hai.
"""
import base64
import datetime
import io
import os


def _img_b64(relpath, mime):
    try:
        path = os.path.join(os.path.dirname(__file__), relpath)
        if os.path.exists(path):
            return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()
    except Exception:
        pass
    return ""


def make_report_id(scan_db_id=None, now=None):
    now = now or datetime.datetime.now()
    if scan_db_id:
        return f"FS-{now.year}-{int(scan_db_id):04d}"
    return f"FS-{now.strftime('%Y%m%d')}-{now.strftime('%H%M%S')}"


def qr_png_bytes(text: str) -> bytes:
    import segno
    qr = segno.make(text, error="m")
    buf = io.BytesIO()
    qr.save(buf, kind="png", scale=6, border=2, dark="#14532d")
    return buf.getvalue()


def report_text(rep: dict) -> str:
    lines = [
        "🌿 FasalShield AI — Diagnosis Report",
        f"Report ID: {rep['report_id']}",
        f"Date: {rep['when']}",
        f"Result: {rep['label']}",
        f"Confidence: {rep['confidence']:.1f}%",
    ]
    if rep.get("severity") is not None:
        lines.append(f"Severity (estimate): {rep['severity']:.1f}% of leaf area")
    lines += [
        f"Treatment: {rep['treatment']}",
        f"Prevention: {rep['prevention']}",
        "Expert help: Agriculture Extension Sindh Helpline 0311-1646111",
        "Note: AI-based advice hai — final tasdeeq agriculture officer se karein.",
        "— Asad Ali & Ali Shan, BS AI, BBS-UTECH Khairpur Mirs",
    ]
    return "\n".join(lines)


def receipt_html(rep: dict, qr_bytes: bytes) -> str:
    qr_b64 = base64.b64encode(qr_bytes).decode()
    logo_uri = _img_b64(os.path.join("assets", "bbsutech-logo.png"), "image/png")
    pa_uri = _img_b64(os.path.join("team", "asad-ali.jpg"), "image/jpeg")
    ps_uri = _img_b64(os.path.join("team", "ali-shan.jpg"), "image/jpeg")
    logo_img = f'<img src="{logo_uri}" style="height:58px;float:right" alt="BBS-UTECH">' if logo_uri else ""
    made_row = ""
    if pa_uri and ps_uri:
        made_row = (f'<div style="margin-top:10px;display:flex;align-items:center;gap:8px">'
                    f'<img src="{pa_uri}" style="width:42px;height:42px;border-radius:50%;object-fit:cover;border:2px solid #16a34a">'
                    f'<img src="{ps_uri}" style="width:42px;height:42px;border-radius:50%;object-fit:cover;border:2px solid #16a34a">'
                    f'<span>Made by <b>Asad Ali</b> &amp; <b>Ali Shan</b> - BS AI, BBS-UTECH</span></div>')
    sev_row = ""
    if rep.get("severity") is not None:
        sev_row = (f"<tr><td>Severity (estimate)</td><td><b>{rep['severity']:.1f}%</b>"
                   f" of leaf area — {rep.get('severity_level', '')}</td></tr>")
    status_color = "#16a34a" if rep.get("healthy") else "#dc2626"
    status_word = "HEALTHY" if rep.get("healthy") else "DISEASE DETECTED"
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>FasalShield AI — Diagnosis Report {rep['report_id']}</title>
<style>
 body{{font-family:Arial,Helvetica,sans-serif;background:#f1f5f2;margin:0;padding:24px;color:#10281a}}
 .receipt{{max-width:640px;margin:0 auto;background:#fff;border:2px solid #14532d;border-radius:14px;overflow:hidden}}
 .head{{background:linear-gradient(120deg,#052e16,#14532d,#16a34a);color:#fff;padding:20px 24px}}
 .head h1{{margin:0;font-size:26px}} .head p{{margin:4px 0 0;opacity:.9;font-size:13px}}
 .meta{{display:flex;justify-content:space-between;padding:12px 24px;background:#f0fdf4;border-bottom:1px dashed #86c79b;font-size:13px}}
 table{{width:100%;border-collapse:collapse;font-size:14px}}
 td{{padding:9px 24px;border-bottom:1px solid #e7f4ea;vertical-align:top}} td:first-child{{width:170px;color:#5f7163;font-weight:600}}
 .status{{display:inline-block;padding:4px 12px;border-radius:999px;color:#fff;background:{status_color};font-weight:700;font-size:12px}}
 .qrrow{{display:flex;gap:18px;align-items:center;padding:16px 24px}}
 .seal{{margin-left:auto;border:3px double #14532d;color:#14532d;border-radius:10px;padding:10px 14px;
        transform:rotate(-6deg);font-weight:800;text-align:center;font-size:12px;letter-spacing:1px}}
 .foot{{padding:14px 24px;font-size:12px;color:#5f7163;border-top:1px dashed #86c79b}}
 button{{background:#16a34a;color:#fff;border:none;border-radius:999px;padding:10px 22px;font-weight:700;cursor:pointer}}
 @media print{{button{{display:none}} body{{background:#fff;padding:0}}}}
</style></head><body>
<div class="receipt">
  <div class="head">{logo_img}<h1>🌿 FasalShield AI</h1>
  <p>Leaf Diagnosis Report • BBS-UTECH Khairpur Mirs, Sindh</p></div>
  <div class="meta"><span><b>Report ID:</b> {rep['report_id']}</span><span><b>Date:</b> {rep['when']}</span></div>
  <table>
    <tr><td>Status</td><td><span class="status">{status_word}</span></td></tr>
    <tr><td>Result</td><td><b>{rep['label']}</b></td></tr>
    <tr><td>Confidence</td><td><b>{rep['confidence']:.1f}%</b></td></tr>
    {sev_row}
    <tr><td>Treatment</td><td>{rep['treatment']}</td></tr>
    <tr><td>Prevention</td><td>{rep['prevention']}</td></tr>
    <tr><td>Expert Help</td><td>Agriculture Extension Sindh Helpline: <b>0311-1646111</b><br>
    Deputy Director Agriculture Extension, Station Road, Khairpur Mirs</td></tr>
  </table>
  <div class="qrrow">
    <img src="data:image/png;base64,{qr_b64}" width="120" height="120" alt="QR">
    <div style="font-size:12.5px;color:#5f7163">Is QR ko scan karein —<br>report ki details khul jayengi.</div>
    <div class="seal">FASALSHIELD AI<br>DIAGNOSIS REPORT<br>🌿</div>
  </div>
  <div class="foot">Ye AI-based advice hai — final tasdeeq apne Agriculture Extension officer se karein.
  Disease data: PlantVillage research dataset (public research), humne ye data apne project me use kiya hai.<br>
  Designed &amp; Built by <b>Asad Ali</b> &amp; <b>Ali Shan</b> — BS AI, BBS-UTECH Khairpur Mirs<br>{made_row}<br>
  <button onclick="window.print()">🖨️ Print / Save as PDF</button></div>
</div>
</body></html>"""
