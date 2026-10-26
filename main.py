import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="비즈니스 대시보드",
    page_icon="📈",
    layout="wide"
)

# -----------------------------------------------------------------------------
# 2. 가상 데이터 생성 (캐싱 적용)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    """최근 100일간의 가상 비즈니스 데이터를 생성합니다."""
    np.random.seed(42)  # 결과 고정
    
    # 최근 100일 날짜 생성
    end_date = datetime.today()
    dates = [end_date - timedelta(days=x) for x in range(100)]
    dates.reverse() # 과거부터 최신순으로 정렬
    
    # 카테고리 설정 (A, B, C 제품군)
    categories = np.random.choice(['제품 A', '제품 B', '제품 C'], size=100)
    
    # 가상의 방문자수 및 매출액 (방문자수에 비례하여 매출액이 나오도록 어느정도 상관관계 부여)
    visitors = np.random.randint(100, 1000, size=100)
    revenue = visitors * np.random.uniform(10, 50, size=100)
    
    df = pd.DataFrame({
        '날짜': dates,
        '카테고리': categories,
        '방문자수': visitors,
        '매출액(만원)': np.round(revenue, 0)
    })
    
    # 날짜 컬럼을 datetime 형식으로 변환 (필터링을 위해)
    df['날짜'] = pd.to_datetime(df['날짜']).dt.date
    return df

df = load_data()

# -----------------------------------------------------------------------------
# 3. UI - 타이틀 및 설명
# -----------------------------------------------------------------------------
st.title("📈 비즈니스 성과 대시보드")
st.markdown("""
이 대시보드는 스트림릿(Streamlit)을 활용하여 제작된 인터랙티브 데이터 분석 앱입니다.  
좌측 사이드바에서 **기간**과 **제품 카테고리**를 선택하여 데이터를 동적으로 탐색해 보세요!
""")

# -----------------------------------------------------------------------------
# 4. UI - 사이드바 필터 (입력 위젯)
# -----------------------------------------------------------------------------
st.sidebar.header("🔍 데이터 필터링")

# 위젯 1: 날짜 범위 선택 (slider 사용)
min_date = df['날짜'].min()
max_date = df['날짜'].max()

start_date, end_date = st.sidebar.slider(
    "조회 기간을 선택하세요",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# 위젯 2: 카테고리 다중 선택 (multiselect 사용)
unique_categories = df['카테고리'].unique()
selected_categories = st.sidebar.multiselect(
    "조회할 카테고리를 선택하세요",
    options=unique_categories,
    default=unique_categories
)

# 필터링 로직 적용
mask = (df['날짜'] >= start_date) & (df['날짜'] <= end_date) & (df['카테고리'].isin(selected_categories))
filtered_df = df.loc[mask]

# 필터링 결과가 없을 경우 예외 처리
if filtered_df.empty:
    st.warning("선택하신 조건에 맞는 데이터가 없습니다. 필터를 다시 조정해 주세요.")
    st.stop()

# -----------------------------------------------------------------------------
# 5. UI - 핵심 지표 (Metric Columns)
# -----------------------------------------------------------------------------
st.markdown("### 💡 주요 지표 요약")
col1, col2, col3 = st.columns(3)

# 지표 계산
total_visitors = int(filtered_df['방문자수'].sum())
total_revenue = int(filtered_df['매출액(만원)'].sum())
avg_revenue_per_visitor = total_revenue / total_visitors if total_visitors > 0 else 0

with col1:
    st.metric(label="총 방문자 수", value=f"{total_visitors:,} 명")

with col2:
    st.metric(label="총 매출액", value=f"{total_revenue:,} 만원")
    
with col3:
    st.metric(label="방문자 당 평균 매출", value=f"{avg_revenue_per_visitor:,.0f} 만원")

st.divider() # 구분선

# -----------------------------------------------------------------------------
# 6. UI - 데이터 시각화 (Charts)
# -----------------------------------------------------------------------------
st.markdown("### 📊 일별 트렌드 분석")

# 차트를 그리기 위해 날짜를 인덱스로 설정한 데이터 준비
chart_data = filtered_df.groupby('날짜')[['방문자수', '매출액(만원)']].sum()

# 탭을 사용하여 두 가지 차트를 번갈아 볼 수 있도록 구성
tab1, tab2 = st.tabs(["일별 방문자 수 트렌드 (Line)", "일별 매출액 비교 (Bar)"])

with tab1:
    # Streamlit 내장 라인 차트
    st.line_chart(chart_data['방문자수'], use_container_width=True, color="#FF4B4B")

with tab2:
    # Streamlit 내장 바 차트
    st.bar_chart(chart_data['매출액(만원)'], use_container_width=True, color="#0068C9")

st.divider()

# -----------------------------------------------------------------------------
# 7. UI - 원본 데이터 테이블 (Dataframe)
# -----------------------------------------------------------------------------
st.markdown("### 📋 상세 데이터 확인")
st.markdown("아래 표의 열 제목을 클릭하여 정렬하거나, 우측 상단 아이콘을 눌러 전체화면으로 볼 수 있습니다.")

# 인덱스를 숨기고 화면 너비에 맞게 데이터프레임 출력
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
