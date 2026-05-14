import os
import pickle

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score, train_test_split

DATASET_PATH = os.path.join(os.path.dirname(__file__), "dataset", "phishing.csv")
MODEL_PATH   = os.path.join(os.path.dirname(__file__), "model.pkl")

# ── STEP 1: LOAD DATASET ─────────────────────────────────────────

def load_data():
    print("\n[1/4] Loading dataset...")

    if not os.path.exists(DATASET_PATH):
        print("      Dataset not found. Downloading from UCI...")
        try:
            from ucimlrepo import fetch_ucirepo
            ds = fetch_ucirepo(id=327)
            X_raw = ds.data.features
            y_raw = ds.data.targets.iloc[:, 0]
            df = pd.concat([X_raw, y_raw.rename("Result")], axis=1)
            os.makedirs(os.path.dirname(DATASET_PATH), exist_ok=True)
            df.to_csv(DATASET_PATH, index=False)
            print(f"      Saved to {DATASET_PATH}")
        except Exception as e:
            raise FileNotFoundError(
                f"Could not download dataset automatically.\n"
                f"Please download manually from:\n"
                f"https://archive.ics.uci.edu/ml/datasets/phishing+websites\n"
                f"and place the CSV at: {DATASET_PATH}\n"
                f"Error: {e}"
            )

    df = pd.read_csv(DATASET_PATH)
    print(f"      Loaded {len(df)} rows, {len(df.columns)} columns")

    # Handle both column name styles
    if "Result" not in df.columns and "result" in df.columns:
        df.rename(columns={"result": "Result"}, inplace=True)

    # Convert labels: -1 (phishing) → 0, 1 (legitimate) → 1
    feature_cols = [c for c in df.columns if c != "Result"]
    X = df[feature_cols].values
    y = (df["Result"].values == 1).astype(int)

    phishing   = int((y == 0).sum())
    legitimate = int((y == 1).sum())
    print(f"      Phishing: {phishing} | Legitimate: {legitimate}")

    return X, y, feature_cols


# ── STEP 2: TRAIN MODEL ──────────────────────────────────────────

def train_model(X, y, feature_cols):
    print("\n[2/4] Splitting data 80/20...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"      Train: {len(X_train)} samples | Test: {len(X_test)} samples")

    print("\n[3/4] Training Random Forest (100 trees)...")
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    print("\n[4/4] Evaluating model...")
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print(f"\n{'='*45}")
    print(f"  Test Accuracy  : {acc * 100:.2f}%")
    print(f"{'='*45}")
    print("\n  Classification Report:")
    print(classification_report(y_test, y_pred,
          target_names=["Phishing", "Legitimate"]))

    print("  Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"  TP={cm[1][1]}  FP={cm[0][1]}  TN={cm[0][0]}  FN={cm[1][0]}\n")

    print("  5-Fold Cross Validation...")
    cv = cross_val_score(model, X, y, cv=5, scoring="accuracy")
    print(f"  CV Accuracy: {cv.mean()*100:.2f}% +/- {cv.std()*100:.2f}%")

    print("\n  Top 10 Most Important Features:")
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    for i in range(10):
        print(f"  {i+1:>2}. {feature_cols[indices[i]]:<35} {importances[indices[i]]:.4f}")

    return model


# ── STEP 3: SAVE MODEL ───────────────────────────────────────────

def save_model(model):
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print(f"\n  Model saved to: {MODEL_PATH}")


# ── MAIN ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 45)
    print("  PhishGuard — Model Training")
    print("=" * 45)

    X, y, feature_cols = load_data()
    model = train_model(X, y, feature_cols)
    save_model(model)

    print("\n  All done! model.pkl is ready.")
    print("=" * 45)