import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------------
# 🎯 1. 웹사이트 기본 환경 설정
# -----------------------------------------------------------------
st.set_page_config(page_title="캠퍼스 혼밥소외지수 진단기", page_icon="📊", layout="centered")

st.title("📊 캠퍼스 혼밥소외지수 진단기")
st.write("설문조사 변수를 소수점 3자리까지 정밀 조절하여 학년별 위험 단계를 진단하고 그래프를 확인하세요.")
st.markdown("---")

# -----------------------------------------------------------------
# 🎯 2. 변수 입력 UI (소수점 3자리 정밀도 패치 완료)
# -----------------------------------------------------------------
st.subheader("🕵️‍♂️ 분석 변수 설정 (소수점 3자리 정밀 제어)")
st.write("진단하고자 하는 학년의 통계 요인값을 입력하세요.")

col1, col2 = st.columns(2)

with col1:
    # step=0.001 설정을 통해 소수점 3자리 조절이 가능하게 만들고, 화면 표기도 .3f(소수점3자리)로 강제 지정했습니다.
    A = st.slider("A: 빈도 요인 (절삭평균 / 7회)", min_value=0.000, max_value=1.000, value=0.306, step=0.001, format="%.3f")
    B = st.slider("B: 비자발적 심리 요인 ('사람 없음' 응답 비율)", min_value=0.000, max_value=1.000, value=0.333, step=0.001, format="%.3f")

with col2:
    C = st.slider("C: 극단적 이상치 요인 (Z-점수 2.5 초과 학생 비율)", min_value=0.000, max_value=1.000, value=0.000, step=0.001, format="%.3f")
    D = st.slider("D: 양극화 요인 (집단 내 변동계수)", min_value=0.000, max_value=2.000, value=1.120, step=0.001, format="%.3f")

# -----------------------------------------------------------------
# 🎯 3. 혼밥소외지수 연산 및 위험 단계 판정 출력 (소수점 3자리 반영)
# -----------------------------------------------------------------
score = 100 * (0.2 * A + 0.3 * B + 0.3 * C + 0.2 * D)

# 통합 기준치 및 위험 구간 설정
baseline = 30.33
danger_line = baseline + (baseline / 5)  # 36.40

st.markdown("---")
st.subheader("📈 위험도 진단 결과")

col_res1, col_res2 = st.columns(2)
with col_res1:
    st.metric(label="산출된 혼밥소외지수", value=f"{score:.3f} 점") # 출력도 소수점 3자리로 매핑
with col_res2:
    st.metric(label="캠퍼스 표준 기준치", value=f"{baseline:.3f} 점")

# 판정 알고리즘
if score >= danger_line:
    st.error("🚨 최종 판정 결과: [🔴 위험 단계]")
    st.info("💡 **결론**: 기준치보다 20% 이상 높아 집중 관리가 필요한 심각한 상태입니다.")
elif score > baseline:
    st.warning("⚠️ 최종 판정 결과: [🟡 주의 단계]")
    st.info("💡 **결론**: 캠퍼스 전체 기준치를 초과하여 모니터링이 필요합니다.")
else:
    st.success("✅ 최종 판정 결과: [🟢 안전 단계]")
    st.info("💡 **결론**: 기준치 이하로 집단 내 정서적 소외도가 매우 낮으며 안정적입니다.")

# -----------------------------------------------------------------
# 🎯 4. 시각화 섹션 ①: 상자수염그림 종합 비교
# -----------------------------------------------------------------
st.markdown("---")
st.subheader("📦 학년별 및 캠퍼스 전체 상자수염그림 종합 비교")

positions = [4, 3, 2, 1]
colors = ['#D6E4F0', '#FCE4D6', '#EAEAEA', '#E2EFDA']
edge_colors = ['#1F4E79', '#C65911', '#7F7F7F', '#548235']
medians = [1.5, 2.0, 2.0, 2.0]
q1s = [0.0, 1.0, 1.0, 1.0]
q3s = [4.5, 3.0, 5.0, 4.0]
mins = [0, 0, 0, 0]
maxs = [7, 7, 6, 7]

