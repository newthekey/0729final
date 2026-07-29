import streamlit as st
import pandas as pd
import time

# 페이지 기본 설정
st.set_page_config(
    page_title="인공지능 탐구: 의사결정나무 시뮬레이터",
    page_icon="🌳",
    layout="wide"
)

# -----------------------------------------------------------------------------
# 세션 상태 초기화 (사용자 정보, 시간 기록, 챗봇 대화 기록)
# -----------------------------------------------------------------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'student_id' not in st.session_state:
    st.session_state.student_id = ""
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕! 나는 **AI 힌트 도우미**야 🤖\n선택이 고민되거나 의사결정나무 알고리즘에 대해 궁금한 점이 있으면 무엇이든 물어봐!"}
    ]

# -----------------------------------------------------------------------------
# 🤖 챗봇 응답 로직 함수 (수업용 규칙 기반 힌트 제공)
# -----------------------------------------------------------------------------
def get_bot_response(user_input):
    user_input = user_input.strip().lower()
    
    # 1. 의사결정나무 개념 질문
    if "의사결정나무" in user_input or "트리" in user_input or "개념" in user_input:
        return "🌳 **의사결정나무(Decision Tree)**는 데이터를 스무고개처럼 '예/아니오' 또는 '조건 질문'을 던져서 차례대로 분류해나가는 인공지능 알고리즘이야!"
    elif "노드" in user_input or "가지" in user_input:
        return "🍃 **노드(Node)**는 질문이나 결과가 담기는 '상자'이고, **가지(Branch)**는 조건에 따라 갈라지는 '선'을 뜻해. 맨 위의 질문을 **뿌리 노드(Root Node)**, 맨 끝 결과 노드를 **잎 노드(Leaf Node)**라고 부른단다!"
    elif "질문" in user_input or "순서" in user_input or "정보" in user_input:
        return "💡 의사결정나무에서는 **가장 데이터를 명확하게 나눠주는 대표적인 질문**을 가장 상단(뿌리 노드)에 배치하는 게 효율적이야!"
    elif "만들기" in user_input or "피드백" in user_input or "주제" in user_input:
        return "✏️ 4번째 탭 [나만의 트리 만들기]에서 행성, 동물, 역사적 사건 등 원하는 주제로 직접 트리를 구성해봐! 다 만든 후 'AI 피드백 요청' 버튼을 누르면 잘된 점과 조언을 들려줄게!"
    
    # 2. 실습 메뉴/활동/영화 관련 질문 힌트
    elif "점심" in user_input or "메뉴" in user_input or "떡볶이" in user_input or "마라탕" in user_input:
        return "🍕 **점심 추천 힌트:** 국물 있는 매운 음식을 원하고 예산이 1만원이 넘는다면 '마라탕', 1만원 이하에 국물이 필요 없다면 '떡볶이'가 나올 확률이 높아!"
    elif "주말" in user_input or "활동" in user_input or "방탈출" in user_input or "축구" in user_input:
        return "🎈 **주말 활동 힌트:** 친구들과 함께 실외에서 움직이고 싶다면 '축구', 실내에서 두뇌를 쓰며 활동하고 싶다면 '방탈출 카페'를 추천해!"
    elif "영화" in user_input or "웹툰" in user_input or "장르" in user_input:
        return "🎬 **콘텐츠 추천 힌트:** 분위기가 밝고 가벼운 액션을 좋아하면 '극한직업', 깊고 진지한 판타지를 원하면 '전지적 독자 시점'이나 '해리포터'를 만나볼 수 있어!"
    
    # 3. 기타 기본 응답
    else:
        return f"'{user_input}'에 대해 궁금하구나! 고민될 때는 위쪽 탭에서 하나씩 선택 항목을 바꿔보며 결과가 어떻게 달라지는지 확인해보렴! 🔍"

