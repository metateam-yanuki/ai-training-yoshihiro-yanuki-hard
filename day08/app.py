from __future__ import annotations
import argparse, logging, sys
from typing import List

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="day08", description="可観測性・ログ設計（構造化ログ・コールバック）")
    p.add_argument("--query", required=True)
    p.add_argument("--log-file", default="day08/run.log", help="JSON ログの出力先ファイル")
    p.add_argument("--region", default=None)
    p.add_argument("--model-id", default=None)
    return p

def _validate_args(args: argparse.Namespace) -> None:
    if not args.query.strip():
        raise ValueError("--query must not be empty")

def run_with_logging(
    query: str,
    log_file: str = "day08/run.log",
    region: str | None = None,
    model_id: str | None = None,
) -> str:
    """カスタムコールバックで各ノードの実行を記録しながらエージェントを実行する。

    実装ガイド:
    1. BaseCallbackHandler を継承したカスタムコールバックを実装する
       記録する情報（最低限）:
       - timestamp (ISO 8601)
       - event: "node_start" / "node_end" / "tool_start" / "tool_end" / "error"
       - node_name または tool_name
       - input / output（長い場合は先頭 200 文字に切り詰め）
       - duration_ms（node_end / tool_end のみ）
    2. ログを JSON Lines 形式（1行1 JSON）で log_file に追記する
    3. Day01 のマルチエージェントフローにコールバックを組み込んで実行する

    戻り値:
        エージェントの最終回答
    """
    raise NotImplementedError("day08: run_with_logging() を実装してください")

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
    logging.info("query=%r log_file=%s", args.query[:50], args.log_file)
    try:
        out = run_with_logging(args.query, args.log_file, args.region, args.model_id)
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
