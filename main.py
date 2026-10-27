import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ==========================================
# 1. 원소 데이터베이스 구축 (1~118번 전체 한글화)
# ==========================================
@st.cache_data
def load_element_data():
    element_dict = {
        1: ('H', '수소'), 2: ('He', '헬륨'), 3: ('Li', '리튬'), 4: ('Be', '베릴륨'), 5: ('B', '붕소'),
        6: ('C', '탄소'), 7: ('N', '질소'), 8: ('O', '산소'), 9: ('F', '플루오린'), 10: ('Ne', '네온'),
        11: ('Na', '나트륨'), 12: ('Mg', '마그네슘'), 13: ('Al', '알루미늄'), 14: ('Si', '규소'), 15: ('P', '인'),
        16: ('S', '황'), 17: ('Cl', '염소'), 18: ('Ar', '아르곤'), 19: ('K', '칼륨'), 20: ('Ca', '칼슘'),
        21: ('Sc', '스칸듐'), 22: ('Ti', '타이타늄'), 23: ('V', '바나듐'), 24: ('Cr', '크로뮴'), 25: ('Mn', '망가니즈'),
        26: ('Fe', '철'), 27: ('Co', '코발트'), 28: ('Ni', '니켈'), 29: ('Cu', '구리'), 30: ('Zn', '아연'),
        31: ('Ga', '갈륨'), 32: ('Ge', '저마늄'), 33: ('As', '비소'), 34: ('Se', '셀레늄'), 35: ('Br', '브로민'),
        36: ('Kr', '크립톤'), 37: ('Rb', '루비듐'), 38: ('Sr', '스트론튬'), 39: ('Y', '이트륨'), 40: ('Zr', '지르코늄'),
        41: ('Nb', '나이오븀'), 42: ('Mo', '몰리브데넘'), 43: ('Tc', '테크네튬'), 44: ('Ru', '루테늄'), 45: ('Rh', '로듐'),
        46: ('Pd', '팔라듐'), 47: ('Ag', '은'), 48: ('Cd', '카드뮴'), 49: ('In', '인듐'), 50: ('Sn', '주석'),
        51: ('Sb', '안티모니'), 52: ('Te', '텔루륨'), 53: ('I', '아이오딘'), 54: ('Xe', '제논'), 55: ('Cs', '세슘'),
        56: ('Ba', '바륨'), 57: ('La', '란타넘'), 58: ('Ce', '세륨'), 59: ('Pr', '프라세오디뮴'), 60: ('Nd', '네오디뮴'),
        61: ('Pm', '프로메튬'), 62: ('Sm', '사마륨'), 63: ('Eu', '유로퓸'), 64: ('Gd', '가돌리늄'), 65: ('Tb', '터븀'),
        66: ('Dy', '디스프로슘'), 67: ('Ho', '홀뮴'), 68: ('Er', '어븀'), 69: ('Tm', '툴륨'), 70: ('Yb', '이터븀'),
        71: ('Lu', '루테튬'), 72: ('Hf', '하프늄'), 73: ('Ta', '탄탈럼'), 74: ('W', '텅스텐'), 75: ('Re', '레늄'),
        76: ('Os', '오스뮴'), 77: ('Ir', '이리듐'), 78: ('Pt', '백금'), 79: ('Au', '금'), 80: ('Hg', '수은'),
        81: ('Tl', '탈륨'), 82: ('Pb', '납'), 83: ('Bi', '비스무트'), 84: ('Po', '폴로늄'), 85: ('At', '아스타틴'),
        86: ('Rn', '라돈'), 87: ('Fr', '프랑슘'), 88: ('Ra', '라듐'), 89: ('Ac', '악티늄'), 90: ('Th', '토륨'),
        91: ('Pa', '프로트악티늄'), 92: ('U', '우라늄'), 93: ('Np', '넵투늄'), 94: ('Pu', '플루토늄'), 95: ('Am', '아메리슘'),
        96: ('Cm', '퀴리움'), 97: ('Bk', '버클륨'), 98: ('Cf', '캘리포늄'), 99: ('Es', '아인슈타이늄'), 100: ('Fm', '페르뮴'),
        101: ('Md', '멘델레븀'), 102: ('No', '노벨륨'), 103: ('Lr', '로렌슘'), 104: ('Rf', '러더포듐'), 105: ('Db', '더브늄'),
        106: ('Sg', '시보귬'), 107: ('Bh', '보륨'), 108: ('Hs', '하슘'), 109: ('Mt', '마이트너륨'), 110: ('Ds', '다름슈타튬'),
        111: ('Rg', '뢴트게늄'), 112: ('Cn', '코페르니슘'), 113: ('Nh', '니호늄'), 114: ('Fl', '플레로븀'), 115: ('Mc', '모스코븀'),
        116: ('Lv', '리버모륨'), 117: ('Ts', '테네신'), 118: ('Og', '오가네손')
    }

    core_data = {
        1: (0.00, True, False, 1), 3: (-3.04, False, False, 1), 4: (-1.85, False, False, 2),
        6: (0.20, True, False, 4), 7: (-0.01, True, False, 3), 8: (1.23, True, False, 2),
        9: (2.87, True, False, 1), 11: (-2.71, False, False, 1), 12: (-2.37, False, False, 2),
        13: (-1.66, False, False, 3), 17: (1.36, True, False, 1), 19: (-2.93, False, False, 1),
        20: (-2.87, False, False, 2), 24: (-0.74, False, False, 3), 25: (-1.18, False, False, 2),
        26: (-0.44, False, False, 2), 27: (-0.28, False, False, 2), 28: (-0.25, False, False, 2),
        29: (0.34, False, False, 2), 30: (-0.76, False, False, 2), 35: (1.07, True, False, 1),
        47: (0.80, False, False, 1), 50: (-0.14, False, False, 2), 53: (0.54, True, False, 1),
        56: (-2.91, False, False, 2), 78: (1.18, False, False, 2), 79: (1.50, False, False, 3),
        80: (0.85, False, False, 2), 82: (-0.13, False, False, 2)
    }

    all_data = []
    for i in range(1, 119):
        symbol, name = element_dict[i]
        
        if i in core_data:
            potential, is_nonmetal, is_theo, ox_state = core_data[i]
        else:
            potential = round(0.5 - (i * 0.01), 2)
            is_theo = True if i >= 100 else False
            nonmetals = [1, 2, 5, 6, 7, 8, 9, 10, 14, 15, 16, 17, 18, 33, 34, 35, 36, 52, 53, 54, 85, 86, 117, 118]
            is_nonmetal = True if i in nonmetals else False
            ox_state = 2 
            
        all_data.append((i, symbol, name, potential, is_nonmetal, is_theo, ox_state))

    df_full = pd.DataFrame(all_data, columns=['원자번호', '기호', '한글이름', '표준환원전위', 'isNonMetal', 'isTheoretical', '산화수'])
    df_full['표시이름'] = df_full.apply(lambda x: f"{x['원자번호']:03d} - {x['한글이름']} ({x['기호']})", axis=1)
    return df_full

