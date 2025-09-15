import argparse
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib, os, yaml
from app.logger import setup_logger

cfg_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
with open(cfg_path) as f:
    cfg = yaml.safe_load(f)

logger = setup_logger(cfg.get('logging', {}))
model_cfg = cfg.get('model', {})

def train_and_detect(features_csv, contamination=0.02, save_model=None, out_results='data/results.csv'):
    df = pd.read_csv(features_csv)
    X = df.select_dtypes(include=['int64','float64']).fillna(0)
    model = IsolationForest(n_estimators=100, contamination=contamination, random_state=42)
    model.fit(X)
    scores = model.decision_function(X)
    preds = model.predict(X)
    df['anomaly_score'] = scores
    df['is_anomaly'] = (preds == -1)
    df.to_csv(out_results, index=False)
    if save_model:
        os.makedirs(os.path.dirname(save_model), exist_ok=True)
        joblib.dump(model, save_model)
    logger.info(f"Model trained and results saved to {out_results}")
    return df, model

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--in-features', default='data/features.csv')
    parser.add_argument('--contamination', type=float, default=model_cfg.get('contamination', 0.02))
    parser.add_argument('--save-model', default=model_cfg.get('model_path'))
    parser.add_argument('--out-results', default=model_cfg.get('results_csv', 'data/results.csv'))
    args = parser.parse_args()
    train_and_detect(args.in_features, contamination=args.contamination, save_model=args.save_model, out_results=args.out_results)
