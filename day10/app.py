from __future__ import annotations
import argparse, logging, sys
from typing import List

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="day10", description="パフォーマンス・コスト最適化")
    p.add_argument("--query", required=True, help="1件の質問（mode=cache/stream 用）または複数行テキスト（mode=batch 用）")
    p.add_argument("--mode", choices=["cache", "stream", "batch"], default="cache",
                   help="cache=セマンティックキャッシュ, stream=TTFT計測, batch=並列バッチ")
    p.add_argument("--batch-size", type=int, default=5, help="batch モード時の並列数")
    p.add_argument("--region", default=None)
    p.add_argument("--model-id", default=None)
    return p

def _validate_args(args: argparse.Namespace) -> None:
    if not args.query.strip():
        raise ValueError("--query must not be empty")
    if args.batch_size < 1 or args.batch_size > 20:
        raise ValueError("--batch-size must be between 1 and 20")

def run_optimized(
    query: str,
    mode: str = "cache",
    batch_size: int = 5,
    region: str | None = None,
    model_id: str | None = None,
) -> str:
    """指定されたモードで最適化された Bedrock 呼び出しを実行する。

    実装ガイド:
    - mode="cache" : セマンティックキャッシュを実装する
                     同一または類似クエリの2回目以降はキャッシュから返す
                     キャッシュヒット時は stdout に "CACHE HIT" と表示する
                     キャッシュには FAISS + Bedrock Embeddings を使う
    - mode="stream" : ストリーミングで応答し、最初のトークンが届くまでの時間
                      (TTFT) をミリ秒で表示する
                      最後の行に "TTFT: XXX ms" を付け足して返す
    - mode="batch"  : query を改行で分割して複数の質問とみなし、
                      asyncio.gather で並列実行して結果リストを返す
                      直列実行との時間比較を末尾に追加する
                      boto3 は同期 API のため、各呼び出しを
                      asyncio.to_thread(bedrock_call, ...) でラップして
                      イベントループをブロックしないこと（Windows/Mac 共通）

    戻り値:
        最適化モードに応じた回答テキスト
    """
    raise NotImplementedError("day10: run_optimized() を実装してください")

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
    logging.info("mode=%s batch_size=%d", args.mode, args.batch_size)
    try:
        out = run_optimized(args.query, args.mode, args.batch_size, args.region, args.model_id)
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
