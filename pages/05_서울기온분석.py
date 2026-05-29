import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="날짜별 기온분석",
    layout="wide"
)

# 데이터 불러오기
try:
    df = pd.read_csv("seoul.csv", encoding="cp949")
except:
    df = pd.read_csv("seoul.csv", encoding="utf-8")

# 컬럼명 공백 제거
df.columns = df.columns.str.strip()

# 날짜 문자열 정리
df["날짜"] = df["날짜"].astype(str).str.strip()

# 날짜 변환
df["날짜"] = pd.to_datetime(
    df["날짜"],
    errors="coerce"
)

# 날짜 변환 실패 행 제거
df = df.dropna(subset=["날짜"])

# 연도, 월, 일 생성
df["연도"] = df["날짜"].dt.year
df["월"] = df["날짜"].dt.month
df["일"] = df["날짜"].dt.day

st.title("날짜별 기온분석")

# 월 선택
month = st.selectbox(
    "월 선택",
    range(1, 13)
)

# 해당 월에 존재하는 일만 표시
available_days = sorted(
    df[df["월"] == month]["일"].unique()
)

day = st.selectbox(
    "일 선택",
    available_days
)

# 데이터 필터링
filtered = df[
    (df["월"] == month) &
    (df["일"] == day)
].copy()

filtered = filtered.sort_values("연도")

if filtered.empty:
    st.warning("해당 날짜 데이터가 없습니다.")
else:

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        filtered["연도"],
        filtered["최고기온(℃)"],
        color="hotpink",
        linewidth=2,
        marker="o",
        label="최고기온"
    )

    ax.plot(
        filtered["연도"],
        filtered["최저기온(℃)"],
        color="lightblue",
        linewidth=2,
        marker="o",
        label="최저기온"
    )

    ax.set_title("날짜별 기온분석")
    ax.set_xlabel("연도")
    ax.set_ylabel("온도(℃)")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

    st.subheader(f"{month}월 {day}일 기온 데이터")

    st.dataframe(
        filtered[
            [
                "연도",
                "최고기온(℃)",
                "최저기온(℃)"
            ]
        ],
        use_container_width=True
    )
