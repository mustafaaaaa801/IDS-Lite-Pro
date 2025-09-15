# app/features.py

import argparse
import os
import sys
import logging
import pandas as pd

# إضافة المجلد الرئيسي لمسار البحث
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from app.logger import setup_logger

# إعداد اللوجر
logger = setup_logger({'level': 'INFO'})

def extract_features(in_csv, out_csv):
    try:
        # قراءة البيانات
        df = pd.read_csv(in_csv)
        logger.info(f"Loaded {len(df)} packets from {in_csv}")

        # معالجة القيم المفقودة وتعويضها بصفر
        for col in ['size', 'proto', 'sport', 'dport']:
            if col in df.columns:
                df[col] = df[col].fillna(0).astype(int)

        # مثال على ميزات إضافية: حساب نسبة TCP/UDP
        df['is_tcp'] = df['proto'].apply(lambda x: 6 if x == 6 else 0)
        df['is_udp'] = df['proto'].apply(lambda x: 17 if x == 17 else 0)

        # حفظ الميزات
        df.to_csv(out_csv, index=False)
        logger.info(f"Saved features to {out_csv}")

    except Exception as e:
        logger.exception(f"Error extracting features: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract features from packet CSV")
    parser.add_argument('--in-csv', required=True, help='Input CSV file from sniffer')
    parser.add_argument('--out-features', required=True, help='Output features CSV')
    args = parser.parse_args()

    extract_features(args.in_csv, args.out_features)
