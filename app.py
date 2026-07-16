# -*- coding: utf-8 -*-
import streamlit as st
from google import genai
import datetime
import random

# --- 1. 페이지 설정 및 나만의 비밀번호 잠금 ---
st.set_page_config(page_title="💪 2307님 전용 AI 헬스 코치", page_icon="🦍", layout="centered")

# 🚨 여기에 형님만의 비밀번호와 아까 발급받은 API 키를 정확히 넣어주세요!
MY_PASSWORD = "1234" 
GEMINI_API_KEY = "AQ.Ab8RN6JraHBCRIdbonQKq6QwdmYaGftFqlJSXTJnxPDoTxhtrQ"

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 나만의 프라이빗 헬스 대시보드")
    pwd = st.text_input("비밀번호를 입력하세요:", type="password")
    if st.button("입장하기"):
        if pwd == MY_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("비밀번호가 틀렸습니다 형님!")
    st.stop()

# --- 2. 웹페이지 헤더 ---
st.title("🦍 2307님 전용 AI 헬스 대시보드")
st.caption("내년 여름 65kg / 체지방 12% 마스터 플랜 가동 중 🔥")

# --- 3. 오늘의 운동 루틴 선택 (동적 변경을 위해 Form 밖에 배치) ---
workout_type = st.selectbox(
    "오늘의 운동 루틴을 선택하세요 🔥",
    [
        "A (가슴/등/복근)", 
        "B (어깨/이두/삼두)", 
        "C (어깨/이두)", 
        "D (휴식)"
    ]
)

# --- 4. 간편 데이터 입력 폼 ---
with st.form("gym_record_form"):
    st.subheader("📝 오늘의 데이터 입력")
    
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("날짜", datetime.date.today())
        weight = st.number_input("오늘 공복 체중 (kg)", value=63.2, step=0.1)
    with col2:
        protein_g = st.number_input("오늘 총 단백질 섭취량 (g)", value=120, step=10)
        
    st.markdown("---")
    
    # 각 루틴별 운동 매핑 (축약어 정식 명칭으로 변경 완료!)
    exercises = []
    rest_quote = ""
    
    if "A" in workout_type:
        st.write("### 🏋️‍♂️ [A 루틴] 가슴 / 등 / 복근")
        exercises = [
            "어시스트 풀업", "딥스", "덤벨 풀오버", 
            "벤치프레스", "랫풀다운", "인클라인 덤벨프레스", "케이블 시티드 로우"
        ]
    elif "B" in workout_type:
        st.write("### 🏋️‍♂️ [B 루틴] 어깨 / 이두 / 삼두")
        exercises = [
            "오버헤드 프레스 (OHP)", "사이드 레터럴 레이즈 (사레레)", "리버스 팩덱플라이", 
            "케이블 푸쉬다운", "바벨컬", "인클라인 덤벨컬", "오버헤드 익스텐션"
        ]
    elif "C" in workout_type:
        st.write("### 🏋️‍♂️ [C 루틴] 어깨 / 이두")
        exercises = [
            "케이블 리어 델트 풀", "리버스 팩덱플라이", "시팅 사이드 레터럴 레이즈 (시팅 사레레)", 
            "오버헤드 프레스 (OHP)", "덤벨 숄더프레스", "사이드 레터럴 레이즈 (사레레)", 
            "케이블 사이드 레터럴 레이즈", "바벨컬", "해머컬"
        ]
    elif "D" in workout_type:
        st.write("### 🧘‍♂️ [D 루틴] 오늘의 휴식")
        # 휴식에 관한 명언 목록
        quotes = [
            "“휴식은 게으름이 아니며, 여름날 잔디밭에 누워 물소리를 듣거나 하늘을 떠다니는 구름을 바라보는 것은 결코 시간 낭비가 아니다.” — 존 러벅",
            "“일만 하고 휴식을 모르는 사람은 브레이크가 없는 자동차와 같이 위험하다.” — 헨리 포드",
            "“잘 쉬는 것이 잘 일하는 것이다. 근육은 운동할 때가 아니라 쉴 때 자란다 형님!” — AI 헬스코치",
            "“진정한 휴식은 단순히 아무것도 하지 않는 것이 아니라, 다음 성장을 위한 에너지를 채우는 시간이다.”",
            "“가장 거친 폭풍 뒤에 가장 달콤한 휴식이 찾아온다. 오늘 푹 쉬고 다음 쇠질을 찢자!”"
        ]
        rest_quote = random.choice(quotes)
        st.info(rest_quote)

    # 🆕 운동별 중량, 단위(kg/lbs), 세트, 횟수 동적 입력창 생성
    workout_records = {}
    if exercises:
        for ex in exercises:
            st.markdown(f"**🔹 {ex}**")
            # 가로로 깔끔하게 배치하기 위한 컬럼 설정
            ec1, ec2, ec3, ec4 = st.columns([3, 2, 2, 2])
            with ec1:
                w = st.number_input("중량", min_value=0.0, value=0.0, step=2.5, key=f"{ex}_w")
            with ec2:
                u = st.selectbox("단위", ["kg", "lbs"], index=0, key=f"{ex}_u")
            with ec3:
                s = st.number_input("세트", min_value=0, value=0, step=1, key=f"{ex}_s")
            with ec4:
                r = st.number_input("횟수", min_value=0, value=0, step=1, key=f"{ex}_r")
            
            # 세트와 횟수가 모두 1 이상 입력된 경우에만 기록에 포함
            if s > 0 and r > 0:
                workout_records[ex] = {"weight": w, "unit": u, "sets": s, "reps": r}
                
    st.markdown("---")
    diet_memo = st.text_area("오늘 식단 및 컨디션 메모", placeholder="예: 점심 잡곡밥 반공기에 만두, 저녁 닭가슴살 2팩. 어깨 근육통 맛있음.")
    
    submit_btn = st.form_submit_button("🔥 AI 코치에게 분석 피드백 받기")

