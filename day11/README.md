# Day 11 — 評価指標の理解と計測

## 受講者が実装する場所

- `day11/app.py` の `load_suite()` と `run_evaluation()`

## 目的

エージェントと RAG の品質を客観的に計測する仕組みを実装する。LLM-as-a-Judge を使った自動評価とタスク達成率の計測を通じて、数値で改善効果を確認できるようにする。

## ゴール（完了条件）

- テストスイート（`day11/suite.json`）を読み込んで実行できる
- RAG ケースに Faithfulness と Answer Relevance が付く
- エージェントケースにタスク達成率とステップ数が付く
- 結果が `day11/results/eval_result.json` に保存される

## 4種類の評価指標

| 指標 | 対象 | 定義 | 計測方法 |
|------|------|------|---------|
| Faithfulness | RAG | 回答が検索結果に基づいているか（幻覚がないか） | LLM-as-a-Judge（0.0〜1.0） |
| Answer Relevance | RAG | 質問に対して回答が適切かどうか | LLM-as-a-Judge（0.0〜1.0） |
| タスク達成率 | エージェント | expected_tools が実際に呼ばれたか | 0 または 1 |
| ステップ数 | エージェント | 何ノードを経由したか | 実行ノード数のカウント |

## LLM-as-a-Judge のプロンプト設計例

### Faithfulness の評価プロンプト

```
以下の質問と回答のペアに対して、Faithfulness（忠実度）を 0.0〜1.0 で評価してください。
Faithfulness とは、回答が提供されたコンテキスト（検索結果）に基づいているかどうかです。
数値のみ回答してください。
質問: {question}
コンテキスト: {context}
回答: {answer}
```

### Answer Relevance の評価プロンプト

```
以下の質問と回答のペアに対して、Answer Relevance（回答の関連性）を 0.0〜1.0 で評価してください。
Answer Relevance とは、回答が質問に対して的確に答えているかどうかです。
数値のみ回答してください。
質問: {question}
回答: {answer}
```

## 機能要件

### コマンド

- `python -m day11.app` で起動できること

### 任意オプション

- `--suite`：テストスイートの JSON ファイルパス（デフォルト: `day11/suite.json`）
- `--output`：評価結果の出力先（デフォルト: `day11/results/eval_result.json`）
- `--region`：AWSリージョン
- `--model-id`：BedrockのモデルID

### 出力フォーマット（標準出力）

```json
{
  "total": 14,
  "rag_faithfulness_avg": 0.82,
  "rag_relevance_avg": 0.75,
  "agent_task_success_rate": 0.67
}
```

### 終了コード

- 正常終了：`0`
- ファイル不存在・JSON パースエラー：`2`
- 実行失敗：`1`

## 実装タスク

1. `load_suite()` を実装する（JSON ファイル読み込み + エラーハンドリング）
2. RAG ケース評価を実装する（`answer_with_advanced_rag()` 呼び出し + LLM-as-a-Judge）
3. エージェントケース評価を実装する（`run_multi_agent()` 呼び出し + ツール呼び出し確認）
4. LLM-as-a-Judge のプロンプトを設計・実装する
5. 結果を `output_path` に JSON Lines 形式で保存する
6. サマリを計算して返す

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
# デフォルト設定で評価を実行
python -m day11.app

# カスタムスイートと出力先を指定
python -m day11.app --suite day11/suite.json --output day11/results/my_eval.json
```

### 期待する出力例

```json
{
  "total": 14,
  "rag_faithfulness_avg": 0.82,
  "rag_relevance_avg": 0.75,
  "agent_task_success_rate": 0.67
}
```

---

**以下は受講者が記入してください**

## 提出物

- `day11/app.py`
- `day11/results/eval_result.json`（評価結果）
- `day11/README.md`

## セルフレビュー

- 正常系：14ケースすべてが実行され results に JSON が保存される
- 異常系：スイートファイルが存在しない場合に終了コード `2` が返る
- 境界：空の `input` を持つ `agent-invalid` ケースでエラーが適切に処理される
- 再実行：2回実行しても results が正常に上書きされる

## 評価結果メモ

| 指標 | スコア |
|------|-------|
| rag_faithfulness_avg | |
| rag_relevance_avg | |
| agent_task_success_rate | |

## リサーチメモ（任意）

- LLM-as-a-Judge の設計原則
- RAGAS の指標定義（参考）
- タスク達成率の計測方法（ノード実行履歴の取得）
