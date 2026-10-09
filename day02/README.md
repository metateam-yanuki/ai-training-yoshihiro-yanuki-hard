# Day 02 — LangGraph 応用（サブグラフ・階層エージェント・ストリーミング）

## 受講者が実装する場所

- `day02/app.py` の `run_graph()`

## 目的

Day01 で作ったマルチエージェントを「サブグラフ」に分割し、それぞれを独立してテスト・再利用できる構造にする。さらにストリーミング実行でノード単位の中間経過をリアルタイムに確認できるようにする。

## ゴール（完了条件）

- サブグラフが独立してテスト可能な構造になっている
- ストリーミングモードでノード別の中間経過が確認できる
- `--stream` なし（invoke モード）でも正しく最終回答が返る

## 機能要件

### コマンド

- `python -m day02.app` で起動できること

### 必須オプション

- `--query`：入力テキスト（文字列、必須）

### 任意オプション

- `--stream`：ストリーミングモードで実行する（フラグ）
- `--region`：AWSリージョン
- `--model-id`：BedrockのモデルID

### サブグラフ構成

- `research_subgraph`：調査処理を担当。独自の State（`research_input`, `research_output`）を持つ
- `summarize_subgraph`：要約処理を担当。独自の State（`text_to_summarize`, `summary`）を持つ
- 親グラフ（Supervisor）が両サブグラフをネストして呼び出す

### 終了コード

- 正常終了：`0`
- 入力不備：`2`
- 実行失敗：`1`

## 実装タスク

1. research サブグラフを定義する（独自 State + ノード + コンパイル）
2. summarize サブグラフを定義する（独自 State + ノード + コンパイル）
3. 親グラフに両サブグラフを `add_node` でネストする
4. `stream=True` のとき `graph.stream()` を使いノード別ログを出す
5. `stream=False` のとき `graph.invoke()` を使う

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
# invoke モード（デフォルト）
python -m day02.app --query "LangGraph のサブグラフについて説明してください"

# ストリーミングモード（ノード別途中経過を確認）
python -m day02.app --query "AWS Bedrock の特徴は？" --stream
```

### 期待する出力例（--stream）

```
INFO research_subgraph: starting...
INFO research_subgraph: done.
INFO summarize_subgraph: starting...
INFO summarize_subgraph: done.
AWS Bedrock はフルマネージドの生成AIサービスです。（最終回答）
```

---

**以下は受講者が記入してください**

## 提出物

- `day02/app.py`
- `day02/README.md`

## セルフレビュー

- 正常系：invoke モードで最終回答が返る
- 異常系：`--query` が空のとき終了コード `2` が返る
- 境界：長文クエリでもクラッシュしない
- 再実行：同じ入力を2回実行し破綻しない

## サブグラフ設計メモ

- research サブグラフの State：
- summarize サブグラフの State：
- 親グラフと子グラフの State マッピング方法：

## リサーチメモ（任意）

- LangGraph のサブグラフ（ネスト）の使い方
- `graph.stream()` の出力フォーマット
- 階層エージェントの設計パターン
