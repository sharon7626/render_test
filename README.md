# FastAPI Hello API

一個可部署至 Render 的最小 FastAPI 專案。

## 本機執行

### Windows PowerShell

第一次建立環境時執行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

成功啟用後，PowerShell 提示字元前方會顯示 `(.venv)`。本專案已包含 `.venv`，而且 VS Code 已設定成開啟新終端機時自動啟用。

也可以在 VS Code 使用以下方式啟動：

- 按 `Ctrl+Shift+P`，選擇 `Tasks: Run Task`，再選擇 `FastAPI: 啟動開發伺服器`。
- 開啟「執行與偵錯」，選擇 `FastAPI: Uvicorn`，再按 `F5`。

開啟 `http://127.0.0.1:8000/`，回應如下：

```json
{"message":"Hello"}
```

互動式 API 文件位於 `http://127.0.0.1:8000/docs`。

健康檢查端點位於 `http://127.0.0.1:8000/health`，回應如下：

```json
{"status":"ok"}
```

## 部署至 Render

1. 將此專案推送至 GitHub、GitLab 或 Bitbucket。
2. 在 Render 建立 **Blueprint**，並連結該儲存庫。
3. Render 會讀取根目錄的 `render.yaml` 並建立 Web Service。

若改用 Render Dashboard 手動建立 Web Service，請設定：

- Build Command：`pip install -r requirements.txt`
- Start Command：`uvicorn main:app --host 0.0.0.0 --port $PORT`
