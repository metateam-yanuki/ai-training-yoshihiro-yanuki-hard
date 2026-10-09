from __future__ import annotations
import argparse, json, logging, sys
from typing import Any, Dict, List

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="day11", description="評価指標の理解と計測")
    p.add_argument("--suite", default="day11/suite.json", help="テスト入力セット（JSON）")
    p.add_argument("--output", default="day11/results/eval_result.json", help="評価結果の出力先")
    p.add_argument("--region", default=None)
    p.add_argument("--model-id", default=None)
    return p

def load_suite(path: str) -> List[Dict[str, Any]]:
    """テスト入力セット（JSON）を読み込む。

    実装ガイド:
    - path のファイルを読み込み、リストを返す
    - ファイルが存在しない場合は FileNotFoundError を raise する
    - JSON のパースに失敗した場合は ValueError を raise する
    """
    raise NotImplementedError("day11: load_suite() を実装してください")

def run_evaluation(
    suite_path: str = "day11/suite.json",
    output_path: str = "day11/results/eval_result.json",
    region: str | None = None,
    model_id: str | None = None,
) -> Dict[str, Any]:
    """テストスイートを実行し、評価結果を JSON ファイルに保存する。

    実装ガイド:
    まず以下のインポートを追加すること:
        from day05.app import answer_with_advanced_rag
        from day01.app import run_multi_agent
    ※ data_dir は "day05/data" を渡す。プロジェクトルートから実行すること。

    1. load_suite() でテストケースを読み込む
    2. type="rag" のケース: answer_with_advanced_rag() を呼び出し、以下を計測する
       - Faithfulness: 回答が検索結果に基づいているかを LLM-as-a-Judge で評価（0.0〜1.0）
       - Answer Relevance: 質問に答えているかを LLM-as-a-Judge で評価（0.0〜1.0）
    3. type="agent" のケース: run_multi_agent() を呼び出し、以下を計測する
       - タスク達成率: expected_tools が実際に呼ばれたかを確認（0 or 1）
       - ステップ数: 何ノードを経由したかを計測
    4. LLM-as-a-Judge のプロンプトは以下の形式で設計すること:
       「以下の質問と回答のペアに対して、[指標名] を 0.0〜1.0 で評価してください。
        数値のみ回答してください。
        質問: {question}
        回答: {answer}」
    5. 結果を output_path に JSON Lines 形式で保存する

    戻り値:
        {"summary": {"total": N, "rag_faithfulness_avg": X.X, "rag_relevance_avg": X.X,
                     "agent_task_success_rate": X.X}, "results": [...]}
    """
    raise NotImplementedError("day11: run_evaluation() を実装してください")

def main(argv: List[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = build_parser()
    args = parser.parse_args(argv)
    logging.info("suite=%s output=%s", args.suite, args.output)
    try:
        result = run_evaluation(args.suite, args.output, args.region, args.model_id)
        print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
        return 0
    except NotImplementedError as e:
        logging.error(str(e))
        print(str(e), file=sys.stderr)
        return 1
    except (FileNotFoundError, ValueError) as e:
        logging.error(str(e))
        print(str(e), file=sys.stderr)
        return 2
    except Exception as e:
        logging.error("unexpected error: %s", e)
        print(str(e), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