# --- 5. AI 코치 프롬프트 및 분석 엔진 ---
if submit_btn:
    with st.spinner("AI 코치가 형님의 데이터를 분석하고 있습니다... 💪"):
        try:
            # API 키 양끝 공백 제거 처리로 에러 방지
            client = genai.Client(api_key=GEMINI_API_KEY.strip())
            
            # 형님의 역사와 SOP가 완벽하게 각인된 시스템 프롬프트
            system_context = """
            당신은 사용자의 전용 일대일 헬스/영양 AI 코치입니다. 무조건 열정적이고 유쾌하며 뼈 때리는 팩트 폭격으로 조언합니다.
            
            [사용자 기본 정보 및 역사]
            - 목표: 2027년 여름 65kg / 체지방률 12% 달성 (현재는 체중 유지하며 체지방 13%까지 걷어내는 린매스업 Phase 1)
            - 최근 인바디(26년 7월): 체중 63.2kg, 골격근 30.2kg(+0.7kg 떡상!), 체지방률 15.1%(-2.8% 떡락!)
            - 과거 역사: 1년 반 전 캐나다 시절 체중 59kg에 벤치 125lbs를 들던 '머슬 메모리'가 현재 미친 듯이 부활 중.
            - 평일 SOP: 04:40 기상, 아침/오후 프로틴 철벽 방어(하루 목표 120g), 점심 구내식당 밥 반공기 고정, 저녁 수지스 닭가슴살 2팩. 하루 6천보 통근.
            - 주의사항: 수요일과 일요일은 '완전 휴식일'이라 운동이나 스트레칭 무리하게 하지 말고 클린하게 먹고 푹 쉬어야 함.
            """
            
            # 운동 기록 텍스트화
            record_lines = []
            if "D" in workout_type:
                record_lines.append("오늘은 공식 휴식일입니다!")
                record_lines.append(f"휴식 명언: {rest_quote}")
            else:
                if workout_records:
                    for ex, details in workout_records.items():
                        record_lines.append(f"- {ex}: {details['weight']}{details['unit']} x {details['sets']}세트 x {details['reps']}회")
                else:
                    record_lines.append("수행한 운동 기록이 입력되지 않았습니다.")
            
            workout_record_str = "\n".join(record_lines)
            
            user_prompt = f"""
            [오늘의 입력 데이터 - {date}]
            - 공복 체중: {weight} kg
            - 오늘의 루틴: {workout_type}
            - 상세 운동 기록:
            {workout_record_str}
            - 하루 단백질: {protein_g} g
            - 식단/컨디션 메모: {diet_memo}
            
            위 데이터를 바탕으로 형님(사용자)에게 오늘의 운동/중량 변화 분석, 식단 및 단백질 방어 여부, 내일 행동 지침을 3가지 포인트로 나누어 아주 찰지고 든든하게 피드백 해줘! 
            만약 휴식일(D 루틴)인 경우, 영양 섭취와 컨디션 회복의 중요성을 강조하며 내일 쇠질을 찢기 위한 에너지를 충전할 수 있게 격려해줘!
            """
            
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[system_context, user_prompt]
            )
            
            st.success("💪 AI 코치의 분석 리포트 도착!")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"에러가 발생했습니다 형님! API 키와 파일 인코딩을 다시 확인해 주세요: {e}")
