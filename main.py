import streamlit as st
from langchain.memory import ConversationBufferMemory
from GPT_cloned import get_chat_response
st.title("QPT-PLUS")
st.write("**这是一款AI助手**")
#设置侧边栏，用户输入密钥
with st.sidebar:
    openai_api_key = st.text_input("请输入API密钥：", type="password")
    if openai_api_key[0:3] == "sk-":
        if st.button("确认"):
            st.write("成功")
        st.divider()
        AI_choice = st.selectbox(label="请选择AI版本",
                                 options=("GPT3", "GPT4", "GPT4o"),
                                 format_func=str,
                                 help="请选择AI版本，以便帮助您更好的完成工作，通常数字越高版本越高，性能也就越好,相对应的收费也会越高")
        # 根据选择的AI版本设置模型
        choice = {
            "GPT3": "gpt-3.5-turbo",
            "GPT4": "gpt-4",
            "GPT4o": "gpt-4o-mini",
        }.get(AI_choice, "gpt-3.5-turbo")
    else:
        st.stop()
#初始化对话框
if "memory" not in st.session_state:
    st.session_state = {}
    st.session_state["memory"] = ConversationBufferMemory(return_message = True)
    st.session_state["messages"] = [{"role":"ai",
                                    "content":"你好，我是QPT，有什么可以帮助你的吗？"}]
#实时将对话加载到历史消息中
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])
#用户输入实例
prompt = st.chat_input()
if prompt:
    if not openai_api_key:
        st.info("请输入你的API")
        st.stop()
    st.session_state["messages"].append({"role":"human","content":prompt})
    st.chat_message("human").write(prompt)
    with st.spinner("AI正在思考中，请稍等..."):
        response = get_chat_response(prompt, st.session_state["memory"],choice,openai_api_key)
    msg = {"role":"ai","content":response}
    st.session_state["messages"].append(msg)
    st.chat_message("ai").write(response)
