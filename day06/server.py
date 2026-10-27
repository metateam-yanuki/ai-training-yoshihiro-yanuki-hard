from __future__ import annotations
import argparse, logging, sys
from typing import List
from pathlib import Path
import json

from mcp.server.fastmcp import FastMCP

from day05.app import answer_with_advanced_rag

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="day06.server", description="MCP サーバー（RAG 検索ツールを公開）")
    p.add_argument("--port", type=int, default=8200)
    p.add_argument("--data-dir", default="day05/data")
    p.add_argument("--region", default=None)
    p.add_argument("--model-id", default=None)
    return p

def serve(
    port: int = 8200,
    data_dir: str = "day05/data",
    region: str | None = None,
    model_id: str | None = None,
) -> None:
    mcp = FastMCP("day06-rag-server")

    @mcp.tool()
    def search(query: str, top_k: int = 5) -> str:
        return answer_with_advanced_rag(
            query=query,
            data_dir=data_dir,
            top_k=top_k,
            region=region,
            model_id=model_id,
        )

    @mcp.resource("documents://list")
    def documents_list() -> str:
        docs = []

        for p in Path(data_dir).glob("*"):
            if p.is_file():
                stat = p.stat()

                docs.append(
                    {
                        "name": p.name,
                        "size": stat.st_size,
                        "updated_at": stat.st_mtime,
                    }
                )

        return json.dumps(docs, ensure_ascii=False, indent=2)

    logging.info(
        "MCP server running at http://127.0.0.1:%d",
        port,
    )

    mcp.run(
        transport="streamable-http"
    )


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
