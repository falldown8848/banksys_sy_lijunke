"""离线训练 CLI。

用法:
    python scripts/train.py [--data data/train.csv] [--out models/pipeline.joblib]
                            [--min-auc 0.75] [--seed 42]

验证集 AUC 低于门槛时以非零退出码失败,阻断 CI/CD(见 standards/00 §4 质量门槛)。
"""

import argparse
import json
import sys
from pathlib import Path

from banksys.config import DEFAULT_MODEL_PATH, MIN_AUC, RANDOM_STATE, TRAIN_PATH
from banksys.data import load_train
from banksys.model import meets_gate, save_model, train_and_evaluate


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="离线训练认购预测模型")
    parser.add_argument("--data", default=str(TRAIN_PATH), help="训练 CSV 路径")
    parser.add_argument("--out", default=str(DEFAULT_MODEL_PATH), help="模型输出路径")
    parser.add_argument("--min-auc", type=float, default=MIN_AUC, help="验证集 AUC 门槛")
    parser.add_argument("--seed", type=int, default=RANDOM_STATE, help="随机种子")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    df = load_train(args.data)

    pipeline, metrics, _val_x, _val_y = train_and_evaluate(df, seed=args.seed)

    model_path = save_model(pipeline, args.out)
    metrics_path = Path(args.out).with_name("metrics.json")
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print("== 验证集指标 ==")
    for key, value in metrics.items():
        print(f"  {key}: {value:.4f}")
    print(f"模型已保存: {model_path}")
    print(f"指标已保存: {metrics_path}")

    if not meets_gate(metrics, args.min_auc):
        print(
            f"!! 验证集 AUC {metrics['auc']:.4f} 低于门槛 {args.min_auc:.4f},终止。",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
