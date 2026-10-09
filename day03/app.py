from __future__ import annotations
import argparse, logging, sys
from typing import List

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="day03", description="A2A クライアント")
    p.add_argument("--task", required=True, help="エージェントに送るタスクテキスト")
    p.add_argument("--server-url", default="http://127.0.0.1:8100", help="A2A サーバーの URL")
    return p

def _validate_args(args: argparse.Namespace) -> None:
    if not args.task.strip():
        raise ValueError("--task must not be empty")

def call_agent(server_url: str, task: str) -> str:
    """A2A サーバーにタスクを送信して結果を受け取る。

    実装ガイド:
    1. a2a-sdk の A2AClient を使ってサーバーに接続する
    2. AgentCard を取得して capabilities を確認する
    3. Task を送信して TaskState.completed になるまで待つ
    4. 結果テキストを返す

    戻り値:
        エージェントからの応答テキスト
    """
    raise NotImplementedError("day03: call_agent() を実装してください")

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
    logging.info("server_url=%s task=%r", args.server_url, args.task[:50])
    try:
        out = call_agent(args.server_url, args.task)
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
