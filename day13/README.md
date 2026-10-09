# Day 13 — 最終課題（統合）

## このDayについて

Day 13 は `final/agent.py` の実装に進む導線です。  
`python -m day13.app --message "..."` を実行すると `final/agent.py` の `run_agent()` が呼び出されます。

## 受講者が実装する場所

- `final/agent.py` の `run_agent()`

## 時間配分（重要）

> 仕上げ要件は 8 項目あり、Day13 の 1 日だけでは完了が困難です。
> **Day12 の午後から着手**し、Day12 午後 + Day13 の合計 1.5 日を実装時間として使ってください。
> Day12 の改善サイクルは午前中に完了させることを目標にします。

## 最終課題への進め方

### 1. final/README.md を確認する

`final/README.md` に仕上げ要件（8項目）が記載されています。まず要件を把握してから実装を始めてください。

### 2. final/agent.py を実装する

`final/agent.py` の `run_agent()` を実装します。Day01〜Day12 で作成したコンポーネントを統合します。

### 3. day13 で動作確認する

```bash
python -m day13.app --message "LangGraph の特徴を調査して要約してください"
```

Day13 は `final/agent.py` の薄いラッパーです。実装が完了するまで `NotImplementedError` が返ります。

### 4. チャット UI で動作確認する

```bash
streamlit run final/chat_ui.py
```

## 実行方法

### 必要な環境変数

```bash
cp .env.example .env
export AWS_PROFILE=training
export AWS_REGION=ap-northeast-1
export BEDROCK_MODEL_ID=anthropic.claude-haiku-4-5-20251001-v1:0
```

### 実行コマンド例

```bash
# day13 経由で最終エージェントを呼び出す
python -m day13.app --message "RAGとマルチエージェントを組み合わせた設計を説明してください"
```

### 期待する出力

`final/agent.py` の実装が完了すると `reply` フィールドのテキストが表示されます。

---

**以下は受講者が記入してください**

## 提出物

- `final/agent.py`（最終課題の実装）
- `final/README.md`（セットアップ・実行手順・設計メモ）
- `docs/`（状態遷移図・主要プロンプト・評価結果）

## 実装チェックリスト

仕上げ要件の8項目すべてを確認してから PR を提出してください。  
→ `final/README.md` のチェックリストを参照してください。
