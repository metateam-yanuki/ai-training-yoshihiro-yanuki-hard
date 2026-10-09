# 最終課題 — 統合マルチエージェント

## 受講者が実装する場所

- `final/agent.py` の `run_agent()`

## 仕上げ要件チェックリスト（8項目）

PR 提出前にすべての項目を満たしていることを確認してください。

- [ ] 1. **LangGraph マルチエージェント構成**：Supervisor + Worker × 2 以上を実装している
- [ ] 2. **A2A 連携**：少なくとも 1 つのエージェントを A2A サーバーとして公開し、別プロセスから呼び出している
- [ ] 3. **MCP 接続**：MCP サーバー経由でツールまたはデータソースを接続している
- [ ] 4. **高度 RAG**：ハイブリッド検索またはリランキングを実装している
- [ ] 5. **Human-in-the-Loop**：少なくとも 1 箇所の承認ポイントがある
- [ ] 6. **メモリ設計**：会話をまたいだ文脈保持が機能する（SqliteSaver 等）
- [ ] 7. **構造化ログ**：Day08 のコールバックを組み込んで実行ログが記録される
- [ ] 8. **セキュリティ**：入力バリデーション・PII マスクが実装されている

## 起動手順

### 1. 事前準備

```bash
# 環境変数の設定
cp .env.example .env
export AWS_PROFILE=training
export AWS_REGION=ap-northeast-1
export BEDROCK_MODEL_ID=anthropic.claude-haiku-4-5-20251001-v1:0

# 依存関係のインストール
pip install -r requirements.txt

# day05/data/ にドキュメントを配置
ls day05/data/
```

### 2. サーバー起動（ターミナル1：A2A サーバー）

```bash
python -m day03.server --port 8100
```

### 3. サーバー起動（ターミナル2：MCP サーバー）

```bash
python -m day06.server --port 8200
```

### 4. チャット UI 起動（ターミナル3）

```bash
streamlit run final/chat_ui.py
```

または CLI で動作確認：

```bash
python -m day13.app --message "LangGraph のサブグラフを使った設計を説明してください"
```

## 出力仕様

`run_agent()` は以下の形式で辞書を返します。

```json
{
  "reply": "ユーザーに表示するテキスト",
  "meta": {
    "actions": ["research", "summarize", "rag_search"],
    "citations": ["langchain_docs.txt", "bedrock_guide.md"],
    "next_actions": ["詳細なコード例を確認する", "実装を試してみる"],
    "debug_info": {
      "nodes_executed": ["supervisor", "research", "summarize"],
      "tools_called": ["search"],
      "memory_type": "long",
      "log_file": "day08/run.log"
    }
  }
}
```

---

**以下は受講者が記入してください**

## 設計メモ

### 状態遷移図

（LangGraph の状態遷移を図示してください）

### 主要プロンプト

- Supervisor プロンプト：
- research Worker プロンプト：
- summarize Worker プロンプト：

### システム構成

- A2A サーバー（port）：
- MCP サーバー（port）：
- メモリバックエンド：
- ログファイル：

## 評価結果

Day11 の評価スコアと改善後のスコアを記録してください。

| 指標 | 初期 | 改善後 |
|------|-----|-------|
| rag_faithfulness_avg | | |
| rag_relevance_avg | | |
| agent_task_success_rate | | |

## セルフレビュー

- 正常系：chat_ui でメッセージを送ると reply と citations が返る
- 異常系：プロンプトインジェクション攻撃がブロックされる
- 境界：セッションをまたいで前の会話を参照できる
- 要件確認：仕上げ要件チェックリスト 8 項目すべて満たしている
