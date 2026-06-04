import streamlit as st
import pandas as pd
from pathlib import Path

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(
    page_title="서울시 패스트푸드 섭취빈도 분석",
    page_icon="🍔",
    layout="wide"
)

# ---------------------------
# CSS 꾸미기
# ---------------------------
st.markdown("""
<style>
.stApp {
    background-color: #EAF8FF;
}

h1 {
    text-align:center;
    color:#FF4FA3;
}

.block-container {
    padding-top: 2rem;
}

div[data-baseweb="select"] {
    background-color:white;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# 제목
# ---------------------------
st.title("🍔 서울시 패스트푸드 섭취빈도 분석")

st.markdown("---")

# ---------------------------
# CSV 불러오기
# ---------------------------
csv_path = Path(__file__).parent.parent / "fastfood(1).csv"

try:
    df = pd.read_csv(csv_path, encoding="cp949")
except:
    df = pd.read_csv(csv_path, encoding="utf-8")

# ---------------------------
# 첫 열 이름
# ---------------------------
first_col = df.columns[0]

# 구분별, 소계 제거
df = df[
    ~df[first_col].astype(str).str.contains(
        "구분별|소계",
        na=False
    )
]

# ---------------------------
# 성별/연령 분리
# ---------------------------
gender_keywords = ["남자", "남성", "여자", "여성"]

gender_df = df[
    df[first_col].astype(str).str.contains(
        "|".join(gender_keywords),
        na=False
    )
]

age_df = df[
    ~df[first_col].astype(str).str.contains(
        "|".join(gender_keywords),
        na=False
    )
]

# ---------------------------
# 탭
# ---------------------------
tab1, tab2 = st.tabs(["👦 성별 분석", "📊 연령별 분석"])

# ---------------------------
# 성별 분석
# ---------------------------
with tab1:

    st.subheader("성별 패스트푸드 섭취 빈도")

    gender = st.selectbox(
        "성별 선택",
        gender_df[first_col].tolist()
    )

    row = gender_df[
        gender_df[first_col] == gender
    ].iloc[0]

    chart_data = pd.to_numeric(
        row.iloc[1:],
        errors="coerce"
    )

    graph_df = pd.DataFrame({
        "섭취빈도": chart_data.index,
        "비율": chart_data.values
    })

    st.bar_chart(
        graph_df,
        x="섭취빈도",
        y="비율",
        color="#FF69B4"
    )

    st.success(f"현재 선택: {gender}")

# ---------------------------
# 연령 분석
# ---------------------------
with tab2:

    st.subheader("연령별 패스트푸드 섭취 빈도")

    age = st.selectbox(
        "연령 선택",
        age_df[first_col].tolist()
    )

    row = age_df[
        age_df[first_col] == age
    ].iloc[0]

    chart_data = pd.to_numeric(
        row.iloc[1:],
        errors="coerce"
    )

    graph_df = pd.DataFrame({
        "섭취빈도": chart_data.index,
        "비율": chart_data.values
    })

    st.bar_chart(
        graph_df,
        x="섭취빈도",
        y="비율",
        color="#FF69B4"
    )

    st.success(f"현재 선택: {age}")

# ---------------------------
# 데이터 보기
# ---------------------------
with st.expander("원본 데이터 보기"):
    st.dataframe(df, use_container_width=True)
