# server.py
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import json
from datetime import datetime

app = FastAPI()

# --- 静的ファイル設定 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = BASE_DIR  # index.htmlと同じディレクトリ
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

# --- ログ保存エンドポイント ---
@app.post("/save_log")
async def save_log(request: Request):
    try:
        data = await request.json()
        participant_id = data.get("participantId", "unknown")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{participant_id}_{timestamp}.json"
        filepath = os.path.join(LOG_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # ローカルのファイルパス（相対URLで返す）
        return JSONResponse({"url": f"logs/{filename}"})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# --- 起動 ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
