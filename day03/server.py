from __future__ import annotations

import argparse
import logging
import sys

from typing import List

from a2a.helpers import new_text_message
from a2a.server.agent_execution import AgentExecutor
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import (
    create_agent_card_routes,
    create_jsonrpc_routes,
)
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCard,
    AgentInterface,
    Role,
    Task,
    TaskState,
)

from fastapi import FastAPI
import uvicorn
import boto3
import json

import boto3
import json


def summarize(text: str) -> str:

    client = boto3.client(
        "bedrock-runtime",
        region_name="ap-northeast-1",
    )

    prompt = f"""
次の文章を簡潔に要約してください。

{text}
"""

    response = client.invoke_model(
        modelId="jp.anthropic.claude-sonnet-4-5-20250929-v1:0",
        body=json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 300,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            }
        ),
    )

    body = response["body"].read()

    result = json.loads(body)

    return result["content"][0]["text"]


class SummarizeExecutor(AgentExecutor):

    async def execute(
        self,
        context,
        event_queue,
    ) -> None:

        user_text = context.message.parts[0].text

        summary = summarize(user_text)

        msg = new_text_message(
            summary,
            role=Role.ROLE_AGENT,
        )

        await event_queue.enqueue_event(msg)




    async def cancel(
        self,
        context,
        event_queue,
    ) -> None:
        pass


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="day03.server", description="A2A サーバー（要約エージェント）")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8100)
    p.add_argument("--region", default=None)
    p.add_argument("--model-id", default=None)
    return p

def serve(
    host: str,
    port: int,
    region: str | None = None,
    model_id: str | None = None,
) -> None:

    card = AgentCard()

    card.name = "summarize-agent"
    card.description = "テキストを要約するエージェント"

    card.version = "1.0.0"

    card.default_input_modes.append("text/plain")
    card.default_output_modes.append("text/plain")

    card.capabilities.streaming = True

    interface = AgentInterface()
    interface.url = f"http://{host}:{port}/"
    interface.protocol_version = "1.0"
    interface.protocol_binding = "JSONRPC"

    card.supported_interfaces.append(interface)


    executor = SummarizeExecutor()

    task_store = InMemoryTaskStore()

    handler = DefaultRequestHandler(
        agent_executor=executor,
        task_store=task_store,
        agent_card=card,
    )

    app = FastAPI()

    app.router.routes.extend(
        create_agent_card_routes(card)
    )

    app.router.routes.extend(
        create_jsonrpc_routes(
            request_handler=handler,
            rpc_url="/",
        )
    )

    print(f"A2A server listening on http://{host}:{port}")

    uvicorn.run(
        app,
        host=host,
        port=port,
    )

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
