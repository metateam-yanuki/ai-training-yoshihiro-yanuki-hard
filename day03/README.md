# Day 03 — A2A（Agent-to-Agent Protocol）

## 受講者が実装する場所

- `day03/server.py` の `serve()`
- `day03/app.py` の `call_agent()`

## 目的

LangGraph 内の閉じたマルチエージェントを超えて、システム間でエージェントを連携する標準プロトコルを実装する。A2A（Agent-to-Agent Protocol）を使って、エージェントを HTTP サーバーとして公開し、別プロセスのクライアントから呼び出す仕組みを理解する。

## ゴール（完了条件）

- AgentCard に能力（capabilities）が記述されている
- クライアントから Task を送り、サーバーがレスポンスを返せる
- 別プロセス（ターミナル2つ）で通信できる

## 起動手順

> **注意：このDayはターミナルを2つ使います。**

### ターミナル1（サーバー起動）

```bash
python -m day03.server --port 8100
```

起動確認ログ：

```
INFO Starting A2A server on 127.0.0.1:8100
INFO A2A server running at http://127.0.0.1:8100
```

### ターミナル2（クライアント実行）

```bash
python -m day03 --task "次の文章を要約してください：..." --server-url http://127.0.0.1:8100
```

## 機能要件

### サーバー（`day03/server.py`）

- `python -m day03.server --port 8100` で起動できること
- AgentCard に `name`, `description`, `capabilities` を記述する
- Task（テキスト）を受け取ったら Bedrock で要約して返す
- `TaskState.completed` で完了を通知する

### クライアント（`day03/app.py`）

- `python -m day03 --task "..."` で実行できること
- `--server-url` でサーバーの URL を指定できる（デフォルト: `http://127.0.0.1:8100`）
- AgentCard を取得して capabilities を確認する
- Task を送信し結果を受け取って標準出力に表示する

### 終了コード

- 正常終了：`0`
- 入力不備：`2`
- 実行失敗：`1`

## 実装タスク

1. AgentCard を定義する（`name`, `description`, `capabilities`）
2. サーバー側の Task ハンドラを実装する（Bedrock で要約）
3. `serve()` で A2AServer を起動する
4. クライアント側で A2AClient を使って AgentCard を取得する
5. Task を送信し `TaskState.completed` になるまでポーリングする
6. 結果テキストを返す

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
python -m day03.server --port 8100

# ターミナル2
python -m day03 --task "次の文章を要約してください：LangGraphはAIエージェントをグラフ構造で定義するフレームワークです。" --server-url http://127.0.0.1:8100
```

### 期待する出力例

```
LangGraphはグラフベースのAIエージェントフレームワークです。
```

---

**以下は受講者が記入してください**

## 提出物

- `day03/server.py`
- `day03/app.py`
- `day03/README.md`

## セルフレビュー

- 正常系：サーバー起動後、クライアントからタスクを送って結果が返る
- 異常系：`--task` が空のとき終了コード `2` が返る
- 境界：長文タスクでもクラッシュしない
- 再実行：サーバーを再起動せずに同じタスクを2回送っても問題ない

## A2A実装メモ

- AgentCard の定義方法：
- Task の送受信フロー：
- 接続に使った SDK バージョン：

## リサーチメモ（任意）

- A2A プロトコルの仕様
- a2a-sdk の使い方（A2AServer / A2AClient）
- AgentCard の設計指針