fig1, ax1 = plt.subplots(figsize=(10, 6))

for pos, color, edge_color, q1, q2, q3, min_val, max_val in zip(positions, colors, edge_colors, q1s, medians, q3s, mins, maxs):
    ax1.fill_between([q1, q3], [pos - 0.2, pos - 0.2], [pos + 0.2, pos + 0.2], facecolor=color, edgecolor=edge_color, linewidth=2, zorder=3)
    ax1.plot([q2, q2], [pos - 0.2, pos + 0.2], color='#C00000', linewidth=3, zorder=4)
    if min_val != q1:
        ax1.plot([min_val, q1], [pos, pos], color='#7F7F7F', linestyle='-', linewidth=1.5, zorder=2)
    ax1.plot([min_val, min_val], [pos - 0.1, pos + 0.1], color='#7F7F7F', linewidth=1.5, zorder=2)
    ax1.plot([q3, max_val], [pos, pos], color='#7F7F7F', linestyle='-', linewidth=1.5, zorder=2)
    ax1.plot([max_val, max_val], [pos - 0.1, pos + 0.1], color='#7F7F7F', linewidth=1.5, zorder=2)

for val in range(8):
    ax1.axvline(x=val, color='#D3D3D3', linestyle=':', alpha=0.6, linewidth=1.2, zorder=1)

ax1.set_yticks(positions)
ax1.set_yticklabels(['1학년', '2학년', '3·4학년', '캠퍼스 전체'], fontsize=11, fontweight='bold')
ax1.set_xlim(-0.5, 7.5)
ax1.set_xticks(range(8))
ax1.set_ylim(0.4, 4.6)
ax1.set_xlabel('일주일 기준 혼밥 횟수 (회)', fontsize=11)
ax1.set_title('상자수염그림 분석 (Box and Whisker Plot)', fontsize=13, fontweight='bold', pad=15)

st.pyplot(fig1)

# -----------------------------------------------------------------
# 🎯 5. 시각화 섹션 ②: Z-점수 곡선 및 실시간 위치 반사
# -----------------------------------------------------------------
st.markdown("---")
st.subheader("📈 표준정규분포 곡선 및 실시간 이상치 위치")

x = np.linspace(-4, 4, 1000)
y = (1 / np.sqrt(2 * np.pi)) * np.exp(-x**2 / 2)

fig2, ax2 = plt.subplots(figsize=(8, 4.5))
ax2.plot(x, y, color='#4A4A4A', linewidth=2)
ax2.fill_between(x, y, color='#F2F2F2', alpha=0.5)

ax2.axvline(x=2.5, color='#E74C3C', linestyle='--', linewidth=1.5, label='이상치 경계선 (Z = +2.5)')
ax2.fill_between(x, y, where=(x >= 2.5), color='#E74C3C', alpha=0.15)

# 입력받은 세밀한 소수점 3자리 A값을 계산식에 연동하여 실시간 이동 반영
current_z = (A * 7 - 2.32) / 1.92
ax2.scatter(current_z, (1 / np.sqrt(2 * np.pi)) * np.exp(-current_z**2 / 2), color='#ED7D31', s=120, zorder=5)
ax2.annotate(f'현재 설정된 변수 위치\n(Z = {current_z:.3f})', 
            xy=(current_z, (1 / np.sqrt(2 * np.pi)) * np.exp(-current_z**2 / 2)), 
            xytext=(current_z - 1.6 if current_z > 1 else current_z + 0.5, 0.25),
            arrowprops=dict(arrowstyle='->', color='#ED7D31', lw=1.5), fontsize=9, fontweight='bold')

ax2.set_xlim(-4, 4)
ax2.set_ylim(0, 0.45)
ax2.set_xlabel('Z-Score (Z점수)')
ax2.set_ylabel('Density (밀도)')
ax2.legend(loc='upper left')
ax2.grid(axis='x', linestyle=':', alpha=0.5)

st.pyplot(fig2)
