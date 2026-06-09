# Streamlit 라이브러리 임포트 (웹 애플리케이션 UI 구성)
import streamlit as st
# LangChain 라이브러리에서 로컬 LLM을 사용하기 위한 CTransformers 임포트
from langchain_community.llms import CTransformers
# 프롬프트 템플릿 생성을 위한 모듈 임포트
from langchain_core.prompts import ChatPromptTemplate
# LLM의 출력 결과를 문자열로 파싱하기 위한 모듈 임포트
from langchain_core.output_parsers import StrOutputParser

# Streamlit의 캐싱 데코레이터. 모델을 한 번만 로드하여 메모리에 유지 (성능 최적화 및 로딩 시간 단축)
@st.cache_resource
def get_llm():
    """Initializes and returns the CTransformers LLM."""
    # Llama 2 모델(양자화된 ggml 파일)을 로드하여 반환
    return CTransformers(
        model="llama-2-7b-chat.ggmlv3.q2_K.bin",
        model_type="llama"
    )

# 웹 페이지의 메인 타이틀 설정
st.title('인공지능 시인')

# CSS 스타일을 추가하여 input 박스의 가로크기, 글자크기, 글자색 변경
st.markdown(
    """
    <style>
    div[data-testid="stTextInput"] div[data-baseweb="input"] {
        width: 600px !important;
    }
    div[data-testid="stTextInput"] input {
        font-size: 20px !important;
        color: hotpink !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 사용자로부터 텍스트 입력을 받는 입력란 생성
content = st.text_input('시의 주제를 제시해주세요.',
                         placeholder='주제를 영어로 넣어주세요.(예: love, nature, etc.)')  # 입력란의 너비를 100%로 설정하여 화면 전체에 걸쳐 표시

# '시 작성 요청하기' 버튼 생성 및 클릭 이벤트 처리
if st.button('시 작성 요청하기'):
    # 사용자가 주제를 입력하지 않은 경우 경고 메시지 출력
    if not content:
        st.warning('시의 주제를 제시해주세요.')
    # 사용자가 주제를 입력한 경우
    else:
        # 모델이 응답을 생성하는 동안 사용자에게 로딩 상태(스피너) 표시
        with st.spinner('시 작성 중...'):
            # 미리 로드해둔 LLM 객체 가져오기
            llm = get_llm()
            # 사용자가 입력한 주제를 {topic}에 넣을 수 있도록 프롬프트 템플릿 생성
            prompt = ChatPromptTemplate.from_template("write a poem about {topic}")
            # 프롬프트, LLM, 출력 파서를 연결하여 처리 체인(Chain) 생성 (LangChain Expression Language 사용)
            chain = prompt | llm | StrOutputParser()
            # 체인을 실행하고(invoke) 사용자 입력 값을 전달하여 결과 텍스트(시) 생성
            result = chain.invoke({"topic": content})
            # 생성된 시를 화면에 출력
            st.write(result)
