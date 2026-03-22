from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import uvicorn

# Inisialisasi FastAPI
app = FastAPI()

# Konfigurasi CORS agar website bisa mengakses API dari domain/IP berbeda
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Konfigurasi Bot Telegram Novus Society
BOT_TOKEN = "8405081792:AAF6LEGqcUWv02vuhZ5cohQAefs0moBg5rg"
CHANNEL_ID = "-1003496635135"

@app.get("/member-count")
def get_member_count():
    """Mengambil jumlah member langsung dari Telegram API"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMemberCount?chat_id={CHANNEL_ID}"
    try:
        response = requests.get(url, timeout=10).json()
        if response.get("ok"):
            return {"count": response["result"]}
        return {"count": "N/A", "error": response.get("description")}
    except Exception as e:
        return {"count": "Offline", "error": str(e)}

if __name__ == "__main__":
    # Menjalankan server di port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
