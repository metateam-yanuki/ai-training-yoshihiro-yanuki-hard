from __future__ import annotations

import json
from typing import Any, Dict, List

import streamlit as st

from final.agent import run_agent


st.set_page_config(page_title="AI Agent Chat（応用編）", layout="centered")

st.title("AI Agent Chat（応用編）")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("meta") is not None:
            meta = m["meta"]
            citations = meta.get("citations", [])
            next_actions = meta.get("next_actions", [])
            if citations:
                with st.expander("根拠（Sources）"):
                    for c in citations:
                        st.markdown(f"- {c}")
            if next_actions:
                with st.expander("次のアクション提案"):
                    st.code(json.dumps(next_actions, ensure_ascii=False, indent=2), language="json")
            with st.expander("meta（デバッグ情報）"):
                st.code(json.dumps(meta, ensure_ascii=False, indent=2), language="json")

prompt = st.chat_input("Type a message")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    history: List[Dict[str, str]] = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
        if m["role"] in ("user", "assistant")
    ]

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result: Dict[str, Any] = run_agent(prompt, history=history)
            reply = str(result.get("reply", ""))
            meta = result.get("meta")

        st.markdown(reply)
        if meta is not None:
            citations = meta.get("citations", [])
            next_actions = meta.get("next_actions", [])
            if citations:
                with st.expander("根拠（Sources）"):
                    for c in citations:
                        st.markdown(f"- {c}")
            if next_actions:
                with st.expander("次のアクション提案"):
                    st.code(json.dumps(next_actions, ensure_ascii=False, indent=2), language="json")
            with st.expander("meta（デバッグ情報）"):
                st.code(json.dumps(meta, ensure_ascii=False, indent=2), language="json")

    st.session_state.messages.append({"role": "assistant", "content": reply, "meta": meta})
