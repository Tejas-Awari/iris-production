import hydra
from omegaconf import DictConfig
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import os

@hydra.main(version_base=None, config_path="../configs", config_name="config")
def train(cfg: DictConfig):
    print(f"🚀 Starting training with model: {cfg.model.name}")

    # 1. Load Data
    print(f"   Loading data from {cfg.data.raw_path}...")
    df = pd.read_csv(cfg.data.raw_path)
    X = df.drop("target", axis=1)
    y = df["target"]

    # 2. Split Data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=cfg.data.test_size, 
        random_state=cfg.data.random_state
    )

    # 3. Initialize Model
    if cfg.model.name == "LogisticRegression":
        model = LogisticRegression(
            C=cfg.model.params.C,
            solver=cfg.model.params.solver,
            max_iter=cfg.model.params.max_iter
        )
    else:
        raise ValueError(f"Model {cfg.model.name} not supported!")

    # 4. Train
    print("   Training...")
    model.fit(X_train, y_train)

    # 5. Evaluate
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"✅ Training Complete. Accuracy: {acc:.4f}")

    # 6. Save Model
    os.makedirs(os.path.dirname(cfg.export.path), exist_ok=True)
    joblib.dump(model, cfg.export.path)
    print(f"💾 Model saved to {cfg.export.path}")

if __name__ == "__main__":
    train()