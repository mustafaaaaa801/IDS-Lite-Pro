import os
import time
import subprocess
import sys

# تأكد أن بايثون يرى الموديولات
sys.path.append(os.path.abspath('.'))

# المسارات
PACKETS_CSV = 'data/packets.csv'
FEATURES_CSV = 'data/features.csv'
RESULTS_CSV = 'data/results.csv'
MODEL_PATH = 'model/joblib/model.joblib'

# --- تشغيل Sniffer في نافذة منفصلة ---
def run_sniffer():
    print("[1/4] تشغيل Sniffer مباشر (live capture)...")
    cmd = f'python -m app.sniffer --live --count 0 --out-csv {PACKETS_CSV}'
    # start cmd منفصل مع keep window open
    subprocess.Popen(['cmd', '/k', cmd])

# --- تحديث الميزات بشكل دوري ---
def update_features():
    print("[2/4] مراقبة CSV وتحديث الميزات بشكل دوري...")
    while True:
        if os.path.exists(PACKETS_CSV):
            subprocess.run(['python', '-m', 'app.features', 
                            '--in-csv', PACKETS_CSV,
                            '--out-features', FEATURES_CSV])
        time.sleep(5)  # تحديث كل 5 ثواني

# --- تشغيل نموذج التحليل ---
def run_model():
    if os.path.exists(FEATURES_CSV):
        print("[3/4] تشغيل نموذج التحليل...")
        subprocess.run(['python', '-m', 'app.model',
                        '--in-features', FEATURES_CSV,
                        '--out-results', RESULTS_CSV,
                        '--save-model', MODEL_PATH])

# --- تشغيل Dashboard ---
def run_dashboard():
    print("[4/4] تشغيل Dashboard...")
    subprocess.run(['python', '-m', 'app.webapp', '--csv', RESULTS_CSV])

# --- التنفيذ الرئيسي ---
if __name__ == '__main__':
    run_sniffer()
    # ننتظر 5 ثواني قبل أول معالجة
    time.sleep(5)
    update_features()
    run_model()
    run_dashboard()
