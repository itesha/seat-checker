import requests
from bs4 import BeautifulSoup
import time
import os
from flask import Flask
from threading import Thread

# 텔레그램 설정
TELEGRAM_TOKEN = '7588405381:AAGjiRU0DFFClUJDYURUz8SISz8b2VCmfTY'
CHAT_ID = '6167718314'

def send_telegram(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=data)

# 자리 감지 함수 (디버그 추가됨)
def seat_checker():
    print("자리 감지 시작!")  # 디버그 로그
    url = 'https://tickets.interpark.com/goods/25005684'
    while True:
        try:
            print("페이지 요청 중...")
            response = requests.get(url)
            print("응답 상태 코드:", response.status_code)

            soup = BeautifulSoup(response.text, 'html.parser')

            seat_info = soup.find_all('li', class_='seatTableItem')
            print(f"좌석 정보 {len(seat_info)}개 찾음")

            found_seat = False
            for seat in seat_info:
                seat_name = seat.find('strong', class_='seatTableName').text.strip()
                seat_status = seat.find('span', class_='seatTableStatus').text.strip()
                print(f'{seat_name}: {seat_status}')  # 좌석 상태 로그

                if '0석' not in seat_status:
                    found_seat = True
                    send_telegram(f'{seat_name} - {seat_status} 자리 떴다!')

            if not found_seat:
                print("아직 빈자리 없음.")

        except Exception as e:
            print(f"오류 발생: {e}")

        time.sleep(1)

# Flask 서버 설정
app = Flask(__name__)

@app.route('/')
def home():
    return "자리 감지 중!"

# Flask 실행 + 자리 감지 쓰레드 같이 실행
if __name__ == "__main__":
    # 자리 감지 쓰레드 실행
    t = Thread(target=seat_checker)
    t.start()

    # Flask 실행
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
