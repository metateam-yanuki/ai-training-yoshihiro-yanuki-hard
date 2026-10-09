# Day 08 — 可観測性・ログ設計（構造化ログ・コールバック）

## 受講者が実装する場所

- `day08/app.py` の `run_with_logging()`

## 目的

エージェントの各ノード・ツール実行をリアルタイムに記録する仕組みを実装する。JSON Lines 形式の構造化ログで運用・デバッグを効率化し、問題発生時にどのノードで何が起きたか追跡できるようにする。

## ゴール（完了条件）

- カスタムコールバックが各ノード・ツールの開始/終了を記録する
- ログが JSON Lines 形式で `--log-file` に追記される
- 各ログに `timestamp`, `event`, `node_name/tool_name`, `input/output`, `duration_ms` が含まれる

## 機能要件

### コマンド

- `python -m day08.app` で起動できること

### 必須オプション

- `--query`：エージェントへの入力テキスト（文字列、必須）

### 任意オプション

- `--log-file`：JSON ログの出力先（デフォルト: `day08/run.log`）
- `--region`：AWSリージョン
- `--model-id`：BedrockのモデルID

### JSON Lines フォーマット例

```json
{"timestamp": "2026-05-01T12:00:00.000Z", "event": "node_start", "node_name": "research", "input": "LangGraph とは..."}
{"timestamp": "2026-05-01T12:00:03.500Z", "event": "node_end", "node_name": "research", "output": "LangGraph はグラフ...", "duration_ms": 3500}
{"timestamp": "2026-05-01T12:00:03.600Z", "event": "tool_start", "tool_name": "search", "input": "LangGraph subgraph"}
{"timestamp": "2026-05-01T12:00:04.100Z", "event": "tool_end", "tool_name": "search", "output": "検索結果...", "duration_ms": 500}
```

### 終了コード

- 正常終了：`0`
- 入力不備：`2`
- 実行失敗：`1`

## 実装タスク

1. `BaseCallbackHandler` を継承したカスタムコールバッククラスを実装する
2. `on_chain_start` / `on_chain_end` でノードの開始/終了を記録する
3. `on_tool_start` / `on_tool_end` でツールの開始/終了を記録する
4. `on_chain_error` / `on_tool_error` でエラーを記録する
5. ログを JSON Lines 形式で `log_file` に追記する（`input`/`output` は 200 文字に切り詰め）
6. Day01 のマルチエージェントにコールバックを組み込む

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
# ログファイルを指定して実行
python -m day08.app --query "LangGraph のサブグラフについて教えてください" --log-file day08/run.log

# ログを確認
cat day08/run.log
```

### jq での絞り込みコマンド例

```bash
# エラーイベントのみ表示
cat day08/run.log | jq 'select(.event == "error")'

# ノード終了イベントと実行時間のみ表示
cat day08/run.log | jq 'select(.event == "node_end") | {node_name, duration_ms}'

# duration_ms が 1000ms 以上のイベントを抽出
cat day08/run.log | jq 'select(.duration_ms != null and .duration_ms > 1000)'

# ツール呼び出し一覧
cat day08/run.log | jq 'select(.event == "tool_start") | .tool_name'
```

---

**以下は受講者が記入してください**

## 提出物

- `day08/app.py`
- `day08/README.md`

## セルフレビュー

- 正常系：実行後にログファイルが生成され JSON Lines フォーマットが正しい
- 異常系：`--query` が空のとき終了コード `2` が返る
- 境界：長文クエリでもログが切り詰められて保存される
- 再実行：2回実行するとログが追記される（上書きではない）

## コールバック実装メモ

- 使用した BaseCallbackHandler のメソッド一覧：
- `duration_ms` の計測方法：
- ログの追記方法（ファイルオープンモード）：

## リサーチメモ（任意）

- LangChain の BaseCallbackHandler の使い方
- JSON Lines 形式の利点と jq での活用
- 構造化ログの設計指針（OpenTelemetry との比較など）
