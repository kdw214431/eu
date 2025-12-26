import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
import time

# 페이지 기본 설정
st.set_page_config(
    page_title="유로(EUR) 환율 모니터링",
    page_icon="💶",
    layout="wide"
)

# ---------------------------------------------------------
# 1. 데이터 가져오기 함수 (캐싱을 사용하여 속도 최적화)
# ---------------------------------------------------------
def get_exchange_rate():
    # 원/유로 티커: EURKRW=X
    ticker = "EURKRW=X"
    data = yf.Ticker(ticker)
    
    # 1일치 데이터 (현재가 확인용)
    todays_data = data.history(period='1d')
    current_price = todays_data['Close'].iloc[-1]
    
    # 그래프용 과거 데이터 (최근 3개월)
    history_data = data.history(period='3mo')
    
    return current_price, history_data

# ---------------------------------------------------------
# 2. UI 구성
# ---------------------------------------------------------
st.title("💶 실시간 유로(EUR/KRW) 환율 알리미")

# 사이드바: 설정 영역
st.sidebar.header("알림 설정")
target_price = st.sidebar.number_input(
    "목표 환율을 설정하세요 (원)", 
    min_value=1000.0, 
    max_value=2000.0, 
    value=1450.0, 
    step=1.0
)
enable_monitoring = st.sidebar.checkbox("실시간 모니터링 켜기 (30초마다 갱신)")

# 데이터 로드
current_price, history_df = get_exchange_rate()

# ---------------------------------------------------------
# 3. 메인 화면: 환율 정보 및 그래프
# ---------------------------------------------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("현재 환율")
    # 전일 대비 변동폭 계산 (단순화를 위해 여기선 생략하거나 추가 가능)
    st.metric(label="EUR/KRW", value=f"{current_price:,.2f} 원")

    # 알림 로직
    # (예: 유로가 싸지면 사기 위해 '목표가보다 낮을 때' 알림)
    if current_price <= target_price:
        st.error(f"🔔 알림: 현재 환율({current_price:,.2f}원)이 목표가({target_price}원)보다 낮습니다! (매수 기회)")
        st.toast("목표 가격 도달! 확인하세요!", icon="🚨")
    else:
        st.success(f"현재 환율이 목표가({target_price}원)보다 높습니다. 기다리는 중...")

with col2:
    st.subheader("최근 3개월 환율 추이")
    # Plotly로 그래프 그리기
    fig = px.line(history_df, x=history_df.index, y='Close', title='EUR/KRW Exchange Rate')
    fig.update_xaxes(title_text='날짜')
    fig.update_yaxes(title_text='환율 (원)')
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# 4. 자동 새로고침 로직
# ---------------------------------------------------------
if enable_monitoring:
    time.sleep(30) # 30초 대기
    st.rerun()     # 화면 다시 그리기 (데이터 갱신)