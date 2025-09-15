# IDS-Lite-Pro
"IDS-Lite-Pro is a lightweight network intrusion detection system with live packet capture, multi-protocol support, signature-based alerts, and a real-time dashboard for monitoring network traffic efficiently
# IDS-Lite-Pro

برنامج IDS خفيف الوزن لالتقاط وتحليل باكيتات الشبكة وعرضها مباشرة على Dashboard.

---

## مميزات المشروع
- التقاط باكيتات الشبكة **Live**.
- دعم **TCP/UDP/ICMP وغيرها من البروتوكولات**.
- كتابة البيانات إلى CSV.
- عرض البيانات على **Dashboard تفاعلي باستخدام Flask + SocketIO**.
- قواعد توقيعية بسيطة للتنبيه عند وجود سلوك مريب.
- يمكن تجربة ملفات pcap بدل Live sniffing.

---

## المتطلبات
- Python 3.10+
- المكتبات موجودة في `requirements.txt`:
  - Flask
  - Flask-SocketIO
  - pandas
  - scapy
  - tqdm
  - pyyaml

---

## طريقة التشغيل

1. إنشاء وتفعيل البيئة الافتراضية:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / Mac
source .venv/bin/activate
