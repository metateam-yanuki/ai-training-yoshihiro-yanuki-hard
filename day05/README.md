# Day 05 — 高度 RAG（ハイブリッド検索・リランキング・クエリ拡張）

## 受講者が実装する場所

- `day05/app.py` の `answer_with_advanced_rag()`

## 目的

基本的な RAG（ベクター検索のみ）を超えて、BM25 との組み合わせ・リランキング・クエリ拡張を実装し、検索精度を段階的に向上させる手法を理解する。4つの戦略を切り替えて比較実験できる構造を作る。

## ゴール（完了条件）

- 4つの strategy が動作する（`vector` / `hybrid` / `rerank` / `expand`）
- 回答に `Answer:` と `Sources:` セクションが含まれる
- 検索結果がない場合に「検索結果が見つかりませんでした」を返す
- `day05/data/` 内のドキュメントをインデックス化して検索できる

## データ準備

> **実行前に `day05/data/` に `.txt` または `.md` ファイルを配置してください。**

- 公開ドキュメントや自分で用意したテキストファイルを置く
- データ出典とライセンスを必ず README に記載すること

例：
```
day05/data/
├── langchain_docs.txt
├── bedrock_guide.md
└── rag_overview.txt
```

## 4つの戦略の説明

| strategy | 検索方法 | 特徴 |
|----------|---------|------|
| `vector` | FAISS ベクター検索のみ | 意味的類似度を重視 |
| `hybrid` | BM25 + ベクター検索を RRF で統合 | キーワード + 意味の両方に強い |
| `rerank` | hybrid に cross-encoder リランキングを追加 | 最終的な順序精度を向上 |
| `expand` | hybrid にクエリ拡張（HyDE / マルチクエリ）を追加 | 表現の揺れに強い |

## 機能要件

### コマンド

- `python -m day05.app` で起動できること

### 必須オプション

- `--question`：質問テキスト（文字列、必須）

### 任意オプション

- `--strategy`：`vector` / `hybrid` / `rerank` / `expand`（デフォルト: `hybrid`）
- `--data-dir`：ドキュメントディレクトリ（デフォルト: `day05/data`）
- `--top-k`：検索上位件数（1〜20、デフォルト: `5`）
- `--region`：AWSリージョン
- `--model-id`：BedrockのモデルID

### 出力フォーマット

```
Answer: <回答テキスト>

Sources:
- <ファイル名> (excerpt: "<抜粋テキスト")
- ...
```

### 終了コード

- 正常終了：`0`
- 入力不備（`--question` が空、`--top-k` 範囲外）：`2`
- 実行失敗：`1`

## 実装タスク

1. `data_dir` 内の `.txt` / `.md` を読み込んでチャンクに分割する
2. FAISS でベクターインデックスを作成する（Bedrock Embeddings を使用）
3. BM25 インデックスを作成する（`rank-bm25` を使用）
4. RRF（Reciprocal Rank Fusion）で BM25 + ベクター検索を統合する
5. cross-encoder でリランキングする（`sentence-transformers`）
6. HyDE またはマルチクエリでクエリ拡張する
7. 回答を `Answer: / Sources:` フォーマットで返す

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
# hybrid（デフォルト）
python -m day05.app --question "LangGraphとは何ですか？"

# vector のみ
python -m day05.app --question "RAGの仕組みを教えてください" --strategy vector

# リランキング追加
python -m day05.app --question "Bedrock のモデル一覧" --strategy rerank --top-k 10

# クエリ拡張追加
python -m day05.app --question "エージェントの設計パターン" --strategy expand
```

### 比較実験のやり方

同じ質問を strategy を変えて実行して回答品質と検索ソースを比較してください：

```bash
Q="LangGraphでサブグラフを使う利点は？"
python -m day05.app --question "$Q" --strategy vector
python -m day05.app --question "$Q" --strategy hybrid
python -m day05.app --question "$Q" --strategy rerank
python -m day05.app --question "$Q" --strategy expand
```

### 期待する出力例

```
Answer: LangGraph のサブグラフを使うと、複雑なフローを独立したモジュールに分割できます。

Sources:
- langchain_docs.txt (excerpt: "LangGraphはサブグラフを使ってネストされた状態機械を...")
- rag_overview.txt (excerpt: "グラフ構造により各エージェントの責務を明確に分離...")
```

---

**以下は受講者が記入してください**

## 提出物

- `day05/app.py`
- `day05/README.md`

## データ出典・ライセンス

- データ名：
- 出典 URL：
- ライセンス：
- ファイル一覧：

## セルフレビュー

- 正常系：4つの strategy すべてで回答と Sources が返る
- 異常系：データが空のとき「検索結果が見つかりませんでした」が返る
- 境界：`--top-k` が範囲外（0 や 21）で終了コード `2` が返る
- 再実行：同じ質問を2回実行して破綻しない

## 比較実験メモ

| strategy | 検索ヒット数 | 回答品質の所感 |
|----------|------------|-------------|
| vector | | |
| hybrid | | |
| rerank | | |
| expand | | |

## リサーチメモ（任意）

- FAISS の使い方と Bedrock Embeddings の組み合わせ
- rank-bm25 の BM25Okapi の使い方
- RRF（Reciprocal Rank Fusion）のアルゴリズム
- cross-encoder リランキングのモデル選択
- HyDE / マルチクエリによるクエリ拡張の手法
