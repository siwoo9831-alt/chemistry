import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ==========================================
# 1. 원소 데이터베이스 구축 (1~118번)
# ==========================================
@st.cache_data
def load_element_data():
    # 교과서 핵심 원소 30여 개 (원자번호, 기호, 한글이름, 환원전위, 비금속여부, 이론상여부, 주 산화수)
    core_data = [
        (1, 'H', '수소', 0.00, True, False, 1),
        (3, 'Li', '리튬', -3.04, False, False, 1),
        (4, 'Be', '베릴륨', -1.85, False, False, 2),
        (6, 'C', '탄소', 0.20, True, False, 4), # 불활성 전극용 대표값
        (7, 'N', '질소', -0.01, True, False, 3),
        (8, 'O', '산소', 1.23, True, False, 2),
        (9, 'F', '플루오린', 2.87, True, False, 1),
        (11, 'Na', '나트륨', -2.71, False, False, 1),
        (12, 'Mg', '마그네슘', -2.37, False, False, 2),
        (13, 'Al', '알루미늄', -1.66, False, False, 3),
        (17, 'Cl', '염소', 1.36, True, False, 1),
        (19, 'K', '칼륨', -2.93, False, False, 1),
        (20, 'Ca', '칼슘', -2.87, False, False, 2),
        (24, 'Cr', '크로뮴', -0.74, False, False, 3),
        (25, 'Mn', '망가니즈', -1.18, False, False, 2),
        (26, 'Fe', '철', -0.44, False, False, 2),
        (27, 'Co', '코발트', -0.28, False, False, 2),
        (28, 'Ni', '니켈', -0.25, False, False, 2),
        (29, 'Cu', '구리', 0.34, False, False, 2),
        (30, 'Zn', '아연', -0.76, False, False, 2),
        (35, 'Br', '브로민', 1.07, True, False, 1),
        (47, 'Ag', '은', 0.80, False, False, 1),
        (50, 'Sn', '주석', -0.14, False, False, 2),
        (53, 'I', '아이오딘', 0.54, True, False, 1),
        (56, 'Ba', '바륨', -2.91, False, False, 2),
        (78, 'Pt', '백금', 1.18, False, False, 2),
        (79, 'Au', '금', 1.50, False, False, 3),
        (80, 'Hg', '수은', 0.85, False, False, 2),
        (82, 'Pb', '납', -0.13, False, False, 2)
    ]
    
    df = pd.DataFrame(core_data, columns=['원자번호', '기호', '한글이름', '표준환원전위', 'isNonMetal', 'isTheoretical', '산화수'])
    
    # 1~118번 중 없는 데이터는 임의/가상 데이터로 채우기
    existing_nums = df['원자번호'].tolist()
    missing_data = []
    for i in range(1, 119):
        if i not in existing_nums:
            is_theo = True if i >= 100 else False
            is_nonmetal = True if i in [2, 10, 18, 36, 54, 86, 118] else False # 비활성기체 등
            fake_potential = round(0.5 - (i * 0.01), 2) # 임의의 전위값 생성
            missing_data.append((i, f"Elem{i}", f"원소{i}", fake_potential, is_nonmetal, is_theo, 2))
            
    df_missing = pd.DataFrame(missing_data, columns=df.columns)
    df_full = pd.concat([df, df_missing]).sort_values('원자번호').reset_index(drop=True)
    df_full['표시이름'] = df_full.apply(lambda x: f"{x['원자번호']:03d} - {x['한글이름']} ({x['기호']})", axis=1)
    return df_full

df = load_element_data()

# ==========================================
# 2. UI 및 로직 함수
# ==========================================
st.set_page_config(page_title="화학 전지 & 전기 분해 시뮬레이터", layout="wide")
st.title("🔋 화학 전지 & 전기 분해 시뮬레이터")
st.markdown("고등학교 화학 교과과정에 맞춘 **산화-환원 반응** 직관적 시뮬레이터입니다.")

# 사이드바에서 모드 선택
mode = st.sidebar.radio("🔬 학습 모드 선택", ["화학 전지 (자발적 반응)", "전기 분해 (비자발적 반응)"])

