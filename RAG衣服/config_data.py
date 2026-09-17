from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

md5_path = str(PROJECT_ROOT / "md5.text")
persist_directory = str(PROJECT_ROOT / "chorma_db")
history_storage = str(PROJECT_ROOT / "history_storage")

collection_name='rag'


chunk_size=1000
chunk_overlap=100
separators=['\n\n','\n',',','.','.','?','!','，','。','？','！']
max_split_number=1000



similarity_threshold=1



chat_model_name='qwen3-max'

session_id = {
    'configurable': {
        'session_id': '01'
    }
}