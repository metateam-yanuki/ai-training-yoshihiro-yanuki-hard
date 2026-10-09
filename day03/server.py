from __future__ import annotations
import argparse, logging, sys
from typing import List

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="day03.server", description="A2A サーバー（要約エージェント）")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8100)
    p.add_argument("--region", default=None)
    p.add_argument("--model-id", default=None)
    return p

def serve(host: str = "127.0.0.1", port: int = 8100, region: str | None = None, model_id: str | None = None) -> None:
    """Day01 の summarize Worker を A2A サーバーとして公開する。

    実装ガイド:
    1. a2a-sdk の A2AServer を使ってサーバーを起動する
    2. AgentCard に以下を記述する
       - name: "summarize-agent"
       - description: "テキストを要約するエージェント"
       - capabilities: ["summarize"]
    3. Task を受け取ったら Bedrock を使って要約し TaskState.completed で返す
    4. サーバーが起動したら logging.info で URL を出力する

    ※ Ctrl-C で停止するまでブロックする
    """
    raise NotImplementedError("day03: serve() を実装してください")

def main(argv: List[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = build_parser()
    args = parser.parse_args(argv)
    logging.info("Starting A2A server on %s:%s", args.host, args.port)
    try:
        serve(args.host, args.port, args.region, args.model_id)
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
