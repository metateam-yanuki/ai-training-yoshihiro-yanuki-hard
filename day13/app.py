from __future__ import annotations
import argparse, logging, sys
from typing import List

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="day13", description="最終課題への導線")
    p.add_argument("--message", required=True)
    p.add_argument("--region", default=None)
    p.add_argument("--model-id", default=None)
    return p

def main(argv: List[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        from final.agent import run_agent
    except ImportError as e:
        logging.error("final/agent.py が見つかりません: %s", e)
        print("final/agent.py を実装してください", file=sys.stderr)
        return 1

    logging.info("message=%r", args.message[:50])
    try:
        result = run_agent(args.message)
        print(result.get("reply", ""))
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
