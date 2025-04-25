from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests

# 텔레그램 설정
TELEGRAM_TOKEN = '7588405381:AAGjiRU0DFFClUJDYURUz8SISz8b2VCmfTY'
CHAT_ID = '6167718314'

def send_telegram(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=data)

# 크롬 드라이버 셋업 (헤드리스 모드)
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 예매 페이지 URL
url = 'https://tickets.interpark.com/goods/25005684'

# 감지 루프
try:
    while True:
        driver.get(url)
        time.sleep(5)  # 페이지 로딩 대기

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        seats = soup.find_all('li', class_='seatTableItem')
        found_seat = False

        for seat in seats:
            seat_name = seat.find('strong', class_='seatTableName').text.strip()
            seat_status = seat.find('span', class_='seatTableStatus').text.strip()
            print(f'{seat_name}: {seat_status}')

            if '0석' not in seat_status:
                found_seat = True
                send_telegram(f'{seat_name} - {seat_status} 자리 떴다!')

        if not found_seat:
            print("아직 빈자리 없음.")
        
        time.sleep(1)  # 1초마다 확인

except Exception as e:
    print("오류 발생:", e)
    send_telegram(f'오류 발생: {e}')

finally:
    driver.quit()
