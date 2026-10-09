from __future__ import annotations
import argparse, logging, sys
from typing import List

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="day06.server", description="MCP サーバー（RAG 検索ツールを公開）")
    p.add_argument("--port", type=int, default=8200)
    p.add_argument("--data-dir", default="day05/data")
    p.add_argument("--region", default=None)
    p.add_argument("--model-id", default=None)
    return p

def serve(port: int = 8200, data_dir: str = "day05/data", region: str | None = None, model_id: str | None = None) -> None:
    """Day05 の RAG 検索ロジックを MCP サーバーの Tool として公開する。

    実装ガイド:
    1. mcp ライブラリの FastMCP または Server を使ってサーバーを起動する
    2. Tools として以下を定義する
       - search(query: str, top_k: int = 5) -> str
         : Day05 の hybrid 検索を呼び出してフォーマット済み結果を返す
    3. Resources として以下を定義する
       - documents://list : data_dir 内のファイル一覧（名前・サイズ・更新日時）を JSON で返す
    4. サーバーが起動したら logging.info で URL を出力する

    ※ Ctrl-C で停止するまでブロックする
    """
    raise NotImplementedError("day06: serve() を実装してください")

def main(argv: List[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = build_parser()
    args = parser.parse_args(argv)
    logging.info("Starting MCP server on port %d", args.port)
    try:
        serve(args.port, args.data_dir, args.region, args.model_id)
        return 0
    except NotImplementedError as e:
        logging.error(str(e))
        print(str(e), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        logging.info("Server stopped")
        return 0
    except Exception as e:
        logging.error("unexpected error: %s", e)
        print(str(e), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
