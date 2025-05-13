import telebot
import json
import os
import datetime
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Telegram Bot Token
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Debug-Nachrichten an Konsole
print("Starte Bot...")

# Google Sheets Setup
try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = json.loads(os.environ["GOOGLE_CREDENTIALS_JSON"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
    client = gspread.authorize(creds)
    print("Google Sheets erfolgreich autorisiert.")

    SPREADSHEET_NAME = "LUNIQ1_Memory_Main"  # 100 % korrekt?
    sheet = client.open(SPREADSHEET_NAME).sheet1
    print("Zugriff auf Tabelle erfolgreich.")

except Exception as e:
    print("Fehler beim Google Sheets Zugriff:")
    print(str(e))
    sheet = None

@bot.message_handler(commands=['test'])
def handle_test(message):
    if sheet:
        try:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet.append_row(["DEBUG-User", "TEST erfolgreich", now])
            bot.send_message(message.chat.id, "Test-Eintrag wurde erfolgreich in die Tabelle geschrieben.")
        except Exception as e:
            error_msg = f"Fehler beim Schreiben in Tabelle: {str(e)}"
            bot.send_message(message.chat.id, error_msg)
            print(error_msg)
    else:
        bot.send_message(message.chat.id, "Kein Zugriff auf die Google Tabelle.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if sheet:
        try:
            user = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
            text = message.text
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet.append_row([user, text, now])
            bot.send_message(message.chat.id, "Nachricht empfangen und gespeichert.")
        except Exception as e:
            error_msg = f"Fehler beim Speichern: {str(e)}"
            bot.send_message(message.chat.id, error_msg)
            print(error_msg)
    else:
        bot.send_message(message.chat.id, "Fehler: Tabelle konnte nicht geladen werden.")

bot.polling()
