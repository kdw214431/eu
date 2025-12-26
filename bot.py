import os
import requests
import yfinance as yf

# 1단계에서 저장한 키를 불러옵니다 (해킹 방지)
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# ==========================================
# [설정] 알림 받고 싶은 목표 가격
# ==========================================
TARGET_PRICE = 1680.0  
# ==========================================

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
        print("전송 성공")
    except Exception as e:
        print(f"전송 실패: {e}")

def check_price():
    ticker = "EURKRW=X"
    try:
        data = yf.Ticker(ticker)
        # 1분봉 데이터로 최신값 조회
        df = data.history(period='1d', interval='1m')
        
        if len(df) > 0:
            current_price = df['Close'].iloc[-1]
            print(f"현재 환율: {current_price:.2f}원")
            
            if current_price <= TARGET_PRICE:
                msg = f"🚨 [자동 알림] 유로가 {current_price:,.2f}원입니다! (목표가 {TARGET_PRICE}원 이하)"
                send_telegram_message(msg)
            else:
                print("아직 목표가보다 비쌉니다.")
        else:
            print("데이터를 가져올 수 없습니다.")
            
    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    check_price()
