
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="날짜별 기온분석", layout="wide")

# 데이터 불러오기
df = pd.read_csv("seoul.csv", encoding="cp949")

# 컬럼명 정리
df.columns = df.columns.str.strip()

# 날짜 변환
df["날짜"] = pd.to_datetime(df["날짜"])

# 연도, 월, 일 추출
df["연도"] = df["날짜"].dt.year
df["월"] = df["날짜"].dt.month
df["일"] = df["날짜"].dt.day

st.title("날짜별 기온분석")

# 월, 일 선택
month = st.selectbox("월 선택", range(1, 13))
day = st.selectbox("일 선택", range(1, 32))

# 선택 날짜 데이터
filtered = df[(df["월"] == month) & (df["일"] == day)].copy()

if len(filtered) == 0:
    st.warning("해당 날짜의 데이터가 없습니다.")
else:
    filtered = filtered.sort_values("연도")

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        filtered["연도"],
        filtered["최고기온(℃)"],
        color="hotpink",
        marker="o",
        label="최고기온"
    )

    ax.plot(
        filtered["연도"],
        filtered["최저기온(℃)"],
        color="lightblue",
        marker="o",
        label="최저기온"
    )

    ax.set_title("날짜별 기온분석", fontsize=16)
    ax.set_xlabel("연도")
    ax.set_ylabel("온도(℃)")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

    st.dataframe(
        filtered[["연도", "최고기온(℃)", "최저기온(℃)"]],
        use_container_width=True
    )
