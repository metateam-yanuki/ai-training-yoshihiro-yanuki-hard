from __future__ import annotations
import argparse, logging, sys
from typing import List

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

def run_chat(
    message: str,
    thread_id: str = "default",
    memory_type: str = "short",
    region: str | None = None,
    model_id: str | None = None,
) -> str:
    """指定されたメモリタイプで会話を継続する。

    実装ガイド:
    - memory_type="short" : LangGraph の MemorySaver でスレッド内のみ保持
    - memory_type="long"  : SqliteSaver で SQLite (memory.db) に永続保存
                            次回同じ thread_id で呼び出すと前の会話を参照できること
    - memory_type="episode": long と同様に永続保存するが、
                             会話が 10 ターン（= ユーザー発言 10 回）を超えたら
                             それまでの履歴を LLM でサマリに圧縮してトークン数を削減する
    - thread_id ごとに会話履歴を分離する

    戻り値:
        アシスタントの返答テキスト
    """
    raise NotImplementedError("day04: run_chat() を実装してください")

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
