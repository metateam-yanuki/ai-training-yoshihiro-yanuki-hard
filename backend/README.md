# backend

このディレクトリは「課題ランナーAPI」（応用編）です。

- `POST /run` で `python -m <module> ...` を実行し、stdout/stderr/exit code を返します。
- UI（`ui/app.py`）がこのAPIを呼び出します。

## 起動方法

```bash
uvicorn backend.main:app --reload --port 8000
```

起動確認：

- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/docs`

## 注意事項

- `day03.server`（A2A サーバー）と `day06.server`（MCP サーバー）はブロッキングプロセスのため、Runner API 経由ではなく直接 CLI で起動してください。
- タイムアウトのデフォルトは 60 秒です（入門編より長め）。RAG や評価で時間がかかる場合は `timeout_sec` を延ばしてください。
