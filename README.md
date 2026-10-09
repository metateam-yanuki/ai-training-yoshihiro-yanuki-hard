# 若手AIエンジニア研修（応用編）

入門編（Day01〜Day10）修了者向けの応用カリキュラムです。LangChain / LangGraph / Bedrock / RAG の基礎を習得済みであることを前提とします。

## 前提条件

| ツール | バージョン | 備考 |
|--------|-----------|------|
| Python | 3.10 以上 | `python3 --version`（Windows: `python --version`）で確認 |
| Git | 2.x | `git --version` で確認 |
| AWS CLI | v2 | `aws --version` で確認。認証設定は `training-requirements.md` 参照 |
| day05/data/ | — | Day05 以降は `day05/data/` に公開ドキュメント（.txt / .md）を配置すること |

## Quickstart（最短導線）

受講者は基本的に「その日の `README` を読む → `app.py` を編集する → 画面 or CLIで動作確認 → PR提出」の繰り返しです。

### 1) 今日やるDayを決める

- `day01/README.md` 〜 `day13/README.md` のいずれかを開きます

### 2) 編集するファイルは原則この2つだけ

- **実装**：`dayXX/app.py`（または `server.py`）
- **提出用メモ**：`dayXX/README.md`

### 3) 動作確認（おすすめ：共通画面）

0. `.env.example` を `.env` にコピーして値を設定
   - `.env` はコミットしません

1. venvを作成・有効化（初回のみ）
   - `python3 -m venv .venv`（Windows: `python -m venv .venv`）
   - `source .venv/bin/activate`（Windows: `.venv\Scripts\activate`）
   - `pip install -U pip`

2. 依存関係をインストール
   - `pip install -r requirements.txt`

3. Runner APIを起動
   - `uvicorn backend.main:app --reload --port 8000`

4. 共通画面を起動
   - `streamlit run ui/app.py`

5. メニューからDayを選んで入力→実行

### 4) Day03 / Day06 はターミナルが2つ必要

> **Day03（A2A）と Day06（MCP）はサーバープロセスが必要です。**

- **Day03**
  - ターミナル1：`python -m day03.server --port 8100`
  - ターミナル2：`python -m day03 --task "..." --server-url http://127.0.0.1:8100`

- **Day06**
  - ターミナル1：`python -m day06.server --port 8200`
  - ターミナル2：`python -m day06.app --query "..." --server-url http://127.0.0.1:8200`

### 5) 代替：CLIで直接動作確認

```bash
# 例（Day01）
python -m day01.app --query "LangGraph の特徴を調査して要約してください" --verbose
```

---

## ドキュメント

- `training-requirements.md`：研修要件
- `curriculum.md`：カリキュラム
- `assignments.md`：課題一覧
- `self-review-checklist.md`：セルフレビュー
- `rubric.md`：採点ルーブリック

---

## 共通画面（UI） + 課題ランナー（FastAPI）

このテンプレートには、各Day課題のCLIを共通画面から実行して、結果（stdout/stderr/exit code）を確認できるフレームが含まれます。

### 1. 依存関係の導入

- venvを作成・有効化（初回のみ）
  - `python3 -m venv .venv`（Windows: `python -m venv .venv`）
  - `source .venv/bin/activate`（Windows: `.venv\Scripts\activate`）
  - `pip install -U pip`
- 依存関係をインストール
  - `pip install -r requirements.txt`

### 2. Runner API（FastAPI）起動

- `uvicorn backend.main:app --reload --port 8000`

起動確認：

- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/docs`

### 3. 共通画面（Streamlit）起動

- `streamlit run ui/app.py`

### 4. 最終課題のチャットUI

> Day03（A2A）と Day06（MCP）のサーバーを先に起動してください。

- `streamlit run final/chat_ui.py`

---

## 受講者が実装する場所

各Dayの課題は、`python -m dayXX.app` のCLIとして実装します。

| Day | 実装ファイル | 実装関数 |
|-----|------------|---------|
| 01 | `day01/app.py` | `run_multi_agent()` |
| 02 | `day02/app.py` | `run_graph()` |
| 03 | `day03/server.py`, `day03/app.py` | `serve()`, `call_agent()` |
| 04 | `day04/app.py` | `run_chat()` |
| 05 | `day05/app.py` | `answer_with_advanced_rag()` |
| 06 | `day06/server.py`, `day06/app.py` | `serve()`, `run_with_mcp()` |
| 07 | `day07/app.py` | `run_with_hitl()` |
| 08 | `day08/app.py` | `run_with_logging()` |
| 09 | `day09/app.py` | `run_secure()` |
| 10 | `day10/app.py` | `run_optimized()` |
| 11 | `day11/app.py` | `load_suite()`, `run_evaluation()` |
| 12 | `day12/app.py` | `run_improvement_cycle()` |
| 13 | `final/agent.py` | `run_agent()` |

---

## パッケージ別セットアップ注意点

### faiss-cpu（Day05）

`pip install faiss-cpu` で Mac（Intel / Apple Silicon）・Windows ともにインストール可能です。  
インストールに失敗する場合は ChromaDB を代替として使用してください。

```bash
pip install chromadb  # faiss-cpu の代替
```

### sentence-transformers（Day05 リランキング）

**初回実行時にクロスエンコーダーモデル（約 400MB）を自動ダウンロードします。**
- インターネット接続が必要です
- ダウンロードは初回のみ（以降はキャッシュを使用）
- ダウンロード先：`~/.cache/huggingface/`（Mac/Linux）または `C:\Users\<ユーザー名>\.cache\huggingface\`（Windows）

### langgraph-checkpoint-sqlite（Day04・Day07）

SQLite を使ったメモリ永続化・HITL のチェックポイントに必要です。  
`pip install -r requirements.txt` で自動的にインストールされます。  
生成される `.db` ファイルは `.gitignore` に含まれているためコミットされません。

### A2A サーバー・MCP サーバー（Day03・Day06）

`.env` の `A2A_SERVER_URL` / `MCP_SERVER_URL` はデフォルト値のままで動作します。  
ポートが競合する場合は `--port` オプションで変更してください。

---

## よくある詰まりポイント

- Runner APIを起動していない
  - `uvicorn backend.main:app --reload --port 8000` を起動してください
- 共通画面がRunner APIに繋がらない
  - `ui/app.py` の左メニュー `Runner API base URL` が `http://127.0.0.1:8000` になっているか確認してください
- Dayを実装していないのに共通画面から実行した
  - `NotImplementedError` が出ます。`dayXX/app.py` の未実装関数（docstring付き）を埋めてください
- Day03/Day06 でサーバーに繋がらない
  - サーバーを別ターミナルで起動しているか確認してください
- Day05 で「検索結果が見つかりませんでした」と出る
  - `day05/data/` にドキュメントファイルを配置してください
- Day05 初回実行が遅い（リランキング使用時）
  - sentence-transformers のモデルダウンロード中です（約 400MB）。完了まで数分かかります
- faiss-cpu がインストールできない
  - `pip install chromadb` を代替として使用し、実装を ChromaDB ベースに切り替えてください
- Day04・Day07 で `SqliteSaver` が見つからない
  - `pip install langgraph-checkpoint-sqlite aiosqlite` を実行してください
