import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
import time
import requests # 텔레그램 전송을 위해 추가

# ==========================================
# [중요] 여기에 아까 받은 정보를 입력하세요
# ==========================================
TELEGRAM_TOKEN = "8598916371:AAEaH7rgLA_Krt0Zi4tK0UZBCS020-F4bm4" 
TELEGRAM_CHAT_ID = "7976546459"

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        requests.post(url, data=data)
    except Exception as e:
        st.error(f"텔레그램 전송 실패: {e}")

# 페이지 설정
st.set_page_config(page_title="유로 환율 알리미", page_icon="💶", layout="wide")

# 세션 상태 초기화 (알림 중복 발송 방지용)
if 'last_msg_time' not in st.session_state:
    st.session_state['last_msg_time'] = 0

def get_exchange_rate():
    ticker = "EURKRW=X"
    data = yf.Ticker(ticker)
    todays_data = data.history(period='1d')
    current_price = todays_data['Close'].iloc[-1]
    history_data = data.history(period='3mo')
    return current_price, history_data

st.title("💶 유로 환율 모니터링 & 텔레그램 알림")

# 사이드바
st.sidebar.header("설정")
target_price = st.sidebar.number_input("목표 환율(원)", value=1450.0)
enable_monitoring = st.sidebar.checkbox("모니터링 시작")

# 데이터 로드
current_price, history_df = get_exchange_rate()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("현재 환율")
    st.metric(label="EUR/KRW", value=f"{current_price:,.2f} 원")

    if current_price <= target_price:
        msg = f"🚨 [매수 신호] 현재 유로 환율이 {current_price:,.2f}원입니다! (목표가: {target_price}원 이하)"
        st.error(msg)
        
        # 텔레그램 알림 보내기 (도배 방지: 1시간에 1번만 보내기)
        if time.time() - st.session_state['last_msg_time'] > 3600:
            if enable_monitoring: # 모니터링이 켜져있을 때만 전송
                send_telegram_message(msg)
                st.session_state['last_msg_time'] = time.time()
                st.toast("텔레그램 메시지를 보냈습니다!", icon="✈️")
    else:
        st.success("아직 목표가보다 높습니다.")

with col2:
    fig = px.line(history_df, x=history_df.index, y='Close', title='최근 3개월 추이')
    st.plotly_chart(fig, use_container_width=True)

if enable_monitoring:
    time.sleep(30)
    st.rerun()