def check_smart_exceptions(element):
    if element['isNonMetal']:
        st.warning(f"⚠️ **{element['한글이름']}({element['기호']})**은(는) 기체 또는 비금속 원소이므로 자체 전극을 만들 수 없습니다. 보조 전극으로 **백금(Pt)** 또는 **탄소(C)**를 사용합니다.")
    if element['isTheoretical']:
        st.info(f"ℹ️ **{element['한글이름']}**은(는) 100번대 인공/방사성 원소이므로, 현실에서 안정적으로 존재하기 힘듭니다. 계산된 전압은 실제가 아닌 이론적 가상값입니다.")

def draw_galvanic_cell(anode, cathode):
    fig = go.Figure()
    
    # 비커 그리기 (산화극 왼쪽, 환원극 오른쪽)
    fig.add_shape(type="rect", x0=1, y0=0, x1=3, y1=3, line=dict(color="black", width=2), fillcolor="lightblue", opacity=0.5)
    fig.add_shape(type="rect", x0=5, y0=0, x1=7, y1=3, line=dict(color="black", width=2), fillcolor="lightblue", opacity=0.5)
    
    # 전극 그리기
    fig.add_shape(type="rect", x0=1.7, y0=1, x1=2.3, y1=4, line=dict(color="black"), fillcolor="darkgray")
    fig.add_shape(type="rect", x0=5.7, y0=1, x1=6.3, y1=4, line=dict(color="black"), fillcolor="silver")
    
    # 전선 및 전압계
    fig.add_shape(type="line", x0=2, y0=4, x1=2, y1=5, line=dict(color="black", width=2))
    fig.add_shape(type="line", x0=6, y0=4, x1=6, y1=5, line=dict(color="black", width=2))
    fig.add_shape(type="line", x0=2, y0=5, x1=6, y1=5, line=dict(color="black", width=2))
    
    # 전압계 동그라미
    fig.add_shape(type="circle", x0=3.5, y0=4.5, x1=4.5, y1=5.5, line=dict(color="black", width=2), fillcolor="white")
    fig.add_annotation(x=4, y=5, text="<b>V</b>", showarrow=False, font=dict(size=20))
    
    # 전자 이동 화살표
    fig.add_annotation(x=4, y=5.7, text="<b>e⁻ 이동 방향 →</b>", showarrow=False, font=dict(color="red", size=14))
    
    # 염다리
    fig.add_shape(type="path", path="M 2.5 2 C 2.5 4.5, 5.5 4.5, 5.5 2", line=dict(color="green", width=15), opacity=0.6)
    fig.add_annotation(x=4, y=3.7, text="염다리", showarrow=False, font=dict(color="darkgreen", size=12))
    
    # 라벨링
    fig.add_annotation(x=2, y=0.5, text=f"(-) 산화극<br>{anode['기호']}", showarrow=False, font=dict(size=14, color="black"))
    fig.add_annotation(x=6, y=0.5, text=f"(+) 환원극<br>{cathode['기호']}", showarrow=False, font=dict(size=14, color="black"))
    
    fig.update_layout(xaxis=dict(visible=False, range=[0, 8]), yaxis=dict(visible=False, range=[0, 6]),
                      margin=dict(l=10, r=10, t=10, b=10), height=400)
    st.plotly_chart(fig, use_container_width=True)

