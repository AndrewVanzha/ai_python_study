from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from dotenv import load_dotenv

from openai import OpenAI

import openai
import os


# получим переменные окружения из .env
#load_dotenv()

# API-key
#openai.api_key = os.environ.get("OPENAI_API_KEY")
#openai.api_key = "sk-##################################"

key = 'sk-######################################'
os.environ["OPENAI_API_KEY"] = key
#model = "gpt-3.5-turbo-1106"
#temperature = 0
openai.api_key = key

client = OpenAI(api_key=openai.api_key)

# задаем system
default_system = "Ты-консультант в компании Simble, ответь на вопрос клиента на основе документа с информацией. Не придумывай ничего от себя, отвечай максимально по документу. Не упоминай Документ с информацией для ответа клиенту. Клиент ничего не должен знать про Документ с информацией для ответа клиенту"

    
class Chunk3():

    def __init__(self, path_to_base:str, sep:str=" ", ch_size:int=1024):
        # загружаем базу
        with open(path_to_base, 'r', encoding='utf-8') as file:
            self.document = file.read()
        self.source_chunks = []

    def chunk_list(self, sep:str=" ", ch_size:int=1024):
        # создаем список чанков
        #source_chunks = []
        splitter = CharacterTextSplitter(separator=sep, chunk_size=ch_size)
        for chunk in splitter.split_text(self.document):
            self.source_chunks.append(Document(page_content=chunk, metadata={}))
            #source_chunks.append(Document(page_content=chunk, metadata={}))
        #for ii, chunk in enumerate(self.source_chunks):
        #    print(ii, chunk)
        #print(self.source_chunks[20:])
        return self.source_chunks
        #return source_chunks

    def make_index(self):
        # создаем индексную базу
        embeddings = OpenAIEmbeddings()
        #self.db = FAISS.from_documents(self.source_chunks, embeddings)
        db = FAISS.from_documents(self.source_chunks, embeddings)
        #print(self.db)
        return db

    def get_answer3(self, system:str = default_system, query:str = None):
        #chunk_list()
        # Простая функция получения ответа от chatgpt
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": f"Ответь на вопрос клиента. Не упоминай документ с информацией для ответа клиенту в ответе. Документ с информацией для ответа клиенту: \n\nВопрос клиента: \n{query}"}
        ]

        # получение ответа от chatgpt
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        #completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", # теперь это не работает
        #                                          messages=messages,
        #                                          temperature=0)
        
        #return completion.choices[0].message.content        
        return chat_completion.choices[0].message.content    
