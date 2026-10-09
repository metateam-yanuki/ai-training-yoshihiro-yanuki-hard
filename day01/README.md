# Day 01 — マルチエージェント基礎（Supervisor / Handoff）

## 受講者が実装する場所

- `day01/app.py` の `run_multi_agent()`

## 目的

複数エージェントが役割分担して動く最小構成を理解し実装する。Supervisor が入力を受け取り適切な Worker に振り分け、各 Worker の出力を統合して最終回答を生成する流れを体験する。

## ゴール（完了条件）

- Supervisor が入力に応じて Worker を選択できる
- research Worker と summarize Worker の出力が state に積み上がる
- `--verbose` で各ノードの動作が確認できる

## 機能要件

CLIは次の仕様を満たしてください。

### コマンド

- `python -m day01.app` で起動できること（モジュール名は固定）

### 必須オプション

- `--query`：調査・要約させたい入力テキスト（文字列、必須）

### 任意オプション

- `--verbose`：各エージェントの動作ログを表示する（フラグ）
- `--region`：AWSリージョン（未指定の場合は環境変数 `AWS_REGION` を利用）
- `--model-id`：BedrockのモデルID（未指定の場合は環境変数 `BEDROCK_MODEL_ID` を利用）

### 出力フォーマット

```
最終回答テキスト

[Research]
調査結果テキスト

[Summary]
要約テキスト
```

### 終了コード

- 正常終了：`0`
- 入力不備（`--query` が空など）：`2`
- 実行失敗（NotImplementedError / 例外）：`1`

### ログ

- 実行開始時に `query` と `verbose` フラグを INFO で出す
- 例外発生時は ERROR で要点を出す
- `verbose=True` のとき各ノードの入出力を INFO で出す

## 実装タスク

1. LangGraph の State を定義する（`query`, `research_result`, `summary`, `final_answer`）
2. research Worker ノードを実装する（Bedrock を使って調査結果を生成）
3. summarize Worker ノードを実装する（research_result を要約）
4. Supervisor ノードを実装する（Command で Worker に Handoff）
5. グラフを組み立てて compile する
6. verbose フラグに応じてログ出力を制御する

## 実行方法

### 必要な環境変数

```bash
# 1. .env.example を .env にコピーして設定
cp .env.example .env

# 2. AWS認証
export AWS_PROFILE=training

# 3. リージョン・モデルID（.env で設定済みなら不要）
export AWS_REGION=ap-northeast-1
export BEDROCK_MODEL_ID=anthropic.claude-haiku-4-5-20251001-v1:0
```

Windows（PowerShell）の場合：

```powershell
copy .env.example .env
$env:AWS_PROFILE = "training"
$env:AWS_REGION = "ap-northeast-1"
$env:BEDROCK_MODEL_ID = "anthropic.claude-haiku-4-5-20251001-v1:0"
```

### 実行コマンド例

```bash
# 基本的な実行
python -m day01.app --query "LangGraphの特徴を調査して要約してください"

# 詳細ログを表示
python -m day01.app --query "AWS Bedrock について教えてください" --verbose

# リージョンとモデルを明示的に指定
python -m day01.app --query "RAGとは何か" --region ap-northeast-1 --model-id anthropic.claude-haiku-4-5-20251001-v1:0
```

### 期待する出力例

```
LangGraphはグラフベースのAIエージェントフレームワークです。（最終回答）

[Research]
LangGraphはLangChainの拡張で、状態管理とノード間の遷移を定義できます。...

[Summary]
LangGraphはAIエージェントの状態遷移をグラフ構造で管理するフレームワークです。
```

---

**以下は受講者が記入してください**

## 提出物

- `day01/app.py`
- `day01/README.md`

## セルフレビュー

- 正常系：query を渡すと Research / Summary セクションを含む最終回答が返る
- 異常系：`--query` が空のとき終了コード `2` で適切なエラーが出る
- 境界：長文クエリでもクラッシュせず結果が返る
- 再実行：同じ入力を2回実行し、破綻しない（多少の揺れは許容）

## Bedrock確認

- モデル：
- リージョン：
- verbose 時の各ノード動作：

## リサーチメモ（任意）

調べたURLや、理解した要点をメモしてください。

- LangGraph の Supervisor パターンについて
- Command / Handoff の使い方
- マルチエージェントの状態設計
