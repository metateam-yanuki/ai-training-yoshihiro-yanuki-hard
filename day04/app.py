from __future__ import annotations
import argparse, logging, sys
from typing import List
from langchain_aws import ChatBedrock
from langgraph.graph import (
    MessagesState,
    StateGraph,
)
from langgraph.checkpoint.memory import (
    MemorySaver,
)
from langgraph.checkpoint.sqlite import (
    SqliteSaver,
)
from langchain_core.messages import HumanMessage

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="day04", description="メモリ設計（短期・長期・エピソード記憶）")
    p.add_argument("--message", required=True, help="ユーザーメッセージ")
    p.add_argument("--thread-id", default="default", help="会話スレッドID（同じIDで履歴を引き継ぐ）")
    p.add_argument("--memory-type", choices=["short", "long", "episode"], default="short",
                   help="short=スレッド内, long=SQLite永続, episode=圧縮サマリ")
    p.add_argument("--region", default=None)
    p.add_argument("--model-id", default=None)
    return p

def _validate_args(args: argparse.Namespace) -> None:
    if not args.message.strip():
        raise ValueError("--message must not be empty")

def call_model(state: MessagesState):

    llm = ChatBedrock(
        model_id="jp.anthropic.claude-sonnet-4-5-20250929-v1:0",
        region_name="ap-northeast-1",
    )

    response = llm.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }

def run_chat(
    message: str,
    thread_id: str = "default",
    memory_type: str = "short",
    region: str | None = None,
    model_id: str | None = None,
) -> str:

    builder = StateGraph(MessagesState)

    builder.add_node(
        "model",
        call_model,
    )

    builder.set_entry_point("model")
    builder.set_finish_point("model")

    if memory_type == "short":

        memory = MemorySaver()

        graph = builder.compile(
            checkpointer=memory
        )

        result = graph.invoke(
            {
                "messages": [
                    HumanMessage(content=message)
                ]
            },
            config={
                "configurable": {
                    "thread_id": thread_id
                }
            },
        )

        return result["messages"][-1].content

    elif memory_type in ("long", "episode"):

        with SqliteSaver.from_conn_string(
            "memory.db"
        ) as memory:

            graph = builder.compile(
                checkpointer=memory
            )

            result = graph.invoke(
                {
                    "messages": [
                        HumanMessage(content=message)
                    ]
                },
                config={
                    "configurable": {
                        "thread_id": thread_id
                    }
                },
            )

            state = graph.get_state(
                {
                    "configurable": {
                        "thread_id": thread_id
                    }
                }
            )

            messages = state.values["messages"]

            print(f"memory_type={memory_type}")
            print(f"message count={len(messages)}")

            if memory_type == "episode":

                print("EPISODE MODE")

                if len(messages) > 10:

                    print("EPISODE MEMORY TRIGGER")

                    llm = ChatBedrock(
                        model_id=model_id
                        or "jp.anthropic.claude-sonnet-4-5-20250929-v1:0",
                        region_name=region or "ap-northeast-1",
                    )

                    summary = llm.invoke(
                        f"""
以下の会話履歴を簡潔に要約してください。

{messages}
"""
                    )

                    print("SUMMARY")
                    print(summary.content)

            return result["messages"][-1].content

    else:
        raise ValueError(
            f"unknown memory_type: {memory_type}"
        )

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
    logging.info("thread_id=%s memory_type=%s", args.thread_id, args.memory_type)
    try:
        out = run_chat(args.message, args.thread_id, args.memory_type, args.region, args.model_id)
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
