import logging
import gspread
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from oauth2client.service_account import ServiceAccountCredentials

# Deine Tokens und Sheet-Daten
TELEGRAM_TOKEN = "7698215127:AAEVW49Bpwaj5JwKqRjawI5u2IS3HTHsqoQ"
SPREADSHEET_ID = "14d4S1lpXz_vEZa8BnAwISzAjiWia6XmCH4T9KcxOsBo"
SHEET_NAME = "LUNIQ1_Memory_Main"

# Logging
logging.basicConfig(level=logging.INFO)

# Telegram Bot Setup
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Google Sheets Verbindung
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("luniq1-botsystem-d7d1e926a489.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

@dp.message_handler()
async def handle_message(message: types.Message):
    now = datetime.now()
    row = [
        now.strftime("%d.%m.%Y"),  # Datum
        now.strftime("%H:%M:%S"),  # Uhrzeit
        message.from_user.full_name,  # Sender
        message.text,  # Inhalt
        "",  # Reaktion
        "",  # Kategorie
        ""   # Gültig bis
    ]
    sheet.append_row(row)
    await message.reply("Nachricht gespeichert!")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
