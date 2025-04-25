import requests
from bs4 import BeautifulSoup
import time

TELEGRAM_TOKEN = '7588405381:AAGjiRU0DFFClUJDYURUz8SISz8b2VCmfTY'
CHAT_ID = '6167718314'

def send_telegram(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=data)

url = 'https://tickets.interpark.com/goods/25005684'

while True:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    seat_info = soup.find_all('li', class_='seatTableItem')

    found_seat = False
    for seat in seat_info:
        seat_name = seat.find('strong', class_='seatTableName').text.strip()
        seat_status = seat.find('span', class_='seatTableStatus').text.strip()
        print(f'{seat_name}: {seat_status}')

        if '0석' not in seat_status:
            found_seat = True
            send_telegram(f'{seat_name} - {seat_status} 자리 떴다!')

    if not found_seat:
        print("아직 빈자리 없음.")
    
    time.sleep(1)
    
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "자리 감지 중!"

port = int(os.environ.get("PORT", 10000))
app.run(host='0.0.0.0', port=port)

# Flask 서버를 별도 쓰레드로 실행
t = Thread(target=run_flask)
t.start()
