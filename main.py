import os
import json
import logging
import datetime
import gspread
from google.oauth2.service_account import Credentials
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# === Logging aktivieren ===
logging.basicConfig(level=logging.INFO)

# === Telegram Bot Token & Google Sheets Setup ===
BOT_TOKEN = os.environ["BOT_TOKEN"]
SPREADSHEET_ID = "14d4S1lpXz_vEZa8BnAwISzAjiWia6XmCH4T9KcxOsBo"
SHEET_NAME = "LUNIQ1_Memory_Main"

# === Google Credentials aus Umgebungsvariable laden ===
google_creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS_JSON"])
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(google_creds_dict, scopes=scopes)
gc = gspread.authorize(credentials)
worksheet = gc.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# === Telegram Bot Setup ===
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# === Nachrichtenbehandlung ===
@dp.message_handler()
async def handle_message(message: types.Message):
    try:
        now = datetime.datetime.now()
        data = [
            now.strftime("%d.%m.%Y"),         # A: Datum
            now.strftime("%H:%M:%S"),         # B: Zeit
            message.from_user.full_name,      # C: Sender
            message.text,                     # D: Inhalt
            "",                               # E: Reaktion
            "",                               # F: Kategorie
            ""                                # G: Gültig bis
        ]
        worksheet.append_row(data)
        await message.reply("✅ Gespeichert.")
    except Exception as e:
        logging.error(f"Fehler beim Speichern in Google Sheets: {e}")
        await message.reply("❌ Fehler beim Speichern.")

# === Bot starten ===
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
