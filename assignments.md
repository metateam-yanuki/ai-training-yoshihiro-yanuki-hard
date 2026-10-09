# 実装課題一覧（Day01〜Day13 + 最終課題）

この研修は講義なしで進めます。各Dayは次の流れで実施してください。

- リサーチ（各自で調べる）
- 実装
- セルフレビュー（`self-review-checklist.md`）
- PR提出（`github-operation.md`）

---

## 共通ルール（全課題）

- PR提出前に `self-review-checklist.md` を確認する
- 実行手順は各DayのREADMEに必ず書く
- 秘密情報（APIキー、AWS認証情報など）をコミットしない

---

# Day 01：マルチエージェント基礎（Supervisor / Handoff）

## 課題

- LangGraph で Supervisor + Worker × 2 のマルチエージェントを実装する
  - Supervisor が入力に応じて research / summarize Worker に振り分ける
  - State に research_result / summary / final_answer を積み上げる
- `--verbose` で各ノードの動作ログを確認できるようにする

## 提出物

- `day01/app.py`
- `day01/README.md`（実行手順、実装したノード構成、確認した入力例）

## 完了条件

- Supervisor の Handoff が動作する
- verbose 時に各ノードの入出力が確認できる
- 出力フォーマット（[Research] / [Summary] セクション）が守られている

---

# Day 02：LangGraph 応用（サブグラフ・ストリーミング）

## 課題

- Day01 のフローをサブグラフに分割する
  - research サブグラフと summarize サブグラフを独立した State で定義する
- `--stream` でノード別の中間経過を確認できるようにする

## 提出物

- `day02/app.py`
- `day02/README.md`（サブグラフ設計、ストリーミング確認手順）

## 完了条件

- サブグラフが独立してテスト可能な構造になっている
- ストリーミングモードでノード別ログが表示される

---

# Day 03：A2A（Agent-to-Agent Protocol）

## 課題

- Day01 の summarize Worker を A2A サーバーとして公開する
  - AgentCard に name / description / capabilities を記述する
  - Task を受け取って Bedrock で要約し、TaskState.completed で返す
- A2A クライアントを実装して別プロセスから呼び出す

## 提出物

- `day03/server.py`
- `day03/app.py`
- `day03/README.md`（起動手順・ターミナル2つの使い方、確認した入力例）

## 完了条件

- AgentCard に capabilities が記述されている
- 別プロセスでサーバー・クライアントが通信できる

---

# Day 04：メモリ設計（短期・長期・エピソード記憶）

## 課題

- 3種類のメモリを実装する
  - short: MemorySaver（スレッド内のみ）
  - long: SqliteSaver（セッションをまたいで永続）
  - episode: long + 10ターン超えでサマリ圧縮
- thread_id で会話を分離する

## 提出物

- `day04/app.py`
- `day04/README.md`（3種類の違い、セッションをまたいだ確認手順）

## 完了条件

- long / episode でセッションをまたいで前の情報を参照できる
- episode でサマリ圧縮が機能する

---

# Day 05：高度 RAG（ハイブリッド検索・リランキング・クエリ拡張）

## 課題

- `day05/data/` に公開ドキュメントを配置してインデックス化する
- 4つの検索戦略を実装する
  - vector: FAISS ベクター検索のみ
  - hybrid: BM25 + ベクター検索（RRF）
  - rerank: hybrid + cross-encoder リランキング
  - expand: hybrid + クエリ拡張（HyDE / マルチクエリ）
- `Answer: / Sources:` フォーマットで出力する

## 提出物

- `day05/app.py`
- `day05/README.md`（データ出典・ライセンス、4戦略の比較実験結果）

## 完了条件

- 4つの strategy が動作する
- 検索ヒットなしのとき「検索結果が見つかりませんでした」を返す
- データ出典・ライセンスが README に明記されている

---

# Day 06：MCP（Model Context Protocol）

## 課題

- Day05 の RAG 検索を MCP サーバーの Tool として公開する
  - search(query, top_k) ツールを定義する
  - documents://list リソースを定義する
- MCP クライアントからエージェントを実行する

## 提出物

- `day06/server.py`
- `day06/app.py`
- `day06/README.md`（起動手順・ターミナル2つの使い方）

## 完了条件

- MCP サーバーの search ツールが呼び出せる
- エージェント側のコードを変えずにサーバーを差し替えられる構成になっている

---

# Day 07：Human-in-the-Loop（承認フロー・中断・再開）

## 課題

- LangGraph の interrupt() でツール実行前に承認を求める
- "n" のとき「承認されなかったため処理を中止しました」を返す
- SqliteSaver でチェックポイントを永続化し、中断後に再開できるようにする

