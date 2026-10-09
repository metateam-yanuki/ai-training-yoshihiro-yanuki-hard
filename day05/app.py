from __future__ import annotations
import argparse, logging, sys
from typing import List

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
    """指定された検索戦略で RAG を実行し、根拠付きの回答を返す。

    実装ガイド:
    - strategy="vector" : FAISS または ChromaDB を使ったベクター検索のみ
    - strategy="hybrid" : BM25（rank-bm25）+ ベクター検索を RRF で統合
    - strategy="rerank" : hybrid に加えて cross-encoder でリランキング
    - strategy="expand" : hybrid に加えて HyDE またはマルチクエリでクエリ拡張
    - data_dir 内の .txt / .md ファイルを読み込んでインデックス化する
    - 検索結果がない場合は "検索結果が見つかりませんでした" を返す

    戻り値 (フォーマット):
        Answer: <回答>

        Sources:
        - <ファイル名または URL> (excerpt: "<抜粋>")
        - ...
    """
    raise NotImplementedError("day05: answer_with_advanced_rag() を実装してください")

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
