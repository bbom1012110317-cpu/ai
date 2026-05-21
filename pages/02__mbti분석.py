import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="Countries MBTI Dashboard",
    page_icon="🌍",
    layout="wide"
)

# 제목
st.title("🌍 Countries MBTI Dashboard")
st.markdown("국가별 MBTI 비율 인터랙티브 시각화")

# 데이터 불러오기
df = pd.read_csv("countriesMBTI_16types.csv")

# 국가 선택
country = st.selectbox(
    "국가 선택",
    df["Country"].unique()
)

# 선택된 국가 데이터
selected = df[df["Country"] == country].iloc[0]

# MBTI 데이터만 추출
mbti_data = selected.drop("Country")

# 정렬
mbti_data = mbti_data.sort_values(ascending=False)

# 1등 찾기
top_type = mbti_data.idxmax()

# 색상 설정
colors = []

for mbti in mbti_data.index:
    if mbti == top_type:
        colors.append("#2563eb")  # 파란색
    else:
        colors.append("rgba(37,99,235,0.25)")  # 연한 파란색

# 그래프 생성
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=mbti_data.index,
        y=mbti_data.values,
        marker=dict(
            color=colors,
            line=dict(
                color="rgba(37,99,235,1)",
                width=1
            )
        ),
        text=[f"{v:.1%}" for v in mbti_data.values],
        textposition="outside",
        hovertemplate=
        "<b>%{x}</b><br>" +
        "비율: %{y:.2%}<extra></extra>"
    )
)

# 레이아웃
fig.update_layout(
    title=f"{country} MBTI 비율",
    template="plotly_white",
    height=650,
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    yaxis_tickformat=".0%",
    showlegend=False,
    font=dict(
        size=15
    ),
    margin=dict(
        l=30,
        r=30,
        t=70,
        b=30
    )
)

# 표시
st.plotly_chart(fig, use_container_width=True)

# TOP3
st.subheader("🏆 TOP 3 MBTI")

top3 = mbti_data.head(3)

for i, (mbti, value) in enumerate(top3.items(), start=1):
    st.write(f"{i}. {mbti} — {value:.2%}")

# 데이터 보기
with st.expander("데이터 보기"):
    st.dataframe(
        mbti_data.reset_index().rename(
            columns={
                "index": "MBTI",
                0: "비율"
            }
        ),
        use_container_width=True
    )