def draw_electrolytic_cell(anode, cathode):
    fig = go.Figure()
    
    # 하나의 큰 비커/수조
    fig.add_shape(type="rect", x0=1, y0=0, x1=7, y1=3, line=dict(color="black", width=2), fillcolor="lightblue", opacity=0.5)
    
    # 전극 (왼쪽: 산화극(+), 오른쪽: 환원극(-))
    fig.add_shape(type="rect", x0=2.5, y0=1, x1=3.1, y1=4, line=dict(color="black"), fillcolor="darkgray")
    fig.add_shape(type="rect", x0=4.9, y0=1, x1=5.5, y1=4, line=dict(color="black"), fillcolor="silver")
    
    # 전선 및 전원 장치 (배터리)
    fig.add_shape(type="line", x0=2.8, y0=4, x1=2.8, y1=5, line=dict(color="black", width=2))
    fig.add_shape(type="line", x0=5.2, y0=4, x1=5.2, y1=5, line=dict(color="black", width=2))
    fig.add_shape(type="line", x0=2.8, y0=5, x1=3.8, y1=5, line=dict(color="black", width=2))
    fig.add_shape(type="line", x0=4.2, y0=5, x1=5.2, y1=5, line=dict(color="black", width=2))
    
    # 직류 전원 (긴 줄 +, 짧은 줄 -)
    fig.add_shape(type="line", x0=3.8, y0=4.6, x1=3.8, y1=5.4, line=dict(color="red", width=3)) # (+)극
    fig.add_shape(type="line", x0=4.2, y0=4.8, x1=4.2, y1=5.2, line=dict(color="blue", width=5)) # (-)극
    fig.add_annotation(x=3.8, y=5.7, text="(+)", showarrow=False, font=dict(color="red"))
    fig.add_annotation(x=4.2, y=5.7, text="(-)", showarrow=False, font=dict(color="blue"))
    fig.add_annotation(x=4, y=6.2, text="외부 전원 장치", showarrow=False, font=dict(size=14))
    
    # 전자 이동
    fig.add_annotation(x=2.5, y=5.3, text="<b>e⁻ →</b>", showarrow=False, font=dict(color="red"))
    fig.add_annotation(x=5.5, y=5.3, text="<b>e⁻ →</b>", showarrow=False, font=dict(color="blue"))

    # 라벨링 (전기분해: 산화극이 (+), 환원극이 (-))
    fig.add_annotation(x=2.8, y=0.5, text=f"(+) 산화극<br>{anode['기호']}", showarrow=False, font=dict(size=14, color="black"))
    fig.add_annotation(x=5.2, y=0.5, text=f"(-) 환원극<br>{cathode['기호']}", showarrow=False, font=dict(size=14, color="black"))
    
    fig.update_layout(xaxis=dict(visible=False, range=[0, 8]), yaxis=dict(visible=False, range=[0, 7]),
                      margin=dict(l=10, r=10, t=10, b=10), height=400)
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 3. 화학 전지 모드 (자발적)
# ==========================================
if "화학 전지" in mode:
    st.subheader("⚡ 화학 전지 (자발적 산화-환원 반응)")
    
    col1, col2 = st.columns(2)
    with col1:
        elem1_str = st.selectbox("첫 번째 원소 선택", df['표시이름'].tolist(), index=29) # Zn
    with col2:
        elem2_str = st.selectbox("두 번째 원소 선택", df['표시이름'].tolist(), index=28) # Cu
        
    e1 = df[df['표시이름'] == elem1_str].iloc[0]
    e2 = df[df['표시이름'] == elem2_str].iloc[0]
    
    if e1['원자번호'] == e2['원자번호']:
        st.error("서로 다른 두 원소를 선택해주세요.")
    else:
        # 환원전위 비교 (더 작은 쪽이 산화극(-), 큰 쪽이 환원극(+))
        if e1['표준환원전위'] < e2['표준환원전위']:
            anode, cathode = e1, e2
        else:
            anode, cathode = e2, e1
            
        st.markdown("---")
        check_smart_exceptions(anode)
        check_smart_exceptions(cathode)
        
        # 기전력 계산
        e_cell = cathode['표준환원전위'] - anode['표준환원전위']
        
        # 결과 및 Metric 표시
        met_col1, met_col2, met_col3 = st.columns(3)
        met_col1.metric("(-) 산화극 (Anode)", f"{anode['기호']} (E°= {anode['표준환원전위']:.2f}V)")
        met_col2.metric("(+) 환원극 (Cathode)", f"{cathode['기호']} (E°= {cathode['표준환원전위']:.2f}V)")
        met_col3.metric("표준 기전력 (E°cell)", f"{e_cell:.2f} V", "자발적 반응" if e_cell > 0 else "")
        
        st.markdown("### ⚗️ 실험 설계 (전해질/염다리 선택)")
        sel_col1, sel_col2, sel_col3 = st.columns(3)
        sel_col1.selectbox("산화극 전해질", [f"{anode['기호']}(NO₃)₂ 수용액", f"{anode['기호']}SO₄ 수용액", "기타"])
        sel_col2.selectbox("환원극 전해질", [f"{cathode['기호']}(NO₃)₂ 수용액", f"{cathode['기호']}SO₄ 수용액", "기타"])
        sel_col3.selectbox("염다리 물질", ["KNO₃", "KCl", "NH₄NO₃"])
        
        st.markdown("### 📊 반응식 및 시각화 도식")
        draw_galvanic_cell(anode, cathode)
        
        st.latex(fr"\text{{[(-) 산화극 반쪽 반응]}} : {anode['기호']} \rightarrow {anode['기호']}^{{{anode['산화수']}+}} + {anode['산화수']}e^-")
        st.latex(fr"\text{{[(+) 환원극 반쪽 반응]}} : {cathode['기호']}^{{{cathode['산화수']}+}} + {cathode['산화수']}e^- \rightarrow {cathode['기호']}")
        st.latex(fr"\text{{[전체 반응식]}} : {cathode['산화수']}{anode['기호']} + {anode['산화수']}{cathode['기호']}^{{{cathode['산화수']}+}} \rightarrow {cathode['산화수']}{anode['기호']}^{{{anode['산화수']}+}} + {anode['산화수']}{cathode['기호']}")

