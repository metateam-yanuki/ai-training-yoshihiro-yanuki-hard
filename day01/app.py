from __future__ import annotations
import argparse, logging, sys
from typing import List
from typing import Dict, TypedDict
from langgraph.graph import END, StateGraph

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="day01", description="マルチエージェント（Supervisor/Handoff）")
    p.add_argument("--query", required=True, help="調査・要約させたい入力テキスト")
    p.add_argument("--verbose", action="store_true", help="各エージェントの動作ログを表示する")
    p.add_argument("--region", default=None)
    p.add_argument("--model-id", default=None)
    return p

def _validate_args(args: argparse.Namespace) -> None:
    if not args.query.strip():
        raise ValueError("--query must not be empty")

def run_multi_agent(query: str, verbose: bool = False, region: str | None = None, model_id: str | None = None) -> str:
    class AgentState(TypedDict):
        query: str
        research_result: str
        summary: str
        final_answer: str

    def supervisor_node(state: AgentState) -> AgentState:
        if verbose:
            logging.info("Supervisor: query=%s", state["query"])
        return state

    def research_node(state: AgentState) -> AgentState:
        state["research_result"] = (
            f"{state['query']} に関する調査結果です。"
        )
        if verbose:
            logging.info("Research: %s", state["research_result"])
        return state

    def summarize_node(state: AgentState) -> AgentState:
        state["summary"] = (
            f"{state['query']} の要約結果です。"
        )
        if verbose:
            logging.info("Summary: %s", state["summary"])
        return state

    def final_node(state: AgentState) -> AgentState:
        state["final_answer"] = (
            f"{state['query']} の回答です。"
        )
        return state

    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("research", research_node)
    graph.add_node("summarize", summarize_node)
    graph.add_node("final", final_node)

    graph.set_entry_point("supervisor")

    graph.add_edge("supervisor", "research")
    graph.add_edge("research", "summarize")
    graph.add_edge("summarize", "final")
    graph.add_edge("final", END)

    app = graph.compile()

    result = app.invoke(
        {
            "query": query,
            "research_result": "",
            "summary": "",
            "final_answer": "",
        }
    )

    return (
        f"{result['final_answer']}\n\n"
        f"[Research]\n{result['research_result']}\n\n"
        f"[Summary]\n{result['summary']}"
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
    logging.info("query=%r verbose=%s", args.query[:50], args.verbose)
    try:
        out = run_multi_agent(args.query, args.verbose, args.region, args.model_id)
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
