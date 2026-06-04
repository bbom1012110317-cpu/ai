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
# CSS
# ---------------------------
st.markdown("""
<style>
.stApp {
    background-color: #EAF8FF;
}

h1 {
    text-align: center;
    color: #FF69B4;
}

div[data-baseweb="tab"] {
    font-size: 18px;
}

div[data-baseweb="select"] {
    background-color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# 제목
# ---------------------------
st.title("🍔 서울시 패스트푸드 섭취빈도 분석")

st.markdown("---")

# ---------------------------
# CSV 읽기
# pages 폴더의 상위 폴더에 있는 CSV
# ---------------------------
csv_path = Path(__file__).resolve().parent.parent / "fastfood(1).csv"

if not csv_path.exists():
    st.error(f"CSV 파일을 찾을 수 없습니다.\n\n찾는 위치:\n{csv_path}")
    st.stop()

try:
    df = pd.read_csv(csv_path, encoding="cp949")
except:
    df = pd.read_csv(csv_path, encoding="utf-8")

# ---------------------------
# 첫 번째 열
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
# 성별 데이터
# ---------------------------
gender_df = df[
    df[first_col].astype(str).str.contains(
        "남성|여성|남자|여자",
        na=False
    )
]

# ---------------------------
# 연령 데이터
# ---------------------------
age_df = df[
    ~df[first_col].astype(str).str.contains(
        "남성|여성|남자|여자",
        na=False
    )
]

# ---------------------------
# 탭 생성
# ---------------------------
tab1, tab2 = st.tabs(["👦 성별 분석", "📊 연령별 분석"])

# ===========================
# 성별 분석
# ===========================
with tab1:

    st.subheader("성별 패스트푸드 섭취 빈도")

    gender = st.selectbox(
        "성별 선택",
        gender_df[first_col].tolist(),
        key="gender"
    )

    row = gender_df[
        gender_df[first_col] == gender
    ].iloc[0]

    values = pd.to_numeric(
        row.iloc[1:],
        errors="coerce"
    )

    chart_df = pd.DataFrame({
        "섭취빈도": values.index,
        "비율": values.values
    })

    st.bar_chart(
        chart_df,
        x="섭취빈도",
        y="비율"
    )

    st.success(f"선택한 성별 : {gender}")

# ===========================
# 연령 분석
# ===========================
with tab2:

    st.subheader("연령별 패스트푸드 섭취 빈도")

    age = st.selectbox(
        "연령 선택",
        age_df[first_col].tolist(),
        key="age"
    )

    row = age_df[
        age_df[first_col] == age
    ].iloc[0]

    values = pd.to_numeric(
        row.iloc[1:],
        errors="coerce"
    )

    chart_df = pd.DataFrame({
        "섭취빈도": values.index,
        "비율": values.values
    })

    st.bar_chart(
        chart_df,
        x="섭취빈도",
        y="비율"
    )

    st.success(f"선택한 연령 : {age}")

# ---------------------------
# 원본 데이터
# ---------------------------
with st.expander("원본 데이터 보기"):
    st.dataframe(df, use_container_width=True)
