import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from telegram import Bot
import asyncio

app = FastAPI()

# Konfigurasi CORS agar bisa diakses dari domain website manapun
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# KREDENSIAL YANG KAMU BERIKAN
BOT_TOKEN = "8405081792:AAF6LEGqcUWv02vuhZ5cohQAefs0moBg5rg"
CHANNEL_ID = -1003496635135 

bot = Bot(token=BOT_TOKEN)

@app.get("/api/novus-member")
async def get_member_count():
    try:
        # Mengambil jumlah member secara real-time langsung ke Telegram
        count = await bot.get_chat_member_count(CHANNEL_ID)
        
        return {
            "status": "success",
            "member_count": count
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    # Menjalankan di port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
