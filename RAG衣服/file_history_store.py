import json
import os.path
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, messages_from_dict, message_to_dict
from collections.abc import Sequence

import config_data


def get_history(session_id):
    return FileChatMessageHistory(session_id,config_data.history_storage)



class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,storage_path):
        self.session_id=session_id
        self.storage_path=storage_path
        self.file_path=os.path.join( self.storage_path,f"{self.session_id}.json")
        os.makedirs(self.storage_path, exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages=list(self.messages)
        all_messages.extend(messages)
        new_messages=[message_to_dict(message)  for message in all_messages]
        os.makedirs(self.storage_path, exist_ok=True)
        with open(self.file_path,'w',encoding='utf-8') as f:
            json.dump(new_messages,f,ensure_ascii=False)

    @property
    def messages(self)->list[BaseMessage]:
        try:
            with open(self.file_path,'r',encoding='utf-8') as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except (FileNotFoundError, json.JSONDecodeError):
            return  []
    def clear(self) -> None:
        os.makedirs(self.storage_path, exist_ok=True)
        with open(self.file_path,'w',encoding='utf-8') as f:
            json.dump([],f,ensure_ascii=False)
