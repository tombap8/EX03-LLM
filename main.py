import streamlit as st
from dotenv import load_dotenv
# from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage# , AIMessage

load_dotenv()

# 텍스트 완성 모델: 단순 문자열을 입력받아 이어지는 텍스트를 예측하여 반환합니다.
# llm = OpenAI()
# 대화형 모델: 메시지 리스트를 입력받아 대화의 다음 메시지를 반환합니다.
chat_model = ChatOpenAI()
st.write("💖사용모델명:"+chat_model.model)

st.title("디지털 글쓰기")
txt = st.text_area(
    "LLM에게 질문 내용:",
)

st.write(f"You wrote {len(txt)} characters.")

if st.button("질문하기",type="secondary",icon="🔍"):
    if txt:
        st.write("LLM에게 질문 내용:")
        st.write(txt)
        
        st.write("LLM Response:")
        with st.spinner("답변을 기다리는 중...", show_time=True):
            llm_response = chat_model.invoke([HumanMessage(content=txt)])
        st.write(llm_response.content)
    else:
        st.warning("질문 내용을 입력해주세요.")

# st.title("_Streamlit_ is :blue[cool] :sunglasses: :heart_eyes: :star_struck: :fire: :rocket:")

# question1 = input("LLM에게 할 질문을 입력하세요: ")

# print("LLM에게 질문 내용:")
# print(question1)

# print("LLM Response:")
# llm_response = llm.invoke(question1)
# # invoke(): 모델에 입력값(프롬프트)을 전달하여 
# # 실행(호출)하고 결과를 동기적으로 받아오는 메서드입니다.
# print(llm_response)

# print("\n=== Chat Model 연속 대화 시작 (종료하려면 '종료' 또는 'exit' 입력) ===")

# chat_history = [] # 대화 문맥을 유지하기 위한 리스트

# while True:
#     question2 = input("\nChat Model에게 할 질문을 입력하세요: ")
#     if question2.strip().lower() in ['종료', 'exit', 'quit']:
#         print("대화를 종료합니다.")
#         break

#     # 1. 사용자의 질문을 대화 기록에 추가
#     chat_history.append(HumanMessage(content=question2))
    
#     # 2. 전체 대화 기록을 모델에 전달하여 문맥을 이해하고 답변하도록 함
#     chat_response = chat_model.invoke(chat_history)
#     # invoke(): 리스트 형태의 대화 기록(메시지 객체들)을 모델에 
#     # 전달하여 응답을 받아옵니다. 여기서도 모델의 실행을 트리거하는 역할을 합니다.
    
#     print("\nChat Model Response:")
#     print(chat_response.content)
#     # content 속성은 AIMessage 객체에서 실제 텍스트 응답을 가져오는 데 사용됩니다.
    
#     # 3. AI의 답변을 대화 기록에 추가하여 다음 질문 시 문맥 유지
#     chat_history.append(AIMessage(content=chat_response.content))

# print("마지막라인이야!~~~~~")
