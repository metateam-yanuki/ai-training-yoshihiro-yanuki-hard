# Day 10 — パフォーマンス・コスト最適化

## 受講者が実装する場所

- `day10/app.py` の `run_optimized()`

## 目的

Bedrock 呼び出しのコストとレイテンシを削減する3つの最適化手法（セマンティックキャッシュ・ストリーミング・バッチ並列）を実装し、それぞれの効果を数値で確認する。

## ゴール（完了条件）

- `mode=cache`：2回目以降のキャッシュヒットで "CACHE HIT" が表示される
- `mode=stream`：ストリーミング応答で "TTFT: XXX ms" が末尾に付く
- `mode=batch`：複数質問が並列実行され、直列との時間比較が表示される

## 機能要件

### コマンド

- `python -m day10.app` で起動できること

### 必須オプション

- `--query`：質問テキスト（`batch` モードでは改行区切りで複数質問）

### 任意オプション

- `--mode`：`cache` / `stream` / `batch`（デフォルト: `cache`）
- `--batch-size`：batch モード時の並列数（1〜20、デフォルト: `5`）
- `--region`：AWSリージョン
- `--model-id`：BedrockのモデルID

### 各モードの仕様

| mode | 仕組み | 確認ポイント |
|------|--------|------------|
| `cache` | FAISS + Bedrock Embeddings でセマンティックキャッシュ | 2回目に "CACHE HIT" が表示される |
| `stream` | Bedrock ストリーミング API で TTFT 計測 | 末尾に "TTFT: XXX ms" が付く |
| `batch` | asyncio.gather で複数質問を並列実行 | 末尾に並列/直列の時間比較が付く |

### 終了コード

- 正常終了：`0`
- 入力不備：`2`
- 実行失敗：`1`

## 実装タスク

1. セマンティックキャッシュを実装する（FAISS + Bedrock Embeddings）
   - コサイン類似度でキャッシュヒット判定（閾値: 0.95 程度）
   - キャッシュヒット時は "CACHE HIT" を標準出力に表示
2. ストリーミング実装（TTFT 計測）
   - 最初のトークンが届いた時刻を記録
   - 末尾に "TTFT: XXX ms" を追加
3. バッチ並列実装
   - `query` を改行で分割して質問リストを生成
   - `asyncio.gather` で並列実行
   - 直列実行との時間を比較して末尾に追加

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
# キャッシュ（1回目）
python -m day10.app --query "LangGraph とは何ですか？" --mode cache

# キャッシュ（2回目：CACHE HIT が表示されるはず）
python -m day10.app --query "LangGraph とは何ですか？" --mode cache

# ストリーミング（TTFT 計測）
python -m day10.app --query "AWS Bedrock の特徴を教えてください" --mode stream

# バッチ（複数質問を並列実行）
python -m day10.app --mode batch --query "LangGraph とは？
RAG とは？
AWS Bedrock とは？"
```

### 比較実験テンプレート

#### キャッシュあり/なし比較

| 実行 | キャッシュ | 実行時間(ms) | コスト |
|------|----------|------------|-------|
| 1回目 | なし | | |
| 2回目（同一質問） | あり（HIT） | | |
| 3回目（類似質問） | あり（HIT） | | |

#### バッチ並列/直列比較

| 実行方法 | 質問数 | 合計時間(ms) | 1件あたり(ms) |
|---------|-------|------------|-------------|
| 直列 | | | |
| 並列（batch-size=5） | | | |

---

**以下は受講者が記入してください**

## 提出物

- `day10/app.py`
- `day10/README.md`

## セルフレビュー

- cache：2回目に CACHE HIT が表示される
- stream：末尾に TTFT: XXX ms が付く
- batch：複数質問が並列実行され時間比較が表示される
- 境界：`--batch-size` が範囲外（0 や 21）で終了コード `2` が返る

## 実験結果メモ

- キャッシュ閾値として設定した値：
- バッチ並列で短縮できた時間（実測値）：
- TTFT の実測値（参考）：

## リサーチメモ（任意）

- FAISS を使ったセマンティックキャッシュの実装方法
- Bedrock ストリーミング API（`invoke_model_with_response_stream`）の使い方
- asyncio を使った並列 Bedrock 呼び出し
- コスト最適化の観点（トークン数削減 vs キャッシュ）
