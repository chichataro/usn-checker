from flask import Flask
from threading import Thread
from telethon.sync import TelegramClient
from telethon.errors import UsernameNotOccupiedError
import requests
import time
import os
from keep_alive import keep_alive
keep_alive()

# Flask app for UptimeRobot pings
app = Flask('')

@app.route('/')
def home():
    return "Bot is running"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

# Telegram credentials (from environment variables)
api_id = int(os.environ.get('25750063'))
api_hash = os.environ.get('c9d0b539efac21fca5a0c8ae9d6bf1cc')
bot_token = os.environ.get('8089857633:AAGG9yJ5qR1LLk6qkFWr48LVsR9VOCQ9D-M') 
chat_id = os.environ.get('7206931841')

# Usernames to check
usernames_to_check = [
    'xaveir', 'xavierr', 'zcaleb', 'ayyel', 'xinghui', 'zhengshuyi',
    'ermanno', 'maabel', 'citlalii', 'seyii', 'calieb', 'caileb',
    'caleba', 'calebl', 'calebn', 'lxavier', 'cxavier'
]

# Function to send messages to Telegram
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("Telegram message sent successfully!")
        else:
            print(f"Failed to send Telegram message. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending Telegram message: {str(e)}")

# Start
print("Starting username checker bot...")
send_telegram_message("🤖 Username checker bot started!")

with TelegramClient('session_name', api_id, api_hash) as client:
    while True:
        try:
            current_time = time.strftime("%H:%M:%S")
            print(f"\n[{current_time}] Starting new check cycle...")

            for username in usernames_to_check:
                try:
                    entity = client.get_entity(username)
                    if entity:
                        print(f"Checking @{username} - Still taken")

                except (UsernameNotOccupiedError, ValueError):
                    message = f"🎉 GO GO claim @{username}! 🏃🏻‍♀️"
                    print(message)
                    send_telegram_message(message)

                except Exception as e:
                    print(f"Error checking {username}: {str(e)}")

                time.sleep(2)  # Delay between checks

            print(f"[{current_time}] Completed check cycle. Waiting 10 minutes...")
            send_telegram_message("✅ Check cycle completed. Waiting 10 minutes for next check.")
            time.sleep(600)

        except Exception as e:
            print(f"Major error in check cycle: {str(e)}")
            send_telegram_message(f"⚠️ Bot encountered an error: {str(e)}\nRestarting check cycle...")
            time.sleep(30)