df = load_element_data()

# ==========================================
# 2. 전역 설정 및 공통 로직
# ==========================================
st.set_page_config(page_title="화학 전지 & 전기 분해 시뮬레이터", layout="wide", initial_sidebar_state="expanded")
st.title("🔋 화학 전지 & 전기 분해 시뮬레이터")
st.markdown("고등학교 화학 교과과정에 맞춘 **산화-환원 반응** 직관적 시뮬레이터입니다. 좌측에서 설정하고 우측에서 결과를 실시간으로 확인하세요.")

mode = st.sidebar.radio("🔬 학습 모드 선택", ["화학 전지 (자발적 반응)", "전기 분해 (비자발적 반응)"])

def check_smart_exceptions(element):
    if element['isNonMetal']:
        st.warning(f"⚠️ **{element['한글이름']}({element['기호']})**은(는) 기체/비금속 원소이므로 백금(Pt) 또는 탄소(C) 보조 전극을 사용합니다.")
    if element['isTheoretical']:
        st.info(f"ℹ️ **{element['한글이름']}**은(는) 현실에서 안정적으로 존재하기 힘들어 계산된 전압은 이론적 가상값입니다.")

def draw_galvanic_cell(anode, cathode):
    fig = go.Figure()
    fig.add_shape(type="rect", x0=1, y0=0, x1=3, y1=3, line=dict(color="black", width=2), fillcolor="lightblue", opacity=0.5)
    fig.add_shape(type="rect", x0=5, y0=0, x1=7, y1=3, line=dict(color="black", width=2), fillcolor="lightblue", opacity=0.5)
    fig.add_shape(type="rect", x0=1.7, y0=1, x1=2.3, y1=4, line=dict(color="black"), fillcolor="darkgray")
    fig.add_shape(type="rect", x0=5.7, y0=1, x1=6.3, y1=4, line=dict(color="black"), fillcolor="silver")
    fig.add_shape(type="line", x0=2, y0=4, x1=2, y1=5, line=dict(color="black", width=2))
    fig.add_shape(type="line", x0=6, y0=4, x1=6, y1=5, line=dict(color="black", width=2))
    fig.add_shape(type="line", x0=2, y0=5, x1=6, y1=5, line=dict(color="black", width=2))
    fig.add_shape(type="circle", x0=3.5, y0=4.5, x1=4.5, y1=5.5, line=dict(color="black", width=2), fillcolor="white")
    fig.add_annotation(x=4, y=5, text="<b>V</b>", showarrow=False, font=dict(size=20))
    fig.add_annotation(x=4, y=5.7, text="<b>e⁻ 이동 방향 →</b>", showarrow=False, font=dict(color="red", size=14))
    fig.add_shape(type="path", path="M 2.5 2 C 2.5 4.5, 5.5 4.5, 5.5 2", line=dict(color="green", width=15), opacity=0.6)
    fig.add_annotation(x=4, y=3.7, text="염다리", showarrow=False, font=dict(color="darkgreen", size=12))
    fig.add_annotation(x=2, y=0.5, text=f"(-) 산화극<br>{anode['기호']}", showarrow=False, font=dict(size=14, color="black"))
    fig.add_annotation(x=6, y=0.5, text=f"(+) 환원극<br>{cathode['기호']}", showarrow=False, font=dict(size=14, color="black"))
    fig.update_layout(xaxis=dict(visible=False, range=[0, 8]), yaxis=dict(visible=False, range=[0, 6]), margin=dict(l=0, r=0, t=10, b=10), height=350)
    st.plotly_chart(fig, use_container_width=True)

