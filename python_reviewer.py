import streamlit as st
import random
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# 환경 변수 로드
load_dotenv()

# 대화형 모델 설정 (기존 chat_model 그대로 사용)
chat_model = ChatOpenAI()

# 페이지 기본 설정
st.set_page_config(page_title="AI 리뷰어 & 로또 생성기", layout="wide")

# 탭 생성
tab1, tab2 = st.tabs(["파이썬 코드리뷰", "로또번호생성"])

with tab1:
    # --- 파이썬 코드 리뷰어 영역 ---
    st.title("🐍 비전공자를 위한 파이썬 코드 리뷰어 & 디버깅 툴")
    st.write("어려운 파이썬 코드, 무엇이든 물어보세요! 코드에 친절한 주석을 달아드리고, 버그가 있다면 쉽게 설명해 드립니다.")
    
    # 모델명 가져오기 (버전 호환성을 위해 getattr 사용)
    model_name = getattr(chat_model, "model_name", getattr(chat_model, "model", "알 수 없음"))
    st.caption(f"💖사용모델명: {model_name}")

    st.subheader("1. 소스 코드 입력")
    # 파일 업로더 (버튼/드래그앤드롭 모두 지원)
    uploaded_file = st.file_uploader("파이썬 파일을 업로드하세요 (최대 200MB, .py 또는 .txt)", type=["py", "txt"])
    
    # 코드 직접 입력 영역
    code_input = st.text_area(
        "또는 여기에 파이썬 소스 코드를 직접 입력하세요:",
        height=200,
        placeholder="def hello_world():\n    print('Hello World!')",
        key="code_input_area"
    )

    # 타겟 코드 설정 및 용량 체크
    target_code = ""
    file_size_error = False
    
    if uploaded_file is not None:
        # 200MB 용량 제한 체크 (200 * 1024 * 1024 bytes)
        if uploaded_file.size > 200 * 1024 * 1024:
            st.error("업로드한 파일이 200MB를 초과했습니다. 200MB 이하의 파일을 업로드해주세요.")
            file_size_error = True
        else:
            try:
                target_code = uploaded_file.read().decode("utf-8")
            except Exception as e:
                st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
                
    # 파일이 업로드 되지 않았거나 비어있을 경우 직접 입력한 코드 사용
    if not target_code and code_input.strip():
        target_code = code_input.strip()

    st.subheader("2. 코드 리뷰 방식 선택")
    col1, col2 = st.columns(2)
    
    with col1:
        btn_summary = st.button("전체코드 총평리뷰", type="primary", use_container_width=True, icon="📝")
    with col2:
        btn_detail = st.button("상세리뷰", type="primary", use_container_width=True, icon="🔍")

    # 세션 상태 초기화
    if "summary_result" not in st.session_state:
        st.session_state.summary_result = ""
    if "detail_result" not in st.session_state:
        st.session_state.detail_result = ""

    # 리뷰 실행 로직
    if btn_summary or btn_detail:
        if file_size_error:
            st.warning("파일 크기 초과 오류를 먼저 해결해주세요.")
        elif not target_code:
            st.warning("먼저 리뷰할 코드를 입력하거나 파일을 업로드해 주세요!")
        else:
            if btn_summary:
                prompt_summary = f"""당신은 프로그래밍을 처음 접하는 비전공자를 위한 친절한 파이썬 코드 리뷰어입니다.
아래 제공된 파이썬 코드에 대해 전체적인 총평을 작성해주세요. 
코드의 목적, 전반적인 구조, 잘된 점, 아쉬운 점 등을 비전공자가 이해하기 쉬운 비유를 들어 간략히 설명해 주세요.

[파이썬 코드]
```python
{target_code}
```
"""
                with st.spinner("전체코드 총평을 작성하는 중입니다... 잠시만 기다려주세요! ⏳"):
                    response = chat_model.invoke([HumanMessage(content=prompt_summary)])
                    st.session_state.summary_result = response.content
                    
            if btn_detail:
                prompt_detail = f"""당신은 프로그래밍을 처음 접하는 비전공자를 위한 아주 친절한 파이썬 코드 리뷰어입니다.
아래 제공된 파이썬 코드를 분석해서 다음 두 가지를 수행해 주세요:

1. **코드 주석 설명**: 비전공자가 이해할 수 있도록, 어려운 전문 용어는 피하고 일상적인 비유를 사용하여 각 줄이나 논리적 블록마다 주석(설명)을 상세히 달아준 전체 코드를 제공해 주세요.
2. **디버깅 및 개선 사항**: 만약 코드에 오류가 발생할 만한 부분이나 비효율적인 부분이 있다면, '🐛 디버깅 및 개선 사항'이라는 제목 아래에 그 이유와 해결 방법을 아주 쉽고 친절하게 설명해 주세요. 코드가 완벽하다면 칭찬과 함께 어떤 점이 좋은지 설명해 주세요.

[파이썬 코드]
```python
{target_code}
```
"""
                with st.spinner("코드를 상세히 리뷰하는 중입니다... 잠시만 기다려주세요! ⏳"):
                    response = chat_model.invoke([HumanMessage(content=prompt_detail)])
                    st.session_state.detail_result = response.content

    # 출력창 분리
    st.subheader("3. 리뷰 결과")
    out_summary, out_detail = st.tabs(["📝 전체코드 총평리뷰", "🔍 상세리뷰"])
    
    with out_summary:
        if st.session_state.summary_result:
            st.markdown(st.session_state.summary_result)
        else:
            st.info("👆 '전체코드 총평리뷰' 버튼을 클릭하면 결과가 여기에 표시됩니다.")
            
    with out_detail:
        if st.session_state.detail_result:
            st.markdown(st.session_state.detail_result)
        else:
            st.info("👆 '상세리뷰' 버튼을 클릭하면 결과가 여기에 표시됩니다.")

