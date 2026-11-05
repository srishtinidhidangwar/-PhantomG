"""Train the PhantomG Random Forest and save it as models/phantomg_rf.joblib.

Usage:
    python train.py --data data/Phishing_Email.csv
Expected CSV columns: "Email Text", "Email Type" ("Phishing Email" / "Safe Email").
"""
import argparse
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from features import FEATURE_NAMES, feature_vector

MODEL_PATH = os.path.join("models", "phantomg_rf.joblib")


def load_dataset(path: str):
    df = pd.read_csv(path).dropna(subset=["Email Text", "Email Type"])
    df["label"] = (df["Email Type"].str.strip().str.lower() == "phishing email").astype(int)
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=os.path.join("data", "sample_emails.csv"))
    ap.add_argument("--test-size", type=float, default=0.2)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    df = load_dataset(args.data)
    print(f"Loaded {len(df)} emails  |  phishing: {df['label'].sum()}  safe: {(1 - df['label']).sum()}")

    tqdm.pandas(desc="hand-crafted features")
    X = np.array([feature_vector(t) for t in tqdm(df["Email Text"], desc="hand-crafted features")])
    y = df["label"].values

    stratify = y if min(np.bincount(y)) >= 2 else None
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=args.test_size, random_state=args.seed, stratify=stratify)

    model = RandomForestClassifier(n_estimators=300, random_state=args.seed, n_jobs=-1,
                                   class_weight="balanced")
    model.fit(X_tr, y_tr)

    pred = model.predict(X_te)
    print("\nConfusion matrix:\n", confusion_matrix(y_te, pred))
    print("\n", classification_report(y_te, pred, target_names=["Safe", "Phishing"], zero_division=0))

    print("Feature importances:")
    for name, imp in sorted(zip(FEATURE_NAMES, model.feature_importances_), key=lambda x: -x[1]):
        print(f"  {name:<20} {imp:.3f}")

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()
