# 研修要件（応用編）：入門編修了者向け / AWS Bedrock / 公開データRAG / 2.5〜3週間

## 1. 前提

- 受講者：入門編修了者（LangChain / LangGraph / AWS Bedrock / RAG の基礎を習得済み）
- LLM 基盤：AWS Bedrock（ローカル環境から SDK 経由でアクセス）
- 実行環境：ローカル（Windows / Mac）
- 社内ドキュメント：利用不可
- RAG を行う場合：公開データを用いる（出典/ライセンス確認を含む）
- 研修ゴール：マルチエージェント・A2A・MCP・高度 RAG・セキュリティ・評価改善サイクルを実務レベルで設計・実装できる

---

## 2. 研修の目的

- 入門編で習得した基礎の上に、複数エージェントが協調する高度なシステムを設計・実装できるようにする
- A2A・MCP という業界標準プロトコルを理解し、実際に実装して連携できるようにする
- セキュリティ・可観測性・コスト最適化を「後付け」でなく設計段階から組み込める観点を身につける
- 「動く」だけでなく「測れる・改善できる」評価サイクルを経験する

---

## 3. 到達目標

### 3.1 Must（必須到達）

- マルチエージェントを設計・実装できる
  - Supervisor / Handoff / 階層型パターンを説明できる
  - LangGraph のサブグラフ・状態スコープを適切に設計できる
- A2A を使ってエージェント間を連携できる
  - AgentCard・Task・TaskState の構造を説明できる
  - A2A サーバーとクライアントを別プロセスで動かせる
- MCP でツール・データソースを標準化できる
  - Tools・Resources の違いを説明できる
  - MCP サーバーを実装してエージェントから呼び出せる
- メモリを設計・実装できる
  - 短期・長期・エピソード記憶の使い分けを説明できる
  - セッションをまたいで文脈が保持されることを確認できる
- 高度 RAG を実装できる
  - ハイブリッド検索・リランキング・クエリ拡張の仕組みを説明できる
  - 入門編の単純検索と品質を比較できる
- Human-in-the-Loop を実装できる
  - 中断・再開・承認拒否の各パスが正しく動作する
- セキュリティを考慮した実装ができる
  - プロンプトインジェクション検知・PII マスク・許可リスト検証を実装できる
- 評価指標を定義・計測・改善できる
  - Faithfulness・Answer Relevance・タスク達成率を LLM-as-a-Judge で計測できる
  - 失敗を 4 分類し、改善前後のスコアを比較できる

### 3.2 Should（できると良い）

- 構造化ログ・コールバックで障害調査できる
- Bedrock のキャッシュ・ストリーミング・バッチ並列処理でコストとレイテンシを最適化できる
- 最終課題でA2A・MCP・HITL・メモリ・RAG・セキュリティ・評価をすべて統合できる

---

## 4. 成果物（Deliverables）

- 日次課題（必須）
  - Day01〜Day12：動くコード + README（実行方法・セルフレビュー結果）
  - Day11：評価結果 CSV
  - Day12：改善前後の比較レポート
- 最終課題（必須）
  - マルチエージェント統合システム（`final/agent.py`）
  - Streamlit チャット UI（`final/chat_ui.py`）
  - README（起動手順・仕上げ要件チェックリスト）
  - 設計メモ（`docs/`：状態遷移図・主要プロンプト・評価結果）

---

## 5. GitHub 運用要件

`github-operation.md` を参照してください。

---

## 6. AWS Bedrock 前提の要件

### 6.1 認証・権限

運営は以下のいずれかの認証方式を事前に決定し、受講者に周知します。

#### A) IAM ユーザー（アクセスキー）

**手順1：アクセスキーの発行（運営が実施）**

1. AWS Console > **IAM** > **ユーザー** > 対象ユーザーを選択
2. **セキュリティ認証情報** タブ > **アクセスキーを作成**
3. `Access Key ID`（`AKIA...`）と `Secret Access Key` を控える

> Secret Access Key は作成時にしか表示されないため、必ずこの時点で保存すること

**手順2：ローカル PC に認証情報を設定（受講者が実施）**

```bash
aws configure --profile training
# 以下を対話形式で入力：
#   AWS Access Key ID: AKIA...
#   AWS Secret Access Key: xxxxxxxx
#   Default region name: ap-northeast-1
#   Default output format: json
```

