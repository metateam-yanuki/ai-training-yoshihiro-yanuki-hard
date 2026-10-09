# Day 12 — 失敗分析と改善サイクル

## 受講者が実装する場所

- `day12/app.py` の `run_improvement_cycle()`

## 目的

Day11 の評価結果を起点に、失敗の原因を分類・分析し、改善を適用して再評価するサイクルを実装する。「分析 → 改善 → 再評価 → 回帰確認」の PDCA サイクルをエージェントに組み込む手法を習得する。

## ゴール（完了条件）

- Day11 の評価結果から失敗ケースを抽出して4分類に振り分けられる
- `--apply-fix` なしで失敗分類の集計と改善案が返る
- `--apply-fix` ありで最も多い失敗種別に改善を適用して再評価できる
- 回帰（前回 passed が今回 failed になった場合）が検出されてログに警告が出る

## 失敗分類タクソノミー

`day12/failure_taxonomy.md` を参照してください。

| 分類 | 説明 | 改善案の例 |
|------|------|----------|
| 検索ミス | 正しいドキュメントが検索されなかった | strategy を `rerank` に変更 |
| 推論ミス | 検索結果はあるが LLM が誤った推論をした | プロンプトに根拠提示を強制する文言を追加 |
| 構造化失敗 | JSON 出力が壊れた・必須キーが欠損 | バリデーションとリトライを追加 |
| ツール呼び出しミス | 必要なツールが呼ばれなかった | Supervisor のプロンプトを修正 |

## 3ステップ手順

### ステップ 1：分析フェーズ（--apply-fix なし）

```bash
python -m day12.app --result day11/results/eval_result.json
```

- 失敗ケースを4分類に振り分けてカウントする
- 最も多い失敗種別と改善案を JSON で出力する（再評価はしない）
- 出力を見て「どの失敗が多いか」を把握する

### ステップ 2：改善フェーズ（--apply-fix あり）

```bash
python -m day12.app --result day11/results/eval_result.json --apply-fix --output day12/results/improved_result.json
```

- 最も多い失敗種別に改善を1つ適用する
- Day11 と同じテストスイートで再評価する
- 改善前後のスコアを比較する

### ステップ 3：回帰テスト確認

改善適用後のログを確認して、前回 passed が今回 failed になったケース（回帰）がないか確認する。

```bash
# 改善後の結果を確認
cat day12/results/improved_result.json | jq '.regressions'
```

## 機能要件

### コマンド

- `python -m day12.app` で起動できること

### 任意オプション

- `--result`：Day11 の評価結果 JSON（デフォルト: `day11/results/eval_result.json`）
- `--output`：改善後の評価結果の保存先（デフォルト: `day12/results/improved_result.json`）
- `--apply-fix`：改善を適用して再評価する（フラグ）
- `--region`：AWSリージョン
- `--model-id`：BedrockのモデルID

### 出力フォーマット

```json
{
  "failure_analysis": {
    "検索ミス": 2,
    "推論ミス": 1,
    "構造化失敗": 0,
    "ツール呼び出しミス": 1,
    "most_common": "検索ミス",
    "improvement_plan": "strategy を rerank に変更して再評価します"
  },
  "before": {"total": 6, "rag_faithfulness_avg": 0.70, "agent_task_success_rate": 0.67},
  "after": {"total": 6, "rag_faithfulness_avg": 0.85, "agent_task_success_rate": 0.83},
  "regressions": []
}
```

### 終了コード

- 正常終了：`0`
- 評価結果ファイルが見つからない：`2`
- 実行失敗：`1`

## 実装タスク

1. `result_path` の評価結果を読み込んで失敗ケースを抽出する
2. 各失敗ケースを4分類に振り分ける（ルールベースでよい）
3. `apply_fix=False` のとき：失敗分類の集計と改善案を返す
4. `apply_fix=True` のとき：
   - 最多失敗種別を特定する
   - 対応する改善を適用する（例：検索ミス → strategy=rerank）
   - Day11 と同じスイートで再評価する
   - 改善前後のスコアを比較する
5. 回帰テスト：前回 passed が今回 failed になったケースを警告ログに出す

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
# ステップ 1: 分析のみ（再評価なし）
python -m day12.app --result day11/results/eval_result.json

# ステップ 2: 改善を適用して再評価
python -m day12.app --result day11/results/eval_result.json --apply-fix

# 改善後の結果を確認
cat day12/results/improved_result.json | jq '.failure_analysis, .before, .after'
```

---

**以下は受講者が記入してください**

## 提出物

- `day12/app.py`
- `day12/results/improved_result.json`（改善後の評価結果）
- `day12/README.md`

## セルフレビュー

- 正常系（分析のみ）：失敗分類の集計と改善案が JSON で返る
- 正常系（改善適用）：改善前後のスコア比較が返る
- 異常系：`--result` ファイルが存在しないとき終了コード `2` が返る
- 回帰確認：regressions が空なら回帰なし

## 改善サイクルメモ

- 特定した最多失敗種別：
- 適用した改善内容：
- 改善前後のスコア変化：

| 指標 | 改善前 | 改善後 | 変化 |
|------|-------|-------|------|
| rag_faithfulness_avg | | | |
| rag_relevance_avg | | | |
| agent_task_success_rate | | | |

## リサーチメモ（任意）

- 失敗分析のアプローチ（ルールベース vs LLM による分類）
- 回帰テストの設計指針
- 改善サイクルの自動化方法
