import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from telegram import Bot
from telegram.error import TelegramError

# --- KONFIGURASI LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("api_access.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Novus Society API", version="2.0")

# --- KONFIGURASI CORS (Keamanan Browser) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Kamu bisa mengganti "*" dengan ["https://novus.web.id"] agar lebih aman
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# --- DATA TELEGRAM ---
BOT_TOKEN = "8405081792:AAF6LEGqcUWv02vuhZ5cohQAefs0moBg5rg"
CHANNEL_ID = -1003496635135 

# Inisialisasi Bot
bot = Bot(token=BOT_TOKEN)

@app.get("/")
async def root():
    return {"message": "Novus Society API is running", "status": "online"}

@app.get("/api/novus-member")
async def get_member_count():
    try:
        # Mengambil jumlah member dari Telegram
        count = await bot.get_chat_member_count(CHANNEL_ID)
        logger.info(f"Berhasil mengambil data: {count} member.")
        
        return {
            "status": "success",
            "member_count": count,
            "community": "Novus Society",
            "version": "2.0"
        }
    except TelegramError as te:
        logger.error(f"Telegram API Error: {te}")
        return {"status": "error", "message": "Gagal terhubung ke Telegram"}
    except Exception as e:
        logger.error(f"System Error: {e}")
        return {"status": "error", "message": "Terjadi kesalahan internal"}

if __name__ == "__main__":
    logger.info("Memulai server Novus API di port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
