from __future__ import annotations
import argparse, logging, sys
from typing import List, TypedDict
from langgraph.graph import END, StateGraph

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="day02", description="LangGraph サブグラフ・ストリーミング")
    p.add_argument("--query", required=True)
    p.add_argument("--stream", action="store_true", help="ストリーミングモードで実行する")
    p.add_argument("--region", default=None)
    p.add_argument("--model-id", default=None)
    return p

def _validate_args(args: argparse.Namespace) -> None:
    if not args.query.strip():
        raise ValueError("--query must not be empty")

def run_graph(query: str, stream: bool = False, region: str | None = None, model_id: str | None = None) -> str:
    class ResearchState(TypedDict):
        research_input: str
        research_output: str

    class SummarizeState(TypedDict):
        text_to_summarize: str
        summary: str

    class ParentState(TypedDict):
        query: str
        research_result: str
        summary: str

    # --------------------
    # Research Subgraph
    # --------------------
    def research_node(state: ResearchState) -> ResearchState:
        state["research_output"] = (
            f"{state['research_input']} に関する調査結果です。"
        )
        return state

    research_graph = StateGraph(ResearchState)
    research_graph.add_node("research", research_node)
    research_graph.set_entry_point("research")
    research_graph.add_edge("research", END)

    research_app = research_graph.compile()

    # --------------------
    # Summarize Subgraph
    # --------------------
    def summarize_node(state: SummarizeState) -> SummarizeState:
        state["summary"] = (
            f"{state['text_to_summarize']} の要約結果です。"
        )
        return state

    summarize_graph = StateGraph(SummarizeState)
    summarize_graph.add_node("summarize", summarize_node)
    summarize_graph.set_entry_point("summarize")
    summarize_graph.add_edge("summarize", END)

    summarize_app = summarize_graph.compile()

    # --------------------
    # Parent Graph
    # --------------------
    def research_subgraph_node(state: ParentState) -> ParentState:
        logging.info("research_subgraph: starting...")
        result = research_app.invoke(
            {
                "research_input": state["query"],
                "research_output": "",
            }
        )
        state["research_result"] = result["research_output"]
        logging.info("research_subgraph: done.")
        return state

    def summarize_subgraph_node(state: ParentState) -> ParentState:
        logging.info("summarize_subgraph: starting...")
        result = summarize_app.invoke(
            {
                "text_to_summarize": state["research_result"],
                "summary": "",
            }
        )
        state["summary"] = result["summary"]
        logging.info("summarize_subgraph: done.")
        return state

    graph = StateGraph(ParentState)

    graph.add_node("research_subgraph", research_subgraph_node)
    graph.add_node("summarize_subgraph", summarize_subgraph_node)

    graph.set_entry_point("research_subgraph")

    graph.add_edge("research_subgraph", "summarize_subgraph")
    graph.add_edge("summarize_subgraph", END)

    app = graph.compile()

    init_state = {
        "query": query,
        "research_result": "",
        "summary": "",
    }

    if stream:
        final_state = init_state

        for chunk in app.stream(init_state):
            logging.info("stream chunk=%s", chunk)
            final_state.update(next(iter(chunk.values())))

        return (
            f"{final_state['summary']}\n\n"
            f"[Research]\n{final_state['research_result']}"
        )

    result = app.invoke(init_state)

    return (
        f"{result['summary']}\n\n"
        f"[Research]\n{result['research_result']}"
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
    logging.info("query=%r stream=%s", args.query[:50], args.stream)
    try:
        out = run_graph(args.query, args.stream, args.region, args.model_id)
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