def draw_electrolytic_cell(anode, cathode):
    fig = go.Figure()
    fig.add_shape(type="rect", x0=1, y0=0, x1=7, y1=3, line=dict(color="black", width=2), fillcolor="lightblue", opacity=0.5)
    fig.add_shape(type="rect", x0=2.5, y0=1, x1=3.1, y1=4, line=dict(color="black"), fillcolor="darkgray")
    fig.add_shape(type="rect", x0=4.9, y0=1, x1=5.5, y1=4, line=dict(color="black"), fillcolor="silver")
    fig.add_shape(type="line", x0=2.8, y0=4, x1=2.8, y1=5, line=dict(color="black", width=2))
    fig.add_shape(type="line", x0=5.2, y0=4, x1=5.2, y1=5, line=dict(color="black", width=2))
    fig.add_shape(type="line", x0=2.8, y0=5, x1=3.8, y1=5, line=dict(color="black", width=2))
    fig.add_shape(type="line", x0=4.2, y0=5, x1=5.2, y1=5, line=dict(color="black", width=2))
    fig.add_shape(type="line", x0=3.8, y0=4.6, x1=3.8, y1=5.4, line=dict(color="red", width=3)) 
    fig.add_shape(type="line", x0=4.2, y0=4.8, x1=4.2, y1=5.2, line=dict(color="blue", width=5)) 
    fig.add_annotation(x=3.8, y=5.7, text="(+)", showarrow=False, font=dict(color="red"))
    fig.add_annotation(x=4.2, y=5.7, text="(-)", showarrow=False, font=dict(color="blue"))
    fig.add_annotation(x=4, y=6.2, text="외부 전원 장치", showarrow=False, font=dict(size=14))
    fig.add_annotation(x=2.5, y=5.3, text="<b>e⁻ →</b>", showarrow=False, font=dict(color="red"))
    fig.add_annotation(x=5.5, y=5.3, text="<b>e⁻ →</b>", showarrow=False, font=dict(color="blue"))
    fig.add_annotation(x=2.8, y=0.5, text=f"(+) 산화극<br>{anode['기호']}", showarrow=False, font=dict(size=14, color="black"))
    fig.add_annotation(x=5.2, y=0.5, text=f"(-) 환원극<br>{cathode['기호']}", showarrow=False, font=dict(size=14, color="black"))
    fig.update_layout(xaxis=dict(visible=False, range=[0, 8]), yaxis=dict(visible=False, range=[0, 7]), margin=dict(l=0, r=0, t=10, b=10), height=350)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==========================================
# 3. 레이아웃 분할 (좌: 설정 / 우: 결과)
# ==========================================
left_col, right_col = st.columns([1, 1.5], gap="large")

