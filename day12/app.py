from __future__ import annotations
import argparse, json, logging, sys
from typing import Any, Dict, List

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="day12", description="失敗分析と改善サイクル")
    p.add_argument("--result", default="day11/results/eval_result.json", help="Day11 の評価結果 JSON")
    p.add_argument("--output", default="day12/results/improved_result.json", help="改善後の評価結果")
    p.add_argument("--apply-fix", action="store_true", help="改善を適用して再評価する")
    p.add_argument("--region", default=None)
    p.add_argument("--model-id", default=None)
    return p

def run_improvement_cycle(
    result_path: str = "day11/results/eval_result.json",
    output_path: str = "day12/results/improved_result.json",
    apply_fix: bool = False,
    region: str | None = None,
    model_id: str | None = None,
) -> Dict[str, Any]:
    """Day11 の評価結果を分析し、最も多い失敗種別に改善を適用して再評価する。

    実装ガイド:
    1. result_path の評価結果を読み込み、失敗ケースを抽出する
    2. 各失敗ケースを failure_taxonomy.md の4分類に振り分けてカウントする
    3. apply_fix=False のとき:
       - 失敗分類の集計結果と改善案を JSON で返す（再評価はしない）
    4. apply_fix=True のとき:
       - 最も件数の多い失敗種別に対して改善を1つ実施する
         例: 検索ミス → strategy を "rerank" に変更
             推論ミス → プロンプトに「必ず根拠を示してください」を追加
       - Day11 と同じテストスイートで再評価し、スコアを比較する
       - 結果を output_path に保存し、改善前後の比較を返す
    5. 回帰テスト: 改善後に全ケースをチェックし、前回 passed だったケースが
       今回 failed になっていたら警告ログを出す

    戻り値:
        {"failure_analysis": {...}, "before": {...}, "after": {...}, "regressions": [...]}
    """
    raise NotImplementedError("day12: run_improvement_cycle() を実装してください")

def main(argv: List[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = build_parser()
    args = parser.parse_args(argv)
    logging.info("result=%s apply_fix=%s", args.result, args.apply_fix)
    try:
        result = run_improvement_cycle(args.result, args.output, args.apply_fix, args.region, args.model_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except NotImplementedError as e:
        logging.error(str(e))
        print(str(e), file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        logging.error(str(e))
        print(str(e), file=sys.stderr)
        return 2
    except Exception as e:
        logging.error("unexpected error: %s", e)
        print(str(e), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
