import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(
    page_title="서울 100년 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울의 연평균 기온 변화")
st.write("서울의 장기간 기온 데이터를 이용해 연도별 평균기온 변화를 확인합니다.")

# 데이터 주소
url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(url, encoding="utf-8-sig")

    # 날짜를 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"])

    # 연도 열 만들기
    df["연도"] = df["날짜"].dt.year

    # 평균기온을 숫자로 변환
    df["평균기온"] = pd.to_numeric(df["평균기온"], errors="coerce")

    return df


df = load_data()

# 연도별 평균기온 계산
yearly_temp = (
    df.groupby("연도", as_index=False)["평균기온"]
    .mean()
    .dropna()
)

# 최근 100년 데이터 선택
latest_year = yearly_temp["연도"].max()
start_year = latest_year - 99

data_100 = yearly_temp[
    yearly_temp["연도"] >= start_year
]

st.subheader(f"📊 {start_year}년 ~ {latest_year}년 연평균 기온")

# 그래프 만들기
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    data_100["연도"],
    data_100["평균기온"],
    marker="o",
    markersize=3
)

ax.set_title("서울 100년간 연평균 기온 변화", fontsize=16)
ax.set_xlabel("연도")
ax.set_ylabel("연평균 기온 (℃)")
ax.grid(True, alpha=0.3)

st.pyplot(fig)

# 간단한 통계 정보
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "100년 중 가장 이른 해의 평균기온",
        f"{data_100.iloc[0]['평균기온']:.2f} ℃"
    )

with col2:
    st.metric(
        "가장 최근 해의 평균기온",
        f"{data_100.iloc[-1]['평균기온']:.2f} ℃"
    )

with col3:
    change = (
        data_100.iloc[-1]["평균기온"]
        - data_100.iloc[0]["평균기온"]
    )

    st.metric(
        "100년간 기온 변화",
        f"{change:.2f} ℃"
    )

st.caption("데이터 출처: 서울 기온 데이터")
