import config_data
from rag import RagService
import streamlit as st
#标题
st.title('智能客服')
st.divider()
#用户输入栏
if 'message' not in st.session_state:
    st.session_state['message']=[{'role':'assistant','content':'有什么可以帮助你的吗？'}]
if 'rag' not  in st.session_state:
    st.session_state['rag']=RagService()
for message in st.session_state['message']:
    st.chat_message(message['role']).write(message['content'])
prompt=st.chat_input()
if prompt:
    st.chat_message('user').write(prompt)
    st.session_state['message'].append({'role':'user','content':prompt})

    res_list = []

    with st.spinner('。。。'):
        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
            yield chunk

        res=st.session_state['rag'].chain.stream({'input':prompt},config_data.session_id)
        st.chat_message("assistant").write_stream(capture(res,res_list))
        st.session_state['message'].append({'role':'assistant','content':''.join(res_list)})



