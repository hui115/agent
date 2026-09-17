from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
import config_data
from vector_stores import VectorStoreService
from file_history_store import get_history
class RagService(object):
    def __init__(self):
        self.vector_service=VectorStoreService()
        self.prompt_template=ChatPromptTemplate.from_messages(
            [
                ('system','以我提供的参考资料为主，简洁和专业回答用户问题。参考资料：{context}。并且参照一下的历史对话消息：'),
                MessagesPlaceholder('history'),


                ('user',"请回答我的提问{input}")

            ]
        )
        self.chat_model=ChatTongyi(model=config_data.chat_model_name)
        self.chain=self.__get_chain()
    def __get_chain(self):

        def print_prompt(prompt):
            print("="*20)
            print(prompt.to_string())
            print("="*20)
            return prompt
        def format_document(docs):
            if not  docs:
                return "无相关参考资料"
            formatted_str=''
            for doc in docs:
                formatted_str+=f'文档片段：{doc.page_content}\n文档数据源：{doc.metadata}'
            return formatted_str
        def format_retriever(value:dict):
            return value['input']
        def formar_prompt_template(value:dict):
            new_dict={}
            new_dict['input']=value['input']['input']
            new_dict['history']=value['input']['history']
            new_dict['context']=value['context']
            return new_dict

        retriever=self.vector_service.get_retriever()
        chain=({'input':RunnablePassthrough(),'context':RunnableLambda(format_retriever)|retriever|format_document}
        |RunnableLambda(formar_prompt_template)|self.prompt_template|print_prompt|self.chat_model|StrOutputParser())
        converstaion_chain=RunnableWithMessageHistory(
        chain,
        get_history,
        input_messages_key='input',
        history_messages_key='history'
        )
        return converstaion_chain

if __name__=='__main__':
    session_id={
        'configurable':{
            'session_id':'01'
        }
    }
    res=RagService().chain.invoke({'input':'i am cat'},config=session_id)
    print(res)
