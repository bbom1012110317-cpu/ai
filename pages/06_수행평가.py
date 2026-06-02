import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="서울시 패스트푸드 섭취빈도 분석",
    layout="wide"
)

# 제목
st.title("서울시 패스트푸드 섭취빈도 분석")

st.write("CSV 파일을 업로드하세요.")

# 파일 업로드
uploaded_file = st.file_uploader(
    "CSV 파일 선택",
    type=["csv"]
)

if uploaded_file is not None:

    # 인코딩 자동 처리
    try:
        df = pd.read_csv(uploaded_file, encoding="cp949")
    except:
        df = pd.read_csv(uploaded_file, encoding="utf-8")

    st.subheader("데이터 미리보기")
    st.dataframe(df)

    # 첫 번째 열 이름
    category_col = df.columns[0]

    # 선택 박스
    selected = st.selectbox(
        "성별 또는 연령대를 선택하세요",
        df[category_col].dropna().unique()
    )

    # 선택된 데이터
    row = df[df[category_col] == selected].iloc[0]

    # 첫 번째 열 제외
    chart_data = row.iloc[1:]

    # 숫자 변환
    chart_data = pd.to_numeric(
        chart_data,
        errors="coerce"
    )

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

    # 범례 역할
    st.info(f"범례 : {selected}")

else:
    st.warning("CSV 파일을 업로드해주세요.")
