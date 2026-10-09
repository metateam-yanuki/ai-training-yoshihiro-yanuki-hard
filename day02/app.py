from __future__ import annotations
import argparse, logging, sys
from typing import List

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="day02", description="LangGraph サブグラフ・ストリーミング")
    p.add_argument("--query", required=True)
    p.add_argument("--stream", action="store_true", help="ストリーミングモードで実行する")
    p.add_argument("--region", default=None)
    p.add_argument("--model-id", default=None)
    return p

def _validate_args(args: argparse.Namespace) -> None:
    if not args.query.strip():
        raise ValueError("--query must not be empty")

def run_graph(query: str, stream: bool = False, region: str | None = None, model_id: str | None = None) -> str:
    """Day01 のフローをサブグラフに分割し、ストリーミング対応したグラフを実行する。

    実装ガイド:
    1. Day01 の research / summarize を独立したサブグラフとして定義する
       - 各サブグラフは独自の State を持ち、親グラフの State とは分離する
       - サブグラフを add_node でネストする
    2. stream=True のとき graph.stream() を使い、各 node/chunk を
       logging.info で表示しながら最終 final_answer を収集して返す
    3. stream=False のとき graph.invoke() を使う

    戻り値:
        最終回答テキスト
    """
    raise NotImplementedError("day02: run_graph() を実装してください")

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
    logging.info("query=%r stream=%s", args.query[:50], args.stream)
    try:
        out = run_graph(args.query, args.stream, args.region, args.model_id)
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
