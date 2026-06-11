import streamlit as st

# 1. 웹사이트 타이틀 및 설명 설정
st.set_page_config(page_title="혼밥소외지수 진단기", page_icon="📊", layout="centered")

st.title("📊 캠퍼스 혼밥소외지수 진단기")
st.write("각 요인의 값을 슬라이더로 조절하여 학년별 위험 단계를 진단해보세요.")
st.markdown("---")

# 2. 사용자 입력 UI (슬라이더 및 직접 입력창)
st.subheader("🕵️‍♂️ 변수 입력")

col1, col2 = st.columns(2)

with col1:
    A = st.slider("A: 빈도 요인 (절삭평균 / 7회)", min_value=0.0, max_value=1.0, value=0.306, step=0.001, format="%0.3f")
    B = st.slider("B: 비자발적 심리 요인 (사람 없음 비율)", min_value=0.0, max_value=1.0, value=0.333, step=0.001, format="%0.3f")

with col2:
    C = st.slider("C: 극단적 이상치 요인 (이상치 학생 비율)", min_value=0.0, max_value=1.0, value=0.000, step=0.001, format="%0.3f")
    D = st.slider("D: 양극화 요인 (변동계수)", min_value=0.0, max_value=2.0, value=1.120, step=0.001, format="%0.3f")

# 3. 혼밥소외지수 계산
score = 100 * (0.2 * A + 0.3 * B + 0.3 * C + 0.2 * D)

# 기준치 설정
baseline = 30.33
danger_line = baseline + (baseline / 5)  # 36.40

st.markdown("---")
st.subheader("📈 진단 결과")

# 4. 시각화 및 위험 단계 판정 출력
col_res1, col_res2 = st.columns(2)

with col_res1:
    st.metric(label="산출된 혼밥소외지수", value=f"{score:.2f} 점")
with col_res2:
    st.metric(label="캠퍼스 표준 기준치", value=f"{baseline:.2f} 점")

if score >= danger_line:
    st.error("🚨 최종 판정 결과: [🔴 위험 단계]")
    st.info("💡 **해석**: 기준치(30.33점)보다 20% 이상 높아 집중 관리가 필요한 심각한 상태입니다. 새내기 맞춤형 소통 프로그램이나 학식 공간 개선이 시급합니다.")
elif score > baseline:
    st.warning("⚠️ 최종 판정 결과: [🟡 주의 단계]")
    st.info("💡 **해석**: 캠퍼스 전체 기준치를 초과하였습니다. 잠재적 소외 위험이 있으므로 지속적인 모니터링과 관심이 필요합니다.")
else:
    st.success("✅ 최종 판정 결과: [🟢 안전 단계]")
    st.info("💡 **해석**: 캠퍼스 기준치 이하로 집단 내 소외도가 낮으며 매우 안정적인 공동체 분포를 보이고 있습니다.")
