from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Tuple

import httpx
import streamlit as st

from dotenv import load_dotenv


def call_runner(base_url: str, module: str, args: List[str], timeout_sec: int) -> Dict[str, Any]:
    payload = {"module": module, "args": args, "timeout_sec": timeout_sec}
    with httpx.Client(timeout=timeout_sec + 10) as client:
        r = client.post(f"{base_url.rstrip('/')}/run", json=payload)
        r.raise_for_status()
        return r.json()


def render_result(result: Dict[str, Any]) -> None:
    st.markdown("### 実行結果")
    cols = st.columns(4)
    cols[0].metric("exit code", int(result.get("returncode", -1)))
    cols[1].metric("duration(ms)", int(result.get("duration_ms", 0)))
    cols[2].metric("stdout bytes", len(str(result.get("stdout", "")).encode("utf-8")))
    cols[3].metric("stderr bytes", len(str(result.get("stderr", "")).encode("utf-8")))

    st.markdown("### command")
    st.code(" ".join(result.get("command", [])), language="bash")

    st.markdown("### stdout")
    st.code(result.get("stdout") or "(empty)")
    st.markdown("### stderr")
    st.code(result.get("stderr") or "(empty)")


def page_day01() -> Tuple[str, List[str], int]:
    st.subheader("Day01: マルチエージェント基礎")
    query = st.text_area("--query", value="LangGraph の特徴を調査して要約してください")
    verbose = st.checkbox("--verbose", value=False)
    region = st.text_input("--region (optional)", value="")
    model_id = st.text_input("--model-id (optional)", value="")
    timeout = st.number_input("timeout(sec)", min_value=1, max_value=300, value=60, step=1)

    module = "day01.app"
    args = ["--query", query]
    if verbose:
        args.append("--verbose")
    if region:
        args += ["--region", region]
    if model_id:
        args += ["--model-id", model_id]
    return module, args, int(timeout)


def page_day02() -> Tuple[str, List[str], int]:
    st.subheader("Day02: LangGraph サブグラフ・ストリーミング")
    query = st.text_area("--query", value="AWS Bedrock の特徴を教えてください")
    stream = st.checkbox("--stream", value=False)
    region = st.text_input("--region (optional)", value="")
    model_id = st.text_input("--model-id (optional)", value="")
    timeout = st.number_input("timeout(sec)", min_value=1, max_value=300, value=60, step=1)

    module = "day02.app"
    args = ["--query", query]
    if stream:
        args.append("--stream")
    if region:
        args += ["--region", region]
    if model_id:
        args += ["--model-id", model_id]
    return module, args, int(timeout)


def page_day03() -> Tuple[str, List[str], int]:
    st.subheader("Day03: A2A クライアント")
    st.info("A2A サーバーを先に起動してください: `python -m day03.server --port 8100`")
    task = st.text_area("--task", value="次の文章を要約してください：LangGraphはグラフベースのAIエージェントフレームワークです。")
    server_url = st.text_input("--server-url", value="http://127.0.0.1:8100")
    timeout = st.number_input("timeout(sec)", min_value=1, max_value=300, value=60, step=1)

    module = "day03.app"
    args = ["--task", task, "--server-url", server_url]
    return module, args, int(timeout)


def page_day04() -> Tuple[str, List[str], int]:
    st.subheader("Day04: メモリ設計")
    message = st.text_area("--message", value="私の名前はTaroです")
    thread_id = st.text_input("--thread-id", value="default")
    memory_type = st.selectbox("--memory-type", options=["short", "long", "episode"], index=0)
    timeout = st.number_input("timeout(sec)", min_value=1, max_value=300, value=60, step=1)

    module = "day04.app"
    args = ["--message", message, "--thread-id", thread_id, "--memory-type", memory_type]
    return module, args, int(timeout)


def page_day05() -> Tuple[str, List[str], int]:
    st.subheader("Day05: 高度 RAG")
    question = st.text_area("--question", value="LangGraph とはどのような技術ですか？")
    strategy = st.selectbox("--strategy", options=["vector", "hybrid", "rerank", "expand"], index=1)
    data_dir = st.text_input("--data-dir", value="day05/data")
    top_k = st.number_input("--top-k", min_value=1, max_value=20, value=5, step=1)
    timeout = st.number_input("timeout(sec)", min_value=1, max_value=300, value=60, step=1)

    module = "day05.app"
    args = ["--question", question, "--strategy", strategy, "--data-dir", data_dir, "--top-k", str(int(top_k))]
    return module, args, int(timeout)


def page_day06() -> Tuple[str, List[str], int]:
    st.subheader("Day06: MCP クライアント")
    st.info("MCP サーバーを先に起動してください: `python -m day06.server --port 8200`")
    query = st.text_area("--query", value="RAG のハイブリッド検索とは何ですか？")
    server_url = st.text_input("--server-url", value="http://127.0.0.1:8200")
    timeout = st.number_input("timeout(sec)", min_value=1, max_value=300, value=60, step=1)

    module = "day06.app"
    args = ["--query", query, "--server-url", server_url]
    return module, args, int(timeout)


def page_day07() -> Tuple[str, List[str], int]:
    st.subheader("Day07: Human-in-the-Loop")
    st.warning("このDayは標準入力で承認プロンプトが出ます。CLIで直接実行するか --auto-approve を使ってください。")
    query = st.text_area("--query", value="重要なドキュメントを処理してください")
    thread_id = st.text_input("--thread-id", value="default")
    auto_approve = st.checkbox("--auto-approve（テスト用）", value=True)
    timeout = st.number_input("timeout(sec)", min_value=1, max_value=300, value=60, step=1)

    module = "day07.app"
    args = ["--query", query, "--thread-id", thread_id]
    if auto_approve:
        args.append("--auto-approve")
    return module, args, int(timeout)


