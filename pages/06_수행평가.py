import streamlit as st
import pandas as pd
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="서울시 패스트푸드 섭취빈도 분석",
    layout="wide"
)

st.title("서울시 패스트푸드 섭취빈도 분석")

# CSV 경로 (pages 폴더의 상위 폴더)
csv_path = Path(__file__).parent.parent / "fastfood.csv"

# CSV 읽기
try:
    df = pd.read_csv(csv_path, encoding="cp949")
except:
    df = pd.read_csv(csv_path, encoding="utf-8")

# 데이터 확인
st.subheader("데이터 미리보기")
st.dataframe(df)

# 첫 번째 열을 기준 열로 사용
category_col = df.columns[0]

# 선택박스
selected = st.selectbox(
    "성별 또는 연령대를 선택하세요",
    df[category_col].dropna().unique()
)

# 선택 데이터
row = df[df[category_col] == selected].iloc[0]

# 첫 번째 열 제외
chart_data = row.iloc[1:]

# 숫자형 변환
chart_data = pd.to_numeric(chart_data, errors="coerce")

# 그래프용 데이터프레임
graph_df = pd.DataFrame({
    "섭취빈도": chart_data.index,
    "비율": chart_data.values
})

st.subheader(f"{selected} 패스트푸드 섭취 빈도")

# 막대그래프
st.bar_chart(
    graph_df,
    x="섭취빈도",
    y="비율"
)

# 범례
st.info(f"범례 : {selected}")