if "화학 전지" in mode:
    with left_col:
        st.subheader("🎛️ 전극 및 전해질 설정")
        st.info("💡 **Tip:** 선택창을 클릭하고 '수소', 'Cu', '11' 등을 키보드로 타이핑하면 바로 검색됩니다.")
        
        elem1_str = st.selectbox("첫 번째 원소 (검색/선택)", df['표시이름'].tolist(), index=29) # Zn
        elem2_str = st.selectbox("두 번째 원소 (검색/선택)", df['표시이름'].tolist(), index=28) # Cu
            
        e1 = df[df['표시이름'] == elem1_str].iloc[0]
        e2 = df[df['표시이름'] == elem2_str].iloc[0]
        
        # 산화극 환원극 자동 판별
        if e1['표준환원전위'] < e2['표준환원전위']:
            anode, cathode = e1, e2
        else:
            anode, cathode = e2, e1
            
        st.markdown("---")
        st.markdown("#### ⚗️ 부가 재료 선택")
        sel1 = st.selectbox("산화극 전해질", [f"{anode['기호']}(NO₃)₂ 수용액", f"{anode['기호']}SO₄ 수용액", "기타"])
        sel2 = st.selectbox("환원극 전해질", [f"{cathode['기호']}(NO₃)₂ 수용액", f"{cathode['기호']}SO₄ 수용액", "기타"])
        sel3 = st.selectbox("염다리 물질", ["KNO₃", "KCl", "NH₄NO₃"])
        
    with right_col:
        st.subheader("📊 반응 결과 및 시각화")
        if e1['원자번호'] == e2['원자번호']:
            st.error("서로 다른 두 원소를 선택해주세요.")
        else:
            e_cell = cathode['표준환원전위'] - anode['표준환원전위']
            
            # 메트릭 표시 (가로 정렬)
            m1, m2, m3 = st.columns(3)
            m1.metric("(-) 산화극", f"{anode['기호']} (E°= {anode['표준환원전위']:.2f}V)")
            m2.metric("(+) 환원극", f"{cathode['기호']} (E°= {cathode['표준환원전위']:.2f}V)")
            m3.metric("표준 기전력", f"{e_cell:.2f} V", "자발적" if e_cell > 0 else "")
            
            # 여기서 예외 처리 경고문 출력! (반응 결과 수치 바로 밑)
            check_smart_exceptions(anode)
            check_smart_exceptions(cathode)
            
            draw_galvanic_cell(anode, cathode)
            
            st.latex(fr"\text{{[(-) 산화극]}} : {anode['기호']} \rightarrow {anode['기호']}^{{{anode['산화수']}+}} + {anode['산화수']}e^-")
            st.latex(fr"\text{{[(+) 환원극]}} : {cathode['기호']}^{{{cathode['산화수']}+}} + {cathode['산화수']}e^- \rightarrow {cathode['기호']}")
            st.latex(fr"\text{{[전체 반응식]}} : {cathode['산화수']}{anode['기호']} + {anode['산화수']}{cathode['기호']}^{{{cathode['산화수']}+}} \rightarrow {cathode['산화수']}{anode['기호']}^{{{anode['산화수']}+}} + {anode['산화수']}{cathode['기호']}")

else:
    with left_col:
        st.subheader("🎛️ 전극 및 전해질 설정")
        st.info("💡 **Tip:** 선택창을 클릭하고 '수소', 'Cu', '11' 등을 키보드로 타이핑하면 바로 검색됩니다.")
        
        st.markdown("**(+)극 연결 원소 (산화 반응)**")
        anode_str = st.selectbox("(+)극 선택 (검색 가능)", df['표시이름'].tolist(), index=28) # Cu
        
        st.markdown("**(-)극 연결 원소 (환원 반응)**")
        cathode_str = st.selectbox("(-)극 선택 (검색 가능)", df['표시이름'].tolist(), index=46) # Ag
            
        anode = df[df['표시이름'] == anode_str].iloc[0]
        cathode = df[df['표시이름'] == cathode_str].iloc[0]
        
        st.markdown("---")
        st.markdown("#### ⚗️ 전해질 통합 선택")
        st.selectbox("전해질 (수용액 또는 용융액)", [f"황산 구리({anode['기호']}SO₄) 수용액", f"염화 나트륨(NaCl) 용융액", "기타 수용액"])
        
    with right_col:
        st.subheader("📊 반응 결과 및 시각화")
        
        e_cell_reverse = cathode['표준환원전위'] - anode['표준환원전위']
        min_voltage = abs(e_cell_reverse) if e_cell_reverse < 0 else 0.0
        
        m1, m2, m3 = st.columns(3)
        m1.metric("(+) 산화극 (전원+)", f"{anode['기호']} ({anode['표준환원전위']:.2f}V)")
        m2.metric("(-) 환원극 (전원-)", f"{cathode['기호']} ({cathode['표준환원전위']:.2f}V)")
        m3.metric("이론적 최소 전압", f"{min_voltage:.2f} V", "비자발적" if e_cell_reverse < 0 else "자발적", delta_color="inverse")
        
        # 여기서 예외 처리 경고문 출력! (반응 결과 수치 바로 밑)
        check_smart_exceptions(anode)
        check_smart_exceptions(cathode)
        
        draw_electrolytic_cell(anode, cathode)
        
        st.latex(fr"\text{{[(+) 산화극]}} : {anode['기호']} \rightarrow {anode['기호']}^{{{anode['산화수']}+}} + {anode['산화수']}e^-")
        st.latex(fr"\text{{[(-) 환원극]}} : {cathode['기호']}^{{{cathode['산화수']}+}} + {cathode['산화수']}e^- \rightarrow {cathode['기호']}")
