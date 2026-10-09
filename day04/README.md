# Day 04 — メモリ設計（短期・長期・エピソード記憶）

## 受講者が実装する場所

- `day04/app.py` の `run_chat()`

## 目的

会話をまたいで文脈を保持する仕組みを理解し、用途に応じて3種類のメモリを使い分けられるようにする。短期記憶（スレッド内）・長期記憶（永続DB）・エピソード記憶（サマリ圧縮）の違いと実装方法を習得する。

## ゴール（完了条件）

- 3種類のメモリタイプ（`short`, `long`, `episode`）がすべて動作する
- `long` / `episode` はセッションをまたいで前の情報を参照できる
- `episode` はターン数が 10 を超えたときサマリ圧縮が機能する

## 機能要件

### コマンド

- `python -m day04.app` で起動できること

### 必須オプション

- `--message`：ユーザーメッセージ（文字列、必須）

### 任意オプション

- `--thread-id`：会話スレッドID（デフォルト: `default`）
- `--memory-type`：`short` / `long` / `episode`（デフォルト: `short`）
- `--region`：AWSリージョン
- `--model-id`：BedrockのモデルID

### メモリタイプの仕様

| タイプ | バックエンド | 永続化 | 圧縮 |
|--------|------------|--------|------|
| short | MemorySaver（インメモリ） | なし（プロセス終了で消える） | なし |
| long | SqliteSaver（memory.db） | あり | なし |
| episode | SqliteSaver（memory.db） | あり | 10ターン超えでサマリ生成 |

### 終了コード

- 正常終了：`0`
- 入力不備：`2`
- 実行失敗：`1`

## 実装タスク

1. MemorySaver を使った短期記憶（`short`）を実装する
2. SqliteSaver を使った長期記憶（`long`）を実装する
3. エピソード圧縮ロジックを実装する（`episode`）
   - 10 ターンを超えたらサマリを生成して古いメッセージを置き換える
4. `thread_id` ごとに会話履歴を分離する

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
# 短期記憶（プロセス終了で消える）
python -m day04.app --message "私の名前はTaroです" --thread-id t1 --memory-type short
python -m day04.app --message "私の名前を覚えていますか？" --thread-id t1 --memory-type short
# ↑ 別プロセスなので名前を覚えていない

# 長期記憶（セッションをまたぐ）
python -m day04.app --message "私の名前はTaroです" --thread-id t2 --memory-type long
python -m day04.app --message "私の名前を覚えていますか？" --thread-id t2 --memory-type long
# ↑ SQLiteに保存されているので「Taro」と答えるはず

# エピソード記憶（10ターン超えでサマリ圧縮）
python -m day04.app --message "AWS Bedrockについて教えてください" --thread-id t3 --memory-type episode
```

### 期待する出力例（long, 2回目）

```
はい、あなたの名前は「Taro」と教えていただきました。
```

---

**以下は受講者が記入してください**

## 提出物

- `day04/app.py`
- `day04/README.md`

## セルフレビュー

- 正常系：short / long / episode それぞれで返答が返る
- 異常系：`--message` が空のとき終了コード `2` が返る
- 境界：長文メッセージでもクラッシュしない
- 再実行（long）：同じ thread-id で2回実行して前の会話を参照できる

## メモリ実装メモ

- MemorySaver の使い方：
- SqliteSaver の使い方（接続先ファイル名など）：
- エピソード圧縮のロジック設計：

## リサーチメモ（任意）

- LangGraph の checkpointer の種類と選び方
- SqliteSaver のスレッド別履歴管理
- エピソード記憶の圧縮タイミングとサマリ生成プロンプト
