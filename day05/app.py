from __future__ import annotations

import argparse, logging, sys
from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from langchain_aws import (
    BedrockEmbeddings,
    ChatBedrock,
)
from rank_bm25 import BM25Okapi


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="day05", description="高度 RAG（ハイブリッド検索・リランキング・クエリ拡張）")
    p.add_argument("--question", required=True, help="質問テキスト")
    p.add_argument("--strategy", choices=["vector", "hybrid", "rerank", "expand"], default="hybrid",
                   help="検索戦略: vector=ベクターのみ, hybrid=BM25+ベクター, rerank=リランキング追加, expand=クエリ拡張追加")
    p.add_argument("--data-dir", default="day05/data", help="ドキュメントを置くディレクトリ")
    p.add_argument("--top-k", type=int, default=5, help="検索上位件数")
    p.add_argument("--region", default=None)
    p.add_argument("--model-id", default=None)
    return p

def _validate_args(args: argparse.Namespace) -> None:
    if not args.question.strip():
        raise ValueError("--question must not be empty")
    if args.top_k < 1 or args.top_k > 20:
        raise ValueError("--top-k must be between 1 and 20")

def answer_with_advanced_rag(
    question: str,
    strategy: str = "hybrid",
    data_dir: str = "day05/data",
    top_k: int = 5,
    region: str | None = None,
    model_id: str | None = None,
) -> str:

    docs = []

    for file in Path(data_dir).glob("*"):

        if file.suffix not in {".txt", ".md"}:
            continue

        text = file.read_text(
            encoding="utf-8"
        )

        docs.append(
            Document(
                page_content=text,
                metadata={
                    "source": file.name
                }
            )
        )

    if not docs:
        return "検索結果が見つかりませんでした"

    embeddings = BedrockEmbeddings(
        region_name=region
        or "ap-northeast-1"
    )

    vectorstore = FAISS.from_documents(
        docs,
        embeddings,
    )

    tokenized_docs = [
        doc.page_content.split()
        for doc in docs
    ]

    bm25 = BM25Okapi(
        tokenized_docs
    )

    llm = ChatBedrock(
        model_id=model_id
        or "jp.anthropic.claude-sonnet-4-5-20250929-v1:0",
        region_name=region
        or "ap-northeast-1",
    )

    if strategy == "vector":

        results = vectorstore.similarity_search(
            question,
            k=top_k,
        )

    elif strategy == "hybrid":

        vector_results = vectorstore.similarity_search(
            question,
            k=top_k,
        )

        bm25_scores = bm25.get_scores(
            question.split()
        )

        bm25_pairs = list(
            zip(docs, bm25_scores)
        )

        bm25_pairs.sort(
            key=lambda x: x[1],
            reverse=True,
        )

        bm25_results = [
            doc
            for doc, _
            in bm25_pairs[:top_k]
        ]

        seen = set()

        results = []

        for doc in (
            vector_results
            + bm25_results
        ):

            source = doc.metadata["source"]

            if source not in seen:

                seen.add(source)

                results.append(doc)

    elif strategy == "expand":

        expanded = llm.invoke(
            f"""
次の質問を検索しやすい別表現で3つに言い換えてください。

質問:
{question}
"""
        )

        print("EXPANDED QUERY")
        print(expanded.content)

        expanded_query = (
            question
            + "\n"
            + expanded.content
        )

        results = vectorstore.similarity_search(
            expanded_query,
            k=top_k,
        )

    else:

        results = vectorstore.similarity_search(
            question,
            k=top_k,
        )

    context = "\n\n".join(
        doc.page_content
        for doc in results
    )

    answer = llm.invoke(
        f"""
以下の資料だけを根拠として回答してください。

資料:
{context}

質問:
{question}
"""
    )

    lines = []

    lines.append("Answer:")
    lines.append(answer.content)
    lines.append("")
    lines.append("Sources:")

    used_sources = set()

    for doc in results:

        source = doc.metadata.get(
            "source"
        )

        if source not in used_sources:

            lines.append(
                f"- {source}"
            )

            used_sources.add(source)

    return "\n".join(lines)

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
    logging.info("question=%r strategy=%s top_k=%d", args.question[:50], args.strategy, args.top_k)
    try:
        out = answer_with_advanced_rag(
            args.question, args.strategy, args.data_dir, args.top_k, args.region, args.model_id
        )
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
