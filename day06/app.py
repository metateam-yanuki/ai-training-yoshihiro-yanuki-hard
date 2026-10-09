from __future__ import annotations
import argparse, logging, sys
from typing import List

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="day06", description="MCP クライアント経由でエージェントを実行する")
    p.add_argument("--query", required=True, help="エージェントへの質問")
    p.add_argument("--server-url", default="http://127.0.0.1:8200", help="MCP サーバーの URL")
    p.add_argument("--region", default=None)
    p.add_argument("--model-id", default=None)
    return p

def _validate_args(args: argparse.Namespace) -> None:
    if not args.query.strip():
        raise ValueError("--query must not be empty")

def run_with_mcp(query: str, server_url: str, region: str | None = None, model_id: str | None = None) -> str:
    """MCP サーバーが公開するツールを使ってエージェントが回答する。

    実装ガイド:
    1. mcp クライアントで server_url に接続し、利用可能な Tools 一覧を取得する
    2. LangChain の MCP Tool として登録し、Day01 の Supervisor エージェントに渡す
    3. エージェントが必要に応じて MCP サーバーの search ツールを呼び出して回答を生成する
    4. MCP サーバーを差し替えてもエージェント側のコードは変わらない構成にする

    戻り値:
        エージェントの最終回答テキスト（根拠付き）
    """
    raise NotImplementedError("day06: run_with_mcp() を実装してください")

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
    logging.info("server_url=%s query=%r", args.server_url, args.query[:50])
    try:
        out = run_with_mcp(args.query, args.server_url, args.region, args.model_id)
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
