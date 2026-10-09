# Day 06 — MCP（Model Context Protocol）

## 受講者が実装する場所

- `day06/server.py` の `serve()`
- `day06/app.py` の `run_with_mcp()`

## 目的

ツール・データソース接続を標準化する MCP（Model Context Protocol）を実装し、エージェントから利用する。通常の `@tool` 定義との違いを理解し、サーバーを差し替えてもクライアント側のコードが変わらない疎結合な構成を体験する。

### 通常の @tool 定義との違い

通常の `@tool` はエージェントのコード内に直接定義するため、ツールを追加・変更するたびにエージェントを修正・再起動する必要がある。MCP を使うとツール定義はサーバーとして独立し、エージェントは接続先 URL を変えるだけで別のツールセットを利用できる。

## ゴール（完了条件）

- MCP サーバーが `search` ツールと `documents://list` リソースを公開している
- クライアントがサーバーから Tools 一覧を取得してエージェントに渡せる
- エージェントが MCP サーバーの `search` ツールを呼び出して回答を生成する

## 起動手順

> **注意：このDayはターミナルを2つ使います。**

### ターミナル1（MCP サーバー起動）

```bash
python -m day06.server --port 8200 --data-dir day05/data
```

起動確認ログ：

```
INFO Starting MCP server on port 8200
INFO MCP server running at http://127.0.0.1:8200
```

### ターミナル2（クライアント実行）

```bash
python -m day06.app --query "LangGraph のサブグラフの使い方は？" --server-url http://127.0.0.1:8200
```

## 機能要件

### MCP サーバー（`day06/server.py`）

- `python -m day06.server --port 8200` で起動できること
- Tools として `search(query: str, top_k: int = 5) -> str` を公開する
- Resources として `documents://list` を公開する（ファイル一覧を JSON で返す）

### MCP クライアント（`day06/app.py`）

- `python -m day06.app --query "..."` で実行できること
- `--server-url` でサーバーの URL を指定できる（デフォルト: `http://127.0.0.1:8200`）
- MCP サーバーから Tools 一覧を取得してエージェントに登録する

### 終了コード

- 正常終了：`0`
- 入力不備：`2`
- 実行失敗：`1`

## 実装タスク

1. MCP サーバーで `search` ツールを定義する（Day05 の hybrid 検索を呼び出す）
   - `mcp` ライブラリの `FastMCP` クラスを使うこと（旧 `Server` クラスは非推奨）
   - `@mcp.tool()` デコレーターでツールを登録し、`mcp.run()` で起動する
2. MCP サーバーで `documents://list` リソースを定義する
3. `serve()` で MCP サーバーを起動する
4. クライアントで MCP 接続を確立し Tools 一覧を取得する
5. LangChain の MCP ツールとして登録しエージェントに渡す
6. エージェントが必要に応じて search ツールを呼び出して回答する

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
# ターミナル1
python -m day06.server --port 8200

# ターミナル2
python -m day06.app --query "RAGのハイブリッド検索とは？" --server-url http://127.0.0.1:8200
```

---

**以下は受講者が記入してください**

## 提出物

- `day06/server.py`
- `day06/app.py`
- `day06/README.md`

## セルフレビュー

- 正常系：MCP サーバー起動後、クライアントから質問を送り根拠付き回答が返る
- 異常系：`--query` が空のとき終了コード `2` が返る
- 境界：`day05/data/` が空のとき適切なメッセージが返る
- 再実行：サーバーを再起動せずに同じ質問を2回送っても問題ない

## MCP実装メモ

- 使用した mcp ライブラリのバージョン：
- Tools の定義方法：
- Resources の定義方法：
- クライアントの接続方法：

## リサーチメモ（任意）

- MCP の仕様（Tools / Resources / Prompts の使い分け）
- FastMCP vs MCP Server の違い
- LangChain からの MCP Tool 呼び出し方法
