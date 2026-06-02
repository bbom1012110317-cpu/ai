import streamlit as st
import pandas as pd

st.set_page_config(page_title="서울시 패스트푸드 섭취빈도 분석")

st.title("서울시 패스트푸드 섭취빈도 분석")

# CSV 읽기
try:
    df = pd.read_csv("fastfood(1).csv", encoding="cp949")
except:
    df = pd.read_csv("fastfood(1).csv", encoding="utf-8")

# 데이터 확인
st.write("데이터 미리보기")
st.dataframe(df.head())

# 첫 번째 열을 선택 기준으로 사용
category_col = df.columns[0]

selected = st.selectbox(
    "성별 또는 연령대를 선택하세요",
    df[category_col].dropna().unique()
)

# 선택된 행
row = df[df[category_col] == selected].iloc[0]

# 첫 번째 열 제외
chart_data = row.iloc[1:]

# 숫자 변환
chart_data = pd.to_numeric(chart_data, errors="coerce")

chart_df = pd.DataFrame({
    "섭취빈도": chart_data.index,
    "비율": chart_data.values
})

st.subheader(f"{selected} 패스트푸드 섭취 빈도")

st.bar_chart(
    chart_df.set_index("섭취빈도")
)

st.caption("서울시 패스트푸드 섭취빈도 분석")
