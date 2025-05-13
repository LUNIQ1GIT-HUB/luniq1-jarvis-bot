import telebot
import json
import os
import datetime
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Bot-Token aus Umgebungsvariable (Render)
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Google Sheets Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = json.loads(os.environ["GOOGLE_CREDENTIALS_JSON"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
client = gspread.authorize(creds)

# Debug: Tabellenname
SPREADSHEET_NAME = "LUNIQ1_Memory_Main"  # Prüfen, ob der Name 100% so heißt!
sheet = client.open(SPREADSHEET_NAME).sheet1

# Testbefehl zur Überprüfung der Integration
@bot.message_handler(commands=['test'])
def handle_test(message):
    try:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row(["DEBUG-User", "TEST erfolgreich", now])
        bot.send_message(message.chat.id, "Testeintrag wurde erfolgreich in die Google Tabelle geschrieben.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Fehler beim Schreiben: {e}")
        print(f"Fehler beim Schreiben in Tabelle: {e}")

# Standardantwort + Logging
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        user = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
        text = message.text
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([user, text, now])
        bot.send_message(message.chat.id, "Nachricht empfangen und gespeichert.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Fehler beim Speichern: {e}")
        print(f"Fehler beim Speichern: {e}")

# Start
print("Bot wird gestartet...")
bot.polling()