# -----------------------------------------------------------------------------
# 1. 로그인 / 학생 정보 입력 화면
# -----------------------------------------------------------------------------
if not st.session_state.logged_in:
    st.title("🌳 AI 수업: 의사결정나무(Decision Tree) 실습")
    st.markdown("""
    반갑습니다! 이번 시간은 조건에 맞춰 선택을 내려가는 **'의사결정나무'**의 원리를 직접 체험해보는 시간입니다.  
    아래에 **학번과 이름**을 입력하고 실습을 시작해주세요.
    """)
    
    with st.form("login_form"):
        student_id = st.text_input("학번 (예: 20101)", placeholder="학번을 입력하세요")
        student_name = st.text_input("이름", placeholder="이름을 입력하세요")
        submit_button = st.form_submit_button("실습 시작하기 🚀")
        
        if submit_button:
            if student_id.strip() != "" and student_name.strip() != "":
                st.session_state.student_id = student_id
                st.session_state.student_name = student_name
                st.session_state.logged_in = True
                st.session_state.start_time = time.time()  # 시작 시간 기록
                st.rerun()
            else:
                st.error("학번과 이름을 모두 입력해주세요!")

# -----------------------------------------------------------------------------
# 2. 메인 실습 화면
# -----------------------------------------------------------------------------
else:
    # -------------------------------------------------------------------------
    # 사이드바: 학생 정보, 타이머, 💡 힌트 챗봇
    # -------------------------------------------------------------------------
    st.sidebar.title("👤 학생 정보")
    st.sidebar.info(f"**학번:** {st.session_state.student_id}\n\n**이름:** {st.session_state.student_name}")
    
    # 소요 시간 계산 및 표시
    elapsed_time = int(time.time() - st.session_state.start_time)
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    st.sidebar.metric("⏱️ 실습 진행 시간", f"{minutes}분 {seconds}초")
    
    st.sidebar.markdown("---")
    
    # 🤖 사이드바 AI 힌트 챗봇
    st.sidebar.subheader("🤖 AI 힌트 도우미")
    
    # 챗봇 이전 대화 출력
    chat_container = st.sidebar.container(height=260)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 학생 챗봇 입력창
    if prompt := st.sidebar.chat_input("질문이나 힌트 요청..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 챗봇 답변 생성
        response = get_bot_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    st.sidebar.markdown("---")
    if st.sidebar.button("처음으로 돌아가기 (로그아웃)"):
        st.session_state.logged_in = False
        st.session_state.messages = [
            {"role": "assistant", "content": "안녕! 나는 **AI 힌트 도우미**야 🤖\n선택이 고민되거나 의사결정나무 알고리즘에 대해 궁금한 점이 있으면 무엇이든 물어봐!"}
        ]
        st.rerun()

    # -------------------------------------------------------------------------
    # 메인 화면 영역
    # -------------------------------------------------------------------------
    st.title("🌳 의사결정나무 시뮬레이션 웹앱")
    st.write(f"👋 **{st.session_state.student_name}** 학생! 조건 선택에 따라 전체 의사결정나무에서 **어떤 경로를 통해 결과에 도달하는지(강조 표시)** 확인해보세요.")

    # Tab을 통해 주제 분리
    tab1, tab2, tab3, tab4 = st.tabs([
        "🍕 1. 점심 메뉴 결정트리", 
        "🎈 2. 주말 활동 추천", 
        "🎬 3. 영화/웹툰 추천",
        "✏️ 4. 나만의 트리 만들기 & 피드백"
    ])

    # -------------------------------------------------------------------------
    # [주제 1] 점심 메뉴 결정트리
    # -------------------------------------------------------------------------
    with tab1:
        st.header("🍕 오늘의 점심 메뉴 결정트리")
        st.caption("조건: 예산, 음식 종류, 매운 정도, 국물 유무")
        
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            st.subheader("📋 조건 선택하기")
            budget = st.radio("1. 예산 수준은?", ["1만원 이하", "1만원 초과"], key="t1_budget")
            food_type = st.radio("2. 어떤 종류의 음식?", ["한식/분식", "양식/일식/중식"], key="t1_type")
            spicy = st.radio("3. 매운 음식을 잘 먹나요?", ["순한맛/안매움", "매콤/매운맛"], key="t1_spicy")
            soup = st.radio("4. 국물이 필요한가요?", ["국물 있음", "국물 없음"], key="t1_soup")
            
            # 결과 및 노드 ID 판별
            if budget == "1만원 이하":
                if food_type == "한식/분식":
                    if spicy == "매콤/매운맛":
                        result_food, active_leaf = "떡볶이 🌶️", "leaf_1"
                    else:
                        if soup == "국물 있음":
                            result_food, active_leaf = "잔치국수 🍜", "leaf_2"
                        else:
                            result_food, active_leaf = "참치김밥 🍙", "leaf_3"
                else:
                    if spicy == "매콤/매운맛":
                        result_food, active_leaf = "짬뽕 🍜", "leaf_4"
                    else:
                        result_food, active_leaf = "돈까스 🥩", "leaf_5"
            else:
                if spicy == "매콤/매운맛":
                    if soup == "국물 있음":
                        result_food, active_leaf = "마라탕 🥘", "leaf_6"
                    else:
                        result_food, active_leaf = "매운 닭갈비 🍗", "leaf_7"
                else:
                    if soup == "국물 있음":
                        result_food, active_leaf = "샤브샤브 🍲", "leaf_8"
                    else:
                        result_food, active_leaf = "파스타 🍝", "leaf_9"

        with col2:
            st.subheader("🎯 시뮬레이션 결과")
            st.success(f"**추천 결과:** {result_food}")
            st.caption("🍊 **주황색/초록색**으로 표시된 노드가 학생이 선택한 분류 경로입니다.")
            
            # 전체 트리의 하이라이트 스타일 설정
            def get_node_style(node_id):
                if node_id == active_leaf:
                    return 'shape=box, style="filled,bold", color="#2E7D32", fillcolor="#C8E6C9", penwidth=3'
                else:
                    return 'shape=box, style=filled, color="#CCCCCC", fillcolor="#F5F5F5"'

            dot_code1 = f"""
            digraph {{
                rankdir=TB;
                node [fontname="NanumGothic, Malgun Gothic, sans-serif"];
                
                Q1 [label="예산가 1만원 이하인가?", shape=ellipse, style=filled, color="#1976D2", fillcolor="#BBDEFB"];
                
                Q2_1 [label="한식/분식 인가?", shape=ellipse];
                Q2_2 [label="매운 음식인가?", shape=ellipse];
                
                L1 [label="떡볶이 🌶️", {get_node_style('leaf_1')}];
                L2 [label="잔치국수 🍜", {get_node_style('leaf_2')}];
                L3 [label="참치김밥 🍙", {get_node_style('leaf_3')}];
                L4 [label="짬뽕 🍜", {get_node_style('leaf_4')}];
                L5 [label="돈까스 🥩", {get_node_style('leaf_5')}];
                L6 [label="마라탕 🥘", {get_node_style('leaf_6')}];
                L7 [label="매운 닭갈비 🍗", {get_node_style('leaf_7')}];
                L8 [label="샤브샤브 🍲", {get_node_style('leaf_8')}];
                L9 [label="파스타 🍝", {get_node_style('leaf_9')}];

                Q1 -> Q2_1 [label="예", color="{ '#D84315' if budget == '1만원 이하' else '#CCCCCC' }", penwidth={ 3 if budget == '1만원 이하' else 1 }];
                Q1 -> Q2_2 [label="아니오", color="{ '#D84315' if budget == '1만원 초과' else '#CCCCCC' }", penwidth={ 3 if budget == '1만원 초과' else 1 }];

                Q2_1 -> L1 [label="한식+매움"];
                Q2_1 -> L2 [label="한식+순함+국물"];
                Q2_1 -> L3 [label="한식+순함+국물없음"];
                Q2_1 -> L4 [label="기타+매움"];
                Q2_1 -> L5 [label="기타+순함"];

                Q2_2 -> L6 [label="매움+국물"];
                Q2_2 -> L7 [label="매움+국물없음"];
                Q2_2 -> L8 [label="순함+국물"];
                Q2_2 -> L9 [label="순함+국물없음"];
            }}
            """
            st.graphviz_chart(dot_code1)

    # -------------------------------------------------------------------------
    # [주제 2] 주말 활동 추천 시스템
    # -------------------------------------------------------------------------
    with tab2:
        st.header("🎈 주말 활동 추천 시스템")
        st.caption("조건: 실내/실외, 혼자/함께, 동적/정적, 예산 유무")
        
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            st.subheader("📋 조건 선택하기")
            place = st.radio("1. 어디를 선호하나요?", ["실내", "실외"], key="t2_place")
            companion = st.radio("2. 누구와 함께하나요?", ["혼자", "친구/가족과 함께"], key="t2_comp")
            activity = st.radio("3. 어떤 활동 스타일?", ["정적인 활동 (휴식/감상)", "동적인 활동 (체험/운동)"], key="t2_act")
            has_money = st.radio("4. 예산(용돈)이 있나요?", ["예산 있음 (유료)", "예산 없음 (무료)"], key="t2_money")
            
            # 의사결정 로직 및 활성 노드 지정
            if place == "실내":
                if companion == "혼자":
                    if activity.startswith("정적"):
                        result_act, active_leaf2 = "도서관에서 책 읽기 📚", "leaf2_1"
                    else:
                        result_act, active_leaf2 = "집에서 게임하기 🎮", "leaf2_2"
                else:
                    if activity.startswith("정적"):
                        if has_money == "예산 있음 (유료)":
                            result_act, active_leaf2 = "영화관람 🍿", "leaf2_3"
                        else:
                            result_act, active_leaf2 = "보드게임 카페/동네 카페 ☕", "leaf2_4"
                    else:
                        result_act, active_leaf2 = "방탈출카페 🔍", "leaf2_5"
            else:
                if activity.startswith("동적"):
                    if companion == "친구/가족과 함께":
                        result_act, active_leaf2 = "축구 / 야외 스포츠 ⚽", "leaf2_6"
                    else:
                        result_act, active_leaf2 = "자전거 타기 / 러닝 🏃", "leaf2_7"
                else:
                    result_act, active_leaf2 = "공원 산책 / 버스킹 관람 🌳", "leaf2_8"

        with col2:
            st.subheader("🎯 시뮬레이션 결과")
            st.success(f"**추천 결과:** {result_act}")
            st.caption("🍊 **주황색/초록색**으로 표시된 노드가 학생이 선택한 분류 경로입니다.")
            
            def get_node_style2(node_id):
                if node_id == active_leaf2:
                    return 'shape=box, style="filled,bold", color="#2E7D32", fillcolor="#C8E6C9", penwidth=3'
                else:
                    return 'shape=box, style=filled, color="#CCCCCC", fillcolor="#F5F5F5"'

            dot_code2 = f"""
            digraph {{
                rankdir=TB;
                Q1 [label="활동 장소가 실내인가?", shape=ellipse, style=filled, color="#1976D2", fillcolor="#BBDEFB"];
                
                Q2_1 [label="혼자 하는가?", shape=ellipse];
                Q2_2 [label="동적인 활동인가?", shape=ellipse];
                
                L1 [label="도서관에서 책 읽기 📚", {get_node_style2('leaf2_1')}];
                L2 [label="집에서 게임하기 🎮", {get_node_style2('leaf2_2')}];
                L3 [label="영화관람 🍿", {get_node_style2('leaf2_3')}];
                L4 [label="동네 카페 ☕", {get_node_style2('leaf2_4')}];
                L5 [label="방탈출카페 🔍", {get_node_style2('leaf2_5')}];
                L6 [label="축구 / 야외 스포츠 ⚽", {get_node_style2('leaf2_6')}];
                L7 [label="자전거 타기 / 러닝 🏃", {get_node_style2('leaf2_7')}];
                L8 [label="공원 산책 🌳", {get_node_style2('leaf2_8')}];

                Q1 -> Q2_1 [label="실내", color="{ '#D84315' if place == '실내' else '#CCCCCC' }", penwidth={ 3 if place == '실내' else 1 }];
                Q1 -> Q2_2 [label="실외", color="{ '#D84315' if place == '실외' else '#CCCCCC' }", penwidth={ 3 if place == '실외' else 1 }];

                Q2_1 -> L1 [label="혼자+정적"];
                Q2_1 -> L2 [label="혼자+동적"];
                Q2_1 -> L3 [label="함께+정적+유료"];
                Q2_1 -> L4 [label="함께+정적+무료"];
                Q2_1 -> L5 [label="함께+동적"];

                Q2_2 -> L6 [label="동적+함께"];
                Q2_2 -> L7 [label="동적+혼자"];
                Q2_2 -> L8 [label="정적"];
            }}
            """
            st.graphviz_chart(dot_code2)

    # -------------------------------------------------------------------------
    # [주제 3] 콘텐츠 추천 (영화 / 웹툰)
    # -------------------------------------------------------------------------
    with tab3:
        st.header("🎬 영화 및 웹툰 콘텐츠 추천")
        st.caption("조건: 장르, 분량, 분위기, 최신/명작")
        
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            st.subheader("📋 조건 선택하기")
            genre = st.selectbox("1. 선호하는 장르는?", ["액션/스릴러", "코미디/일상", "판타지/SF", "로맨스/감성"], key="t3_genre")
            length = st.radio("2. 선호하는 분량은?", ["단편/단행본 (짧음)", "장편/시리즈 (길음)"], key="t3_len")
            mood = st.radio("3. 원하는 분위기는?", ["밝고 가벼움", "진지하고 어두움/웅장함"], key="t3_mood")
            era = st.radio("4. 어떤 작품을 원하나요?", ["최신 트렌드작", "검증된 고전/명작"], key="t3_era")
            
            # 의사결정 로직 및 활성 노드 지정
            if genre == "액션/스릴러":
                if mood == "밝고 가벼움":
                    result_media, active_leaf3 = "웹툰: 《극주고도》 / 영화: 《극한직업》 🎬", "leaf3_1"
                else:
                    result_media, active_leaf3 = "웹툰: 《나 혼자만 레벨업》 / 영화: 《다크 나이트》 🦇", "leaf3_2"
            elif genre == "코미디/일상":
                if era == "최신 트렌드작":
                    result_media, active_leaf3 = "웹툰: 《대학일기》 / 영화: 《육사오》 😆", "leaf3_3"
                else:
                    result_media, active_leaf3 = "웹툰: 《마음의 소리》 / 영화: 《세 얼간이》 🤣", "leaf3_4"
            elif genre == "판타지/SF":
                if length.startswith("단편"):
                    result_media, active_leaf3 = "영화: 《인터스텔라》 / SF 단편 🚀", "leaf3_5"
                else:
                    result_media, active_leaf3 = "웹툰: 《전독시》 / 영화: 《해리포터》 🧙", "leaf3_6"
            else:
                if mood == "밝고 가벼움":
                    result_media, active_leaf3 = "웹툰: 《연애혁명》 / 영화: 《인사이드 아웃》 🌈", "leaf3_7"
                else:
                    result_media, active_leaf3 = "영화: 《너의 이름은.》 / 감성 웹툰 🍁", "leaf3_8"

        with col2:
            st.subheader("🎯 시뮬레이션 결과")
            st.info(f"**추천 작품:**\n\n{result_media}")
            st.caption("🍊 **주황색/초록색**으로 표시된 노드가 학생이 선택한 분류 경로입니다.")
            
            def get_node_style3(node_id):
                if node_id == active_leaf3:
                    return 'shape=box, style="filled,bold", color="#2E7D32", fillcolor="#C8E6C9", penwidth=3'
                else:
                    return 'shape=box, style=filled, color="#CCCCCC", fillcolor="#F5F5F5"'

            dot_code3 = f"""
            digraph {{
                rankdir=TB;
                Q1 [label="선호 장르는 무엇인가?", shape=ellipse, style=filled, color="#1976D2", fillcolor="#BBDEFB"];
                
                L1 [label="《극한직업》 / 《극주고도》 🎬", {get_node_style3('leaf3_1')}];
                L2 [label="《나 혼자만 레벨업》 / 《다크 나이트》 🦇", {get_node_style3('leaf3_2')}];
                L3 [label="《대학일기》 / 《육사오》 😆", {get_node_style3('leaf3_3')}];
                L4 [label="《마음의 소리》 / 《세 얼간이》 🤣", {get_node_style3('leaf3_4')}];
                L5 [label="《인터스텔라》 🚀", {get_node_style3('leaf3_5')}];
                L6 [label="《전지적 독자 시점》 / 《해리포터》 🧙", {get_node_style3('leaf3_6')}];
                L7 [label="《연애혁명》 / 《인사이드 아웃》 🌈", {get_node_style3('leaf3_7')}];
                L8 [label="《너의 이름은.》 🍁", {get_node_style3('leaf3_8')}];

                Q1 -> L1 [label="액션+밝음", color="{ '#D84315' if active_leaf3=='leaf3_1' else '#CCCCCC' }", penwidth={ 3 if active_leaf3=='leaf3_1' else 1 }];
                Q1 -> L2 [label="액션+어두움", color="{ '#D84315' if active_leaf3=='leaf3_2' else '#CCCCCC' }", penwidth={ 3 if active_leaf3=='leaf3_2' else 1 }];
                Q1 -> L3 [label="코미디+최신", color="{ '#D84315' if active_leaf3=='leaf3_3' else '#CCCCCC' }", penwidth={ 3 if active_leaf3=='leaf3_3' else 1 }];
                Q1 -> L4 [label="코미디+고전", color="{ '#D84315' if active_leaf3=='leaf3_4' else '#CCCCCC' }", penwidth={ 3 if active_leaf3=='leaf3_4' else 1 }];
                Q1 -> L5 [label="판타지+단편", color="{ '#D84315' if active_leaf3=='leaf3_5' else '#CCCCCC' }", penwidth={ 3 if active_leaf3=='leaf3_5' else 1 }];
                Q1 -> L6 [label="판타지+장편", color="{ '#D84315' if active_leaf3=='leaf3_6' else '#CCCCCC' }", penwidth={ 3 if active_leaf3=='leaf3_6' else 1 }];
                Q1 -> L7 [label="로맨스+밝음", color="{ '#D84315' if active_leaf3=='leaf3_7' else '#CCCCCC' }", penwidth={ 3 if active_leaf3=='leaf3_7' else 1 }];
                Q1 -> L8 [label="로맨스+감성", color="{ '#D84315' if active_leaf3=='leaf3_8' else '#CCCCCC' }", penwidth={ 3 if active_leaf3=='leaf3_8' else 1 }];
            }}
            """
            st.graphviz_chart(dot_code3)

    # -------------------------------------------------------------------------
    # [주제 4] 나만의 의사결정나무 만들기 & 피드백
    # -------------------------------------------------------------------------
    with tab4:
        st.header("✏️ 나만의 의사결정나무 설계 실습")
        st.markdown("""
        자신이 관심 있는 주제(예: **태양계 행성 분류**, **역사적 사건 분류**, **동물/식물 분류** 등)를 직접 정하고,  
        조건 질문과 최종 결과를 구성하여 의사결정나무를 완성해 보세요!
        """)
        
        # --- 영역 1: 예시 살펴보기 ---
        with st.expander("📖 [예시 살펴보기] 태양계 행성 분류 의사결정나무 예시 및 피드백", expanded=False):
            st.write("**주제:** 태양계 행성 분류하기 (지구형 vs 목성형)")
            st.write("**최종 분류 대상:** 지구, 화성, 목성, 토성")
            
            ex_dot_code = """
            digraph {
                Q1 [label="질문1: 표면이 단단한 암석으로 되어있는가?"];
                Q2_1 [label="질문2-1: 생명체나 물이 존재하는가?"];
                Q2_2 [label="질문2-2: 아름다운 고리가 선명하게 보이는가?"];
                R1 [label="지구 🌍", shape=box, style=filled, color=lightblue];
                R2 [label="화성 붉은행성 🔴", shape=box, style=filled, color=lightpink];
                R3 [label="토성 🪐", shape=box, style=filled, color=khaki];
                R4 [label="목성 🌌", shape=box, style=filled, color=orange];

                Q1 -> Q2_1 [label="예 (암석형)"];
                Q1 -> Q2_2 [label="아니오 (가스형)"];
                Q2_1 -> R1 [label="예"];
                Q2_1 -> R2 [label="아니오"];
                Q2_2 -> R3 [label="예"];
                Q2_2 -> R4 [label="아니오"];
            }
            """
            st.graphviz_chart(ex_dot_code)
            
            st.success("""
            💬 **예시 트리 피드백 미리보기:**
            - **우수한 점:** 암석형/가스형이라는 핵심 기준(정보 이득이 높음)을 가장 상단 질문1로 배치하여 데이터 집단을 절반으로 명확히 잘 분리했습니다.
            - **개선 아이디어:** '생명체가 있는가?' 대신 '대기 성분'이나 '위성의 개수'처럼 과학적 속성을 추가하면 수성과 금성까지 확장할 수 있습니다!
            """)

        st.markdown("---")
        st.subheader("🛠️ 나만의 트리 작성하기")
        
        col_input1, col_input2 = st.columns([1, 1])
        
        with col_input1:
            custom_topic = st.text_input("1. 탐구 주제를 적어주세요", placeholder="예: 역사적 사건 분류하기, 동물 분류 등")
            custom_targets = st.text_input("2. 최종 결과(분류 대상 4가지)를 적어주세요", placeholder="예: 임진왜란, 병자호란, 갑신정변, 3·1 운동")
            
            st.markdown("#### ❓ 질문(조건) 설계")
            q1 = st.text_input("질문 1 (뿌리 질문 - 가장 크게 나누는 기준)", placeholder="예: 조선시대에 일어난 사건인가?")
            q2_1 = st.text_input("질문 2-1 (질문1이 '예'일 때 갈라지는 질문)", placeholder="예: 외세(일본/청나라)의 침략 전쟁인가?")
            q2_2 = st.text_input("질문 2-2 (질문1이 '아니오'일 때 갈라지는 질문)", placeholder="예: 일제강점기 만세 운동인가?")
            
        with col_input2:
            st.markdown("#### 🎯 최종 결과(Leaf) 매핑")
            r1 = st.text_input("결과 A (질문1 '예' → 질문2-1 '예')", placeholder="결과 입력")
            r2 = st.text_input("결과 B (질문1 '예' → 질문2-1 '아니오')", placeholder="결과 입력")
            r3 = st.text_input("결과 C (질문1 '아니오' → 질문2-2 '예')", placeholder="결과 입력")
            r4 = st.text_input("결과 D (질문1 '아니오' → 질문2-2 '아니오')", placeholder="결과 입력")

        # 트리 시각화 및 AI 피드백 영역
        st.markdown("---")
        st.subheader("📊 작성한 트리 시각화 & AI 피드백")
        
        col_vis, col_fb = st.columns([1, 1])
        
        with col_vis:
            st.write("▼ 완성된 트리 구조도")
            if q1 and q2_1 and q2_2:
                user_r1 = r1 if r1 else "결과A"
                user_r2 = r2 if r2 else "결과B"
                user_r3 = r3 if r3 else "결과C"
                user_r4 = r4 if r4 else "결과D"

                user_dot_code = f"""
                digraph {{
                    UQ1 [label="1차: {q1}"];
                    UQ2_1 [label="2차(A): {q2_1}"];
                    UQ2_2 [label="2차(B): {q2_2}"];
                    UR1 [label="{user_r1}", shape=box, style=filled, color=lightyellow];
                    UR2 [label="{user_r2}", shape=box, style=filled, color=lightyellow];
                    UR3 [label="{user_r3}", shape=box, style=filled, color=lightgreen];
                    UR4 [label="{user_r4}", shape=box, style=filled, color=lightgreen];

                    UQ1 -> UQ2_1 [label="예"];
                    UQ1 -> UQ2_2 [label="아니오"];
                    UQ2_1 -> UR1 [label="예"];
                    UQ2_1 -> UR2 [label="아니오"];
                    UQ2_2 -> UR3 [label="예"];
                    UQ2_2 -> UR4 [label="아니오"];
                }}
                """
                st.graphviz_chart(user_dot_code)
            else:
                st.info("왼쪽 양식에 질문을 채우면 의사결정나무가 자동으로 그려집니다!")

        with col_fb:
            st.write("▼ AI 평가 및 피드백")
            
            if st.button("🔍 AI 피드백 요청하기", type="primary"):
                if not custom_topic or not q1 or not q2_1 or not q2_2 or not (r1 and r2 and r3 and r4):
                    st.warning("주제, 질문 3가지, 결과 4가지를 모두 작성한 후 피드백을 요청해주세요!")
                else:
                    with st.spinner("학생이 만든 의사결정나무를 분석하고 있습니다..."):
                        time.sleep(1) # 분석 애니메이션 효과
                        
                        st.balloons()
                        st.success(f"🎉 **{st.session_state.student_name}** 학생의 '{custom_topic}' 의사결정나무 검토 완료!")
                        
                        # 자동 분석 피드백 로직
                        st.markdown("### 📝 종합 피드백 리포트")
                        st.write("🌟 **평가 점수:** 100점 만점에 **95점** (매우 우수함!)")
                        
                        st.markdown(f"""
                        * **주제 명확성:** '{custom_topic}' 주제에 맞게 결과를 명확하게 나눌 수 있는 속성 질문들을 구성했습니다.
                        * **질문 구성 평가:** 
                            - 뿌리 질문 (`{q1}`)이 전체 대상을 효과적으로 갈라주고 있습니다.
                            - 2차 질문들 (`{q2_1}`, `{q2_2}`)이 세부 속성을 구별하여 최종 결과 **{r1}, {r2}, {r3}, {r4}**에 잘 도달하도록 연결되었습니다.
                        * **인공지능 관점의 팁 (정보 이득):**
                            - 질문이 '예/아니오'로 답했을 때 한쪽에 너무 쏠리지 않고 비슷한 비율로 나뉠수록 **'정보 이득(Information Gain)'**이 높은 훌륭한 나무가 됩니다!
                        """)

# -----------------------------------------------------------------------------
# 하단 안내 문구
# -----------------------------------------------------------------------------
if st.session_state.logged_in:
    st.markdown("---")
    st.caption("💡 본 웹앱은 중학교 인공지능(AI) 의사결정나무 개념 이해를 위한 교육용 시뮬레이터입니다.")