**手順3：プロファイルの有効化**

```bash
# Mac / Linux
export AWS_PROFILE=training

# Windows（PowerShell）
$env:AWS_PROFILE = "training"
```

**手順4：動作確認**

```bash
aws sts get-caller-identity
aws bedrock list-foundation-models --region ap-northeast-1 --query "modelSummaries[].modelId" --output table
```

#### B) IAM Identity Center（SSO）

```bash
aws configure sso --profile training
aws sso login --profile training
export AWS_PROFILE=training
```

#### C) AssumeRole

```bash
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/BedrockTrainingRole \
  --role-session-name training-session
export AWS_ACCESS_KEY_ID=<AccessKeyId>
export AWS_SECRET_ACCESS_KEY=<SecretAccessKey>
export AWS_SESSION_TOKEN=<SessionToken>
```

#### 最小権限 IAM ポリシー例

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "BedrockInvoke",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:ap-northeast-1::foundation-model/*"
    },
    {
      "Sid": "BedrockListModels",
      "Effect": "Allow",
      "Action": ["bedrock:ListFoundationModels"],
      "Resource": "*"
    }
  ]
}
```

### 6.2 モデル選定

全 Day 共通で以下の 1 モデルに統一する。

| モデルID | ステータス | EOL 予定 |
|---------|----------|---------|
| `anthropic.claude-haiku-4-5-20251001-v1:0` | Active | 2026年10月1日以降 |

Claude Haiku 4.5 は Claude 4 シリーズの最安価モデルで、応用編の課題水準に対して十分な品質を持つ。
LLM-as-a-Judge（Day11/12）は繰り返し呼び出しが多いため、安価なモデルへの統一でコストを抑えられる。

**⚠️ Claude 3.5 Haiku（旧モデル）は使用しないこと**
`anthropic.claude-3-5-haiku-20241022-v1:0` は 2026年6月19日に Bedrock から完全廃止予定。

**研修開始前に運営側で利用可否を確認すること：**

```bash
aws bedrock list-foundation-models \
  --region ap-northeast-1 \
  --by-provider Anthropic \
  --query "modelSummaries[?contains(modelId, 'haiku-4')].{id:modelId, status:modelLifecycle.status}" \
  --output table
```

### 6.3 コスト管理

**Claude Haiku 4.5 料金（us-east-1 基準）**
- Input: $1.00 / 1M tokens
- Output: $5.00 / 1M tokens

**1人あたりの予算と上限**

| 区分 | 目安 |
|------|------|
| 総額（13日合計） | $15〜20 / 人 |
| 日次ソフトリミット | $1.50 / 日 |
| Day11・12 の日次上限 | $2.00 / 日（評価スクリプトで呼び出しが多い） |
| テストスイート件数（Day11・12） | 15 件以内 |
| バッチサイズ（Day10） | `--batch-size 5` 以下を推奨 |

**コスト増加を防ぐルール（受講者向け）**
- `suite.json` のテストケースは 15 件以内にする
- Day12 の `--apply-fix` オプションは 1 日 1〜2 回を目安にする
- Day04 の会話履歴は 10 ターンを超えたらリセットする
- バッチ処理（Day10）は `--batch-size 5` 以下で動作確認する
- 無限ループ・極端に長いプロンプトは禁止
- ログにトークン数・呼び出し回数を残してコストを把握する

### 6.4 安全設計

- ツール実行は許可リストで制限する（Day09 で実装）
- PII・機密情報を入力・ログに残さない（Day09 で実装）
- プロンプトインジェクション対策を最低限実施する（Day09 で実装）
- A2A サーバー・MCP サーバーはローカルのみで起動する（外部公開しない）

---

## 7. 評価基準（Rubric の骨子）

`rubric.md` を参照してください。

---

## 8. 公開データ RAG の方針

- データ条件
  - ライセンスが明確
  - 文書構造が扱いやすい（.txt / .md / PDF 等）
  - 参照元 URL を提示できる
- 候補例
  - 公開ドキュメント（政府統計の解説、自治体公開資料、製品マニュアル、OSS ドキュメント等）
  - Wikipedia 等は可否判断が必要（方針次第）
- `day05/data/` に配置するファイルは受講者が各自準備する
  - ファイルは `.gitignore` に入っているため、README に「どのファイルを使ったか」を明記すること
