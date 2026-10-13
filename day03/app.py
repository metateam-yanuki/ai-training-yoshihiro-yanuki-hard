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
    import asyncio

    from a2a.client import (
        ClientConfig,
        create_client,
    )
    from a2a.helpers import new_text_message
    from a2a.types import (
        GetExtendedAgentCardRequest,
        Role,
        SendMessageRequest,
    )

    async def _run():

        config = ClientConfig()
        config.supported_protocol_bindings.append(
            "JSONRPC"
        )

        client = await create_client(
            server_url,
            client_config=config,
        )

        card_req = GetExtendedAgentCardRequest()

        card = await client.get_extended_agent_card(
            card_req
        )

        print(card)

        msg = new_text_message(
            task,
            role=Role.ROLE_USER,
        )

        req = SendMessageRequest(
            message=msg,
        )

        async for resp in client.send_message(req):
            return str(resp)

        return "No response"

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