# ==========================================
# 4. 전기 분해 모드 (비자발적)
# ==========================================
else:
    st.subheader("🔌 전기 분해 (외부 에너지를 통한 비자발적 반응)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**(+)극 연결 원소 (산화 반응)**")
        anode_str = st.selectbox("(+)극 선택", df['표시이름'].tolist(), index=18) # Cu
    with col2:
        st.markdown("**(-)극 연결 원소 (환원 반응)**")
        cathode_str = st.selectbox("(-)극 선택", df['표시이름'].tolist(), index=21) # Ag
        
    anode = df[df['표시이름'] == anode_str].iloc[0]
    cathode = df[df['표시이름'] == cathode_str].iloc[0]
    
    st.markdown("---")
    check_smart_exceptions(anode)
    check_smart_exceptions(cathode)
    
    # 필요 전압 계산 (최소 외부 인가 전압)
    e_cell_reverse = cathode['표준환원전위'] - anode['표준환원전위']
    min_voltage = abs(e_cell_reverse) if e_cell_reverse < 0 else 0.0
    
    met_col1, met_col2, met_col3 = st.columns(3)
    met_col1.metric("(+) 산화극 (외부전원 +연결)", f"{anode['기호']} (E°= {anode['표준환원전위']:.2f}V)")
    met_col2.metric("(-) 환원극 (외부전원 -연결)", f"{cathode['기호']} (E°= {cathode['표준환원전위']:.2f}V)")
    met_col3.metric("최소 인가 전압 (이론치)", f"{min_voltage:.2f} V 이상", "비자발적 반응" if e_cell_reverse < 0 else "자발적", delta_color="inverse")
    
    st.markdown("### ⚗️ 전해질 통합 선택")
    st.selectbox("전해질 (수용액 또는 용융액)", [f"황산 구리({anode['기호']}SO₄) 수용액", f"염화 나트륨(NaCl) 용융액", "기타 수용액"])
    
    st.markdown("### 📊 반응식 및 시각화 도식")
    draw_electrolytic_cell(anode, cathode)
    
    st.latex(fr"\text{{[(+) 산화극 반쪽 반응]}} : {anode['기호']} \rightarrow {anode['기호']}^{{{anode['산화수']}+}} + {anode['산화수']}e^-")
    st.latex(fr"\text{{[(-) 환원극 반쪽 반응]}} : {cathode['기호']}^{{{cathode['산화수']}+}} + {cathode['산화수']}e^- \rightarrow {cathode['기호']}")
