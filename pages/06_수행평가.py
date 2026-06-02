import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="서울시 패스트푸드 섭취빈도 분석")

# 데이터 불러오기
df = pd.read_csv("fastfood(1).csv", encoding="cp949")

# 첫 번째 행을 컬럼명으로 사용
freq_cols = df.iloc[0, 1:].tolist()

# 실제 데이터
data = df.iloc[1:].copy()
data.columns = ["구분"] + freq_cols

# 숫자 변환
for col in freq_cols:
    data[col] = pd.to_numeric(data[col].replace("-", 0), errors="coerce")

st.title("서울시 패스트푸드 섭취빈도 분석")

# 선택
selected = st.selectbox(
    "성별 또는 연령대를 선택하세요",
    data["구분"]
)

row = data[data["구분"] == selected].iloc[0]

graph_data = pd.DataFrame({
    "섭취빈도": freq_cols,
    "비율": [row[col] for col in freq_cols]
})

# 그래프
fig, ax = plt.subplots(figsize=(8, 5))

fig.patch.set_facecolor("#E6F7FF")
ax.set_facecolor("#E6F7FF")

bars = ax.bar(
    graph_data["섭취빈도"],
    graph_data["비율"],
    color="pink",
    label=selected
)

ax.set_title("서울시 패스트푸드 섭취빈도 분석")
ax.set_xlabel("섭취 빈도")
ax.set_ylabel("비율(%)")
ax.legend()

plt.xticks(rotation=20)

st.pyplot(fig)
