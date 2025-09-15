@echo off
REM ==== تفعيل البيئة الافتراضية ====
call .venv\Scripts\activate

REM ==== تشغيل sniffer لجمع الحزم ====
python app\sniffer.py --live --count 50 --out-csv data\packets.csv

REM ==== تشغيل الواجهة (dashboard) ====
python app\dashboard.py --csv data\results.csv

pause