with tab2:
    # --- 로또 번호 생성기 영역 ---
    st.title("🎰 로또 번호 생성기")
    st.write("행운의 로또 번호를 5게임 생성합니다.")
    
    # 버튼을 누를 때마다 화면이 리로드되면서 새 번호가 생성됨 (덮어쓰기 효과)
    if st.button("로또 번호 만들기", type="primary", icon="🍀", key="lotto_btn"):
        st.divider()
        st.subheader("🎉 생성된 행운의 번호")
        
        # 현재 시간 표시
        current_time = datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
        st.info(f"⏱️ 생성 시간: {current_time}")
        
        # 로또 공 색상 결정 함수 (한국 로또 기준)
        def get_ball_style(num):
            if num <= 10:
                return "#fbc400", "black", "none"  # 노랑
            elif num <= 20:
                return "#69c8f2", "white", "1px 1px 2px rgba(0,0,0,0.5)" # 파랑
            elif num <= 30:
                return "#ff7272", "white", "1px 1px 2px rgba(0,0,0,0.5)" # 빨강
            elif num <= 40:
                return "#aaaaaa", "white", "1px 1px 2px rgba(0,0,0,0.5)" # 회색
            else:
                return "#b0d840", "white", "1px 1px 2px rgba(0,0,0,0.5)" # 초록

        html_content = ""
        # 5게임 생성
        for i in range(5):
            # 1부터 45까지 중복 없이 6개 숫자 선택 및 정렬
            lotto_numbers = random.sample(range(1, 46), 6)
            lotto_numbers.sort()
            
            balls_html = ""
            for num in lotto_numbers:
                bg_color, text_color, shadow = get_ball_style(num)
                balls_html += f'<div style="display: inline-flex; justify-content: center; align-items: center; width: 45px; height: 45px; border-radius: 50%; background-color: {bg_color}; color: {text_color}; font-weight: bold; font-size: 1.2rem; margin-right: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.2); text-shadow: {shadow};">{num}</div>'
                
            html_content += f'<div style="display: flex; align-items: center; margin-bottom: 15px; padding: 15px; background-color: #ffffff; border: 1px solid #eee; border-radius: 10px; box-shadow: 2px 2px 8px rgba(0,0,0,0.05);"><div style="width: 70px; font-weight: bold; font-size: 1.1rem; color: #555;">{i+1}게임</div>{balls_html}</div>'

        st.markdown(html_content, unsafe_allow_html=True)

# 사용된 프롬프트
# 
# http://192.168.0.34:8599/
# 
# (프롬프트 실행1)
# 현재 파일을 기준으로 내용을 전면 개편할거야. 
# 주제는 비전공자를 위한 파이썬 코드 리뷰어 및 
# 디버깅 툴 만들기. 입력창에 소스 코드를 넣고 
# '코드리뷰하기'버튼을 클릭하면 아래쪽에 코드를 
# 설명하는 주석을 써주고 디버깅 내용이 있으면 
# 그 내용도 표시해 주는 어플리케이션을 만들거야. 
# chat_model을 그대로 사용해.
# 
# (프롬프트 실행2)
# 현재 페이지에서 탭 메뉴를 구분하여 다른 주제를 실행하려고해. 
# python과 streamlit 을 이용해서 로또 생성기 웹 사이트 만들기. 
# 로또 생성된 시간도 나오게 해줘. 기본 로또 번호는 5개 까지 
# 한번에 생성되고 다시 만들기 누르면 새로 5개 덥어쓰기로 생성되게해.
# 그리고 상단 탭 메뉴는 기존에 코드리뷰는 '파이썬 코드리뷰'라고 쓰고
# 지금 것은 '로또번호생성'이라고 구분해줘. 그리고 로또 번호가 생성될때
# 그래픽을 넣어서 공모양으로 나오게 해줘.

# (프롬프트 실행3)
# (위의 2가지 따로 실행후 아래 프롬프트로 추가 수정구현함)
# 파이썬 소스 리뷰 파트에서 파일을 직접 업로드 할 수 있도 추가 수정해. 
# 업로드 방법은 버튼으로 파일열기를 하거나 드래그 앤 드롭 두 가지 방법을 
# 모두 사용할 수 있게해. 그리고 최대 200MB 까지만 업로드 한계 체크해줘. 
# 코드리뷰는 "전체코드 총평리뷰" 와 "상세리뷰" 2가지 버튼을 만들고 
# 출력창도 따로 만들어서 출력되게해. 당연히 직접 올린 코드나 업로드한 
# 코드가 없으면 코드를 넣으라고 메시지를 보여주면돼.
