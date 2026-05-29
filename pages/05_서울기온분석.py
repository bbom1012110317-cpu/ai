import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

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

# 날짜 정리
df["날짜"] = df["날짜"].astype(str).str.strip()
df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")

# 날짜 변환 실패 제거
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

# 선택한 월에 존재하는 일만 표시
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
    st.stop()

# 미래 연도 선택
future_year = st.number_input(
    "예측할 미래 연도 선택",
    min_value=int(filtered["연도"].max()) + 1,
    value=int(filtered["연도"].max()) + 1,
    step=1
)

# 선형회귀 예측
X = filtered[["연도"]]

max_model = LinearRegression()
max_model.fit(X, filtered["최고기온(℃)"])
pred_max = max_model.predict([[future_year]])[0]

min_model = LinearRegression()
min_model.fit(X, filtered["최저기온(℃)"])
pred_min = min_model.predict([[future_year]])[0]

# Plotly 그래프
fig = go.Figure()

# 최고기온
fig.add_trace(
    go.Scatter(
        x=filtered["연도"],
        y=filtered["최고기온(℃)"],
        mode="lines+markers",
        name="최고기온",
        line=dict(color="hotpink", width=3),
        hovertemplate=
        "연도: %{x}<br>" +
        "최고기온: %{y:.1f}℃" +
        "<extra></extra>"
    )
)

# 최저기온
fig.add_trace(
    go.Scatter(
        x=filtered["연도"],
        y=filtered["최저기온(℃)"],
        mode="lines+markers",
        name="최저기온",
        line=dict(color="lightblue", width=3),
        hovertemplate=
        "연도: %{x}<br>" +
        "최저기온: %{y:.1f}℃" +
        "<extra></extra>"
    )
)

# 예측 최고기온
fig.add_trace(
    go.Scatter(
        x=[future_year],
        y=[pred_max],
        mode="markers",
        name="예측 최고기온",
        marker=dict(
            size=14,
            color="red"
        ),
        hovertemplate=
        f"연도: {future_year}<br>"
        f"예상 최고기온: {pred_max:.1f}℃"
        "<extra></extra>"
    )
)

# 예측 최저기온
fig.add_trace(
    go.Scatter(
        x=[future_year],
        y=[pred_min],
        mode="markers",
        name="예측 최저기온",
        marker=dict(
            size=14,
            color="blue"
        ),
        hovertemplate=
        f"연도: {future_year}<br>"
        f"예상 최저기온: {pred_min:.1f}℃"
        "<extra></extra>"
    )
)

fig.update_layout(
    title="날짜별 기온분석",
    xaxis_title="연도",
    yaxis_title="온도(℃)",
    hovermode="closest",
    legend_title="범례"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# 예측 결과 표시
st.subheader(f"{future_year}년 예측 결과")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "예상 최고기온",
        f"{pred_max:.1f}℃"
    )

with col2:
    st.metric(
        "예상 최저기온",
        f"{pred_min:.1f}℃"
    )

# 데이터 표
st.subheader(f"{month}월 {day}일 실제 데이터")

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