## 提出物

- `day07/app.py`
- `day07/README.md`（承認フロー・中断・再開の動作確認手順）

## 完了条件

- 承認 / 中止 の両パスが動作する
- 同じ thread_id で再実行すると続きから再開できる

---

# Day 08：可観測性・ログ設計（構造化ログ・コールバック）

## 課題

- BaseCallbackHandler を継承したカスタムコールバックを実装する
  - 記録：timestamp / event / node_name or tool_name / input / output / duration_ms
- JSON Lines 形式でログを出力する
- Day01 のマルチエージェントに組み込む

## 提出物

- `day08/app.py`
- `day08/README.md`（JSON Lines フォーマット例・jq での絞り込みコマンド例）

## 完了条件

- 実行後にログファイルが JSON Lines 形式で生成される
- jq で特定イベントを絞り込める

---

# Day 09：セキュリティ強化（インジェクション対策・PII）

## 課題

- プロンプトインジェクション検知（日本語・英語パターン）
- PII マスク（メールアドレス → [EMAIL]、電話番号 → [PHONE]）
- ツール引数の文字数制限
- `--mode attack` でケース1〜3が正しくブロック・マスクされることを確認する

## 提出物

- `day09/app.py`
- `day09/README.md`（攻撃パターン3件の説明と対策の対応表）

## 完了条件

- インジェクション攻撃（Case 1, 2）がブロックされる
- PII（Case 3）が入力・出力の両方でマスクされる

---

# Day 10：パフォーマンス・コスト最適化

## 課題

- セマンティックキャッシュ（FAISS + Bedrock Embeddings）
  - 2回目以降に "CACHE HIT" を表示する
- ストリーミング TTFT 計測
  - 末尾に "TTFT: XXX ms" を付ける
- バッチ並列実行（asyncio.gather）
  - 直列実行との時間比較を末尾に追加する

## 提出物

- `day10/app.py`
- `day10/README.md`（キャッシュあり/なし・直列/並列の比較表テンプレートと実測値）

## 完了条件

- 3つのモードが動作する
- 数値で最適化効果を確認できる

---

# Day 11：評価指標の理解と計測

## 課題

- `day11/suite.json` の6ケースを実行する
  - RAG ケース：Faithfulness / Answer Relevance を LLM-as-a-Judge で評価
  - エージェントケース：タスク達成率 / ステップ数を計測
- 結果を `day11/results/eval_result.json` に保存する

## 提出物

- `day11/app.py`
- `day11/results/eval_result.json`（評価結果）
- `day11/README.md`（LLM-as-a-Judge のプロンプト設計・4指標の定義）

## 完了条件

- サマリに4指標のスコアが含まれる
- `day11/results/eval_result.json` が保存される

---

# Day 12：失敗分析と改善サイクル

## 課題

- Day11 の評価結果から失敗ケースを4分類に振り分ける
- `--apply-fix` で最多失敗種別に改善を適用して再評価する
- 回帰テスト：前回 passed が今回 failed になったケースを警告ログに出す

## 提出物

- `day12/app.py`
- `day12/results/improved_result.json`（改善後の評価結果）
- `day12/README.md`（3ステップ手順・改善前後の比較）

## 完了条件

- 改善前後のスコア比較が出力される
- 回帰が検出された場合に警告ログが出る

---

# Day 13：最終課題（統合）

## 課題

- `final/agent.py` の `run_agent()` を実装する
- Day13 から動作確認できること

## 提出物

- `final/agent.py`
- `final/README.md`（仕上げ要件チェックリスト・起動手順・設計メモ）
- `docs/`（状態遷移図・主要プロンプト・評価結果）

## 完了条件

- 仕上げ要件8項目すべてを満たしている
- `streamlit run final/chat_ui.py` でチャットUIが動作する

---

# 最終課題：統合マルチエージェント

## 概要

応用編全体の技術を統合したマルチエージェントを実装します。

## 必須要件（8項目）

1. LangGraph でマルチエージェント構成（Supervisor + Worker × 2 以上）
2. A2A で少なくとも 1 つのエージェントを外部サービスとして公開・呼び出し
3. MCP サーバー経由でツールまたはデータソースを接続
4. 高度 RAG（ハイブリッド検索またはリランキング）
5. Human-in-the-Loop（少なくとも 1 箇所の承認ポイント）
6. メモリ設計（会話をまたいだ文脈保持）
7. 構造化ログ・コールバック（Day08 の実装を組み込む）
8. セキュリティ（入力バリデーション・PII マスク）

## 提出物

- `final/README.md`（セットアップ、実行、設計メモ）
- `docs/`（状態遷移図、主要プロンプト、評価結果、改善ログ）
