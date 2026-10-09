from __future__ import annotations
import argparse, logging, sys
from typing import List

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="day01", description="マルチエージェント（Supervisor/Handoff）")
    p.add_argument("--query", required=True, help="調査・要約させたい入力テキスト")
    p.add_argument("--verbose", action="store_true", help="各エージェントの動作ログを表示する")
    p.add_argument("--region", default=None)
    p.add_argument("--model-id", default=None)
    return p

def _validate_args(args: argparse.Namespace) -> None:
    if not args.query.strip():
        raise ValueError("--query must not be empty")

def run_multi_agent(query: str, verbose: bool = False, region: str | None = None, model_id: str | None = None) -> str:
    """Supervisor + Worker × 2 のマルチエージェントを実行する。

    実装ガイド:
    1. LangGraph で以下の構成を組む
       - Supervisor ノード: query を受け取り「research」か「summarize」に振り分ける
       - research Worker ノード: query に対して調査結果を返す
       - summarize Worker ノード: research の出力を要約する
       - Supervisor が両 Worker の出力を統合して最終回答を生成する
    2. state には少なくとも query / research_result / summary / final_answer を持たせる
    3. verbose=True のとき各ノードの入出力を logging.info で出力する
    4. Bedrock の認証情報は boto3 のデフォルト認証チェーン (環境変数 > ~/.aws) に従う
       region / model_id が None のとき .env の値を使う

    戻り値:
        最終回答テキスト（最後に「\\n\\n[Research]」「[Summary]」セクションを付ける）
    """
    raise NotImplementedError("day01: run_multi_agent() を実装してください")

def main(argv: List[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        _validate_args(args)
    except ValueError as e:
        logging.error(str(e))
        print(str(e), file=sys.stderr)
        return 2
    logging.info("query=%r verbose=%s", args.query[:50], args.verbose)
    try:
        out = run_multi_agent(args.query, args.verbose, args.region, args.model_id)
        print(out)
        return 0
    except NotImplementedError as e:
        logging.error(str(e))
        print(str(e), file=sys.stderr)
        return 1
    except Exception as e:
        logging.error("unexpected error: %s", e)
        print(str(e), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
