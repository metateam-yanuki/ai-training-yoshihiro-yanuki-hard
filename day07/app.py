from __future__ import annotations
import argparse, logging, sys
from typing import List
from langchain_aws import ChatBedrock

from langgraph.types import interrupt, Command
from langgraph.checkpoint.sqlite import SqliteSaver
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    query: str
    approved: str
    result: str
    region: str | None
    model_id: str | None

def approve_node(state: State) -> State:
    answer = interrupt(
        "このアクションを実行してよいですか？ [y/n]"
    )

    return {
        "approved": answer
    }


def llm_node(state: State) -> State:
    llm = ChatBedrock(
        region_name=state["region"],
        model_id=state["model_id"],
    )

    response = llm.invoke(state["query"])

    return {
        "result": response.content
    }


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

    with SqliteSaver.from_conn_string("hitl.db") as checkpointer:

        builder = StateGraph(State)

        builder.add_node("approve", approve_node)
        builder.add_node("llm", llm_node)

        builder.add_edge(START, "approve")
        builder.add_edge("approve", "llm")
        builder.add_edge("llm", END)

        graph = builder.compile(
            checkpointer=checkpointer
        )

        config = {
            "configurable": {
                "thread_id": thread_id,
            }
        }

        # 初回実行
        result = graph.invoke(
            {
                "query": query,
                "region": region,
                "model_id": model_id,
            },
            config=config,
        )

        # interruptで止まった場合
        if "__interrupt__" in result:

            if auto_approve:
                answer = "y"
            else:
                answer = input("このアクションを実行してよいですか？ [y/n]: ")

            if answer.lower() != "y":
                return "承認されなかったため処理を中止しました"

            # checkpointから再開
            result = graph.invoke(
                Command(resume=answer),
                config=config,
            )

        if isinstance(result, dict) and "result" in result:
            return str(result["result"])

        return str(result)

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
