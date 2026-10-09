from __future__ import annotations
from typing import Any, Dict, List

def run_agent(
    message: str,
    history: List[Dict[str, str]] | None = None,
) -> Dict[str, Any]:
    """応用編全体を統合したマルチエージェントを実行する。

    仕上げ要件（すべて実装すること）:
    1. LangGraph でマルチエージェント構成（Supervisor + Worker × 2 以上）
    2. A2A で少なくとも 1 つのエージェントを外部サービスとして公開・呼び出し
    3. MCP サーバー経由でツールまたはデータソースを接続
    4. 高度 RAG（ハイブリッド検索またはリランキング）
    5. Human-in-the-Loop（少なくとも 1 箇所の承認ポイント）
       ※ Streamlit からの呼び出しは同期実行のため、interrupt() は別スレッドで
          状態保存後に "AWAITING_APPROVAL" を返し、次回メッセージで再開すること
    6. メモリ設計（会話をまたいだ文脈保持）
    7. 構造化ログ・コールバック（Day08 の実装を組み込む）
    8. セキュリティ（入力バリデーション・PII マスク）

    戻り値:
        {
            "reply": "ユーザーに表示するテキスト",
            "meta": {
                "actions": [...],        # 実行したアクション一覧
                "citations": [...],      # 根拠（URL/ファイル名）
                "next_actions": [...],   # 次にとるべきアクション提案（JSON）
                "debug_info": {...}      # デバッグ情報（ノード実行順、ツール呼び出し）
            }
        }
    """
    raise NotImplementedError("final: run_agent() を実装してください")