def page_day08() -> Tuple[str, List[str], int]:
    st.subheader("Day08: 可観測性・ログ設計")
    query = st.text_area("--query", value="LangGraph のサブグラフについて教えてください")
    log_file = st.text_input("--log-file", value="day08/run.log")
    timeout = st.number_input("timeout(sec)", min_value=1, max_value=300, value=60, step=1)

    module = "day08.app"
    args = ["--query", query, "--log-file", log_file]
    return module, args, int(timeout)


def page_day09() -> Tuple[str, List[str], int]:
    st.subheader("Day09: セキュリティ強化")
    text = st.text_area("--text (optional)", value="")
    mode = st.selectbox("--mode", options=["normal", "attack"], index=0)
    case = st.number_input("--case（attack モード時）", min_value=1, max_value=3, value=1, step=1)
    timeout = st.number_input("timeout(sec)", min_value=1, max_value=300, value=60, step=1)

    module = "day09.app"
    args = ["--mode", mode, "--case", str(int(case))]
    if text.strip():
        args += ["--text", text]
    return module, args, int(timeout)


def page_day10() -> Tuple[str, List[str], int]:
    st.subheader("Day10: パフォーマンス・コスト最適化")
    query = st.text_area("--query", value="LangGraph とは何ですか？")
    mode = st.selectbox("--mode", options=["cache", "stream", "batch"], index=0)
    batch_size = st.number_input("--batch-size（batch モード時）", min_value=1, max_value=20, value=5, step=1)
    timeout = st.number_input("timeout(sec)", min_value=1, max_value=300, value=60, step=1)

    module = "day10.app"
    args = ["--query", query, "--mode", mode, "--batch-size", str(int(batch_size))]
    return module, args, int(timeout)


def page_day11() -> Tuple[str, List[str], int]:
    st.subheader("Day11: 評価指標の理解と計測")
    suite = st.text_input("--suite", value="day11/suite.json")
    output = st.text_input("--output", value="day11/results/eval_result.json")
    timeout = st.number_input("timeout(sec)", min_value=1, max_value=600, value=120, step=1)

    module = "day11.app"
    args = ["--suite", suite, "--output", output]
    return module, args, int(timeout)


def page_day12() -> Tuple[str, List[str], int]:
    st.subheader("Day12: 失敗分析と改善サイクル")
    result = st.text_input("--result", value="day11/results/eval_result.json")
    output = st.text_input("--output", value="day12/results/improved_result.json")
    apply_fix = st.checkbox("--apply-fix（改善を適用して再評価）", value=False)
    timeout = st.number_input("timeout(sec)", min_value=1, max_value=600, value=120, step=1)

    module = "day12.app"
    args = ["--result", result, "--output", output]
    if apply_fix:
        args.append("--apply-fix")
    return module, args, int(timeout)


def page_day13() -> Tuple[str, List[str], int]:
    st.subheader("Day13: 最終課題への導線")
    message = st.text_area("--message", value="LangGraph の特徴を調査して要約してください")
    timeout = st.number_input("timeout(sec)", min_value=1, max_value=300, value=60, step=1)

    module = "day13.app"
    args = ["--message", message]
    return module, args, int(timeout)


def page_final() -> None:
    st.subheader("Final: Chat UI")
    st.markdown("最終課題はチャットUIで稼働確認します。")
    st.markdown("事前に A2A サーバーと MCP サーバーを起動してください。")
    st.code(
        "# ターミナル1: A2A サーバー\npython -m day03.server --port 8100\n\n"
        "# ターミナル2: MCP サーバー\npython -m day06.server --port 8200\n\n"
        "# ターミナル3: チャット UI\nstreamlit run final/chat_ui.py",
        language="bash",
    )


PAGES = {
    "Day01: マルチエージェント": page_day01,
    "Day02: LangGraph 応用": page_day02,
    "Day03: A2A クライアント": page_day03,
    "Day04: メモリ設計": page_day04,
    "Day05: 高度 RAG": page_day05,
    "Day06: MCP クライアント": page_day06,
    "Day07: Human-in-the-Loop": page_day07,
    "Day08: 可観測性・ログ": page_day08,
    "Day09: セキュリティ": page_day09,
    "Day10: パフォーマンス最適化": page_day10,
    "Day11: 評価計測": page_day11,
    "Day12: 失敗分析・改善": page_day12,
    "Day13: 最終課題導線": page_day13,
    "Final (Chat UI)": page_final,
}


st.set_page_config(page_title="研修 共通画面（応用編）", layout="centered")
st.title("研修 共通画面（応用編）")
st.caption("メニューからDayを選び、入力→実行で稼働確認します。")

load_dotenv()

base_url = st.sidebar.text_input("Runner API base URL", value=os.getenv("RUNNER_BASE_URL", "http://127.0.0.1:8000"))
page = st.sidebar.selectbox("メニュー", options=list(PAGES.keys()))

builder = PAGES[page]

if builder is page_final:
    builder()
    st.stop()

module, args, timeout_sec = builder()

st.markdown("### リクエスト")
st.code(
    json.dumps({"module": module, "args": args, "timeout_sec": timeout_sec}, ensure_ascii=False, indent=2),
    language="json",
)

run = st.button("実行")

if run:
    try:
        result = call_runner(base_url, module, args, timeout_sec)
        render_result(result)
    except httpx.HTTPError as e:
        st.error(str(e))
    except Exception as e:
        st.exception(e)
