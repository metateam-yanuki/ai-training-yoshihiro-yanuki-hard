from __future__ import annotations
import argparse, logging, sys
from typing import List
from langchain_aws import ChatBedrock
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import asyncio


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

def run_with_mcp(
    query: str,
    server_url: str,
    region: str | None = None,
    model_id: str | None = None,
) -> str:

    async def _run():
        client = MultiServerMCPClient(
            {
                "rag-server": {
                    "url": server_url,
                    "transport": "streamable_http",
                }
            }
        )

        tools = await client.get_tools()

        llm = ChatBedrock(
            region_name=region,
            model_id=model_id,
        )

        agent = create_react_agent(
            llm,
            tools,
        )

        result = await agent.ainvoke(
            {
                "messages": [
                    ("user", query),
                ]
            }
        )

        return result["messages"][-1].content

    return asyncio.run(_run())

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
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
