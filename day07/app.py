from __future__ import annotations
import argparse, logging, sys
from typing import List

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="day07", description="Human-in-the-Loop（承認フロー・中断・再開）")
    p.add_argument("--query", required=True)
    p.add_argument("--thread-id", default="default", help="チェックポイントを識別するID")
    p.add_argument("--auto-approve", action="store_true", help="テスト用：承認プロンプトを自動で y にする")
    p.add_argument("--region", default=None)
    p.add_argument("--model-id", default=None)
    return p

def _validate_args(args: argparse.Namespace) -> None:
    if not args.query.strip():
        raise ValueError("--query must not be empty")

def run_with_hitl(
    query: str,
    thread_id: str = "default",
    auto_approve: bool = False,
    region: str | None = None,
    model_id: str | None = None,
) -> str:
    """ツール実行前に人間の承認を求める LangGraph フローを実行する。

    実装ガイド:
    1. LangGraph の interrupt() を使い、ツール実行ノードの直前で一時停止する
    2. 停止時に「このアクションを実行してよいか？[y/n]: 」と標準入力から確認を求める
       auto_approve=True のときは自動で "y" とみなす（テスト・CI 用）
    3. "n" の場合は代替ノードに分岐し「承認されなかったため処理を中止しました」を返す
    4. SqliteSaver で thread_id ごとにチェックポイントを永続化する
       （中断後に同じ thread_id で再実行すると続きから再開できること）

    戻り値:
        エージェントの最終回答、または中止メッセージ
    """
    raise NotImplementedError("day07: run_with_hitl() を実装してください")

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
    logging.info("thread_id=%s auto_approve=%s", args.thread_id, args.auto_approve)
    try:
        out = run_with_hitl(args.query, args.thread_id, args.auto_approve, args.region, args.model_id)
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
